# -*- coding: utf-8 -*-
"""
ESBOCO A MAO LIVRE - representacao inicial do produto
Item D | Projeto de Produto e Processo | Poli-USP

RODAR:  python desenhos/esboco.py
SAIDA:  desenhos/esboco.svg  +  desenhos/preview.html

Convencao de desenho tecnico - vistas ortograficas alinhadas, linhas de
centro, cotas com linha de extensao e legenda - mas tracado a mao livre,
porque e' esboco inicial.

As medidas NAO estao digitadas aqui: sao lidas de fusion/Antifurto.py, o
mesmo arquivo que gera o CAD. Mudou la, muda aqui.

Cada quadro registra tudo que desenha e o script confere no fim se algo
vazou da moldura. Sem dependencia externa - so a biblioteca padrao.
"""

import io
import os
import re
import math

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FONTE_CAD = os.path.join(RAIZ, 'fusion', 'Antifurto.py')
SVG = os.path.join(AQUI, 'esboco.svg')
HTML = os.path.join(AQUI, 'preview.html')

TINTA, COTA, CENTRO = '#1b1b1b', '#1d6fa5', '#9aa0a6'
DESTAQ, VERDE = '#b5341f', '#2f6b46'
PAPEL, MOLDURA = '#fcfbf7', '#c9c4b8'


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
    src = io.open(FONTE_CAD, encoding='utf-8').read()
    ns = {}
    for nome in ('P', 'PAR', 'GARRA', 'PINO', 'TECIDO', 'CUR', 'BUCHA', 'UI', 'REC'):
        b = _bloco(src, nome)
        if not b:
            raise SystemExit('nao achei o bloco %s' % nome)
        exec(b, ns)
    for nome in ('FUROS', 'XY_GARRA', 'MECANISMO'):
        m = re.search(r'^%s\s*= .*$' % nome, src, re.M)
        if m:
            exec(m.group(0), ns)
    return ns


# ============================================================================
# LAPIS
# ============================================================================

class Lapis:
    def __init__(self, semente=20260909):
        self.s = semente
        self.out = []

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

    def path(self, pts, cor=TINTA, larg=1.6, fechar=False, duplo=True,
             fill='none', op=1.0, tracejado=None, amp=1.0):
        if fechar:
            pts = list(pts) + [pts[0]]
        dash = ' stroke-dasharray="%s"' % tracejado if tracejado else ''
        for i in range(2 if duplo else 1):
            d = 'M ' + ' L '.join('%.1f %.1f' % p
                                  for p in self._tremido(pts, amp if i == 0 else amp * 1.5))
            self.out.append(
                '<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f"%s '
                'stroke-linecap="round" stroke-linejoin="round" opacity="%.2f"/>'
                % (d, fill if i == 0 else 'none', cor,
                   larg if i == 0 else larg * 0.5, dash, op if i == 0 else op * 0.4))

    def reta(self, x1, y1, x2, y2, **k):
        self.path([(x1, y1), (x2, y2)], **k)

    def ret(self, x, y, w, h, **k):
        self.path([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fechar=True, **k)

    def circ(self, cx, cy, r, **k):
        n = max(16, int(r * 1.2))
        self.path([(cx + r * math.cos(2 * math.pi * i / n),
                    cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)],
                  fechar=True, **k)

    def hach(self, pts, passo=8.0, cor='#8d8d8d', larg=0.8):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        d = (math.cos(math.radians(45)), math.sin(math.radians(45)))
        t = -(x1 - x0) - (y1 - y0)
        while t < (x1 - x0) + (y1 - y0):
            seg = self._corta(pts, (x0 + t, y0), d)
            if seg:
                self.path(list(seg), cor=cor, larg=larg, duplo=False, op=0.5, amp=0.5)
            t += passo

    def _corta(self, poly, p0, d):
        ts = []
        n = len(poly)
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

    def centro(self, x1, y1, x2, y2):
        self.reta(x1, y1, x2, y2, cor=CENTRO, larg=0.9, duplo=False,
                  tracejado='11 4 2 4', amp=0.35)

    def txt(self, x, y, s, tam=12.5, cor=TINTA, anc='start', peso='normal', it=False):
        self.out.append(
            '<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" text-anchor="%s" '
            'font-weight="%s" font-style="%s" transform="rotate(%.2f %.1f %.1f)" '
            'font-family="Segoe Print, Bradley Hand, Comic Sans MS, Chalkboard, cursive">'
            '%s</text>' % (x, y, tam, cor, anc, peso, 'italic' if it else 'normal',
                           self._n(0.55), x, y, _esc(s)))

    def seta(self, x, y, ang, tam=7.0, cor=TINTA, larg=1.1):
        for s in (+1, -1):
            self.reta(x, y, x - tam * math.cos(ang + s * 0.4),
                      y - tam * math.sin(ang + s * 0.4),
                      cor=cor, larg=larg, duplo=False, amp=0.35)

    def flecha(self, x1, y1, x2, y2, cor=TINTA, larg=1.5, tam=8.0):
        self.reta(x1, y1, x2, y2, cor=cor, larg=larg, duplo=False, amp=0.7)
        self.seta(x2, y2, math.atan2(y2 - y1, x2 - x1), tam, cor, larg)


def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ============================================================================
# QUADRO - cada vista com origem e escala proprias, em mm
# ============================================================================

class Quadro:
    def __init__(self, L, x, y, w, h, titulo, cx_mm=0.0, cy_mm=0.0, esc=1.0,
                 ox=0.5, oy=0.5):
        self.L, self.x, self.y, self.w, self.h = L, x, y, w, h
        self.esc = esc
        self.px, self.py = x + w * ox, y + h * oy
        self.cx_mm, self.cy_mm = cx_mm, cy_mm
        self.marcas = []
        L.ret(x, y, w, h, cor=MOLDURA, larg=1.1, duplo=False, amp=0.5)
        L.txt(x + 14, y + 25, titulo, tam=15, peso='bold')
        L.reta(x + 14, y + 32, x + 14 + len(titulo) * 7.2, y + 32,
               cor='#d9a520', larg=2.4, duplo=False, amp=0.5)

    def p(self, xm, ym):
        """mm -> pixel. +Y do modelo aponta para CIMA na folha."""
        px = self.px + (xm - self.cx_mm) * self.esc
        py = self.py - (ym - self.cy_mm) * self.esc
        self.marcas.append((px, py))
        return px, py

    def reg(self, px, py):
        self.marcas.append((px, py))
        return px, py

    def rotulo(self, px, py, s, tam=12, **k):
        anc = k.get('anc', 'start')
        w = len(s) * tam * 0.5
        esq = px - w if anc == 'end' else (px - w / 2 if anc == 'middle' else px)
        self.reg(esq, py - tam)
        self.reg(esq + w, py + 3)
        self.L.txt(px, py, s, tam=tam, **k)

    def vazou(self, folga=8.0):
        if not self.marcas:
            return None
        xs = [m[0] for m in self.marcas]
        ys = [m[1] for m in self.marcas]
        v = []
        if min(xs) < self.x + folga:
            v.append('esq %.0f' % (self.x + folga - min(xs)))
        if max(xs) > self.x + self.w - folga:
            v.append('dir %.0f' % (max(xs) - self.x - self.w + folga))
        if min(ys) < self.y + 40:
            v.append('topo %.0f' % (self.y + 40 - min(ys)))
        if max(ys) > self.y + self.h - folga:
            v.append('baixo %.0f' % (max(ys) - self.y - self.h + folga))
        return ', '.join(v) if v else None

    # ---- cotas ----
    def cota_h(self, x1m, x2m, ym, rot, fora=26.0):
        L = self.L
        a, b = self.p(x1m, ym), self.p(x2m, ym)
        yl = a[1] - fora
        self.reg(a[0], yl); self.reg(b[0], yl)
        for px in (a[0], b[0]):
            L.reta(px, a[1] - 4 * (1 if fora > 0 else -1), px, yl - 4 * (1 if fora > 0 else -1),
                   cor=COTA, larg=0.7, duplo=False, op=0.7, amp=0.3)
        L.reta(a[0], yl, b[0], yl, cor=COTA, larg=1.0, duplo=False, amp=0.45)
        L.seta(a[0], yl, math.pi, 6.5, COTA, 1.0)
        L.seta(b[0], yl, 0.0, 6.5, COTA, 1.0)
        self.rotulo((a[0] + b[0]) / 2, yl - 7 if fora > 0 else yl + 15, rot,
                    tam=12, cor=COTA, anc='middle')

    def cota_v(self, y1m, y2m, xm, rot, fora=26.0):
        L = self.L
        a, b = self.p(xm, y1m), self.p(xm, y2m)
        xl = a[0] + fora
        s = 1 if fora > 0 else -1
        self.reg(xl, a[1]); self.reg(xl, b[1])
        for py in (a[1], b[1]):
            L.reta(a[0] + 4 * s, py, xl + 4 * s, py,
                   cor=COTA, larg=0.7, duplo=False, op=0.7, amp=0.3)
        L.reta(xl, a[1], xl, b[1], cor=COTA, larg=1.0, duplo=False, amp=0.45)
        L.seta(xl, a[1], math.pi / 2, 6.5, COTA, 1.0)
        L.seta(xl, b[1], -math.pi / 2, 6.5, COTA, 1.0)
        self.rotulo(xl + 7 * s, (a[1] + b[1]) / 2 + 4, rot, tam=12, cor=COTA,
                    anc='start' if s > 0 else 'end')

    def chamada(self, xm, ym, dx, dy, txt, cor=TINTA, anc='start'):
        L = self.L
        a = self.p(xm, ym)
        b = (a[0] + dx, a[1] + dy)
        self.reg(*b)
        L.reta(a[0], a[1], b[0], b[1], cor='#7a7a7a', larg=0.8, duplo=False,
               op=0.85, amp=0.5)
        L.circ(a[0], a[1], 2.0, cor='#7a7a7a', larg=0.8, duplo=False)
        self.rotulo(b[0] + (4 if anc == 'start' else -4), b[1] + 4, txt,
                    tam=11.5, cor=cor, anc=anc)


# ============================================================================
# VISTAS
# ============================================================================

def planta(Q, ns):
    L, P, UI, FUROS, PAR = Q.L, ns['P'], ns['UI'], ns['FUROS'], ns['PAR']
    a, b = P['larg'] / 2, P['prof'] / 2

    L.path([Q.p(-a, -b), Q.p(a, -b), Q.p(a, b), Q.p(-a, b)], fechar=True, larg=2.0)
    L.path([Q.p(-a + 2.4, -b + 2.4), Q.p(a - 2.4, -b + 2.4),
            Q.p(a - 2.4, b - 2.4), Q.p(-a + 2.4, b - 2.4)],
           fechar=True, cor='#a8a8a8', larg=0.8, duplo=False)
    L.centro(*(Q.p(-a - 7, 0) + Q.p(a + 7, 0)))
    L.centro(*(Q.p(0, -b - 7) + Q.p(0, b + 7)))

    qw, qh, qx, qy = UI['qr']
    L.path([Q.p(qx - qw / 2, qy - qh / 2), Q.p(qx + qw / 2, qy - qh / 2),
            Q.p(qx + qw / 2, qy + qh / 2), Q.p(qx - qw / 2, qy + qh / 2)],
           fechar=True, larg=1.5)
    for i in range(5):
        for j in range(5):
            if (i * 3 + j * 5 + i * j) % 4 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 5, qy - qh / 2 + j * qh / 5
                p1 = Q.p(x0 + 0.6, y0 + 0.6)
                p2 = Q.p(x0 + qw / 5 - 0.6, y0 + qh / 5 - 0.6)
                L.path([p1, (p2[0], p1[1]), p2, (p1[0], p2[1])], fechar=True,
                       cor='#2b2b2b', larg=0.6, duplo=False, fill='#2b2b2b', op=0.8)
    Q.chamada(qx, qy + qh / 2, 4, -34, 'QR impresso')
    Q.chamada(qx, qy + qh / 2, 4, -20, '(o celular le este)')

    lx, ly = UI['xy_led']
    pl = Q.p(lx, ly)
    L.circ(pl[0], pl[1], UI['furo_led'] * Q.esc / 2, larg=1.5)
    Q.chamada(lx, ly, -18, 32, 'LED vermelho/verde', anc='end')

    bx, by = UI['xy_botao']
    pb = Q.p(bx, by)
    L.circ(pb[0], pb[1], UI['furo_botao'] * Q.esc / 2, larg=2.0)
    L.circ(pb[0], pb[1], UI['furo_botao'] * Q.esc / 2 - 4, cor='#8d8d8d',
           larg=0.9, duplo=False)
    Q.chamada(bx, by, 26, 26, 'BOTAO')

    for fx, fy in FUROS:
        pf = Q.p(fx, fy)
        L.circ(pf[0], pf[1], PAR['d_cabeca'] * Q.esc / 2, larg=1.2)
        L.reta(pf[0] - 4, pf[1], pf[0] + 4, pf[1], larg=0.9, duplo=False, amp=0.4)
    Q.chamada(FUROS[1][0], FUROS[1][1], 6, 26, '4x M2 c/ inserto', anc='end')

    Q.cota_h(-a, a, b, 'L = %.0f' % P['larg'], fora=30)
    Q.cota_v(-b, b, a, 'P = %.0f' % P['prof'], fora=16)
    Q.cota_h(qx - qw / 2, qx + qw / 2, qy - qh / 2, '%.0f' % qw, fora=-18)


def frontal(Q, ns):
    L, P, PINO, TEC, GAR = Q.L, ns['P'], ns['PINO'], ns['TECIDO'], ns['GARRA']
    a, H, zs, t = P['larg'] / 2, P['alt'], P['z_split'], P['t_parede']

    L.path([Q.p(-a, zs), Q.p(a, zs), Q.p(a, H), Q.p(-a, H)], fechar=True, larg=1.9)
    L.path([Q.p(-a, 0), Q.p(a, 0), Q.p(a, zs), Q.p(-a, zs)], fechar=True, larg=1.9)
    Q.rotulo(*(Q.p(-a + 3, H - 5) + ('carcaca superior',)), tam=10.5, cor='#666666')
    Q.rotulo(*(Q.p(-a + 3, 3) + ('carcaca inferior',)), tam=10.5, cor='#666666')

    te = TEC['esp'] * 3.5
    tw = P['larg'] * 0.84
    quad = [Q.p(-tw / 2, 0), Q.p(tw / 2, 0), Q.p(tw / 2, -te), Q.p(-tw / 2, -te)]
    L.path(quad, fechar=True, larg=1.6, cor=DESTAQ)
    L.hach(quad, passo=9, cor=DESTAQ, larg=1.0)
    Q.chamada(-tw / 2 + 8, -te / 2, -8, 24, 'A CAMISA', cor=DESTAQ, anc='end')

    dw, dh = PINO['d_cabeca'], PINO['t_cabeca'] * 3.5
    disco = [Q.p(-dw / 2, -te), Q.p(dw / 2, -te), Q.p(dw / 2, -te - dh),
             Q.p(-dw / 2, -te - dh)]
    L.path(disco, fechar=True, larg=1.7)
    L.hach(disco, passo=6)
    Q.chamada(dw / 2, -te - dh / 2, 30, 20, 'disco do pino')

    hw = PINO['d_haste'] * 1.8
    L.path([Q.p(-hw / 2, -te), Q.p(hw / 2, -te), Q.p(hw / 2, PINO['h_haste'] - te),
            Q.p(-hw / 2, PINO['h_haste'] - te)], fechar=True, larg=1.5)

    gw, gh = GAR['diam'], GAR['alt']
    L.path([Q.p(-gw / 2, t), Q.p(gw / 2, t), Q.p(gw / 2, t + gh), Q.p(-gw / 2, t + gh)],
           fechar=True, larg=1.5, cor=VERDE)
    Q.chamada(-gw / 2, t + gh / 2, -40, 14, 'garra', cor=VERDE, anc='end')

    L.centro(*(Q.p(0, -te - dh - 5) + Q.p(0, H + 5)))
    Q.cota_v(0, H, a, 'A = %.0f' % H, fora=14)


def lateral(Q, ns):
    L, P, GAR, BU, CU = Q.L, ns['P'], ns['GARRA'], ns['BUCHA'], ns['CUR']
    b, H, zs, t = P['prof'] / 2, P['alt'], P['z_split'], P['t_parede']
    gy = ns['XY_GARRA'][1]

    L.path([Q.p(-b, zs), Q.p(b, zs), Q.p(b, H), Q.p(-b, H)], fechar=True, larg=1.9)
    L.path([Q.p(-b, 0), Q.p(b, 0), Q.p(b, zs), Q.p(-b, zs)], fechar=True, larg=1.9)

    L.path([Q.p(gy - GAR['diam'] / 2, t), Q.p(gy + GAR['diam'] / 2, t),
            Q.p(gy + GAR['diam'] / 2, t + GAR['alt']),
            Q.p(gy - GAR['diam'] / 2, t + GAR['alt'])], fechar=True, larg=1.4, cor=VERDE)
    zc = t + GAR['alt'] + BU['alt']
    L.path([Q.p(gy - CU['prof'] / 2, zc), Q.p(gy + CU['prof'] / 2, zc),
            Q.p(gy + CU['prof'] / 2, zc + CU['t_fino'] + GAR['curso']),
            Q.p(gy - CU['prof'] / 2, zc + CU['t_fino'])], fechar=True, larg=1.4, cor=COTA)
    Q.chamada(gy + CU['prof'] / 2, zc + 1, 18, -22, 'cursor', cor=COTA)
    L.centro(*(Q.p(gy, -5) + Q.p(gy, H + 5)))
    Q.cota_h(-b, b, H, 'P = %.0f' % P['prof'], fora=28)


def perspectiva(Q, ns):
    L, P, UI = Q.L, ns['P'], ns['UI']
    a, b, h = P['larg'] / 2, P['prof'] / 2, P['alt']
    ca, sa = math.cos(math.radians(30)), math.sin(math.radians(30))

    def iso(x, y, z):
        return Q.reg(Q.px + (x - y) * ca * Q.esc,
                     Q.py - ((x + y) * sa - z * 1.2) * Q.esc)

    L.path([iso(-a, -b, h), iso(a, -b, h), iso(a, b, h), iso(-a, b, h)],
           fechar=True, larg=1.9)
    for sx, sy in ((a, -b), (a, b), (-a, b)):
        L.reta(*(iso(sx, sy, h) + iso(sx, sy, 0)), larg=1.7)
    L.path([iso(a, -b, 0), iso(a, b, 0), iso(-a, b, 0)], larg=1.7)

    qw, qh, qx, qy = UI['qr']
    L.path([iso(qx - qw / 2, qy - qh / 2, h), iso(qx + qw / 2, qy - qh / 2, h),
            iso(qx + qw / 2, qy + qh / 2, h), iso(qx - qw / 2, qy + qh / 2, h)],
           fechar=True, larg=1.3)
    for i in range(4):
        for j in range(4):
            if (i + j * 3) % 3 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 4, qy - qh / 2 + j * qh / 4
                L.path([iso(x0 + 1, y0 + 1, h), iso(x0 + qw / 4 - 1, y0 + 1, h),
                        iso(x0 + qw / 4 - 1, y0 + qh / 4 - 1, h),
                        iso(x0 + 1, y0 + qh / 4 - 1, h)], fechar=True,
                       cor='#2b2b2b', larg=0.5, duplo=False, fill='#2b2b2b', op=0.75)

    pbt = iso(*UI['xy_botao'], h)
    L.circ(pbt[0], pbt[1], UI['furo_botao'] * Q.esc / 2, larg=1.8)
    pl = iso(*UI['xy_led'], h)
    L.circ(pl[0], pl[1], UI['furo_led'] * Q.esc / 2, larg=1.4)
    Q.rotulo(Q.x + Q.w / 2, Q.y + Q.h - 18,
             'a peca fica pendurada por baixo, presa pelo pino',
             tam=11.5, cor='#666666', anc='middle', it=True)


def detalhe(Q, ns):
    L, GAR = Q.L, ns['GARRA']
    E = Q.esc

    L.path([Q.p(-16, 20), Q.p(-9, -1), Q.p(9, -1), Q.p(16, 20)], larg=1.8)
    Q.chamada(-13, 16, -22, -14, 'copo conico', anc='end')
    for dx in (-6, 0, 6):
        pc = Q.p(dx, 5)
        L.circ(pc[0], pc[1], 3.1 * E, larg=1.5)
    Q.chamada(14, 7, 22, -20, '3 esferas de aco')
    L.path([Q.p(-8, -1), Q.p(8, -1), Q.p(8, 5), Q.p(-8, 5)], fechar=True,
           larg=1.6, cor='#8a5a1a')
    Q.chamada(8, 1, 30, 36, 'carretel')

    mx = -21
    pts = [Q.p(mx, 6)]
    for i in range(8):
        pts.append(Q.p(mx + (2.2 if i % 2 == 0 else -2.2), 6 + (i + 1) * 1.6))
    L.path(pts, larg=1.2, duplo=False)
    Q.chamada(mx, 16, -16, 20, 'mola', anc='end')

    L.path([Q.p(-6, -7), Q.p(6, -7), Q.p(6, -1), Q.p(-6, -1)], fechar=True,
           larg=1.6, cor=COTA)
    L.path([Q.p(-30, -16), Q.p(16, -16), Q.p(16, -9), Q.p(-20, -9)],
           fechar=True, larg=1.7, cor=COTA)
    Q.chamada(-30, -13, -8, 22, 'cursor com rampa', cor=COTA, anc='end')
    Q.chamada(6, -4, 34, 12, 'bucha', cor=COTA)

    p1, p2 = Q.p(31, -12), Q.p(18, -12)
    L.flecha(p1[0], p1[1], p2[0], p2[1], cor=DESTAQ, larg=2.1)
    Q.chamada(31, -12, 2, -16, 'o atuador empurra', cor=DESTAQ)

    pa, pb = Q.p(11, -7), Q.p(11, -1)
    L.flecha(pa[0], pa[1], pb[0], pb[1], cor=DESTAQ, larg=2.0, tam=6)
    Q.rotulo(pa[0] + 7, (pa[1] + pb[1]) / 2 + 4, '%.1f mm' % GAR['curso'],
             tam=11.5, cor=DESTAQ)

    y = Q.y + Q.h - 56
    for i, (s, cor, peso) in enumerate([
            ('A rampa converte o curso do atuador em %.1f mm de queda.' % GAR['curso'],
             TINTA, 'normal'),
            ('As esferas ganham folga no cone e o pino sai.', TINTA, 'normal'),
            ('Nao ha ima aqui - o movimento e mecanico.', DESTAQ, 'bold')]):
        Q.rotulo(Q.x + 16, y + i * 18, s, tam=11.5, cor=cor, peso=peso)


def fluxo(Q):
    L = Q.L
    passos = ['1   aponta o celular no QR impresso',
              '2   paga no app',
              '3   o app manda o token por Bluetooth',
              '4   o LED passa de vermelho a VERDE',
              '5   aperta o botao e a camisa solta']
    y = Q.y + 66
    for s in passos:
        Q.rotulo(Q.x + 22, y, s, tam=12.5)
        y += 28
    Q.rotulo(Q.x + 22, y + 10, 'Sem internet na hora de liberar:', tam=11.5, cor=VERDE)
    Q.rotulo(Q.x + 22, y + 26, 'o token ja esta no celular.', tam=11.5, cor=VERDE)


def legenda(L, ns, x, y, w, h):
    L.ret(x, y, w, h, cor=MOLDURA, larg=1.1, duplo=False, amp=0.5)
    L.reta(x, y + 30, x + w, y + 30, cor=MOLDURA, larg=0.9, duplo=False, amp=0.4)
    L.txt(x + 14, y + 21, 'Tag&Go - etiqueta antifurto autoliberavel',
          tam=13.5, peso='bold')
    yy = y + 50
    for k, v in (('desenho', 'esboco inicial, a mao livre'),
                 ('cotas', 'em milimetros, sem escala'),
                 ('mecanismo', str(ns.get('MECANISMO', '?'))),
                 ('origem das cotas', 'fusion/Antifurto.py')):
        L.txt(x + 14, yy, k, tam=11, cor='#8d8d8d')
        L.txt(x + 138, yy, v, tam=11.5)
        yy += 19


# ============================================================================
# FOLHA
# ============================================================================

def gerar():
    ns = parametros()
    W, H = 1400, 990
    L = Lapis()
    L.out.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPEL))
    L.ret(18, 18, W - 36, H - 36, cor=MOLDURA, larg=1.4, duplo=False, amp=0.6)
    L.txt(44, 62, 'Esboco inicial do produto', tam=26, peso='bold')
    L.reta(44, 72, 400, 72, cor='#d9a520', larg=3.0, duplo=False)
    L.txt(44, 92, 'Etiqueta antifurto que o proprio cliente libera depois de pagar.',
          tam=13.5, cor='#555555')
    L.txt(W - 44, 62, 'Projeto de Produto e Processo | Poli-USP',
          tam=12.5, anc='end', cor='#777777')

    P = ns['P']
    E = 3.4
    qs = []

    q = Quadro(L, 40, 112, 470, 452, 'A) planta', esc=E, oy=0.56)
    planta(q, ns); qs.append(('A planta', q))

    q = Quadro(L, 40, 578, 470, 250, 'B) frontal - onde entra a camisa',
               esc=E, cy_mm=P['alt'] / 2, oy=0.56)
    frontal(q, ns); qs.append(('B frontal', q))

    q = Quadro(L, 526, 578, 372, 250, 'C) lateral', esc=E,
               cy_mm=P['alt'] / 2, oy=0.56)
    lateral(q, ns); qs.append(('C lateral', q))

    q = Quadro(L, 526, 112, 372, 452, 'D) perspectiva', esc=1.75, oy=0.50)
    perspectiva(q, ns); qs.append(('D perspectiva', q))

    q = Quadro(L, 914, 112, 446, 452, 'E) detalhe - como a garra solta',
               esc=3.6, oy=0.44)
    detalhe(q, ns); qs.append(('E detalhe', q))

    q = Quadro(L, 914, 578, 446, 250, 'F) fluxo de uso')
    fluxo(q); qs.append(('F fluxo', q))

    legenda(L, ns, 40, 842, 858, 118)
    L.txt(914, 862, 'medidas em milimetros', tam=11.5, cor='#9d9d9d')
    L.txt(914, 882, 'tracado a mao livre - representacao inicial', tam=11.5, cor='#9d9d9d')
    L.txt(914, 902, 'gerado por desenhos/esboco.py', tam=11.5, cor='#9d9d9d')

    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
           'viewBox="0 0 %d %d">%s</svg>' % (W, H, W, H, ''.join(L.out)))
    io.open(SVG, 'w', encoding='utf-8').write(svg)
    io.open(HTML, 'w', encoding='utf-8').write(
        '<body style="margin:0;background:#e9e6de;padding:12px">'
        + svg.replace('<svg ', '<svg style="width:100%;height:auto;display:block;'
                               'box-shadow:0 2px 18px rgba(0,0,0,.18)" ', 1)
        + '</body>')
    return qs, len(svg)


if __name__ == '__main__':
    qs, n = gerar()
    print('esboco: %s  (%.0f KB)' % (SVG, n / 1024.0))
    print()
    print('vazamento por quadro:')
    ruim = 0
    for nome, q in qs:
        v = q.vazou()
        print('  %-15s %s' % (nome, v if v else 'ok'))
        if v:
            ruim += 1
    print()
    print('%d de %d quadros com vazamento' % (ruim, len(qs)))
