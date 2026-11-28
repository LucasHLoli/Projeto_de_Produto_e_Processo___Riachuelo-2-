"""Dados da aba "Arquivos para imprimir" da maquete: cada mesa da Ender (peças na posição de impressão)
e as chapas do laser. Lê os arquivos de ../IMPRIMIR/A, então mostra exatamente o que vai para a impressora.

Rodar depois de gerar as mesas: python impressao_dados.py  (gera impressao.js)
"""
import base64, glob, json, os
import numpy as np
import trimesh

AQUI = os.path.dirname(os.path.abspath(__file__))
IMP = os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'PLA')
PASTA_LASER = os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'MDF_laser')
CORES = ['#db2777', '#ea580c', '#0284c7', '#16a34a', '#7c3aed', '#ca8a04', '#0d9488', '#be185d', '#2563eb', '#65a30d']

MESAS = [
    ('mesa0_teste_de_folga', 'Mesa 0 · teste de folga (10 min, primeiro)', 'Mecanismo (PLA)', 'não', ['T1_teste_de_folga']),
    ('mesa1_pecas_pequenas', 'Mesa 1 · peças pequenas', 'Mecanismo (PLA)', 'não', ['A2a_lingueta_corpo', 'A2b_lingueta_garfo', 'A2c_lingueta_haste', 'A3_braco_biela', 'A3b_pino_braco', 'A5_dobradica', 'A7_eixo_garra', 'C3_cantos_tampa_x2']),
    ('mesa2_garra_e_base_do_servo', 'Mesa 2 · garra e base do servo', 'Mecanismo (PLA)', 'sim, tocando a mesa', ['A4_garra_dentes', 'A1_base_servo_e_trilho']),
    ('mesa3_pes_batentes_e_suporte_do_esp32', 'Mesa 3 · pés, batentes, suporte do ESP32 e pinos da tampa', 'Mecanismo (PLA)', 'não', ['C7_suporte_expansor', 'C4_pes_prateleira_x4', 'C2_batentes_x5', 'C5_pinos_tampa_x2']),
    ('extra_calcos_do_servo_so_se_precisar', 'Extra · calços do servo (só se precisar)', 'Mecanismo (PLA)', 'não', ['C1_calcos_servo']),
    ('mesa8_reposicao_pecas_frageis', 'Mesa 8 · reposição das peças frágeis (100% preenchimento)', 'Reposição (PLA)', 'não', ['A7_eixo_garra', 'C5_pinos_tampa_x2', 'A3_braco_biela', 'A3b_pino_braco', 'A2a_lingueta_corpo', 'A2b_lingueta_garfo', 'A2c_lingueta_haste', 'A5_dobradica']),
    ('carcaca_PLA/mesa4_caixa_esquerda', 'Mesa 4 · caixa, metade esquerda', 'Carcaça (PLA)', 'não', None),
    ('carcaca_PLA/mesa5_caixa_direita', 'Mesa 5 · caixa, metade direita', 'Carcaça (PLA)', 'não', None),
    ('carcaca_PLA/mesa6_tampa_e_prateleira_esquerda', 'Mesa 6 · tampa e prateleira, esquerda', 'Carcaça (PLA)', 'não', None),
    ('carcaca_PLA/mesa7_tampa_e_prateleira_direita', 'Mesa 7 · tampa e prateleira, direita', 'Carcaça (PLA)', 'não', None),
]
NOMES_PECAS = {'A1_base_servo_e_trilho': 'Base do servo e trilho', 'A2a_lingueta_corpo': 'Lingueta (corpo)', 'A2b_lingueta_garfo': 'Lingueta (garfo)',
               'A3_braco_biela': 'Braço do servo', 'A4_garra_dentes': 'Garra com dentes', 'A5_dobradica': 'Dobradiça', 'A7_eixo_garra': 'Eixo da garra',
               'C1_calcos_servo': 'Calços do servo', 'C3_cantos_tampa_x2': 'Cantos da tampa (2)', 'C4_pes_prateleira_x4': 'Pés da prateleira (4)',
               'C5_pinos_tampa_x2': 'Pinos da tampa (2)', 'C6_pinos_semaforo_x2': 'Pinos do semáforo (2)',
               'C2_batentes_x5': 'Batentes do power bank (5)', 'A2c_lingueta_haste': 'Lingueta (haste)', 'A3b_pino_braco': 'Pino do braço', 'C7_suporte_expansor': 'Suporte do expansor do ESP32', 'T1_teste_de_folga': 'Teste de folga'}
NOMES_CARCACA = {'mesa4': ['Caixa, metade esquerda'], 'mesa5': ['Caixa, metade direita'],
                 'mesa6': ['Tampa, metade esquerda (de cabeça para baixo)', 'Prateleira, metade esquerda'],
                 'mesa7': ['Tampa, metade direita', 'Prateleira, metade direita (de cabeça para baixo)']}
LASER = [('laser1_tampas_3_chapas', 'Laser 1 · 3 chapas da tampa'), ('laser2_prateleira_e_fundo', 'Laser 2 · prateleira e fundo'), ('laser3_paredes', 'Laser 3 · 4 paredes')]


def pack(t):
    v = np.round(np.asarray(t.vertices) * 20).astype(np.int16)
    return {'v': base64.b64encode(v.tobytes()).decode(), 'f': base64.b64encode(np.asarray(t.faces).astype(np.uint32).tobytes()).decode()}


def assinatura(t):
    return tuple(np.round(sorted(t.extents), 1))


def main():
    fontes = {}
    for f in glob.glob(os.path.join(AQUI, 'stl_v3', '*.stl')):
        n = os.path.splitext(os.path.basename(f))[0]
        fontes[n] = [assinatura(c) for c in trimesh.load(f).split(only_watertight=False)]
    mesas = []
    for arq, titulo, grupo, suporte, pecas in MESAS:
        t = trimesh.load(os.path.join(IMP, arq + '.stl'))
        comps = t.split(only_watertight=False)
        partes = {}
        for k, c in enumerate(sorted(comps, key=lambda c: (c.bounds[0][1], c.bounds[0][0]))):
            if pecas:
                nome = next((NOMES_PECAS[p] for p in pecas if any(np.allclose(assinatura(c), s, atol=0.3) for s in fontes[p])), 'Peça')
            else:
                chave = os.path.basename(arq).split('_')[0]
                nome = NOMES_CARCACA[chave][min(k, len(NOMES_CARCACA[chave]) - 1)]
            partes.setdefault(nome, []).append(c)
        lista = []
        for i, (nome, cs) in enumerate(partes.items()):
            lista.append({'nome': nome, 'cor': CORES[i % len(CORES)], **pack(trimesh.util.concatenate(cs))})
        mesas.append({'arquivo': arq + '.stl', 'titulo': titulo, 'grupo': grupo, 'suporte': suporte,
                      'tam': [round(x, 1) for x in t.extents], 'vol': round(t.volume / 1000, 1), 'partes': lista})
    laser = []
    for arq, titulo in LASER:
        s = open(os.path.join(PASTA_LASER, arq + '.svg'), encoding='utf-8').read()
        laser.append({'arquivo': arq + '.svg', 'titulo': titulo, 'grupo': 'Carcaça (MDF, laser)', 'svg': s})
    js = 'window.IMPRESSAO=' + json.dumps({'mesas': mesas, 'laser': laser}).replace('</', '<\\/') + ';'
    open(os.path.join(AQUI, 'impressao.js'), 'w', encoding='utf-8').write(js)
    for m in mesas:
        print(f"  {m['arquivo']:52s} {[p['nome'] for p in m['partes']]}")
    print('impressao.js', os.path.getsize(os.path.join(AQUI, 'impressao.js')) // 1024, 'KB')


if __name__ == '__main__':
    main()
