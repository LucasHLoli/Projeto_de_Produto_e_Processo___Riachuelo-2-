"""Gera os STL do protótipo Tag&Go (impressora Ender, PLA) e o SVG da base em MDF.

Rodar:  python gerar_pecas.py
Saída:  stl/*.stl, mdf/base_exposicao.svg, previa.png

Todas as medidas em mm. As medidas marcadas MEDIR são estimativas:
confira com paquímetro e mude aqui antes de imprimir a peça final.
"""
import os
import numpy as np
import trimesh
from manifold3d import Manifold

AQUI = os.path.dirname(os.path.abspath(__file__))
SEG = 64

# ---------------- medidas das peças compradas ----------------
EMBREAGEM_D = 13.0      # MEDIR: diâmetro do copinho de metal da etiqueta
EMBREAGEM_H = 11.0      # MEDIR: altura do copinho
PINO_D = 3.0            # MEDIR: grossura do pino da etiqueta
CABECA_D = 13.0         # MEDIR: diâmetro da cabeça do pino
IMA_D, IMA_H, N_IMAS = 10.0, 4.0, 3
SERVO_C, SERVO_L = 22.7, 12.2          # corpo do SG90
SERVO_EIXO_PONTA = 5.95                 # do eixo até a ponta mais próxima do corpo
SERVO_FURO_ENTRE = 27.5                 # distância entre os furos das orelhas
SERVO_ORELHA_Z = 15.9   # MEDIR: do fundo do servo até a parte de baixo da orelha
SERVO_BRACO_Z = 16.1    # MEDIR: da parte de baixo da orelha até o topo do braço plástico
FOLGA = 0.3             # folga de encaixe para a Ender

# ---------------- caixa ----------------
CX, CY = 210.0, 76.0    # tamanho externo
PAREDE, FUNDO, TAMPA = 2.0, 1.6, 3.0
BASE_MEC = 2.0          # espessura da placa do mecanismo

# posições (coordenadas da caixa, origem no canto externo de baixo)
EMB_X, EMB_Y = 184.0, 38.0               # eixo do pino e da embreagem
SERVO_X, SERVO_Y = EMB_X, EMB_Y - 16.0   # eixo do servo, 16 mm do pino

# alturas encadeadas
Z_SERVO = FUNDO + BASE_MEC
Z_ORELHA = Z_SERVO + SERVO_ORELHA_Z
Z_BRACO = Z_ORELHA + SERVO_BRACO_Z       # topo do braço do servo
COPO_H = N_IMAS * IMA_H                   # copo dos ímãs
Z_COPO_TOPO = Z_BRACO + COPO_H
Z_PRAT_BAIXO = Z_COPO_TOPO + 0.2          # 0,2 mm de folga ímã x prateleira
PRAT = 0.8
Z_EMB_BAIXO = Z_PRAT_BAIXO + PRAT
Z_EMB_TOPO = Z_EMB_BAIXO + EMBREAGEM_H
CZ = round(Z_EMB_TOPO + 1.4, 1)          # altura da parede (tampa apoia aqui)

PB_X0 = 9.0             # power bank 149 x 69 x 15 começa aqui
CHAVE_TAMPA = (162.0, EMB_Y)             # pino que aperta a chave da garra
DOBRA_X = 138.0                          # eixo da dobradiça da garra


def cubo(x0, y0, z0, x1, y1, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def cil(x, y, z0, z1, d, seg=SEG):
    return Manifold.cylinder(z1 - z0, d / 2, d / 2, seg).translate([x, y, z0])


def cil_y(x, z, y0, y1, d):
    return Manifold.cylinder(y1 - y0, d / 2, d / 2, SEG).rotate([-90, 0, 0]).translate([x, y0, z])


def uniao(lista):
    m = lista[0]
    for o in lista[1:]:
        m = m + o
    return m


def salvar(m, nome):
    mesh = m.to_mesh()
    t = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts))
    # deita no chão da impressora
    t.apply_translation([-t.bounds[0][0], -t.bounds[0][1], -t.bounds[0][2]])
    os.makedirs(os.path.join(AQUI, 'stl'), exist_ok=True)
    t.export(os.path.join(AQUI, 'stl', nome + '.stl'))
    ext = t.bounds[1]
    print(f'{nome:28s} {ext[0]:6.1f} x {ext[1]:5.1f} x {ext[2]:5.1f} mm  {t.volume / 1000:5.1f} cm3')
    return t


# ---------------- 01 peça de teste de encaixe ----------------
def teste_encaixe():
    p = cubo(0, 0, 0, 92, 40, 6)
    furos = []
    for i, d in enumerate([EMBREAGEM_D - 0.2, EMBREAGEM_D + 0.1, EMBREAGEM_D + 0.4, EMBREAGEM_D + 0.7]):
        furos.append(cil(12 + i * 22, 12, 1, 7, d))
    for i, d in enumerate([IMA_D, IMA_D + 0.2, IMA_D + 0.4, IMA_D + 0.6]):
        furos.append(cil(12 + i * 22, 30, 2, 7, d))
    p = p - uniao(furos)
    # marcas: 1 a 4 entalhes indicam o furo (1 = mais justo)
    for i in range(4):
        for k in range(i + 1):
            p = p - cubo(4 + i * 22 + k * 2.2, 0, 4.5, 5.2 + i * 22 + k * 2.2, 2, 7)
    return p


# ---------------- 02 calços do servo ----------------
def calcos():
    pecas = []
    for i, h in enumerate([0.5, 1.0, 1.5, 2.0]):
        c = cubo(0, i * 12, 0, 36, i * 12 + 9, h)
        c = c - cil(4.25, i * 12 + 4.5, -1, 3, 2.4) - cil(4.25 + SERVO_FURO_ENTRE, i * 12 + 4.5, -1, 3, 2.4)
        c = c - cubo(8, i * 12 + 1.5, -1, 28, i * 12 + 7.5, 3)
        pecas.append(c)
    return uniao(pecas)


# ---------------- 03 mecanismo (servo + prateleira + berço da embreagem) ----------------
def mecanismo():
    x0, x1, y0, y1 = 166.0, 202.0, 4.0, 53.0
    placa = cubo(x0, y0, FUNDO, x1, y1, Z_SERVO)
    # corpo do servo: eixo perto de uma ponta
    sx0 = SERVO_X - SERVO_EIXO_PONTA
    sx1 = sx0 + SERVO_C
    sy0, sy1 = SERVO_Y - SERVO_L / 2, SERVO_Y + SERVO_L / 2
    cx = (sx0 + sx1) / 2
    berco_servo = cubo(cx - 18, sy0 - 4, Z_SERVO, cx + 18, sy1 + 4, Z_ORELHA)
    berco_servo = berco_servo - cubo(sx0 - FOLGA, sy0 - FOLGA, Z_SERVO - 0.5, sx1 + FOLGA, sy1 + FOLGA, Z_ORELHA + 1)
    for fx in (cx - SERVO_FURO_ENTRE / 2, cx + SERVO_FURO_ENTRE / 2):
        berco_servo = berco_servo - cil(fx, SERVO_Y, Z_ORELHA - 8, Z_ORELHA + 1, 1.9)
    # saída do fio do servo
    berco_servo = berco_servo - cubo(sx1 - 2, SERVO_Y - 2.5, Z_SERVO - 0.5, cx + 19, SERVO_Y + 2.5, Z_SERVO + 6)
    # torre que segura a prateleira e o berço da embreagem
    torre = cubo(EMB_X - 10, 47.0, Z_SERVO, EMB_X + 10, 53.0, Z_PRAT_BAIXO)
    torre = torre - cil(EMB_X, 50.0, Z_PRAT_BAIXO - 10, Z_PRAT_BAIXO + 1, 2.6)
    corpo = uniao([placa, berco_servo, torre])
    # furos para prender no fundo da caixa (parafuso M3 de 8 mm)
    for (hx, hy) in [(170, 8), (198, 8), (170, 44), (198, 40)]:
        corpo = corpo - cil(hx, hy, FUNDO - 1, Z_SERVO + 0.1, 3.4)
    return corpo


# ---------------- 03b berço da embreagem (imprimir com a prateleira na mesa) ----------------
def berco_embreagem():
    anel = cil(EMB_X, EMB_Y, Z_PRAT_BAIXO, Z_EMB_TOPO - 1.0, EMBREAGEM_D + 6)
    aba = cubo(EMB_X - 7, EMB_Y, Z_PRAT_BAIXO, EMB_X + 7, 53.0, Z_EMB_BAIXO + 4)
    b = anel + aba
    b = b - cil(EMB_X, EMB_Y, Z_EMB_BAIXO, Z_EMB_TOPO + 5, EMBREAGEM_D + FOLGA)
    b = b - cil(EMB_X, 50.0, Z_PRAT_BAIXO - 1, Z_EMB_BAIXO + 5, 3.4)
    return b


# ---------------- 04 braço dos ímãs ----------------
def braco_imas():
    L = 16.0
    barra = cubo(-4, -4, 0, L, 4, 3)
    barra = barra + cil(0, 0, 0, 3, 8)
    copo = cil(L, 0, 0, COPO_H, IMA_D + 4)
    b = barra + copo
    b = b - cil(L, 0, COPO_H - N_IMAS * IMA_H, COPO_H + 1, IMA_D + 0.2)
    b = b - cil(0, 0, -1, 4, 2.2)                     # parafuso do meio do servo
    b = b - cubo(-3.5, -2.3, -1, L - 7, 2.3, 1.3)     # encaixe do braço plástico (por baixo)
    return b


# ---------------- 05 caixa ----------------
def caixa():
    c = cubo(0, 0, 0, CX, CY, CZ) - cubo(PAREDE, PAREDE, FUNDO, CX - PAREDE, CY - PAREDE, CZ + 1)
    # pilares da tampa nas pontas
    for x in (PAREDE + 3.5, CX - PAREDE - 3.5):
        c = c + (cil(x, CY / 2, 0, CZ, 8) - cil(x, CY / 2, 4, CZ + 1, 2.6))
    # pernas da prateleira do ESP32 (fora do power bank)
    # furos do mecanismo no fundo
    for (hx, hy) in [(170, 8), (198, 8), (170, 44), (198, 40)]:
        c = c - cil(hx, hy, -1, FUNDO + 1, 2.7)
    # rasgo da chave da base
    c = c - cubo(175, 61, -1, 195, 66, FUNDO + 1)
    # saída de cabo opcional na ponta esquerda
    c = c - cubo(-1, CY / 2 - 6, FUNDO + 4, PAREDE + 1, CY / 2 + 6, FUNDO + 14)
    # batente do power bank
    c = c + cubo(PB_X0 + 149 + 0.5, PAREDE, FUNDO, PB_X0 + 149 + 2.5, 14, FUNDO + 8)
    c = c + cubo(PB_X0 + 149 + 0.5, CY - 14, FUNDO, PB_X0 + 149 + 2.5, CY - PAREDE, FUNDO + 8)
    return c


# ---------------- 06 tampa ----------------
def tampa():
    t = cubo(0, 0, 0, CX, CY, TAMPA)
    for x in (PAREDE + 3.5, CX - PAREDE - 3.5):
        t = t - cil(x, CY / 2, -4, TAMPA + 1, 3.4)
        t = t - cil(x, CY / 2, TAMPA - 1.6, TAMPA + 1, 6.4)
    t = t - cil(EMB_X, EMB_Y, -4, TAMPA + 1, 6.0)                      # furo do pino
    t = t - cil(CHAVE_TAMPA[0], CHAVE_TAMPA[1], -4, TAMPA + 1, 4.5)    # pino da chave
    t = t - cubo(30, 33, -4, 80, 43, TAMPA + 1)                        # janela dos LEDs
    t = t - cubo(90, 22, TAMPA - 0.6, 122, 54, TAMPA + 1)              # rebaixo do QR code
    # orelhas da dobradiça
    for y0 in (20.0, 52.5):
        o = cubo(DOBRA_X - 6, y0, TAMPA, DOBRA_X + 6, y0 + 3.5, TAMPA + 9) + cil_y(DOBRA_X, TAMPA + 9, y0, y0 + 3.5, 12)
        o = o - cil_y(DOBRA_X, TAMPA + 7, y0 - 1, y0 + 5, 3.3)
        t = t + o
    t = t - cil(DOBRA_X - 10, EMB_Y, -4, TAMPA + 1, 2.2)               # perna da mola
    return t


# ---------------- 07 garra ----------------
def garra():
    # coordenadas locais: dobradiça em x=0, fundo da barra em z=0
    comp = EMB_X - DOBRA_X + 8
    largura = 31.0
    eixo_z = 5.0
    barra = cubo(0, -largura / 2, 0, comp, largura / 2, 6)
    junta = cil_y(0, eixo_z, -largura / 2 + 1.0, largura / 2 - 1.0, 11)
    g = barra + junta
    g = g - cubo(-8, -largura / 2 - 1, -8, comp + 1, largura / 2 + 1, 0)       # corta o que passa do chão
    g = g - cil_y(0, eixo_z, -largura, largura, 3.5)                            # eixo M3
    # folga para as orelhas da tampa
    g = g - cubo(-7, -largura / 2 - 1, -1, 7, -largura / 2 + 1.0 + 0.0, 12)
    g = g - cubo(-7, largura / 2 - 1.0, -1, 7, largura / 2 + 1, 12)
    px = EMB_X - DOBRA_X
    g = g - cil(px, 0, -1, 7, PINO_D + FOLGA)                                   # passagem do pino
    g = g - cil(px, 0, 6 - 2.2, 7, CABECA_D + FOLGA)                            # rebaixo da cabeça
    g = g - cil(10, 0, -1, 7, 2.2)                                              # perna da mola
    # sulcos para a borracha (lado de baixo)
    for k in range(5):
        g = g - cubo(18 + k * 5, -largura / 2 + 3, -1, 19.5 + k * 5, largura / 2 - 3, 0.6)
    return g


# ---------------- 08 prateleira do ESP32 ----------------
def prateleira_esp32():
    x0, x1 = PAREDE + 8.0, PB_X0 + 149 - 2
    y0, y1 = PAREDE + 0.5, CY - PAREDE - 0.5
    alt = 21.0                      # vão para o power bank + receptor
    p = cubo(x0, y0, alt, x1, y1, alt + 2)
    p = p - cubo(x0 + 15, y0 + 12, alt - 1, x1 - 15, y1 - 12, alt + 3)     # janela para fios
    pernas = [cubo(x, y, 0, x + 5, y + 5, alt) for x in (x0, x1 - 5) for y in (y0, y1 - 5)]
    # as pernas ficam nas pontas, fora do power bank no comprimento
    return p + uniao(pernas)


# ---------------- 09 pino da chave ----------------
def pino_chave():
    return cil(0, 0, 0, 1.5, 7.5) + cil(0, 0, 1.5, 1.5 + TAMPA + 3, 4.0)


def svg_mdf():
    W, H = 300, 200
    QX, QY = 216, 92
    ox, oy = (W - QX) / 2, 70
    cut = 'fill="none" stroke="#ff0000" stroke-width="0.1"'
    eng = 'fill="#000000"'
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{2 * W + 10}mm" height="{H}mm" viewBox="0 0 {2 * W + 10} {H}">
<!-- Vermelho = cortar. Preto = gravar. MDF 3 mm. Duas placas: cole a de cima (com o recorte) sobre a de baixo. -->
<g id="placa_de_baixo">
<rect x="0" y="0" width="{W}" height="{H}" rx="8" {cut}/>
<text x="{W / 2}" y="40" font-family="Arial" font-size="22" text-anchor="middle" {eng}>Tag&amp;Go</text>
<text x="{W / 2}" y="185" font-family="Arial" font-size="7" text-anchor="middle" {eng}>PRO3474 · Grupo 4 · Poli-USP</text>
</g>
<g id="placa_de_cima" transform="translate({W + 10},0)">
<rect x="0" y="0" width="{W}" height="{H}" rx="8" {cut}/>
<rect x="{ox}" y="{oy}" width="{QX}" height="{QY}" rx="4" {cut}/>
<path d="M {ox + QX - 30} {oy + QY} L {ox + QX - 30} {H} M {ox + QX - 18} {oy + QY} L {ox + QX - 18} {H}" {cut}/>
<text x="{W / 2}" y="40" font-family="Arial" font-size="22" text-anchor="middle" {eng}>Tag&amp;Go</text>
<text x="{W / 2}" y="58" font-family="Arial" font-size="7" text-anchor="middle" {eng}>Apoie a etiqueta aqui para recarregar</text>
</g>
</svg>'''
    os.makedirs(os.path.join(AQUI, 'mdf'), exist_ok=True)
    open(os.path.join(AQUI, 'mdf', 'base_exposicao.svg'), 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    print(f'Altura da caixa: {CZ} mm (+ tampa {TAMPA} mm). Prateleira da embreagem a {Z_PRAT_BAIXO:.1f} mm.')
    pecas = {
        '01_teste_encaixe': teste_encaixe(),
        '02_calcos_servo': calcos(),
        '03_mecanismo': mecanismo(),
        '04_braco_imas': braco_imas(),
        '05_caixa': caixa(),
        '03b_berco_embreagem': berco_embreagem(),
        '06_tampa': tampa(),
        '07_garra': garra(),
        '08_prateleira_esp32': prateleira_esp32().rotate([180, 0, 0]),
        '09_pino_chave': pino_chave(),
    }
    malhas = {n: salvar(m, n) for n, m in pecas.items()}
    svg_mdf()
    # prévia montada
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        def mm(m):
            k = m.to_mesh(); return np.asarray(k.vert_properties)[:, :3], np.asarray(k.tri_verts)
        cena = [
            (caixa(), '#9aa5b1', 0.25), (mecanismo(), '#ea580c', 0.9), (berco_embreagem(), '#f59e0b', 0.9),
            (braco_imas().rotate([0, 0, 180]).translate([SERVO_X, SERVO_Y, Z_BRACO]), '#2563eb', 0.9),
            (prateleira_esp32().translate([0, 0, FUNDO]), '#0d9488', 0.5),
            (tampa().translate([0, 0, CZ]), '#94a3b8', 0.18),
            (garra().translate([DOBRA_X, EMB_Y, CZ + TAMPA + 2]), '#db2777', 0.9),
        ]
        fig = plt.figure(figsize=(12, 6), dpi=130)
        ax = fig.add_subplot(111, projection='3d')
        for m, cor, a in cena:
            v, f = mm(m)
            ax.add_collection3d(Poly3DCollection(v[f], facecolor=cor, edgecolor='none', alpha=a))
        ax.set_xlim(0, 210); ax.set_ylim(-20, 96); ax.set_zlim(0, 80); ax.set_box_aspect((210, 116, 80))
        ax.view_init(28, -60); ax.set_axis_off()
        ax.set_title('Tag&Go protótipo: caixa (cinza), mecanismo (laranja), braço dos ímãs (azul), prateleira ESP32 (verde), garra (rosa)', fontsize=9)
        plt.tight_layout(); plt.savefig(os.path.join(AQUI, 'previa.png'))
    except Exception as e:
        print('prévia não gerada:', e)
