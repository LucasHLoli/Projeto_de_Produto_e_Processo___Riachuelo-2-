"""Chave fim de curso (módulo YL-99 com micro-switch KW11) desenhada como a peça real,
e as duas montagens: versão A (o gancho aperta) e versão B (a cabeça do pino aperta).

Referencial local da chave: placa de 25 x 13,7 x 1,6 mm de x=0 a 25, centrada em y, fundo em z=0.
A alavanca de metal sai de uma dobradiça em x=18,5 (em cima do micro-switch) e a ponta fica em x=5,5.
Os 3 pinos (VCC, GND, OUT) saem para baixo na ponta x=23,5.
Medidas da placa [L]: 25 x 13,7 x 5,8 (com o micro-switch). Alavanca e pinos: estimados; conferir com paquímetro.
"""
import numpy as np
from manifold3d import Manifold
import tagandgo_v2 as M
import tagandgo_v3 as C
from tagandgo_v2 import cubo, cil, uniao

PLACA = (25.0, 13.7, 1.6)
HINGE = (18.5, 7.0)          # x, z da dobradiça da alavanca
PONTA_TOPO = 7.3             # topo da ponta da alavanca, solta
CURSO_PONTA = 1.0            # quanto a ponta desce quando apertada
BRACO = HINGE[0] - 5.5
ANG_APERTADA = -np.degrees(np.arcsin(CURSO_PONTA / BRACO))
PINOS_Y = (-2.54, 0.0, 2.54)  # VCC, GND, OUT


def partes_locais():
    L, W, T = PLACA
    pcb = cubo(0, -W / 2, 0, L, W / 2, T) - cil(3.0, 0, -1, T + 1, 3.0)
    corpo = cubo(8.5, -3.2, T, 21.5, 3.2, T + 5.2)                        # micro-switch KW11 (12,8 x 5,8 x 6,5)
    botao = cubo(14.5, -1.0, T + 5.2, 16.0, 1.0, T + 5.7)
    terminais = uniao([cubo(9.5 + k * 4.5, -0.4, T - 0.01, 10.3 + k * 4.5, 0.4, T + 0.6) for k in range(3)])
    smd = cubo(4.5, 3.2, T, 6.5, 4.5, T + 0.5) + cubo(4.5, -4.5, T, 6.5, -3.2, T + 0.5)       # resistores
    led = cubo(1.2, 4.6, T, 2.8, 5.6, T + 0.7)
    base_pin = cubo(22.25, -3.8, -2.5, 24.75, 3.8, 0)
    pinos = uniao([cubo(23.18, y - 0.32, -8.5, 23.82, y + 0.32, -2.5) for y in PINOS_Y])
    estaticas = [('#1d4ed8', pcb), ('#111827', corpo + base_pin), ('#ef4444', botao), ('#d4a017', terminais + pinos),
                 ('#0f172a', smd), ('#f87171', led)]
    hx, hz = HINGE
    alav = Manifold.batch_hull([cubo(hx - 0.5, -1.4, hz - 0.2, hx + 0.5, 1.4, hz + 0.2),
                                cubo(5.0, -1.4, PONTA_TOPO - 0.4, 6.0, 1.4, PONTA_TOPO)])
    rolo = Manifold.cylinder(2.8, 1.0, 1.0, 16).rotate([90, 0, 0]).translate([5.5, 1.4, PONTA_TOPO - 1.0])
    alavanca = [('#cbd5e1', alav + rolo)]
    return estaticas, alavanca


def alavanca_girada(alav_local, ang):
    """Gira a alavanca em torno da dobradiça (eixo y local). Ângulo negativo abaixa a ponta."""
    hx, hz = HINGE
    return [(c, m.translate([-hx, 0, -hz]).rotate([0, ang, 0]).translate([hx, 0, hz])) for c, m in alav_local]


# ---------------- montagem A: placa no suporte da A1, ponta embaixo do gancho ----------------
def para_A(m):
    """local -> referencial do módulo v2 -> caixa."""
    ch = M.CH
    return C.P(m.translate([ch['x0'], ch['yc'], ch['z_placa']]))


def A_estaticas():
    e, _ = partes_locais()
    return [(c, para_A(m)) for c, m in e]


def A_alavanca(apertada=False):
    _, a = partes_locais()
    if apertada:
        a = alavanca_girada(a, ANG_APERTADA)
    return [(c, para_A(m)) for c, m in a]


def A_pivo():
    ch = M.CH
    return C.P_pt(ch['x0'] + HINGE[0], ch['yc'], ch['z_placa'] + HINGE[1]), [1.0, 0.0, 0.0]
    # o eixo y local vira +x na caixa; a ponta fica para +y, então ângulo negativo abaixa a ponta


def A_pino(i):
    ch = M.CH
    return C.P_pt(ch['x0'] + 23.5, ch['yc'] + PINOS_Y[i], ch['z_placa'] - 8.5)


# ---------------- montagem B: em cima da tampa, ponta embaixo da cabeça do pino ----------------
PONTA_B = -5.0                # na B a ponta (com a ponteira impressa B7) vai até 4,5 mm do pino
ANG_B = -np.degrees(np.arcsin(1.2 / (HINGE[0] - PONTA_B)))   # a cabeça empurra 1,2 mm


def ponteira_local():
    """Peça impressa B7: encaixa na ponta da alavanca e a alonga até a cabeça do pino."""
    corpo = cubo(PONTA_B - 0.5, -1.7, PONTA_TOPO - 0.9, 7.0, 1.7, PONTA_TOPO)
    return corpo - cubo(4.0, -1.45, PONTA_TOPO - 0.65, 7.1, 1.45, PONTA_TOPO - 0.25)


def B_ref():
    cx, cy, _ = C.P_pt(*M.CAPS, 0)
    z_anel = C.H + M.CAV + M.EMB[1] + 0.3 + 1.6
    z_placa = z_anel + 2.4 - PONTA_TOPO
    return cx + 9.5, cy, z_placa, z_anel            # placa fora da cápsula (raio 8,5)


def para_B(m):
    x0, y0, z0, _ = B_ref()
    return m.translate([x0, y0, z0])


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
    x0, y0, z0, _ = B_ref()
    return (x0 + HINGE[0], y0, z0 + HINGE[1]), [0.0, 1.0, 0.0]


def B_pino(i):
    x0, y0, z0, _ = B_ref()
    return (x0 + 23.5, y0 + PINOS_Y[i], z0 - 8.5)


def B_suporte():
    """Peça impressa B6: suporte colado na tampa; a placa da chave assenta em cima. Rasgo para os pinos descerem."""
    x0, y0, z0, _ = B_ref()
    tz = C.H + M.MDF
    s = cubo(x0 + 7.0, y0 - 7.85, tz, x0 + 21.0, y0 + 7.85, z0)
    for sy in (-1, 1):
        a, b = y0 + sy * 6.95, y0 + sy * 7.85
        s = s + cubo(x0 + 7.0, min(a, b), z0 - 0.01, x0 + 21.0, max(a, b), z0 + 1.2)
    return s


def B_rasgo_tampa():
    x0, y0, z0, _ = B_ref()
    return cubo(x0 + 21.5, y0 - 4.5, C.H - 1, x0 + 26.0, y0 + 4.5, C.H + M.MDF + 1)
