"""Exporta as peças montadas para a maquete 3D (maquete_dados.js)."""
import base64, json, os
import numpy as np
from manifold3d import Manifold
import gerar_pecas as g

AQUI = os.path.dirname(os.path.abspath(__file__))


def pack(m):
    k = m.to_mesh()
    v = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)   # 0,05 mm
    f = np.asarray(k.tri_verts).astype(np.uint32)
    return {'v': base64.b64encode(v.tobytes()).decode(), 'f': base64.b64encode(f.tobytes()).decode()}


Z_PB = g.FUNDO + 1.0
partes = [
    # nome, grupo, cor, manifold (posição montada), tipo de movimento
    ('Caixa', 'impressa', '#9aa5b1', g.caixa(), None),
    ('Tampa', 'impressa', '#cbd5e1', g.tampa().translate([0, 0, g.CZ]), 'tampa'),
    ('Mecanismo', 'impressa', '#ea580c', g.mecanismo(), None),
    ('Berço da embreagem', 'impressa', '#f59e0b', g.berco_embreagem(), None),
    ('Braço dos ímãs', 'impressa', '#2563eb', g.braco_imas().translate([0, 0, 0]), 'braco'),
    ('Prateleira do ESP32', 'impressa', '#0d9488', g.prateleira_esp32().translate([0, 0, g.FUNDO]), None),
    ('Garra', 'impressa', '#db2777', g.garra(), 'garra'),
    ('Pino da chave', 'impressa', '#be185d', g.pino_chave().translate([g.CHAVE_TAMPA[0], g.CHAVE_TAMPA[1], g.CZ - 1.5]), None),
    # comprados (formas simples)
    ('Receptor Qi', 'comprada', '#475569', g.cubo(45, 15, g.FUNDO, 120, 60, Z_PB), None),
    ('Power bank', 'comprada', '#1f2937', g.cubo(g.PB_X0, 3.5, Z_PB, g.PB_X0 + 149, 72.5, Z_PB + 15), None),
    ('ESP32 + expansor', 'comprada', '#15803d', g.cubo(40, 11, 23.6, 109, 65, 39.6) + g.cubo(48, 24, 39.6, 101, 52, 44), None),
    ('Servo SG90', 'comprada', '#1d4ed8', g.cubo(g.SERVO_X - g.SERVO_EIXO_PONTA, g.SERVO_Y - 6.1, g.Z_SERVO, g.SERVO_X - g.SERVO_EIXO_PONTA + 22.7, g.SERVO_Y + 6.1, g.Z_ORELHA + 6)
     + g.cubo(g.SERVO_X - g.SERVO_EIXO_PONTA - 4.8, g.SERVO_Y - 6.1, g.Z_ORELHA, g.SERVO_X - g.SERVO_EIXO_PONTA + 27.5, g.SERVO_Y + 6.1, g.Z_ORELHA + 2.5)
     + g.cil(g.SERVO_X, g.SERVO_Y, g.Z_ORELHA + 6, g.Z_BRACO, 5), None),
    ('Embreagem (da etiqueta)', 'comprada', '#a1a1aa', g.cil(g.EMB_X, g.EMB_Y, g.Z_EMB_BAIXO, g.Z_EMB_TOPO, g.EMBREAGEM_D), None),
    ('Ímãs N50', 'comprada', '#e5e7eb', g.cil(16, 0, 0, 12, 10), 'braco'),
    ('Pino da etiqueta', 'comprada', '#d4d4d8', g.cil(g.EMB_X, g.EMB_Y, g.Z_EMB_BAIXO + 3, g.CZ + g.TAMPA + 8.2, g.PINO_D) + g.cil(g.EMB_X, g.EMB_Y, g.CZ + g.TAMPA + 6, g.CZ + g.TAMPA + 8.2, g.CABECA_D - 0.4), 'garra_abs'),
    ('Semáforo LED', 'comprada', '#111827', g.cubo(29, 31, g.CZ - 6, 81, 45, g.CZ - 0.2)
     + g.cil(40, 38, g.CZ - 1, g.CZ + 1, 8, 24) + g.cil(55, 38, g.CZ - 1, g.CZ + 1, 8, 24) + g.cil(70, 38, g.CZ - 1, g.CZ + 1, 8, 24), 'leds'),
    ('Chave da garra', 'comprada', '#334155', g.cubo(155.2, 25.5, g.CZ - 9, 168.9, 50.5, g.CZ - 3), None),
    ('Chave da base', 'comprada', '#334155', g.cubo(172, 57, g.FUNDO, 197, 70.7, g.FUNDO + 6), None),
    ('QR code', 'comprada', '#f8fafc', g.cubo(91, 23, g.CZ + g.TAMPA - 0.6, 121, 53, g.CZ + g.TAMPA - 0.1), None),
]
dados = {
    'pivos': {
        'braco': [g.SERVO_X, g.SERVO_Y, g.Z_BRACO],
        'garra': [g.DOBRA_X, g.EMB_Y, g.CZ + g.TAMPA + 7],
        'garra_z0': g.CZ + g.TAMPA + 2,
        'emb': [g.EMB_X, g.EMB_Y],
    },
    'partes': [],
}
for nome, grupo, cor, m, mov in partes:
    d = {'nome': nome, 'grupo': grupo, 'cor': cor, 'mov': mov}
    d.update(pack(m))
    dados['partes'].append(d)
open(os.path.join(AQUI, 'maquete_dados.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
print(os.path.getsize(os.path.join(AQUI, 'maquete_dados.js')) // 1024, 'KB')
