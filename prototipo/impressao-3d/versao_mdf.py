"""Versão MDF + lingueta: caixa e tampa no laser, mecanismo em PLA, molas de elástico.

A garra prende a roupa por aperto (não fura). O gancho fica na ponta, depois
de um batente que impede o tecido de chegar até ele.

Rodar: python versao_mdf.py
Saída: stl_mdf/*.stl, mdf/caixa_mdf.svg, maquete_mdf.js
"""
import base64, json, os
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection
import gerar_pecas as g

# MDF de 3 mm no fundo: o mecanismo sobe junto
g.FUNDO = 3.0
g.Z_SERVO = g.FUNDO + g.BASE_MEC
import lingueta as L
from gerar_pecas import cubo, cil, cil_y, uniao

AQUI = os.path.dirname(os.path.abspath(__file__))
MDF = 3.0
CX, CY, CZ = 210.0, 76.0, 61.0           # caixa externa (sem tampa)
TZ = CZ + MDF                            # topo da tampa = 64
VAO = 1.5                                # vão da roupa entre garra e tampa
GZ0 = TZ + VAO                           # fundo da garra fechada = 65,5
DOB_X, EIXO = 120.0, 4.0                 # dobradiça; eixo 4 mm acima do fundo da garra
HX, HY = L.HX, g.EMB_Y                   # gancho (x 184, y 38)
ESP = 6.0                                # espessura da garra
BAT_X = 171.0                            # batente


def prisma_xz(pts, y0, y1):
    return Manifold.extrude(CrossSection([pts]), y1 - y0).rotate([90, 0, 0]).translate([0, y1, 0])


def garra():
    """Coordenadas locais: eixo da dobradiça em x=0; fundo da garra fechada em z=0."""
    c = HX - DOB_X + 6                                          # vai até x=190
    barra = cubo(7, -15, 0, c, 15, ESP)
    junta = cubo(-5, -10, 0, 7, 10, ESP) + cil_y(0, EIXO, -10, 10, 9)
    rabo = cubo(-15, -4, 0, -2, 4, ESP) + cil(-12, 0, ESP, ESP + 6, 3.2)
    gg = uniao([barra, junta, rabo])
    gg = gg - cubo(-20, -20, -10, c + 5, 20, 0)                  # nada abaixo do fundo
    gg = gg - cil_y(0, EIXO, -12, 12, 3.4)                       # eixo: prego ou palito
    gg = gg - cubo(BAT_X - DOB_X - 1, -16, -1, BAT_X - DOB_X + 4.5, 16, 2.5)   # vão do batente
    for k in range(7):                                           # nervuras que apertam o pano
        gg = gg + cubo(10 + k * 6, -13, -0.8, 11.4 + k * 6, 13, 0.01)
    hx = HX - DOB_X
    gancho = cubo(hx - 2, -3, 53.0 - GZ0, hx + 2, 3, 0.5)
    gancho = gancho - cubo(hx - 2.1, -4, L.ENT_Z0 - GZ0, hx, 4, L.ENT_Z1 - GZ0)
    gancho = gancho - prisma_xz([[hx - 2.1, 52.9 - GZ0], [hx + 0.2, 52.9 - GZ0], [hx - 2.1, 55.2 - GZ0]], -4, 4)
    return gg + gancho


def dobradica():
    """Peça colada na tampa: orelhas da dobradiça + pino do elástico de abertura."""
    z = TZ
    base = cubo(90, 28, z, 128, 48, z + 2) + cubo(112, 20, z, 128, 56, z + 2)
    orelhas = uniao([cubo(114, y0, z, 126, y0 + 3.5, z + 5.5) + cil_y(DOB_X, GZ0 + EIXO, y0, y0 + 3.5, 12) for y0 in (22.0, 50.5)])
    d = base + orelhas
    d = d - cil_y(DOB_X, GZ0 + EIXO, 10, 66, 3.4)
    d = d + cil(96, 38, z + 2, z + 9, 3.2)                       # pino do elástico
    return d


def batente():
    return cubo(BAT_X, 20, TZ, BAT_X + 3, 56, TZ + 3.5)


def canto_tampa():
    """Bloquinho colado por dentro da parede, para o parafuso da tampa."""
    return cubo(0, 0, 0, 6, 12, 10) - cil(3, 6, 2, 11, 1.6)


# ---------------- SVG do MDF ----------------
def svg():
    cut = 'fill="none" stroke="#ff0000" stroke-width="0.1"'
    eng = 'fill="none" stroke="#000000" stroke-width="0.3"'
    txt = 'font-family="Arial" fill="#000000"'
    pecas = []

    def r(x, y, w, h, extra=''):
        return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" {extra}/>'

    # tampa 210 x 76 (vista de cima; y da caixa vira y do desenho)
    t = [r(0, 0, CX, CY, cut),
         r(HX - 2.5, HY - 4, 5, 8, cut),                           # rasgo do gancho
         r(18, 10, 52, 10, cut),                                   # janela dos LEDs
         f'<circle cx="6" cy="38" r="1.25" {cut}/>', f'<circle cx="{CX - 4.5}" cy="38" r="1.25" {cut}/>',
         r(30, 40, 30, 30, eng), f'<text x="45" y="38" font-size="4" text-anchor="middle" {txt}>cole o QR aqui</text>',
         r(90, 28, 38, 20, eng), r(112, 20, 16, 36, eng), f'<text x="109" y="62" font-size="3.5" text-anchor="middle" {txt}>dobradiça</text>',
         r(BAT_X, 20, 3, 36, eng), f'<text x="{BAT_X + 1.5}" y="17" font-size="3.5" text-anchor="middle" {txt}>batente</text>',
         r(128, 16, 42, 44, eng), f'<text x="149" y="66" font-size="3.5" text-anchor="middle" {txt}>EVA (a roupa fica aqui)</text>',
         f'<text x="44" y="27" font-size="4" text-anchor="middle" {txt}>Tag&amp;Go</text>']
    pecas.append(('Tampa', CX, CY, t))
    # fundo 204 x 70 (fica dentro das paredes): rasgo da chave da base
    fx, fy = CX - 2 * MDF, CY - 2 * MDF
    pecas.append(('Fundo', fx, fy, [r(0, 0, fx, fy, cut), r(175 - MDF, 61 - MDF, 20, 5, cut)]))
    pecas.append(('Parede longa 1', CX, CZ, [r(0, 0, CX, CZ, cut)]))
    pecas.append(('Parede longa 2', CX, CZ, [r(0, 0, CX, CZ, cut)]))
    pecas.append(('Parede curta 1', fy, CZ, [r(0, 0, fy, CZ, cut), r(fy / 2 - 6, CZ - 22, 12, 10, cut)]))
    pecas.append(('Parede curta 2', fy, CZ, [r(0, 0, fy, CZ, cut)]))

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
         '<!-- MDF 3 mm. Vermelho = cortar. Preto = gravar (marcas de onde colar). Azul = só legenda, não mandar para o laser. -->\n'
         + '\n'.join(out) + '\n</svg>')
    open(os.path.join(AQUI, 'mdf', 'caixa_mdf.svg'), 'w', encoding='utf-8').write(s)


def caixa_3d():
    paredes = cubo(0, 0, 0, CX, CY, CZ) - cubo(MDF, MDF, MDF, CX - MDF, CY - MDF, CZ + 1)
    paredes = paredes - cubo(175, 61, -1, 195, 66, MDF + 1)
    return paredes


def tampa_3d():
    t = cubo(0, 0, CZ, CX, CY, TZ)
    t = t - cubo(HX - 2.5, HY - 4, CZ - 1, HX + 2.5, HY + 4, TZ + 1) - cubo(18, 10, CZ - 1, 70, 20, TZ + 1)
    return t


def salvar(m, nome, pasta='stl_mdf'):
    k = m.to_mesh()
    t = trimesh.Trimesh(vertices=np.asarray(k.vert_properties)[:, :3], faces=np.asarray(k.tri_verts))
    t.apply_translation(-t.bounds[0])
    os.makedirs(os.path.join(AQUI, pasta), exist_ok=True)
    t.export(os.path.join(AQUI, pasta, nome + '.stl'))
    print(f'{nome:24s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  fechada={t.is_watertight}')


def pack(m):
    k = m.to_mesh()
    v = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)
    return {'v': base64.b64encode(v.tobytes()).decode(),
            'f': base64.b64encode(np.asarray(k.tri_verts).astype(np.uint32).tobytes()).decode()}


if __name__ == '__main__':
    salvar(L.mecanismo_lingueta(), 'M1_trilho_e_servo')
    salvar(L.lingueta(), 'M2_lingueta')
    salvar(L.braco_servo(), 'M3_braco_servo')
    salvar(garra().rotate([90, 0, 0]), 'M4_garra')
    salvar(dobradica(), 'M5_dobradica')
    salvar(batente().rotate([0, 90, 0]), 'M6_batente')
    salvar(uniao([canto_tampa().translate([k * 9, 0, 0]) for k in range(2)]), 'M7_cantos_tampa')
    salvar(g.prateleira_esp32().rotate([180, 0, 0]), 'M8_prateleira_esp32')
    svg()

    zpb = g.FUNDO + 1
    sx0 = L.SX - g.SERVO_EIXO_PONTA
    partes = [
        ('Caixa (MDF)', 'casca', '#c8a77a', caixa_3d(), None),
        ('Tampa (MDF)', 'casca', '#d9bc8c', tampa_3d(), None),
        ('Garra', 'impressa', '#db2777', garra(), 'garra'),
        ('Dobradiça', 'impressa', '#be185d', dobradica(), None),
        ('Batente', 'impressa', '#9d174d', batente(), None),
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
        ('EVA', 'comprada', '#16a34a', cubo(128, 16, TZ, 170, 60, TZ + 0.6), None),
        ('Pano (a roupa)', 'comprada', '#60a5fa', cubo(126, 14, TZ + 0.6, 169, 62, TZ + 1.4) + cubo(126, 61, TZ - 40, 169, 62, TZ + 1.4), None),
        ('Elástico da lingueta', 'comprada', '#111827', cubo(155.5, 44.4, 58.6, 200, 45.6, 59.4), 'elastico'),
    ]
    dados = {'pivo_braco': [L.SX, L.SY, L.Z_BRACO], 'pivo_garra': [DOB_X, HY, GZ0 + EIXO], 'garra_z0': GZ0,
             'pino_rabo': [-12, 0, ESP + 5], 'poste': [96, 38, TZ + 7], 'partes': []}
    for nome, grupo, cor, m, mov in partes:
        d = {'nome': nome, 'grupo': grupo, 'cor': cor, 'mov': mov}
        d.update(pack(m))
        dados['partes'].append(d)
    open(os.path.join(AQUI, 'maquete_mdf.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('ok')
