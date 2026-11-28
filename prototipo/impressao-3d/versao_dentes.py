"""Versão garra com dentes: a garra empurra o tecido para dentro de furos da tampa.

O pano entra em zigue-zague em 4 furos. Cada volta em quina multiplica o atrito
(efeito cabrestante: F_solta = F_segura * e^(mu*theta)). A garra trava com o
gancho na lingueta (mesmo clique da versão MDF) e o servo solta.

Rodar: python versao_dentes.py
Saída: stl_dentes/*.stl, mdf/caixa_dentes.svg, maquete_dentes.js
"""
import json, os
import numpy as np
import trimesh
import gerar_pecas as g

g.FUNDO = 3.0
g.Z_SERVO = g.FUNDO + g.BASE_MEC
import lingueta as L
import versao_mdf as V
from gerar_pecas import cubo, cil, cil_y, uniao

AQUI = os.path.dirname(os.path.abspath(__file__))
CX, CY, CZ, MDF, TZ, GZ0 = V.CX, V.CY, V.CZ, V.MDF, V.TZ, V.GZ0
DOB_X, EIXO, ESP = V.DOB_X - 24, V.EIXO, V.ESP     # dobradiça mais para trás, longe do trilho
HX, HY = V.HX, V.HY

DENTES_X = [108.0, 117.0, 126.0, 135.0]   # centro de cada dente (abs)
DENTE_L, DENTE_H, DENTE_Y = 4.0, 8.0, 26.0
FURO_L = 7.5                               # dente + 2 camadas de pano + folga do arco
FURO_Y = DENTE_Y + 3
FUNDO_FURO = CZ - 9.0
FOLGA_ARCO = 1.5                           # a garra gira: o dente sai inclinado                      # profundidade do encaixe


def garra():
    c = HX - DOB_X + 6
    barra = cubo(7, -15, 0, c, 15, ESP)
    junta = cubo(0, -10, 0, 7, 10, ESP) + cil_y(0, EIXO, -10, 10, 9)
    gg = uniao([barra, junta])
    gg = gg - cubo(-20, -20, -10, c + 5, 20, 0)
    gg = gg - cil_y(0, EIXO, -12, 12, 3.4)
    for x in DENTES_X:
        lx = x - DOB_X
        d = cubo(lx - DENTE_L / 2, -DENTE_Y / 2, -DENTE_H + 2, lx + DENTE_L / 2, DENTE_Y / 2, 0.01)
        d = d + cil_y(lx, -DENTE_H + 2, -DENTE_Y / 2, DENTE_Y / 2, DENTE_L)   # ponta arredondada
        gg = gg + d
    hx = HX - DOB_X
    gancho = cubo(hx - 2, -3, 53.0 - GZ0, hx + 2, 3, 0.5)
    gancho = gancho - cubo(hx - 2.1, -4, L.ENT_Z0 - GZ0, hx, 4, L.ENT_Z1 - GZ0)
    gancho = gancho - V.prisma_xz([[hx - 2.1, 52.9 - GZ0], [hx + 0.2, 52.9 - GZ0], [hx - 2.1, 55.2 - GZ0]], -4, 4)
    return gg + gancho


REF_X0, REF_X1 = DENTES_X[0] - 8, DENTES_X[-1] + 10   # reforço de MDF colado sob a tampa
REF_Y0, REF_Y1 = HY - FURO_Y / 2 - 4, HY + FURO_Y / 2 + 4


def reforco():
    """Segunda chapa de MDF com os mesmos furos, colada por baixo da tampa: furo com 6 mm de parede."""
    b = cubo(REF_X0, REF_Y0, CZ - MDF, REF_X1, REF_Y1, CZ)
    for x in DENTES_X:
        b = b - cubo(x - FURO_L / 2, HY - FURO_Y / 2, CZ - MDF - 1, x + FURO_L / 2 + FOLGA_ARCO, HY + FURO_Y / 2, CZ + 1)
    return b


def tampa_3d():
    t = cubo(0, 0, CZ, CX, CY, TZ)
    t = t - cubo(HX - 2.5, HY - 4, CZ - 1, HX + 4, HY + 4, TZ + 1) - cubo(18, 10, CZ - 1, 70, 20, TZ + 1)
    for x in DENTES_X:
        t = t - cubo(x - FURO_L / 2, HY - FURO_Y / 2, CZ - 1, x + FURO_L / 2 + FOLGA_ARCO, HY + FURO_Y / 2, TZ + 1)
    return t


def dobradica():
    """Orelhas da dobradiça coladas na tampa. Eixo: prego fino ou palito de churrasco."""
    z = TZ
    base = cubo(DOB_X - 8, HY - 18, z, DOB_X + 6, HY + 18, z + 2)
    orelhas = uniao([cubo(DOB_X - 6, y0, z, DOB_X + 6, y0 + 3.5, z + 5.5) + cil_y(DOB_X, GZ0 + EIXO, y0, y0 + 3.5, 12)
                     for y0 in (HY - 16.0, HY + 12.5)])
    d = base + orelhas
    d = d - cil_y(DOB_X, GZ0 + EIXO, HY - 30, HY + 30, 3.4)
    d = d - cubo(DOB_X - 8, HY - 11, z + 0.3, DOB_X + 10, HY + 11, z + 3)
    return d


def svg():
    cut = 'fill="none" stroke="#ff0000" stroke-width="0.1"'
    eng = 'fill="none" stroke="#000000" stroke-width="0.3"'
    txt = 'font-family="Arial" fill="#000000"'

    def r(x, y, w, h, extra=''):
        return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" {extra}/>'
    fx, fy = CX - 2 * MDF, CY - 2 * MDF
    tampa = [r(0, 0, CX, CY, cut), r(HX - 2.5, HY - 4, 6.5, 8, cut), r(18, 10, 52, 10, cut),
             f'<circle cx="6" cy="38" r="1.25" {cut}/>', f'<circle cx="{CX - 4.5}" cy="38" r="1.25" {cut}/>',
             r(30, 40, 30, 30, eng), f'<text x="45" y="38" font-size="4" text-anchor="middle" {txt}>cole o QR aqui</text>',
             r(DOB_X - 8, HY - 18, 14, 36, eng), f'<text x="95" y="62" font-size="3.5" text-anchor="middle" {txt}>dobradiça</text>',
             f'<text x="44" y="27" font-size="4" text-anchor="middle" {txt}>Tag&amp;Go</text>']
    for x in DENTES_X:
        tampa.append(r(x - FURO_L / 2, HY - FURO_Y / 2, FURO_L + FOLGA_ARCO, FURO_Y, cut))
    pecas = [('Tampa', CX, CY, tampa),
             ('Fundo', fx, fy, [r(0, 0, fx, fy, cut), r(175 - MDF, 61 - MDF, 20, 5, cut)]),
             ('Parede longa 1', CX, CZ, [r(0, 0, CX, CZ, cut)]), ('Parede longa 2', CX, CZ, [r(0, 0, CX, CZ, cut)]),
             ('Parede curta 1', fy, CZ, [r(0, 0, fy, CZ, cut), r(fy / 2 - 6, CZ - 22, 12, 10, cut)]),
             ('Parede curta 2', fy, CZ, [r(0, 0, fy, CZ, cut)])]
    W = 450
    x, y, linha, out = 5, 5, 0, []
    for nome, w, h, els in pecas:
        if x + w > W:
            x, y, linha = 5, y + linha + 12, 0
        out.append(f'<g transform="translate({x},{y})"><title>{nome}</title>{"".join(els)}'
                   f'<text x="{w / 2}" y="{h + 6}" font-size="4" text-anchor="middle" fill="#0000ff">{nome}</text></g>')
        x += w + 8
        linha = max(linha, h)
    H = y + linha + 12
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n'
         '<!-- MDF 3 mm. Vermelho = cortar. Preto = gravar. Azul = legenda: apagar antes do laser. -->\n'
         + '\n'.join(out) + '\n</svg>')
    open(os.path.join(AQUI, 'mdf', 'caixa_dentes.svg'), 'w', encoding='utf-8').write(s)


def salvar(m, nome):
    k = m.to_mesh()
    t = trimesh.Trimesh(vertices=np.asarray(k.vert_properties)[:, :3], faces=np.asarray(k.tri_verts))
    t.apply_translation(-t.bounds[0])
    os.makedirs(os.path.join(AQUI, 'stl_dentes'), exist_ok=True)
    t.export(os.path.join(AQUI, 'stl_dentes', nome + '.stl'))
    print(f'{nome:24s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  fechada={t.is_watertight}')


if __name__ == '__main__':
    salvar(L.mecanismo_lingueta(), 'D1_trilho_e_servo')
    salvar(L.lingueta(), 'D2_lingueta')
    salvar(L.braco_servo(), 'D3_braco_servo')
    salvar(garra().rotate([90, 0, 0]), 'D4_garra_dentes')
    salvar(dobradica(), 'D6_dobradica')
    salvar(uniao([V.canto_tampa().translate([k * 9, 0, 0]) for k in range(2)]), 'D7_cantos_tampa')
    salvar(g.prateleira_esp32().rotate([180, 0, 0]), 'D8_prateleira_esp32')
    svg()

    zpb = g.FUNDO + 1
    sx0 = L.SX - g.SERVO_EIXO_PONTA
    partes = [
        ('Caixa (MDF)', 'casca', '#c8a77a', V.caixa_3d(), None),
        ('Tampa (MDF)', 'casca', '#d9bc8c', tampa_3d(), None),
        ('Garra com dentes', 'impressa', '#db2777', garra(), 'garra'),
        ('Dobradiça', 'impressa', '#be185d', dobradica(), None),
        ('Lingueta', 'impressa', '#f59e0b', L.lingueta(), 'lingueta'),
        ('Trilho e berço do servo', 'impressa', '#ea580c', L.mecanismo_lingueta(), None),
        ('Braço do servo', 'impressa', '#2563eb', L.braco_servo(), 'braco'),
        ('Prateleira do ESP32', 'impressa', '#0d9488', g.prateleira_esp32().translate([0, 0, g.FUNDO]), None),
        ('Servo SG90', 'comprada', '#1d4ed8', cubo(sx0, L.SY - 6.1, g.Z_SERVO + 9, sx0 + 22.7, L.SY + 6.1, L.Z_ORELHA + 6)
         + cubo(sx0 - 4.8, L.SY - 6.1, L.Z_ORELHA, sx0 + 27.5, L.SY + 6.1, L.Z_ORELHA + 2.5)
         + cil(L.SX, L.SY, L.Z_ORELHA + 6, L.Z_BRACO, 5), None),
        ('Power bank', 'comprada', '#1f2937', cubo(g.PB_X0, 4, zpb, g.PB_X0 + 149, 72, zpb + 15), None),
        ('ESP32 + expansor', 'comprada', '#15803d', cubo(40, 11, 25, 109, 65, 41) + cubo(48, 24, 41, 101, 52, 45), None),
        ('Semáforo LED', 'comprada', '#111827', cubo(17, 8, CZ - 6, 71, 22, CZ - 0.2)
         + uniao([cil(x, 15, CZ - 1, CZ + 1, 8, 24) for x in (30, 44, 58)]), None),
        ('QR code', 'comprada', '#f8fafc', cubo(30, 40, TZ, 60, 70, TZ + 0.4), None),
        ('Elástico da lingueta', 'comprada', '#111827', cubo(155.5, 44.4, 58.6, 200, 45.6, 59.4), 'elastico'),
    ]
    dados = {'pivo_braco': [L.SX, L.SY, L.Z_BRACO], 'pivo_garra': [DOB_X, HY, GZ0 + EIXO], 'garra_z0': GZ0,
             
             'dentes': DENTES_X, 'furo_l': FURO_L, 'fundo_furo': GZ0 - DENTE_H + 2.8, 'tz': TZ, 'pano_y': [HY - 16, HY + 16],
             'partes': []}
    for nome, grupo, cor, m, mov in partes:
        d = {'nome': nome, 'grupo': grupo, 'cor': cor, 'mov': mov}
        d.update(V.pack(m))
        dados['partes'].append(d)
    open(os.path.join(AQUI, 'maquete_dentes.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('ok')
