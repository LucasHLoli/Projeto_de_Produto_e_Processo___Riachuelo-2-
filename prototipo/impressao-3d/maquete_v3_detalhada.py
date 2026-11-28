"""Maquete v3 com as peças compradas detalhadas + checagem de colisão delas."""
import base64, json, os
import numpy as np
import tagandgo_v2 as M
import tagandgo_v3 as C
import comprados_detalhados as K
import ligacoes as L
import chave as CH
from tagandgo_v2 import cubo, cil
from tagandgo_v2 import uniao

AQUI = os.path.dirname(os.path.abspath(__file__))


def pack(m):
    k = m.to_mesh()
    v = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)
    return {'v': base64.b64encode(v.tobytes()).decode(), 'f': base64.b64encode(np.asarray(k.tri_verts).astype(np.uint32).tobytes()).decode()}


P = C.P
pb = C.P_pt(M.SX, M.SY, M.Z_BRACO)
pbB = C.P_pt(M.SXB, M.SYB, M.Z_BRACO_B)
pg = C.P_pt(M.A_GX, M.A_EIXO_Y, M.A_GZ0 + M.A_EIXO_DZ)


def loc(m, piv):
    return m.translate([-piv[0], -piv[1], -piv[2]])


def v(a, b):
    return (a ^ b).volume()


servo = [(c, P(m)) for c, m in K.servo_sg90()[:4]]
servoB = [(c, P(M.servo_T(m))) for c, m in K.servo_sg90(M.Z_ORELHA_B)[:4]]
horn = [(c, loc(P(m.translate([M.SX, M.SY, M.Z_BRACO])), pb)) for c, m in K.braco_plastico()]
hornB = [(c, loc(P(M.servo_T(m.translate([M.SX, M.SY, M.Z_BRACO_B]))), pbB)) for c, m in K.braco_plastico()]
TZ_A = TZ_B = C.H + M.CAMADAS_A * M.MDF                      # as duas versões têm a tampa de 3 chapas
comuns_det = [('Base de carga Qi HyperX', K.base_qi()), ('Power bank ELG 149 × 69 × 15', K.power_bank()), ('Receptor Qi', K.receptor_qi()), ('ESP32 no expansor', K.esp32_expansor()),
              ('Cabo USB (power bank → micro-USB do expansor)', L.cabo_usb()), ('Capacitor 1000 µF (V/G do GPIO 12)', L.capacitor())]
so_A = [('Servo SG90', servo), ('Cabo do servo (GPIO 13)', L.servo_cabo()), ('Semáforo LED (em cima da tampa)', L.semaforo(TZ_A)), ('Fios do semáforo (26, 33, 25, GND)', L.semaforo_fios(TZ_A)),
        ('Chave fim de curso', CH.A_estaticas()), ('Fios da chave (OUT 27, GND)', L.chave_a_fios())]
so_B = [('Servo SG90', servoB), ('Cabo do servo (GPIO 13)', L.servo_cabo_B()), ('Semáforo LED (em cima da tampa)', L.semaforo(TZ_B)), ('Fios do semáforo (26, 33, 25, GND)', L.semaforo_fios(TZ_B)),
        ('Etiqueta de loja (casca)', K.etiqueta_loja()), ('Chave fim de curso', CH.A_estaticas()), ('Fios da chave (OUT 27, GND)', L.chave_a_fios())]
FIOS = ('Cabo', 'Fios', 'Capacitor')
LIBERADO = {('Cabo USB (power bank → micro-USB do expansor)', 'prateleira'), ('Cabo USB (power bank → micro-USB do expansor)', 'ESP32 no expansor'),
            ('Cabo do servo (GPIO 13)', 'ESP32 no expansor'), ('Cabo do servo (GPIO 13)', 'Servo SG90'),
            ('Capacitor 1000 µF (V/G do GPIO 12)', 'ESP32 no expansor'), ('Fios do semáforo (26, 33, 25, GND)', 'ESP32 no expansor'),
            ('Fios do semáforo (26, 33, 25, GND)', 'Semáforo LED (em cima da tampa)'), ('Fios da chave (OUT 27, GND)', 'ESP32 no expansor'),
            ('Fios da chave (OUT 27, GND)', 'Chave fim de curso'), ('Fios da chave (OUT 27, GND)', 'tampa B'), ('Cabo do servo (GPIO 13)', 'base servo'), ('Cabo USB (power bank → micro-USB do expansor)', 'Power bank ELG 149 × 69 × 15')}

if __name__ == '__main__':
    erros = []
    cantos = uniao([C.canto_tampa(x, y) for x, y in C.PARAF])
    est_comum = {'caixa': C.caixa(), 'prateleira': C.prateleira(), 'pés': C.pes(), 'cantos': cantos}
    est_comum.update({'batentes PB': C.batentes_pb(), 'suporte expansor': C.suporte_expansor()})
    est_A = dict(est_comum, **{'tampa A': C.a_tampa(), 'base mecanismo': P(M.a_base_mecanismo()), 'dobradiça': P(M.a_dobradica()),
                                 'lingueta travada': P(M.a_lingueta(0)),
                                 'lingueta solta': P(M.a_lingueta(M.ling_off(M.ANG_SOLTA)))})
    est_B = dict(est_comum, **{'prateleira': C.prateleira(True), 'tampa B': C.b_tampa(), 'base servo': P(M.b_base()), 'berço': P(M.b_berco()),
                                 'dobradiça B': P(M.a_dobradica()), 'suporte da chave B': P(M.b_suporte_chave()),
                                 'embreagem': uniao([m for _, m in K.embreagem_partes()[1]])})
    det = {n: uniao([m for _, m in ps]) for n, ps in comuns_det}
    det_A = dict(det, **{n: uniao([m for _, m in ps]) for n, ps in so_A})
    det_B = dict(det, **{n: uniao([m for _, m in ps]) for n, ps in so_B})
    for ver, est, dd in (('A', est_A, det_A), ('B', est_B, det_B)):
        for n, m in dd.items():
            for e, me in est.items():
                if (n, e) in LIBERADO:
                    continue
                x = v(m, me)
                if x > 0.05:
                    erros.append(f'{ver}: {n} x {e} = {x:.1f} mm3')
        ks = list(dd)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                if (ks[i], ks[j]) in LIBERADO or (ks[j], ks[i]) in LIBERADO or (ks[i].startswith(FIOS) and ks[j].startswith(FIOS)):
                    continue
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
    # alavanca: solta com a garra aberta, apertada com a garra fechada (A); apertada com o pino dentro (B)
    al_A_solta, al_A_apert = uniao([m for _, m in CH.A_alavanca(False)]), uniao([m for _, m in CH.A_alavanca(True)])
    if v(P(M.a_garra_ang(0)), al_A_apert) > 0.05:
        erros.append('A: gancho fechado ainda encosta na alavanca apertada')
    if v(P(M.a_garra_ang(0)), al_A_solta) < 0.05:
        erros.append('A: o gancho fechado NÃO alcança a alavanca (a chave não seria apertada)')
    for a in range(3, 61, 6):
        if v(P(M.a_garra_ang(a)), al_A_solta) > 0.05:
            erros.append(f'A: garra {a}° x alavanca solta')
    for nm, al in (('solta', al_A_solta), ('apertada', al_A_apert)):
        for e, me in est_A.items():
            if v(al, me) > 0.05:
                erros.append(f'A: alavanca {nm} x {e}')
    # B: garra com o pino girando; o pino entra na embreagem; ímãs embaixo dela
    pinoB = uniao([m for _, m in K.pino_etiqueta()])
    eixoB = np.array(C.P_pt(0, M.A_EIXO_Y, M.A_GZ0 + M.A_EIXO_DZ))
    for a in range(0, 61, 3):
        g = P(M.b_garra_ang(a))
        pa = pinoB.translate([0, -eixoB[1], -eixoB[2]]).rotate([0, 0, 0])
        e = M.b_garra_ang(a).bounding_box()
        pm = P(uniao([m for m in [M.pino_T(cil(0, 0, -M.PINO_L - 0.8, 3.5, 1.2))]]).translate([0, -M.A_EIXO_Y, -(M.A_GZ0 + M.A_EIXO_DZ)]).rotate([a, 0, 0]).translate([0, M.A_EIXO_Y, M.A_GZ0 + M.A_EIXO_DZ]))
        for n, m in list(est_B.items()) + [('Etiqueta de loja (casca)', det_B['Etiqueta de loja (casca)']), ('Chave fim de curso', det_B['Chave fim de curso'])]:
            if n == 'embreagem':
                continue
            for pn, pp in (('garra', g), ('pino', pm)):
                x = v(pp, m)
                if x > 0.05:
                    erros.append(f'B {pn} {a}° x {n} = {x:.2f}')
    if v(P(M.b_garra_ang(0)), al_A_apert) > 0.05:
        erros.append('B: gancho fechado ainda encosta na alavanca apertada')
    if v(P(M.b_garra_ang(0)), al_A_solta) < 0.05:
        erros.append('B: o gancho fechado NÃO alcança a alavanca')
    ec = C.P_pt(*M.E_ETQ)
    bb = P(M.b_imas(M.ANG_SOLTAR)).bounding_box()
    emb = uniao([m for _, m in K.embreagem_partes()[1]]).bounding_box()
    print(f'B: ímãs a {M.ANG_SOLTAR:.0f}°: centro ({(bb[0] + bb[3]) / 2:.1f}, {(bb[1] + bb[4]) / 2:.1f}), embreagem ({(emb[0] + emb[3]) / 2:.1f}, {(emb[1] + emb[4]) / 2:.1f}); '
          f'topo dos ímãs {bb[5] - C.ZS:.2f}, fundo do berço {P(M.b_berco()).bounding_box()[2] - C.ZS:.2f} (módulo)')
    hornm = uniao([m for _, m in K.braco_plastico()]).translate([M.SX, M.SY, M.Z_BRACO])
    for ver, base, angs in (('A', P(M.a_base_mecanismo()), range(int(M.ANG_TRAVA), int(M.ANG_SOLTA) + 1, 5)), ('B', P(M.b_base()), range(0, int(M.ANG_SOLTAR) - 1, -5))):
        for a in angs:
            hm = hornm if ver == 'A' else hornm.translate([0, 0, M.Z_BRACO_B - M.Z_BRACO])
            h = hm.translate([-M.SX, -M.SY, 0]).rotate([0, 0, a]).translate([M.SX, M.SY, 0])
            h = P(h if ver == 'A' else M.servo_T(h))
            for n, m in (('berço', base), ('servo', (det_A if ver == 'A' else det_B)['Servo SG90'])):
                x = v(h, m)
                if x > 0.05:
                    erros.append(f'{ver}: braço plástico {a}° x {n} = {x:.1f}')
            if ver == 'A':
                x = v(h, P(M.a_lingueta(M.ling_off(a))))
                if x > 0.05:
                    erros.append(f'A: braço plástico {a}° x lingueta = {x:.1f}')
            moveis = [('braço plástico', h)]
            if ver == 'A':
                moveis += [('braço biela', P(M.a_braco(a))), ('lingueta', P(M.a_lingueta(M.ling_off(a))))]
            else:
                moveis += [('braço dos ímãs', P(M.b_braco(a)[0])), ('ímãs', P(M.b_imas(a)))]
            ddm = det_A if ver == 'A' else det_B
            for mn, mm in moveis:
                for n, m in ddm.items():
                    if n == 'Servo SG90' and mn == 'braço plástico':
                        continue
                    x = v(mm, m)
                    if x > 0.05:
                        erros.append(f'{ver}: {mn} {a}° x {n} = {x:.1f}')
    print('Checagem das peças detalhadas:', 'nenhuma colisão' if not erros else '')
    for e in erros:
        print('  -', e)

    def parte(nome, grupo, pecas, mov=None):
        return {'nome': nome, 'grupo': grupo, 'mov': mov, 'cor': pecas[0][0], 'pecas': [dict(cor=c, **pack(m)) for c, m in pecas]}

    comum = [parte('Caixa (MDF)', 'casca', [('#c8a77a', C.caixa())]),
             parte('Pés da prateleira', 'impressa', [('#a16207', C.pes())]), parte('Batentes do power bank (C2)', 'impressa', [('#a16207', C.batentes_pb())]),
             parte('Suporte do expansor (C7)', 'impressa', [('#a16207', C.suporte_expansor())])] + [parte(n, 'comprada', ps) for n, ps in comuns_det] + \
            []
    pa, ea = CH.A_pivo()
    comum_A = comum + [parte('Braço plástico do servo', 'comprada', horn, 'braco')] + [parte(n, 'comprada', ps) for n, ps in so_A] + \
        [parte('Alavanca da chave', 'comprada', [(c, m.translate([-pa[0], -pa[1], -pa[2]])) for c, m in CH.A_alavanca(False)], 'alavanca')]
    ec, copo, carr, esf = K.embreagem_partes()
    pgB = pg
    comum_B = comum + [parte('Braço plástico do servo', 'comprada', hornB, 'braco')] + [parte(n, 'comprada', ps) for n, ps in so_B] + \
        [parte('Embreagem: copo e mola', 'comprada', copo), parte('Embreagem: carretel', 'comprada', carr, 'carretel'),
         parte('Embreagem: esferas', 'comprada', [(c, m.translate([-ec[0], -ec[1], 0])) for c, m in esf], 'esferas')] + \
        [parte('Alavanca da chave', 'comprada', [(c, m.translate([-pa[0], -pa[1], -pa[2]])) for c, m in CH.A_alavanca(False)], 'alavanca')]
    A = comum_A + [parte('Prateleira (MDF)', 'casca', [('#b08d5e', C.prateleira())]), parte('Tampa (3 chapas MDF)', 'casca', [('#d9bc8c', C.a_tampa())]),
                 parte('Garra com dentes', 'impressa', [('#db2777', loc(P(M.a_garra()), pg))], 'garra'),
                 parte('Dobradiça', 'impressa', [('#be185d', P(M.a_dobradica()))]),
                 parte('Base do servo e trilho', 'impressa', [('#ea580c', P(M.a_base_mecanismo()))]),
                 parte('Lingueta', 'impressa', [('#f59e0b', P(M.a_lingueta()))], 'lingueta'),
                 parte('Braço do servo (biela)', 'impressa', [('#0284c7', loc(P(M.a_braco(0)), pb))], 'braco'),
                 ]
    B = comum_B + [parte('Prateleira (MDF, furo do servo)', 'casca', [('#b08d5e', C.prateleira(True))]), parte('Tampa (3 chapas MDF)', 'casca', [('#d9bc8c', C.b_tampa())]),
                 parte('Garra com o pino (B4)', 'impressa', [('#db2777', loc(P(M.b_garra()), pg))], 'garra'),
                 parte('Pino da etiqueta', 'comprada', [(c, loc(m, pg)) for c, m in K.pino_etiqueta()], 'garra'),
                 parte('Tampinha do pino (B7)', 'impressa', [('#be185d', loc(P(M.b_tampinha()), pg))], 'garra'),
                 parte('Dobradiça', 'impressa', [('#be185d', P(M.a_dobradica()))]),
                 parte('Berço da etiqueta (B3)', 'impressa', [('#f59e0b', P(M.b_berco()))]),
                 parte('Torre do servo (B1)', 'impressa', [('#ea580c', P(M.b_base()))]),
                 parte('Suporte da chave (B6)', 'impressa', [('#a16207', P(M.b_suporte_chave()))]),
                 parte('Braço dos ímãs (B2)', 'impressa', [('#0284c7', loc(P(M.b_braco(0)[0]), pbB))], 'braco'),
                 parte('Ímãs 15 × 5 (2)', 'comprada', K.imas_local(pbB), 'braco')]
    furos0 = C.a_furos_global()[0][2][:4]
    dados = {'centro': [C.LX / 2, C.LY / 2, C.H / 2],
             'A': {'pivo_braco': list(pb), 'pivo_garra': list(pg), 'biela': [M.SX, M.R_BIELA, M.PINO_X_TRAVA],
                   'tz': C.H + M.CAMADAS_A * M.MDF, 'gy': C.P_pt(M.A_GX, 0, 0)[1], 'furos': [[x0, x1] for x0, y0, x1, y1 in furos0],
                   'fundo_furo': C.H - 1.5, 'corte': list(C.P_pt(*M.HOOK, 0)[:2]), 'partes': A, 'alavanca': {'pivo': list(pa), 'eixo': ea, 'ang': CH.ANG_A}},
             'B': {'pivo_braco': list(pbB), 'pivo_garra': list(pg), 'emb_centro': list(ec), 'corte': [ec[0], ec[1]], 'tz': C.H + M.CAMADAS_A * M.MDF,
                   'gy': C.P_pt(M.A_GX, 0, 0)[1], 'furos': [], 'pano_x': [C.P_pt(0, M.A_EIXO_Y + 12, 0)[0], C.P_pt(0, M.HOOK[1] + 8, 0)[0]],
                   'partes': B, 'alavanca': {'pivo': list(pa), 'eixo': ea, 'ang': CH.ANG_A}}}
    open(os.path.join(AQUI, 'maquete_v3.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('maquete_v3.js ok', os.path.getsize(os.path.join(AQUI, 'maquete_v3.js')) // 1024, 'KB')
