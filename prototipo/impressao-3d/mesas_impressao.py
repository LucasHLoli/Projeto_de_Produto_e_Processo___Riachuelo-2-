"""Gera a pasta ../IMPRIMIR/A: mesas prontas para a Ender (220 x 220) e os SVGs do laser só com o corte.

Rodar depois de tagandgo_v2.py e tagandgo_v3.py: python mesas_impressao.py
"""
import glob, io, os, re
import trimesh

AQUI = os.path.dirname(os.path.abspath(__file__))
IMP = os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'PLA')
LASER = os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'MDF_laser')
SRC = os.path.join(AQUI, 'stl_v3')
MESAS = {
    'mesa0_teste_de_folga': ['T1_teste_de_folga'],
    'mesa1_pecas_pequenas': ['A2a_lingueta_corpo', 'A2b_lingueta_garfo', 'A2c_lingueta_haste', 'A3_braco_biela', 'A3b_pino_braco',
                             'A5_dobradica', 'A7_eixo_garra', 'C3_cantos_tampa_x2'],
    'mesa2_garra_e_base_do_servo': ['A4_garra_dentes', 'A1_base_servo_e_trilho'],
    'mesa3_pes_batentes_e_suporte_do_esp32': ['C7_suporte_expansor', 'C4_pes_prateleira_x4', 'C2_batentes_x5', 'C5_pinos_tampa_x2'],
    'extra_calcos_do_servo_so_se_precisar': ['C1_calcos_servo'],
    # reposição: as peças que fazem força ou são finas (quebram primeiro). Imprimir com 100% de preenchimento.
    'mesa8_reposicao_pecas_frageis': ['A7_eixo_garra', 'A7_eixo_garra', 'C5_pinos_tampa_x2', 'A3_braco_biela', 'A3b_pino_braco', 'A3b_pino_braco',
                                      'A2a_lingueta_corpo', 'A2b_lingueta_garfo', 'A2c_lingueta_haste', 'A5_dobradica'],
}


LOTES = {
    'mesa0_teste_de_folga': ('Lote1_teste_10min', 'Imprimir primeiro (10 min). Conferir: o pino de 3,2 gira solto no furo DEITADO de 3,6 (eixo da garra); '
                             'o pino de 3,0 entra justo no furo de 3,0 (pinos da tampa). Se não encaixar, NÃO imprimir o resto: avisar.'),
    'mesa1_pecas_pequenas': ('Lote2_pecas_pequenas', 'Conferir: a haste quadrada (4 x 4) passa no furo do corpo da lingueta; o eixo passa nos furos da dobradiça e gira.'),
    'mesa2_garra_e_base_do_servo': ('Lote3_garra_e_base_do_servo', 'ANTES: medir o servo (topo do braço plástico até a orelha; o desenho reserva 19 mm). '
                                    'Ligar suporte "tocando a mesa". Conferir: o servo entra no berço; a placa da chave entra entre as abas da coluna.'),
    'mesa3_pes_batentes_e_suporte_do_esp32': ('Lote4_pes_batentes_suporte_pinos', 'Conferir: o expansor do ESP32 assenta no suporte; os 4 pés têm a mesma altura (17 mm).'),
    'mesa8_reposicao_pecas_frageis': ('Lote6_reposicao_100porcento', 'Peças de reserva. Imprimir com 100% de preenchimento. Guardar num saquinho.'),
    'extra_calcos_do_servo_so_se_precisar': ('Extra_calcos_so_se_precisar', 'Só se o servo medir menos de 19 mm do topo do braço plástico até a orelha.'),
}


def mesa(nome, pecas):
    ms = sorted([trimesh.load(os.path.join(SRC, p + '.stl')) for p in pecas], key=lambda m: -m.extents[1])
    x = y = linha = 0.0
    out = []
    for m in ms:
        m = m.copy()
        m.apply_translation(-m.bounds[0])
        if x + m.extents[0] > 200:
            x, y, linha = 0.0, y + linha + 8, 0.0
        m.apply_translation([x, y, 0])
        out.append(m)
        x += m.extents[0] + 8
        linha = max(linha, m.extents[1])
    t = trimesh.util.concatenate(out)
    t.apply_translation([110 - (t.bounds[0][0] + t.bounds[1][0]) / 2, 110 - (t.bounds[0][1] + t.bounds[1][1]) / 2, 0])
    assert t.bounds[0][0] >= 5 and t.bounds[0][1] >= 5 and t.bounds[1][0] <= 215 and t.bounds[1][1] <= 215, nome
    pasta, nota = LOTES[nome]
    d = os.path.join(IMP, pasta)
    os.makedirs(d, exist_ok=True)
    t.export(os.path.join(d, nome + '.stl'))
    io.open(os.path.join(d, 'O_QUE_CONFERIR.txt'), 'w', encoding='utf-8').write(nota + chr(10))
    print(f'  {nome:42s} {t.extents[0]:6.1f} x {t.extents[1]:5.1f} x {t.extents[2]:5.1f} mm  {t.volume / 1000:5.1f} cm3')


def laser():
    s = io.open(os.path.join(AQUI, 'mdf', 'caixa_v3_A.svg'), encoding='utf-8').read()
    gs = re.findall(r'<g transform="translate\(([\d.]+),([\d.]+)\)"><title>([^<]*)</title>(.*?)</g>', s, re.S)

    def tam(n):
        if n.startswith('Tampa'):
            return 230, 92
        if n.startswith('Prateleira') or n == 'Fundo':
            return 224, 86
        return (230, 71.5) if n.startswith('Parede longa') else (86, 71.5)
    grupos = {'laser1_tampas_3_chapas': lambda n: n.startswith('Tampa'),
              'laser2_prateleira_e_fundo': lambda n: n.startswith('Prateleira') or n == 'Fundo',
              'laser3_paredes': lambda n: n.startswith('Parede')}
    for arq, f in grupos.items():
        els, y, W = [], 5.0, 0
        for _, _, n, corpo in gs:
            if not f(n):
                continue
            corpo = re.sub(r'<text[^>]*>.*?</text>', '', corpo, flags=re.S)                 # sem textos
            corpo = re.sub(r'<(rect|circle)[^>]*stroke="#000000"[^>]*/>', '', corpo)         # sem gravação: só o corte
            w, h = tam(n)
            els.append(f'<g transform="translate(5,{y})"><title>{n}</title>{corpo}</g>')
            y += h + 6
            W = max(W, w + 10)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{y}mm" viewBox="0 0 {W} {y}">\n'
               '<!-- MDF 3 mm. Só linhas de corte. -->\n' + '\n'.join(els) + '\n</svg>')
        io.open(os.path.join(LASER, arq.replace('laser', '', 1) + '.svg'), 'w', encoding='utf-8').write(svg)
        print(f'  {arq:42s} {W:.0f} x {y:.0f} mm, {len(els)} peças, {svg.count("<rect") + svg.count("<circle")} cortes')


if __name__ == '__main__':
    os.makedirs(IMP, exist_ok=True)
    os.makedirs(LASER, exist_ok=True)
    import shutil
    for f in glob.glob(os.path.join(IMP, '*.stl')) + glob.glob(os.path.join(LASER, '*.svg')):
        os.remove(f)
    for d in glob.glob(os.path.join(IMP, 'Lote*')) + glob.glob(os.path.join(IMP, 'Extra*')):
        if 'carcaca' not in d:
            shutil.rmtree(d)
    for n, p in MESAS.items():
        mesa(n, p)
    laser()
