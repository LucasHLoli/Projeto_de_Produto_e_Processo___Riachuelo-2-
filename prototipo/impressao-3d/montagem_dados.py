"""Peças soltas da carcaça (MDF e PLA) e dos pinos/eixo, na posição montada, para a animação de montagem.

Rodar: python montagem_dados.py  (gera montagem.js)
"""
import base64, json, os
import numpy as np
import tagandgo_v2 as M
import tagandgo_v3 as C
import carcaca_pla as CP
from tagandgo_v2 import cubo, cil, cil_x, uniao

AQUI = os.path.dirname(os.path.abspath(__file__))
T = M.MDF


def pack(m):
    k = m.to_mesh()
    v = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)
    return {'v': base64.b64encode(v.tobytes()).decode(), 'f': base64.b64encode(np.asarray(k.tri_verts).astype(np.uint32).tobytes()).decode()}


def parte(nome, cor, m, casca=False):
    return {'nome': nome, 'cor': cor, 'casca': casca, **pack(m)}


def main():
    LX, LY, H = C.LX, C.LY, C.H
    mdf, madeira = [], '#c8a77a'
    mdf.append(parte('Fundo (MDF)', madeira, cubo(0.3, 0.3, -T, LX - 0.3, LY - 0.3, 0), True))
    mdf.append(parte('Parede longa 1 (MDF)', madeira, cubo(-T, -T, -T, LX + T, 0, H), True))
    mdf.append(parte('Parede longa 2 (MDF)', madeira, cubo(-T, LY, -T, LX + T, LY + T, H), True))
    mdf.append(parte('Parede curta 1 (MDF)', madeira, C.caixa() ^ cubo(-T - 1, 0, -T - 1, 0, LY, H + 1), True))
    mdf.append(parte('Parede curta 2 (MDF)', madeira, cubo(LX, 0, -T, LX + T, LY, H), True))
    mdf.append(parte('Cantos da tampa (C3)', '#a16207', uniao([C.canto_tampa(x, y) for x, y in C.PARAF])))
    mdf.append(parte('Prateleira (MDF)', '#b08d5e', C.prateleira(), True))
    tampa = C.a_tampa()
    for k, nome in ((0, 'Tampa: chapa 3 (de baixo)'), (1, 'Tampa: chapa 2 (meio)'), (2, 'Tampa: chapa 1 (de cima)')):
        mdf.append(parte(nome, '#d9bc8c', tampa ^ cubo(-50, -50, H + k * T, LX + 50, LY + 50, H + (k + 1) * T), True))

    pla, branco = [], '#e7e5e4'
    caixa = CP.caixa_pla()
    ce, cd = CP.metades(caixa, None, None, por_fora=True)
    tp = C.a_tampa()
    te, td = CP.metades(tp, H, H + M.CAMADAS_A * T, por_fora=False, esq_baixo=False)
    pe_, pd = CP.metades(C.prateleira(), C.Z_PRAT, C.ZS, por_fora=False)
    pla += [parte('Cantos da tampa (C3)', '#a16207', uniao([C.canto_tampa(x, y) for x, y in C.PARAF])), parte('Caixa PLA, metade esquerda (mesa 4)', branco, ce, True), parte('Caixa PLA, metade direita (mesa 5)', '#d6d3d1', cd, True),
            parte('Prateleira PLA, metade esquerda (mesa 6)', '#a8a29e', pe_, True), parte('Prateleira PLA, metade direita (mesa 7)', '#78716c', pd, True),
            parte('Tampa PLA, metade esquerda (mesa 6)', branco, te, True), parte('Tampa PLA, metade direita (mesa 7)', '#d6d3d1', td, True)]

    TZ = H + M.CAMADAS_A * T
    pinos_t = uniao([cil(x, y, TZ, TZ + 1.5, 6.0) + cil(x, y, TZ - 3 * T - 8, TZ, 3.0) for x, y in C.PARAF])
    ez = M.A_GZ0 + M.A_EIXO_DZ
    eixo = C.P(cil_x(M.A_EIXO_Y, ez, M.A_GX - 22, M.A_GX + 22, 3.2) + cil_x(M.A_EIXO_Y, ez, M.A_GX - 24, M.A_GX - 22, 6.0))
    extras = [parte('Pinos da tampa (C5)', '#a16207', pinos_t), parte('Eixo da garra (A7)', '#be185d', eixo)]
    # teste de montagem da lingueta: peças soltas com o servo em 90° e o caminho de cada uma (no referencial da caixa)
    ang = M.ANG_SOLTA
    rot = lambda m: m.translate([-M.SX, -M.SY, 0]).rotate([0, 0, ang]).translate([M.SX, M.SY, 0])
    off = M.ling_off(ang)
    teste = [dict(parte('Teste: braço A3 (sem o pino)', '#0284c7', C.P(rot(M.a_braco_peca().translate([M.SX, M.SY, M.Z_BRACO])))), vec=None),
             dict(parte('Teste: corpo A2a', '#f59e0b', C.P(M.a_lingueta_corpo(off))), vec=[0, 0, 40]),
             dict(parte('Teste: garfo A2b', '#facc15', C.P(M.a_lingueta_garfo(off))), vec=[0, -40, 0]),
             dict(parte('Teste: haste A2c', '#ea580c', C.P(M.a_lingueta_haste(off))), vec=[0, 0, 40]),
             dict(parte('Teste: pino A3b', '#0ea5e9', C.P(rot(M.a_braco_pino().translate([M.SX, M.SY, M.Z_BRACO])))), vec=[0, 0, 40])]
    js = 'window.MONTAGEM=' + json.dumps({'mdf': mdf, 'pla': pla, 'extras': extras, 'teste': teste}) + ';'
    js += chr(10) + 'window.VERIF=' + open(os.path.join(AQUI, 'verificacao.json'), encoding='utf-8').read() + ';'
    open(os.path.join(AQUI, 'montagem.js'), 'w', encoding='utf-8').write(js)
    print('montagem.js', os.path.getsize(os.path.join(AQUI, 'montagem.js')) // 1024, 'KB')


if __name__ == '__main__':
    main()
