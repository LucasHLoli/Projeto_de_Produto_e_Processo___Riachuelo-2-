"""Maquete v3 com as peças compradas detalhadas + checagem de colisão delas."""
import base64, json, os
import numpy as np
import tagandgo_v2 as M
import tagandgo_v3 as C
import comprados_detalhados as K
from tagandgo_v2 import uniao

AQUI = os.path.dirname(os.path.abspath(__file__))


def pack(m):
    k = m.to_mesh()
    v = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)
    return {'v': base64.b64encode(v.tobytes()).decode(), 'f': base64.b64encode(np.asarray(k.tri_verts).astype(np.uint32).tobytes()).decode()}


P = C.P
pb = C.P_pt(M.SX, M.SY, M.Z_BRACO)
pg = C.P_pt(M.A_GX, M.A_EIXO_Y, M.A_GZ0 + M.A_EIXO_DZ)


def loc(m, piv):
    return m.translate([-piv[0], -piv[1], -piv[2]])


def v(a, b):
    return (a ^ b).volume()


servo = [(c, P(m)) for c, m in K.servo_sg90()]
horn = [(c, loc(P(m.translate([M.SX, M.SY, M.Z_BRACO])), pb)) for c, m in K.braco_plastico()]
comuns_det = [('Power bank ELG 149 × 69 × 15', K.power_bank()), ('Receptor Qi', K.receptor_qi()), ('ESP32 no expansor', K.esp32_expansor()),
              ('Semáforo LED', K.semaforo()), ('Cabo USB', K.cabo_usb()), ('Servo SG90', servo)]

if __name__ == '__main__':
    erros = []
    cantos = uniao([C.canto_tampa(x, y) for x, y in C.PARAF])
    est_comum = {'caixa': C.caixa(), 'prateleira': C.prateleira(), 'pés': C.pes(), 'cantos': cantos}
    est_A = dict(est_comum, **{'tampa A': C.a_tampa(), 'base mecanismo': P(M.a_base_mecanismo()), 'dobradiça': P(M.a_dobradica()),
                                 'pino da chave': P(M.a_pino_chave()), 'lingueta travada': P(M.a_lingueta(0)),
                                 'lingueta solta': P(M.a_lingueta(M.ling_off(M.ANG_SOLTA)))})
    est_B = dict(est_comum, **{'tampa B': C.b_tampa(), 'base servo': P(M.b_base()), 'cápsula': P(M.b_capsula() + M.b_anel())})
    det = {n: uniao([m for _, m in ps]) for n, ps in comuns_det}
    det_A = dict(det, **{'Chave fim de curso': uniao([m for _, m in K.chave_a()])})
    for ver, est, dd in (('A', est_A, det_A), ('B', est_B, det)):
        for n, m in dd.items():
            for e, me in est.items():
                if n == 'Cabo USB' and e == 'prateleira':
                    continue                                  # o cabo passa pelo furo; o modelo é aproximado
                x = v(m, me)
                if x > 0.05:
                    erros.append(f'{ver}: {n} x {e} = {x:.1f} mm3')
        ks = list(dd)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                x = v(dd[ks[i]], dd[ks[j]])
                if x > 0.05:
                    erros.append(f'{ver}: {ks[i]} x {ks[j]} = {x:.1f} mm3')
        # garra girando x peças detalhadas
        if ver == 'A':
            for a in range(0, 61, 6):
                g = P(M.a_garra_ang(a))
                for n, m in dd.items():
                    x = v(g, m)
                    if x > 0.05:
                        erros.append(f'A garra {a}° x {n} = {x:.1f}')
    hornm = uniao([m for _, m in K.braco_plastico()]).translate([M.SX, M.SY, M.Z_BRACO])
    for ver, base, angs in (('A', P(M.a_base_mecanismo()), range(int(M.ANG_TRAVA), int(M.ANG_SOLTA) + 1, 5)), ('B', P(M.b_base()), range(0, 121, 5))):
        for a in angs:
            h = P(hornm.translate([-M.SX, -M.SY, 0]).rotate([0, 0, a]).translate([M.SX, M.SY, 0]))
            for n, m in (('berço', base), ('servo', det['Servo SG90'])):
                x = v(h, m)
                if x > 0.05:
                    erros.append(f'{ver}: braço plástico {a}° x {n} = {x:.1f}')
            if ver == 'A':
                x = v(h, P(M.a_lingueta(M.ling_off(a))))
                if x > 0.05:
                    erros.append(f'A: braço plástico {a}° x lingueta = {x:.1f}')
    print('Checagem das peças detalhadas:', 'nenhuma colisão' if not erros else '')
    for e in erros:
        print('  -', e)

    def parte(nome, grupo, pecas, mov=None):
        return {'nome': nome, 'grupo': grupo, 'mov': mov, 'cor': pecas[0][0], 'pecas': [dict(cor=c, **pack(m)) for c, m in pecas]}

    comum = [parte('Caixa (MDF)', 'casca', [('#c8a77a', C.caixa())]), parte('Prateleira (MDF)', 'casca', [('#b08d5e', C.prateleira())]),
             parte('Pés da prateleira', 'impressa', [('#a16207', C.pes())])] + [parte(n, 'comprada', ps) for n, ps in comuns_det] + \
            [parte('Braço plástico do servo', 'comprada', horn, 'braco')]
    A = comum + [parte('Tampa (3 chapas MDF)', 'casca', [('#d9bc8c', C.a_tampa())]),
                 parte('Garra com dentes', 'impressa', [('#db2777', loc(P(M.a_garra()), pg))], 'garra'),
                 parte('Dobradiça', 'impressa', [('#be185d', P(M.a_dobradica()))]),
                 parte('Base do servo e trilho', 'impressa', [('#ea580c', P(M.a_base_mecanismo()))]),
                 parte('Lingueta', 'impressa', [('#f59e0b', P(M.a_lingueta()))], 'lingueta'),
                 parte('Braço do servo (biela)', 'impressa', [('#0284c7', loc(P(M.a_braco(0)), pb))], 'braco'),
                 parte('Pino da chave', 'impressa', [('#9d174d', P(M.a_pino_chave()))], 'pino_chave'),
                 parte('Chave fim de curso', 'comprada', K.chave_a())]
    B = comum + [parte('Tampa (MDF)', 'casca', [('#d9bc8c', C.b_tampa())]),
                 parte('Base do servo', 'impressa', [('#ea580c', P(M.b_base()))]),
                 parte('Braço dos ímãs', 'impressa', [('#0284c7', loc(P(M.b_braco(0)[0]), pb))], 'braco'),
                 parte('Ímãs 15 × 5 (2)', 'comprada', K.imas_local(pb), 'braco'),
                 parte('Cápsula da embreagem', 'impressa', [('#f59e0b', P(M.b_capsula() + M.b_anel()))]),
                 parte('Embreagem da etiqueta', 'comprada', K.embreagem_pino()),
                 parte('Pino da etiqueta', 'comprada', K.pino_etiqueta(), 'pino')]
    furos0 = C.a_furos_global()[0][2][:4]
    dados = {'centro': [C.LX / 2, C.LY / 2, C.H / 2],
             'A': {'pivo_braco': list(pb), 'pivo_garra': list(pg), 'biela': [M.SX, M.R_BIELA, M.PINO_X_TRAVA],
                   'tz': C.H + M.CAMADAS_A * M.MDF, 'gy': C.P_pt(M.A_GX, 0, 0)[1], 'furos': [[x0, x1] for x0, y0, x1, y1 in furos0],
                   'fundo_furo': C.H - 1.5, 'partes': A},
             'B': {'pivo_braco': list(pb), 'partes': B}}
    open(os.path.join(AQUI, 'maquete_v3.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('maquete_v3.js ok', os.path.getsize(os.path.join(AQUI, 'maquete_v3.js')) // 1024, 'KB')
