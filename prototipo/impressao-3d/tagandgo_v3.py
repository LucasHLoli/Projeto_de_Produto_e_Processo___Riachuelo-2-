"""Tag&Go protótipo v3 (compacto): power bank no fundo, prateleira de MDF por cima,
mecanismo e ESP32 lado a lado na prateleira. Mesmas duas versões da v2 (A garra com
dentes, B etiqueta de loja + ímãs). O mecanismo é o da v2, girado 90° e levantado
até a prateleira, então as folgas internas dele continuam as mesmas.

Rodar: python tagandgo_v3.py
"""
import base64, json, os
import numpy as np
import trimesh
import tagandgo_v2 as M
from tagandgo_v2 import cubo, cil, uniao, MDF, FOLGA

AQUI = os.path.dirname(os.path.abspath(__file__))

# ======================= caixa compacta =======================
LX, LY = 194.0, 86.0                        # interno
QI_E, PB_C, PB_L, PB_A = 1.0, 149.0, 69.0, 15.0
POS_PB = (40.0, 15.0, 40.0 + PB_C + 1, 15.0 + PB_L + 1)   # USB para x=40 (vão do plugue); micro-USB para y=15 (faixa de 14 mm)
Z_PRAT = POS_PB and (QI_E + PB_A + 1.0)     # base da prateleira = 17
ZS = Z_PRAT + MDF                           # topo da prateleira = 20
H = ZS + M.H                                # face de baixo da tampa = 68,5
# módulo da v2 -> caixa: gira -90° em z e sobe até a prateleira
DX, DY = -9.0, 194.0
POS_ESP = (120.0, 16.0, 120.0 + M.EXP[0] + 1, 16.0 + M.EXP[1] + 1)
POS_SEM = (18.0, 60.0)                      # semáforo embaixo da tampa (canto)
QR = (122.0, 54.0, 30.0)                    # QR na tampa (x, y, lado)
PARAF = [(4.0, 70.0), (LX - 4.0, 70.0)]
PES = [(2, 2), (2, 72), (100, 1), (180, 1)]  # pés da prateleira (12 x 12), fora do power bank e do plugue
FURO_CABO = (6.0, 24.0, 34.0, 58.0)          # furo na prateleira para o cabo USB subir


def P(m):
    return m.rotate([0, 0, -90]).translate([DX, DY, ZS])


def P_pt(x, y, z):
    return (y + DX, -x + DY, z + ZS)


# ======================= peças =======================
def caixa():
    return cubo(-MDF, -MDF, -MDF, LX + MDF, LY + MDF, H) - cubo(0, 0, 0, LX, LY, H + 1)


def prateleira():
    p = cubo(0, 0, Z_PRAT, LX, LY, ZS)
    return p - cubo(FURO_CABO[0], FURO_CABO[1], Z_PRAT - 1, FURO_CABO[2], FURO_CABO[3], ZS + 1)


def pes():
    return uniao([cubo(x, y, 0, x + 12, y + 12, Z_PRAT) for x, y in PES])


def pe_unico():
    return cubo(0, 0, 0, 12, 12, Z_PRAT)


def janela_leds(z0, z1):
    return cubo(POS_SEM[0] + 5, POS_SEM[1] + 5, z0, POS_SEM[0] + M.SEMAFORO[0] - 5, POS_SEM[1] + M.SEMAFORO[1] - 5, z1)


def furos_tampa(z0, z1):
    return uniao([cil(x, y, z0, z1, 3.2) for x, y in PARAF])


def a_furos_global():
    """Furos de cada chapa já na caixa: lista por chapa de retângulos (x0, y0, x1, y1)."""
    out = []
    for z0, z1, linha in M.a_furos_por_camada():
        rs = []
        for i, (y0, y1) in enumerate(linha):
            w = M.DENTE_C / 2 + 1.5 if i < len(M.DENTES_U) else 2.6
            xa, ya, _ = P_pt(M.A_GX - w, y0, 0)
            xb, yb, _ = P_pt(M.A_GX + w, y1, 0)
            rs.append((min(xa, xb), min(ya, yb), max(xa, xb), max(ya, yb)))
        px, py, _ = P_pt(*M.PLUNGER, 0)
        out.append((z0 + ZS, z1 + ZS, rs, (px, py)))
    return out


def a_tampa():
    t = uniao([cubo(-MDF, -MDF, H + k * MDF, LX + MDF, LY + MDF, H + (k + 1) * MDF) for k in range(M.CAMADAS_A)])
    for z0, z1, rs, (px, py) in a_furos_global():
        for x0, y0, x1, y1 in rs:
            t = t - cubo(x0, y0, z0 - 0.01, x1, y1, z1 + 0.01)
        t = t - cil(px, py, z0 - 0.01, z1 + 0.01, 4.6)
    return t - janela_leds(H - 1, H + 20) - furos_tampa(H - 1, H + 20)


def b_tampa():
    cx, cy, _ = P_pt(*M.CAPS, 0)
    t = cubo(-MDF, -MDF, H, LX + MDF, LY + MDF, H + MDF)
    return t - cil(cx, cy, H - 1, H + MDF + 1, M.CAP_D + 0.4) - janela_leds(H - 1, H + 20) - furos_tampa(H - 1, H + 20)


def canto_tampa(x, y):
    return cubo(x - 4, y - 6, H - 10, x + 4, y + 6, H) - cil(x, y, H - 9, H + 1, 2.2)


def comprados():
    pb, e = POS_PB, POS_ESP
    return [
        ('Power bank 149 × 69 × 15', 'comprada', '#1f2937', cubo(pb[0] + .5, pb[1] + .5, QI_E, pb[2] - .5, pb[3] - .5, QI_E + PB_A)),
        ('Receptor Qi', 'comprada', '#475569', cubo(78, 27, 0, 78 + 75, 27 + 45, QI_E)),
        ('Plugue USB (espaço)', 'comprada', '#64748b', cubo(8, 44, 3, 40, 56, 13)),
        ('Expansor + ESP32', 'comprada', '#15803d', cubo(e[0] + .5, e[1] + .5, ZS, e[2] - .5, e[3] - .5, ZS + 11) + cubo(e[0] + 9, e[1] + 12, ZS + 11, e[0] + 61, e[1] + 41, ZS + 17)),
        ('Fios do ESP32 (espaço)', 'comprada', '#86efac', cubo(e[0] + 2, e[1] + 2, ZS + 11, e[0] + 66, e[1] + 10, ZS + 38) + cubo(e[0] + 2, e[3] - 10, ZS + 11, e[0] + 66, e[3] - 2, ZS + 38)),
        ('Semáforo LED', 'comprada', '#111827', cubo(POS_SEM[0], POS_SEM[1], H - M.SEMAFORO[2], POS_SEM[0] + M.SEMAFORO[0], POS_SEM[1] + M.SEMAFORO[1], H - 0.2)),
    ]


def checar():
    erros = []

    def v(a, b):
        return (a ^ b).volume()
    comuns = {'caixa': caixa(), 'prateleira': prateleira(), 'pés': pes()}
    for n, _g, _c, m in comprados():
        comuns[n] = m
    # comprados x estrutura
    nomes = list(comuns)
    for i in range(len(nomes)):
        for j in range(i + 1, len(nomes)):
            if v(comuns[nomes[i]], comuns[nomes[j]]) > 0.05:
                erros.append(f'parado: {nomes[i]} x {nomes[j]}')
    # ---- A
    fa = dict(comuns)
    fa.update({'tampa A': a_tampa(), 'dobradiça': P(M.a_dobradica()), 'base mecanismo': P(M.a_base_mecanismo()),
               'cantos': uniao([canto_tampa(x, y) for x, y in PARAF])})
    servo = P(M.servo_modelo(M.Z_ORELHA - 15.6))
    for n, m in fa.items():
        if n != 'base mecanismo' and v(servo, m) > 0.05:
            erros.append(f'A servo x {n}')
    ks = list(fa)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            if ks[i] in comuns and ks[j] in comuns:
                continue
            if v(fa[ks[i]], fa[ks[j]]) > 0.05:
                erros.append(f'A parado: {ks[i]} x {ks[j]}')
    for ang in range(0, 61, 3):
        g = P(M.a_garra_ang(ang))
        for n in ('tampa A', 'dobradiça', 'base mecanismo', 'Semáforo LED', 'caixa'):
            if v(g, fa[n]) > 0.05:
                erros.append(f'A garra {ang}° x {n}')
    for ang in range(int(M.ANG_TRAVA), int(M.ANG_SOLTA) + 1, 5):
        li, br = P(M.a_lingueta(M.ling_off(ang))), P(M.a_braco(ang))
        for n, m in fa.items():
            if n == 'base mecanismo':
                continue
            for pn, p in (('lingueta', li), ('braço', br)):
                if v(p, m) > 0.05:
                    erros.append(f'A servo {ang}°: {pn} x {n}')
    # ---- B
    fb = dict(comuns)
    fb.update({'tampa B': b_tampa(), 'base servo': P(M.b_base()), 'cápsula': P(M.b_capsula() + M.b_anel()),
               'cantos': uniao([canto_tampa(x, y) for x, y in PARAF])})
    for ang in range(0, 121, 5):
        br, _ = M.b_braco(ang)
        for pn, p in (('braço', P(br)), ('ímãs', P(M.b_imas(ang)))):
            for n, m in fb.items():
                if v(p, m) > 0.05:
                    erros.append(f'B servo {ang}°: {pn} x {n}')
    return erros


def svgs():
    cut = 'fill="none" stroke="#ff0000" stroke-width="0.1"'
    eng = 'fill="none" stroke="#000000" stroke-width="0.3"'
    txt = 'font-family="Arial" fill="#000000"'
    o = MDF
    EX, EY = LX + 2 * MDF, LY + 2 * MDF

    def r(x, y, w, h, s, oo=o):
        return f'<rect x="{x + oo:.2f}" y="{y + oo:.2f}" width="{w:.2f}" height="{h:.2f}" {s}/>'

    def c(x, y, d, s):
        return f'<circle cx="{x + o:.2f}" cy="{y + o:.2f}" r="{d / 2:.2f}" {s}/>'
    base = [r(-o, -o, EX, EY, cut)] + [c(x, y, 3.2, cut) for x, y in PARAF] + \
        [r(POS_SEM[0] + 5, POS_SEM[1] + 5, M.SEMAFORO[0] - 10, M.SEMAFORO[1] - 10, cut)]
    qr = [r(QR[0], QR[1], QR[2], QR[2], eng), f'<text x="{QR[0] + QR[2] / 2 + o}" y="{QR[1] - 2 + o}" font-size="4" text-anchor="middle" {txt}>QR aqui</text>']
    paredes = [('Prateleira (fica sobre os pés)', LX, LY, [r(0, 0, LX, LY, cut, 0), r(FURO_CABO[0], FURO_CABO[1], FURO_CABO[2] - FURO_CABO[0], FURO_CABO[3] - FURO_CABO[1], cut, 0)]),
               ('Fundo', LX, LY, [r(0, 0, LX, LY, cut, 0)]),
               ('Parede longa 1', EX, H + MDF, [r(0, 0, EX, H + MDF, cut, 0)]),
               ('Parede longa 2', EX, H + MDF, [r(0, 0, EX, H + MDF, cut, 0)]),
               ('Parede curta 1', LY, H + MDF, [r(0, 0, LY, H + MDF, cut, 0)]),
               ('Parede curta 2', LY, H + MDF, [r(0, 0, LY, H + MDF, cut, 0)])]

    def escreve(nome, tampas):
        W = 430
        x, y, lin, out = 5, 5, 0, []
        for n, w, h, els in tampas + paredes:
            if x + w > W:
                x, y, lin = 5, y + lin + 12, 0
            out.append(f'<g transform="translate({x},{y})"><title>{n}</title>{"".join(els)}'
                       f'<text x="{w / 2}" y="{h + 6}" font-size="4" text-anchor="middle" fill="#0000ff">{n}</text></g>')
            x += w + 8
            lin = max(lin, h)
        Ht = y + lin + 12
        s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{Ht}mm" viewBox="0 0 {W} {Ht}">\n'
             '<!-- MDF 3 mm. Vermelho = cortar. Preto = gravar. Azul = legenda (apagar antes do laser). '
             'O fundo e a prateleira ficam DENTRO das paredes; as paredes curtas ficam entre as longas. -->\n' + '\n'.join(out) + '\n</svg>')
        open(os.path.join(AQUI, 'mdf', nome), 'w', encoding='utf-8').write(s)
    tA = []
    for k, (z0, z1, rs, (px, py)) in enumerate(a_furos_global()):
        els = base + [r(x0, y0, x1 - x0, y1 - y0, cut) for x0, y0, x1, y1 in rs] + [c(px, py, 4.6, cut)]
        if k == 0:
            hx, hy, _ = P_pt(M.A_GX, M.A_EIXO_Y, 0)
            els += qr + [r(hx - 7, hy - 18.5, 14, 37, eng), f'<text x="{hx + o}" y="{hy - 20 + o}" font-size="3.5" text-anchor="middle" {txt}>dobradiça</text>']
        tA.append((['Tampa 1 (de cima)', 'Tampa 2 (meio)', 'Tampa 3 (de baixo)'][k], EX, EY, els))
    escreve('caixa_v3_A.svg', tA)
    cx, cy, _ = P_pt(*M.CAPS, 0)
    escreve('caixa_v3_B.svg', [('Tampa', EX, EY, base + qr + [c(cx, cy, M.CAP_D + 0.4, cut)])])


def salvar(m, nome):
    k = m.to_mesh()
    t = trimesh.Trimesh(vertices=np.asarray(k.vert_properties)[:, :3], faces=np.asarray(k.tri_verts))
    t.merge_vertices()
    t.apply_translation(-t.bounds[0])
    os.makedirs(os.path.join(AQUI, 'stl_v3'), exist_ok=True)
    t.export(os.path.join(AQUI, 'stl_v3', nome + '.stl'))
    assert max(t.extents[:2]) <= 220 and t.extents[2] <= 250, nome
    print(f'  {nome:28s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  {"ok" if t.is_watertight else "MALHA ABERTA"}')


if __name__ == '__main__':
    print(f'Caixa interna {LX:.0f} x {LY:.0f} x {H:.1f}; externa {LX + 2 * MDF:.0f} x {LY + 2 * MDF:.0f} x {H + MDF:.1f} (+ tampa A {M.CAMADAS_A * MDF:.0f} / B {MDF:.0f})')
    print(f'Prateleira de MDF a {Z_PRAT:.0f}-{ZS:.0f} mm, sobre 4 pés; power bank embaixo')
    erros = checar()
    print('Checagem de colisões:', 'nenhuma' if not erros else '')
    for e in erros:
        print('  -', e)
    import shutil
    os.makedirs(os.path.join(AQUI, 'stl_v3'), exist_ok=True)
    # peças do mecanismo: iguais às da v2
    for n in ['A1_base_servo_e_trilho', 'A2a_lingueta_corpo', 'A2b_lingueta_garfo', 'A3_braco_biela', 'A4_garra_dentes',
              'A5_dobradica', 'A6_pino_da_chave', 'B1_base_servo', 'B2_braco_imas', 'B3_capsula_embreagem', 'B4_anel_capsula',
              'B5_teste_embreagem', 'C1_calcos_servo', 'C2_batentes_x6']:
        shutil.copy(os.path.join(AQUI, 'stl_v2', n + '.stl'), os.path.join(AQUI, 'stl_v3', n + '.stl'))
    salvar(uniao([pe_unico().translate([k * 15, 0, 0]) for k in range(4)]), 'C4_pes_prateleira_x4')
    salvar(uniao([canto_tampa(4, 70).translate([-4 + k * 10, -64, -(H - 10)]) for k in range(2)]), 'C3_cantos_tampa_x2')
    svgs()

    def pack(m):
        k = m.to_mesh()
        vv = np.round(np.asarray(k.vert_properties)[:, :3] * 20).astype(np.int16)
        return {'v': base64.b64encode(vv.tobytes()).decode(), 'f': base64.b64encode(np.asarray(k.tri_verts).astype(np.uint32).tobytes()).decode()}

    def loc(m, piv):
        return m.translate([-piv[0], -piv[1], -piv[2]])
    comuns = [('Caixa (MDF)', 'casca', '#c8a77a', caixa(), None), ('Prateleira (MDF)', 'casca', '#b08d5e', prateleira(), None),
              ('Pés da prateleira', 'impressa', '#a16207', pes(), None)] + [(n, g, c, m, None) for n, g, c, m in comprados()] + \
             [('Servo SG90', 'comprada', '#1d4ed8', P(M.servo_modelo(M.Z_ORELHA - 15.6)), None)]
    pb = P_pt(M.SX, M.SY, M.Z_BRACO)
    pg = P_pt(M.A_GX, M.A_EIXO_Y, M.A_GZ0 + M.A_EIXO_DZ)
    A = comuns + [('Tampa (3 chapas MDF)', 'casca', '#d9bc8c', a_tampa(), None),
                  ('Garra com dentes', 'impressa', '#db2777', loc(P(M.a_garra()), pg), 'garra'),
                  ('Dobradiça', 'impressa', '#be185d', P(M.a_dobradica()), None),
                  ('Base do servo e trilho', 'impressa', '#ea580c', P(M.a_base_mecanismo()), None),
                  ('Lingueta', 'impressa', '#f59e0b', P(M.a_lingueta()), 'lingueta'),
                  ('Braço do servo (biela)', 'impressa', '#2563eb', loc(P(M.a_braco(0)), pb), 'braco'),
                  ('Pino da chave', 'impressa', '#9d174d', P(M.a_pino_chave()), 'pino_chave'),
                  ('Chave fim de curso', 'comprada', '#334155', P(cubo(M.PLUNGER[0] - 4, M.PLUNGER[1] - 12, M.H - 9, M.PLUNGER[0] + 9.7, M.PLUNGER[1] + 13, M.H - 3.2)), None)]
    B = comuns + [('Tampa (MDF)', 'casca', '#d9bc8c', b_tampa(), None),
                  ('Base do servo', 'impressa', '#ea580c', P(M.b_base()), None),
                  ('Braço dos ímãs', 'impressa', '#2563eb', loc(P(M.b_braco(0)[0]), pb), 'braco'),
                  ('Ímãs 15 × 5 (2)', 'comprada', '#d4d4d8', loc(P(M.b_imas(0)), pb), 'braco'),
                  ('Cápsula da embreagem', 'impressa', '#f59e0b', P(M.b_capsula() + M.b_anel()), None),
                  ('Embreagem da etiqueta', 'comprada', '#71717a', P(cil(M.CAPS[0], M.CAPS[1], M.H, M.H + M.EMB[1], M.EMB[0])), None),
                  ('Pino da etiqueta', 'comprada', '#e4e4e7', P(cil(M.CAPS[0], M.CAPS[1], M.H + 2, M.H + M.EMB[1] + 18, M.PINO_ETQ) + cil(M.CAPS[0], M.CAPS[1], M.H + M.EMB[1] + 17, M.H + M.EMB[1] + 19, 12)), 'pino')]
    furos0 = a_furos_global()[0][2][:4]
    gy = P_pt(M.A_GX, 0, 0)[1]
    dados = {'centro': [LX / 2, LY / 2, H / 2],
             'A': {'pivo_braco': list(pb), 'pivo_garra': list(pg), 'biela': [M.SX, M.R_BIELA, M.PINO_X_TRAVA],
                   'tz': H + M.CAMADAS_A * MDF, 'gy': gy, 'furos': [[x0, x1] for x0, y0, x1, y1 in furos0], 'fundo_furo': H - 1.5,
                   'partes': [dict(nome=n, grupo=g, cor=c, mov=mv, **pack(m)) for n, g, c, m, mv in A]},
             'B': {'pivo_braco': list(pb), 'partes': [dict(nome=n, grupo=g, cor=c, mov=mv, **pack(m)) for n, g, c, m, mv in B]}}
    open(os.path.join(AQUI, 'maquete_v3.js'), 'w', encoding='utf-8').write('window.MAQ=' + json.dumps(dados) + ';')
    print('maquete_v3.js ok')
