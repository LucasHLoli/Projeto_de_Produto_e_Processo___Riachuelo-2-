"""Tag&Go protótipo v2: medidas reais, nada empilhado, duas versões.

Versão A (principal): garra com 4 dentes que empurra a roupa para dentro de furos
numa tampa de 3 chapas de MDF. O gancho da garra é travado por uma lingueta
movida pelo servo por uma biela (pino num rasgo). Sem mola, sem elástico.

Versão B (reserva): etiqueta antifurto de loja. O pino da etiqueta entra numa
cápsula na tampa; o servo leva 2 ímãs 15 x 5 mm até embaixo da embreagem.

Coordenadas: origem no canto interno do fundo da caixa (em cima da chapa do fundo).
x = comprimento, y = largura, z = altura. Tudo em mm.

Fontes das medidas: research_notes/Medidas reais/medidas.md
Rodar: python tagandgo_v2.py   (precisa de manifold3d, trimesh, numpy)
"""
import base64, json, os
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection

AQUI = os.path.dirname(os.path.abspath(__file__))
SEG = 48

# ======================= MEDIDAS DAS PEÇAS COMPRADAS =======================
# [C] comunidade, [L] loja, [F] fabricante, [E] estimativa, [MEDIR] confirmar com paquímetro
SERVO = dict(corpo_c=22.7, corpo_l=12.4,          # SG90 22,2-22,7 x 11,8-12,4; MG90S 22,5-22,9 x 12-12,4 [C]
             orelhas=32.5,                        # 32,1-32,5 [C]
             orelha_esp=2.5,                      # [C]
             eixo_ponta=5.2,                      # eixo a 5,1 (SG90) / 5,3 (MG90S) da ponta [C]
             furos=(27.94, 28.32),                # entre centros SG90 / MG90S [C] -> furo oblongo
             braco_acima_orelha_max=17.0)         # topo do braço plástico acima da base da orelha (máx. estimado)
PB = (149.0, 69.0, 15.0)                          # power bank ELG PB102BK [L]
EXP = (68.6, 53.4)                                # expansor ESP32 [L]
QI = (75.0, 45.0, 1.0)                            # receptor Qi [E][MEDIR]
CHAVE = (25.0, 13.7, 5.8)                         # chave fim de curso YL-99 [L]
SEMAFORO = (56.0, 21.0, 11.0)                     # módulo semáforo [F distribuidor]
IMA = (15.0, 5.0, 3.2)                            # ímã 15 x 5 com furo 3 mm [L]
EMB = (13.0, 11.0)                                # embreagem da etiqueta de loja [MEDIR]
PINO_ETQ = 1.5                                    # haste do pino da etiqueta, com folga [C]

# ======================= CAIXA =======================
MDF = 3.0
LX, LY = 194.0, 146.0         # interno
H = 48.5                      # do fundo até a face de baixo da tampa
FOLGA = 0.5                   # folga de encaixe das peças compradas
CAMADAS_A = 3                 # tampa da versão A: 3 chapas
VAO = 1.5                     # vão do pano entre a garra fechada e a tampa

# berços (x0, y0, x1, y1)
POS_PB = (42.0, 16.0, 42.0 + PB[0] + 1, 16.0 + PB[1] + 1)          # USB virado para x=42, micro-USB para y=16
POS_ESP = (2.0, 90.0, 2.0 + EXP[0] + 1, 90.0 + EXP[1] + 1)
SX, SY = 160.0, 102.0                                              # eixo do servo
Z_ORELHA = 35.0 - SERVO['braco_acima_orelha_max']                  # apoio das orelhas = 18
Z_BRACO = 35.0                                                     # topo do braço plástico (nominal; calços acertam)
POS_SEMAFORO = (80.0, 125.0)                                       # canto da janela dos LEDs
PARAF_TAMPA = [(3.0, 80.0), (LX - 3.0, 8.0)]


# ======================= utilitários =======================
def cubo(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def cil(x, y, z0, z1, d, seg=SEG):
    return Manifold.cylinder(z1 - z0, d / 2, d / 2, seg).translate([x, y, z0])


def cil_x(y, z, x0, x1, d):
    return Manifold.cylinder(x1 - x0, d / 2, d / 2, SEG).rotate([0, 90, 0]).translate([x0, y, z])


def uniao(ms):
    m = ms[0]
    for o in ms[1:]:
        m = m + o
    return m


def prisma_yz(pts, x0, x1):
    """Extrusão em x de um polígono no plano (y, z)."""
    return Manifold.extrude(CrossSection([pts]), x1 - x0).rotate([0, 90, 0]).rotate([0, 0, 0]).translate([x0, 0, 0]) \
        if False else Manifold.extrude(CrossSection([[[p[1], p[0]] for p in pts]]), x1 - x0).rotate([0, 90, 0]).translate([x0, 0, 0])


# ======================= SERVO (comum às duas versões) =======================
def berco_servo(x0, x1, y0, y1):
    """Placa de base + berço do servo. Orelhas apoiam em Z_ORELHA; furo oblongo serve SG90 e MG90S."""
    s = SERVO
    bx0 = SX - s['eixo_ponta']
    bx1 = bx0 + s['corpo_c']
    cx = (bx0 + bx1) / 2
    base = cubo(x0, y0, 0, x1, y1, 2)
    bloco = cubo(cx - s['orelhas'] / 2 - 2, SY - s['corpo_l'] / 2 - 2.5, 0, cx + s['orelhas'] / 2 + 2, SY + s['corpo_l'] / 2 + 2.5, Z_ORELHA)
    m = base + bloco
    m = m - cubo(bx0 - 0.3, SY - s['corpo_l'] / 2 - 0.3, 0.6, bx1 + 0.3, SY + s['corpo_l'] / 2 + 0.3, Z_ORELHA + 1)
    for sgn in (-1, 1):
        f0, f1 = s['furos']
        a = cx + sgn * f0 / 2
        b = cx + sgn * f1 / 2
        m = m - (cil(a, SY, Z_ORELHA - 8, Z_ORELHA + 1, 2.0) + cil(b, SY, Z_ORELHA - 8, Z_ORELHA + 1, 2.0)
                 + cubo(min(a, b), SY - 1.0, Z_ORELHA - 8, max(a, b), SY + 1.0, Z_ORELHA + 1))
    # saída do fio nas duas pontas, embaixo
    m = m - cubo(cx - s['orelhas'] / 2 - 3, SY - 2.5, 0.6, cx + s['orelhas'] / 2 + 3, SY + 2.5, 7)   # fio sai pelas duas pontas
    return m


def calcos():
    """Calços sob as orelhas: 0,5 / 1 / 1,5 / 2 / 3 mm."""
    ps = []
    for i, h in enumerate([0.5, 1.0, 1.5, 2.0, 3.0]):
        c = cubo(0, i * 10, 0, 38, i * 10 + 8, h)
        c = c - cubo(7, i * 10 + 1.5, -1, 31, i * 10 + 6.5, h + 1)
        for x in (5.0 - 0.2, 33.0 + 0.2):
            c = c - cil(x, i * 10 + 4, -1, h + 1, 2.4)
        ps.append(c)
    return uniao(ps)


# ======================= VERSÃO A: garra com dentes =======================
A_TZ = H + CAMADAS_A * MDF               # topo da tampa
A_GZ0 = A_TZ + VAO                        # fundo da garra fechada
A_EIXO_Y, A_EIXO_DZ = 20.0, 4.0           # dobradiça: y do eixo e altura acima do fundo da garra
A_GX = 174.0                              # linha central da garra em x
DENTES_U = [20.0, 34.0, 48.0, 62.0]       # distância de cada dente ao eixo
DENTE_C, DENTE_E = 25.0, 4.0              # comprimento (em x) e espessura (em y) do dente
DENTE_H = CAMADAS_A * MDF + 3.0           # dente atravessa as 3 chapas
FOLGA_PANO = 1.75
HOOK = (A_GX, SY + 16.0)                  # gancho (x, y)
HOOK_U = HOOK[1] - A_EIXO_Y
Z_LING = (44.3, 46.7)                     # altura da lingueta
Z_ENTALHE = (44.0, 47.0)
Z_GANCHO_BAIXO = 42.0
R_BIELA, ANG_TRAVA, ANG_SOLTA = 6.0, 40.0, 90.0
PINO_X_TRAVA = SX + R_BIELA * np.cos(np.radians(ANG_TRAVA))
CURSO = PINO_X_TRAVA - (SX + R_BIELA * np.cos(np.radians(ANG_SOLTA)))
PLUNGER = (182.0, 92.0)                   # pino que aciona a chave da garra


def a_garra():
    """Coordenadas locais: u ao longo da garra (y global), v em x (0 = A_GX), w para cima (0 = fundo fechado).
    Devolvida já em posição global (fechada)."""
    c = HOOK_U + 6
    m = cubo(-13, 7, 0, 13, c, 9)                                   # barra (9 mm: a junta fica dentro)
    m = m + cubo(-10, 0, 0, 10, 7, 9) + cil_x(0, A_EIXO_DZ, -10, 10, 9)   # junta
    m = m - cubo(-20, -10, -10, 20, c + 5, 0)
    m = m - cil_x(0, A_EIXO_DZ, -12, 12, 3.4)                       # eixo: prego ou palito
    for u in DENTES_U:
        d = cubo(-DENTE_C / 2, u - DENTE_E / 2, -DENTE_H + 2, DENTE_C / 2, u + DENTE_E / 2, 0.01)
        d = d + cil_x(u, -DENTE_H + 2, -DENTE_C / 2, DENTE_C / 2, DENTE_E)
        m = m + d
    gz = Z_GANCHO_BAIXO - A_GZ0
    g = cubo(-2, HOOK_U - 3, gz, 2, HOOK_U + 3, 0.5)
    g = g - cubo(-2.1, HOOK_U - 4, Z_ENTALHE[0] - A_GZ0, 0, HOOK_U + 4, Z_ENTALHE[1] - A_GZ0)   # entalhe no lado -x
    m = m + g
    return m.translate([A_GX, A_EIXO_Y, A_GZ0])


def a_garra_ang(ang):
    """Garra aberta 'ang' graus (ponta para cima)."""
    eixo = np.array([0, A_EIXO_Y, A_GZ0 + A_EIXO_DZ])
    return a_garra().translate((-eixo).tolist()).rotate([ang, 0, 0]).translate(eixo.tolist())


def a_furos_por_camada(ang_max=60.0):
    """Intervalos y de cada furo, em cada chapa, seguindo o arco do dente e do gancho."""
    ez = A_GZ0 + A_EIXO_DZ
    pecas = [(u, DENTE_E / 2, -DENTE_H, FOLGA_PANO) for u in DENTES_U] + [(HOOK_U, 3.0, Z_GANCHO_BAIXO - A_GZ0, 0.6)]
    res = []
    for k in range(CAMADAS_A):
        z1 = A_TZ - k * MDF
        z0 = z1 - MDF
        linha = []
        for u, meia, wmin, folga in pecas:
            ys = []
            for w in np.linspace(wmin, 0, 30):
                for uu in (u - meia, u + meia):
                    py, pz = uu, (A_GZ0 + w) - ez
                    for a in np.radians(np.linspace(0, ang_max, 121)):
                        y = py * np.cos(a) - pz * np.sin(a)
                        z = py * np.sin(a) + pz * np.cos(a) + ez
                        if z0 - 0.5 <= z <= z1 + 0.5:
                            ys.append(y + A_EIXO_Y)
            linha.append((min(ys) - folga, max(ys) + folga))
        res.append((z0, z1, linha))
    return res


def a_tampa():
    t = uniao([cubo(-MDF, -MDF, H + k * MDF, LX + MDF, LY + MDF, H + (k + 1) * MDF) for k in range(CAMADAS_A)])
    for z0, z1, linha in a_furos_por_camada():
        for i, (y0, y1) in enumerate(linha):
            w = DENTE_C / 2 + 1.5 if i < len(DENTES_U) else 2.6
            t = t - cubo(A_GX - w, y0, z0 - 0.01, A_GX + w, y1, z1 + 0.01)
    t = t - janela_leds() - furos_tampa()
    t = t - cil(PLUNGER[0], PLUNGER[1], H - 1, A_TZ + 1, 4.6)
    return t


def janela_leds():
    return cubo(POS_SEMAFORO[0] + 5, POS_SEMAFORO[1] + 5, H - 1, POS_SEMAFORO[0] + SEMAFORO[0] - 5, POS_SEMAFORO[1] + SEMAFORO[1] - 5, H + 20)


def furos_tampa():
    return uniao([cil(x, y, H - 1, H + 20, 3.2) for x, y in PARAF_TAMPA])


def a_dobradica():
    z = A_TZ
    ez = A_GZ0 + A_EIXO_DZ
    base = cubo(A_GX - 18.5, A_EIXO_Y - 8, z, A_GX + 18.5, A_EIXO_Y + 6, z + 2)
    orelhas = uniao([cubo(x0, A_EIXO_Y - 6, z, x0 + 3.5, A_EIXO_Y + 6, z + 5.5) + cil_x(A_EIXO_Y, ez, x0, x0 + 3.5, 12)
                     for x0 in (A_GX - 18.0, A_GX + 14.5)])
    d = base + orelhas
    d = d - cil_x(A_EIXO_Y, ez, A_GX - 30, A_GX + 30, 3.4)
    d = d - cubo(A_GX - 30, A_EIXO_Y - 20, z - 10, A_GX + 30, A_EIXO_Y + 20, z)
    d = d - cubo(A_GX - 11, A_EIXO_Y - 9, z + 0.3, A_GX + 11, A_EIXO_Y + 9, z + 3)
    return d


def a_base_mecanismo():
    """Berço do servo + pilares + trilho da lingueta. Uma peça só, colada no fundo."""
    m = berco_servo(SX - 20, SX + 21, SY - 9, SY + 23)
    lx0, lx1 = HOOK[0] - 2 - 32, HOOK[0] - 2                         # curso da lingueta
    ly0, ly1 = HOOK[1] - 3, HOOK[1] + 3
    p1 = cubo(SX - 18, SY + 10, 0, SX - 12, SY + 22, 42.0)
    p2 = cubo(SX - 2, SY + 19.5, 0, SX + 2, SY + 22, 42.0)
    p3 = cubo(lx1 - 4.0, SY + 19.5, 0, lx1 - 0.5, SY + 22, 42.0)
    abas = cubo(SX - 20, ly0 - 0.4, Z_LING[1] + 0.2, lx1 - 0.5, ly0 + 0.4, Z_LING[1] + 1.1) + cubo(SX - 20, ly1 - 0.4, Z_LING[1] + 0.2, lx1 - 0.5, ly1 + 0.4, Z_LING[1] + 1.1)
    chao = cubo(SX - 20, SY + 10, 42.0, lx1 - 0.5, SY + 22, 44.1)
    chao = chao - cubo(PINO_X_TRAVA - 2.6 - CURSO - 0.6, ly0 + 0.6, 41, PINO_X_TRAVA + 1.4 + 0.6, ly1 - 0.6, 45)
    paredes = cubo(SX - 20, SY + 10, 44.1, lx1 - 0.5, ly0 - 0.4, 47.4) + cubo(SX - 20, ly1 + 0.4, 44.1, lx1 - 0.5, SY + 22, 47.4)
    return uniao([m, p1, p2, p3, chao, paredes, abas])


def a_lingueta_corpo(off=0.0):
    """Barra que corre no trilho. A ponta entra 2 mm no entalhe do gancho. Furo quadrado para a haste do garfo."""
    lx1 = HOOK[0]
    cx = PINO_X_TRAVA
    corpo = cubo(lx1 - 32, HOOK[1] - 2.8, Z_LING[0], lx1, HOOK[1] + 2.8, Z_LING[1])
    corpo = corpo - cubo(cx - 2.6 - 0.15, HOOK[1] - 2.15, Z_LING[0] - 1, cx + 1.4 + 0.15, HOOK[1] + 2.15, Z_LING[1] + 1)
    return corpo.translate([off, 0, 0])


def a_lingueta_garfo(off=0.0):
    """Garfo com o rasgo onde corre o pino do servo, e a haste que encaixa (e cola) no corpo."""
    cx = PINO_X_TRAVA
    haste = cubo(cx - 2.6, HOOK[1] - 2.0, 41.4, cx + 1.4, HOOK[1] + 2.0, Z_LING[1])
    garfo = cubo(cx - 3.6, SY + 0.5, 38.5, cx + 3.6, HOOK[1] + 2.0, 41.5)
    garfo = garfo - cubo(cx - 1.7, SY + 1.0, 38, cx + 1.7, SY + 9.0, 42)
    return (haste + garfo).translate([off, 0, 0])


def a_lingueta(off=0.0):
    return a_lingueta_corpo(off) + a_lingueta_garfo(off)


def a_braco(ang=ANG_TRAVA):
    b = cubo(-4, -4, 0, R_BIELA + 3, 4, 3) + cil(0, 0, 0, 3, 8) + cil(R_BIELA, 0, 0, 3, 7)
    b = b + cil(R_BIELA, 0, 3, 6.6, 3.0)
    b = b - cil(0, 0, -1, 4, 2.2) - cubo(-3.5, -2.3, -1, 1.5, 2.3, 1.3)
    return b.rotate([0, 0, ang]).translate([SX, SY, Z_BRACO])


def a_pino_chave():
    """Pino que atravessa a tampa: a garra fechada empurra, ele aperta a alavanca da chave por baixo."""
    return cil(PLUNGER[0], PLUNGER[1], H - 2.5, H, 8.0) + cil(PLUNGER[0], PLUNGER[1], H, A_GZ0 + 1.0, 4.0)


def ling_off(ang):
    return SX + R_BIELA * np.cos(np.radians(ang)) - PINO_X_TRAVA


# ======================= VERSÃO B: etiqueta de loja + ímãs =======================
B_TZ = H + MDF
R_IMA, ANG_REPOUSO, ANG_SOLTAR = 18.0, 0.0, 120.0
N_IMAS = 2
CAPS = (SX + R_IMA * np.cos(np.radians(ANG_SOLTAR)), SY + R_IMA * np.sin(np.radians(ANG_SOLTAR)))
CAP_D = EMB[0] + 4.0


def b_tampa():
    t = cubo(-MDF, -MDF, H, LX + MDF, LY + MDF, B_TZ)
    return t - cil(CAPS[0], CAPS[1], H - 1, B_TZ + 1, CAP_D + 0.4) - janela_leds() - furos_tampa()


CAV = 4.0          # vão embaixo da embreagem para a ponta do pino (pino de 16 mm passa ~4 mm da embreagem)


def b_capsula():
    """Corpo da cápsula: fundo de 0,8 mm na face de baixo da tampa. A embreagem apoia num degrau a 4 mm do fundo;
    embaixo dela fica o vão da ponta do pino."""
    x, y = CAPS
    z_fundo = H - 0.8
    corpo = cil(x, y, z_fundo, H + CAV + EMB[1] + 0.3, CAP_D)
    aba = Manifold.cylinder(3.0, CAP_D / 2 + 4, CAP_D / 2, SEG).translate([x, y, B_TZ])     # aba em 45 graus
    c = corpo + aba
    c = c - cil(x, y, H + CAV, H + CAV + EMB[1] + 1, EMB[0] + 0.3)        # embreagem
    c = c - cil(x, y, H, H + CAV + 0.01, EMB[0] - 3.0)                     # vão da ponta do pino (degrau de 1,5 mm)
    return c


def b_anel():
    """Tampa de cima da cápsula, colada depois de pôr a embreagem. Furo do pino no centro."""
    x, y = CAPS
    z = H + CAV + EMB[1] + 0.3
    return cil(x, y, z, z + 1.6, CAP_D) - cil(x, y, z - 1, z + 3, PINO_ETQ + 0.6)


def b_braco(ang=ANG_REPOUSO):
    esp = H - 0.8 - 0.2 - N_IMAS * IMA[1] - Z_BRACO        # espessura do braço sob os ímãs
    b = cubo(-4, -4, 0, R_IMA, 4, esp) + cil(0, 0, 0, esp, 8) + cil(R_IMA, 0, 0, esp, IMA[0] + 2)
    b = b - cil(0, 0, -1, esp + 1, 2.2) - cubo(-3.5, -2.3, -1, 1.5, 2.3, min(1.3, esp - 1.2))
    b = b - cil(R_IMA, 0, -1, esp + 1, 3.3)                                 # parafuso M3 dos ímãs
    b = b - cil(R_IMA, 0, -1, 1.2, 6.4, 6)                                   # porca M3 por baixo
    return b.rotate([0, 0, ang]).translate([SX, SY, Z_BRACO]), esp


def b_imas(ang=ANG_REPOUSO):
    _, esp = b_braco()
    m = cil(R_IMA, 0, esp, esp + N_IMAS * IMA[1], IMA[0]) - cil(R_IMA, 0, esp - 1, esp + 20, IMA[2])
    return m.rotate([0, 0, ang]).translate([SX, SY, Z_BRACO])


def b_base():
    return berco_servo(SX - 20, SX + 21, SY - 9, SY + 9)


def teste_embreagem():
    p = cubo(0, 0, 0, 80, 22, 6)
    for i, d in enumerate([EMB[0] - 0.4, EMB[0], EMB[0] + 0.4, EMB[0] + 0.8]):
        p = p - cil(11 + i * 19, 11, 1, 7, d)
        for k in range(i + 1):
            p = p - cubo(4 + i * 19 + k * 2.2, 0, 4.5, 5.2 + i * 19 + k * 2.2, 2, 7)
    return p


# ======================= peças comuns =======================
def caixa():
    return cubo(-MDF, -MDF, -MDF, LX + MDF, LY + MDF, H) - cubo(0, 0, 0, LX, LY, H + 1)


def batente():
    """L de 10 x 10 x 8: segura o power bank e o expansor no lugar (colar no fundo)."""
    return cubo(0, 0, 0, 10, 2.5, 8) + cubo(0, 0, 0, 2.5, 10, 8)


def canto_tampa(x, y):
    return cubo(x - 3, y - 6, H - 10, x + 3, y + 6, H) - cil(x, y, H - 9, H + 1, 2.2)


def comprados_comuns():
    pb = POS_PB
    e = POS_ESP
    return [
        ('Power bank 149 × 69 × 15', 'comprada', '#1f2937', cubo(pb[0] + .5, pb[1] + .5, QI[2], pb[2] - .5, pb[3] - .5, QI[2] + PB[2])),
        ('Receptor Qi (embaixo do power bank)', 'comprada', '#475569', cubo(80, 28, 0, 80 + QI[0], 28 + QI[1], QI[2])),
        ('Expansor + ESP32', 'comprada', '#15803d', cubo(e[0] + .5, e[1] + .5, 0, e[2] - .5, e[3] - .5, 11) + cubo(e[0] + 9, e[1] + 12, 11, e[0] + 61, e[1] + 41, 17)),
        ('Semáforo LED', 'comprada', '#111827', cubo(POS_SEMAFORO[0], POS_SEMAFORO[1], H - SEMAFORO[2], POS_SEMAFORO[0] + SEMAFORO[0], POS_SEMAFORO[1] + SEMAFORO[1], H - 0.2)),
    ]


def servo_modelo(z_base):
    s = SERVO
    bx0 = SX - s['eixo_ponta']
    cx = bx0 + s['corpo_c'] / 2
    return (cubo(bx0, SY - s['corpo_l'] / 2, z_base, bx0 + s['corpo_c'], SY + s['corpo_l'] / 2, Z_ORELHA + 9)
            + cubo(cx - s['orelhas'] / 2, SY - s['corpo_l'] / 2, Z_ORELHA, cx + s['orelhas'] / 2, SY + s['corpo_l'] / 2, Z_ORELHA + 2.5)
            + cil(SX, SY, Z_ORELHA + 9, Z_BRACO, 7))


# ======================= SVG do MDF =======================
def svg(nome, chapas_tampa, extras_por_chapa):
    cut = 'fill="none" stroke="#ff0000" stroke-width="0.1"'
    eng = 'fill="none" stroke="#000000" stroke-width="0.3"'
    txt = 'font-family="Arial" fill="#000000"'
    o = MDF                                          # interno -> chapa externa

    def r(x, y, w, h, s):
        return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" {s}/>'

    def circ(x, y, d, s):
        return f'<circle cx="{x + o:.2f}" cy="{y + o:.2f}" r="{d / 2:.2f}" {s}/>'
    EX, EY = LX + 2 * MDF, LY + 2 * MDF
    base = [r(0, 0, EX, EY, cut)] + [circ(x, y, 3.2, cut) for x, y in PARAF_TAMPA] + \
        [r(POS_SEMAFORO[0] + 5 + o, POS_SEMAFORO[1] + 5 + o, SEMAFORO[0] - 10, SEMAFORO[1] - 10, cut)]
    pecas = []
    for i, extras in enumerate(extras_por_chapa):
        pecas.append((chapas_tampa[i], EX, EY, base + extras))
    pecas += [('Fundo', LX, LY, [r(0, 0, LX, LY, cut)]),
              ('Parede longa 1', EX, H + MDF, [r(0, 0, EX, H + MDF, cut)]),
              ('Parede longa 2', EX, H + MDF, [r(0, 0, EX, H + MDF, cut)]),
              ('Parede curta 1', LY, H + MDF, [r(0, 0, LY, H + MDF, cut)]),
              ('Parede curta 2', LY, H + MDF, [r(0, 0, LY, H + MDF, cut)])]
    W = 640
    x, y, lin, out = 5, 5, 0, []
    for n, w, h, els in pecas:
        if x + w > W:
            x, y, lin = 5, y + lin + 12, 0
        out.append(f'<g transform="translate({x},{y})"><title>{n}</title>{"".join(els)}'
                   f'<text x="{w / 2}" y="{h + 6}" font-size="4" text-anchor="middle" fill="#0000ff">{n}</text></g>')
        x += w + 8
        lin = max(lin, h)
    Ht = y + lin + 12
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{Ht}mm" viewBox="0 0 {W} {Ht}">\n'
         '<!-- MDF 3 mm. Vermelho = cortar. Preto = gravar. Azul = legenda (apagar antes do laser). '
         'Montagem: o fundo fica DENTRO das 4 paredes; as paredes curtas ficam entre as longas. -->\n' + '\n'.join(out) + '\n</svg>')
    os.makedirs(os.path.join(AQUI, 'mdf'), exist_ok=True)
    open(os.path.join(AQUI, 'mdf', nome), 'w', encoding='utf-8').write(s)
    return txt, eng, r, o


def svgs():
    cut = 'fill="none" stroke="#ff0000" stroke-width="0.1"'
    eng = 'fill="none" stroke="#000000" stroke-width="0.3"'
    txt = 'font-family="Arial" fill="#000000"'
    o = MDF

    def r(x, y, w, h, s):
        return f'<rect x="{x + o:.2f}" y="{y + o:.2f}" width="{w:.2f}" height="{h:.2f}" {s}/>'
    qr = [r(5, 25, 32, 32, eng), f'<text x="{21 + o}" y="{22 + o}" font-size="4" text-anchor="middle" {txt}>QR aqui</text>']
    extras = []
    for k, (z0, z1, linha) in enumerate(a_furos_por_camada()):
        ex = []
        for i, (y0, y1) in enumerate(linha):
            w = DENTE_C / 2 + 1.5 if i < len(DENTES_U) else 2.6
            ex.append(r(A_GX - w, y0, 2 * w, y1 - y0, cut))
        ex.append(f'<circle cx="{PLUNGER[0] + o}" cy="{PLUNGER[1] + o}" r="2.3" {cut}/>')
        if k == 0:
            ex += qr + [r(A_GX - 18.5, A_EIXO_Y - 8, 37, 14, eng),
                        f'<text x="{A_GX + o}" y="{A_EIXO_Y - 10 + o}" font-size="3.5" text-anchor="middle" {txt}>dobradiça</text>']
        extras.append(ex)
    svg('caixa_v2_A.svg', ['Tampa 1 (de cima)', 'Tampa 2 (meio)', 'Tampa 3 (de baixo)'], extras)
    svg('caixa_v2_B.svg', ['Tampa'], [qr + [f'<circle cx="{CAPS[0] + o:.2f}" cy="{CAPS[1] + o:.2f}" r="{(CAP_D + 0.4) / 2:.2f}" {cut}/>']])


# ======================= saída =======================
def salvar(m, nome):
    k = m.to_mesh()
    t = trimesh.Trimesh(vertices=np.asarray(k.vert_properties)[:, :3], faces=np.asarray(k.tri_verts))
    t.merge_vertices()
    t.apply_translation(-t.bounds[0])
    os.makedirs(os.path.join(AQUI, 'stl_v2'), exist_ok=True)
    t.export(os.path.join(AQUI, 'stl_v2', nome + '.stl'))
    ok = 'ok' if t.is_watertight else 'MALHA ABERTA'
    assert max(t.extents[:2]) <= 220 and t.extents[2] <= 250, nome + ' não cabe na Ender'
    print(f'  {nome:28s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  {ok}')


def pack(m):
    k = m.to_mesh()
    v = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)
    return {'v': base64.b64encode(v.tobytes()).decode(), 'f': base64.b64encode(np.asarray(k.tri_verts).astype(np.uint32).tobytes()).decode()}


def vol(a, b):
    return (a ^ b).volume()


def checar():
    erros = []
    # tudo dentro da caixa
    # ---- A
    fixas = {'base_mec': a_base_mecanismo(), 'tampa': a_tampa(), 'dobradica': a_dobradica(), 'caixa': caixa()}
    for n, _g, _c, m in comprados_comuns():
        fixas[n] = m
    fixas['servo'] = servo_modelo(Z_ORELHA - 15.6)
    nomes = list(fixas)
    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            a, b = nomes[i], nomes[j]
            if {a, b} in ({'base_mec', 'servo'},):
                continue
            v = vol(fixas[a], fixas[b])
            if v > 0.05:
                erros.append(f'A parado: {a} x {b} = {v:.1f} mm3')
    for ang in range(0, 61, 3):
        g = a_garra_ang(ang)
        for n in ('tampa', 'dobradica', 'base_mec', 'Semáforo LED'):
            v = vol(g, fixas[n])
            if v > 0.05:
                erros.append(f'A garra {ang}°: x {n} = {v:.1f}')
        v = vol(g, a_lingueta(ling_off(ANG_SOLTA)))
        if v > 0.05:
            erros.append(f'A garra {ang}° x lingueta solta = {v:.1f}')
    for ang in range(int(ANG_TRAVA), int(ANG_SOLTA) + 1, 5):
        li, br = a_lingueta(ling_off(ang)), a_braco(ang)
        for n, m in (('base_mec', fixas['base_mec']), ('tampa', fixas['tampa'])):
            for pn, p in (('lingueta', li), ('braço', br)):
                v = vol(p, m)
                if v > 0.05:
                    erros.append(f'A servo {ang}°: {pn} x {n} = {v:.1f}')
        v = vol(li, br)
        if v > 0.05:
            erros.append(f'A servo {ang}°: lingueta x braço = {v:.1f}')
        v = vol(li, a_garra())
        if v > 0.05 and ang > ANG_TRAVA + 1:
            erros.append(f'A servo {ang}°: lingueta x gancho = {v:.1f}')
    trava = vol(a_lingueta(0), cubo(HOOK[0] - 2, HOOK[1] - 3, Z_ENTALHE[0], HOOK[0], HOOK[1] + 3, Z_ENTALHE[1]))
    if trava < 1:
        erros.append('A: a lingueta não entra no entalhe')
    if vol(a_lingueta(ling_off(ANG_SOLTA)), a_garra()) > 0.05:
        erros.append('A: com o servo em 90° a lingueta ainda prende o gancho')
    # ---- B
    fb = {'base': b_base(), 'tampa': b_tampa(), 'capsula': b_capsula() + b_anel(), 'caixa': caixa()}
    for n, _g, _c, m in comprados_comuns():
        fb[n] = m
    for ang in range(0, 121, 5):
        br, _ = b_braco(ang)
        im = b_imas(ang)
        for n in fb:
            for pn, p in (('braço', br), ('ímãs', im)):
                v = vol(p, fb[n])
                if v > 0.05:
                    erros.append(f'B servo {ang}°: {pn} x {n} = {v:.1f}')
    return erros


if __name__ == '__main__':
    print(f'Caixa interna {LX} x {LY} x {H}; externa {LX + 2 * MDF:.0f} x {LY + 2 * MDF:.0f} x {H + MDF:.1f} (+ tampa A {CAMADAS_A * MDF:.0f} / B {MDF:.0f})')
    print(f'Servo: apoio das orelhas a {Z_ORELHA:.1f} mm do fundo; braço plástico em {Z_BRACO} mm (calços acertam)')
    print(f'Biela: curso da lingueta {CURSO:.1f} mm entre {ANG_TRAVA:.0f}° e {ANG_SOLTA:.0f}°')
    erros = checar()
    print('Checagem de colisões:', 'nenhuma' if not erros else '')
    for e in erros:
        print('  -', e)
    print('Versão A:')
    salvar(a_base_mecanismo(), 'A1_base_servo_e_trilho')
    salvar(a_lingueta_corpo(), 'A2a_lingueta_corpo')
    salvar(a_lingueta_garfo(), 'A2b_lingueta_garfo')
    salvar(a_braco(0).translate([-SX, -SY, -Z_BRACO]), 'A3_braco_biela')
    salvar(a_garra().rotate([180, 0, 0]), 'A4_garra_dentes')
    salvar(a_dobradica(), 'A5_dobradica')
    salvar(a_pino_chave().rotate([180, 0, 0]), 'A6_pino_da_chave')
    print('Versão B:')
    salvar(b_base(), 'B1_base_servo')
    salvar(b_braco(0)[0].translate([-SX, -SY, -Z_BRACO]), 'B2_braco_imas')
    salvar(b_capsula(), 'B3_capsula_embreagem')
    salvar(b_anel(), 'B4_anel_capsula')
    salvar(teste_embreagem(), 'B5_teste_embreagem')
    print('Comuns:')
    salvar(calcos(), 'C1_calcos_servo')
    salvar(uniao([batente().translate([k * 13, 0, 0]) for k in range(6)]), 'C2_batentes_x6')
    salvar(uniao([canto_tampa(x, y) for x, y in [(3, 6), (12, 6)]]), 'C3_cantos_tampa_x2')
    svgs()

    # maquete
    def partes_comuns(tampa, tz):
        return [('Caixa (MDF)', 'casca', '#c8a77a', caixa(), None),
                ('Tampa (MDF)', 'casca', '#d9bc8c', tampa, None)] + [(n, g, c, m, None) for n, g, c, m in comprados_comuns()] + \
               [('Servo SG90', 'comprada', '#1d4ed8', servo_modelo(Z_ORELHA - 15.6), None)]
    A = partes_comuns(a_tampa(), A_TZ) + [
        ('Garra com dentes', 'impressa', '#db2777', a_garra(), 'garra'),
        ('Dobradiça', 'impressa', '#be185d', a_dobradica(), None),
        ('Base do servo e trilho', 'impressa', '#ea580c', a_base_mecanismo(), None),
        ('Lingueta', 'impressa', '#f59e0b', a_lingueta(), 'lingueta'),
        ('Braço do servo (biela)', 'impressa', '#2563eb', a_braco(0).translate([-SX, -SY, -Z_BRACO]), 'braco'),
        ('Pino da chave', 'impressa', '#9d174d', a_pino_chave(), 'pino_chave'),
        ('Chave fim de curso', 'comprada', '#334155', cubo(PLUNGER[0] - 4, PLUNGER[1] - 12, H - 9, PLUNGER[0] + 9.7, PLUNGER[1] + 13, H - 3.2), None),
    ]
    B = partes_comuns(b_tampa(), B_TZ) + [
        ('Base do servo', 'impressa', '#ea580c', b_base(), None),
        ('Braço dos ímãs', 'impressa', '#2563eb', b_braco(0)[0].translate([-SX, -SY, -Z_BRACO]), 'braco'),
        ('Ímãs 15 × 5 (2)', 'comprada', '#d4d4d8', b_imas(0).translate([-SX, -SY, -Z_BRACO]), 'braco'),
        ('Cápsula da embreagem', 'impressa', '#f59e0b', b_capsula() + b_anel(), None),
        ('Embreagem da etiqueta', 'comprada', '#71717a', cil(CAPS[0], CAPS[1], H + CAV, H + CAV + EMB[1], EMB[0]), None),
        ('Pino da etiqueta', 'comprada', '#e4e4e7', cil(CAPS[0], CAPS[1], H + CAV + EMB[1] + 2.9 - 16, H + CAV + EMB[1] + 2.9, PINO_ETQ) + cil(CAPS[0], CAPS[1], H + CAV + EMB[1] + 2.9, H + CAV + EMB[1] + 4.4, 12), 'pino'),
    ]
    dados = {
        'A': {'pivo_braco': [SX, SY, Z_BRACO], 'pivo_garra': [A_GX, A_EIXO_Y, A_GZ0 + A_EIXO_DZ], 'biela': [SX, R_BIELA, PINO_X_TRAVA],
              'trava': ANG_TRAVA, 'solta': ANG_SOLTA, 'tz': A_TZ, 'dentes': [A_EIXO_Y + u for u in DENTES_U], 'gx': A_GX,
              'furos': [[float(a), float(b)] for a, b in a_furos_por_camada()[0][2][:4]], 'fundo_furo': H - 1.5,
              'partes': [dict(nome=n, grupo=g, cor=c, mov=mv, **pack(m)) for n, g, c, m, mv in A]},
        'B': {'pivo_braco': [SX, SY, Z_BRACO], 'repouso': ANG_REPOUSO, 'soltar': ANG_SOLTAR, 'tz': B_TZ,
              'partes': [dict(nome=n, grupo=g, cor=c, mov=mv, **pack(m)) for n, g, c, m, mv in B]},
    }
    open(os.path.join(AQUI, 'maquete_v2.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('maquete_v2.js ok')
