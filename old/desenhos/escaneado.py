# -*- coding: utf-8 -*-
"""
ESCANEADO - o esboco como se fosse folha de papel passada no escaner
Projeto de Produto e Processo | Poli-USP

RODAR:  python desenhos/escaneado.py
SAIDA:  desenhos/escaneado.svg
        desenhos/escaneado.pdf
        desenhos/escaneado.html

O QUE E'
--------
Tres vistas do dispositivo, em preto e branco, com o aspecto de um desenho
feito a caneta e depois digitalizado. Nenhuma palavra, nenhuma cota,
nenhuma linha de chamada - so a forma.

O QUE FAZ PARECER ESCANEADO
---------------------------
Nao basta desenhar torto. O que denuncia um escaneamento sao quatro coisas,
e todas estao aqui:

1. PAPEL QUE NAO E BRANCO. Fundo levemente acinzentado, salpicado de graos
   escuros dispersos - o ruido que o sensor sempre captura.
2. TINTA QUE NAO E PRETA. Cada traco varia de densidade; alguns saem mais
   fracos, como caneta falhando.
3. CANTOS QUE SE CRUZAM. Quem desenha a mao passa do canto. As linhas se
   estendem um pouco alem do encontro, em vez de fechar exatamente.
4. FOLHA TORTA. A pagina inteira e' girada uma fracao de grau, porque
   ninguem apoia a folha perfeitamente alinhada no vidro.

As medidas continuam vindo de fusion/Antifurto.py.
"""

import io
import os
import sys
import math

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

from esboco import Tela, parametros            # noqa: E402

SVG = os.path.join(AQUI, 'escaneado.svg')
PDF = os.path.join(AQUI, 'escaneado.pdf')
HTML = os.path.join(AQUI, 'escaneado.html')

# Preto no branco, limpo. O fundo tem de ser branco de verdade: qualquer
# cinza vira uma caixa visivel no meio da pagina do relatorio.
PAPEL = (1.0, 1.0, 1.0)
TINTA = (0.0, 0.0, 0.0)
FRACA = (0.42, 0.42, 0.42)       # linha de apoio, o unico meio-tom
GRAO  = (0.72, 0.72, 0.72)

GRANULADO = False                # ruido de sensor: atrapalha na impressao
INCLINACAO = -0.55               # graus - a folha nunca fica reta no vidro


class Caneta(Tela):
    """Tela com tracado de caneta e as marcas do escaneamento."""

    def _estende(self, pts, quanto):
        """Empurra as pontas de cada segmento para alem do encontro.
        E' o que produz os cantos cruzados de desenho a mao."""
        if len(pts) < 2:
            return []
        saida = []
        if quanto <= 0:
            # sem passar do canto, mas ainda devolvendo SEGMENTOS - quem
            # chama itera sobre segmentos, nao sobre pontos
            return [[pts[i], pts[i + 1]] for i in range(len(pts) - 1)]
        for i in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[i], pts[i + 1]
            d = math.hypot(x2 - x1, y2 - y1) or 1.0
            ux, uy = (x2 - x1) / d, (y2 - y1) / d
            a = quanto * (0.4 + self._r())
            b = quanto * (0.4 + self._r())
            saida.append([(x1 - ux * a, y1 - uy * a), (x2 + ux * b, y2 + uy * b)])
        return saida

    def tinta(self, pts, larg=1.7, fechar=False, amp=1.6, passadas=2,
              alem=2.6, fraca=False):
        """Cada segmento vira um risco proprio, com peso e densidade
        variaveis - caneta de verdade nao mantem pressao constante."""
        if fechar:
            pts = list(pts) + [pts[0]]
        for seg in self._estende(pts, alem):
            for k in range(passadas):
                cor = FRACA if (fraca or self._r() < 0.12) else TINTA
                w = larg * (0.72 + 0.55 * self._r()) * (1.0 if k == 0 else 0.7)
                op = (0.92 if k == 0 else 0.42) * (0.55 if cor is FRACA else 1.0)
                self.path(seg, cor=cor, larg=w, duplo=False, op=op, amp=amp)

    def tinta_circ(self, cx, cy, r, larg=1.7, **k):
        # tremor proporcional ao raio: senao o circulo pequeno vira borrao
        k.setdefault('amp', max(0.3, min(1.6, r * 0.14)))
        k.setdefault('alem', 0.0)            # circulo nao tem canto para passar
        n = max(20, int(r * 1.6))
        # abre um pouco o arco, como quem nao fecha o circulo direito
        falta = int(n * 0.04) + 1
        pts = [(cx + r * math.cos(2 * math.pi * i / n),
                cy + r * math.sin(2 * math.pi * i / n))
               for i in range(n - falta)]
        self.tinta(pts, larg=larg, **k)

    def flecha_mao(self, x1, y1, x2, y2, larg=1.8, cabeca=9.0):
        """Seta rabiscada: haste e duas barbas, cada uma com seu proprio
        tremor. Indica movimento sem precisar de legenda."""
        import math as _m
        self.tinta([(x1, y1), (x2, y2)], larg=larg, amp=0.9, alem=1.2)
        a = _m.atan2(y2 - y1, x2 - x1)
        for k in (+1, -1):
            self.tinta([(x2, y2),
                        (x2 - cabeca * _m.cos(a + k * 0.42),
                         y2 - cabeca * _m.sin(a + k * 0.42))],
                       larg=larg * 0.9, amp=0.6, alem=0.8, passadas=1)

    def graos(self, n=900):
        """O ruido do sensor: pontinhos escuros espalhados pela folha."""
        for _ in range(n):
            x, y = self._r() * self.w, self._r() * self.h
            r = 0.35 + self._r() * 0.75
            op = 0.05 + self._r() * 0.22
            self.path([(x, y), (x + r, y)], cor=GRAO, larg=r * 1.7,
                      duplo=False, op=op, amp=0.0)

    def sombra_borda(self):
        """A faixa escura que aparece quando a tampa nao encosta na folha."""
        for i in range(14):
            t = i / 14.0
            op = 0.05 * (1 - t) ** 2
            self.path([(0, self.h - i * 2.2), (self.w, self.h - i * 2.2)],
                      cor=GRAO, larg=2.4, duplo=False, op=op, amp=0.0)
            self.path([(self.w - i * 2.2, 0), (self.w - i * 2.2, self.h)],
                      cor=GRAO, larg=2.4, duplo=False, op=op, amp=0.0)


def envolver(corpo, w, h, ang):
    return ('<g transform="rotate(%.3f %.1f %.1f)">%s</g>'
            % (ang, w / 2.0, h / 2.0, corpo))


def svg_papel(T):
    s = T.svg()
    i = s.index('<rect')
    j = s.index('/>', i) + 2
    fundo = ('<rect width="%d" height="%d" fill="rgb(%d,%d,%d)"/>'
             % ((T.w, T.h) + tuple(int(v * 255) for v in PAPEL)))
    corpo = s[j:s.rindex('</svg>')]
    return s[:i] + fundo + envolver(corpo, T.w, T.h, INCLINACAO) + '</svg>'


# ============================================================================
# AS TRES VISTAS
# ============================================================================

def vista_planta(T, ns, cx, cy, e):
    P, UI, FUROS = ns['P'], ns['UI'], ns['FUROS']
    a, b = P['larg'] / 2, P['prof'] / 2

    def p(x, y):
        return (cx + x * e, cy - y * e)

    T.tinta([p(-a, -b), p(a, -b), p(a, b), p(-a, b)], fechar=True, larg=2.1, alem=3.4)
    T.tinta([p(-a + 2.4, -b + 2.4), p(a - 2.4, -b + 2.4),
             p(a - 2.4, b - 2.4), p(-a + 2.4, b - 2.4)],
            fechar=True, larg=1.0, amp=1.1, alem=1.6, fraca=True)

    qw, qh, qx, qy = UI['qr']
    T.tinta([p(qx - qw / 2, qy - qh / 2), p(qx + qw / 2, qy - qh / 2),
             p(qx + qw / 2, qy + qh / 2), p(qx - qw / 2, qy + qh / 2)],
            fechar=True, larg=1.5, alem=2.2)
    for i in range(5):
        for j in range(5):
            if (i * 3 + j * 5 + i * j) % 4 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 5, qy - qh / 2 + j * qh / 5
                q = [p(x0 + 0.8, y0 + 0.8), p(x0 + qw / 5 - 0.8, y0 + 0.8),
                     p(x0 + qw / 5 - 0.8, y0 + qh / 5 - 0.8), p(x0 + 0.8, y0 + qh / 5 - 0.8)]
                T.tinta(q, fechar=True, larg=0.9, amp=0.7, alem=0.8)
                # rabiscado por dentro, como quem preenche a caneta
                for k in range(4):
                    t = (k + 0.5) / 4.0
                    T.tinta([(q[0][0] + (q[1][0] - q[0][0]) * t, q[0][1]),
                             (q[3][0] + (q[2][0] - q[3][0]) * t, q[3][1])],
                            larg=1.0, amp=0.5, alem=0.6, passadas=1)

    px, py = p(*UI['xy_led'])
    T.tinta_circ(px, py, UI['furo_led'] * e / 2, larg=1.3)
    px, py = p(*UI['xy_botao'])
    T.tinta_circ(px, py, UI['furo_botao'] * e / 2, larg=1.9)
    T.tinta_circ(px, py, UI['furo_botao'] * e / 2 - 3.5, larg=1.0, fraca=True)
    for fx, fy in FUROS:
        px, py = p(fx, fy)
        T.tinta_circ(px, py, 4.2 * e / 2, larg=1.2)
        T.tinta([(px - 3, py), (px + 3, py)], larg=1.0, amp=0.4, alem=0.8)

    # o que esta por dentro - linha fraca, como quem esbocou por baixo
    gx, gy = ns['XY_GARRA']
    px, py = p(gx, gy)
    T.tinta_circ(px, py, ns['GARRA']['diam'] * e / 2, larg=1.3)
    T.tinta_circ(px, py, 2.4 * e / 2, larg=1.0)
    for nome, (lx, ly, lz) in ns['COMP'].items():
        if nome not in ns['POS'] or nome == 'botao':
            continue
        ox, oy, _ = ns['POS'][nome]
        T.tinta([p(ox - lx / 2, oy - ly / 2), p(ox + lx / 2, oy - ly / 2),
                 p(ox + lx / 2, oy + ly / 2), p(ox - lx / 2, oy + ly / 2)],
                fechar=True, larg=1.0, amp=1.2, alem=1.8, fraca=True)
    sx, sy = ns['XY_ATUADOR'][ns['MECANISMO']]
    ax, ay, _ = ns['MEC'][ns['MECANISMO']]['peca']
    T.tinta([p(sx - ax / 2, sy - ay / 2), p(sx + ax / 2, sy - ay / 2),
             p(sx + ax / 2, sy + ay / 2), p(sx - ax / 2, sy + ay / 2)],
            fechar=True, larg=1.1, amp=1.2, alem=1.8, fraca=True)


def vista_frontal(T, ns, cx, cy, e):
    P, PINO, TEC, GAR = ns['P'], ns['PINO'], ns['TECIDO'], ns['GARRA']
    a, H, zs, t = P['larg'] / 2, P['alt'], P['z_split'], P['t_parede']

    def p(x, z):
        return (cx + x * e, cy - (z - H / 2) * e)

    T.tinta([p(-a, zs), p(a, zs), p(a, H), p(-a, H)], fechar=True, larg=2.0, alem=3.2)
    T.tinta([p(-a, 0), p(a, 0), p(a, zs), p(-a, zs)], fechar=True, larg=2.0, alem=3.2)

    # o tecido, hachurado a caneta
    te = TEC['esp'] * 4.5
    tw = P['larg'] * 0.84
    quad = [p(-tw / 2, 0), p(tw / 2, 0), p(tw / 2, -te), p(-tw / 2, -te)]
    T.tinta(quad, fechar=True, larg=1.4, alem=2.4)
    n = 26
    for i in range(n):
        x0 = -tw / 2 + tw * i / float(n)
        T.tinta([p(x0, 0), p(x0 - te * 0.9, -te)], larg=0.9, amp=0.6,
                alem=0.8, passadas=1)

    dw, dh = PINO['d_cabeca'], PINO['t_cabeca'] * 4.5
    T.tinta([p(-dw / 2, -te), p(dw / 2, -te), p(dw / 2, -te - dh), p(-dw / 2, -te - dh)],
            fechar=True, larg=1.6, alem=2.2)
    hw = PINO['d_haste'] * 1.8
    T.tinta([p(-hw / 2, -te), p(hw / 2, -te), p(hw / 2, PINO['h_haste'] - te),
             p(-hw / 2, PINO['h_haste'] - te)], fechar=True, larg=1.4, alem=1.6)

    gw, gh = GAR['diam'], GAR['alt']
    T.tinta([p(-gw / 2, t), p(gw / 2, t), p(gw / 2, t + gh), p(-gw / 2, t + gh)],
            fechar=True, larg=1.5, alem=2.0)
    for dx in (-3.4, 0, 3.4):
        px, py = p(dx, t + gh * 0.55)
        T.tinta_circ(px, py, 1.5 * e, larg=1.1)

    zc = t + gh + ns['BUCHA']['alt']
    CU = ns['CUR']
    T.tinta([p(-CU['larg'] / 2, zc), p(CU['larg'] / 2, zc),
             p(CU['larg'] / 2, zc + CU['t_fino'] + GAR['curso']),
             p(-CU['larg'] / 2, zc + CU['t_fino'])], fechar=True, larg=1.2,
            amp=1.2, alem=1.6)

    for nome in ('bateria', 'carga', 'mcu'):
        if nome not in ns['POS']:
            continue
        lx, ly, lz = ns['COMP'][nome]
        ox, oy, oz = ns['POS'][nome]
        T.tinta([p(ox - lx / 2, oz), p(ox + lx / 2, oz),
                 p(ox + lx / 2, oz + lz), p(ox - lx / 2, oz + lz)],
                fechar=True, larg=1.0, amp=1.1, alem=1.6, fraca=True)


def vista_perspectiva(T, ns, cx, cy, e):
    P, UI = ns['P'], ns['UI']
    a, b, h = P['larg'] / 2, P['prof'] / 2, P['alt']
    ca, sa = 0.866, 0.5

    def iso(x, y, z):
        return (cx + (x - y) * ca * e, cy - ((x + y) * sa - z * 1.2) * e)

    cantos = [(-a, -b), (a, -b), (a, b), (-a, b)]
    T.tinta([iso(x, y, h) for x, y in cantos], fechar=True, larg=2.0, alem=3.4)
    for x, y in ((a, -b), (a, b), (-a, b)):
        T.tinta([iso(x, y, h), iso(x, y, 0)], larg=1.8, alem=2.6)
    T.tinta([iso(a, -b, 0), iso(a, b, 0), iso(-a, b, 0)], larg=1.8, alem=2.6)
    # a aresta escondida, esbocada fraco
    T.tinta([iso(-a, -b, h), iso(-a, -b, 0)], larg=0.9, alem=1.2, fraca=True)

    qw, qh, qx, qy = UI['qr']
    T.tinta([iso(qx - qw / 2, qy - qh / 2, h), iso(qx + qw / 2, qy - qh / 2, h),
             iso(qx + qw / 2, qy + qh / 2, h), iso(qx - qw / 2, qy + qh / 2, h)],
            fechar=True, larg=1.4, alem=2.0)
    for i in range(4):
        for j in range(4):
            if (i + j * 3) % 3 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 4, qy - qh / 2 + j * qh / 4
                T.tinta([iso(x0 + 1.2, y0 + 1.2, h), iso(x0 + qw / 4 - 1.2, y0 + 1.2, h),
                         iso(x0 + qw / 4 - 1.2, y0 + qh / 4 - 1.2, h),
                         iso(x0 + 1.2, y0 + qh / 4 - 1.2, h)],
                        fechar=True, larg=1.0, amp=0.7, alem=0.9)

    px, py = iso(UI['xy_botao'][0], UI['xy_botao'][1], h)
    T.tinta_circ(px, py, UI['furo_botao'] * e / 2, larg=1.7)
    px, py = iso(UI['xy_led'][0], UI['xy_led'][1], h)
    T.tinta_circ(px, py, UI['furo_led'] * e / 2, larg=1.2)


def vista_detalhe(T, ns, cx, cy, e):
    """A garra por dentro, ampliada. Sem uma palavra: o texto da secao
    explica, o desenho so mostra.

    A ordem vertical segue a do modelo: garra embaixo, bucha em cima dela
    e cursor por cima de tudo. O cursor empurra a bucha para BAIXO, e e'
    isso que solta o pino.
    """
    GAR = ns['GARRA']

    def p(x, y):
        return (cx + x * e, cy - y * e)

    # --- copo conico, aberto para cima ---
    T.tinta([p(-17, 20), p(-9.5, 0)], larg=2.0, alem=2.6)
    T.tinta([p(9.5, 0), p(17, 20)], larg=2.0, alem=2.6)
    T.tinta([p(-9.5, 0), p(9.5, 0)], larg=1.6, alem=2.0)

    # --- carretel, no fundo, e a mola que o empurra ---
    T.tinta([p(-8, 0), p(8, 0), p(8, 5), p(-8, 5)], fechar=True,
            larg=1.7, alem=2.2)
    mx = -12.5
    pts = [p(mx, 0)]
    for i in range(7):
        pts.append(p(mx + (2.0 if i % 2 == 0 else -2.0), 0.6 + (i + 1) * 1.4))
    pts.append(p(mx, 11))
    T.tinta(pts, larg=1.2, amp=0.7, alem=0.8, passadas=1)
    T.tinta([p(mx - 3.4, 11), p(mx + 3.4, 11)], larg=1.3, alem=1.4)

    # --- tres esferas apertadas contra a haste ---
    for dx in (-6.2, 0, 6.2):
        px, py = p(dx, 8.4)
        T.tinta_circ(px, py, 3.1 * e, larg=1.5)

    # --- haste do pino, subindo pelo meio ---
    T.tinta([p(-1.1, 0), p(-1.1, 30)], larg=1.4, alem=1.4)
    T.tinta([p(1.1, 0), p(1.1, 30)], larg=1.4, alem=1.4)

    # --- bucha, acima do carretel, abracando a haste ---
    for lado in (-1, 1):
        T.tinta([p(lado * 1.9, 13), p(lado * 6.5, 13),
                 p(lado * 6.5, 17.5), p(lado * 1.9, 17.5)],
                fechar=True, larg=1.6, alem=2.0)

    # --- cursor com rampa, por cima, correndo na horizontal ---
    T.tinta([p(-30, 19), p(20, 19), p(20, 25), p(-22, 25)],
            fechar=True, larg=1.8, alem=2.6)

    # --- as duas setas do acionamento ---
    a1, a2 = p(35, 22), p(23, 22)
    T.flecha_mao(a1[0], a1[1], a2[0], a2[1], larg=2.0, cabeca=10)
    b1, b2 = p(11.5, 18.5), p(11.5, 11.5)
    T.flecha_mao(b1[0], b1[1], b2[0], b2[1], larg=1.8, cabeca=8)


# ============================================================================
# FOLHA
# ============================================================================

def gerar():
    ns = parametros()
    W, H = 1500, 640
    T = Caneta(W, H, semente=4471903)

    if GRANULADO:
        T.graos(1100)
    vista_planta(T, ns, 272, 322, 3.55)
    vista_frontal(T, ns, 762, 322, 3.55)
    vista_perspectiva(T, ns, 1232, 330, 2.55)
    if GRANULADO:
        T.sombra_borda()

    io.open(SVG, 'w', encoding='utf-8').write(svg_papel(T))
    io.open(PDF, 'wb').write(pdf_papel(T))
    io.open(HTML, 'w', encoding='utf-8').write(
        '<body style="margin:0;background:#8b8880;padding:18px">'
        + svg_papel(T).replace('<svg ', '<svg style="width:100%;height:auto;display:block;'
                                        'box-shadow:0 3px 22px rgba(0,0,0,.35)" ', 1)
        + '</body>')
    n_det = folha_detalhe(ns)
    return W, H, len(T.prims), n_det


def folha_detalhe(ns):
    """O detalhe do mecanismo em folha propria, no mesmo estilo."""
    W, H = 720, 560
    T = Caneta(W, H, semente=9930517)
    if GRANULADO:
        T.graos(520)
    vista_detalhe(T, ns, 330, 300, 7.4)
    if GRANULADO:
        T.sombra_borda()
    base = os.path.join(AQUI, 'escaneado-detalhe')
    io.open(base + '.svg', 'w', encoding='utf-8').write(svg_papel(T))
    io.open(base + '.pdf', 'wb').write(pdf_papel(T))
    return len(T.prims)


def pdf_papel(T):
    """O PDF herda o fundo da Tela; aqui e' o cinza do papel."""
    import esboco
    orig = esboco.PAPEL
    esboco.PAPEL = PAPEL
    try:
        return T.pdf()
    finally:
        esboco.PAPEL = orig


if __name__ == '__main__':
    w, h, n, n_det = gerar()
    print('escaneado: %d x %d, %d tracos' % (w, h, n))
    for f in (SVG, PDF, HTML, 'escaneado-detalhe.svg', 'escaneado-detalhe.pdf'):
        print('   ' + os.path.basename(f))
    print('detalhe do mecanismo: %d tracos' % n_det)
    print()
    print('preto e branco, sem texto, sem cota - folha girada %.2f grau' % INCLINACAO)
