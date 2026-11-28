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
    """Chave fim de curso deitada no suporte do mecanismo. O fundo do gancho aperta a alavanca quando a garra fecha."""
    ch = M.CH
    yc, zp = ch['yc'], ch['z_placa']
    pcb = cubo(ch['x0'], yc - 6.85, zp, ch['x1'], yc + 6.85, zp + 1.6) - cil(ch['x0'] + 4, yc, zp - 1, zp + 3, 3.0)
    corpo = cubo(176.5, yc - 3.35, zp + 1.6, 189.5, yc + 3.35, zp + 6.8)
    botao = cubo(179.0, yc - 1.0, zp + 6.8, 180.6, yc + 1.0, zp + 7.4)
    alav = Manifold.batch_hull([cubo(186.0, yc - 1.4, zp + 6.8, 187.0, yc + 1.4, zp + 7.2), cubo(173.0, yc - 1.4, 41.6, 174.0, yc + 1.4, 42.0)])
    base_pin = cubo(189.6, yc - 3.8, zp - 2.5, 192.1, yc + 3.8, zp)
    pinos = uniao([cubo(190.53, yc - 2.54 + j * 2.54 - 0.32, zp - 8.5, 191.17, yc - 2.54 + j * 2.54 + 0.32, zp - 2.5) for j in range(3)])
    led = cubo(170.0, yc + 3.5, zp + 1.6, 172.0, yc + 5.0, zp + 2.4)
    return [(c, C.P(m)) for c, m in (('#1d4ed8', pcb), ('#111827', corpo + base_pin), ('#ef4444', botao), ('#cbd5e1', alav), ('#d4a017', pinos), ('#f87171', led))]


def chave_a_fios():
    """Só OUT e GND: o ESP32 usa o pull-up interno, o pino nunca recebe 5 V. Pinos da chave: VCC, GND, OUT."""
    ch = M.CH
    yc, zp = ch['yc'], ch['z_placa']
    out = []
    for j, cor, fl in ((1, '#111827', 'G'), (2, '#38bdf8', 'S')):
        xs, ys, zs = C.P_pt(190.85, yc - 2.54 + j * 2.54, zp - 8.5)
        out.append(('#111827', cubo(xs - 1.25, ys - 1.25, zs - 8, xs + 1.25, ys + 1.25, zs + 6)))
        px, py, pz = pino(27, fl)
        zc = pz - 6 + Z_CAPA
        out.append(('#111827', capa(px, py, pz)))
        pts = [(xs, ys, zs - 8), (xs, ys, zs - 12), (xs + 8, 2.6 + j * 0.9, zs - 13), (px - 8, 2.6 + j * 0.9, zc + 12), (px, py, zc + 6), (px, py, zc)]
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
        pts = [a, c, (c[0] + 6, 3.3 + dy, c[2] + 2), (xs - 14, 3.3 + dy, zs + 12), (xs, yy, zs - 6 + Z_CAPA + 6), (xs, yy, zs - 6 + Z_CAPA)]
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
    """Cabo de celular USB-A -> micro-USB (o que vem com o power bank serve): power bank -> micro-USB do expansor.
    O expansor alimenta o ESP32 e o 5 V do servo."""
    pb = C.POS_PB
    yc = (pb[1] + pb[3]) / 2 + 18
    plugue = cubo(pb[0] - 26, yc - 8, C.QI_E + 3.5, pb[0] + 0.5, yc + 8, C.QI_E + 11.5)
    e = layout_esp()
    xu, yu, zu = e['x0'] - 1.0, e['y0'] + 24.0, e['zt'] + 1.5
    micro = cubo(xu - 18, yu - 5.0, zu - 3.2, xu, yu + 5.0, zu + 3.2)
    fc = C.FURO_CABO
    pts = [(pb[0] - 26, yc, C.QI_E + 7.5), (pb[0] - 33, yc, 12), (fc[0] + 12, fc[3] - 6, C.Z_PRAT - 2), (fc[0] + 12, fc[3] - 6, C.ZS + 5),
           (fc[0] + 20, 80, C.ZS + 5), (118, 80, C.ZS + 5), (xu - 30, 78, zu), (xu - 30, yu, zu), (xu - 18, yu, zu)]
    return [('#111827', plugue + micro), ('#1f2937', tubo(pts, 3.6))]
