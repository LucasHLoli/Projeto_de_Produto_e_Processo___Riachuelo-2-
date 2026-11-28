"""Ligações reais do protótipo v3: posição de cada pino do expansor, jumpers, cabo do servo,
capacitor, semáforo em cima da tampa, chave e cabo USB.

Pinagem DOIT ESP32 DevKit V1 (30 pinos), fileira esquerda, a partir da ponta da antena:
EN, VP(36), VN(39), 34, 35, 32, 33, 25, 26, 27, 14, 12, 13, GND, VIN  -> índice 0..14
"""
from manifold3d import Manifold
import tagandgo_v2 as M
import tagandgo_v3 as C
from tagandgo_v2 import cubo, cil, uniao
from comprados_detalhados import tubo, esfera

IDX_ESQ = {32: 5, 33: 6, 25: 7, 26: 8, 27: 9, 14: 10, 12: 11, 13: 12}
LIGACOES = [  # (peça, fio, GPIO, fileira do expansor)
    ('Servo SG90', 'laranja (sinal)', 13, 'S'), ('Servo SG90', 'vermelho (5 V)', 13, 'V'), ('Servo SG90', 'marrom (GND)', 13, 'G'),
    ('Chave fim de curso', 'OUT', 27, 'S'), ('Chave fim de curso', 'GND', 27, 'G'), ('Chave fim de curso', 'VCC', None, 'não ligar'),
    ('Semáforo', 'R (vermelho)', 26, 'S'), ('Semáforo', 'Y (amarelo)', 33, 'S'), ('Semáforo', 'G (verde)', 25, 'S'),
    ('Semáforo', 'GND', 26, 'G'),
    ('Capacitor 1000 µF', '+ (perna longa)', 12, 'V'), ('Capacitor 1000 µF', '− (lado da faixa)', 12, 'G')]
Z_CAPA = 14.0


def layout_esp():
    x0, y0 = C.POS_ESP[0] + 0.5, C.POS_ESP[1] + 0.5
    L, W = M.EXP
    zt = C.ZS + 2.0 + 1.6
    ex0, ey0 = x0 + (L - 51.6) / 2 + 3.0, y0 + (W - 28.3) / 2
    return dict(x0=x0, y0=y0, zt=zt, ex0=ex0, yc=ey0 + 28.3 / 2)


def pino(gpio, fila):
    """Centro do pino macho S/V/G do expansor (lado esquerdo do ESP32) e altura do topo do pino."""
    e = layout_esp()
    i = 14 - IDX_ESQ[gpio]
    x = e['ex0'] + 9.32 + i * 2.54
    k = 'SVG'.index(fila)
    y = e['yc'] - (12.7 + 4.0 + k * 2.54)
    return x, y, e['zt'] + 8.5


def capa(x, y, ztopo):
    return cubo(x - 1.25, y - 1.25, ztopo - 6.0, x + 1.25, y + 1.25, ztopo - 6.0 + Z_CAPA)


def fio(pts, cor, d=1.4):
    return (cor, tubo(pts, d))


def semaforo(tz):
    """Semáforo parafusado EM CIMA da tampa, LEDs para cima; os 4 pinos saem pela ponta (lado -x)."""
    x0, y0 = C.POS_SEM
    L, W, _ = M.SEMAFORO
    pcb = cubo(x0, y0, tz + 0.01, x0 + L, y0 + W, tz + 1.6)
    for hx, hy in C.SEM_FUROS:
        pcb = pcb - cil(hx, hy, tz - 1, tz + 3, 3.0)
    paraf = uniao([cil(hx, hy, tz + 1.6, tz + 3.4, 5.4) for hx, hy in C.SEM_FUROS])
    leds = []
    for k, cor in enumerate(('#ef4444', '#facc15', '#22c55e')):
        cx = x0 + L / 2 + (k - 1) * 12.5
        cy = y0 + W / 2
        dome = esfera(cx, cy, tz + 7.0, 8.0) ^ cubo(cx - 5, cy - 5, tz + 7.0, cx + 5, cy + 5, tz + 11.0)
        leds.append((cor, cil(cx, cy, tz + 1.6, tz + 7.0, 8.0) + dome))
    base_pin = cubo(x0 - 2.5, y0 + W / 2 - 5.1, tz + 0.01, x0, y0 + W / 2 + 5.1, tz + 2.5)
    pinos = uniao([cubo(x0 - 8.5, y0 + W / 2 - 3.81 + j * 2.54 - 0.32, tz + 0.93, x0 - 2.5, y0 + W / 2 - 3.81 + j * 2.54 + 0.32, tz + 1.57) for j in range(4)])
    return [('#0f172a', pcb), ('#111827', base_pin), ('#d4a017', pinos), ('#94a3b8', paraf)] + leds


def semaforo_fios(tz):
    x0, y0 = C.POS_SEM
    W = M.SEMAFORO[1]
    alvo = [('#111827', 26, 'G'), ('#ef4444', 26, 'S'), ('#eab308', 33, 'S'), ('#22c55e', 25, 'S')]   # GND, R, Y, G
    xr = (C.SEM_RASGO[0] + C.SEM_RASGO[2]) / 2
    out = []
    for j, (cor, gp, fl) in enumerate(alvo):
        yp = y0 + W / 2 - 3.81 + j * 2.54
        out.append(('#111827', cubo(x0 - 8.5 - 9, yp - 1.25, tz + 0.05, x0 - 6.0, yp + 1.25, tz + 2.55)))
        px, py, pz = pino(gp, fl)
        zc = pz - 6 + Z_CAPA
        out.append(('#111827', capa(px, py, pz)))
        pts = [(x0 - 17.5, yp, tz + 1.3), (xr, yp, tz + 1.3), (xr, yp, C.H - 6), (xr + 4, 82 - j * 1.4, C.H - 9),
               (px - 6, 82 - j * 1.4, C.H - 10), (px, py, zc + 10), (px, py, zc)]
        out.append(fio(pts, cor))
    return out


def chave_a():
    px, py, _ = C.P_pt(*M.PLUNGER, 0)
    z1 = C.H - 4.5
    x0, y0 = px - 18.5, py - 6.85
    pcb = cubo(x0, y0, z1 - 7.6, x0 + 25, y0 + 13.7, z1 - 6.0)
    sw = cubo(x0 + 6, y0 + 3.5, z1 - 6.0, x0 + 19, y0 + 10.2, z1 - 0.8)
    alav = Manifold.batch_hull([cubo(x0 + 7, y0 + 5.5, z1 - 1.0, x0 + 8, y0 + 8.2, z1 - 0.6), cubo(px - 0.5, y0 + 5.5, z1 - 0.2, px + 1.5, y0 + 8.2, z1 + 0.2)])
    pinos = uniao([cubo(x0 + 1.2, y0 + 4.3 + j * 2.54 - 0.32, z1 - 7.6 - 6, x0 + 1.84, y0 + 4.3 + j * 2.54 + 0.32, z1 - 7.6) for j in range(3)])
    base_pin = cubo(x0 + 0.27, y0 + 3.0, z1 - 7.6 - 2.5, x0 + 2.77, y0 + 10.9, z1 - 7.6)
    return [('#1d4ed8', pcb), ('#111827', sw + base_pin), ('#cbd5e1', alav), ('#d4a017', pinos)]


def chave_a_fios():
    """Só OUT e GND: o ESP32 usa o pull-up interno, o pino nunca recebe 5 V."""
    px0, py0, _ = C.P_pt(*M.PLUNGER, 0)
    z1 = C.H - 4.5
    x0, y0 = px0 - 18.5, py0 - 6.85
    out = []
    for j, cor, fl in ((1, '#111827', 'G'), (2, '#38bdf8', 'S')):     # pinos da chave: VCC(0, livre), GND(1), OUT(2)
        xs, ys, zs = x0 + 1.52, y0 + 4.3 + j * 2.54, z1 - 7.6 - 6
        out.append(('#111827', cubo(xs - 1.25, ys - 1.25, zs - 8, xs + 1.25, ys + 1.25, zs + 6)))
        px, py, pz = pino(27, fl)
        zc = pz - 6 + Z_CAPA
        out.append(('#111827', capa(px, py, pz)))
        pts = [(xs, ys, zs - 8), (xs, ys, zs - 12), (xs + 6, 4 + j, zs - 13), (px - 6, 4 + j, zc + 12), (px, py, zc + 6), (px, py, zc)]
        out.append(fio(pts, cor))
    return out


def servo_cabo():
    """Cabo do servo com o conector de 3 vias encaixado direto na coluna S/V/G do GPIO 13."""
    s = M.SERVO
    zb = M.Z_ORELHA - 15.9
    bx1 = M.SX - s['eixo_ponta'] + 22.7
    xs, ys, zs = pino(13, 'S')
    _, yv, _ = pino(13, 'V')
    _, yg, _ = pino(13, 'G')
    out = [('#111827', cubo(xs - 1.4, min(ys, yg) - 1.4, zs - 6, xs + 1.4, max(ys, yg) + 1.4, zs - 6 + Z_CAPA))]
    for cor, dy, yy in (('#7c2d12', -1.3, yg), ('#dc2626', 0.0, yv), ('#f97316', 1.3, ys)):
        a = C.P_pt(bx1, M.SY + dy, zb + 1.5)
        c = C.P_pt(bx1 + 11, M.SY + dy, zb + 1.5)
        pts = [a, c, (c[0] + 8, 5.5 + dy, c[2] + 2), (xs - 14, 5.5 + dy, zs + 12), (xs, yy, zs - 6 + Z_CAPA + 6), (xs, yy, zs - 6 + Z_CAPA)]
        out.append(fio(pts, cor, 1.2))
    return out


def capacitor():
    """1000 µF 16 V deitado na prateleira, com 2 jumpers fêmea no V e no G da coluna do GPIO 12."""
    e = layout_esp()
    cx0, cy, cz = e['x0'] + 2, 79.5, C.ZS + 5.2
    corpo = Manifold.cylinder(20, 5, 5, 32).rotate([0, 90, 0]).translate([cx0, cy, cz])
    faixa = corpo ^ cubo(cx0, cy - 6, cz + 2.6, cx0 + 20, cy + 6, cz + 6)
    out = [('#1e3a8a', corpo - faixa), ('#e5e7eb', faixa)]
    for j, cor, fl in ((0, '#dc2626', 'V'), (1, '#111827', 'G')):
        ly = cy - 2.5 + j * 5
        out.append(('#cbd5e1', Manifold.cylinder(4, 0.3, 0.3, 8).rotate([0, 90, 0]).translate([cx0 + 20, ly, cz])))
        out.append(('#111827', cubo(cx0 + 22, ly - 1.25, cz - 1.25, cx0 + 36, ly + 1.25, cz + 1.25)))
        px, py, pz = pino(12, fl)
        zc = pz - 6 + Z_CAPA
        out.append(('#111827', capa(px, py, pz)))
        pts = [(cx0 + 36, ly, cz), (cx0 + 42, ly, cz + 4), (px + 3, 73 - j * 1.6, zc + 12), (px, py, zc + 6), (px, py, zc)]
        out.append(fio(pts, cor))
    return out


def cabo_usb():
    """Power bank (USB-A) até o USB-C do expansor. O expansor alimenta o ESP32 e o 5 V do servo."""
    pb = C.POS_PB
    yc = (pb[1] + pb[3]) / 2 + 18
    plugue = cubo(pb[0] - 26, yc - 8, C.QI_E + 3.5, pb[0] + 0.5, yc + 8, C.QI_E + 11.5)
    e = layout_esp()
    xu, yu, zu = e['x0'] - 1.0, e['y0'] + 37.5, e['zt'] + 1.6
    usbc = cubo(xu - 22, yu - 4.2, zu - 3.2, xu, yu + 4.2, zu + 3.2)
    fc = C.FURO_CABO
    pts = [(pb[0] - 26, yc, C.QI_E + 7.5), (pb[0] - 33, yc, 12), (fc[0] + 12, fc[3] - 6, C.Z_PRAT - 2), (fc[0] + 12, fc[3] - 6, C.ZS + 5),
           (fc[0] + 20, 80, C.ZS + 5), (118, 80, C.ZS + 5), (xu - 30, 78, zu), (xu - 30, yu, zu), (xu - 22, yu, zu)]
    return [('#111827', plugue + usbc), ('#1f2937', tubo(pts, 3.6))]
