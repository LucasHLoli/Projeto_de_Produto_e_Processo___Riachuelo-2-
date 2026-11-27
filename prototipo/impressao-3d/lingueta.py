"""Variante da lingueta (sem etiqueta comercial e sem ímãs).

A garra leva um gancho. Ao fechar, o gancho empurra a rampa da lingueta,
que recua e volta com o elástico, entrando no entalhe: travou sem energia.
Para soltar, o servo gira e empurra o ressalto da lingueta para trás;
a mola abre a garra. O servo volta e o elástico devolve a lingueta.

Rodar: python lingueta.py  ->  stl_lingueta/*.stl e maquete_lingueta.js
"""
import base64, json, os
import numpy as np
import trimesh
from manifold3d import Manifold
import gerar_pecas as g
from gerar_pecas import cubo, cil, uniao

AQUI = os.path.dirname(os.path.abspath(__file__))

GZ0 = g.CZ + g.TAMPA + 2          # fundo da garra fechada
HX = g.EMB_X                      # gancho no mesmo lugar do pino
LZ0, LZ1 = 55.3, 57.7             # altura da lingueta
ENT_Z0, ENT_Z1 = 55.0, 58.0       # entalhe do gancho
SX, SY = 170.0, 22.0              # eixo do servo
Z_ORELHA = 29.9
Z_BRACO = Z_ORELHA + g.SERVO_BRACO_Z


def cunha_x(x0, x1, y0, y1, z0, z1, subindo=True):
    """Prisma triangular: rampa no plano xz."""
    pts = [[x0, z0], [x1, z0], [x0, z1]] if subindo else [[x0, z0], [x1, z0], [x1, z1]]
    from manifold3d import CrossSection
    cs = CrossSection([pts])
    m = Manifold.extrude(cs, y1 - y0)            # extrude em z local
    return m.rotate([90, 0, 0]).translate([0, y1, 0])


def garra_gancho():
    """Garra com gancho, em coordenadas de montagem (fechada)."""
    base = g.garra().translate([g.DOBRA_X, g.EMB_Y, GZ0])
    base = base - cil(HX, g.EMB_Y, GZ0 - 1, GZ0 + 8, 13.5)             # tira o rebaixo do pino
    base = base + cil(HX, g.EMB_Y, GZ0, GZ0 + 6, 13)
    gancho = cubo(HX - 2, g.EMB_Y - 3, 53.0, HX + 2, g.EMB_Y + 3, GZ0 + 1)
    gancho = gancho - cubo(HX - 2.1, g.EMB_Y - 4, ENT_Z0, HX, g.EMB_Y + 4, ENT_Z1)   # entalhe (lado -x)
    # rampa na ponta: corta o canto de baixo do lado -x
    rampa = cunha_x(HX - 2.1, HX + 0.2, g.EMB_Y - 4, g.EMB_Y + 4, 52.9, 55.2, subindo=True)
    gancho = gancho - rampa
    return base + gancho


def lingueta():
    corpo = cubo(152, 35, LZ0, HX, 41, LZ1)
    # chanfro no topo da ponta: o gancho desce e empurra a lingueta para trás
    from manifold3d import CrossSection
    cs = CrossSection([[[HX + 0.1, LZ0 + 0.6], [HX + 0.1, LZ1 + 0.1], [HX - 1.8, LZ1 + 0.1]]])
    chanfro = Manifold.extrude(cs, 8).rotate([90, 0, 0]).translate([0, 42, 0])
    corpo = corpo - chanfro
    ressalto = cubo(174, 36, 47.0, 177, 40, LZ0 + 0.01)
    braco_el = cubo(153, 41, LZ0, 158, 47, LZ1)
    pino_el = cil(155.5, 45, LZ1, 60.0, 3)
    return uniao([corpo, ressalto, braco_el, pino_el])


def mecanismo_lingueta():
    placa = cubo(146, 4, g.FUNDO, 206, 53, g.Z_SERVO)
    # berço do servo
    sx0 = SX - g.SERVO_EIXO_PONTA
    sx1 = sx0 + g.SERVO_C
    cx = (sx0 + sx1) / 2
    sy0, sy1 = SY - g.SERVO_L / 2, SY + g.SERVO_L / 2
    bs = cubo(cx - 18, sy0 - 4, g.Z_SERVO, cx + 18, sy1 + 4, Z_ORELHA)
    bs = bs - cubo(sx0 - g.FOLGA, sy0 - g.FOLGA, g.Z_SERVO - 0.5, sx1 + g.FOLGA, sy1 + g.FOLGA, Z_ORELHA + 1)
    for fx in (cx - g.SERVO_FURO_ENTRE / 2, cx + g.SERVO_FURO_ENTRE / 2):
        bs = bs - cil(fx, SY, Z_ORELHA - 8, Z_ORELHA + 1, 1.9)
    bs = bs - cubo(sx1 - 2, SY - 2.5, g.Z_SERVO - 0.5, cx + 19, SY + 2.5, g.Z_SERVO + 6)
    # trilho da lingueta
    pilar = cubo(147, 31, g.Z_SERVO, 154, 45, 53.0)
    chao = cubo(147, 31, 53.0, 181.5, 45, 55.1)
    chao = chao - cubo(168, 35.4, 52, 181.6, 40.6, 56)             # rasgo do ressalto
    paredes = cubo(147, 31, 55.1, 181.5, 34.7, 58.4) + cubo(147, 41.3, 55.1, 181.5, 45, 58.4)
    paredes = paredes - cubo(152.5, 40, 55, 159, 46, 59)             # passagem do braço do elástico
    pilar2 = cubo(176, 41.3, g.Z_SERVO, 181.5, 45, 53.0)
    poste = cil(200, 45, g.Z_SERVO, 60.0, 5) + cubo(196, 42, g.Z_SERVO, 204, 48, 8)
    m = uniao([placa, bs, pilar, chao, paredes, pilar2, poste])
    for (hx, hy) in [(150, 8), (198, 8), (150, 50), (198, 40)]:
        m = m - cil(hx, hy, g.FUNDO - 1, g.Z_SERVO + 0.1, 3.4)
    return m


def braco_servo():
    L = 16.0
    b = cubo(-4, -4, 0, L + 3, 4, 3) + cil(0, 0, 0, 3, 8) + cil(L + 3, 0, 0, 3, 8)
    b = b - cil(0, 0, -1, 4, 2.2)
    b = b - cubo(-3.5, -2.3, -1, L - 7, 2.3, 1.3)
    return b


def tampa_lingueta():
    t = g.tampa()
    t = t + cil(g.EMB_X, g.EMB_Y, 0, g.TAMPA, 6.4)                    # fecha o furo redondo
    t = t - cubo(HX - 3, g.EMB_Y - 4, -1, HX + 3, g.EMB_Y + 4, g.TAMPA + 1)  # rasgo do gancho
    return t


def salvar(m, nome):
    mesh = m.to_mesh()
    t = trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3], faces=np.asarray(mesh.tri_verts))
    t.apply_translation(-t.bounds[0])
    os.makedirs(os.path.join(AQUI, 'stl_lingueta'), exist_ok=True)
    t.export(os.path.join(AQUI, 'stl_lingueta', nome + '.stl'))
    print(f'{nome:26s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  fechada={t.is_watertight}')


def pack(m):
    k = m.to_mesh()
    v = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)
    f = np.asarray(k.tri_verts).astype(np.uint32)
    return {'v': base64.b64encode(v.tobytes()).decode(), 'f': base64.b64encode(f.tobytes()).decode()}


if __name__ == '__main__':
    salvar(mecanismo_lingueta(), 'L1_mecanismo_lingueta')
    salvar(lingueta().rotate([0, 0, 0]), 'L2_lingueta')
    salvar(braco_servo(), 'L3_braco_servo')
    gg = garra_gancho().translate([-g.DOBRA_X, -g.EMB_Y, -GZ0]).rotate([90, 0, 0])
    salvar(gg, 'L4_garra_gancho')
    salvar(tampa_lingueta(), 'L5_tampa_lingueta')

    Z_PB = g.FUNDO + 1
    partes = [
        ('Caixa', 'casca', '#9aa5b1', g.caixa(), None),
        ('Tampa', 'casca', '#cbd5e1', tampa_lingueta().translate([0, 0, g.CZ]), None),
        ('Garra com gancho', 'impressa', '#db2777', garra_gancho().translate([-g.DOBRA_X, -g.EMB_Y, -GZ0]), 'garra'),
        ('Lingueta', 'impressa', '#f59e0b', lingueta(), 'lingueta'),
        ('Trilho e berço do servo', 'impressa', '#ea580c', mecanismo_lingueta(), None),
        ('Braço do servo', 'impressa', '#2563eb', braco_servo(), 'braco'),
        ('Servo SG90', 'comprada', '#1d4ed8', cubo(SX - g.SERVO_EIXO_PONTA, SY - 6.1, g.Z_SERVO, SX - g.SERVO_EIXO_PONTA + 22.7, SY + 6.1, Z_ORELHA + 6)
         + cubo(SX - g.SERVO_EIXO_PONTA - 4.8, SY - 6.1, Z_ORELHA, SX - g.SERVO_EIXO_PONTA + 27.5, SY + 6.1, Z_ORELHA + 2.5)
         + cil(SX, SY, Z_ORELHA + 6, Z_BRACO, 5), None),
        ('Elástico', 'comprada', '#111827', cubo(155.5, 44.4, 58.6, 200, 45.6, 59.4), 'elastico'),
        ('Power bank', 'comprada', '#1f2937', cubo(g.PB_X0, 3.5, Z_PB, g.PB_X0 + 149, 72.5, Z_PB + 15), None),
        ('Pano (a roupa)', 'comprada', '#60a5fa', cubo(120, 10, g.CZ + g.TAMPA, 210, 66, g.CZ + g.TAMPA + 1.2), 'pano'),
    ]
    dados = {'pivo_braco': [SX, SY, Z_BRACO], 'pivo_garra': [g.DOBRA_X, g.EMB_Y, GZ0 + 5], 'garra_z0': GZ0, 'partes': []}
    for nome, grupo, cor, m, mov in partes:
        d = {'nome': nome, 'grupo': grupo, 'cor': cor, 'mov': mov}
        d.update(pack(m))
        dados['partes'].append(d)
    open(os.path.join(AQUI, 'maquete_lingueta.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('maquete ok')
