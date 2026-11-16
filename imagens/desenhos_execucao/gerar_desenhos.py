# Gera os desenhos de execução da Entrega 4 (itens A e D): peças fabricadas, subconjunto do
# mecanismo e gabarito de colagem do ímã.
# Uso: python gerar_desenhos.py  ->  de01_base.png ... fd01_gabarito.png na mesma pasta.
# Folha A4 paisagem, coordenadas do papel em mm. Cada vista tem origem e escala próprias.
# As medidas seguem o conjunto revisado pelo DFMA (imagens/conjunto_produto/gerar_conjunto.py).
# Tolerâncias: valores de projeto propostos pela equipe, a confirmar com os fornecedores e com os ensaios.
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Arc, FancyBboxPatch

K = 'black'
COTA = '#1f4e79'
EIXO = (0, (10, 2.5, 1.5, 2.5))
TRAC = (0, (4, 2))
FANT = (0, (9, 2, 1.5, 2, 1.5, 2))
AQUI = os.path.dirname(os.path.abspath(__file__))
TOTAL = 8


class Folha:
    def __init__(self, n, codigo, titulo, material, escala, notas, arquivo):
        self.fig = plt.figure(figsize=(11.69, 8.27))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        ax = self.ax
        ax.set_xlim(0, 297); ax.set_ylim(0, 210); ax.set_aspect('equal'); ax.axis('off')
        ax.add_patch(Rectangle((10, 8), 277, 194, fc='none', ec=K, lw=1.4))
        self.arquivo = arquivo
        # legenda (carimbo)
        x0, y0, w, h = 167, 8, 120, 38
        ax.add_patch(Rectangle((x0, y0), w, h, fc='white', ec=K, lw=1.1, zorder=20))
        for yy in (y0 + 9.5, y0 + 19, y0 + 28.5):
            ax.plot([x0, x0 + w], [yy, yy], color=K, lw=0.6, zorder=21)
        ax.plot([x0 + 78, x0 + 78], [y0, y0 + 28.5], color=K, lw=0.6, zorder=21)
        t = lambda x, y, s, **k: ax.text(x, y, s, zorder=22, va='center', **k)
        t(x0 + 2, y0 + 33.2, 'Tag&Go  –  ' + titulo, fontsize=9.5, fontweight='bold')
        t(x0 + 2, y0 + 23.7, 'Código: ' + codigo, fontsize=8, fontweight='bold')
        t(x0 + 80, y0 + 23.7, 'Escala: ' + escala, fontsize=7.5)
        t(x0 + 2, y0 + 14.2, 'Material: ' + material, fontsize=6.6 if len(material) < 48 else 5.4)
        t(x0 + 80, y0 + 14.2, 'Folha %d/%d  ·  A4' % (n, TOTAL), fontsize=7.5)
        t(x0 + 2, y0 + 4.7, 'PRO3474 – Poli-USP · Grupo 4 · Prof. Eduardo Zancul', fontsize=6.6)
        t(x0 + 80, y0 + 4.7, 'Rev. A  ·  nov. 2026', fontsize=7.5)
        # notas
        ax.text(13, 44, 'NOTAS', fontsize=7.5, fontweight='bold', va='top')
        linhas, n = [], 0
        for s in notas:                 # linha iniciada por espaço continua a nota anterior, sem número novo
            if s.startswith(' '):
                linhas.append('    ' + s.strip())
            else:
                n += 1
                linhas.append('%d. %s' % (n, s))
        ax.text(13, 40, '\n'.join(linhas), fontsize=6.3, va='top', linespacing=1.35)

    def salvar(self):
        self.fig.savefig(os.path.join(AQUI, self.arquivo), dpi=220)
        plt.close(self.fig)


class Vista:
    """Vista com origem (ox, oy) no papel e escala k. Coordenadas em mm da peça."""

    def __init__(self, folha, ox, oy, k, titulo=None, ty=None):
        self.ax, self.ox, self.oy, self.k = folha.ax, ox, oy, k
        if titulo:
            self.ax.text(ox, oy + (ty if ty is not None else -6), titulo, fontsize=7.5, fontweight='bold', zorder=12, bbox=dict(fc='white', ec='none', pad=0.5))

    def P(self, x, y):
        return self.ox + self.k * x, self.oy + self.k * y

    def lin(self, x0, y0, x1, y1, lw=0.9, ls='-', c=K, z=5):
        a, b = self.P(x0, y0), self.P(x1, y1)
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color=c, lw=lw, ls=ls, zorder=z, solid_capstyle='butt')

    def ret(self, x0, y0, x1, y1, lw=0.9, fc='none', ls='-', h=None, ec=K, z=4):
        a = self.P(min(x0, x1), min(y0, y1))
        self.ax.add_patch(Rectangle(a, abs(x1 - x0) * self.k, abs(y1 - y0) * self.k, fc=fc, ec=ec, lw=lw, ls=ls, hatch=h, zorder=z))

    def pol(self, pts, lw=0.9, fc='none', h=None, ls='-', z=4, ec=K):
        self.ax.add_patch(Polygon([self.P(*p) for p in pts], closed=True, fc=fc, ec=ec, lw=lw, hatch=h, ls=ls, zorder=z))

    def cir(self, x, y, r, lw=0.9, fc='none', ls='-', ec=K, z=5, h=None):
        self.ax.add_patch(Circle(self.P(x, y), r * self.k, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z, hatch=h))

    def arco(self, x, y, r, t1, t2, lw=0.9, ls='-', c=K):
        self.ax.add_patch(Arc(self.P(x, y), 2 * r * self.k, 2 * r * self.k, theta1=t1, theta2=t2, color=c, lw=lw, ls=ls, zorder=5))

    def cantos(self, x0, y0, x1, y1, r, lw=1.2, fc='none', z=3):
        a = self.P(x0, y0)
        self.ax.add_patch(FancyBboxPatch(a, (x1 - x0) * self.k, (y1 - y0) * self.k,
                                         boxstyle='round,pad=0,rounding_size=%f' % (r * self.k), fc=fc, ec=K, lw=lw, zorder=z))

    def centro(self, x, y, d):
        self.lin(x - d, y, x + d, y, lw=0.4, ls=EIXO); self.lin(x, y - d, x, y + d, lw=0.4, ls=EIXO)

    def eixo(self, x0, y0, x1, y1):
        self.lin(x0, y0, x1, y1, lw=0.4, ls=EIXO)

    def txt(self, x, y, s, fs=6.3, c=K, **k):
        a = self.P(x, y)
        k.setdefault('ha', 'center'); k.setdefault('va', 'center')
        self.ax.text(a[0], a[1], s, fontsize=fs, color=c, zorder=12, **k)

    def _seta(self, a, b):
        self.ax.annotate('', xy=a, xytext=b, zorder=11,
                         arrowprops=dict(arrowstyle='<|-|>', color=COTA, lw=0.6, shrinkA=0, shrinkB=0, mutation_scale=6))

    def ch(self, x0, x1, y, d, s):
        """Cota horizontal entre x0 e x1, tirada da altura y e afastada d mm no papel."""
        a, b = self.P(x0, y), self.P(x1, y)
        yy = a[1] + d
        sg = 1 if d > 0 else -1
        for p in (a, b):
            self.ax.plot([p[0], p[0]], [p[1] + sg * 0.8, yy + sg * 1.0], color=COTA, lw=0.4, zorder=10)
        self._seta((a[0], yy), (b[0], yy))
        self.ax.text((a[0] + b[0]) / 2, yy + 0.9, s, ha='center', va='bottom', fontsize=6.3, color=COTA, zorder=12, bbox=dict(fc='white', ec='none', pad=0.5))

    def cv(self, y0, y1, x, d, s):
        """Cota vertical entre y0 e y1, tirada da abscissa x e afastada d mm no papel."""
        a, b = self.P(x, y0), self.P(x, y1)
        xx = a[0] + d
        sg = 1 if d > 0 else -1
        for p in (a, b):
            self.ax.plot([p[0] + sg * 0.8, xx + sg * 1.0], [p[1], p[1]], color=COTA, lw=0.4, zorder=10)
        self._seta((xx, a[1]), (xx, b[1]))
        self.ax.text(xx - 0.9, (a[1] + b[1]) / 2, s, ha='right', va='center', fontsize=6.3, color=COTA, rotation=90, zorder=12, bbox=dict(fc='white', ec='none', pad=0.5))

    def cham(self, x, y, dx, dy, s, ha='left'):
        """Chamada: seta no ponto (x, y) e texto deslocado (dx, dy) mm no papel."""
        a = self.P(x, y)
        self.ax.annotate(s, xy=a, xytext=(a[0] + dx, a[1] + dy), fontsize=6.3, color=COTA, ha=ha, va='center', zorder=12, bbox=dict(fc='white', ec='none', pad=0.5), 
                         arrowprops=dict(arrowstyle='-|>', color=COTA, lw=0.5, shrinkA=1, shrinkB=0, mutation_scale=6))

    def balao(self, n, x, y, dx, dy):
        a = self.P(x, y); b = (a[0] + dx, a[1] + dy)
        self.ax.plot([a[0], b[0]], [a[1], b[1]], color='#444444', lw=0.5, zorder=13)
        self.ax.add_patch(Circle(a, 0.5, color='#222222', zorder=14))
        self.ax.add_patch(Circle(b, 3.0, fc='white', ec=K, lw=0.8, zorder=15))
        self.ax.text(b[0], b[1] - 0.1, str(n), ha='center', va='center', fontsize=7, fontweight='bold', zorder=16)

    def corte(self, x0, y0, x1, y1, letra, dx=0, dy=6):
        self.lin(x0, y0, x1, y1, lw=0.5, ls=EIXO)
        for (x, y) in ((x0, y0), (x1, y1)):
            a = self.P(x, y)
            self.ax.annotate('', xy=(a[0] + dx, a[1] + dy), xytext=a, zorder=11,
                             arrowprops=dict(arrowstyle='-|>', color=K, lw=0.9, mutation_scale=8))
            self.ax.text(a[0] + dx * 1.35, a[1] + dy * 1.35, letra, ha='center', va='center', fontsize=8, fontweight='bold')


def quadro_gdt(v, x, y, simbolo, valor, ref=None):
    """Quadro de tolerância geométrica simplificado, no ponto (x, y) da vista."""
    a = v.P(x, y)
    cel = [simbolo, valor] + ([ref] if ref else [])
    w = [5, 9, 5]
    xx = a[0]
    for i, s in enumerate(cel):
        v.ax.add_patch(Rectangle((xx, a[1]), w[i], 4.2, fc='white', ec=COTA, lw=0.5, zorder=12))
        v.ax.text(xx + w[i] / 2, a[1] + 2.0, s, ha='center', va='center', fontsize=6, color=COTA, zorder=13)
        xx += w[i]


def ref_dado(v, x, y, letra, dx=0, dy=-5):
    a = v.P(x, y)
    v.ax.plot([a[0], a[0] + dx], [a[1], a[1] + dy], color=COTA, lw=0.5, zorder=12)
    v.ax.add_patch(Polygon([(a[0] - 1.2, a[1]), (a[0] + 1.2, a[1]), (a[0] + dx * 0.25, a[1] + dy * 0.25 if dx == 0 else a[1])],
                           fc=COTA, ec=COTA, zorder=12)) if dx == 0 else None
    v.ax.add_patch(Rectangle((a[0] + dx - 2.2, a[1] + dy - (4.2 if dy < 0 else 0)), 4.4, 4.2, fc='white', ec=COTA, lw=0.5, zorder=12))
    v.ax.text(a[0] + dx, a[1] + dy + (-2.1 if dy < 0 else 2.1), letra, ha='center', va='center', fontsize=6.3, color=COTA, zorder=13)


GERAL_PLAST = 'Tolerâncias gerais não indicadas: ISO 20457, grau TG5. Ângulo de saída de 1° nas paredes, salvo indicação.'
GERAL_USIN = 'Tolerâncias gerais não indicadas: ISO 2768-fH. Rebarbas removidas; cantos vivos quebrados 0,1 mm.'
A_CONF = 'Tolerâncias indicadas são valores de projeto, a confirmar com o fornecedor e após o ensaio do campo.'


# ------------------------------------------------------------------ DE-01 base
def de01():
    f = Folha(1, 'TG-111 / DE-01', 'Base da carcaça', 'PC/ABS injetado, preto', '1:1', [
        GERAL_PLAST,
        'Fundo de 1,50 ±0,10 sob a bobina (cota funcional da recarga por indução).',
        'Raios internos mínimos de 0,5 mm. Sem marcas de extração na face externa do fundo.',
        'Marcar >PC+ABS< em relevo na face interna do fundo (ISO 11469).',
        'Torres dos parafusos: furo-piloto Ø1,8 para parafuso autoatarraxante 2,2 mm.',
        A_CONF], 'de01_base.png')
    L, W, H = 120, 60, 28
    v = Vista(f, 32, 116, 1, 'Vista superior', ty=77)
    v.cantos(0, 0, L, W, 5); v.cantos(2, 2, L - 2, W - 2, 3, lw=0.8)
    for z in (5, 55):
        v.cir(5, z, 2.6); v.cir(5, z, 0.9); v.centro(5, z, 4.5)
    for z in (14, 46):                                   # janelas das abas da tampa
        v.ret(L - 2, z - 3, L, z + 3, lw=0.8, fc='#dddddd')
    v.cir(82, 30, 20.5, lw=0.6, ls=TRAC); v.centro(82, 30, 24)
    for (x, z, sx, sz) in ((57, 13, 1, 1), (107, 13, -1, 1), (57, 47, 1, -1), (107, 47, -1, -1)):   # nervuras da célula
        v.lin(x, z, x + 5 * sx, z, lw=0.8); v.lin(x, z, x, z + 5 * sz, lw=0.8)
    for (x, z) in ((40.5, 21), (14, 48)):                # pinos de posição do suporte
        v.cir(x, z, 1.0, fc='#bbbbbb'); v.centro(x, z, 3)
    v.corte(-8, 30, 128, 30, 'A')
    v.corte(5, -23, 5, 66, 'B', dx=-6, dy=0)
    v.ch(0, L, W, 10, '120 ±0,2'); v.cv(0, W, L, 14, '60 ±0,2')
    v.ch(0, 5, 0, -8, '5'); v.cv(5, 55, 0, -12, '50 ±0,1')
    v.ch(0, 40.5, 0, -14, '40,5 ±0,05'); v.ch(0, 82, 0, -20, '82')
    v.cham(8.5, 1.5, 12, -4, 'R5')
    v.cham(82 - 14.5, 30 - 14.5, -8, -22, 'assento da bobina Ø41, ressalto 0,8')
    v.cham(14, 48, 14, -8, '2 pinos Ø2,0 −0,05 (posição do suporte)')
    v.cham(120, 46, 22, 12, '2 janelas 6 × 2 (abas da tampa)')
    v.cham(107, 47, 12, 22, 'nervuras de posição da célula')
    # corte A-A
    c = Vista(f, 32, 58, 1, 'Corte A–A', ty=31)
    c.ax.texts[-1].set_x(60)
    c.ret(0, 0, L, 1.5, h='/////', lw=1.0); c.ret(0, 1.5, 2, H, h='/////', lw=1.0); c.ret(L - 2, 1.5, L, H, h='/////', lw=1.0)
    c.ret(L - 2, 23, L, 25, fc='white', lw=0.7)
    c.ret(61.5, 1.5, 102.5, 2.3, lw=0.6, fc='#dddddd')
    c.ret(13, 1.5, 15, 6, lw=0.7, fc='#bbbbbb'); c.ret(39.5, 1.5, 41.5, 6, lw=0.7, fc='#bbbbbb')
    c.cv(0, H, L, 12, '28 ±0,1'); c.cham(8, 0.75, -14, 8, '1,50 ±0,10', ha='right'); c.cham(1, 12, 10, 4, 'parede 2,0')
    c.cham(L - 1, 24, 10, 6, 'janela a 23 do fundo')
    quadro_gdt(c, 50, -8, '⏥', '0,15'); c.lin(52, -3.8, 52, 0, lw=0.4, c=COTA)
    ref_dado(c, 20, 0, 'A')
    # corte B-B
    b = Vista(f, 215, 116, 1, 'Corte B–B', ty=77)
    b.ret(0, 0, 1.5, W, h='/////', lw=1.0); b.ret(1.5, 0, H, 2, h='/////', lw=1.0); b.ret(1.5, W - 2, H, W, h='/////', lw=1.0)
    for z in (5, 55):
        b.ret(1.5, z - 2.6, 26.5, z + 2.6, h='/////', lw=0.8); b.ret(16.5, z - 0.9, 26.5, z + 0.9, fc='white', lw=0.6)
    b.ch(1.5, 26.5, W, 8, '25'); b.ch(16.5, 26.5, 0, -8, 'Ø1,8 × 10')
    b.txt(14, -16, '(vista girada 90°)', fs=5.8)
    f.salvar()


# ------------------------------------------------------------------ DE-02 tampa
def de02():
    f = Folha(2, 'TG-112 / DE-02', 'Tampa', 'PC/ABS injetado, grau para marcação a laser', '1:1', [
        GERAL_PLAST,
        'Área de 30 × 30 reservada à gravação a laser do código 2D: face lisa, sem ponto de injeção nem linha de solda.',
        'Furo do pino com chanfro de 0,5 × 45° na face externa, para guiar o pino.',
        'Mancais da garra (M7): assento Ø3,1 aberto para cima; a garra entra por encaixe.',
        'Marcar >PC+ABS< em relevo na face interna (ISO 11469).',
        A_CONF], 'de02_tampa.png')
    L, W = 120, 60
    v = Vista(f, 34, 112, 1, 'Vista superior (face externa)', ty=82)
    v.cantos(0, 0, L, W, 5)
    v.cir(24, 40, 1.0); v.cir(24, 40, 1.5, lw=0.5); v.centro(24, 40, 5)
    for z in (5, 55):
        v.cir(5, z, 1.2); v.cir(5, z, 2.2, lw=0.5); v.centro(5, z, 4)
    v.cir(102, 40, 2.0); v.centro(102, 40, 4.5)
    v.cir(36, 44, 1.5); v.centro(36, 44, 3.5)
    v.ret(67, 15, 97, 45, lw=0.5, ls=TRAC); v.txt(82, 30, 'área do código 2D\n30 × 30', fs=5.8)
    for z0 in (20.5, 56.5):                              # mancais da garra
        v.ret(51.5, z0, 56.5, z0 + 3, lw=0.9, fc='#dddddd')
    v.eixo(54, 16, 54, 64)
    for z in (14, 46):
        v.ret(L - 4, z - 3, L - 2.1, z + 3, lw=0.6, ls=TRAC)
    v.corte(-8, 40, 128, 40, 'A')
    v.ch(0, L, W, 15, '120 ±0,2'); v.cv(0, W, L, 14, '60 ±0,2')
    v.ch(0, 24, W, 7, '24,00 ±0,05'); v.cv(0, 40, 0, -8, '40,00 ±0,05')
    v.ch(24, 54, 0, -8, '30,00 ±0,05'); v.ch(0, 102, 0, -15, '102'); v.ch(0, 36, 0, -21, '36 ±0,1')
    v.cham(24, 40, -6, -12, 'Ø2,0 +0,1/0 (pino)', ha='center')
    v.cham(102, 40, -4, 13, 'Ø4,0 +0,05/0 (guia de luz)', ha='right')
    v.cham(36, 44, 8, 8, 'Ø3,0 (haste da chave)')
    v.cham(5, 5, 10, 9, '2 × Ø2,4, escareado Ø4,4', ha='left')
    v.cham(56.5, 22, 10, -8, '2 mancais, assento Ø3,1 +0,05/0')
    v.cham(118, 14, 6, -7, '2 abas de encaixe, 6 de largura')
    ref_dado(v, 70, 0, 'A'); ref_dado(v, 0, 52, 'B', dx=-6, dy=0)
    # corte A-A
    c = Vista(f, 34, 62, 1, 'Corte A–A', ty=16)
    c.ret(0, 0, 23, 2, h='/////', lw=1.0); c.ret(25, 0, 100, 2, h='/////', lw=1.0); c.ret(104, 0, L, 2, h='/////', lw=1.0)
    c.ret(2.1, -1.5, 3.6, 0, h='/////', lw=0.8); c.ret(L - 3.6, -1.5, L - 2.1, 0, h='/////', lw=0.8)
    c.pol([(L - 3.6, -1.5), (L - 2.1, -1.5), (L - 2.1, -4), (L - 1.5, -4.6), (L - 2.1, -5.4), (L - 3.6, -5.4)], fc='#dddddd', lw=0.8)
    c.pol([(51.5, 2), (56.5, 2), (56.5, 7), (55.6, 7), (55.6, 4.4), (52.4, 4.4), (52.4, 7), (51.5, 7)], fc='#dddddd', lw=0.8)
    c.cir(54, 4.4, 1.55, lw=0.6, ls=TRAC)
    c.eixo(24, -5, 24, 6)
    c.cham(12, 1, -16, 8, '2,0 ±0,1', ha='right'); c.cham(54, 4.4, -12, 7, 'eixo a 2,4 ±0,05 da face', ha='right')
    c.cham(L - 1.5, -4.6, 8, -4, 'aba: gancho de 0,6')
    c.cham(3, -1.5, 4, -8, 'ressalto de posição 1,5 × 1,5 em todo o contorno')
    quadro_gdt(c, 70, 6, '⊕', 'Ø0,10', 'A B'); c.txt(70, 13, 'posição do furo do pino', fs=5.8, ha='left', c=COTA)
    # detalhe do furo
    d = Vista(f, 228, 140, 6, 'Detalhe do furo do pino (6:1)', ty=26)
    d.ret(-4, 0, -1, 2, h='/////', lw=1.0); d.ret(1, 0, 4, 2, h='/////', lw=1.0)
    d.pol([(-1, 2), (-1.5, 2), (-1, 1.5)], fc='white', lw=0.8); d.pol([(1, 2), (1.5, 2), (1, 1.5)], fc='white', lw=0.8)
    d.eixo(0, -1, 0, 3.2); d.ch(-1, 1, 0, -6, 'Ø2,0 +0,1/0'); d.cham(1.25, 1.75, 10, 5, '0,5 × 45°')
    f.salvar()


# ------------------------------------------------------------------ DE-03 suporte
def de03():
    f = Folha(3, 'TG-113 / DE-03', 'Suporte do mecanismo', 'POM copolímero injetado, natural', '2:1', [
        GERAL_PLAST,
        'Item crítico. Características críticas (CC): espessura e planicidade da prateleira, distância de 16,00 entre os eixos,',
        '   altura de 14,50 da face inferior da prateleira ao plano dos pés (referência A) e furo do alojamento da embreagem.',
        'Ponto de injeção na borda da prateleira, do lado oposto ao alojamento. Sem marcas de extração na prateleira.',
        'Marcar >POM< em relevo na parede A (ISO 11469).',
        A_CONF], 'de03_suporte.png')
    k = 2
    v = Vista(f, 38, 112, k, 'Vista superior', ty=74)
    # paredes e prateleira (u = x − 12, v = z − 19)
    v.ret(0, 12, 29.5, 30, lw=1.1)                        # prateleira
    v.ret(27.5, 0, 29.5, 30, lw=1.1, fc='#dddddd')        # parede A
    v.ret(0, 28, 27.5, 30, lw=1.1, fc='#dddddd')          # parede B
    v.cir(12, 21, 8.0, lw=1.1); v.cir(12, 21, 6.525, lw=0.9); v.centro(12, 21, 10.5)
    v.ret(7, 0.75, 27.5, 9.25, lw=0.6, ls=FANT); v.txt(19.5, 7.6, 'microatuador', fs=5.5)
    v.cir(12, 5, 1.6, lw=0.6, ls=FANT); v.centro(12, 5, 4.5)
    v.ret(21, 22, 27, 28, lw=0.9, fc='#eeeeee'); v.txt(24, 25, 'apoio\nda chave', fs=5)
    v.pol([(22.5, 0.75), (27.5, 0.75), (27.5, 0), (22.5, 0)], lw=0.8, fc='#dddddd')
    v.pol([(22.5, 9.25), (27.5, 9.25), (27.5, 10), (22.5, 10)], lw=0.8, fc='#dddddd')
    for (x, y) in ((28.5, 2), (2, 29)):
        v.cir(x, y, 1.0, lw=0.8, fc='white'); v.centro(x, y, 2.2)
    v.corte(-5, 21, 34.5, 21, 'A')
    v.ch(0, 29.5, 30, 9, '29,5'); v.cv(0, 30, 29.5, 16, '30')
    v.cv(5, 21, 0, -9, '16,00 ±0,05  (CC)')
    v.ch(0, 12, 0, -8, '12,00 ±0,05')
    v.cham(12 + 4.6, 21 + 4.6, 9, 12, 'Ø13,05 +0,05/0  (CC)')
    v.cham(28.5, 2, 10, -5, '2 × Ø2,05 +0,05/0')
    v.cham(25, 9.6, 10, 6, 'presilhas do microatuador')
    ref_dado(v, 12, 12, 'B', dx=0, dy=-5)
    # corte A-A (u horizontal, w vertical)
    c = Vista(f, 158, 112, k, 'Corte A–A', ty=74)
    c.ret(27.5, 0, 29.5, 15.3, h='/////', lw=1.0)                       # parede A
    c.ret(0, 14.5, 5.475, 15.3, h='/////', lw=1.0); c.ret(18.525, 14.5, 27.5, 15.3, h='/////', lw=1.0)
    c.ret(5.475, 14.5, 18.525, 15.3, h='/////', lw=1.0)                 # prateleira sob a embreagem
    c.ret(4, 15.3, 5.475, 26.3, h='/////', lw=1.0); c.ret(18.525, 15.3, 20, 26.3, h='/////', lw=1.0)
    c.ret(21, 15.3, 27, 22.5, h='/////', lw=0.9)                        # apoio da chave
    c.ret(0, 0, 27.5, 14.5, lw=0.5, ls=TRAC)                            # parede B ao fundo
    c.eixo(12, -3, 12, 30)
    c.lin(-3, 0, 33, 0, lw=0.4, c=COTA)
    c.cv(0, 14.5, 29.5, 12, '14,50 ±0,05  (CC)'); c.cv(15.3, 26.3, 29.5, 22, '11,0 ±0,1')
    c.cv(15.3, 22.5, 27, 5, '7,2')
    c.ch(5.475, 18.525, 26.3, 6, 'Ø13,05'); c.ch(4, 20, 26.3, 12, 'Ø16')
    c.cham(23, 14.9, 4, -12, '0,80 ±0,05  (CC)', ha='center')
    quadro_gdt(c, -11, 19.5, '⏥', '0,05'); c.lin(-4, 20.5, 2, 15.3, lw=0.4, c=COTA)
    ref_dado(c, 5, 0, 'A')
    quadro_gdt(c, -11, 8, '∥', '0,05', 'A'); c.lin(-1.5, 9, 2, 14.5, lw=0.4, c=COTA)
    # detalhe da prateleira
    d = Vista(f, 158, 62, 10, 'Detalhe da prateleira (10:1)', ty=24)
    d.ret(0, 0, 7, 0.8, h='/////', lw=1.0); d.ret(0, 0.8, 1.4, 1.8, h='/////', lw=1.0)
    d.pol([(1.4, 0.8), (1.7, 0.8), (1.4, 1.1)], fc='white', lw=0.7)
    d.cv(0, 0.8, 7, 8, '0,80 ±0,05'); d.cham(1.55, 0.95, 14, 8, 'R0,3 na raiz do alojamento')
    d.txt(3.5, -0.6, 'face voltada para o ímã: Ra ≤ 0,8 μm (polimento do molde)', fs=5.5, c=COTA)
    f.salvar()


# ------------------------------------------------------------------ DE-04 garra
def de04():
    f = Folha(4, 'TG-211 / DE-04', 'Corpo da garra (com pino e revestimento)',
              'Al fundido (AlSi9Cu3) + pino AISI 420 + TPE 65 Shore A', '1,5:1', [
        'Fundição sob pressão. Tolerâncias gerais não indicadas: ISO 8062-3, grau DCTG 6. Ângulo de saída de 1,5°.',
        'Pino TG-221 (Ø1,2 × 16, AISI 420 temperado) colocado como inserto no molde, com 5 mm embutidos e recartilhado na parte embutida.',
        'Verificar a dureza do pino depois da fundição (≥ 48 HRC). Se houver revenimento, o pino passa a ser prensado após a fundição.',
        'Revestimento de TPE sobreinjetado na face do tecido, com 1,0 mm de espessura; os dentes ficam 0,3 mm acima do revestimento.',
        'Munhões: usinar após a fundição, Ø3,00 −0,02/−0,06. Acabamento por vibroacabamento e conversão química; não anodizar (pino de aço).',
        A_CONF], 'de04_garra.png')
    k = 1.5
    v = Vista(f, 50, 116, k, 'Vista inferior (face do tecido)', ty=68)
    v.cantos(0, 0, 52, 32, 2)
    for z0, z1 in ((-2.5, 0), (32, 34.5)):               # munhões
        v.ret(50.5, z0, 53.5, z1, lw=0.9, fc='#dddddd')
    v.eixo(52, -6, 52, 38)
    v.ret(6, 3, 40, 29, lw=0.6, fc='#f4e3c1'); v.txt(31, 8, 'TPE', fs=5.8)
    for i in range(12):                                   # dentes
        x = 3 + i * 1.6
        v.lin(x, 5, x, 27, lw=0.5)
    v.cir(22, 16, 0.6, fc=K); v.centro(22, 16, 4)
    v.ret(42, 11, 49, 21, lw=0.7, ls=TRAC); v.txt(45.5, 16, 'alojamento\nda mola', fs=4.8)
    v.corte(-18, 16, 64, 16, 'A')
    v.ch(0, 52, 34.5, 8, '52 ±0,15'); v.cv(0, 32, 0, -8, '32 ±0,15'); v.cv(-2.5, 34.5, 53.5, 12, '37,0 −0,1')
    v.ch(22, 52, -2.5, -7, '30,00 ±0,05'); v.cv(0, 16, 0, -16, '16,00 ±0,05')
    v.cham(52, 33.5, 8, 9, '2 munhões Ø3,00 −0,02/−0,06')
    v.cham(12, 27, 4, 14, '12 dentes, passo 1,6', ha='center')
    ref_dado(v, 52, -4.5, 'A', dx=8, dy=0)
    # corte A-A
    c = Vista(f, 50, 72, k, 'Corte A–A (garra na posição de uso, tecido para baixo)', ty=24)
    c.pol([(0, 0), (52, 0), (52, 6), (0, 6)], h='/////', lw=1.0)
    c.ret(42, 0, 49, 3, fc='white', lw=0.7)
    c.cir(52, 3, 1.5, lw=0.9, fc='#dddddd')
    c.ret(6, -1, 40, 0, fc='#f4e3c1', lw=0.7)
    for i in range(12):
        x = 3 + i * 1.6
        c.pol([(x - 0.5, -0.0), (x + 0.5, 0.0), (x, -1.3)], fc='#999999', lw=0.5)
    c.ret(21.4, -11, 22.6, 5, fc='#555555', lw=0.6, z=6)
    c.eixo(22, -14, 22, 9)
    c.cv(0, 6, 0, -8, '6,0 ±0,1'); c.cv(-11, 0, 22, -14, '11,0 ±0,2')
    c.cham(34, -0.5, 10, -10, 'TPE, 1,0 de espessura')
    c.cham(22.6, -8, 12, -6, 'pino Ø1,2 h9, ponta arredondada R0,3')
    c.cham(52, 3, 8, 5, 'eixo da articulação')
    quadro_gdt(c, 62, -6, '⊥', 'Ø0,10', 'B'); c.txt(62, -8.5, 'pino em relação à face do tecido (B)', fs=5.5, ha='left', c=COTA)
    ref_dado(c, 3, 0, 'B', dx=0, dy=-9)
    f.salvar()


# ------------------------------------------------------------------ DE-05 braço
def de05():
    f = Folha(5, 'TG-312 / DE-05', 'Braço dos ímãs', 'Al 6061-T6, anodizado natural', '4:1', [
        GERAL_USIN,
        'Item crítico. Características críticas (CC): distância de 16,00 entre o furo do eixo e o alojamento do ímã,',
        '   profundidade do alojamento e planicidade da face de apoio.',
        'Furo do cubo no perfil do eixo do microatuador (duplo D). Medidas a confirmar com o microatuador escolhido;',
        '   interferência de 0,02 a 0,05 mm para a montagem por pressão (M3).',
        'Alojamento com rugosidade Ra 1,6 a 3,2 μm, para ancorar o adesivo.',
        A_CONF], 'de05_braco.png')
    k = 4
    v = Vista(f, 70, 126, k, 'Vista superior', ty=40)
    import numpy as np
    r1, r2, d = 4.0, 5.9, 16.0
    # contorno por tangentes externas
    a = np.arcsin((r2 - r1) / d)
    t1 = np.linspace(np.pi / 2 + a, 3 * np.pi / 2 - a, 40)
    t2 = np.linspace(-np.pi / 2 - a + 0, np.pi / 2 + a, 40)
    pts = [(r1 * np.cos(t), r1 * np.sin(t)) for t in t1] + [(d + r2 * np.cos(t), r2 * np.sin(t)) for t in t2]
    v.pol(pts, lw=1.2)
    v.cir(d, 0, 5.05, lw=0.9); v.centro(d, 0, 7.5); v.centro(0, 0, 5.5)
    ang = np.arcsin(1.5 / 2.0)
    hd = [(2.0 * np.cos(t), 2.0 * np.sin(t)) for t in np.linspace(-ang, ang, 12)] + [(2.0 * np.cos(t), 2.0 * np.sin(t)) for t in np.linspace(np.pi - ang, np.pi + ang, 12)]
    v.pol(hd, lw=0.9)
    v.corte(-12, 0, 30, 0, 'A', dy=6)
    v.ch(0, d, -5.9, -9, '16,00 ±0,03  (CC)')
    v.ch(-4, d + 5.9, 5.9, 9, '25,9')
    v.cv(-5.9, 5.9, d + 5.9, 10, '11,8'); v.cv(-4, 4, -4, -8, 'Ø8')
    v.cham(d + 3.6, 3.6, 22, 14, 'alojamento Ø10,10 +0,05/0')
    v.cham(1.2, 1.5, -2, 26, 'furo duplo D: Ø4,0 com faces a 3,0 (a confirmar)', ha='center')
    # corte
    c = Vista(f, 70, 70, k, 'Corte A–A', ty=20)
    c.pol([(-4, 0), (-2, 0), (-2, 2), (-4, 2)], h='/////', lw=1.0)
    c.pol([(2, 0), (d - 5.05, 0), (d - 5.05, 1.5), (d + 5.05, 1.5), (d + 5.05, 2), (d + 5.9, 2), (d + 5.9, 0), (d + 5.9, 0), (2, 0)], lw=0)
    c.pol([(2, 0), (d + 5.9, 0), (d + 5.9, 2), (d + 5.05, 2), (d + 5.05, 1.5), (d - 5.05, 1.5), (d - 5.05, 2), (2, 2)], h='/////', lw=1.0)
    c.eixo(0, -2, 0, 4); c.eixo(d, -2, d, 4)
    c.cv(0, 2, -4, -8, '2,00 ±0,05'); c.cv(1.5, 2, d + 5.9, 10, '0,50 ±0,02  (CC)')
    quadro_gdt(c, 4, -4.5, '⏥', '0,03'); c.lin(5, -3.45, 5, 0, lw=0.4, c=COTA); c.txt(8, -4.0, 'face de apoio no batente da prensa', fs=5.5, ha='left', c=COTA)
    ref_dado(c, 8, 2, 'A', dx=0, dy=6)
    f.salvar()


# ------------------------------------------------------------------ DE-06 guia de luz
def de06():
    f = Folha(6, 'TG-412 / DE-06', 'Guia de luz', 'PC transparente injetado, grau óptico', '5:1', [
        GERAL_PLAST,
        'Faces de entrada e de saída da luz com polimento óptico (Ra ≤ 0,05 μm). Corpo com textura leve, para difundir a luz.',
        'Ponto de injeção no colar. Sem bolhas nem inclusões visíveis a olho nu.',
        'Montagem por encaixe na janela Ø4,0 da tampa (DE-02), pela face interna; o ressalto de 0,1 retém a guia.',
        'Marcar >PC< no colar, se o tamanho permitir (ISO 11469).',
        A_CONF], 'de06_guia.png')
    k = 5
    v = Vista(f, 50, 125, k, 'Vista lateral', ty=32)
    v.ret(0, -1.5, 12, 1.5, lw=1.1)        # haste
    v.ret(12, -2.75, 13, 2.75, lw=1.1)     # colar
    v.ret(13, -2.0, 15, 2.0, lw=1.1)       # cabeça
    v.pol([(13.6, 2.0), (14.0, 2.1), (14.4, 2.0)], lw=0.7); v.pol([(13.6, -2.0), (14.0, -2.1), (14.4, -2.0)], lw=0.7)
    v.eixo(-2, 0, 17, 0)
    v.ch(0, 15, 2.75, 8, '15,0 ±0,1'); v.ch(0, 12, -2.75, -6, '12,0'); v.ch(12, 13, -2.75, -12, '1,0'); v.ch(13, 15, -2.75, -6, '2,0 ±0,05')
    v.cv(-1.5, 1.5, 0, -7, 'Ø3,0'); v.cham(14.6, -2.0, 16, -16, 'Ø4,00 −0,02/−0,06 (cabeça)'); v.cv(-2.75, 2.75, 15, 14, 'Ø5,5')
    v.cham(14.0, 2.1, -6, 10, 'ressalto de retenção 0,1', ha='right')
    v.cham(0, 1.0, -10, 9, 'entrada da luz (LED)', ha='right'); v.cham(15, 1.0, 26, 8, 'saída da luz')
    w = Vista(f, 215, 125, k, 'Vista frontal', ty=32)
    w.cir(0, 0, 2.75, lw=1.1); w.cir(0, 0, 2.0, lw=1.1); w.cir(0, 0, 1.5, lw=0.6, ls=TRAC); w.centro(0, 0, 4)
    # montagem na tampa
    m = Vista(f, 200, 82, 4, 'Guia montada na tampa (4:1) – subconjunto da tampa', ty=16)
    m.ox, m.oy = 215, 80
    m.ret(-8, 0, -2, 2, h='/////', lw=1.0); m.ret(2, 0, 8, 2, h='/////', lw=1.0)
    m.pol([(-2, 0), (2, 0), (2, 2), (-2, 2)], fc='#ddebf7', lw=0.9)
    m.ret(-2.75, -1, 2.75, 0, fc='#ddebf7', lw=0.9); m.ret(-1.5, -6, 1.5, -1, fc='#ddebf7', lw=0.9)
    m.lin(-1.5, -6, -1.3, -6.6, lw=0.6); m.lin(1.5, -6, 1.3, -6.6, lw=0.6)
    m.txt(9, 1, 'tampa (TG-112)', fs=5.8, ha='left'); m.txt(3, -3.5, 'guia (TG-412)', fs=5.8, ha='left')
    m.txt(-8, 2.8, 'face externa', fs=5.5, ha='left')
    f.salvar()


# ------------------------------------------------------------------ DE-07 subconjunto do mecanismo
def de07():
    f = Folha(7, 'SC-01 / DE-07', 'Subconjunto do mecanismo (montagem)', 'ver lista de itens', '2:1', [
        'Montado no Posto 1 (plano macro). Braço (4) recebido do Posto 0 já com o ímã (5) colado no gabarito FD-01.',
        'Braço prensado no eixo do microatuador com batente: face superior do braço a 2,50 ±0,03 do plano dos pés (referência A).',
        'Característica crítica (CC): folga de 0,20 ±0,10 entre o ímã e a prateleira, na posição de soltar. Conferir com calibre não magnético.',
        'Teste de saída: giro de 90° com retorno e liberação do pino-padrão. Ferramentas não magnéticas.',
        'A tolerância da folga só será fixada depois do ensaio do campo.'], 'de07_mecanismo.png')
    k = 2
    v = Vista(f, 34, 116, k, 'Vista superior (ímã em repouso; em traço, na posição de soltar)', ty=78)
    v.ret(0, 12, 29.5, 30, lw=0.9); v.ret(27.5, 0, 29.5, 30, lw=0.9, fc='#dddddd'); v.ret(0, 28, 27.5, 30, lw=0.9, fc='#dddddd')
    v.cir(12, 21, 8.0, lw=0.9); v.cir(12, 21, 6.5, lw=0.9, fc='#b7bcc4'); v.cir(12, 21, 0.6, fc=K)
    v.ret(7, 0.75, 27.5, 9.25, lw=0.9, fc='#fbe5a3')
    v.lin(12, 5, -4, 5, lw=3.0); v.cir(-4, 5, 5, lw=0.9, fc='#c0504d')
    v.cir(12, 21, 5, lw=0.8, ls=TRAC, ec='#8c1c13'); v.lin(12, 5, 12, 21, lw=0.7, ls=TRAC)
    v.arco(12, 5, 16, 90, 180, lw=0.5)
    v.txt(0.5, 15.5, '90°', fs=6)
    v.ret(21, 22, 27, 28, lw=0.9, fc='#d9d9d9')
    v.centro(12, 5, 5); v.centro(12, 21, 10)
    v.corte(-11, 21, 34.5, 21, 'A')
    v.cv(5, 21, 29.5, 12, '16,00 ±0,05')
    v.balao(1, 2, 26, -12, 8); v.balao(2, 14.5, 23.5, 6, 20); v.balao(3, 22, 3, 22, -6)
    v.balao(4, 3, 5, -2, -14); v.balao(5, -6, 7, -12, 8); v.balao(6, 24, 25, 22, 8)
    # corte
    c = Vista(f, 162, 112, k, 'Corte A–A (ímã na posição de soltar)', ty=78)
    c.ret(27.5, 0, 29.5, 15.3, h='/////', lw=0.9)
    c.ret(0, 14.5, 27.5, 15.3, h='/////', lw=0.9)
    c.ret(4, 15.3, 5.475, 26.3, h='/////', lw=0.9); c.ret(18.525, 15.3, 20, 26.3, h='/////', lw=0.9)
    c.ret(21, 15.3, 27, 22.5, h='/////', lw=0.9); c.ret(21, 22.5, 27, 26.5, fc='#d9d9d9', lw=0.8)
    c.ret(5.5, 15.3, 18.5, 26.3, fc='#b7bcc4', lw=0.8)                       # embreagem
    c.pol([(8.5, 16.2), (15.5, 16.2), (14, 23.5), (10, 23.5)], fc='white', lw=0.7)
    c.cir(10.6, 22.4, 1.1, fc='white', lw=0.7); c.cir(13.4, 22.4, 1.1, fc='white', lw=0.7)
    c.ret(7, 2.5, 17, 14.3, fc='#c0504d', lw=0.9)                            # ímã Ø10 × 11,8 visível + cola
    c.ret(6, 0.5, 18, 2.5, h='\\\\\\\\\\', lw=0.9)                           # braço
    c.ret(7, 3.5, 27.5, 13.5, lw=0.6, ls=FANT)                               # microatuador ao fundo
    c.eixo(12, -3, 12, 30)
    c.lin(-4, 0, 33, 0, lw=0.4, c=COTA); ref_dado(c, 0, 0, 'A')
    c.cham(8, 14.4, -22, 10, 'folga 0,20 ±0,10  (CC)', ha='right')
    c.cv(0, 2.5, 29.5, 10, '2,50 ±0,03'); c.cv(0, 14.5, 29.5, 20, '14,50 ±0,05')
    c.cv(2.5, 14.3, 29.5, 30, '11,80 ±0,03')
    c.balao(2, 16, 20, 20, 10); c.balao(5, 9, 8, -16, -4); c.balao(4, 16.5, 1.5, 6, -12); c.balao(1, 2, 14.9, -14, -10); c.balao(3, 24, 8, -2, -22); c.balao(6, 24, 24.5, 14, 12)
    # lista
    ax = f.ax
    x0, y0 = 190, 52
    linhas = [('Nº', 'Código', 'Item', 'Qtd.'), ('1', 'TG-113', 'Suporte do mecanismo', '1'), ('2', 'TG-222', 'Embreagem de esferas', '1'),
              ('3', 'TG-311', 'Microatuador rotativo', '1'), ('4', 'TG-312', 'Braço dos ímãs', '1'),
              ('5', 'TG-313', 'Ímã Ø10 × 12, NdFeB', '1'), ('6', 'TG-512', 'Chave da garra', '1')]
    for i, l in enumerate(linhas):
        y = y0 + (len(linhas) - 1 - i) * 4.6
        ax.add_patch(Rectangle((x0, y), 91, 4.6, fc='white', ec=K, lw=0.5))
        for xx, s in zip((x0 + 4, x0 + 16, x0 + 48, x0 + 86), l):
            ax.text(xx, y + 2.2, s, ha='center', va='center', fontsize=6.2, fontweight='bold' if i == 0 else 'normal')
    f.salvar()


# ------------------------------------------------------------------ FD-01 gabarito de colagem
def fd01():
    f = Folha(8, 'FD-01', 'Gabarito de colagem do ímã no braço', 'Al 6061-T6 anodizado; pastilhas SAE 1020; pinos inox 304', '2:1 e 1:2', [
        'Dispositivo específico do Posto 0. Dez ninhos por placa (lote de colagem).',
        'Função: fixar em 11,80 ±0,03 a distância entre a face polar do ímã e a face do braço que apoia no gabarito.',
        '   A linha de adesivo (nominal 0,3 mm) absorve a variação de altura do ímã e de profundidade do alojamento.',
        'A pastilha de aço sob o ninho mantém o ímã assentado no fundo durante a cura. Furo Ø3 para a extração com pino de latão.',
        'Pino de posição com o perfil do furo do braço (duplo D). Tampa de pressão com êmbolos de mola de 5 N por braço.',
        'Aferição: calibre de profundidade a cada 500 ciclos; planicidade da face superior ≤ 0,02 mm.'], 'fd01_gabarito.png')
    k = 2
    c = Vista(f, 46, 112, k, 'Corte de um ninho, com o braço e o ímã em cura (2:1)', ty=44)
    # corpo: x de -12 a 44, y de -20 a 0 (face superior em y = 0)
    c.pol([(-12, -20), (44, -20), (44, 0), (21.05, 0), (21.05, -11.8), (10.95, -11.8), (10.95, 0), (-12, 0)], h='/////', lw=1.0)
    c.ret(12, -15.8, 20, -11.8 - 1.5, fc='#888888', lw=0.7, z=6)            # pastilha de aço
    c.ret(14.5, -20, 17.5, -15.8, fc='white', lw=0.7, z=6); c.ret(14.5, -13.3, 17.5, -11.8, fc='white', lw=0.7, z=7)
    c.ret(11, -11.8, 21, 0.2, fc='#c0504d', lw=0.9, z=7)                    # ímã Ø10 × 12
    c.pol([(-4, 0), (10.95, 0), (10.95, 0.5), (21.05, 0.5), (21.05, 0), (21.9, 0), (21.9, 2), (-4, 2)], fc='#bfbfbf', lw=0.9, z=6)  # braço invertido
    c.ret(11, 0.2, 21, 0.5, fc='#f2c94c', lw=0.3, z=8)                       # adesivo
    c.ret(-2, -8, 2, 2, fc='#dddddd', lw=0.8, z=7)                           # pino de posição
    c.ret(-12, 6, 44, 12, h='\\\\\\\\\\', lw=1.0)                            # tampa de pressão
    c.ret(6, 2, 10, 9, fc='#dddddd', lw=0.8, z=7); c.ret(14, 2, 18, 9, fc='#dddddd', lw=0.8, z=7)
    c.eixo(0, -22, 0, 14); c.eixo(16, -22, 16, 14)
    c.ch(0, 16, 12, 6, '16,00 ±0,02'); c.cv(-11.8, 0, 44, 20, '11,80 ±0,02')
    c.ch(10.95, 21.05, -20, -6, 'Ø10,10 +0,03/0'); c.cv(-20, 0, 44, 10, '20')
    c.balao(1, 36, -16, 46, -6); c.balao(2, 36, 9, 46, 6); c.balao(3, 8, 6, -22, 16); c.balao(4, 0, -6, -32, 2)
    c.balao(5, 3, 1, -40, 12); c.balao(6, 16, -6, 86, 14); c.balao(7, 16, 0.35, 86, 12.5); c.balao(8, 13, -14.5, -36, -8); c.balao(9, 16, -18.5, 40, -18)
    f.ax.text(150, 196, 'ITENS DO GABARITO', fontsize=7, fontweight='bold', va='top')
    f.ax.text(150, 191.5, '\n'.join(['1  corpo da placa (Al 6061-T6 anodizado)', '2  tampa de pressão', '3  êmbolo de mola, 5 N (2 por braço)',
              '4  pino de posição, perfil duplo D', '5  braço TG-312, com o alojamento para baixo', '6  ímã TG-313, com a face polar no fundo do ninho',
              '7  adesivo estrutural, 0,3 mm nominal', '8  pastilha de aço Ø8 × 2,5', '9  furo de extração Ø3']), fontsize=6.3, va='top', linespacing=1.4)
    quadro_gdt(c, 26, -6, '⏥', '0,02'); c.lin(30, 0, 30, -3.9, lw=0.4, c=COTA)
    # planta
    p = Vista(f, 186, 66, 0.5, 'Planta da placa, sem a tampa (1:2)', ty=52)
    p.cantos(0, 0, 170, 84, 4)
    for i in range(5):
        for j in range(2):
            x, y = 16 + i * 32, 22 + j * 40
            p.cir(x, y, 2.0, lw=0.7, fc='#dddddd'); p.cir(x + 16, y, 5.05, lw=0.8)
            p.pol([(x - 4, y - 4), (x + 16, y - 5.9), (x + 21.9, y - 5.9), (x + 21.9, y + 5.9), (x + 16, y + 5.9), (x - 4, y + 4)], lw=0.4, ls=TRAC)
    for (x, y) in ((6, 6), (164, 6), (6, 78), (164, 78)):
        p.cir(x, y, 2.5, lw=0.7)
    p.ch(0, 170, 84, 6, '170'); p.cv(0, 84, 170, 10, '84'); p.ch(16, 48, 0, -6, '32'); p.cv(22, 62, 0, -8, '40')
    p.cham(164, 6, -8, -10, '4 colunas-guia da tampa', ha='right')
    f.salvar()


if __name__ == '__main__':
    for fn in (de01, de02, de03, de04, de05, de06, de07, fd01):
        fn()
    print('ok')
