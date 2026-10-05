# -*- coding: utf-8 -*-
"""
TagAndGo - carcaca do prototipo de etiqueta antifurto autoliberavel
Blocos 1 a 5.

COMO RODAR
----------
Shift+S -> aba Scripts -> TagAndGo -> Run
Ao terminar, uma janela mostra o relatorio com volumes e verificacoes.

PARA MUDAR QUALQUER MEDIDA
--------------------------
Edite os numeros do dicionario P abaixo e rode de novo. Cada execucao cria um
documento NOVO, entao nao ha risco de sujar o anterior.

Todas as medidas aqui estao em MILIMETROS. A API do Fusion trabalha em
centimetros; a constante MM faz a conversao.
"""

import adsk.core
import adsk.fusion
import traceback
import math

MM = 0.1
TOL = 1e-4
VOL_MACICO = [1.0]

# ============================================================================
# PARAMETROS - edite aqui, tudo em milimetros
# ============================================================================

P = {
    # --- envelope da carcaca (decisao de projeto) ---
    'r_lobo':               24.0,
    'r_cauda':              11.0,
    'd_lobo_cauda':         45.0,
    'h_corpo':              18.0,
    'h_split':               8.0,
    't_parede':              2.0,
    'r_pillow':              5.0,
    'r_pillow_inf':          2.0,
    'folga_impressao':       0.3,

    # --- pecas compradas: MEDIR AS PECAS REAIS E SUBSTITUIR ---
    'd_garra':              12.0,
    'h_garra':              10.0,   # LIMITE 10.7 - ver verificar_parametros()
    'curso_garra':           1.2,
    'forca_mola_garra':      2.5,   # N
    'd_furo_pino':           2.4,
    'L_mcu':                22.5,
    'W_mcu':                18.0,
    'H_mcu':                 4.0,
    'L_driver':             12.0,
    'W_driver':             12.0,
    'H_driver':              3.0,
    'd_nfc':                25.0,
    't_nfc':                 0.2,
    'L_inlay':              44.0,
    'W_inlay':              12.0,
    'd_pogo':                6.0,

    # --- atuador SMA ---
    'd_sma':                 0.15,
    'L_sma':                42.0,   # por fio; sao 2 fios retos, sem poste
    'forca_sma':             3.2,   # N por fio, datasheet Flexinol 150 um

    # --- montagem ---
    'd_inserto':             3.2,
    'h_inserto':             4.0,
    'd_parafuso_passante':   2.4,
    'd_cabeca_parafuso':     4.2,
    'd_torre':               6.0,
}

N_SMA = 2
MU = 0.30   # atrito PETG-aco, ESTIMADO - medir na bancada

# Posicoes dos 4 parafusos. Calculadas para nao bater no alojamento da garra
# nem na parede. Sao ZONA PROIBIDA para a eletronica.
FUROS = [
    (  0.0,  17.0),   # F1 - lobo, acima da garra
    (-15.0,  -8.0),   # F2 - lateral esquerda
    ( 15.0,  -8.0),   # F3 - lateral direita
    (  0.0, -49.0),   # F4 - cauda
]

# Geometria do cursor
CUR = {
    'w':        10.0,
    'y_tras':  -10.0,
    'y_frente':  5.0,
    'y_raiz':   -4.0,
    'w_slot':    3.0,
}
X_GUIA = 5.3

# Eletronica e face superior
Y_MCU    = -20.0
Y_DRIVER = -39.0
Y_NFC    = -25.0
Y_QR     =   2.0
LADO_QR  =  20.0
XY_POGO  = (8.0, -8.0)
Y_LED    = -44.0
D_LED    =   3.2
PROF_REB =   0.4
X_SMA    =   3.5
Y_POSTE  = -52.0


def D(k):
    """Valores derivados dos parametros."""
    t = P['t_parede']
    if k == 'd_alojamento':  return P['d_garra'] + P['folga_impressao']
    if k == 'z_topo_garra':  return t + P['h_garra']
    if k == 'z_teto':        return P['h_corpo'] - t
    if k == 'curso_sma':     return P['L_sma'] * 0.04
    if k == 't_fino':        return 2.0
    if k == 't_grosso':      return 2.0 + P['curso_garra']
    if k == 'z_cursor_base': return D('z_teto') - D('t_grosso')
    if k == 'z_cursor_fino': return D('z_teto') - D('t_fino')
    if k == 'h_bucha':       return D('z_cursor_fino') - D('z_topo_garra')
    raise KeyError(k)


# ============================================================================
# VERIFICACOES - rodam antes de modelar
# ============================================================================

def verificar_parametros():
    """Melhor falhar aqui, em 1 segundo, do que depois de imprimir."""
    erros = []
    camara = D('z_teto') - D('z_topo_garra') - P['folga_impressao']

    if camara < 3.0:
        erros.append(
            "Camara de atuacao com apenas %.2f mm (minimo 3.0).\n"
            "  A garra de %.1f mm nao deixa espaco para o cursor.\n"
            "  Solucao: aumente h_corpo para pelo menos %.1f mm."
            % (camara, P['h_garra'], P['h_corpo'] + (3.0 - camara)))

    dist_F1 = math.hypot(FUROS[0][0], FUROS[0][1])
    folga_F1 = dist_F1 - P['d_torre'] / 2.0 - D('d_alojamento') / 2.0
    if folga_F1 < 1.0:
        erros.append("Garra Ø%.1f colide com a torre F1 (folga %.2f mm)."
                     % (P['d_garra'], folga_F1))

    if D('curso_sma') < P['curso_garra']:
        erros.append(
            "Curso do fio (%.2f mm) menor que o curso necessario da garra (%.2f mm).\n"
            "  Solucao: aumente L_sma para pelo menos %.0f mm."
            % (D('curso_sma'), P['curso_garra'], P['curso_garra'] / 0.04))

    return erros, camara


def analise_mecanismo():
    """Cinematica e forca do conjunto fio -> rampa -> bucha."""
    curso = D('curso_sma')
    ang = math.degrees(math.atan2(P['curso_garra'], curso))
    phi = math.degrees(math.atan(MU))
    efic = math.tan(math.radians(ang)) / math.tan(math.radians(ang + phi))
    ganho = 1.0 / math.tan(math.radians(ang))
    forca = N_SMA * P['forca_sma'] * ganho * efic
    return {
        'curso': curso, 'ang': ang, 'efic': efic, 'ganho': ganho,
        'forca': forca, 'margem': forca / P['forca_mola_garra'],
        'autotrava': math.tan(math.radians(ang)) <= MU,
    }


# ============================================================================
# GEOMETRIA DO CONTORNO
# ============================================================================

def pontos_tangencia():
    """Tangente EXTERNA: os dois centros ficam do mesmo lado da reta."""
    r1, r2, d = P['r_lobo'], P['r_cauda'], P['d_lobo_cauda']
    sin_f = (r1 - r2) / d
    cos_f = math.sqrt(1.0 - sin_f * sin_f)
    p_lobo = (r1 * cos_f, -r1 * sin_f)
    p_cauda = (r2 * cos_f, -d - r2 * sin_f)
    return p_lobo, p_cauda, math.sqrt(d * d - (r1 - r2) ** 2)


# ============================================================================
# UTILITARIOS
# ============================================================================

def pt(x_mm, y_mm, z_mm=0.0):
    return adsk.core.Point3D.create(x_mm * MM, y_mm * MM, z_mm * MM)


def vr(mm):
    return adsk.core.ValueInput.createByReal(mm * MM)


def vs(expr):
    return adsk.core.ValueInput.createByString(expr)


def corpo(root, nome):
    """Referencias diretas morrem depois de Split/Join - sempre rebusque."""
    for b in root.bRepBodies:
        if b.name == nome:
            return b
    raise RuntimeError('corpo nao encontrado: ' + nome)


def plano_z(root, z_mm, nome):
    pl = root.constructionPlanes
    pi = pl.createInput()
    pi.setByOffset(root.xYConstructionPlane, vr(z_mm))
    pln = pl.add(pi)
    pln.name = nome
    return pln


def todos_perfis(sk):
    col = adsk.core.ObjectCollection.create()
    for i in range(sk.profiles.count):
        col.add(sk.profiles.item(i))
    return col


def perfil_maior(sk):
    melhor, area = None, -1.0
    for i in range(sk.profiles.count):
        pr = sk.profiles.item(i)
        a = pr.areaProperties().area
        if a > area:
            melhor, area = pr, a
    col = adsk.core.ObjectCollection.create()
    col.add(melhor)
    return col


def arestas_na_cota_z(body, z_mm):
    z = z_mm * MM
    col = adsk.core.ObjectCollection.create()
    for e in body.edges:
        bb = e.boundingBox
        if abs(bb.minPoint.z - z) < TOL and abs(bb.maxPoint.z - z) < TOL:
            col.add(e)
    return col


def extrudar(root, perfis, alvo, dist_mm, op, nome=None):
    """dist_mm negativo = para baixo. alvo=None -> novo corpo."""
    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfis, op)
    if alvo is not None:
        ei.participantBodies = [alvo]
    ei.setDistanceExtent(False, vr(dist_mm))
    f = ext.add(ei)
    if nome and f.bodies.count:
        f.bodies.item(0).name = nome
    return f


def cortar_passante(root, perfis, alvo, negativo=False):
    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfis, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ei.participantBodies = [alvo]
    d = (adsk.fusion.ExtentDirections.NegativeExtentDirection if negativo
         else adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ei.setAllExtent(d)
    return ext.add(ei)


def retangulo(sk, cx, cy, larg_x, larg_y):
    return sk.sketchCurves.sketchLines.addTwoPointRectangle(
        pt(cx - larg_x / 2.0, cy - larg_y / 2.0),
        pt(cx + larg_x / 2.0, cy + larg_y / 2.0))


def criar_parametros(design, log):
    ups = design.userParameters
    n = 0
    for nome, valor in sorted(P.items()):
        if nome in ('forca_mola_garra', 'forca_sma'):
            continue
        existente = ups.itemByName(nome)
        if existente:
            existente.expression = '%.4f mm' % valor
        else:
            ups.add(nome, vs('%.4f mm' % valor), 'mm', '')
        n += 1
    log.append("Parametros de usuario criados: %d" % n)


# ============================================================================
# BLOCO 1 - contorno mestre e solido mestre
# ============================================================================

def bloco1(root, log):
    p_lobo, p_cauda, comp_tan = pontos_tangencia()

    sk = root.sketches.add(root.xYConstructionPlane)
    sk.name = 'S00_Contorno_Mestre'
    arcos = sk.sketchCurves.sketchArcs
    linhas = sk.sketchCurves.sketchLines

    arco_lobo = arcos.addByThreePoints(
        pt(p_lobo[0], p_lobo[1]), pt(0.0, P['r_lobo']), pt(-p_lobo[0], p_lobo[1]))
    reta_esq = linhas.addByTwoPoints(
        arco_lobo.endSketchPoint, pt(-p_cauda[0], p_cauda[1]))
    arco_cauda = arcos.addByThreePoints(
        reta_esq.endSketchPoint,
        pt(0.0, -(P['d_lobo_cauda'] + P['r_cauda'])),
        pt(p_cauda[0], p_cauda[1]))
    linhas.addByTwoPoints(arco_cauda.endSketchPoint, arco_lobo.startSketchPoint)

    if sk.profiles.count == 0:
        raise RuntimeError('O contorno mestre nao fechou um perfil.')

    f = extrudar(root, perfil_maior(sk), None, P['h_corpo'],
                 adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
                 'B00_Solido_Mestre')
    body = f.bodies.item(0)

    fil = root.features.filletFeatures
    for cota, raio in ((P['h_corpo'], 'r_pillow'), (0.0, 'r_pillow_inf')):
        col = arestas_na_cota_z(body, cota)
        if col.count:
            fi = fil.createInput()
            fi.addConstantRadiusEdgeSet(col, vs(raio), True)
            fil.add(fi)

    bb = body.boundingBox
    VOL_MACICO[0] = body.volume / (MM ** 3)
    log.append("BLOCO 1")
    log.append("  comprimento Y : %.2f mm  (esperado %.2f)"
               % ((bb.maxPoint.y - bb.minPoint.y) / MM,
                  P['r_lobo'] + P['d_lobo_cauda'] + P['r_cauda']))
    log.append("  largura X     : %.2f mm  (esperado %.2f)"
               % ((bb.maxPoint.x - bb.minPoint.x) / MM, 2 * P['r_lobo']))
    log.append("  reta tangente : %.2f mm" % comp_tan)
    log.append("  volume macico : %.0f mm3" % VOL_MACICO[0])
    return body


# ============================================================================
# BLOCO 2 - casca, divisao e fechamento por parafuso
# ============================================================================

def bloco2(root, body, log):
    col = adsk.core.ObjectCollection.create()
    col.add(body)
    sh = root.features.shellFeatures
    si = sh.createInput(col, False)
    si.insideThickness = vs('t_parede')
    sh.add(si)
    vol_casca = body.volume / (MM ** 3)

    p_split = plano_z(root, P['h_split'], 'P_Split')

    sp = root.features.splitBodyFeatures
    sp.add(sp.createInput(body, p_split, True))

    if root.bRepBodies.count != 2:
        raise RuntimeError('Split gerou %d corpos, esperado 2.' % root.bRepBodies.count)

    b1, b2 = root.bRepBodies.item(0), root.bRepBodies.item(1)
    if b1.boundingBox.minPoint.z < b2.boundingBox.minPoint.z:
        inferior, superior = b1, b2
    else:
        inferior, superior = b2, b1
    inferior.name = '02_Carcaca_Inferior'
    superior.name = '01_Carcaca_Superior'

    # torres e tubos, de um sketch so
    sk = root.sketches.add(p_split)
    sk.name = 'S01_Furacao'
    for (x, y) in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), P['d_torre'] * MM / 2)
    perfis = todos_perfis(sk)

    extrudar(root, perfis, inferior, -P['h_split'],
             adsk.fusion.FeatureOperations.JoinFeatureOperation)
    extrudar(root, perfis, corpo(root, '01_Carcaca_Superior'),
             P['h_corpo'] - P['h_split'] - P['t_parede'],
             adsk.fusion.FeatureOperations.JoinFeatureOperation)

    # furos do inserto termico
    sk = root.sketches.add(p_split)
    sk.name = 'S02_Furos_Inserto'
    for (x, y) in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(x, y), P['d_inserto'] * MM / 2)
    extrudar(root, todos_perfis(sk), corpo(root, '02_Carcaca_Inferior'), -P['h_inserto'],
             adsk.fusion.FeatureOperations.CutFeatureOperation)

    # furos de passagem
    sk = root.sketches.add(p_split)
    sk.name = 'S03_Furos_Passantes'
    for (x, y) in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(
            pt(x, y), P['d_parafuso_passante'] * MM / 2)
    cortar_passante(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'))

    # rebaixo da cabeca
    p_topo = plano_z(root, P['h_corpo'], 'P_Topo')
    sk = root.sketches.add(p_topo)
    sk.name = 'S04_Rebaixo_Cabeca'
    for (x, y) in FUROS:
        sk.sketchCurves.sketchCircles.addByCenterRadius(
            pt(x, y), P['d_cabeca_parafuso'] * MM / 2)
    extrudar(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'), -2.0,
             adsk.fusion.FeatureOperations.CutFeatureOperation)

    v_inf = corpo(root, '02_Carcaca_Inferior').volume / (MM ** 3)
    v_sup = corpo(root, '01_Carcaca_Superior').volume / (MM ** 3)
    razao = vol_casca / VOL_MACICO[0]
    log.append("")
    log.append("BLOCO 2")
    log.append("  volume apos ocar   : %.0f mm3" % vol_casca)
    log.append("  razao casca/macico : %.1f%%  (esperado 25%% a 40%%)" % (razao * 100))
    if not (0.25 <= razao <= 0.40):
        log.append("  ATENCAO: razao fora do esperado. O Shell rodou?")
    log.append("  corpos             : %d" % root.bRepBodies.count)
    log.append("  metade inferior    : %.0f mm3" % v_inf)
    log.append("  metade superior    : %.0f mm3" % v_sup)


# ============================================================================
# BLOCO 3 - alojamento da garra e furo do pino
# ============================================================================

def bloco3(root, log):
    p_assento = plano_z(root, P['t_parede'], 'P_Assento')

    sk = root.sketches.add(p_assento)
    sk.name = 'S05_Alojamento_Garra'
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(0, 0), D('d_alojamento') * MM / 2)
    cortar_passante(root, todos_perfis(sk), corpo(root, '02_Carcaca_Inferior'))

    sk = root.sketches.add(root.xYConstructionPlane)
    sk.name = 'S06_Furo_Pino'
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(0, 0), P['d_furo_pino'] * MM / 2)
    cortar_passante(root, todos_perfis(sk), corpo(root, '02_Carcaca_Inferior'))

    log.append("")
    log.append("BLOCO 3")
    log.append("  alojamento Ø%.2f, de Z=%.1f a Z=%.1f"
               % (D('d_alojamento'), P['t_parede'], P['h_split']))
    log.append("  topo da garra em Z=%.1f - ela atravessa o plano de particao"
               % D('z_topo_garra'))
    log.append("  furo do pino Ø%.1f no piso" % P['d_furo_pino'])
    log.append("  metade inferior agora: %.0f mm3"
               % (corpo(root, '02_Carcaca_Inferior').volume / (MM ** 3)))


# ============================================================================
# BLOCO 4 - bucha, cursor com rampa, guias, batente e ancoras
# ============================================================================

def contorno_cursor(sk):
    """Planta em U: duas hastes para +Y, unidas por um corpo em -Y."""
    w, ws = CUR['w'] / 2.0, CUR['w_slot'] / 2.0
    yt, yf, yr = CUR['y_tras'], CUR['y_frente'], CUR['y_raiz']
    pts = [(w, yt), (w, yf), (ws, yf), (ws, yr),
           (-ws, yr), (-ws, yf), (-w, yf), (-w, yt)]
    linhas = sk.sketchCurves.sketchLines
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        linhas.addByTwoPoints(pt(a[0], a[1]), pt(b[0], b[1]))


def bloco4(root, log):
    z_fino = D('z_cursor_fino')
    z_base = D('z_cursor_base')
    curso = D('curso_sma')

    # --- 04_Bucha_Empurradora ---
    p_bucha = plano_z(root, D('z_topo_garra'), 'P_TopoGarra')
    sk = root.sketches.add(p_bucha)
    sk.name = 'S07_Bucha'
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(0, 0), 6.0 * MM / 2)
    extrudar(root, perfil_maior(sk), None, D('h_bucha'),
             adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
             '04_Bucha_Empurradora')

    sk = root.sketches.add(p_bucha)
    sk.name = 'S08_Bucha_Furo'
    sk.sketchCurves.sketchCircles.addByCenterRadius(
        pt(0, 0), (P['d_furo_pino'] + P['folga_impressao']) * MM / 2)
    cortar_passante(root, todos_perfis(sk), corpo(root, '04_Bucha_Empurradora'))

    # --- 03_Cursor_Rampa: laje em U, depois a rampa cortada por baixo ---
    p_base = plano_z(root, z_base, 'P_CursorBase')
    sk = root.sketches.add(p_base)
    sk.name = 'S09_Cursor_Planta'
    contorno_cursor(sk)
    extrudar(root, perfil_maior(sk), None, D('t_grosso'),
             adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
             '03_Cursor_Rampa')

    # No sketch do plano YZ: eixo local X = Y global, eixo local Y = Z global.
    sk = root.sketches.add(root.yZConstructionPlane)
    sk.name = 'S10_Cursor_Rampa'
    y0 = CUR['y_tras'] - 2.0
    verts = [(y0, z_base), (y0, z_fino), (0.0, z_fino), (curso, z_base)]
    linhas = sk.sketchCurves.sketchLines
    for i in range(len(verts)):
        a, b = verts[i], verts[(i + 1) % len(verts)]
        linhas.addByTwoPoints(pt(a[0], a[1]), pt(b[0], b[1]))
    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfil_maior(sk),
                         adsk.fusion.FeatureOperations.CutFeatureOperation)
    ei.participantBodies = [corpo(root, '03_Cursor_Rampa')]
    ei.setSymmetricExtent(vr(CUR['w']), True)
    ext.add(ei)

    # furos de crimpagem dos fios
    sk = root.sketches.add(p_base)
    sk.name = 'S11_Cursor_Furos_Fio'
    for sx in (-1, 1):
        sk.sketchCurves.sketchCircles.addByCenterRadius(
            pt(sx * X_SMA, CUR['y_tras'] + 1.5), 1.0 * MM / 2)
    cortar_passante(root, todos_perfis(sk), corpo(root, '03_Cursor_Rampa'))

    # --- guias e batente, na metade superior ---
    p_guia = plano_z(root, z_base - 0.2, 'P_Guias')
    h_guia = D('z_teto') - (z_base - 0.2)
    sk = root.sketches.add(p_guia)
    sk.name = 'S12_Guias_Batente'
    for sx in (-1, 1):
        retangulo(sk, sx * (X_GUIA + 0.75), CUR['y_tras'] / 2.0, 1.5, abs(CUR['y_tras']))
    y_bat = CUR['y_tras'] - curso - 0.75
    retangulo(sk, 0.0, y_bat, CUR['w'] + 2.0, 1.5)
    extrudar(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'), h_guia,
             adsk.fusion.FeatureOperations.JoinFeatureOperation)

    # --- postes de ancoragem dos fios ---
    p_poste = plano_z(root, D('z_teto') - 3.0, 'P_Postes')
    sk = root.sketches.add(p_poste)
    sk.name = 'S13_Postes_Ancora'
    for sx in (-1, 1):
        sk.sketchCurves.sketchCircles.addByCenterRadius(pt(sx * X_SMA, Y_POSTE), 3.0 * MM / 2)
    extrudar(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'), 3.0,
             adsk.fusion.FeatureOperations.JoinFeatureOperation)

    m = analise_mecanismo()
    L_real = abs(Y_POSTE - (CUR['y_tras'] + 1.5))
    log.append("")
    log.append("BLOCO 4")
    log.append("  curso de cada fio  : %.2f mm  (4%% de %.0f mm)" % (m['curso'], P['L_sma']))
    log.append("  angulo da rampa    : %.1f graus" % m['ang'])
    log.append("  ganho de forca     : %.2fx" % m['ganho'])
    log.append("  eficiencia (mu=%.2f): %.3f" % (MU, m['efic']))
    log.append("  forca na garra     : %.2f N  vs mola de %.1f N"
               % (m['forca'], P['forca_mola_garra']))
    log.append("  margem             : %.2fx  %s"
               % (m['margem'], 'OK' if m['margem'] >= 1.5 else 'BAIXA - use 3 fios'))
    log.append("  autotravante       : %s" % ('SIM - precisa de mola de retorno'
                                              if m['autotrava'] else 'NAO'))
    log.append("  vao ancora-cursor  : %.1f mm  (L_sma = %.1f)" % (L_real, P['L_sma']))
    if abs(L_real - P['L_sma']) > 0.5:
        log.append("  ATENCAO: vao diferente de L_sma - ajuste Y_POSTE")
    log.append("  bucha Ø6.0 x %.2f, de Z=%.1f a Z=%.1f"
               % (D('h_bucha'), D('z_topo_garra'), z_fino))
    log.append("  cursor: %.0f mm3 (esperado ~280)"
               % (corpo(root, '03_Cursor_Rampa').volume / (MM ** 3)))
    log.append("  bucha : %.0f mm3 (esperado ~45)"
               % (corpo(root, '04_Bucha_Empurradora').volume / (MM ** 3)))


# ============================================================================
# BLOCO 5 - eletronica, contatos e elementos de face
# ============================================================================

def bloco5(root, log):
    f = P['folga_impressao']
    p_piso = plano_z(root, P['t_parede'], 'P_Piso')

    for nome, y, lx, ly, prof in (
            ('S14_Baia_MCU', Y_MCU,
             P['W_mcu'] + 2 * f, P['L_mcu'] + 2 * f, P['H_mcu'] + 0.5),
            ('S15_Baia_Driver', Y_DRIVER,
             P['W_driver'] + 2 * f, P['L_driver'] + 2 * f, P['H_driver'] + 0.5)):
        sk = root.sketches.add(p_piso)
        sk.name = nome
        retangulo(sk, 0.0, y, lx, ly)
        extrudar(root, perfil_maior(sk), corpo(root, '02_Carcaca_Inferior'), prof,
                 adsk.fusion.FeatureOperations.CutFeatureOperation)

    p_face = plano_z(root, P['h_corpo'], 'P_FaceSuperior')

    sk = root.sketches.add(p_face)
    sk.name = 'S16_Rebaixo_NFC'
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(0, Y_NFC), (P['d_nfc'] + 1.0) * MM / 2)
    extrudar(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'),
             -(P['t_nfc'] + 0.2), adsk.fusion.FeatureOperations.CutFeatureOperation)

    sk = root.sketches.add(p_face)
    sk.name = 'S17_Rebaixo_QR'
    retangulo(sk, 0.0, Y_QR, LADO_QR, LADO_QR)
    extrudar(root, perfil_maior(sk), corpo(root, '01_Carcaca_Superior'), -PROF_REB,
             adsk.fusion.FeatureOperations.CutFeatureOperation)

    sk = root.sketches.add(p_face)
    sk.name = 'S18_Contatos'
    for sx in (-1, 1):
        sk.sketchCurves.sketchCircles.addByCenterRadius(
            pt(sx * XY_POGO[0], XY_POGO[1]), (P['d_pogo'] + 0.5) * MM / 2)
    extrudar(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'), -0.6,
             adsk.fusion.FeatureOperations.CutFeatureOperation)

    sk = root.sketches.add(p_face)
    sk.name = 'S19_Furos_Contato_LED'
    for sx in (-1, 1):
        sk.sketchCurves.sketchCircles.addByCenterRadius(
            pt(sx * XY_POGO[0], XY_POGO[1]), 2.0 * MM / 2)
    sk.sketchCurves.sketchCircles.addByCenterRadius(pt(0, Y_LED), D_LED * MM / 2)
    cortar_passante(root, todos_perfis(sk), corpo(root, '01_Carcaca_Superior'),
                    negativo=True)

    fm_garra = abs(Y_MCU) - (P['L_mcu'] / 2 + f) - D('d_alojamento') / 2
    fm_drv = (abs(Y_DRIVER) - (P['L_driver'] / 2 + f)) - (abs(Y_MCU) + P['L_mcu'] / 2 + f)
    fd_F4 = abs(FUROS[3][1]) - P['d_torre'] / 2 - (abs(Y_DRIVER) + P['L_driver'] / 2 + f)
    fl_F4 = abs(FUROS[3][1]) - P['d_cabeca_parafuso'] / 2 - (abs(Y_LED) + D_LED / 2)

    log.append("")
    log.append("BLOCO 5")
    log.append("  baia MCU    : %.1f x %.1f x %.1f em Y=%.0f"
               % (P['W_mcu'] + 2 * f, P['L_mcu'] + 2 * f, P['H_mcu'] + 0.5, Y_MCU))
    log.append("  baia driver : %.1f x %.1f x %.1f em Y=%.0f"
               % (P['W_driver'] + 2 * f, P['L_driver'] + 2 * f, P['H_driver'] + 0.5, Y_DRIVER))
    for txt, v in (("folga MCU-garra ", fm_garra), ("folga MCU-driver", fm_drv),
                   ("folga driver-F4 ", fd_F4), ("folga LED-F4    ", fl_F4)):
        log.append("  %s: %+.2f mm%s" % (txt, v, '' if v >= 0.3 else '   <-- APERTADO'))
    log.append("  contatos na face SUPERIOR em (+-%.0f, %.0f)" % XY_POGO)
    log.append("  area reservada do inlay: %.0f x %.0f na face inferior"
               % (P['L_inlay'] + 2, P['W_inlay'] + 2))


# ============================================================================
# PRINCIPAL
# ============================================================================

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        erros, camara = verificar_parametros()
        if erros:
            ui.messageBox('PARAMETROS INVALIDOS - nada foi modelado:\n\n'
                          + '\n\n'.join(erros), 'TagAndGo')
            return

        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent
        # o componente raiz nao pode ser renomeado pela API - ele herda o nome
        # do documento quando voce salvar (Ctrl+S -> TagAndGo_Prototipo)

        log = []
        criar_parametros(design, log)
        log.append("Camara de atuacao disponivel: %.2f mm" % camara)
        log.append("")

        body = bloco1(root, log)
        bloco2(root, body, log)
        bloco3(root, log)
        bloco4(root, log)
        bloco5(root, log)

        log.append("")
        log.append("BLOCOS 1 A 5 CONCLUIDOS. Corpos no modelo:")
        for b in root.bRepBodies:
            log.append("   %-24s %8.0f mm3" % (b.name, b.volume / (MM ** 3)))

        log.append("")
        log.append("MUDANCA EM RELACAO AO PROMPT DO BLOCO 3:")
        log.append("os 3 apoios de retencao da garra foram removidos - ao posicionar")
        log.append("o cursor eles caiam em cima dele. A garra fica retida pela pilha")
        log.append("bucha -> cursor -> teto, que e o caminho de carga real. Uma peca")
        log.append("a menos e um conflito a menos.")
        log.append("")
        log.append("Falta: promover a componentes, juntas e exportacao.")

        ui.messageBox('\n'.join(log), 'TagAndGo - relatorio')

    except:
        if ui:
            ui.messageBox('FALHOU:\n{}'.format(traceback.format_exc()), 'TagAndGo - erro')
