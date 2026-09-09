# -*- coding: utf-8 -*-
"""
RAIO-X - o produto so em linha, sem texto e sem cota
Projeto de Produto e Processo | Poli-USP

RODAR:  python desenhos/raiox.py
SAIDA:  desenhos/raiox.svg
        desenhos/raiox.pdf
        desenhos/raiox.html

O QUE E'
--------
Tres vistas do dispositivo em aspecto de radiografia: fundo escuro, tracado
luminoso e translucido, e as pecas internas visiveis atraves da carcaca.
Nenhuma palavra, nenhuma cota, nenhuma linha de chamada - so a forma.

O tracado e' proposital e assumidamente torto: amplitude de ruido alta,
tremor grosso, sem repasse de limpeza. E' desenho de mao, nao de regua.

O brilho e' feito por camadas: o mesmo caminho e' desenhado tres vezes,
do mais largo e apagado ao mais fino e claro. Funciona igual em SVG e em
PDF, sem depender de filtro de desfoque - que o PDF nao teria.

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

SVG = os.path.join(AQUI, 'raiox.svg')
PDF = os.path.join(AQUI, 'raiox.pdf')
HTML = os.path.join(AQUI, 'raiox.html')

FUNDO   = (0.031, 0.071, 0.106)   # azul quase preto
CASCA   = (0.62, 0.93, 1.00)      # ciano claro - o contorno externo
INTERNO = (0.42, 0.78, 0.92)      # pecas internas, mais apagadas
OSSO    = (0.86, 0.97, 1.00)      # pino e garra - o que e' metal
CARNE   = (0.95, 0.55, 0.42)      # o tecido, unico ponto quente


class Raio(Tela):
    """Tela com tracado luminoso e bem mais torto."""

    def brilho(self, pts, cor=CASCA, larg=1.6, fechar=False, amp=2.2):
        """Tres passadas: larga e apagada, media, fina e clara."""
        if fechar:
            pts = list(pts) + [pts[0]]
        # caminho curto recebe menos tremor, pela mesma razao dos circulos
        ext = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
                  for i in range(len(pts) - 1))
        amp = min(amp, max(0.3, ext * 0.035))
        for mult, op, damp in ((5.0, 0.10, 1.5), (2.2, 0.22, 1.1), (1.0, 0.95, 1.0)):
            self.path(pts, cor=cor, larg=larg * mult, duplo=False,
                      op=op, amp=amp * damp)

    def brilho_circ(self, cx, cy, r, **k):
        # o tremor tem de acompanhar o tamanho: 3 mm de ruido num circulo de
        # 5 px de raio nao vira desenho torto, vira borrao.
        k.setdefault('amp', max(0.35, min(2.2, r * 0.16)))
        n = max(18, int(r * 1.4))
        self.brilho([(cx + r * math.cos(2 * math.pi * i / n),
                      cy + r * math.sin(2 * math.pi * i / n))
                     for i in range(n)], fechar=True, **k)


def svg_escuro(T):
    s = T.svg()
    # o fundo claro herdado da Tela vira o fundo da radiografia
    i = s.index('<rect')
    j = s.index('/>', i) + 2
    fundo = ('<rect width="%d" height="%d" fill="rgb(%d,%d,%d)"/>'
             % ((T.w, T.h) + tuple(int(v * 255) for v in FUNDO)))
    return s[:i] + fundo + s[j:]


# ============================================================================
# AS TRES VISTAS
# ============================================================================

def vista_planta(T, ns, cx, cy, e):
    P, UI, FUROS = ns['P'], ns['UI'], ns['FUROS']
    a, b = P['larg'] / 2, P['prof'] / 2

    def p(x, y):
        return (cx + x * e, cy - y * e)

    T.brilho([p(-a, -b), p(a, -b), p(a, b), p(-a, b)], fechar=True, larg=2.0)
    T.brilho([p(-a + 2.4, -b + 2.4), p(a - 2.4, -b + 2.4),
              p(a - 2.4, b - 2.4), p(-a + 2.4, b - 2.4)],
             fechar=True, cor=INTERNO, larg=1.0, amp=1.6)

    qw, qh, qx, qy = UI['qr']
    T.brilho([p(qx - qw / 2, qy - qh / 2), p(qx + qw / 2, qy - qh / 2),
              p(qx + qw / 2, qy + qh / 2), p(qx - qw / 2, qy + qh / 2)],
             fechar=True, larg=1.3, amp=1.8)
    for i in range(5):
        for j in range(5):
            if (i * 3 + j * 5 + i * j) % 4 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 5, qy - qh / 2 + j * qh / 5
                T.brilho([p(x0 + 1, y0 + 1), p(x0 + qw / 5 - 1, y0 + 1),
                          p(x0 + qw / 5 - 1, y0 + qh / 5 - 1), p(x0 + 1, y0 + qh / 5 - 1)],
                         fechar=True, cor=INTERNO, larg=0.7, amp=1.2)

    px, py = p(*UI['xy_led'])
    T.brilho_circ(px, py, UI['furo_led'] * e / 2, larg=1.2)
    px, py = p(*UI['xy_botao'])
    T.brilho_circ(px, py, UI['furo_botao'] * e / 2, larg=1.8)
    T.brilho_circ(px, py, UI['furo_botao'] * e / 2 - 3.5, cor=INTERNO, larg=0.9)
    for fx, fy in FUROS:
        px, py = p(fx, fy)
        T.brilho_circ(px, py, 4.2 * e / 2, cor=OSSO, larg=1.1)

    # o que esta por dentro, visto de cima
    gx, gy = ns['XY_GARRA']
    px, py = p(gx, gy)
    T.brilho_circ(px, py, ns['GARRA']['diam'] * e / 2, cor=OSSO, larg=1.4)
    T.brilho_circ(px, py, 2.4 * e / 2, cor=OSSO, larg=1.0)
    for nome, (lx, ly, lz) in ns['COMP'].items():
        if nome not in ns['POS'] or nome == 'botao':
            continue
        ox, oy, _ = ns['POS'][nome]
        T.brilho([p(ox - lx / 2, oy - ly / 2), p(ox + lx / 2, oy - ly / 2),
                  p(ox + lx / 2, oy + ly / 2), p(ox - lx / 2, oy + ly / 2)],
                 fechar=True, cor=INTERNO, larg=0.9, amp=1.9)
    sx, sy = ns['XY_ATUADOR'][ns['MECANISMO']]
    ax, ay, _ = ns['MEC'][ns['MECANISMO']]['peca']
    T.brilho([p(sx - ax / 2, sy - ay / 2), p(sx + ax / 2, sy - ay / 2),
              p(sx + ax / 2, sy + ay / 2), p(sx - ax / 2, sy + ay / 2)],
             fechar=True, cor=INTERNO, larg=1.0, amp=1.9)


def vista_frontal(T, ns, cx, cy, e):
    P, PINO, TEC, GAR = ns['P'], ns['PINO'], ns['TECIDO'], ns['GARRA']
    a, H, zs, t = P['larg'] / 2, P['alt'], P['z_split'], P['t_parede']

    def p(x, z):
        return (cx + x * e, cy - (z - H / 2) * e)

    T.brilho([p(-a, zs), p(a, zs), p(a, H), p(-a, H)], fechar=True, larg=1.9)
    T.brilho([p(-a, 0), p(a, 0), p(a, zs), p(-a, zs)], fechar=True, larg=1.9)

    te = TEC['esp'] * 4.0
    tw = P['larg'] * 0.84
    T.brilho([p(-tw / 2, 0), p(tw / 2, 0), p(tw / 2, -te), p(-tw / 2, -te)],
             fechar=True, cor=CARNE, larg=1.5, amp=2.6)

    dw, dh = PINO['d_cabeca'], PINO['t_cabeca'] * 4.0
    T.brilho([p(-dw / 2, -te), p(dw / 2, -te), p(dw / 2, -te - dh), p(-dw / 2, -te - dh)],
             fechar=True, cor=OSSO, larg=1.5)
    hw = PINO['d_haste'] * 1.8
    T.brilho([p(-hw / 2, -te), p(hw / 2, -te), p(hw / 2, PINO['h_haste'] - te),
              p(-hw / 2, PINO['h_haste'] - te)], fechar=True, cor=OSSO, larg=1.3)

    gw, gh = GAR['diam'], GAR['alt']
    T.brilho([p(-gw / 2, t), p(gw / 2, t), p(gw / 2, t + gh), p(-gw / 2, t + gh)],
             fechar=True, cor=OSSO, larg=1.4)
    # as tres esferas dentro da garra
    for dx in (-3.4, 0, 3.4):
        px, py = p(dx, t + gh * 0.55)
        T.brilho_circ(px, py, 1.5 * e, cor=OSSO, larg=1.0)

    zc = t + gh + ns['BUCHA']['alt']
    CU = ns['CUR']
    T.brilho([p(-CU['larg'] / 2, zc), p(CU['larg'] / 2, zc),
              p(CU['larg'] / 2, zc + CU['t_fino'] + GAR['curso']),
              p(-CU['larg'] / 2, zc + CU['t_fino'])], fechar=True,
             cor=INTERNO, larg=1.1, amp=1.8)

    for nome in ('bateria', 'carga', 'mcu'):
        if nome not in ns['POS']:
            continue
        lx, ly, lz = ns['COMP'][nome]
        ox, oy, oz = ns['POS'][nome]
        T.brilho([p(ox - lx / 2, oz), p(ox + lx / 2, oz),
                  p(ox + lx / 2, oz + lz), p(ox - lx / 2, oz + lz)],
                 fechar=True, cor=INTERNO, larg=0.9, amp=1.7)


def vista_perspectiva(T, ns, cx, cy, e):
    P, UI = ns['P'], ns['UI']
    a, b, h = P['larg'] / 2, P['prof'] / 2, P['alt']
    ca, sa = 0.866, 0.5

    def iso(x, y, z):
        return (cx + (x - y) * ca * e, cy - ((x + y) * sa - z * 1.2) * e)

    # a caixa inteira, inclusive as arestas escondidas: e' raio-x
    cantos = [(-a, -b), (a, -b), (a, b), (-a, b)]
    T.brilho([iso(x, y, h) for x, y in cantos], fechar=True, larg=1.8)
    T.brilho([iso(x, y, 0) for x, y in cantos], fechar=True, cor=INTERNO,
             larg=1.1, amp=2.4)
    for x, y in cantos:
        T.brilho([iso(x, y, h), iso(x, y, 0)], larg=1.5)

    qw, qh, qx, qy = UI['qr']
    T.brilho([iso(qx - qw / 2, qy - qh / 2, h), iso(qx + qw / 2, qy - qh / 2, h),
              iso(qx + qw / 2, qy + qh / 2, h), iso(qx - qw / 2, qy + qh / 2, h)],
             fechar=True, larg=1.2, amp=1.8)
    for i in range(4):
        for j in range(4):
            if (i + j * 3) % 3 < 2:
                x0, y0 = qx - qw / 2 + i * qw / 4, qy - qh / 2 + j * qh / 4
                T.brilho([iso(x0 + 1.4, y0 + 1.4, h), iso(x0 + qw / 4 - 1.4, y0 + 1.4, h),
                          iso(x0 + qw / 4 - 1.4, y0 + qh / 4 - 1.4, h),
                          iso(x0 + 1.4, y0 + qh / 4 - 1.4, h)],
                         fechar=True, cor=INTERNO, larg=0.7, amp=1.2)

    px, py = iso(UI['xy_botao'][0], UI['xy_botao'][1], h)
    T.brilho_circ(px, py, UI['furo_botao'] * e / 2, larg=1.6)
    px, py = iso(UI['xy_led'][0], UI['xy_led'][1], h)
    T.brilho_circ(px, py, UI['furo_led'] * e / 2, larg=1.1)

    # o pino atravessando, visto por dentro
    gx, gy = ns['XY_GARRA']
    T.brilho([iso(gx, gy, -3), iso(gx, gy, ns['PINO']['h_haste'])],
             cor=OSSO, larg=1.4, amp=1.6)
    px, py = iso(gx, gy, ns['P']['t_parede'] + ns['GARRA']['alt'] / 2)
    T.brilho_circ(px, py, ns['GARRA']['diam'] * e / 2, cor=OSSO, larg=1.2)


# ============================================================================
# FOLHA
# ============================================================================

def gerar():
    ns = parametros()
    W, H = 1500, 560
    T = Raio(W, H, semente=771103)

    vista_planta(T, ns, 250, 285, 2.55)
    vista_frontal(T, ns, 750, 285, 2.55)
    vista_perspectiva(T, ns, 1230, 290, 1.85)

    io.open(SVG, 'w', encoding='utf-8').write(svg_escuro(T))
    io.open(PDF, 'wb').write(pdf_escuro(T))
    io.open(HTML, 'w', encoding='utf-8').write(
        '<body style="margin:0;background:#05090d">'
        + svg_escuro(T).replace('<svg ', '<svg style="width:100%;height:auto;'
                                         'display:block" ', 1) + '</body>')
    return W, H, len(T.prims)


def pdf_escuro(T):
    """O PDF da Tela pinta o fundo claro; aqui o fundo e' o da radiografia."""
    import esboco
    orig = esboco.PAPEL
    esboco.PAPEL = FUNDO
    try:
        return T.pdf()
    finally:
        esboco.PAPEL = orig


if __name__ == '__main__':
    w, h, n = gerar()
    print('raio-x gerado: %d x %d, %d tracos' % (w, h, n))
    for f in (SVG, PDF, HTML):
        print('   ' + os.path.basename(f))
    print()
    print('sem texto, sem cota, sem linha de chamada - so a forma')
