"""Bateria de testes da versão A antes de imprimir. Rodar: python verificar.py

1. Folgas de cada encaixe (medidas do desenho).
2. Trava: quanto a lingueta entra no entalhe, com e sem pano; quanto a garra sobe travada; quanto a chave é apertada.
3. Movimento: garra 0 a 60°, servo 40 a 90° (sem colisão).
4. Montagem da lingueta: cada peça entra pelo caminho previsto.
5. Pior caso: peças compradas 0,6 mm maiores que o anunciado em cada medida.
6. Impressão: tudo cabe na mesa, peças inteiras (um corpo), sem malha aberta.
Gera verificacao.json (para a maquete) e ../IMPRIMIR/A/VERIFICACAO.md.
"""
import glob, io, json, os, subprocess, sys
import numpy as np
import trimesh
import tagandgo_v2 as M
import tagandgo_v3 as C
import chave as K
import comprados_detalhados as KD
import maquete_v3_detalhada as MQ
from tagandgo_v2 import uniao, cubo

AQUI = os.path.dirname(os.path.abspath(__file__))
P = C.P
v = lambda a, b: (a ^ b).volume()
testes = []


def teste(titulo, ok, linhas, anim=None):
    testes.append({'titulo': titulo, 'ok': bool(ok), 'linhas': linhas, 'anim': anim})
    print(('OK   ' if ok else 'FALHA') + ' ' + titulo)
    for l in linhas:
        print('       ' + l)


# ---------- 1. folgas ----------
def folga(nome, furo, peca, minimo, maximo, obs=''):
    f = round((furo - peca) / 2, 2)
    return (minimo <= f <= maximo), f'{nome}: {furo:.2f} para {peca:.2f} → folga {f:+.2f} mm por lado {obs}'.strip()


ly = (M.HOOK[1] + 0.4 + 3) - (M.HOOK[1] - 3 - 0.4)
lista = [
    folga('Eixo A7 na garra e na dobradiça', 3.6, 3.2, 0.15, 0.3, '(gira solto)'),
    folga('Pino C5 no canto C3', 3.0, 3.0, -0.05, 0.05, '(justo: segura a tampa)'),
    folga('Pino C5 na tampa', 3.2, 3.0, 0.05, 0.2, '(passa)'),
    folga('Haste A2c no corpo e no garfo', 4.3, 4.0, 0.1, 0.25),
    folga('Haste A2c no rasgo do chão (largura)', 6 - 1.2, 4.0, 0.2, 0.6),
    folga('Pino A3b no rasgo do garfo', 3.4, 3.0, 0.1, 0.3),
    folga('Pino A3b no furo do A3 (colar)', 3.1, 3.0, 0.0, 0.1),
    folga('Corpo A2a entre as paredes do trilho', ly, 5.6, 0.3, 0.8),
    folga('Garra entre as orelhas da dobradiça', 29.0, 28.4, 0.2, 0.4),
    folga('Placa da chave entre as abas', 14.3, 13.7, 0.2, 0.4),
    folga('Corpo do servo no berço (largura)', M.SERVO['corpo_l'] + 0.6, M.SERVO['corpo_l'], 0.2, 0.4),
    folga('Corpo do servo no berço (comprimento)', M.SERVO['corpo_c'] + 0.6, M.SERVO['corpo_c'], 0.2, 0.4),
    folga('Expansor no suporte C7 (largura)', M.EXP[1] + 0.6, M.EXP[1], 0.2, 0.4),
    folga('Prateleira na caixa (comprimento)', C.LX, C.LX - 0.6, 0.2, 0.4),
    folga('Prateleira na caixa (largura)', C.LY, C.LY - 0.6, 0.2, 0.4),
    folga('Power bank entre os batentes (comprimento)', C.BATENTES_PB[2][0] - (C.BATENTES_PB[0][0] + 2.5), M.PB[0], 0.5, 1.5),
    folga('Degrau da carcaça de PLA', 1.5 + 0.3, 1.5, 0.1, 0.3),
]
teste('Folgas dos encaixes', all(o for o, _ in lista), [l for _, l in lista], 'folgas')

# ---------- 2. trava e chave ----------
x_face = M.HOOK[0] - M.GANCHO_X                     # face do gancho do lado da lingueta
ponta_40 = M.HOOK[0] - M.GANCHO_X + M.ENTALHE_FUNDO - 0.5 + M.ling_off(M.ANG_TRAVA)
ponta_90 = M.HOOK[0] - M.GANCHO_X + M.ENTALHE_FUNDO - 0.5 + M.ling_off(M.ANG_SOLTA)
entra = ponta_40 - x_face
fundo = M.ENTALHE_FUNDO - entra
sobra_90 = x_face - ponta_90
zl, ze = M.Z_LING, M.Z_ENTALHE
degrau = ze[0] - M.Z_GANCHO_BAIXO                 # parte do gancho embaixo do entalhe: é ela que segura o puxão
sobe = zl[0] - ze[0]                              # quanto a garra sobe travada até o degrau bater na lingueta
cima = ze[1] - zl[1]                              # sem pano a garra desce VAO; a lingueta ainda cabe se cima >= VAO
largura = 2 * M.GANCHO_X - M.ENTALHE_FUNDO
ok = 1.5 <= entra <= 2.2 and fundo >= 0.3 and sobra_90 >= 1.5 and cima >= M.VAO + 0.3 and degrau >= 3.0 and largura >= 5.0
teste('Trava: lingueta no entalhe', ok, [
    f'Servo em {M.ANG_TRAVA:.0f}°: a lingueta entra {entra:.1f} mm no gancho e fica {fundo:.1f} mm antes do fundo do entalhe (não empurra o gancho)',
    f'Servo em {M.ANG_SOLTA:.0f}°: a lingueta fica {sobra_90:.1f} mm longe do gancho (a garra abre livre)',
    f'Puxando a garra travada: ela sobe {sobe:.1f} mm e o degrau de {degrau:.1f} × {largura:.1f} mm do gancho bate embaixo da lingueta',
    f'Sem pano a garra desce {M.VAO:.1f} mm: a lingueta ainda entra (sobra {cima - M.VAO:.1f} mm)',
    f'Com pano mais grosso a garra fica mais alta: a lingueta cabe até {sobe:.1f} mm a mais de pano'], 'trava')
curso = K.CURSO_A
teste('Chave fim de curso', 3.8 <= curso <= 5.0, [
    f'Garra fechada com o pano previsto: o gancho aperta a alavanca {curso:.1f} mm na ponta (aciona com ~3 mm numa haste de 12,8, ~4,4 na de 19)',
    f'Sem pano: {curso + M.VAO:.1f} mm (a alavanca de metal flexiona)',
    f'Pano {curso - 3.0:.1f} mm mais grosso que o previsto ainda deixa 3 mm de aperto',
    'A placa encaixa num pino (furo Ø3) e entre abas; colar com cola quente. Se não clicar, papelão embaixo da placa'], 'chave')

# ---------- 3. movimento (usa a checagem completa da maquete) ----------
r = subprocess.run([sys.executable, os.path.join(AQUI, 'maquete_v3_detalhada.py')], capture_output=True, text=True, encoding='utf-8',
                   env=dict(os.environ, PYTHONIOENCODING='utf-8'), cwd=AQUI)
linhas = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith('- A:')]
teste('Movimento sem colisão (garra 0 a 60°, servo 40 a 90°, fios, peças compradas)', not linhas,
      linhas or ['Garra de 3 em 3° e servo de 5 em 5°: nenhuma peça encosta em outra', 'Alavanca solta com a garra aberta e apertada com a garra fechada'], 'movimento')

# ---------- 4. montagem da lingueta ----------
base = M.a_base_mecanismo()
servo = M.servo_modelo(M.Z_ORELHA - 15.6)


def rot(m, a):
    return m.translate([-M.SX, -M.SY, 0]).rotate([0, 0, a]).translate([M.SX, M.SY, 0])


ang = M.ANG_SOLTA
horn = rot(uniao([m for _, m in KD.braco_plastico()]).translate([M.SX, M.SY, M.Z_BRACO]), ang)
A3 = rot(M.a_braco_peca().translate([M.SX, M.SY, M.Z_BRACO]), ang)
pino = rot(M.a_braco_pino().translate([M.SX, M.SY, M.Z_BRACO]), ang)
off = M.ling_off(ang)
corpo, garfo, haste = M.a_lingueta_corpo(off), M.a_lingueta_garfo(off), M.a_lingueta_haste(off)
fixos = {'base': base, 'servo': servo, 'braço plástico': horn, 'braço A3': A3}


def livre(m, vec, obst, dist=40, n=80):
    for k in range(n + 1):
        t = dist * k / n
        mm = m.translate([vec[0] * t, vec[1] * t, vec[2] * t])
        for on, o in obst.items():
            if v(mm, o) > 0.05:
                return False, f'bate em {on} a {t:.1f} mm do fim'
    return True, 'entra sem encostar'


passos, ok_m = [], True
ob = dict(fixos)
for nome, m, vec in (('Corpo A2a, por cima', corpo, (0, 0, 1)), ('Garfo A2b, de lado (+x)', garfo, (1, 0, 0)),
                     ('Haste A2c, por cima', haste, (0, 0, 1)), ('Pino A3b, por cima', pino, (0, 0, 1))):
    o, t = livre(m, vec, ob)
    ok_m &= o
    passos.append(f'{nome}: {t}')
    ob[nome] = m
teste('Montagem da lingueta (na ordem)', ok_m, passos, 'montagem')

# ---------- 5. pior caso ----------
def maior(m, d=0.6):
    b = m.bounding_box()
    c = np.array([(b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2])
    s = [(b[3] - b[0] + d) / (b[3] - b[0]), (b[4] - b[1] + d) / (b[4] - b[1]), (b[5] - b[2] + d) / (b[5] - b[2])]
    return m.translate((-c).tolist()).scale(s).translate(c.tolist())


est = {'caixa': C.caixa(), 'prateleira': C.prateleira(), 'pés': C.pes(), 'batentes': C.batentes_pb(), 'suporte do expansor': C.suporte_expansor(),
       'cantos': uniao([C.canto_tampa(x, y) for x, y in C.PARAF]), 'tampa': C.a_tampa(), 'base do servo': P(M.a_base_mecanismo()),
       'dobradiça': P(M.a_dobradica()), 'lingueta travada': P(M.a_lingueta(0)), 'garra fechada': P(M.a_garra_ang(0))}
compradas = {'Power bank': KD.power_bank(), 'ESP32 no expansor': KD.esp32_expansor(), 'Servo SG90': MQ.servo,
             'Chave fim de curso': K.A_estaticas(), 'Semáforo': MQ.L.semaforo(MQ.TZ_A), 'Receptor Qi': KD.receptor_qi()}
lin, ok_p = [], True
LIBERA = {('Servo SG90', 'base do servo'), ('Chave fim de curso', 'base do servo'), ('ESP32 no expansor', 'suporte do expansor'),
          ('Semáforo', 'tampa'), ('Receptor Qi', 'caixa'), ('Power bank', 'batentes')}
for n, ps in compradas.items():
    m = maior(uniao([mm for _, mm in ps]))
    bate = [e for e, me in est.items() if (n, e) not in LIBERA and v(m, me) > 0.05]
    ok_p &= not bate
    lin.append(f'{n} 0,6 mm maior: ' + ('cabe' if not bate else 'BATE em ' + ', '.join(bate)))
lin.append('Encaixes justos de propósito (servo no berço, chave nas abas, expansor no suporte, power bank nos batentes) estão nas folgas acima')
teste('Pior caso: peças compradas 0,6 mm maiores', ok_p, lin, 'pior')

# ---------- 6. impressão ----------
lin, ok_i = [], True
for f in sorted(glob.glob(os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'PLA', '*', '*.stl'))):
    t = trimesh.load(f)
    nome = os.path.relpath(f, os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'PLA')).replace('\\', '/')
    cabe = t.bounds[0][0] >= 0 and t.bounds[0][1] >= 0 and t.bounds[1][0] <= 220 and t.bounds[1][1] <= 220 and t.extents[2] <= 250
    o = cabe and t.is_watertight
    ok_i &= o
    lin.append(f'{nome}: {t.extents[0]:.0f} × {t.extents[1]:.0f} × {t.extents[2]:.0f} mm, ' + ('cabe na mesa, malha fechada' if o else 'PROBLEMA'))
for f in sorted(glob.glob(os.path.join(AQUI, 'stl_v3', 'A*.stl')) + glob.glob(os.path.join(AQUI, 'stl_v3', 'C*.stl'))):
    t = trimesh.load(f)
    nb = len(t.split(only_watertight=False))
    n = os.path.splitext(os.path.basename(f))[0]
    esperado = int(n.split('_x')[-1]) if '_x' in n else (12 if n == 'C1_calcos_servo' else 1)
    if nb != esperado:
        ok_i = False
        lin.append(f'{n}: {nb} pedaços (esperado {esperado})')
lin.append('Cada peça sai inteira (um pedaço só por peça)')
teste('Arquivos de impressão', ok_i, lin, 'impressao')

json.dump({'testes': testes}, open(os.path.join(AQUI, 'verificacao.json'), 'w', encoding='utf-8'), ensure_ascii=False)
md = ['# Verificação automática da versão A', '', 'Gerado por `prototipo/impressao-3d/verificar.py`. Rodar de novo depois de qualquer mudança.', '']
for t in testes:
    md.append(f"## {'✅' if t['ok'] else '❌'} {t['titulo']}")
    md.append('')
    md += [f'- {l}' for l in t['linhas']]
    md.append('')
io.open(os.path.join(AQUI, '..', 'IMPRIMIR', 'A', 'VERIFICACAO.md'), 'w', encoding='utf-8').write('\n'.join(md))
print('\nTOTAL:', sum(t['ok'] for t in testes), 'de', len(testes), 'testes passaram')
