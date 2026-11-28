"""Chave fim de curso YL-99 (Curto Circuito), desenhada como a foto da loja:
placa azul de 25 x 13,7 mm; o micro-switch preto fica NA PONTA da placa; a alavanca de metal
sai do micro-switch e passa da borda da placa; os 3 pinos (VCC, GND, OUT) saem retos na outra ponta.

Referencial local: placa de x=0 a 25, centrada em y, fundo em z=0. A alavanca aponta para -x.
Medidas da placa [L]: 25 x 13,7. Micro-switch KW11 ~12,8 x 5,8 x 6,5. Alavanca ~19 mm (conferir).
"""
import numpy as np
from manifold3d import Manifold
import tagandgo_v2 as M
import tagandgo_v3 as C
from tagandgo_v2 import cubo, cil, uniao

PLACA = (25.0, 13.7, 1.6)
HINGE = (11.0, 8.3)              # dobradiça da alavanca (x, z), em cima do micro-switch, na ponta de dentro
PONTA = -8.0                     # ponta da alavanca, além da borda da placa
PONTA_TOPO = 8.9                 # topo da ponta, solta
PINOS_Y = (-2.54, 0.0, 2.54)     # VCC, GND, OUT


def ang_para(curso, ponta):
    return -np.degrees(np.arcsin(curso / (HINGE[0] - ponta)))


ANG_A = ang_para(1.3, PONTA)          # o gancho desce 1 mm na alavanca; 0,3 mm de folga


def partes_locais():
    L, W, T = PLACA
    pcb = cubo(0, -W / 2, 0, L, W / 2, T) - cil(17.0, 0, -1, T + 1, 3.0)
    corpo = cubo(-1.0, -2.9, T, 11.8, 2.9, T + 6.5)                         # micro-switch na ponta da placa
    rebite = uniao([cubo(x - 1.1, 2.9, T + 2.2, x + 1.1, 3.05, T + 4.4) for x in (1.5, 8.5)])
    botao = cubo(1.0, -1.0, T + 6.5, 2.6, 1.0, T + 7.0)
    smd = cubo(13.5, 3.0, T, 15.5, 4.3, T + 0.5) + cubo(13.5, -4.3, T, 15.5, -3.0, T + 0.5) + cubo(19.5, 3.2, T, 21.0, 4.6, T + 0.5)
    led = cubo(19.5, -4.6, T, 21.0, -3.2, T + 0.7)
    espacador = cubo(23.0, -3.8, 0, 25.5, 3.8, T + 2.5)
    pinos = uniao([cubo(23.0, y - 0.32, T / 2 + 0.88, 31.0, y + 0.32, T / 2 + 1.52) for y in PINOS_Y])
    estaticas = [('#1d4ed8', pcb), ('#111827', corpo + espacador), ('#9ca3af', rebite), ('#ef4444', botao),
                 ('#0f172a', smd), ('#f87171', led), ('#d4a017', pinos)]
    hx, hz = HINGE
    alav = Manifold.batch_hull([cubo(hx - 0.6, -1.5, hz - 0.15, hx + 0.6, 1.5, hz + 0.15),
                                cubo(PONTA + 1.5, -1.5, PONTA_TOPO - 0.3, PONTA + 2.5, 1.5, PONTA_TOPO)])
    dobra = Manifold.batch_hull([cubo(PONTA + 1.5, -1.5, PONTA_TOPO - 0.3, PONTA + 2.5, 1.5, PONTA_TOPO),
                                 cubo(PONTA, -1.5, PONTA_TOPO - 1.6, PONTA + 0.6, 1.5, PONTA_TOPO - 1.3)])
    return estaticas, [('#d1d5db', alav + dobra)]


def alavanca_girada(alav_local, ang):
    hx, hz = HINGE
    return [(c, m.translate([-hx, 0, -hz]).rotate([0, ang, 0]).translate([hx, 0, hz])) for c, m in alav_local]


# ---------------- versão A: sobre um suporte da A1, alavanca embaixo do gancho ----------------
def A_origem():
    """No referencial do módulo v2. A placa fica atrás do trilho (ao longo de +y); a alavanca vai até o gancho."""
    x, y = M.HOOK
    z0 = 42.0 + 1.0 - PONTA_TOPO           # ponta solta 1 mm acima do fundo do gancho fechado
    return x, y - PONTA, z0


def para_A(m):
    x, y, z0 = A_origem()
    return C.P(m.rotate([0, 0, 90]).translate([x, y, z0]))


def A_estaticas():
    e, _ = partes_locais()
    return [(c, para_A(m)) for c, m in e]


def A_alavanca(apertada=False):
    _, a = partes_locais()
    if apertada:
        a = alavanca_girada(a, ANG_A)
    return [(c, para_A(m)) for c, m in a]


def A_pivo():
    x, y, z0 = A_origem()
    return C.P_pt(x, y + HINGE[0], z0 + HINGE[1]), [0.0, 1.0, 0.0]


def A_pino(i):
    x, y, z0 = A_origem()
    return C.P_pt(x - PINOS_Y[i], y + 31.0, z0 + 2.0)


def A_suporte_modulo():
    """Coluna do suporte (vai junto com a peça A1), no referencial do módulo v2."""
    x, y, z0 = A_origem()
    s = cubo(x - 6.0, y + 13.0, 0, x + 6.0, y + 22.0, z0)
    for sx in (-1, 1):
        a, b = x + sx * 6.95, x + sx * 7.85
        s = s + cubo(min(a, b), y + 13.0, z0 - 2.0, max(a, b), y + 22.0, z0 + 1.2)
    return s


# ---------------- versão B: por dentro, alavanca entra pela fenda da cápsula ----------------
PONTA_B = -14.0                         # ponteira B7 alonga a alavanca até o centro da cápsula
ANG_B = ang_para(2.1, PONTA_B)          # a ponta (afiada) do pino empurra ~1,8 mm


def ponteira_local():
    """B7: encaixa na ponta da alavanca e alonga até o centro da cápsula, onde a ponta do pino aperta."""
    z1 = PONTA_TOPO + 0.2
    corpo = cubo(PONTA_B - 0.5, -1.9, z1 - 1.0, PONTA + 3.5, 1.9, z1)
    return corpo - cubo(PONTA - 0.3, -1.6, PONTA_TOPO - 1.8, PONTA + 3.6, 1.6, PONTA_TOPO + 0.05)


def B_frame():
    cx, cy, _ = C.P_pt(*M.CAPS, 0)
    sx, sy, _ = C.P_pt(M.SX, M.SY, 0)
    u = np.array([cx - sx, cy - sy])
    u /= np.linalg.norm(u)
    teta = float(np.degrees(np.arctan2(u[1], u[0])))
    z_ponta = C.ZS + M.B_PONTA_PINO + 1.0         # ponta solta 1 mm acima de onde a ponta do pino chega
    z0 = z_ponta - (PONTA_TOPO + 0.2)
    ox, oy = cx - PONTA_B * u[0], cy - PONTA_B * u[1]
    return ox, oy, z0, teta, u


def para_B(m):
    ox, oy, z0, teta, _ = B_frame()
    return m.rotate([0, 0, teta]).translate([ox, oy, z0])


def B_estaticas():
    e, _ = partes_locais()
    return [(c, para_B(m)) for c, m in e]


def B_alavanca(apertada=False):
    _, a = partes_locais()
    a = a + [('#a16207', ponteira_local())]
    if apertada:
        a = alavanca_girada(a, ANG_B)
    return [(c, para_B(m)) for c, m in a]


def B_pivo():
    ox, oy, z0, teta, u = B_frame()
    t = np.radians(teta)
    hx = HINGE[0]
    return (ox + hx * np.cos(t), oy + hx * np.sin(t), z0 + HINGE[1]), [float(-np.sin(t)), float(np.cos(t)), 0.0]


def B_pino(i):
    ox, oy, z0, teta, _ = B_frame()
    t = np.radians(teta)
    lx, ly = 31.0, PINOS_Y[i]
    return (ox + lx * np.cos(t) - ly * np.sin(t), oy + lx * np.sin(t) + ly * np.cos(t), z0 + 2.0)


def B_suporte():
    """B6: coluna colada na prateleira; a placa da chave encaixa em cima (abas dos lados)."""
    ox, oy, z0, teta, _ = B_frame()
    s = cubo(13.0, -6.0, C.ZS - z0, 22.0, 6.0, 0)
    for sy in (-1, 1):
        a, b = sy * 6.95, sy * 7.85
        s = s + cubo(13.0, min(a, b), -2.0, 22.0, max(a, b), 1.2)
    return s.rotate([0, 0, teta]).translate([ox, oy, z0])
