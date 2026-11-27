"""Versão cabo em laço: a roupa fica presa num laço de cabo de aço, sem furar.

Uma ponta do cabo fica presa na caixa (furo A, presilha por dentro).
A outra ponta tem um plugue de PLA. O plugue entra no rasgo B da tampa,
empurra a rampa da lingueta e trava com um clique. O servo solta.

Rodar: python versao_cabo.py
Saída: stl_cabo/*.stl, mdf/caixa_cabo.svg, maquete_cabo.js
"""
import base64, json, os
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection
import gerar_pecas as g

g.FUNDO = 3.0
g.Z_SERVO = g.FUNDO + g.BASE_MEC
import lingueta as L
import versao_mdf as V
from gerar_pecas import cubo, cil, cil_y, uniao

AQUI = os.path.dirname(os.path.abspath(__file__))
CX, CY, CZ, MDF, TZ = V.CX, V.CY, V.CZ, V.MDF, V.TZ
HX, HY = L.HX, g.EMB_Y
AX, AY = 120.0, 38.0                     # furo A: ponta fixa do cabo


def plugue():
    """Em posição de montagem (encaixado). Haste 4 x 6 mm com entalhe; cabeça por cima da tampa."""
    haste = cubo(HX - 2, HY - 3, 53.0, HX + 2, HY + 3, TZ + 0.5)
    haste = haste - cubo(HX - 2.1, HY - 4, L.ENT_Z0, HX, HY + 4, L.ENT_Z1)
    haste = haste - V.prisma_xz([[HX - 2.1, 52.9], [HX + 0.2, 52.9], [HX - 2.1, 55.2]], HY - 4, HY + 4)
    cabeca = cubo(HX - 8, HY - 5, TZ, HX + 8, HY + 5, TZ + 8)
    cabeca = cabeca - cil_y(HX + 3.5, TZ + 4.5, HY - 6, HY + 6, 2.8)      # furo do cabo
    cabeca = cabeca - cil(HX - 4, HY, TZ + 5, TZ + 9, 6) if False else cabeca
    return haste + cabeca


def tampa_3d():
    t = cubo(0, 0, CZ, CX, CY, TZ)
    t = t - cubo(HX - 2.5, HY - 3.5, CZ - 1, HX + 2.5, HY + 3.5, TZ + 1)     # rasgo B do plugue
    t = t - cil(AX, AY, CZ - 1, TZ + 1, 3.5)                                 # furo A do cabo
    t = t - cubo(18, 10, CZ - 1, 70, 20, TZ + 1)                             # LEDs
    return t


def svg():
    cut = 'fill="none" stroke="#ff0000" stroke-width="0.1"'
    eng = 'fill="none" stroke="#000000" stroke-width="0.3"'
    txt = 'font-family="Arial" fill="#000000"'

    def r(x, y, w, h, extra=''):
        return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" {extra}/>'
    fx, fy = CX - 2 * MDF, CY - 2 * MDF
    pecas = [
        ('Tampa', CX, CY, [r(0, 0, CX, CY, cut), r(HX - 2.5, HY - 3.5, 5, 7, cut), f'<circle cx="{AX}" cy="{AY}" r="1.75" {cut}/>',
                           r(18, 10, 52, 10, cut), f'<circle cx="6" cy="38" r="1.25" {cut}/>', f'<circle cx="{CX - 4.5}" cy="38" r="1.25" {cut}/>',
                           r(30, 40, 30, 30, eng), f'<text x="45" y="38" font-size="4" text-anchor="middle" {txt}>cole o QR aqui</text>',
                           f'<text x="{AX}" y="{AY - 5}" font-size="3.5" text-anchor="middle" {txt}>cabo</text>',
                           r(HX - 9, HY - 6, 18, 12, eng), f'<text x="{HX}" y="{HY - 8}" font-size="3.5" text-anchor="middle" {txt}>plugue</text>',
                           f'<text x="44" y="27" font-size="4" text-anchor="middle" {txt}>Tag&amp;Go</text>']),
        ('Fundo', fx, fy, [r(0, 0, fx, fy, cut), r(175 - MDF, 61 - MDF, 20, 5, cut)]),
        ('Parede longa 1', CX, CZ, [r(0, 0, CX, CZ, cut)]),
        ('Parede longa 2', CX, CZ, [r(0, 0, CX, CZ, cut)]),
        ('Parede curta 1', fy, CZ, [r(0, 0, fy, CZ, cut), r(fy / 2 - 6, CZ - 22, 12, 10, cut)]),
        ('Parede curta 2', fy, CZ, [r(0, 0, fy, CZ, cut)]),
    ]
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
         '<!-- MDF 3 mm. Vermelho = cortar. Preto = gravar. Azul = legenda: apagar antes de mandar para o laser. -->\n'
         + '\n'.join(out) + '\n</svg>')
    open(os.path.join(AQUI, 'mdf', 'caixa_cabo.svg'), 'w', encoding='utf-8').write(s)


def salvar(m, nome):
    k = m.to_mesh()
    t = trimesh.Trimesh(vertices=np.asarray(k.vert_properties)[:, :3], faces=np.asarray(k.tri_verts))
    t.apply_translation(-t.bounds[0])
    os.makedirs(os.path.join(AQUI, 'stl_cabo'), exist_ok=True)
    t.export(os.path.join(AQUI, 'stl_cabo', nome + '.stl'))
    print(f'{nome:24s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  fechada={t.is_watertight}')


if __name__ == '__main__':
    salvar(L.mecanismo_lingueta(), 'C1_trilho_e_servo')
    salvar(L.lingueta(), 'C2_lingueta')
    salvar(L.braco_servo(), 'C3_braco_servo')
    salvar(uniao([plugue().rotate([180, 0, 0]).translate([k * 20, 0, 0]) for k in range(2)]), 'C4_plugue_x2')
    salvar(uniao([V.canto_tampa().translate([k * 9, 0, 0]) for k in range(2)]), 'C5_cantos_tampa')
    salvar(g.prateleira_esp32().rotate([180, 0, 0]), 'C6_prateleira_esp32')
    svg()

    zpb = g.FUNDO + 1
    sx0 = L.SX - g.SERVO_EIXO_PONTA
    partes = [
        ('Caixa (MDF)', 'casca', '#c8a77a', V.caixa_3d(), None),
        ('Tampa (MDF)', 'casca', '#d9bc8c', tampa_3d(), None),
        ('Plugue', 'impressa', '#db2777', plugue(), 'plugue'),
        ('Lingueta', 'impressa', '#f59e0b', L.lingueta(), 'lingueta'),
        ('Trilho e berço do servo', 'impressa', '#ea580c', L.mecanismo_lingueta(), None),
        ('Braço do servo', 'impressa', '#2563eb', L.braco_servo(), 'braco'),
        ('Prateleira do ESP32', 'impressa', '#0d9488', g.prateleira_esp32().translate([0, 0, g.FUNDO]), None),
        ('Servo SG90', 'comprada', '#1d4ed8', cubo(sx0, L.SY - 6.1, g.Z_SERVO + 9, sx0 + 22.7, L.SY + 6.1, L.Z_ORELHA + 6)
         + cubo(sx0 - 4.8, L.SY - 6.1, L.Z_ORELHA, sx0 + 27.5, L.SY + 6.1, L.Z_ORELHA + 2.5)
         + cil(L.SX, L.SY, L.Z_ORELHA + 6, L.Z_BRACO, 5), None),
        ('Power bank', 'comprada', '#1f2937', cubo(g.PB_X0, 4, zpb, g.PB_X0 + 149, 72, zpb + 15), None),
        ('Receptor Qi', 'comprada', '#475569', cubo(45, 15, g.FUNDO, 120, 60, zpb), None),
        ('ESP32 + expansor', 'comprada', '#15803d', cubo(40, 11, 25, 109, 65, 41) + cubo(48, 24, 41, 101, 52, 45), None),
        ('Semáforo LED', 'comprada', '#111827', cubo(17, 8, CZ - 6, 71, 22, CZ - 0.2)
         + uniao([cil(x, 15, CZ - 1, CZ + 1, 8, 24) for x in (30, 44, 58)]), None),
        ('QR code', 'comprada', '#f8fafc', cubo(30, 40, TZ, 60, 70, TZ + 0.4), None),
        ('Presilha do cabo (dentro)', 'comprada', '#a1a1aa', cubo(AX - 4, AY - 3, CZ - 5, AX + 4, AY + 3, CZ), None),
        ('Elástico da lingueta', 'comprada', '#111827', cubo(155.5, 44.4, 58.6, 200, 45.6, 59.4), 'elastico'),
    ]
    dados = {'pivo_braco': [L.SX, L.SY, L.Z_BRACO], 'ancora': [AX, AY, TZ], 'furo_plugue': [HX + 3.5, HY, TZ + 4.5],
             'partes': []}
    for nome, grupo, cor, m, mov in partes:
        d = {'nome': nome, 'grupo': grupo, 'cor': cor, 'mov': mov}
        d.update(V.pack(m))
        dados['partes'].append(d)
    open(os.path.join(AQUI, 'maquete_cabo.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('ok')
