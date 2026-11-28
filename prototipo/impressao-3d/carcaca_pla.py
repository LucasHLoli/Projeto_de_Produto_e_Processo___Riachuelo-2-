"""Carcaça da versão A em PLA (alternativa ao MDF), com as mesmas medidas internas.

A caixa tem 230 mm e a mesa da Ender tem 220, então caixa, tampa e prateleira saem em 2 metades,
cortadas em x = CORTE (depois do fim da garra). As metades encaixam com um degrau de 10 mm e são coladas.
Os cantos que seguram os pinos da tampa (C3) já vêm na caixa.

Rodar: python carcaca_pla.py  (gera ../IMPRIMIR/A/carcaca_PLA/)
"""
import os
import numpy as np
import trimesh
import tagandgo_v2 as M
import tagandgo_v3 as C
from tagandgo_v2 import cubo, uniao

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'PLA', 'carcaca_PLA')
T = C.MDF                      # parede de 3 mm: mesma medida externa da caixa de MDF
CORTE = 120.0                  # x do corte (a garra termina em x ~ 115)
DEG = 10.0                     # comprimento do degrau de encaixe
FOLGA = 0.15
GRANDE = 1000.0


def caixa_pla():
    c = C.caixa() + uniao([C.canto_tampa(x, y) for x, y in C.PARAF])
    return c


def metades(m, z0, z1, por_fora=True, esq_baixo=True):
    """Corta m em x = CORTE com degrau: a metade esquerda fica com a parte de dentro (ou de baixo) do degrau,
    a direita com a de fora (ou de cima). Para a caixa o degrau é na parede (meia espessura);
    para chapas (tampa e prateleira) é na altura (meia espessura)."""
    esq_inteira = cubo(-GRANDE, -GRANDE, -GRANDE, CORTE - DEG / 2, GRANDE, GRANDE)
    dir_inteira = cubo(CORTE + DEG / 2, -GRANDE, -GRANDE, GRANDE, GRANDE, GRANDE)
    zona = cubo(CORTE - DEG / 2, -GRANDE, -GRANDE, CORTE + DEG / 2, GRANDE, GRANDE)
    if por_fora:
        # parede: a esquerda fica com a metade de dentro, a direita com a de fora (e com todo o fundo no degrau)
        esq = (m ^ esq_inteira) + (m ^ zona ^ cubo(-T / 2 + FOLGA, -T / 2 + FOLGA, 0.0, C.LX + T / 2 - FOLGA, C.LY + T / 2 - FOLGA, GRANDE))
        dir_ = (m ^ dir_inteira) + ((m ^ zona) - cubo(-T / 2, -T / 2, 0.0, C.LX + T / 2, C.LY + T / 2, GRANDE))
    else:
        zm = (z0 + z1) / 2
        baixo = cubo(-GRANDE, -GRANDE, z0 - 1, GRANDE, GRANDE, zm - FOLGA / 2)
        cima = cubo(-GRANDE, -GRANDE, zm + FOLGA / 2, GRANDE, GRANDE, z1 + 1)
        esq = (m ^ esq_inteira) + (m ^ zona ^ (baixo if esq_baixo else cima))
        dir_ = (m ^ dir_inteira) + (m ^ zona ^ (cima if esq_baixo else baixo))
    return esq, dir_


def salvar_mesa(nome, pecas):
    """pecas: lista de (manifold, rotação). Arruma lado a lado (em y) e centraliza na mesa 220 x 220."""
    ms = []
    for p in pecas:
        k = p.to_mesh()
        t = trimesh.Trimesh(vertices=np.asarray(k.vert_properties)[:, :3], faces=np.asarray(k.tri_verts))
        t.merge_vertices()
        t.apply_translation(-t.bounds[0])
        ms.append(t)
    y = 0.0
    for t in ms:
        t.apply_translation([0, y, 0])
        y += t.extents[1] + 8
    t = trimesh.util.concatenate(ms)
    t.apply_translation([110 - (t.bounds[0][0] + t.bounds[1][0]) / 2, 110 - (t.bounds[0][1] + t.bounds[1][1]) / 2, 0])
    assert t.bounds[0][0] >= 3 and t.bounds[0][1] >= 3 and t.bounds[1][0] <= 217 and t.bounds[1][1] <= 217, (nome, t.extents)
    os.makedirs(SAIDA, exist_ok=True)
    t.export(os.path.join(SAIDA, nome + '.stl'))
    n, a = t.face_normals, t.area_faces
    cz = t.triangles_center[:, 2]
    print(f'  {nome:38s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  {t.volume / 1000:5.1f} cm3  '
          f'pendurado {a[(n[:, 2] < -0.71) & (cz > t.bounds[0][2] + 0.2)].sum():5.0f} mm2  {"ok" if t.is_watertight else "MALHA ABERTA"}')


if __name__ == '__main__':
    caixa = caixa_pla()
    ce, cd = metades(caixa, None, None, por_fora=True)
    tampa = C.a_tampa()
    # rebaixo de 0,6 mm onde a dobradiça (A5) encaixa e cola: marca o lugar certo, como a gravação do MDF
    tampa = tampa - C.P(cubo(M.A_GX - 18.7, M.A_EIXO_Y - 8.2, M.A_TZ - 0.6, M.A_GX + 18.7, M.A_EIXO_Y + 6.2, M.A_TZ + 1))
    zt0, zt1 = C.H, C.H + M.CAMADAS_A * M.MDF
    te, td = metades(tampa, zt0, zt1, por_fora=False, esq_baixo=False)
    prat = C.prateleira()
    pe_, pd = metades(prat, C.Z_PRAT, C.ZS, por_fora=False)
    # conferência: as metades juntas = a peça inteira, sem sobrepor
    for n, a, b, inteira in (('caixa', ce, cd, caixa), ('tampa', te, td, tampa), ('prateleira', pe_, pd, prat)):
        sobra = (a ^ b).volume()
        falta = inteira.volume() - a.volume() - b.volume()
        print(f'{n}: metades se sobrepõem {sobra:.2f} mm3; folga do encaixe {falta:.0f} mm3')
    print('Mesas:')
    salvar_mesa('mesa4_caixa_esquerda', [ce])
    salvar_mesa('mesa5_caixa_direita', [cd])
    # cada metade fica com o degrau encostado na mesa: sem suporte
    salvar_mesa('mesa6_tampa_e_prateleira_esquerda', [te.rotate([180, 0, 0]), pe_])
    salvar_mesa('mesa7_tampa_e_prateleira_direita', [td, pd.rotate([180, 0, 0])])
