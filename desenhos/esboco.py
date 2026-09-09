# -*- coding: utf-8 -*-
"""
ESBOCO A MAO LIVRE - representacao inicial do produto
Item D | Projeto de Produto e Processo | Poli-USP

RODAR:  python desenhos/esboco.py

SAIDA (em desenhos/):
    esboco.svg          folha inteira, para olhar no navegador
    esboco.pdf          folha inteira, para \\includegraphics no LaTeX
    fig-planta.pdf      cada vista sozinha, com sua propria legenda
    fig-frontal.pdf
    fig-lateral.pdf
    fig-perspectiva.pdf
    fig-detalhe.pdf
    preview.html
    incluir.tex         trecho pronto para colar no Overleaf

DUAS COISAS QUE ESTE SCRIPT FAZ E VALE SABER
--------------------------------------------
1. Os ROTULOS SE POSICIONAM SOZINHOS. Voce so diz "anote este ponto com
   este texto"; o script separa os rotulos em duas colunas (esquerda e
   direita), ordena por altura e distribui sem sobreposicao, puxando a
   linha de chamada ate cada um. E' o que impede o desenho de virar um
   amontoado de setas cruzadas.

2. As COTAS VEM DO CAD. Nenhuma medida esta digitada aqui - todas sao
   lidas de fusion/Antifurto.py. Mudou a carcaca la, o esboco acompanha.

Sem dependencia externa: so a biblioteca padrao. O PDF e' escrito na mao.
"""

import io
import os
import re
import math
import zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FONTE_CAD = os.path.join(RAIZ, 'fusion', 'Antifurto.py')

TINTA, COTA, CENTRO = (0.10, 0.10, 0.10), (0.11, 0.44, 0.65), (0.60, 0.63, 0.65)
DESTAQ, VERDE = (0.71, 0.20, 0.12), (0.18, 0.42, 0.27)
CINZA, MOLDURA = (0.52, 0.52, 0.52), (0.79, 0.77, 0.72)
PAPEL = (0.988, 0.984, 0.969)


def hexcor(c):
    return '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in c)


# ============================================================================
# PARAMETROS, LIDOS DO CAD
# ============================================================================

def _bloco(src, nome):
    m = re.search(r'^%s\s*=\s*\{' % nome, src, re.M)
    if not m:
        return None
    i = src.index('{', m.start())
    prof, j = 0, i
    while j < len(src):
        if src[j] == '{':
            prof += 1
        elif src[j] == '}':
            prof -= 1
            if prof == 0:
                return src[m.start():j + 1]
        j += 1
    return None


def parametros():
    """Le os parametros de Antifurto.py. A ordem importa: XY_ATUADOR depende
    de XY_GARRA, de MEC e de Y_FRENTE_CURSOR, entao os escalares vem antes."""
    src = io.open(FONTE_CAD, encoding='utf-8').read()
    ns = {'math': math}
    for nome in ('MM', 'MU', 'MECANISMO', 'XY_GARRA'):
        m = re.search(r'^%s\s*= .*$' % nome, src, re.M)
        if m:
            exec(m.group(0), ns)
    for nome in ('P', 'PAR', 'GARRA', 'PINO', 'TECIDO', 'CUR', 'BUCHA',
                 'UI', 'COMP', 'POS', 'MEC'):
        b = _bloco(src, nome)
        if not b:
            raise SystemExit('nao achei o bloco %s' % nome)
        exec(b, ns)
    for nome in ('FUROS', 'Y_FRENTE_CURSOR'):
        m = re.search(r'^%s\s*= .*$' % nome, src, re.M)
        if m:
            exec(m.group(0), ns)
    b = _bloco(src, 'XY_ATUADOR')
    if b:
        exec(b, ns)
    return ns


# ============================================================================
# TELA - guarda primitivas e depois emite SVG ou PDF
# ============================================================================

LARG_CHAR = 0.50    # largura media de caractere, em fracao do corpo


def larg_txt(s, tam):
    return len(s) * tam * LARG_CHAR


class Tela:
    def __init__(self, w, h, semente=20260909):
        self.w, self.h = w, h
        self.s = semente
        self.prims = []

    # ---- ruido reprodutivel ----
    def _r(self):
        self.s = (1103515245 * self.s + 12345) % 2147483648
        return self.s / 2147483648.0

    def _n(self, a):
        return (self._r() - 0.5) * 2.0 * a

    def _tremido(self, pts, amp, passo=11.0):
        r = []
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            d = math.hypot(x2 - x1, y2 - y1)
            n = max(2, int(d / passo))
            for k in range(n):
                t = k / float(n)
                w = math.sin(math.pi * t) ** 0.6
                r.append((x1 + (x2 - x1) * t + self._n(amp) * w,
                          y1 + (y2 - y1) * t + self._n(amp) * w))
        r.append(pts[-1])
        return r

    # ---- primitivas ----
    def path(self, pts, cor=TINTA, larg=1.6, fechar=False, duplo=True,
             fill=None, op=1.0, tracejado=None, amp=1.0):
        if fechar:
            pts = list(pts) + [pts[0]]
        for i in range(2 if duplo else 1):
            self.prims.append(('p', self._tremido(pts, amp if i == 0 else amp * 1.5),
                               cor, larg if i == 0 else larg * 0.5,
                               fill if i == 0 else None,
                               op if i == 0 else op * 0.4, tracejado))

    def reta(self, x1, y1, x2, y2, **k):
        self.path([(x1, y1), (x2, y2)], **k)

    def ret(self, x, y, w, h, **k):
        self.path([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fechar=True, **k)

    def circ(self, cx, cy, r, **k):
        n = max(16, int(r * 1.2))
        self.path([(cx + r * math.cos(2 * math.pi * i / n),
                    cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
                  fechar=True, **k)

    def txt(self, x, y, s, tam=12.0, cor=TINTA, anc='start', peso='normal'):
        self.prims.append(('t', x, y, s, tam, cor, anc, peso))

    def seta(self, x, y, ang, tam=6.5, cor=TINTA, larg=1.0):
        for k in (+1, -1):
            self.reta(x, y, x - tam * math.cos(ang + k * 0.4),
                      y - tam * math.sin(ang + k * 0.4),
                      cor=cor, larg=larg, duplo=False, amp=0.3)

    def flecha(self, x1, y1, x2, y2, cor=TINTA, larg=1.4, tam=7.0):
        self.reta(x1, y1, x2, y2, cor=cor, larg=larg, duplo=False, amp=0.6)
        self.seta(x2, y2, math.atan2(y2 - y1, x2 - x1), tam, cor, larg)

    def hach(self, pts, passo=8.0, cor=CINZA, larg=0.8):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        d = (0.7071, 0.7071)
        t = -(x1 - x0) - (y1 - y0)
        while t < (x1 - x0) + (y1 - y0):
            seg = self._corta(pts, (x0 + t, y0), d)
            if seg:
                self.path(list(seg), cor=cor, larg=larg, duplo=False, op=0.5, amp=0.5)
            t += passo

    def _corta(self, poly, p0, d):
        ts, n = [], len(poly)
        for i in range(n):
            ax, ay = poly[i]
            bx, by = poly[(i + 1) % n]
            ex, ey = bx - ax, by - ay
            den = d[0] * ey - d[1] * ex
            if abs(den) < 1e-9:
                continue
            s = ((ax - p0[0]) * ey - (ay - p0[1]) * ex) / den
            u = ((ax - p0[0]) * d[1] - (ay - p0[1]) * d[0]) / -den
            if -1e-9 <= u <= 1 + 1e-9:
                ts.append(s)
        if len(ts) < 2:
            return None
        a, b = min(ts), max(ts)
        if b - a < 2:
            return None
        return ((p0[0] + d[0] * a, p0[1] + d[1] * a),
                (p0[0] + d[0] * b, p0[1] + d[1] * b))

    # ---- saida ----
    def svg(self):
        out = ['<rect width="%d" height="%d" fill="%s"/>' % (self.w, self.h, hexcor(PAPEL))]
        for pr in self.prims:
            if pr[0] == 'p':
                _, pts, cor, larg, fill, op, tr = pr
                d = 'M ' + ' L '.join('%.1f %.1f' % p for p in pts)
                dash = ' stroke-dasharray="%s"' % tr if tr else ''
                out.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f"%s '
                           'stroke-linecap="round" stroke-linejoin="round" '
                           'opacity="%.2f"/>'
                           % (d, hexcor(fill) if fill else 'none', hexcor(cor),
                              larg, dash, op))
            else:
                _, x, y, s, tam, cor, anc, peso = pr
                out.append('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" '
                           'text-anchor="%s" font-weight="%s" font-family="Segoe Print, '
                           'Bradley Hand, Comic Sans MS, Chalkboard, cursive">%s</text>'
                           % (x, y, tam, hexcor(cor), anc, peso, _esc(s)))
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                'viewBox="0 0 %d %d">%s</svg>'
                % (self.w, self.h, self.w, self.h, ''.join(out)))

    def pdf(self):
        """PDF minimo, escrito na mao. Tracado igual; texto em Helvetica-Oblique,
        que e' base-14 e nao precisa ser embutido."""
        W, H = self.w, self.h
        c = ['%.3f %.3f %.3f rg 0 0 %d %d re f' % (PAPEL + (W, H))]
        c.append('1 J 1 j')
        for pr in self.prims:
            if pr[0] == 'p':
                _, pts, cor, larg, fill, op, tr = pr
                c.append('q')
                if op < 0.999:
                    # so existem os estados de 10 em 10; arredondar para o
                    # mais proximo, senao o PDF referencia recurso inexistente
                    c.append('/GS%d gs' % max(10, min(90, int(round(op * 10)) * 10)))
                c.append('%.3f %.3f %.3f RG %.2f w' % (cor + (larg,)))
                if tr:
                    c.append('[%s] 0 d' % tr.replace(' ', ' '))
                if fill:
                    c.append('%.3f %.3f %.3f rg' % fill)
                c.append('%.2f %.2f m ' % (pts[0][0], H - pts[0][1])
                         + ' '.join('%.2f %.2f l' % (p[0], H - p[1]) for p in pts[1:]))
                c.append('B' if fill else 'S')
                c.append('Q')
            else:
                _, x, y, s, tam, cor, anc, peso = pr
                w = larg_txt(s, tam)
                px = x - w if anc == 'end' else (x - w / 2 if anc == 'middle' else x)
                fonte = 'F2' if peso == 'bold' else 'F1'
                c.append('q %.3f %.3f %.3f rg BT /%s %.1f Tf %.2f %.2f Td (%s) Tj ET Q'
                         % (cor + (fonte, tam, px, H - y, _pdftxt(s))))
        stream = zlib.compress(('\n'.join(c)).encode('latin-1', 'replace'))

        objs = []
        objs.append('<</Type/Catalog/Pages 2 0 R>>')
        objs.append('<</Type/Pages/Kids[3 0 R]/Count 1>>')
        gs = ' '.join('/GS%d %d 0 R' % (i, 7 + n) for n, i in enumerate(range(10, 100, 10)))
        objs.append('<</Type/Page/Parent 2 0 R/MediaBox[0 0 %d %d]/Resources<</Font<</F1 '
                    '5 0 R/F2 6 0 R>>/ExtGState<<%s>>>>/Contents 4 0 R>>' % (W, H, gs))
        objs.append(('<</Length %d/Filter/FlateDecode>>' % len(stream), stream))
        objs.append('<</Type/Font/Subtype/Type1/BaseFont/Helvetica-Oblique>>')
        objs.append('<</Type/Font/Subtype/Type1/BaseFont/Helvetica-BoldOblique>>')
        for i in range(10, 100, 10):
            objs.append('<</Type/ExtGState/ca %.2f/CA %.2f>>' % (i / 100.0, i / 100.0))

        buf = bytearray(b'%PDF-1.4\n')
        pos = []
        for i, o in enumerate(objs, 1):
            pos.append(len(buf))
            if isinstance(o, tuple):
                buf += ('%d 0 obj\n%s\nstream\n' % (i, o[0])).encode('latin-1')
                buf += o[1] + b'\nendstream\nendobj\n'
            else:
                buf += ('%d 0 obj\n%s\nendobj\n' % (i, o)).encode('latin-1')
        xref = len(buf)
        buf += ('xref\n0 %d\n0000000000 65535 f \n' % (len(objs) + 1)).encode()
        for p in pos:
            buf += ('%010d 00000 n \n' % p).encode()
        buf += ('trailer\n<</Size %d/Root 1 0 R>>\nstartxref\n%d\n%%%%EOF\n'
                % (len(objs) + 1, xref)).encode()
        return bytes(buf)


def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _pdftxt(s):
    s = (s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)'))
    return s.encode('latin-1', 'replace').decode('latin-1')


# ============================================================================
# QUADRO - vista com origem e escala proprias, em mm, e rotulos automaticos
# ============================================================================

class Quadro:
    def __init__(self, T, x, y, w, h, titulo, cy_mm=0.0, esc=1.0, oy=0.5,
                 col_esq=112, col_dir=112):
        self.T, self.x, self.y, self.w, self.h = T, x, y, w, h
        self.esc, self.cy_mm = esc, cy_mm
        self.col_esq, self.col_dir = col_esq, col_dir
        # a area de desenho fica entre as duas colunas de rotulo
        self.dx0 = x + col_esq
        self.dx1 = x + w - col_dir
        self.px = (self.dx0 + self.dx1) / 2.0
        self.py = y + h * oy
        self.notas = []
        self.marcas = []
        T.ret(x, y, w, h, cor=MOLDURA, larg=1.1, duplo=False, amp=0.5)
        T.txt(x + 14, y + 24, titulo, tam=14, peso='bold')
        T.reta(x + 14, y + 31, x + 14 + larg_txt(titulo, 14), y + 31,
               cor=(0.85, 0.65, 0.13), larg=2.2, duplo=False, amp=0.5)

    def p(self, xm, ym):
        px = self.px + xm * self.esc
        py = self.py - (ym - self.cy_mm) * self.esc
        self.marcas.append((px, py))
        return px, py

    def reg(self, px, py):
        self.marcas.append((px, py))
        return px, py

    # ---- rotulos automaticos ----
    def nota(self, xm, ym, texto, lado=None, cor=TINTA):
        """Anota um ponto. A posicao do texto e' resolvida depois, em coluna."""
        px, py = self.p(xm, ym)
        if lado is None:
            lado = 'dir' if px >= self.px else 'esq'
        self.notas.append([px, py, texto, cor, lado])

    def resolver(self, topo=None, base=None, passo=17.0):
        """Distribui os rotulos em duas colunas, sem sobreposicao, mantendo
        a ordem vertical dos pontos anotados."""
        T = self.T
        y0 = topo if topo is not None else self.y + 46
        y1 = base if base is not None else self.y + self.h - 12
        for lado in ('esq', 'dir'):
            itens = [n for n in self.notas if n[4] == lado]
            if not itens:
                continue
            itens.sort(key=lambda n: n[1])
            n = len(itens)
            alt = min(passo, (y1 - y0) / n) if n > 1 else 0
            alt = max(alt, 15.0)
            total = alt * (n - 1)
            centro = sum(i[1] for i in itens) / float(n)
            ini = min(max(centro - total / 2.0, y0), y1 - total)
            for k, (px, py, txt, cor, _) in enumerate(itens):
                ly = ini + k * alt
                if lado == 'esq':
                    lx = self.x + 10
                    anc, ponta = 'start', lx + larg_txt(txt, 11.5) + 5
                else:
                    lx = self.x + self.w - 10
                    anc, ponta = 'end', lx - larg_txt(txt, 11.5) - 5
                T.circ(px, py, 1.9, cor=CINZA, larg=0.8, duplo=False)
                T.path([(px, py), (ponta, ly - 3)], cor=CINZA, larg=0.8,
                       duplo=False, op=0.85, amp=0.6)
                T.txt(lx, ly, txt, tam=11.5, cor=cor, anc=anc)
                self.reg(lx if anc == 'start' else lx - larg_txt(txt, 11.5), ly - 11)
                self.reg(lx + larg_txt(txt, 11.5) if anc == 'start' else lx, ly + 3)
        self.notas = []

    def vazou(self, folga=6.0):
        if not self.marcas:
            return None
        xs = [m[0] for m in self.marcas]
        ys = [m[1] for m in self.marcas]
        v = []
        if min(xs) < self.x + folga:
            v.append('esq %.0f' % (self.x + folga - min(xs)))
        if max(xs) > self.x + self.w - folga:
            v.append('dir %.0f' % (max(xs) - self.x - self.w + folga))
        if min(ys) < self.y + 36:
            v.append('topo %.0f' % (self.y + 36 - min(ys)))
        if max(ys) > self.y + self.h - folga:
            v.append('baixo %.0f' % (max(ys) - self.y - self.h + folga))
        return ', '.join(v) if v else None

    # ---- cotas ----
    def cota_h(self, x1m, x2m, ym, rot, fora=24.0):
        T = self.T
        a, b = self.p(x1m, ym), self.p(x2m, ym)
        yl = a[1] - fora
        s = 1 if fora > 0 else -1
        self.reg(a[0], yl); self.reg(b[0], yl)
        for px in (a[0], b[0]):
            T.reta(px, a[1] - 4 * s, px, yl - 4 * s, cor=COTA, larg=0.7,
                   duplo=False, op=0.7, amp=0.3)
        T.reta(a[0], yl, b[0], yl, cor=COTA, larg=1.0, duplo=False, amp=0.45)
        T.seta(a[0], yl, math.pi, 6.0, COTA, 1.0)
        T.seta(b[0], yl, 0.0, 6.0, COTA, 1.0)
        ty = yl - 6 if fora > 0 else yl + 14
        T.txt((a[0] + b[0]) / 2, ty, rot, tam=11.5, cor=COTA, anc='middle')
        self.reg((a[0] + b[0]) / 2, ty - 11)

    def cota_v(self, y1m, y2m, xm, rot, fora=24.0):
        T = self.T
        a, b = self.p(xm, y1m), self.p(xm, y2m)
        xl = a[0] + fora
        s = 1 if fora > 0 else -1
        self.reg(xl, a[1]); self.reg(xl, b[1])
        for py in (a[1], b[1]):
            T.reta(a[0] + 4 * s, py, xl + 4 * s, py, cor=COTA, larg=0.7,
                   duplo=False, op=0.7, amp=0.3)
        T.reta(xl, a[1], xl, b[1], cor=COTA, larg=1.0, duplo=False, amp=0.45)
        T.seta(xl, a[1], math.pi / 2, 6.0, COTA, 1.0)
        T.seta(xl, b[1], -math.pi / 2, 6.0, COTA, 1.0)
        tx = xl + 6 * s
        T.txt(tx, (a[1] + b[1]) / 2 + 4, rot, tam=11.5, cor=COTA,
              anc='start' if s > 0 else 'end')
        self.reg(tx + (larg_txt(rot, 11.5) if s > 0 else -larg_txt(rot, 11.5)),
                 (a[1] + b[1]) / 2)


# ============================================================================
# VISTAS
# ============================================================================

def planta(Q, ns):
    T, P, UI, FUROS, PAR = Q.T, ns['P'], ns['UI'], ns['FUROS'], ns['PAR']
    a, b = P['larg'] / 2, P['prof'] / 2
    T.path([Q.p(-a, -b), Q.p(a, -b), Q.p(a, b), Q.p(-a, b)], fechar=True, larg=2.0)
    T.path([Q.p(-a + 2.4, -b + 2.4), Q.p(a - 2.4, -b + 2.4),
            Q.p(a - 2.4, b - 2.4), Q.p(-a + 2.4, b - 2.4)],
           fechar=True, cor=(0.66, 0.66, 0.66), larg=0.8, duplo=False)
    T.reta(*(Q.p(-a - 6, 0) + Q.p(a + 6, 0)), cor=CENTRO, larg=0.9,
           duplo=False, tracejado='11 4 2 4', amp=0.3)
    T.reta(*(Q.p(0, -b - 6) + Q.p(0, b + 6)), cor=CENTRO, larg=0.9,
           duplo=False, tracejado='11 4 2 4', amp=0.3)

    qw, qh, qx, qy = UI['qr']
    T.path([Q.p(qx - qw / 2, qy - qh / 2), Q.p(qx + qw / 2, qy - qh / 2),
            Q.p(qx + qw / 2, qy + qh / 2), Q.p(qx - qw / 2, qy + qh / 2)],
           fechar=True, larg=1.5)
    for i in range(5):
        for j in range(5):
            if (i * 3 + j * 5 + i * j) % 4 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 5, qy - qh / 2 + j * qh / 5
                p1 = Q.p(x0 + 0.6, y0 + 0.6)
                p2 = Q.p(x0 + qw / 5 - 0.6, y0 + qh / 5 - 0.6)
                T.path([p1, (p2[0], p1[1]), p2, (p1[0], p2[1])], fechar=True,
                       cor=(0.17, 0.17, 0.17), larg=0.6, duplo=False,
                       fill=(0.17, 0.17, 0.17), op=0.8)
    Q.nota(qx - qw / 2, qy + qh / 2, 'QR impresso - o celular le', lado='esq')

    lx, ly = UI['xy_led']
    pl = Q.p(lx, ly)
    T.circ(pl[0], pl[1], UI['furo_led'] * Q.esc / 2, larg=1.5)
    Q.nota(lx, ly, 'LED vermelho / verde', lado='esq')

    bx, by = UI['xy_botao']
    pb = Q.p(bx, by)
    T.circ(pb[0], pb[1], UI['furo_botao'] * Q.esc / 2, larg=2.0)
    T.circ(pb[0], pb[1], UI['furo_botao'] * Q.esc / 2 - 4, cor=CINZA,
           larg=0.9, duplo=False)
    Q.nota(bx, by, 'botao de liberacao', lado='dir')

    for fx, fy in FUROS:
        pf = Q.p(fx, fy)
        T.circ(pf[0], pf[1], PAR['d_cabeca'] * Q.esc / 2, larg=1.2)
        T.reta(pf[0] - 4, pf[1], pf[0] + 4, pf[1], larg=0.9, duplo=False, amp=0.4)
    Q.nota(FUROS[1][0], FUROS[1][1], '4x M2 com inserto', lado='dir')

    Q.cota_h(-a, a, b, 'L = %.0f' % P['larg'], fora=28)
    Q.cota_v(-b, b, a, 'P = %.0f' % P['prof'], fora=20)
    Q.cota_h(qx - qw / 2, qx + qw / 2, qy - qh / 2, '%.0f' % qw, fora=-16)
    Q.resolver()


def frontal(Q, ns):
    T, P, PINO, TEC, GAR = Q.T, ns['P'], ns['PINO'], ns['TECIDO'], ns['GARRA']
    a, H, zs, t = P['larg'] / 2, P['alt'], P['z_split'], P['t_parede']
    T.path([Q.p(-a, zs), Q.p(a, zs), Q.p(a, H), Q.p(-a, H)], fechar=True, larg=1.9)
    T.path([Q.p(-a, 0), Q.p(a, 0), Q.p(a, zs), Q.p(-a, zs)], fechar=True, larg=1.9)
    Q.nota(-a + 6, (zs + H) / 2, 'carcaca superior', lado='esq', cor=CINZA)
    Q.nota(-a + 6, zs / 2, 'carcaca inferior', lado='esq', cor=CINZA)

    te = TEC['esp'] * 3.5
    tw = P['larg'] * 0.84
    quad = [Q.p(-tw / 2, 0), Q.p(tw / 2, 0), Q.p(tw / 2, -te), Q.p(-tw / 2, -te)]
    T.path(quad, fechar=True, larg=1.6, cor=DESTAQ)
    T.hach(quad, passo=9, cor=DESTAQ, larg=1.0)
    Q.nota(-tw / 2 + 10, -te / 2, 'A CAMISA ENTRA AQUI', lado='esq', cor=DESTAQ)

    dw, dh = PINO['d_cabeca'], PINO['t_cabeca'] * 3.5
    disco = [Q.p(-dw / 2, -te), Q.p(dw / 2, -te), Q.p(dw / 2, -te - dh),
             Q.p(-dw / 2, -te - dh)]
    T.path(disco, fechar=True, larg=1.7)
    T.hach(disco, passo=6)
    Q.nota(dw / 2, -te - dh / 2, 'disco do pino, por baixo', lado='dir')

    hw = PINO['d_haste'] * 1.8
    T.path([Q.p(-hw / 2, -te), Q.p(hw / 2, -te), Q.p(hw / 2, PINO['h_haste'] - te),
            Q.p(-hw / 2, PINO['h_haste'] - te)], fechar=True, larg=1.5)
    Q.nota(hw / 2, PINO['h_haste'] / 2, 'haste atravessa o tecido', lado='dir')

    gw, gh = GAR['diam'], GAR['alt']
    T.path([Q.p(-gw / 2, t), Q.p(gw / 2, t), Q.p(gw / 2, t + gh), Q.p(-gw / 2, t + gh)],
           fechar=True, larg=1.5, cor=VERDE)
    Q.nota(-gw / 2, t + gh / 2, 'garra', lado='esq', cor=VERDE)

    T.reta(*(Q.p(0, -te - dh - 5) + Q.p(0, H + 5)), cor=CENTRO, larg=0.9,
           duplo=False, tracejado='11 4 2 4', amp=0.3)
    Q.cota_v(0, H, a, 'A = %.0f' % H, fora=16)
    Q.resolver()


def lateral(Q, ns):
    T, P, GAR, BU, CU = Q.T, ns['P'], ns['GARRA'], ns['BUCHA'], ns['CUR']
    b, H, zs, t = P['prof'] / 2, P['alt'], P['z_split'], P['t_parede']
    gy = ns['XY_GARRA'][1]
    T.path([Q.p(-b, zs), Q.p(b, zs), Q.p(b, H), Q.p(-b, H)], fechar=True, larg=1.9)
    T.path([Q.p(-b, 0), Q.p(b, 0), Q.p(b, zs), Q.p(-b, zs)], fechar=True, larg=1.9)
    T.path([Q.p(gy - GAR['diam'] / 2, t), Q.p(gy + GAR['diam'] / 2, t),
            Q.p(gy + GAR['diam'] / 2, t + GAR['alt']),
            Q.p(gy - GAR['diam'] / 2, t + GAR['alt'])], fechar=True, larg=1.4, cor=VERDE)
    Q.nota(gy - GAR['diam'] / 2, t + GAR['alt'] / 2, 'garra', lado='esq', cor=VERDE)
    zc = t + GAR['alt'] + BU['alt']
    T.path([Q.p(gy - CU['prof'] / 2, zc), Q.p(gy + CU['prof'] / 2, zc),
            Q.p(gy + CU['prof'] / 2, zc + CU['t_fino'] + GAR['curso']),
            Q.p(gy - CU['prof'] / 2, zc + CU['t_fino'])], fechar=True, larg=1.4, cor=COTA)
    Q.nota(gy + CU['prof'] / 2, zc + 2, 'cursor com rampa', lado='dir', cor=COTA)
    T.reta(*(Q.p(gy, -5) + Q.p(gy, H + 5)), cor=CENTRO, larg=0.9,
           duplo=False, tracejado='11 4 2 4', amp=0.3)
    Q.cota_h(-b, b, H, 'P = %.0f' % P['prof'], fora=26)
    Q.resolver()


def perspectiva(Q, ns):
    T, P, UI = Q.T, ns['P'], ns['UI']
    a, b, h = P['larg'] / 2, P['prof'] / 2, P['alt']
    ca, sa = 0.866, 0.5

    def iso(x, y, z):
        return Q.reg(Q.px + (x - y) * ca * Q.esc,
                     Q.py - ((x + y) * sa - z * 1.2) * Q.esc)

    T.path([iso(-a, -b, h), iso(a, -b, h), iso(a, b, h), iso(-a, b, h)],
           fechar=True, larg=1.9)
    for sx, sy in ((a, -b), (a, b), (-a, b)):
        T.reta(*(iso(sx, sy, h) + iso(sx, sy, 0)), larg=1.7)
    T.path([iso(a, -b, 0), iso(a, b, 0), iso(-a, b, 0)], larg=1.7)

    qw, qh, qx, qy = UI['qr']
    T.path([iso(qx - qw / 2, qy - qh / 2, h), iso(qx + qw / 2, qy - qh / 2, h),
            iso(qx + qw / 2, qy + qh / 2, h), iso(qx - qw / 2, qy + qh / 2, h)],
           fechar=True, larg=1.3)
    for i in range(4):
        for j in range(4):
            if (i + j * 3) % 3 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 4, qy - qh / 2 + j * qh / 4
                T.path([iso(x0 + 1, y0 + 1, h), iso(x0 + qw / 4 - 1, y0 + 1, h),
                        iso(x0 + qw / 4 - 1, y0 + qh / 4 - 1, h),
                        iso(x0 + 1, y0 + qh / 4 - 1, h)], fechar=True,
                       cor=(0.17, 0.17, 0.17), larg=0.5, duplo=False,
                       fill=(0.17, 0.17, 0.17), op=0.75)
    pbt = iso(UI['xy_botao'][0], UI['xy_botao'][1], h)
    T.circ(pbt[0], pbt[1], UI['furo_botao'] * Q.esc / 2, larg=1.8)
    pl = iso(UI['xy_led'][0], UI['xy_led'][1], h)
    T.circ(pl[0], pl[1], UI['furo_led'] * Q.esc / 2, larg=1.4)
    s = 'a peca fica pendurada por baixo, presa pelo pino'
    T.txt(Q.x + Q.w / 2, Q.y + Q.h - 16, s, tam=11, cor=CINZA, anc='middle')
    Q.reg(Q.x + Q.w / 2 - larg_txt(s, 11) / 2, Q.y + Q.h - 26)
    Q.reg(Q.x + Q.w / 2 + larg_txt(s, 11) / 2, Q.y + Q.h - 13)


def detalhe(Q, ns):
    T, GAR = Q.T, ns['GARRA']
    E = Q.esc
    T.path([Q.p(-16, 20), Q.p(-9, -1), Q.p(9, -1), Q.p(16, 20)], larg=1.8)
    Q.nota(-13, 14, 'copo conico', lado='esq')
    for dx in (-6, 0, 6):
        pc = Q.p(dx, 5)
        T.circ(pc[0], pc[1], 3.1 * E, larg=1.5)
    Q.nota(9, 7, '3 esferas de aco', lado='dir')
    T.path([Q.p(-8, -1), Q.p(8, -1), Q.p(8, 5), Q.p(-8, 5)], fechar=True,
           larg=1.6, cor=(0.54, 0.35, 0.10))
    Q.nota(8, 2, 'carretel', lado='dir', cor=(0.54, 0.35, 0.10))
    mx = -21
    pts = [Q.p(mx, 6)]
    for i in range(8):
        pts.append(Q.p(mx + (2.2 if i % 2 == 0 else -2.2), 6 + (i + 1) * 1.6))
    T.path(pts, larg=1.2, duplo=False)
    Q.nota(mx, 14, 'mola', lado='esq')
    T.path([Q.p(-6, -7), Q.p(6, -7), Q.p(6, -1), Q.p(-6, -1)], fechar=True,
           larg=1.6, cor=COTA)
    Q.nota(-6, -4, 'bucha', lado='esq', cor=COTA)
    T.path([Q.p(-30, -16), Q.p(16, -16), Q.p(16, -9), Q.p(-20, -9)],
           fechar=True, larg=1.7, cor=COTA)
    Q.nota(-28, -13, 'cursor com rampa', lado='esq', cor=COTA)
    p1, p2 = Q.p(30, -12), Q.p(18, -12)
    T.flecha(p1[0], p1[1], p2[0], p2[1], cor=DESTAQ, larg=2.0)
    Q.nota(30, -12, 'o atuador empurra', lado='dir', cor=DESTAQ)
    pa, pb = Q.p(11, -7), Q.p(11, -1)
    T.flecha(pa[0], pa[1], pb[0], pb[1], cor=DESTAQ, larg=1.9, tam=6)
    Q.nota(11, -4, '%.1f mm de queda' % GAR['curso'], lado='dir', cor=DESTAQ)
    Q.resolver(base=Q.y + Q.h - 66)
    y = Q.y + Q.h - 50
    for i, (s, cor) in enumerate([
            ('A rampa converte o curso do atuador em %.1f mm.' % GAR['curso'], TINTA),
            ('As esferas ganham folga no cone e o pino sai.', TINTA),
            ('Nao ha ima aqui - o movimento e mecanico.', DESTAQ)]):
        T.txt(Q.x + 14, y + i * 16, s, tam=11, cor=cor)
        Q.reg(Q.x + 14 + larg_txt(s, 11), y + i * 16)


def fluxo(Q):
    T = Q.T
    passos = ['1   aponta o celular no QR impresso',
              '2   paga no app',
              '3   o app manda o token por Bluetooth',
              '4   o LED passa de vermelho a VERDE',
              '5   aperta o botao e a camisa solta']
    y = Q.y + 60
    for s in passos:
        T.txt(Q.x + 20, y, s, tam=12)
        Q.reg(Q.x + 20 + larg_txt(s, 12), y)
        y += 26
    for i, s in enumerate(['Sem internet na hora de liberar:',
                           'o token ja esta no celular.']):
        T.txt(Q.x + 20, y + 8 + i * 15, s, tam=11, cor=VERDE)
        Q.reg(Q.x + 20 + larg_txt(s, 11), y + 8 + i * 15)


def legenda(T, ns, x, y, w, h):
    T.ret(x, y, w, h, cor=MOLDURA, larg=1.1, duplo=False, amp=0.5)
    T.reta(x, y + 28, x + w, y + 28, cor=MOLDURA, larg=0.9, duplo=False, amp=0.4)
    T.txt(x + 14, y + 20, 'Tag&Go - etiqueta antifurto autoliberavel',
          tam=13, peso='bold')
    yy = y + 47
    for k, v in (('desenho', 'esboco inicial, a mao livre'),
                 ('cotas', 'em milimetros, sem escala'),
                 ('mecanismo', str(ns.get('MECANISMO', '?'))),
                 ('origem das cotas', 'fusion/Antifurto.py')):
        T.txt(x + 14, yy, k, tam=10.5, cor=CINZA)
        T.txt(x + 136, yy, v, tam=11)
        yy += 18


# ============================================================================
# FOLHAS
# ============================================================================

def folha_completa(ns):
    W, H = 1440, 1000
    T = Tela(W, H)
    T.ret(18, 18, W - 36, H - 36, cor=MOLDURA, larg=1.4, duplo=False, amp=0.6)
    T.txt(44, 60, 'Esboco inicial do produto', tam=24, peso='bold')
    T.reta(44, 70, 370, 70, cor=(0.85, 0.65, 0.13), larg=3.0, duplo=False)
    T.txt(44, 90, 'Etiqueta antifurto que o proprio cliente libera depois de pagar.',
          tam=13, cor=(0.33, 0.33, 0.33))
    T.txt(W - 44, 60, 'Projeto de Produto e Processo | Poli-USP',
          tam=12, anc='end', cor=(0.47, 0.47, 0.47))

    P = ns['P']
    qs = []
    q = Quadro(T, 40, 108, 470, 462, 'A) planta', esc=3.2, oy=0.55,
               col_esq=118, col_dir=104)
    planta(q, ns); qs.append(('A planta', q))
    q = Quadro(T, 40, 584, 470, 250, 'B) frontal - onde entra a camisa',
               esc=3.0, cy_mm=P['alt'] / 2, oy=0.56, col_esq=126, col_dir=118)
    frontal(q, ns); qs.append(('B frontal', q))
    q = Quadro(T, 526, 584, 392, 250, 'C) lateral', esc=2.6,
               cy_mm=P['alt'] / 2, oy=0.56, col_esq=52, col_dir=92)
    lateral(q, ns); qs.append(('C lateral', q))
    q = Quadro(T, 526, 108, 392, 462, 'D) perspectiva', esc=1.8, oy=0.48,
               col_esq=10, col_dir=10)
    perspectiva(q, ns); qs.append(('D perspectiva', q))
    q = Quadro(T, 934, 108, 466, 462, 'E) detalhe - como a garra solta',
               esc=3.4, oy=0.40, col_esq=108, col_dir=118)
    detalhe(q, ns); qs.append(('E detalhe', q))
    q = Quadro(T, 934, 584, 466, 250, 'F) fluxo de uso', col_esq=10, col_dir=10)
    fluxo(q); qs.append(('F fluxo', q))

    legenda(T, ns, 40, 848, 878, 116)
    for i, s in enumerate(['medidas em milimetros',
                           'tracado a mao livre - representacao inicial',
                           'gerado por desenhos/esboco.py']):
        T.txt(934, 868 + i * 19, s, tam=11, cor=(0.62, 0.62, 0.62))
    return T, qs


def folha_solta(ns, qual):
    """Uma vista por folha, para entrar no LaTeX como figura propria."""
    conf = {
        'planta':      (560, 470, 'Planta', planta, dict(esc=3.4, oy=0.55,
                                                         col_esq=126, col_dir=112)),
        'frontal':     (560, 340, 'Vista frontal - onde entra a camisa', frontal,
                        dict(esc=3.2, oy=0.56, col_esq=134, col_dir=126)),
        'lateral':     (470, 300, 'Vista lateral', lateral,
                        dict(esc=2.8, oy=0.56, col_esq=56, col_dir=100)),
        'perspectiva': (470, 380, 'Perspectiva', perspectiva,
                        dict(esc=2.0, oy=0.50, col_esq=10, col_dir=10)),
        'detalhe':     (560, 430, 'Detalhe - como a garra solta', detalhe,
                        dict(esc=3.6, oy=0.40, col_esq=118, col_dir=126)),
    }
    W, H, titulo, fn, kw = conf[qual]
    T = Tela(W, H)
    if qual in ('frontal', 'lateral'):
        kw['cy_mm'] = ns['P']['alt'] / 2
    q = Quadro(T, 8, 8, W - 16, H - 16, titulo, **kw)
    if qual == 'perspectiva':
        fn(q, ns)
    else:
        fn(q, ns)
    return T, q


TEX = r"""% ---------------------------------------------------------------
% Esbocos gerados por desenhos/esboco.py - cole onde couber.
% Os PDFs ficam em desenhos/. No Overleaf, o \graphicspath do
% preambulo ja aponta para imagens/, entao ou copie os PDFs para
% imagens/ ou use o caminho completo, como abaixo.
% ---------------------------------------------------------------

\begin{figure}[h!]
    \centering
    \caption{Esboco inicial do produto: vistas, detalhe do mecanismo e fluxo de uso}
    \includegraphics[width=\textwidth]{desenhos/esboco.pdf}
    \label{fig:proposta-esboco-geral}
    \source{Autor}
\end{figure}

\begin{figure}[h!]
    \caption{Vistas do dispositivo}
    \begin{subfigure}{0.48\textwidth}
        \includegraphics[width=0.95\textwidth]{desenhos/fig-planta.pdf}
        \caption{Planta}
        \label{fig:proposta-planta}
    \end{subfigure}%
    \begin{subfigure}{0.48\textwidth}
        \includegraphics[width=0.95\textwidth]{desenhos/fig-perspectiva.pdf}
        \caption{Perspectiva}
        \label{fig:proposta-perspectiva}
    \end{subfigure}
    \begin{subfigure}{0.48\textwidth}
        \includegraphics[width=0.95\textwidth]{desenhos/fig-frontal.pdf}
        \caption{Vista frontal, mostrando onde a peca de roupa e presa}
        \label{fig:proposta-frontal}
    \end{subfigure}%
    \begin{subfigure}{0.48\textwidth}
        \includegraphics[width=0.95\textwidth]{desenhos/fig-lateral.pdf}
        \caption{Vista lateral}
        \label{fig:proposta-lateral}
    \end{subfigure}
    \label{fig:proposta-vistas}
    \source{Autor}
\end{figure}

\begin{figure}[h!]
    \centering
    \caption{Detalhe do mecanismo de destravamento}
    \includegraphics[width=0.8\textwidth]{desenhos/fig-detalhe.pdf}
    \label{fig:proposta-detalhe}
    \source{Autor}
\end{figure}
"""


def gerar():
    ns = parametros()
    saidas = []

    T, qs = folha_completa(ns)
    io.open(os.path.join(AQUI, 'esboco.svg'), 'w', encoding='utf-8').write(T.svg())
    io.open(os.path.join(AQUI, 'esboco.pdf'), 'wb').write(T.pdf())
    io.open(os.path.join(AQUI, 'preview.html'), 'w', encoding='utf-8').write(
        '<body style="margin:0;background:#e9e6de;padding:12px">'
        + T.svg().replace('<svg ', '<svg style="width:100%;height:auto;display:block;'
                                   'box-shadow:0 2px 18px rgba(0,0,0,.18)" ', 1)
        + '</body>')
    saidas += ['esboco.svg', 'esboco.pdf', 'preview.html']

    for qual in ('planta', 'frontal', 'lateral', 'perspectiva', 'detalhe'):
        Ts, q = folha_solta(ns, qual)
        nome = 'fig-%s' % qual
        io.open(os.path.join(AQUI, nome + '.pdf'), 'wb').write(Ts.pdf())
        io.open(os.path.join(AQUI, nome + '.svg'), 'w', encoding='utf-8').write(Ts.svg())
        qs.append((nome, q))
        saidas.append(nome + '.pdf')

    io.open(os.path.join(AQUI, 'incluir.tex'), 'w', encoding='utf-8').write(TEX)
    saidas.append('incluir.tex')
    return qs, saidas


if __name__ == '__main__':
    qs, saidas = gerar()
    print('arquivos gerados em desenhos/:')
    for s in saidas:
        print('   ' + s)
    print()
    print('conferencia - conteudo que passa da moldura:')
    ruim = 0
    for nome, q in qs:
        v = q.vazou()
        print('   %-16s %s' % (nome, v if v else 'ok'))
        if v:
            ruim += 1
    print()
    print('%d de %d quadros com vazamento' % (ruim, len(qs)))
