"""Modelos detalhados das peças compradas, nas posições da caixa compacta (v3).

Só para a maquete e para a checagem de colisão. Medidas: research_notes/Medidas reais/medidas.md
Cada peça é uma lista de (cor, sólido) para a maquete mostrar as cores reais.
"""
import numpy as np
from manifold3d import Manifold
import tagandgo_v2 as M
import tagandgo_v3 as C
from tagandgo_v2 import cubo, cil, uniao

SEG = 40


def esfera(x, y, z, d):
    return Manifold.sphere(d / 2, 16).translate([x, y, z])


def tubo(pts, d):
    """Fio: casca convexa entre esferas consecutivas."""
    ps = [esfera(*p, d) for p in pts]
    return uniao([Manifold.batch_hull([ps[i], ps[i + 1]]) for i in range(len(ps) - 1)])


def caixa_arred(x0, y0, z0, x1, y1, z1, r):
    """Caixa com cantos arredondados em planta."""
    pts = []
    for (cx, cy) in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x1 - r, y1 - r), (x0 + r, y1 - r)):
        pts.append(cil(cx, cy, z0, z1, 2 * r, 24))
    return Manifold.batch_hull(pts)


# ---------------- servo SG90 (no referencial do módulo v2; depois P()) ----------------
def servo_sg90(z_or=None):
    s = M.SERVO
    zb = (M.Z_ORELHA if z_or is None else z_or) - 15.9      # fundo do servo
    bx0 = M.SX - s['eixo_ponta']
    bx1 = bx0 + 22.7
    cx = (bx0 + bx1) / 2
    y0, y1 = M.SY - 6.1, M.SY + 6.1
    corpo = cubo(bx0, y0, zb, bx1, y1, zb + 22.7)
    orelha = cubo(cx - 16.15, y0, zb + 15.9, cx + 16.15, y1, zb + 18.4)
    for sx in (-1, 1):
        a, b = cx + sx * 13.97, cx + sx * 16.2
        orelha = orelha - cil(a, M.SY, zb + 15, zb + 19, 2.0) - cubo(min(a, b), M.SY - 0.5, zb + 15, max(a, b), M.SY + 0.5, zb + 19)
    torre = cil(M.SX, M.SY, zb + 22.7, zb + 26.7, 11.8) + cil(bx0 + 13.5, M.SY, zb + 22.7, zb + 25.2, 6.0)
    eixo = cil(M.SX, M.SY, zb + 26.7, zb + 29.6, 4.8)
    etiqueta = cubo(bx0 - 0.01, y0 + 1.5, zb + 4, bx1 + 0.01, y1 - 1.5, zb + 12)
    fios = [('#7c2d12', tubo([(bx1, M.SY - 1.3, zb + 1.5), (bx1 + 6, M.SY - 1.3, zb + 1.5), (bx1 + 14, M.SY - 1.3, zb + 1.5)], 1.2)),
            ('#dc2626', tubo([(bx1, M.SY, zb + 1.5), (bx1 + 6, M.SY, zb + 1.5), (bx1 + 14, M.SY, zb + 1.5)], 1.2)),
            ('#f97316', tubo([(bx1, M.SY + 1.3, zb + 1.5), (bx1 + 6, M.SY + 1.3, zb + 1.5), (bx1 + 14, M.SY + 1.3, zb + 1.5)], 1.2))]
    return [('#2563eb', corpo + orelha), ('#1e40af', torre), ('#f1f5f9', eixo), ('#e2e8f0', etiqueta)] + fios


def braco_plastico():
    """Braço plástico de uma ponta do SG90, no referencial do pivô (gira com o servo)."""
    hub = cil(0, 0, -3.25, 0, 7.0)
    braco = Manifold.batch_hull([cil(0, 0, -1.6, 0, 6.0), cil(15.5, 0, -1.6, 0, 3.8)])
    for d in (6.0, 9.0, 12.0, 15.0):
        braco = braco - cil(d, 0, -2, 1, 1.1)
    return [('#f8fafc', hub + braco)]


# ---------------- ESP32 + expansor ----------------
def esp32_expansor():
    x0, y0, x1, y1 = C.POS_ESP
    x0 += 0.5
    y0 += 0.5
    zs = C.ZS
    L, W = M.EXP
    z_pcb = zs + 2.0
    pcb = cubo(x0, y0, z_pcb, x0 + L, y0 + W, z_pcb + 1.6)
    for hx, hy in ((3, 3), (L - 3, 3), (3, W - 3), (L - 3, W - 3)):
        pcb = pcb - cil(x0 + hx, y0 + hy, z_pcb - 1, z_pcb + 3, 3.4)
    zt = z_pcb + 1.6
    # ESP32 ao longo do comprimento, centrado; fileiras a 25,4
    ex0, ey0 = x0 + (L - 51.6) / 2 + 3.0, y0 + (W - 28.3) / 2
    yc = ey0 + 28.3 / 2
    fem = uniao([cubo(ex0 + 7.9, yc + s * 12.7 - 1.27, zt, ex0 + 7.9 + 38.1, yc + s * 12.7 + 1.27, zt + 8.5) for s in (-1, 1)])
    # fileiras S/V/G: 3 pinos para cada GPIO, por fora das fêmeas
    pinos = []
    for s in (-1, 1):
        for k in range(3):
            yy = yc + s * (12.7 + 4.0 + k * 2.54)
            pinos.append(cubo(ex0 + 7.9, yy - 1.27, zt, ex0 + 7.9 + 38.1, yy + 1.27, zt + 2.5))
            for i in range(15):
                pinos.append(cubo(ex0 + 9.0 + i * 2.54, yy - 0.32, zt + 2.5, ex0 + 9.64 + i * 2.54, yy + 0.32, zt + 8.5))
    conect = cubo(x0 - 1, y0 + 6, zt, x0 + 13, y0 + 15, zt + 11) + cubo(x0 - 1, y0 + 20, zt, x0 + 5, y0 + 28, zt + 3) + cubo(x0 - 1, y0 + 33, zt, x0 + 6.5, y0 + 42, zt + 3.2)
    reg = cubo(x0 + 6, y0 + W - 12, zt, x0 + 16, y0 + W - 3, zt + 4)
    ze = zt + 8.5
    epcb = cubo(ex0, ey0, ze, ex0 + 51.6, ey0 + 28.3, ze + 1.6)
    for hx in (2.8, 51.6 - 2.8):
        for hy in (2.65, 28.3 - 2.65):
            epcb = epcb - cil(ex0 + hx, ey0 + hy, ze - 1, ze + 3, 3.0)
    modulo = cubo(ex0 + 51.6 - 25.5, yc - 9, ze + 1.6, ex0 + 51.6, yc + 9, ze + 1.6 + 0.8)
    blind = cubo(ex0 + 51.6 - 25.5 + 1, yc - 8, ze + 2.4, ex0 + 51.6 - 7.2, yc + 8, ze + 4.7)
    usb = cubo(ex0 - 1.0, yc - 4.5, ze + 1.6, ex0 + 7.5, yc + 4.5, ze + 4.8)
    botoes = cubo(ex0 + 1, yc - 11, ze + 1.6, ex0 + 5, yc - 7, ze + 3.4) + cubo(ex0 + 1, yc + 7, ze + 1.6, ex0 + 5, yc + 11, ze + 3.4)
    chips = cubo(ex0 + 10, yc - 5, ze + 1.6, ex0 + 16, yc + 1, ze + 2.8) + cubo(ex0 + 18, yc + 4, ze + 1.6, ex0 + 24, yc + 9, ze + 3.2)
    return [('#b91c1c', pcb), ('#111827', fem + conect), ('#d4a017', uniao(pinos)), ('#334155', reg),
            ('#1e3a8a', epcb), ('#111827', modulo), ('#cbd5e1', blind + usb), ('#e5e7eb', botoes), ('#0f172a', chips)]


# ---------------- power bank ELG PB102BK ----------------
def power_bank():
    x0, y0, x1, y1 = C.POS_PB
    x0, y0, x1, y1 = x0 + 0.5, y0 + 0.5, x1 - 0.5, y1 - 0.5
    z0, z1 = C.QI_E, C.QI_E + 15.0
    corpo = caixa_arred(x0, y0, z0, x1, y1, z1, 4.0)
    portas = []
    yc = (y0 + y1) / 2
    for dy, w, h in ((-18, 13.2, 5.6), (0, 9.0, 3.3), (18, 13.2, 5.6)):     # USB-A, USB-C, USB-A na face curta
        portas.append(cubo(x0 - 0.01, yc + dy - w / 2, z0 + 7.5 - h / 2, x0 + 8, yc + dy + w / 2, z0 + 7.5 + h / 2))
    micro = cubo(x0 + 12, y0 - 0.01, z0 + 6, x0 + 20, y0 + 6, z0 + 9)
    corpo = corpo - uniao(portas) - micro
    visor = cubo(x0 + 22, yc - 8, z1 - 0.2, x0 + 38, yc + 8, z1 + 0.05)
    botao = cubo(x0 + 30, y1 - 0.5, z0 + 5, x0 + 38, y1 + 0.3, z0 + 10)
    logo = cubo(x0 + 70, yc - 6, z1 - 0.1, x0 + 100, yc + 6, z1 + 0.04)
    return [('#111827', corpo), ('#0ea5e9', visor), ('#374151', botao), ('#4b5563', logo)]


# ---------------- receptor Qi ----------------
def receptor_qi():
    """Folha Qi centrada embaixo do power bank, sobre a bobina; rabicho até o micro-USB do power bank."""
    x0, y0 = C.QI_POS
    folha = cubo(x0, y0, 0, x0 + 75, y0 + 45, 0.6)
    aneis = uniao([cil(x0 + 37.5, y0 + 22.5, 0.6, 0.9, d, 48) - cil(x0 + 37.5, y0 + 22.5, 0.5, 1.0, d - 1.2, 48) for d in range(12, 42, 4)])
    pb = C.POS_PB
    xm = pb[0] + 16.0                                     # centro do micro-USB do power bank (lateral, perto da ponta do USB)
    rab = cubo(xm - 3, pb[1] - 6, 0, xm + 3, y0 + 8, 0.4) + cubo(xm - 3, y0 + 2, 0, x0 + 1, y0 + 8, 0.4)
    plugue = cubo(xm - 3.5, pb[1] - 7, C.QI_E + 5.5, xm + 3.5, pb[1] + 0.4, C.QI_E + 9.5) + \
        cubo(xm - 2.5, pb[1] + 0.4, C.QI_E + 6.3, xm + 2.5, pb[1] + 4, C.QI_E + 8.7) + cubo(xm - 2, pb[1] - 7, 0, xm + 2, pb[1] - 5, C.QI_E + 5.5)
    return [('#334155', folha), ('#b45309', aneis), ('#f59e0b', rab), ('#111827', plugue)]


def pilula_y(cx, y0, comp, larg, z0, z1, seg=48):
    """Pílula (retângulo com pontas semicirculares) deitada ao longo de y."""
    r = larg / 2
    return Manifold.batch_hull([cil(cx, y0 + r, z0, z1, larg, seg), cil(cx, y0 + comp - r, z0, z1, larg, seg)])


def base_qi():
    """HyperX ChargePlay Base (215,05 x 90,91 x 17,36): pílula preta com 2 áreas de carga ovais e um ressalto
    no meio, onde entram o cabo USB-C e ficam os 2 LEDs. A caixa apoia atravessada sobre a área 1."""
    cx, y0 = C.BASE_QI
    L, W, Ht = 215.05, 90.91, 17.36
    topo_area = -3.0                       # topo da borracha da área de carga = fundo da caixa
    z_corpo = topo_area - 0.6              # topo do corpo
    z0 = topo_area - 11.0                  # fundo (área de carga a ~11 mm da mesa; o ressalto chega a 17,36)
    corpo = pilula_y(cx, y0, L, W, z0, z_corpo)
    ym = y0 + L / 2
    ressalto = Manifold.batch_hull([cil(cx - W / 2 + 12, ym, z_corpo - 0.1, z0 + Ht - 3, 22, 32), cil(cx + W / 2 - 12, ym, z_corpo - 0.1, z0 + Ht - 3, 22, 32),
                                    cil(cx - W / 2 + 14, ym, z0 + Ht - 3, z0 + Ht, 16, 32), cil(cx + W / 2 - 14, ym, z0 + Ht - 3, z0 + Ht, 16, 32)])
    areas = pilula_y(cx, y0 + 7, 85, 76, z_corpo - 0.01, topo_area) + pilula_y(cx, y0 + L - 7 - 85, 85, 76, z_corpo - 0.01, topo_area)
    marcas = uniao([cil(cx, y0 + 47 + k * 121.0, topo_area - 0.2, topo_area + 0.0, 34, 48) - cil(cx, y0 + 47 + k * 121.0, topo_area - 1, topo_area + 1, 31, 48) for k in range(2)])
    leds = uniao([cil(cx + sx * 20, ym + sy * 6.5, z0 + Ht - 0.4, z0 + Ht + 0.15, 3, 16) for sx, sy in ((-1, -1), (1, 1))])
    logo = cubo(cx - 9, ym - 2.5, z0 + Ht - 0.05, cx + 9, ym + 2.5, z0 + Ht + 0.05)
    plugue = cubo(cx + W / 2 - 4, ym - 5, z0 + 5, cx + W / 2 + 14, ym + 5, z0 + 12)
    cabo = tubo([(cx + W / 2 + 14, ym, z0 + 8.5), (cx + W / 2 + 40, ym + 8, z0 + 4), (cx + W / 2 + 70, ym + 30, z0 + 2)], 3.5)
    return [('#111827', corpo), ('#1f2937', ressalto), ('#262b33', areas), ('#3f4652', marcas), ('#38bdf8', leds), ('#9ca3af', logo), ('#111827', plugue + cabo)]


# ---------------- semáforo ----------------
def semaforo():
    x0, y0 = C.POS_SEM
    L, W, _ = M.SEMAFORO
    z1 = C.H - 0.2 - 8.6                  # face de cima da placa: LEDs sobem 8,6 mm até a tampa
    pcb = cubo(x0, y0, z1 - 1.6, x0 + L, y0 + W, z1)
    for hx in (3.5, L - 3.5):
        pcb = pcb - cil(x0 + hx, y0 + W / 2, z1 - 3, z1 + 1, 3.0)
    leds = []
    for k, cor in enumerate(('#ef4444', '#facc15', '#22c55e')):
        cx = x0 + L / 2 + (k - 1) * 12.5
        cy = y0 + W / 2
        leds.append((cor, cil(cx, cy, z1, z1 + 5.4, 8.0) + esfera(cx, cy, z1 + 5.4, 8.0) ^ (cubo(cx - 5, cy - 5, z1 + 5.4, cx + 5, cy + 5, z1 + 9.4))))
    pinos = cubo(x0 + 1.5, y0 + W / 2 - 5.1, z1 - 1.6 - 8.5, x0 + 4.0, y0 + W / 2 + 5.1, z1 - 1.6)
    return [('#0f172a', pcb), ('#111827', pinos)] + leds


# ---------------- chave fim de curso (versão A, embaixo do pino da chave) ----------------
def chave_a():
    px, py, _ = C.P_pt(*M.PLUNGER, 0)
    z1 = C.H - 4.5                         # alavanca encosta no pino da chave
    x0, y0 = px - 18.5, py - 6.85
    pcb = cubo(x0, y0, z1 - 7.6, x0 + 25, y0 + 13.7, z1 - 6.0)
    sw = cubo(x0 + 6, y0 + 3.5, z1 - 6.0, x0 + 19, y0 + 10.2, z1 - 0.8)
    alav = Manifold.batch_hull([cubo(x0 + 7, y0 + 5.5, z1 - 1.0, x0 + 8, y0 + 8.2, z1 - 0.6), cubo(px - 0.5, y0 + 5.5, z1 - 0.2, px + 1.5, y0 + 8.2, z1 + 0.2)])
    pinos = cubo(x0 + 0.5, y0 + 3, z1 - 7.6 - 6, x0 + 2.5, y0 + 10.7, z1 - 7.6)
    return [('#1d4ed8', pcb), ('#111827', sw), ('#cbd5e1', alav), ('#d4a017', pinos)]


# ---------------- cabo USB do power bank ao ESP32 ----------------
def cabo_usb():
    pb = C.POS_PB
    yc = (pb[1] + pb[3]) / 2
    plugue = cubo(pb[0] - 26, yc - 8, C.QI_E + 3.5, pb[0] + 0.5, yc + 8, C.QI_E + 11.5)
    fc = C.FURO_CABO
    ex0 = C.POS_ESP[0] + 0.5 + (M.EXP[0] - 51.6) / 2 + 3.0
    ey = C.POS_ESP[1] + 0.5 + M.EXP[1] / 2
    ze = C.ZS + 2.0 + 1.6 + 8.5 + 3.2
    pts = [(pb[0] - 26, yc, C.QI_E + 7.5), (pb[0] - 32, yc, 10), (fc[0] + 10, yc, C.Z_PRAT - 3), (fc[0] + 10, (fc[1] + fc[3]) / 2, C.ZS + 6),
           (fc[0] + 14, 78, C.ZS + 6), (110, 79, C.ZS + 8), (ex0 - 13, 70, ze), (ex0 - 14, ey, ze), (ex0 - 9, ey, ze)]
    cabo = tubo(pts, 3.6)
    usbc = cubo(ex0 - 9, ey - 4, ze - 2.2, ex0 - 1.05, ey + 4, ze + 2.2)
    return [('#111827', plugue + usbc), ('#1f2937', cabo)]


# ---------------- versão B ----------------
def embreagem_partes():
    """Embreagem de etiqueta de loja em corte simplificado: copo de aço, carretel (desce quando o ímã puxa)
    e 3 esferas que prendem o pino (abrem quando o carretel desce). Medidas: modelo da equipe [MEDIR]."""
    cx, cy, _ = C.P_pt(*M.CAPS, 0)
    z0 = C.ZS + M.ZC0
    D, Hc = M.EMB
    copo = cil(cx, cy, z0, z0 + Hc, D) - cil(cx, cy, z0 + 1.0, z0 + Hc + 1, D - 1.6) - cil(cx, cy, z0 - 1, z0 + 2, 3.0)
    copo = copo + (Manifold.cylinder(2.5, D / 2 - 0.8, 1.6, 32).translate([cx, cy, z0 + Hc - 4.0]) - cil(cx, cy, z0, z0 + Hc + 1, 3.2))   # cone das esferas
    carretel = cil(cx, cy, z0 + 1.2, z0 + 6.0, D - 2.2) - cil(cx, cy, z0, z0 + 7, 3.2)
    mola = uniao([cil(cx, cy, z0 + 6.0 + k * 0.9, z0 + 6.4 + k * 0.9, D - 2.6, 24) - cil(cx, cy, z0, z0 + 20, D - 3.6, 24) for k in range(3)])
    esferas = uniao([Manifold.sphere(1.2, 16).translate([cx + 1.85 * np.cos(np.radians(a)), cy + 1.85 * np.sin(np.radians(a)), z0 + Hc - 2.6]) for a in (0, 120, 240)])
    return (cx, cy, z0), [('#9ca3af', copo), ('#94a3b8', mola)], [('#cbd5e1', carretel)], [('#e5e7eb', esferas)]


def pino_etiqueta():
    cx, cy, _ = C.P_pt(*M.CAPS, 0)
    zc = C.ZS + M.Z_ANEL_TOPO + 0.6                      # cabeça apoiada no pano (0,6 mm) em cima da cápsula
    haste = cil(cx, cy, zc - 16, zc, 1.2) + Manifold.cylinder(0.8, 0.1, 0.6, 12).translate([cx, cy, zc - 16.8])
    cabeca = cil(cx, cy, zc, zc + 1.5, 12.5) + (esfera(cx, cy, zc + 1.5, 12.5) ^ cubo(cx - 7, cy - 7, zc + 1.5, cx + 7, cy + 7, zc + 4))
    return [('#e5e7eb', haste), ('#94a3b8', cabeca)]


def imas_local(pb):
    _, esp = M.b_braco()
    pecas = []
    for k in range(M.N_IMAS):
        z0 = esp + k * M.IMA[1]
        m = cil(M.R_IMA, 0, z0, z0 + M.IMA[1] - 0.05, M.IMA[0]) - cil(M.R_IMA, 0, z0 - 1, z0 + 6, M.IMA[2])
        pecas.append(m)
    m = uniao(pecas).translate([M.SX, M.SY, M.Z_BRACO_B])
    return [('#d4d4d8', C.P(m).translate([-pb[0], -pb[1], -pb[2]]))]
