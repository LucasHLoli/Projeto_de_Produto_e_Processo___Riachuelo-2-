# Gera os desenhos do item A da Entrega 3 (conjunto do produto Tag&Go).
# Uso: python gerar_conjunto.py  ->  conjunto_produto.png e conjunto_camadas.png na mesma pasta.
# Medidas em mm. Origem no canto externo inferior da base: x = comprimento, z = largura, y = altura.
# As medidas do mecanismo vêm do modelo digital do protótipo (prototipo/dados.js); as demais são estimativas.
# Para mudar uma medida, altere o dicionário P e rode de novo.
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arc, Polygon

P = dict(
    L=120, W=60, H=30, parede=2, fundo=1.5, tampa=2,
    emb=dict(x=24, z=40, r=6.5, y0=16.8, y1=27.8),          # embreagem de esferas, Ø 13 x 11
    eixo=dict(x=24, z=24), raio=16,                          # eixo do microatuador e raio do braço
    ima=dict(r=5, y0=4, y1=15.8),                            # três ímãs Ø 10 x 4 empilhados, 0,2 de folga
    prat=dict(x0=12, x1=41.5, y0=16, y1=16.8, z0=31, z1=49),  # prateleira do suporte
    atu=dict(x0=19, x1=39, z0=19.75, z1=28.25, y0=5, y1=22),
    braco=dict(y0=2, y1=4, larg=8),
    cel=dict(x0=57, x1=107, z0=13, z1=47, y0=2.5, y1=8.5),   # célula de 50 x 34 x 6
    bob=dict(x=82, z=30, r=20, y0=1.5, y1=2.5),
    pci=dict(x0=60, x1=105, z0=15, z1=45, y0=10, y1=11.6),
    qr=dict(x0=67, x1=97, z0=15, z1=45),                     # código 2D gravado na tampa, 30 x 30
    leds=dict(x=112, zs=[18, 30, 42], r=1.5),
    chg=dict(x0=33, x1=39, z0=41, z1=47, y0=24, y1=28),      # chave da garra
    chb=dict(x0=43, x1=49, z0=4, z1=10, y0=1.5, y1=5.5),     # chave da base
    garra=dict(x0=2, x1=54, z0=24, z1=56, esp=6, folga=1),
    pino=dict(d=1.2, comp=16, cab=12),
)
K = 'black'
COTA = '#1f4e79'
COR = dict(carc='#f2f2f2', emb='#b7bcc4', ima='#c0504d', atu='#fbe5a3', cel='#bcd6ee', bob='#f4b183', pci='#a9d18e', chave='#d9d9d9', sup='#7f7f7f')
LEGENDA = [
    (1, 'TG-111', 'base da carcaça'), (2, 'TG-112', 'tampa'), (3, 'TG-211', 'corpo da garra'),
    (4, 'TG-221', 'pino'), (5, 'TG-222', 'embreagem de esferas'), (6, 'TG-313', 'ímãs (3)'),
    (7, 'TG-312', 'braço dos ímãs'), (8, 'TG-311', 'microatuador rotativo'), (9, 'TG-113', 'suporte do mecanismo'),
    (10, 'TG-411', 'LEDs (3)'), (11, 'TG-511', 'placa de controle'), (12, 'TG-521', 'célula recarregável'),
    (13, 'TG-522', 'bobina de indução'), (14, 'TG-512', 'chave da garra'), (15, 'TG-513', 'chave da base'),
]
FANT = (0, (9, 2, 1.5, 2, 1.5, 2))      # traço e dois pontos (linha fantasma)
EIXO = (0, (10, 2.5, 1.5, 2.5))         # traço e ponto (linha de centro)


def balao(ax, n, alvo, onde):
    ax.plot([alvo[0], onde[0]], [alvo[1], onde[1]], color='#444444', lw=0.6, zorder=6)
    ax.add_patch(Circle(alvo, 0.55, color='#222222', zorder=7))
    ax.add_patch(Circle(onde, 3.3, fc='white', ec=K, lw=0.9, zorder=8))
    ax.text(onde[0], onde[1] - 0.1, str(n), ha='center', va='center', fontsize=7.5, fontweight='bold', zorder=9)


def seta(ax, a, b):
    ax.annotate('', xy=a, xytext=b, arrowprops=dict(arrowstyle='<|-|>', color=COTA, lw=0.7, shrinkA=0, shrinkB=0, mutation_scale=8))


def cota_h(ax, x0, x1, y, texto, de):
    seta(ax, (x0, y), (x1, y))
    ax.text((x0 + x1) / 2, y + 0.8, texto, ha='center', va='bottom', fontsize=7.5, color=COTA)
    for x, y0 in zip((x0, x1), de):
        ax.plot([x, x], [y0, y + 1.2], color=COTA, lw=0.45)


def cota_v(ax, x, y0, y1, texto, de):
    seta(ax, (x, y0), (x, y1))
    ax.text(x - 0.9, (y0 + y1) / 2, texto, ha='right', va='center', fontsize=7.5, color=COTA, rotation=90)
    for y, x0 in zip((y0, y1), de):
        ax.plot([x0, x + (1.2 if x > x0 else -1.2)], [y, y], color=COTA, lw=0.45)


def ret(ax, x0, x1, y0, y1, **k):
    k.setdefault('ec', K); k.setdefault('lw', 0.8)
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, **k))


def hach(ax, x0, x1, y0, y1, h='////', fc='white', **k):
    ret(ax, x0, x1, y0, y1, fc=fc, hatch=h, lw=k.pop('lw', 1.2), **k)


# ---------- vista superior ----------
def vista_superior(ax, oy):
    p = P; T = lambda z: z + oy
    ax.text(-40, T(84), 'Vista superior (tampa tratada como transparente)', fontsize=9, fontweight='bold')
    ax.add_patch(FancyBboxPatch((0, T(0)), p['L'], p['W'], boxstyle='round,pad=0,rounding_size=5', fc=COR['carc'], ec=K, lw=1.5))
    b, c, d = p['bob'], p['cel'], p['pci']
    ret(ax, c['x0'], c['x1'], T(c['z0']), T(c['z1']), fc=COR['cel'])
    ret(ax, d['x0'], d['x1'], T(d['z0']), T(d['z1']), fc=COR['pci'])
    ax.add_patch(Circle((b['x'], T(b['z'])), b['r'], fc='none', ec='#b35410', lw=0.9, ls='--'))
    q = p['qr']                                                   # código 2D gravado na face da tampa
    ret(ax, q['x0'], q['x1'], T(q['z0']), T(q['z1']), fc='none', lw=0.7)
    for qx, qz in ((q['x0'] + 1.5, q['z1'] - 8.5), (q['x1'] - 8.5, q['z1'] - 8.5), (q['x0'] + 1.5, q['z0'] + 1.5)):
        ret(ax, qx, qx + 7, T(qz), T(qz) + 7, fc='none', lw=0.7); ret(ax, qx + 2, qx + 5, T(qz) + 2, T(qz) + 5, fc=K, lw=0)
    ax.text((q['x0'] + q['x1']) / 2, T(q['z0'] + 15),'código 2D gravado\nna face da tampa', ha='center', va='center', fontsize=6.3)
    a = p['atu']; ret(ax, a['x0'], a['x1'], T(a['z0']), T(a['z1']), fc=COR['atu'])
    s = p['prat']; ret(ax, s['x0'], s['x1'], T(s['z0']), T(s['z1']), fc='none', lw=0.6)
    e, m, r = p['eixo'], p['emb'], p['raio']
    ax.plot([e['x'], e['x'] - r], [T(e['z'])] * 2, color=K, lw=3.2, solid_capstyle='round')          # braço em repouso
    ax.add_patch(Circle((e['x'] - r, T(e['z'])), p['ima']['r'], fc=COR['ima'], ec=K, lw=0.9))
    ax.plot([e['x'], m['x']], [T(e['z']), T(m['z'])], color=K, lw=0.9, ls='--')                       # braço na posição de soltar
    ax.add_patch(Circle((m['x'], T(m['z'])), p['ima']['r'], fc='none', ec='#8c1c13', lw=1.0, ls='--'))
    ax.add_patch(Arc((e['x'], T(e['z'])), 2 * r, 2 * r, theta1=90, theta2=180, color='#444444', lw=0.6))
    ax.text(10.5, T(37.5), '90°', fontsize=6.5, color='#444444', ha='center')
    ax.add_patch(Circle((m['x'], T(m['z'])), m['r'], fc=COR['emb'], ec=K, lw=0.9, alpha=0.8))
    ax.add_patch(Circle((m['x'], T(m['z'])), 0.6, fc=K))
    for cx, cz in ((e['x'], e['z']), (m['x'], m['z'])):                                               # linhas de centro
        ax.plot([cx - 9, cx + 9], [T(cz)] * 2, color=K, lw=0.4, ls=EIXO); ax.plot([cx] * 2, [T(cz) - 9, T(cz) + 9], color=K, lw=0.4, ls=EIXO)
    for k_ in ('chg', 'chb'):
        h = p[k_]; ret(ax, h['x0'], h['x1'], T(h['z0']), T(h['z1']), fc=COR['chave'])
    for z, cor in zip(p['leds']['zs'], ['#c00000', '#ffc000', '#548235']):
        ax.add_patch(Circle((p['leds']['x'], T(z)), p['leds']['r'], fc=cor, ec=K, lw=0.7))
    g = p['garra']                                                                                    # garra em linha fantasma
    ax.add_patch(Rectangle((g['x0'], T(g['z0'])), g['x1'] - g['x0'], g['z1'] - g['z0'], fc='none', ec=K, lw=0.9, ls=FANT))
    ax.plot([g['x1']] * 2, [T(g['z0'] - 3), T(g['z1'] + 3)], color=K, lw=0.5, ls=EIXO)
    # plano de corte A-A
    ax.plot([-22, 128], [T(40)] * 2, color=K, lw=0.5, ls=EIXO)
    for x0, x1 in ((-22, -17), (123, 128)):
        ax.plot([x0, x1], [T(40)] * 2, color=K, lw=2.2)
    for xa in (-22, 128):
        ax.annotate('', xy=(xa, T(47)), xytext=(xa, T(40)), arrowprops=dict(arrowstyle='-|>', color=K, lw=1, mutation_scale=9))
        ax.text(xa, T(48.5), 'A', ha='center', fontsize=8.5, fontweight='bold')
    # cotas
    cota_h(ax, 0, 24, T(67), '24', (T(60), T(49)))
    cota_h(ax, 29, 62, T(67), '33', (T(40), T(30)))
    cota_h(ax, 0, p['L'], T(75), '120', (T(60), T(60)))
    cota_v(ax, 138, T(0), T(p['W']), '60', (p['L'], p['L']))
    cota_v(ax, -10, T(e['z']), T(m['z']), '16', (e['x'] - r - 5, 0))
    ax.plot([19.4, 12.5], [T(44.6), T(51)], color=COTA, lw=0.5); ax.text(12, T(51.2), '⌀13', ha='right', va='bottom', fontsize=7.5, color=COTA)
    ax.plot([8.4, 8.8], [T(19.2), T(16.4)], color=COTA, lw=0.5); ax.text(9, T(13.2), '⌀10', ha='center', va='bottom', fontsize=7.5, color=COTA)
    ax.text(e['x'] - r, T(30.5), 'repouso', ha='center', fontsize=6, color='#444444')
    # balões
    balao(ax, 14, (35, T(46)), (-34, T(66))); balao(ax, 3, (4, T(53.5)), (-34, T(55)))
    balao(ax, 6, (5, T(21)), (-34, T(14))); balao(ax, 1, (1.4, T(4)), (-34, T(0)))
    for n, alvo, bx in ((7, (17, 24), 14), (5, (25.5, 34.2), 27), (8, (35, 21), 40), (15, (47, 6), 53), (13, (78, 11.3), 68),
                        (12, (93, 14), 84), (11, (103, 17.5), 100), (10, (112.4, 16.8), 116)):
        balao(ax, n, (alvo[0], T(alvo[1])), (bx, T(-14)))


# ---------- peças na vista lateral (usadas no corte e na vista em camadas) ----------
def d_base(ax, dy=0):
    p = P
    hach(ax, 0, p['L'], dy, dy + p['fundo']); hach(ax, 0, p['parede'], dy + p['fundo'], dy + 28); hach(ax, p['L'] - p['parede'], p['L'], dy + p['fundo'], dy + 28)
    h = p['chb']; ret(ax, h['x0'], h['x1'], dy + h['y0'], dy + h['y1'], fc=COR['chave'], lw=0.6)


def d_bobina(ax, dy=0):
    b = P['bob']; ret(ax, b['x'] - b['r'], b['x'] + b['r'], dy + b['y0'], dy + b['y1'], fc=COR['bob'], lw=0.7)


def d_celula(ax, dy=0):
    c = P['cel']; ret(ax, c['x0'], c['x1'], dy + c['y0'], dy + c['y1'], fc=COR['cel'])


def d_placa(ax, dy=0):
    d = P['pci']; ret(ax, d['x0'], d['x1'], dy + d['y0'], dy + d['y1'], fc=COR['pci'], lw=0.7)
    ret(ax, d['x0'] + 6, d['x0'] + 18, dy + d['y1'], dy + d['y1'] + 2.2, fc='#595959', lw=0.5)


def d_mecanismo(ax, dy=0, corte=True):
    p = P; m, i, s, a, b = p['emb'], p['ima'], p['prat'], p['atu'], p['braco']
    ret(ax, s['x0'], s['x1'], dy + s['y0'], dy + s['y1'], fc=COR['sup'], lw=0.6)                       # prateleira
    hach(ax, 39.5, 41.5, dy + p['fundo'], dy + s['y0'], lw=0.8)                                         # coluna do suporte
    for xw in (m['x'] - m['r'] - 1.2, m['x'] + m['r']):
        ret(ax, xw, xw + 1.2, dy + s['y1'], dy + m['y1'], fc=COR['sup'], lw=0.5)                         # berço da embreagem
    ret(ax, m['x'] - m['r'], m['x'] + m['r'], dy + m['y0'], dy + m['y1'], fc=COR['emb'], lw=0.9)
    cone = [(m['x'] - 4.9, dy + m['y0'] + 1), (m['x'] + 4.9, dy + m['y0'] + 1), (m['x'] + 4.9, dy + m['y0'] + 3), (m['x'] + 2.1, dy + m['y1'] - 0.8),
            (m['x'] - 2.1, dy + m['y1'] - 0.8), (m['x'] - 4.9, dy + m['y0'] + 3)]
    ax.add_patch(Polygon(cone, fc='white', ec=K, lw=0.6))
    ret(ax, m['x'] - 3.4, m['x'] + 3.4, dy + m['y0'] + 4.2, dy + m['y0'] + 5.6, fc='#595959', lw=0.4)   # carretel
    for dx in (-1.9, 1.9):
        ax.add_patch(Circle((m['x'] + dx, dy + m['y0'] + 7.6), 1.25, fc='white', ec=K, lw=0.7))
    for k in range(3):
        ret(ax, m['x'] - i['r'], m['x'] + i['r'], dy + i['y0'] + k * (i['y1'] - i['y0']) / 3, dy + i['y0'] + (k + 1) * (i['y1'] - i['y0']) / 3, fc=COR['ima'], lw=0.7)
    hach(ax, m['x'] - b['larg'] / 2, m['x'] + b['larg'] / 2, dy + b['y0'], dy + b['y1'], h='\\\\\\\\', lw=0.8)
    if corte:   # o microatuador fica à frente do plano de corte: linha fantasma
        ax.add_patch(Rectangle((a['x0'], dy + a['y0']), a['x1'] - a['x0'], a['y1'] - a['y0'], fc='none', ec=K, lw=0.8, ls=FANT))
    else:
        ret(ax, a['x0'] + 11, a['x1'], dy + a['y0'], dy + a['y1'], fc=COR['atu'])


def d_tampa(ax, dy=0):
    p = P; m = p['emb']
    hach(ax, 0, m['x'] - 1, dy + 28, dy + 30); hach(ax, m['x'] + 1, p['L'], dy + 28, dy + 30)
    hach(ax, 54, 58.5, dy + 30, dy + 35, lw=0.8)                                                        # apoio da articulação
    h = p['chg']; ret(ax, h['x0'], h['x1'], dy + h['y0'], dy + h['y1'], fc=COR['chave'], lw=0.6)
    x = p['leds']['x']; ret(ax, x - 1.5, x + 1.5, dy + 23, dy + 28, fc='#548235', lw=0.6)
    ax.add_patch(Arc((x, dy + 30), 3, 1.8, theta1=0, theta2=180, color=K, lw=0.7))


def d_garra(ax, dy=0):
    p = P; g, m = p['garra'], p['emb']; y0 = dy + p['H'] + g['folga']
    hach(ax, g['x0'], m['x'] - 6, y0, y0 + g['esp'], h='\\\\\\\\'); hach(ax, m['x'] + 6, g['x1'], y0, y0 + g['esp'], h='\\\\\\\\')
    hach(ax, m['x'] - 6, m['x'] + 6, y0, y0 + g['esp'] - 2, h='\\\\\\\\')
    ax.add_patch(Circle((g['x1'] + 1.5, y0 + 3), 2.6, fc='white', ec=K, lw=1.0)); ax.add_patch(Circle((g['x1'] + 1.5, y0 + 3), 0.9, fc=K))
    ret(ax, m['x'] - 6, m['x'] + 6, y0 + g['esp'] - 2, y0 + g['esp'], fc=COR['emb'], lw=0.8)             # cabeça do pino
    ret(ax, m['x'] - 0.6, m['x'] + 0.6, y0 + g['esp'] - 2 - p['pino']['comp'], y0 + g['esp'] - 2, fc='#404040', lw=0.5, zorder=5)
    return y0 + g['esp']


def corte(ax):
    p = P
    ax.text(-40, 58, 'Corte A–A, pelo eixo do pino, com os ímãs na posição de soltar', fontsize=9, fontweight='bold')
    d_base(ax); d_bobina(ax); d_celula(ax); d_placa(ax); d_mecanismo(ax); d_tampa(ax)
    ax.add_patch(Rectangle((-14, p['H']), 68, p['garra']['folga'], fc='#dbe5f1', ec=K, lw=0.5, hatch='xxxx'))  # tecido
    ax.text(-15, p['H'] + 0.5, 'tecido', ha='right', va='center', fontsize=6.5)
    topo = d_garra(ax)
    ax.plot([24, 24], [-2, topo + 3], color=K, lw=0.4, ls=EIXO)
    cota_v(ax, 132, 0, p['H'], '30', (p['L'], p['L']))
    cota_v(ax, 142, 0, topo, f'{topo:g}', (p['L'], 59))
    balao(ax, 3, (9, topo - 3), (4, 50)); balao(ax, 4, (24.3, 29.5), (18, 50)); balao(ax, 14, (36, 26), (36, 50)); balao(ax, 2, (57, 29), (50, 50))
    balao(ax, 5, (18.6, 22.5), (-30, 27)); balao(ax, 9, (13, 16.4), (-30, 16)); balao(ax, 6, (19.6, 8), (-30, 5)); balao(ax, 1, (4, 0.7), (-30, -8))
    for n, alvo, bx in ((7, (22, 3), 14), (8, (35, 12), 34), (13, (68, 2), 62), (12, (88, 6), 84), (11, (100, 10.8), 102), (10, (112, 25), 118)):
        balao(ax, n, alvo, (bx, -14))
    ax.plot([96, 116], [-25, -25], color=K, lw=2); ax.plot([96, 96, 106, 106, 116, 116], [-26.2, -23.8, -23.8, -26.2, -26.2, -23.8], color=K, lw=0.7)
    for x, tx in ((96, '0'), (106, '10'), (116, '20 mm')):
        ax.text(x, -28, tx, ha='center', va='top', fontsize=6.5)


def conjunto(pasta):
    fig = plt.figure(figsize=(9.4, 11.6))
    gs = fig.add_gridspec(2, 1, height_ratios=[204, 24], hspace=0.02)
    ax = fig.add_subplot(gs[0]); oy = 84
    vista_superior(ax, oy); corte(ax)
    ax.set_xlim(-42, 148); ax.set_ylim(-32, oy + 88); ax.set_aspect('equal'); ax.axis('off')
    al = fig.add_subplot(gs[1]); al.axis('off'); al.set_xlim(0, 3); al.set_ylim(-1.3, 5.6)
    for k, (n, cod, nome) in enumerate(LEGENDA):
        col, lin = divmod(k, 5)
        al.text(col + 0.02, 5 - lin, f'{n}', fontsize=8, fontweight='bold', va='center'); al.text(col + 0.13, 5 - lin, f'{cod}   {nome}', fontsize=8, va='center')
    al.text(0.02, -0.25, 'Cotas em mm. As duas vistas estão na mesma escala. Traço cheio: ímãs em repouso. Tracejado: ímãs sob a embreagem.', fontsize=7, color='#333333', va='center')
    al.text(0.02, -1.0, 'Traço e dois pontos: garra, na vista superior, e microatuador, que fica à frente do plano de corte. Dimensões estimadas, exceto as do mecanismo.', fontsize=7, color='#333333', va='center')
    destino = os.path.join(pasta, 'conjunto_produto.png'); fig.savefig(destino, dpi=220, bbox_inches='tight', facecolor='white'); plt.close(fig); print(destino)


def camadas(pasta):
    fig, ax = plt.subplots(figsize=(9.0, 7.6))
    passos = [(0, d_base, 1, (119, 12), 'base, com a chave da base'), (16, d_bobina, 13, (100, 2), 'bobina de indução'), (26, d_celula, 12, (105, 5.5), 'célula recarregável'),
              (36, d_placa, 11, (104, 10.8), 'placa de controle'), (44, lambda a, dy: d_mecanismo(a, dy, corte=False), 9, (41, 10), 'suporte, com embreagem, ímãs, braço e microatuador'),
              (62, d_tampa, 2, (116, 29), 'tampa, com LEDs e chave da garra'), (72, d_garra, 3, (50, 34), 'garra, com o pino')]
    for dy, fn, n, alvo, nome in passos:
        fn(ax, dy); yb = alvo[1] + dy
        balao(ax, n, (alvo[0], yb), (136, yb)); ax.text(141.5, yb, nome, fontsize=7.5, va='center')
    for n, alvo, onde in ((15, (46, 3.5), (30, 9)), (5, (18.5, 44 + 22), (-12, 44 + 24)), (6, (19.5, 44 + 9), (-12, 44 + 11)), (7, (21, 44 + 3), (-12, 44 + 0)),
                          (8, (36, 44 + 18), (52, 44 + 26)), (10, (112, 62 + 25), (124, 62 + 20)), (14, (36, 62 + 26), (36, 62 + 19)), (4, (24, 72 + 24), (-12, 72 + 27))):
        balao(ax, n, alvo, onde)
    ax.plot([24, 24], [2, 112], color=K, lw=0.4, ls=EIXO)
    ax.annotate('', xy=(-24, 100), xytext=(-24, 6), arrowprops=dict(arrowstyle='-|>', color='#444444', lw=1))
    ax.text(-27, 53, 'ordem de montagem', rotation=90, ha='center', va='center', fontsize=7.5, color='#444444')
    ax.set_xlim(-32, 232); ax.set_ylim(-6, 116); ax.set_aspect('equal'); ax.axis('off')
    destino = os.path.join(pasta, 'conjunto_camadas.png'); fig.savefig(destino, dpi=220, bbox_inches='tight', facecolor='white'); plt.close(fig); print(destino)


if __name__ == '__main__':
    pasta = os.path.dirname(os.path.abspath(__file__))
    conjunto(pasta); camadas(pasta)
