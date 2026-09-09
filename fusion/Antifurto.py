# -*- coding: utf-8 -*-
"""
DISPOSITIVO ANTIFURTO Tag&Go
Projeto de Produto e Processo | Escola Politecnica da USP

RODAR:  Shift+S -> aba Scripts -> Antifurto -> Run

=============================================================================
O FLUXO
=============================================================================
  1. o cliente aponta o CELULAR para o QR IMPRESSO no dispositivo
  2. o app abre a peca e o cliente PAGA
  3. o backend assina um token e devolve ao app
  4. o app entrega o token ao dispositivo por BLUETOOTH (BLE)
  5. o dispositivo confere a assinatura -> LED VERMELHO passa a VERDE
  6. o cliente aperta o BOTAO
  7. o atuador move o cursor, a garra abre, o PINO SOLTA

O BLE ja esta dentro do ESP32-C3 - nao e' peca nova. O celular fala direto
com o dispositivo: se a internet da loja cair depois do pagamento, a
liberacao ainda funciona.

=============================================================================
COMO A CAMISA ENTRA
=============================================================================
      [ CARCACA SUPERIOR ]   <- QR impresso, LED, botao
      [ CARCACA INFERIOR ]   <- garra, mecanismo, eletronica
  Z=0 #####################  <- face inferior + contatos de recarga
      ==== TECIDO ====       <- A CAMISA, prensada aqui
        (disco do pino)      <- POR BAIXO do tecido

  A haste sobe do disco, atravessa o tecido, entra pelo furo e a garra agarra.
  O tecido fica preso entre a face inferior e o disco.

=============================================================================
TRES CHAVES  <<<<<  as unicas linhas que voce precisa trocar
=============================================================================
"""

import adsk.core
import adsk.fusion
import traceback
import math

MECANISMO   = 'came'        # came | fuso | solenoide | sma | eletroima
MODO_ESPERA = 'botao'       # botao (6,8 anos) | anuncio (41 dias)
RECARGA     = 'contatos'    # contatos (bandeja) | usb (recorte lateral)

MM = 0.1
MU = 0.30                   # atrito PETG-aco, ESTIMADO - medir na bancada


# ============================================================================
# CARCACA
# ============================================================================

P = {
    'larg':          98.0,
    'prof':          82.0,
    'alt':           26.0,
    't_parede':       2.4,
    'z_split':       13.0,
    'r_canto':        8.0,
    'r_topo':         3.0,
    'folga':          0.6,
}

PAR = {
    'd_torre':    7.0, 'd_inserto': 3.2, 'h_inserto': 4.0,
    'd_passante': 2.4, 'd_cabeca':  4.2, 'h_cabeca':  2.0,
}
FUROS = [(-43.0, -35.0), (43.0, -35.0), (-43.0, 35.0), (43.0, 35.0)]

# ============================================================================
# GARRA, PINO E TECIDO - COMPRADOS (canibalizados da hard tag)
# ============================================================================

GARRA = {'diam': 12.4, 'alt': 10.0, 'curso': 1.2, 'forca': 2.5}   # [MEDIR]
PINO  = {'d_cabeca': 14.0, 't_cabeca': 1.2, 'd_haste': 2.0,
         'h_haste': 16.0, 'folga': 0.4}
TECIDO = {'esp': 1.0, 'lado': 70.0}

XY_GARRA = (-25.0, -17.0)

CUR   = {'larg': 14.0, 'prof': 26.0, 't_fino': 2.0, 'w_garfo': 3.6, 'folga': 0.6}
BUCHA = {'d_ext': 7.0, 'alt': 2.0}

# ============================================================================
# ATUADORES
# ============================================================================

MEC = {
    'came': {
        'nome': 'Servo MG90S + braco',
        'peca': (22.8, 28.5, 12.2), 'custo': 24.0,
        'forca': 36.0, 'curso': 8.0, 'tempo': 0.4, 'braco': 20.0,
        'busca': 'servo motor mg90s micro metal 9g',
        'risco': 'pico de ~700 mA ao mover - capacitor de 1000 uF junto',
    },
    'fuso': {
        'nome': 'Micromotor N20 + fuso M3',
        'peca': (12.0, 26.0, 10.0), 'custo': 30.0,
        'forca': 40.0, 'curso': 5.0, 'tempo': 1.6, 'braco': 0.0,
        'busca': 'micro motor n20 6v caixa reducao com fuso',
        'risco': 'precisa de fim de curso nos DOIS extremos, senao queima',
    },
    'solenoide': {
        'nome': 'Solenoide push 5V',
        'peca': (15.0, 30.0, 12.0), 'custo': 25.0,
        'forca': 5.0, 'curso': 4.0, 'tempo': 0.1, 'braco': 0.0,
        'busca': 'mini solenoide push pull 5v 10mm',
        'risco': 'forca cai muito com o curso; nao pode ficar energizado',
    },
    'sma': {
        'nome': '2 fios de nitinol + rampa',
        'peca': (6.0, 44.0, 2.0), 'custo': 40.0,
        'forca': 6.4, 'curso': 1.68, 'tempo': 1.5, 'braco': 0.0,
        'busca': 'fio nitinol flexinol 0.15mm memoria de forma',
        'risco': 'ciclo lento - ~10 s para esfriar e rearmar',
    },
    'eletroima': {
        'nome': 'Eletroima na gaiola (SEM cursor)',
        'peca': (25.0, 25.0, 15.0), 'custo': 35.0,
        'forca': 3.0, 'curso': 0.0, 'tempo': 0.1, 'braco': 0.0,
        'busca': 'eletroima 5v 25mm solenoide eletromagnetico',
        'risco': 'RISCO ALTO: forca cai com o QUADRADO do entreferro',
    },
}

# O braco do servo GIRA: a ponta anda PERPENDICULAR ao braco. Para empurrar o
# cursor em -Y, o braco tem de apontar em -X. Isso fixa onde o servo mora.
Y_FRENTE_CURSOR = XY_GARRA[1] + CUR['prof'] / 2.0
XY_ATUADOR = {
    'came':      (XY_GARRA[0] + MEC['came']['braco'], Y_FRENTE_CURSOR + 1.0),
    'fuso':      (XY_GARRA[0], Y_FRENTE_CURSOR + 20.0),
    'solenoide': (XY_GARRA[0], Y_FRENTE_CURSOR + 22.0),
    'sma':       (XY_GARRA[0], Y_FRENTE_CURSOR + 20.0),
    'eletroima': XY_GARRA,
}

# ============================================================================
# ELETRONICA - envelope (X, Y, Z) e posicao (x, y, z_base)
# ============================================================================

COMP = {
    'mcu':      (22.5, 18.0,  4.0),   # ESP32-C3 Super Mini - o BLE esta aqui
    'bateria':  (30.0, 20.0,  5.5),   # LiPo 502030 ~300 mAh
    'carga':    (26.0, 17.0,  4.0),   # TP4056 USB-C
    'botao':    (12.0, 12.0,  7.0),   # chave tactil 12 mm
}
POS = {
    'bateria':  ( 30.0, -19.0,  2.9),
    'carga':    ( 30.0, -19.0,  9.4),   # EMPILHADO sobre a bateria
    'mcu':      ( 30.0,  17.0,  2.9),
    'botao':    ( -2.0, -30.0, 16.6),
}

ENERGIA = {
    'capacidade': 300.0,  'i_sleep': 0.005,
    'i_anuncio':   30.0,  't_anuncio': 0.010, 'periodo': 1.0,
    'i_atuacao':  700.0,
}

# ============================================================================
# PAINEL E RECARGA
# ============================================================================

UI = {
    'qr':          (28.0, 28.0,  -2.0,   6.0),   # QR IMPRESSO - o celular le
    'xy_led':      (-14.0, -30.0),
    'xy_botao':    ( -2.0, -30.0),
    'furo_led':      5.0,
    'furo_botao':   12.5,
    'prof_rebaixo':  0.5,
}

REC = {
    'd_pad':     6.5,    # rebaixo do contato na face inferior
    'prof_pad':  0.6,
    'd_fio':     2.0,
    'xy_pads':   [(5.0, -14.0), (5.0, 14.0)],
    'usb_larg':  9.5,    # recorte para o USB-C do TP4056
    'usb_alt':   4.0,
}


# ============================================================================
# ANALISE
# ============================================================================

def analisar(chave):
    m = MEC[chave]
    if chave == 'eletroima':
        return {'ang': 0.0, 'ganho': 1.0, 'efic': 1.0, 'saida': m['forca'],
                'margem': m['forca'] / GARRA['forca'], 'autotrava': False,
                'usa_cursor': False}
    ang = math.degrees(math.atan2(GARRA['curso'], m['curso']))
    phi = math.degrees(math.atan(MU))
    efic = math.tan(math.radians(ang)) / math.tan(math.radians(ang + phi))
    ganho = 1.0 / math.tan(math.radians(ang))
    saida = m['forca'] * ganho * efic
    return {'ang': ang, 'ganho': ganho, 'efic': efic, 'saida': saida,
            'margem': saida / GARRA['forca'],
            'autotrava': math.tan(math.radians(ang)) <= MU, 'usa_cursor': True}


def autonomia():
    E = ENERGIA
    if MODO_ESPERA == 'anuncio':
        med = E['i_sleep'] + E['i_anuncio'] * (E['t_anuncio'] / E['periodo'])
    else:
        med = E['i_sleep']
    por_lib = E['i_atuacao'] * MEC[MECANISMO]['tempo'] / 3600.0
    h = E['capacidade'] / med
    return {'media': med, 'horas': h, 'dias': h / 24.0, 'anos': h / 8760.0,
            'por_lib': por_lib, 'n_lib': E['capacidade'] / por_lib}


def arco_braco():
    """Angulo que o braco varre para dar o curso do atuador."""
    b = MEC[MECANISMO]['braco']
    if b <= 0:
        return 0.0
    return math.degrees(2.0 * math.asin(min(1.0, MEC[MECANISMO]['curso'] / (2.0 * b))))


def tabela():
    L = ["  %-10s %7s %7s %6s %6s %9s %6s %5s" %
         ('mecanismo', 'F_saida', 'margem', 'rampa', 'efic', 'autotrav', 't(s)', 'R$')]
    for k in ('came', 'fuso', 'solenoide', 'sma', 'eletroima'):
        a = analisar(k)
        L.append("  %-10s %6.1fN %6.1fx %5.1fg %6.2f %9s %6.1f %5.0f%s" % (
            k, a['saida'], a['margem'], a['ang'], a['efic'],
            'SIM' if a['autotrava'] else 'nao', MEC[k]['tempo'], MEC[k]['custo'],
            '  <<<' if k == MECANISMO else ''))
    return L


def bom():
    """Lista de compras - termos como se digita no Mercado Livre."""
    itens = [
        ('etiqueta antifurto rigida mini tag com pino 100un', 1, 170.0,
         'garra + pino: canibalizar. Compre 100, vai quebrar varias'),
        ('esp32 c3 super mini placa desenvolvimento', 2, 25.0,
         'controle + BLE. Duas: uma queima na semana da entrega'),
        ('bateria lipo 502030 300mah 3.7v com conector', 2, 22.0,
         'alimentacao'),
        ('modulo carregador tp4056 usb-c com protecao', 2, 9.0,
         'recarga e protecao da celula'),
        ('led rgb 5mm catodo comum difuso', 10, 1.0,
         'vermelho -> verde'),
        ('chave tactil push button 12x12x7 com capa', 10, 1.5,
         'botao de liberacao'),
        ('mosfet irlz44n canal n logic level to-220', 3, 6.0,
         'driver do atuador. NAO usar IRF520'),
        ('capacitor eletrolitico 1000uf 25v', 5, 2.5,
         'anti-brownout - o item de R$3 que decide se funciona'),
        ('filamento petg 1kg', 1, 130.0,
         'carcaca, bucha, cursor, braco'),
        ('inserto rosca m2 latao termico kit', 1, 25.0,
         'fechamento'),
        ('parafuso m2 8mm philips inox kit', 1, 15.0,
         'fechamento'),
    ]
    if RECARGA == 'contatos':
        itens.append(('pino pogo contato mola 2mm kit', 1, 20.0,
                      'contatos da bandeja de recarga'))
    itens.append((MEC[MECANISMO]['busca'], 2, MEC[MECANISMO]['custo'],
                  'ATUADOR do mecanismo escolhido'))
    return itens


# ============================================================================
# VERIFICACOES
# ============================================================================

def z_base_garra():
    if MECANISMO == 'eletroima':
        return P['t_parede'] + MEC['eletroima']['peca'][2] + 1.0
    return P['t_parede']


def envelopes():
    E = []
    for n in POS:
        x, y, z = POS[n]
        lx, ly, lz = COMP[n]
        E.append((n, lx, ly, lz, x, y, z))
    gx, gy = XY_GARRA
    E.append(('garra', GARRA['diam'], GARRA['diam'], GARRA['alt'], gx, gy, z_base_garra()))
    a = analisar(MECANISMO)
    if a['usa_cursor']:
        z = z_base_garra() + GARRA['alt'] + BUCHA['alt']
        # o cursor RECUA: o envelope inclui o curso, senao a colisao passa batido
        E.append(('cursor', CUR['larg'], CUR['prof'] + MEC[MECANISMO]['curso'],
                  CUR['t_fino'] + GARRA['curso'], gx,
                  gy - MEC[MECANISMO]['curso'] / 2.0, z))
    sx, sy = XY_ATUADOR[MECANISMO]
    lx, ly, lz = MEC[MECANISMO]['peca']
    if MECANISMO not in ('eletroima', 'sma'):
        E.append(('atuador', lx, ly, lz, sx, sy, P['t_parede'] + 0.5))
    return E


def verificar():
    erros, avisos = [], []
    f = P['folga']
    ix, iy = P['larg'] - 2 * P['t_parede'], P['prof'] - 2 * P['t_parede']
    teto = P['alt'] - P['t_parede']

    if MECANISMO not in MEC:
        return ["MECANISMO '%s' nao existe." % MECANISMO], [], None
    a = analisar(MECANISMO)
    E = envelopes()

    for n, lx, ly, lz, x, y, z in E:
        if x - lx / 2 < -ix / 2 or x + lx / 2 > ix / 2:
            erros.append("%s sai da carcaca em X." % n)
        if y - ly / 2 < -iy / 2 or y + ly / 2 > iy / 2:
            erros.append("%s sai da carcaca em Y." % n)
        if z + lz > teto:
            erros.append("%s vai ate Z=%.1f e o teto interno esta em %.1f. "
                         "Aumente alt para %.1f." % (n, z + lz, teto,
                                                     P['alt'] + z + lz - teto))

    for i in range(len(E)):
        for j in range(i + 1, len(E)):
            A, B = E[i], E[j]
            dx = abs(A[4] - B[4]) - (A[1] + B[1]) / 2.0 - 2 * f
            dy = abs(A[5] - B[5]) - (A[2] + B[2]) / 2.0 - 2 * f
            dz = abs((A[6] + A[3] / 2.0) - (B[6] + B[3] / 2.0)) - (A[3] + B[3]) / 2.0 - f
            if dx < 0 and dy < 0 and dz < 0:
                erros.append("%s e %s se sobrepoem (%.1f X, %.1f Y, %.1f Z)."
                             % (A[0], B[0], -dx, -dy, -dz))

    for fx, fy in FUROS:
        if abs(fx) + PAR['d_torre'] / 2 > ix / 2 or abs(fy) + PAR['d_torre'] / 2 > iy / 2:
            erros.append("Torre em (%+.0f, %+.0f) fura a parede." % (fx, fy))
        for n, lx, ly, lz, x, y, z in E:
            if abs(fx - x) - (PAR['d_torre'] + lx) / 2 - f < 0 and \
               abs(fy - y) - (PAR['d_torre'] + ly) / 2 - f < 0:
                erros.append("Torre em (%+.0f, %+.0f) bate em %s." % (fx, fy, n))

    # VOLUME VARRIDO do braco: um bloco-envelope nao pega isso
    if MEC[MECANISMO]['braco'] > 0:
        sx, sy = XY_ATUADOR[MECANISMO]
        R = MEC[MECANISMO]['braco']
        z_arco = z_base_garra() + GARRA['alt'] + BUCHA['alt']
        for n, lx, ly, lz, x, y, z in E:
            if n in ('atuador', 'cursor'):
                continue
            if abs((z + lz / 2.0) - z_arco) > 6.0:
                continue
            if math.hypot(x - sx, y - sy) < R + max(lx, ly) / 2.0:
                erros.append("O braco do servo varre sobre %s. Um envelope de caixa\n"
                             "  nao pegaria isso - so o volume varrido pega." % n)

    if MECANISMO == 'sma':
        gy = XY_GARRA[1]
        disp = (gy - CUR['prof'] / 2.0) - (-iy / 2.0 + 4.0)
        need = MEC['sma']['curso'] / 0.04
        if disp < need:
            msg = [
                'O fio SMA precisa de %.0f mm RETOS atras do cursor e so ha %.0f mm.' % (need, disp),
                '  O fio contrai 4%% do comprimento.',
                '  Solucoes: (a) prof para %.0f mm, (b) girar o mecanismo para o cursor' % (P['prof'] + need - disp),
                '  correr em X (ha %.0f mm), ou (c) trocar de mecanismo.' % ix,
                '  NAO desviar em poste: cada volta de 180 graus custa ~1,9x de forca.',
            ]
            erros.append(chr(10).join(msg))

    z_ponta = PINO['h_haste'] - TECIDO['esp']
    if z_ponta > teto:
        erros.append("A ponta do pino chega a Z=%.1f e o teto esta em %.1f."
                     % (z_ponta, teto))

    if a['margem'] < 1.5:
        avisos.append("Margem de forca de apenas %.2fx (alvo >= 1,5x)." % a['margem'])
    if a['autotrava'] and a['usa_cursor']:
        avisos.append("Rampa de %.1f graus com mu=%.2f: AUTOTRAVANTE.\n"
                      "  Segura sem energia, mas PRECISA de mola de retorno."
                      % (a['ang'], MU))
    if MODO_ESPERA == 'anuncio':
        au = autonomia()
        avisos.append("Com anuncio BLE continuo a bateria dura %.0f dias.\n"
                      "  Se a etiqueta morrer na arara, o cliente paga e NAO libera.\n"
                      "  MODO_ESPERA='botao' leva isso para %.1f anos."
                      % (au['dias'], ENERGIA['capacidade'] / ENERGIA['i_sleep'] / 8760.0))
    if RECARGA == 'usb':
        avisos.append("Com USB-C, cada etiqueta e' plugada a mao. Numa loja com\n"
                      "  milhares delas isso nao escala. RECARGA='contatos' permite\n"
                      "  empilhar numa bandeja e carregar todas de uma vez.")
    avisos.append("QR impresso de %.0f mm de lado: teste a leitura a 20 cm com um\n"
                  "  celular de camera fraca - e' o pior caso da loja." % UI['qr'][0])
    return erros, avisos, a


# ============================================================================
# UTILITARIOS
# ============================================================================

NOVO  = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
CORTE = adsk.fusion.FeatureOperations.CutFeatureOperation
JUNTA = adsk.fusion.FeatureOperations.JoinFeatureOperation


def pt(x, y, z=0.0):
    return adsk.core.Point3D.create(x * MM, y * MM, z * MM)


def vr(mm):
    return adsk.core.ValueInput.createByReal(mm * MM)


def corpo(root, nome):
    for b in root.bRepBodies:
        if b.name == nome:
            return b
    raise RuntimeError('corpo nao encontrado: ' + nome)


def plano_z(root, z, nome):
    pl = root.constructionPlanes
    pi = pl.createInput()
    pi.setByOffset(root.xYConstructionPlane, vr(z))
    p = pl.add(pi)
    p.name = nome
    return p


def todos_perfis(sk):
    col = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        col.add(sk.profiles.item(i))
    return col


def perfil_maior(sk):
    melhor, area = None, -1.0
    for i in range(sk.profiles.count):
        pr = sk.profiles.item(i)
        ar = pr.areaProperties().area
        if ar > area:
            melhor, area = pr, ar
    col = adsk.core.ObjectCollection.create()
    col.add(melhor)
    return col


def retangulo(sk, cx, cy, lx, ly):
    return sk.sketchCurves.sketchLines.addTwoPointRectangle(
        pt(cx - lx / 2.0, cy - ly / 2.0), pt(cx + lx / 2.0, cy + ly / 2.0))


def poligono(sk, pts):
    ln = sk.sketchCurves.sketchLines
    for i in range(len(pts)):
        A, B = pts[i], pts[(i + 1) % len(pts)]
        ln.addByTwoPoints(pt(A[0], A[1]), pt(B[0], B[1]))


def extrudar(root, perfis, alvo, dist, op, nome=None):
    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfis, op)
    if alvo is not None:
        ei.participantBodies = [alvo]
    ei.setDistanceExtent(False, vr(dist))
    f = ext.add(ei)
    if nome and f.bodies.count:
        f.bodies.item(0).name = nome
    return f


def cortar_tudo(root, perfis, alvo, negativo=False):
    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfis, CORTE)
    ei.participantBodies = [alvo]
    d = (adsk.fusion.ExtentDirections.NegativeExtentDirection if negativo
         else adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ei.setAllExtent(d)
    return ext.add(ei)


def arestas_z(body, z):
    col = adsk.core.ObjectCollection.create()
    for e in body.edges:
        bb = e.boundingBox
        if abs(bb.minPoint.z - z * MM) < 1e-4 and abs(bb.maxPoint.z - z * MM) < 1e-4:
            col.add(e)
    return col


def bloco(root, nome, cx, cy, z0, lx, ly, lz):
    sk = root.sketches.add(plano_z(root, z0, 'P_' + nome))
    sk.name = 'S_' + nome
    retangulo(sk, cx, cy, lx, ly)
    extrudar(root, perfil_maior(sk), None, lz, NOVO, nome)


def cilindro(root, nome, cx, cy, z0, diam, alt, alvo=None, op=NOVO):
    sk = root.sketches.add(plano_z(root, z0, 'P_' + nome))
    sk.name = 'S_' + nome
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(cx, cy), diam * MM / 2)
    extrudar(root, perfil_maior(sk), alvo, alt, op, nome if op == NOVO else None)


# ============================================================================
# BLOCO 1 - carcaca
# ============================================================================

def massa(root, log):
    sk = root.sketches.add(root.xYConstructionPlane)
    sk.name = 'S00_Contorno'
    retangulo(sk, 0.0, 0.0, P['larg'], P['prof'])
    f = extrudar(root, perfil_maior(sk), None, P['alt'], NOVO, 'B00_Massa')
    body = f.bodies.item(0)

    fil = root.features.filletFeatures
    col = adsk.core.ObjectCollection.create()
    for e in body.edges:
        bb = e.boundingBox
        if abs((bb.maxPoint.z - bb.minPoint.z) / MM - P['alt']) < 1e-3:
            col.add(e)
    if col.count:
        fi = fil.createInput()
        fi.addConstantRadiusEdgeSet(col, vr(P['r_canto']), True)
        fil.add(fi)
    for z, r in ((P['alt'], P['r_topo']), (0.0, 1.5)):
        c = arestas_z(body, z)
        if c.count:
            fi = fil.createInput()
            fi.addConstantRadiusEdgeSet(c, vr(r), True)
            fil.add(fi)

    col = adsk.core.ObjectCollection.create()
    col.add(body)
    sh = root.features.shellFeatures
    si = sh.createInput(col, False)
    si.insideThickness = vr(P['t_parede'])
    sh.add(si)

    sp = root.features.splitBodyFeatures
    sp.add(sp.createInput(body, plano_z(root, P['z_split'], 'P_Split'), True))

    b1, b2 = root.bRepBodies.item(0), root.bRepBodies.item(1)
    inf, sup = (b1, b2) if b1.boundingBox.minPoint.z < b2.boundingBox.minPoint.z else (b2, b1)
    inf.name = '02_Carcaca_Inferior'
    sup.name = '01_Carcaca_Superior'
    log.append("BLOCO 1 - carcaca")
    log.append("  %.0f x %.0f x %.0f | parede %.1f | particao Z=%.0f"
               % (P['larg'], P['prof'], P['alt'], P['t_parede'], P['z_split']))


# ============================================================================
# BLOCO 2 - parafusos M2
# ============================================================================

def parafusos(root, log):
    ps = None
    for i in range(root.constructionPlanes.count):
        if root.constructionPlanes.item(i).name == 'P_Split':
            ps = root.constructionPlanes.item(i)

    sk = root.sketches.add(ps)
    sk.name = 'S01_Torres'
    for x, y in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), PAR['d_torre'] * MM / 2)
    perfis = todos_perfis(sk)
    extrudar(root, perfis, corpo(root, '02_Carcaca_Inferior'), -P['z_split'], JUNTA)
    extrudar(root, perfis, corpo(root, '01_Carcaca_Superior'),
             P['alt'] - P['z_split'] - P['t_parede'], JUNTA)

    sk = root.sketches.add(ps)
    sk.name = 'S02_Furos_Inserto'
    for x, y in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), PAR['d_inserto'] * MM / 2)
    extrudar(root, todos_perfis(sk), corpo(root, '02_Carcaca_Inferior'),
             -PAR['h_inserto'], CORTE)

    sk = root.sketches.add(ps)
    sk.name = 'S03_Furos_Passantes'
    for x, y in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), PAR['d_passante'] * MM / 2)
    cortar_tudo(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'))

    sk = root.sketches.add(plano_z(root, P['alt'], 'P_Topo'))
    sk.name = 'S04_Rebaixo_Cabeca'
    for x, y in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), PAR['d_cabeca'] * MM / 2)
    extrudar(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'),
             -PAR['h_cabeca'], CORTE)
    log.append("")
    log.append("BLOCO 2 - fechamento")
    log.append("  4 parafusos M2 com inserto termico, em (+-43, +-35)")


# ============================================================================
# BLOCO 3 - garra, pino e tecido
# ============================================================================

def trava(root, log):
    gx, gy = XY_GARRA
    d_aloj = GARRA['diam'] + P['folga']
    d_furo = PINO['d_haste'] + PINO['folga']
    z_g = z_base_garra()

    sk = root.sketches.add(plano_z(root, z_g, 'P_Assento'))
    sk.name = 'S05_Alojamento_Garra'
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(gx, gy), d_aloj * MM / 2)
    cortar_tudo(root, todos_perfis(sk), corpo(root, '02_Carcaca_Inferior'))

    sk = root.sketches.add(root.xYConstructionPlane)
    sk.name = 'S06_Furo_Pino'
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(gx, gy), d_furo * MM / 2)
    cortar_tudo(root, todos_perfis(sk), corpo(root, '02_Carcaca_Inferior'))

    z_tec = -TECIDO['esp']
    sk = root.sketches.add(plano_z(root, z_tec, 'P_Tecido'))
    sk.name = 'S07_Tecido'
    retangulo(sk, gx, gy, TECIDO['lado'], TECIDO['lado'])
    extrudar(root, perfil_maior(sk), None, TECIDO['esp'], NOVO, '93_Tecido_da_peca')

    cilindro(root, '90_Pino_Disco', gx, gy, z_tec - PINO['t_cabeca'],
             PINO['d_cabeca'], PINO['t_cabeca'])
    cilindro(root, '91_Pino_Haste', gx, gy, z_tec, PINO['d_haste'], PINO['h_haste'])

    log.append("")
    log.append("BLOCO 3 - trava, pino e tecido")
    log.append("  alojamento D%.1f em (%+.0f, %+.0f) - garra COMPRADA" % (d_aloj, gx, gy))
    log.append("  a CAMISA entra entre Z=%.1f e Z=0, prensada entre a face inferior"
               % z_tec)
    log.append("  e o disco do pino (D%.0f). A haste sobe ate Z=%.1f."
               % (PINO['d_cabeca'], z_tec + PINO['h_haste']))


# ============================================================================
# BLOCO 4 - mecanismo
# ============================================================================

def bucha_e_cursor(root, a, log):
    gx, gy = XY_GARRA
    m = MEC[MECANISMO]
    z_garra = z_base_garra() + GARRA['alt']
    z_cursor = z_garra + BUCHA['alt']
    t_grosso = CUR['t_fino'] + GARRA['curso']
    z_teto = P['alt'] - P['t_parede']
    d_furo = PINO['d_haste'] + PINO['folga']

    cilindro(root, '30_Bucha', gx, gy, z_garra, BUCHA['d_ext'], BUCHA['alt'])
    sk = root.sketches.add(plano_z(root, z_garra, 'P_BuchaFuro'))
    sk.name = 'S10_Bucha_Furo'
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(gx, gy), d_furo * MM / 2)
    cortar_tudo(root, todos_perfis(sk), corpo(root, '30_Bucha'))

    y0, y1 = gy - CUR['prof'] / 2.0, gy + CUR['prof'] / 2.0
    w, ws = CUR['larg'] / 2.0, CUR['w_garfo'] / 2.0
    sk = root.sketches.add(plano_z(root, z_cursor, 'P_CursorBase'))
    sk.name = 'S11_Cursor_Planta'
    poligono(sk, [(gx - w, y0), (gx - w, y1), (gx - ws, y1), (gx - ws, gy + 2.0),
                  (gx + ws, gy + 2.0), (gx + ws, y1), (gx + w, y1), (gx + w, y0)])
    extrudar(root, perfil_maior(sk), None, t_grosso, NOVO, '31_Cursor')

    sk = root.sketches.add(root.yZConstructionPlane)
    sk.name = 'S12_Cursor_Rampa'
    poligono(sk, [(y0 - 2.0, z_cursor), (y0 - 2.0, z_cursor + GARRA['curso']),
                  (gy, z_cursor + GARRA['curso']), (gy + m['curso'], z_cursor)])
    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfil_maior(sk), CORTE)
    ei.participantBodies = [corpo(root, '31_Cursor')]
    ei.setSymmetricExtent(vr(CUR['larg']), True)
    ext.add(ei)

    sk = root.sketches.add(plano_z(root, z_cursor - 0.3, 'P_Guias'))
    sk.name = 'S13_Guias_Batente'
    for s in (-1, 1):
        retangulo(sk, gx + s * (w + CUR['folga'] + 0.75), gy, 1.5, CUR['prof'])
    retangulo(sk, gx, y0 - m['curso'] - 0.75, CUR['larg'] + 3.0, 1.5)
    extrudar(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'),
             z_teto - z_cursor + 0.3, JUNTA)
    log.append("  bucha D%.1f | cursor %.0f x %.0f, %.1f -> %.1f, rampa %.1f graus"
               % (BUCHA['d_ext'], CUR['larg'], CUR['prof'], CUR['t_fino'],
                  t_grosso, a['ang']))
    return z_cursor


def mec_came(root, a, log):
    z = bucha_e_cursor(root, a, log)
    m = MEC[MECANISMO]
    sx, sy = XY_ATUADOR[MECANISMO]
    R = m['braco']
    bloco(root, '40_Servo_MG90S', sx, sy, P['t_parede'] + 0.5, *m['peca'])

    # braco APONTANDO EM -X: girando, a ponta anda em Y e empurra o cursor
    cilindro(root, '41_Braco', sx, sy, z - 3.2, 7.0, 3.0)
    sk = root.sketches.add(plano_z(root, z - 3.2, 'P_Braco'))
    sk.name = 'S14_Braco'
    retangulo(sk, sx - R / 2.0, sy, R, 6.0)
    extrudar(root, perfil_maior(sk), corpo(root, '41_Braco'), 3.0, JUNTA)

    # VOLUME VARRIDO - o que um bloco-envelope nao mostra
    arco = arco_braco()
    sk = root.sketches.add(plano_z(root, z - 3.4, 'P_Varredura'))
    sk.name = 'S15_Varredura_Braco'
    c = sk.sketchCurves
    a0 = math.radians(180.0 - arco / 2.0)
    arc = c.sketchArcs.addByCenterStartSweep(
        pt(sx, sy), pt(sx + R * math.cos(a0), sy + R * math.sin(a0)),
        math.radians(arco))
    ln = c.sketchLines
    ln.addByTwoPoints(arc.startSketchPoint, pt(sx, sy))
    ln.addByTwoPoints(pt(sx, sy), arc.endSketchPoint)
    extrudar(root, perfil_maior(sk), None, 3.4, NOVO, '42_Varredura_Braco')

    log.append("  braco de %.0f mm apontando em -X, eixo em (%+.0f, %+.0f)" % (R, sx, sy))
    log.append("  varre %.1f graus para dar %.1f mm de curso ao cursor" % (arco, m['curso']))
    log.append("  42_Varredura_Braco: o volume que o braco ocupa AO GIRAR.")
    log.append("  Nada pode estar dentro dele - e' o que o envelope de caixa nao pega.")


def mec_fuso(root, a, log):
    z = bucha_e_cursor(root, a, log)
    m = MEC[MECANISMO]
    sx, sy = XY_ATUADOR[MECANISMO]
    gx, gy = XY_GARRA
    bloco(root, '40_Motor_N20', sx, sy, P['t_parede'] + 0.5, *m['peca'])
    comp = abs(sy - (gy + CUR['prof'] / 2.0)) + 8.0
    sk = root.sketches.add(plano_z(root, z + 1.0, 'P_Fuso'))
    sk.name = 'S14_Fuso'
    retangulo(sk, gx, sy - comp / 2.0, 3.0, comp)
    extrudar(root, perfil_maior(sk), None, 3.0, NOVO, '41_Fuso_M3')
    for i, s in enumerate((-1, 1)):
        bloco(root, '42_Fim_Curso_%d' % (i + 1), gx + 10.0,
              gy + s * (CUR['prof'] / 2.0 + 3.0), z, 6.0, 3.0, 4.0)
    log.append("  fuso M3 passo 0,5: %.1f voltas | DOIS fins de curso"
               % (GARRA['curso'] / 0.5))


def mec_solenoide(root, a, log):
    z = bucha_e_cursor(root, a, log)
    m = MEC[MECANISMO]
    sx, sy = XY_ATUADOR[MECANISMO]
    gx, gy = XY_GARRA
    bloco(root, '40_Solenoide', sx, sy, P['t_parede'] + 0.5, *m['peca'])
    comp = abs(sy - (gy + CUR['prof'] / 2.0)) + 6.0
    sk = root.sketches.add(plano_z(root, z + 1.0, 'P_Embolo'))
    sk.name = 'S14_Embolo'
    retangulo(sk, gx, sy - comp / 2.0, 4.0, comp)
    extrudar(root, perfil_maior(sk), None, 4.0, NOVO, '41_Embolo')
    log.append("  embolo empurra o cursor %.1f mm | timeout de 1 s" % m['curso'])


def mec_sma(root, a, log):
    z = bucha_e_cursor(root, a, log)
    gx, gy = XY_GARRA
    y_anc = max(gy - CUR['prof'] / 2.0 - 42.0,
                -P['prof'] / 2.0 + P['t_parede'] + 4.0)
    comp = abs((gy - CUR['prof'] / 2.0) - y_anc)
    for i, s in enumerate((-1, 1)):
        cilindro(root, '40_Poste_SMA_%d' % (i + 1), gx + s * 3.5, y_anc, z - 2.0, 3.0, 4.0)
        sk = root.sketches.add(plano_z(root, z + 0.5, 'P_Fio_%d' % (i + 1)))
        sk.name = 'S14_Fio_%d' % (i + 1)
        retangulo(sk, gx + s * 3.5, y_anc + comp / 2.0, 0.6, comp)
        extrudar(root, perfil_maior(sk), None, 0.6, NOVO, '41_Fio_SMA_%d' % (i + 1))
    log.append("  2 fios RETOS de %.0f mm (sem desvio: efeito capstan)" % comp)


def mec_eletroima(root, a, log):
    gx, gy = XY_GARRA
    lx, ly, lz = MEC[MECANISMO]['peca']
    cilindro(root, '40_Eletroima', gx, gy, 0.2, lx, lz)
    sk = root.sketches.add(plano_z(root, 0.2, 'P_Jugo'))
    sk.name = 'S14_Jugo'
    c = sk.sketchCurves.sketchCircles
    c.addByCenterRadius(pt(gx, gy), (lx + 6.0) * MM / 2)
    c.addByCenterRadius(pt(gx, gy), (lx + 2.0) * MM / 2)
    extrudar(root, perfil_maior(sk), None, lz + 2.0, NOVO, '41_Jugo_Aco')
    log.append("  SEM cursor: a bobina puxa a gaiola direto")


def mecanismo(root, a, log):
    log.append("")
    log.append("BLOCO 4 - mecanismo: %s" % MEC[MECANISMO]['nome'])
    {'came': mec_came, 'fuso': mec_fuso, 'solenoide': mec_solenoide,
     'sma': mec_sma, 'eletroima': mec_eletroima}[MECANISMO](root, a, log)
    log.append("  forca: %.1f N contra mola de %.1f N -> margem %.2fx"
               % (a['saida'], GARRA['forca'], a['margem']))


# ============================================================================
# BLOCO 5 - painel e recarga
# ============================================================================

def painel(root, log):
    p_topo = plano_z(root, P['alt'], 'P_FaceSuperior')
    qx, qy, qcx, qcy = UI['qr']

    sk = root.sketches.add(p_topo)
    sk.name = 'S20_QR_Impresso'
    retangulo(sk, qcx, qcy, qx, qy)
    extrudar(root, perfil_maior(sk), corpo(root, '01_Carcaca_Superior'),
             -UI['prof_rebaixo'], CORTE)

    sk = root.sketches.add(p_topo)
    sk.name = 'S21_LED_Botao'
    c = sk.sketchCurves.sketchCircles
    c.addByCenterRadius(pt(UI['xy_led'][0], UI['xy_led'][1]), UI['furo_led'] * MM / 2)
    c.addByCenterRadius(pt(UI['xy_botao'][0], UI['xy_botao'][1]), UI['furo_botao'] * MM / 2)
    cortar_tudo(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'), negativo=True)

    log.append("")
    log.append("BLOCO 5 - painel e recarga")
    log.append("  QR IMPRESSO %.0f x %.0f - o CELULAR le este" % (qx, qy))
    log.append("  LED D%.0f (vermelho -> verde) | botao D%.1f"
               % (UI['furo_led'], UI['furo_botao']))


def recarga(root, log):
    inf = corpo(root, '02_Carcaca_Inferior')
    if RECARGA == 'contatos':
        # rebaixos na FACE INFERIOR: a etiqueta deita na bandeja e carrega
        sk = root.sketches.add(root.xYConstructionPlane)
        sk.name = 'S22_Contatos_Recarga'
        for x, y in REC['xy_pads']:
            sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), REC['d_pad'] * MM / 2)
        extrudar(root, todos_perfis(sk), inf, REC['prof_pad'], CORTE)

        sk = root.sketches.add(root.xYConstructionPlane)
        sk.name = 'S23_Passagem_Fio'
        for x, y in REC['xy_pads']:
            sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), REC['d_fio'] * MM / 2)
        cortar_tudo(root, todos_perfis(sk), corpo(root, '02_Carcaca_Inferior'))
        log.append("  RECARGA por CONTATOS: 2 pads D%.1f na face inferior, em %s"
                   % (REC['d_pad'], ' e '.join('(%+.0f,%+.0f)' % p for p in REC['xy_pads'])))
        log.append("  A etiqueta deita na bandeja e carrega. Ninguem pluga nada -")
        log.append("  e' o que permite carregar milhares delas.")
    else:
        # recorte lateral no nivel do TP4056
        bx, by, bz = POS['carga']
        z_usb = bz + COMP['carga'][2] / 2.0
        pl = root.constructionPlanes
        pi = pl.createInput()
        pi.setByOffset(root.xZConstructionPlane, vr(by))
        pln = pl.add(pi)
        pln.name = 'P_USB'
        sk = root.sketches.add(pln)
        sk.name = 'S22_Recorte_USB'
        retangulo(sk, P['larg'] / 2.0 - 4.0, z_usb, REC['usb_larg'], REC['usb_alt'])
        extrudar(root, perfil_maior(sk), inf, 12.0, CORTE)
        log.append("  RECARGA por USB-C: recorte %.1f x %.1f na lateral, em Z=%.1f"
                   % (REC['usb_larg'], REC['usb_alt'], z_usb))
        log.append("  Confira em qual borda do ESP32-C3 fica o conector real.")


# ============================================================================
# BLOCO 6 - eletronica
# ============================================================================

def eletronica(root, log):
    for i, n in enumerate(('bateria', 'carga', 'mcu', 'botao')):
        x, y, z = POS[n]
        bloco(root, '5%d_%s' % (i, n), x, y, z, *COMP[n])
    log.append("")
    log.append("BLOCO 6 - eletronica")
    for n in ('mcu', 'bateria', 'carga', 'botao'):
        log.append("  %-9s %5.1f x %5.1f x %5.1f" % ((n,) + COMP[n]))


# ============================================================================
# PRINCIPAL
# ============================================================================

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        erros, avisos, a = verificar()
        if erros:
            ui.messageBox("MECANISMO: %s\n\nNAO CABE - nada foi modelado:\n\n%s"
                          % (MECANISMO, '\n\n'.join(erros)), 'Antifurto Tag&Go')
            return

        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent

        log = ["MECANISMO %s | ESPERA %s | RECARGA %s"
               % (MECANISMO, MODO_ESPERA, RECARGA), ""]
        massa(root, log)
        parafusos(root, log)
        trava(root, log)
        mecanismo(root, a, log)
        painel(root, log)
        recarga(root, log)
        eletronica(root, log)

        au = autonomia()
        log.append("")
        log.append("AUTONOMIA (LiPo %.0f mAh)" % ENERGIA['capacidade'])
        log.append("  modo de espera   : %s" % MODO_ESPERA)
        log.append("  corrente media   : %.3f mA" % au['media'])
        if au['anos'] >= 1.0:
            log.append("  standby          : %.1f anos (limitado pela autodescarga do LiPo)"
                       % au['anos'])
        else:
            log.append("  standby          : %.0f dias" % au['dias'])
        log.append("  por liberacao    : %.3f mAh -> %.0f liberacoes por carga"
                   % (au['por_lib'], au['n_lib']))

        log.append("")
        log.append("COMPARATIVO DOS CINCO MECANISMOS")
        log.extend(tabela())

        log.append("")
        log.append("LISTA DE COMPRAS - buscar no Mercado Livre")
        tot = 0.0
        for termo, qt, pu, nota in bom():
            tot += qt * pu
            log.append('  %2dx  R$%7.2f  "%s"' % (qt, qt * pu, termo))
            log.append('                    %s' % nota)
        log.append("  %s" % ('-' * 58))
        log.append("  TOTAL ~R$ %.2f   (%.2f por aluno, em 8)" % (tot, tot / 8.0))
        log.append("  precos de ordem de grandeza - conferir no dia da compra")

        if avisos:
            log.append("")
            log.append("AVISOS")
            for x in avisos:
                log.append("  - " + x.replace(chr(10), chr(10) + "    "))

        log.append("")
        log.append("CORPOS - o que e' PROJETADO e o que e' so ENVELOPE")
        for b in root.bRepBodies:
            tipo = 'PROJETADO (imprimir)' if b.name[:2] in ('01', '02', '30', '31', '41') \
                   else 'envelope de peca comprada'
            log.append("   %-24s %8.2f cm3  %s" % (b.name, b.volume / 1000.0, tipo))

        log.append("")
        log.append("O QUE FALTA MEDIR - trocar em GARRA e PINO no topo")
        log.append("  diametro, altura, curso e forca da garra real.")

        ui.messageBox(chr(10).join(log), 'Antifurto Tag&Go - %s' % MECANISMO)
    except:
        if ui:
            ui.messageBox('FALHOU:' + chr(10) + traceback.format_exc(),
                          'Antifurto Tag&Go - erro')
