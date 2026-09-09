# -*- coding: utf-8 -*-
"""
ESTACAO DE LIBERACAO Tag&Go - esboco de massa e alojamentos
Projeto de Produto e Processo | Escola Politecnica da USP

COMO RODAR
----------
Shift+S -> aba Scripts -> Estacao -> Run
Ao final, uma janela mostra o relatorio: folgas, volumes e verificacoes.

O QUE ESTE SCRIPT FAZ
---------------------
Modela o gabinete, o berco de duas posicoes, os recortes de painel, a calha
e a caixa coletora - e coloca CADA COMPONENTE COMPRADO como um bloco-envelope,
para voce ver na hora se cabe e se colide.

Os componentes NAO sao detalhados de proposito: sao pecas de prateleira.
O que se projeta aqui e' o espaco onde elas entram.

PARA MUDAR QUALQUER MEDIDA
--------------------------
Edite o dicionario P (gabinete) ou COMP (componentes comprados) e rode de novo.
Cada execucao cria um documento NOVO.

>>> AS DIMENSOES MARCADAS [MEDIR] SAO ESTIMATIVAS. A mais critica e' a do
>>> desacoplador magnetico: o fornecedor nao publica. Meca no recebimento.

Todas as medidas em MILIMETROS. A API do Fusion usa centimetros; MM converte.
"""

import adsk.core
import adsk.fusion
import traceback
import math

MM = 0.1
TOL = 1e-4

# ============================================================================
# PARAMETROS DO GABINETE
# ============================================================================

P = {
    'larg':            300.0,   # X - largura externa
    'prof':            280.0,   # Y - profundidade externa (<=300, NBR 9050 9.4.3.5)
    'alt':             250.0,   # Z - altura externa
    't_parede':          6.0,   # MDF 6 mm
    'z_prateleira':    170.0,   # altura do plano onde fica o berco
    'prof_prateleira': 100.0,   # quanto a prateleira avanca a partir da frente
    'ang_painel':       20.0,   # inclinacao do painel frontal (graus da vertical)
    'folga':             1.0,   # folga geral em volta dos componentes
    'vao_max_guarda':    8.0,   # nenhuma abertura acessivel pode passar disto
    'sep_posicoes':    110.0,   # distancia entre POSICAO 1 (leitura) e 2 (destrave)
    'sep_min_ima':      80.0,   # o ima tem de estar a >= isto da tag na POSICAO 1
    'ang_calha':        35.0,   # inclinacao da calha de queda
}

# ============================================================================
# COMPONENTES COMPRADOS - envelope (X, Y, Z) em mm
# ============================================================================

COMP = {
    #  nome                     X      Y      Z    [MEDIR?]
    'desacoplador':         (130.0, 100.0,  60.0),   # [MEDIR] fornecedor nao publica
    'blindagem':            (120.0, 100.0,   3.0),   # chapa de aco-carbono
    'rc522':                 (60.0,  39.0,   5.0),
    'esp32':                 (52.0,  28.0,  20.0),   # com barras de pinos
    'lm2596':                (43.0,  21.0,  14.0),   # x2
    'servo_mg995':           (40.7,  19.7,  42.9),   # came do berco
    'servo_mg90s':           (22.8,  12.2,  28.5),   # x2: ejetor e portinhola
    'solenoide':             (55.0,  24.0,  28.0),
    'oled':                  (27.0,  27.0,   4.0),   # PCB; area visivel 22 x 11
    'buzzer':                (33.0,  15.0,  12.0),
    'protoboard':           (165.0,  55.0,  10.0),
    'bornes':                (80.0,  25.0,  25.0),
    'coletora':             (150.0, 120.0, 100.0),   # volume INTERNO, ~200 tags
}

# Etiqueta e berco
TAG = {
    'larg': 48.0,   # mini tag RF 8,2 MHz confirmada: 48 x 42 mm
    'prof': 42.0,
    'alt':  14.0,   # [MEDIR]
}
BERCO = {
    'larg': 55.0, 'prof': 50.0, 'alt': 20.0,   # cavidade
    'parede': 6.0,
    'rasgo_tecido': 4.0,                        # por onde passa a roupa
}

# Recortes do painel frontal
PAINEL = {
    'furo_botao':   25.0,   # ARMADILHA: a moldura tem 60 mm, o CORTE e' 25
    'moldura_botao':60.0,   # so para verificar que nao encosta em nada
    'furo_led':      5.0,
    'n_leds':          3,
    'passo_led':    22.0,
    'viseira':      30.0,   # aba sobre o OLED (NBR 9050 9.4.3.3)
    'furo_som':      6.0,
}

# Posicoes no plano XY (origem = centro da base do gabinete)
X_POS1 = -P['sep_posicoes'] / 2.0   # leitura   (RC522 embaixo)
X_POS2 = +P['sep_posicoes'] / 2.0   # destrave  (desacoplador embaixo)


# ============================================================================
# VERIFICACOES - rodam ANTES de modelar
# ============================================================================

def verificar():
    """Melhor falhar em 1 segundo do que depois de cortar MDF."""
    erros, avisos = [], []

    # 1. a separacao das posicoes garante o gating por distancia fisica?
    meia_tag = TAG['larg'] / 2.0
    meio_ima = COMP['desacoplador'][0] / 2.0
    vao = P['sep_posicoes'] - meia_tag - meio_ima
    if vao < P['sep_min_ima']:
        avisos.append(
            "Na POSICAO 1 a tag fica a %.0f mm da borda do desacoplador (alvo >= %.0f).\n"
            "  Aumente sep_posicoes para %.0f mm, ou aceite e MEA o campo no ensaio."
            % (vao, P['sep_min_ima'], P['sep_min_ima'] + meia_tag + meio_ima))

    # 2. o compartimento inferior comporta ima + coletora lado a lado?
    largura_util = P['larg'] - 2 * P['t_parede']
    soma = COMP['desacoplador'][0] + COMP['coletora'][0] + 4 * P['folga']
    if soma > largura_util:
        erros.append(
            "Desacoplador (%.0f) + caixa coletora (%.0f) nao cabem lado a lado em %.0f mm.\n"
            "  Solucao: aumentar larg para %.0f mm, ou empilhar a coletora atras."
            % (COMP['desacoplador'][0], COMP['coletora'][0], largura_util,
               soma + 2 * P['t_parede']))

    # 3. altura do compartimento inferior
    h_inferior = P['z_prateleira'] - P['t_parede']
    mais_alto = max(COMP['desacoplador'][2], COMP['coletora'][2], COMP['servo_mg995'][2])
    if mais_alto + 2 * P['folga'] > h_inferior:
        erros.append(
            "Componente de %.0f mm nao cabe no compartimento inferior de %.0f mm.\n"
            "  Solucao: subir z_prateleira para %.0f mm."
            % (mais_alto, h_inferior, mais_alto + 2 * P['folga'] + P['t_parede']))

    # 4. a cavidade do berco comporta a etiqueta?
    if TAG['larg'] + 2 * P['folga'] > BERCO['larg'] or TAG['prof'] + 2 * P['folga'] > BERCO['prof']:
        erros.append(
            "Etiqueta %.0f x %.0f nao cabe na cavidade %.0f x %.0f."
            % (TAG['larg'], TAG['prof'], BERCO['larg'], BERCO['prof']))

    # 5. guarda mecanica: o rasgo do tecido nao pode virar entrada de dedo
    if BERCO['rasgo_tecido'] > P['vao_max_guarda']:
        erros.append("Rasgo do tecido (%.0f mm) passa do vao maximo de guarda (%.0f mm)."
                     % (BERCO['rasgo_tecido'], P['vao_max_guarda']))

    # 6. o RC522 alcanca a etiqueta na POSICAO 1?
    dist_rc = BERCO['parede'] + P['t_parede']
    if dist_rc > 8.0:
        avisos.append(
            "RC522 a %.0f mm da etiqueta. Com adesivo de 23 mm o alcance real e' 10-20 mm:\n"
            "  esta apertado. Considere rebaixar o fundo do berco." % dist_rc)

    # 7. a moldura do botao cabe no painel sem encostar no OLED?
    if PAINEL['moldura_botao'] / 2.0 + COMP['oled'][0] / 2.0 > P['larg'] / 2.0 - P['t_parede']:
        avisos.append("Moldura do botao e OLED podem se sobrepor no painel - confira o layout.")

    return erros, avisos, vao


# ============================================================================
# UTILITARIOS (mesmo padrao do script da etiqueta)
# ============================================================================

def pt(x, y, z=0.0):
    return adsk.core.Point3D.create(x * MM, y * MM, z * MM)


def vr(mm):
    return adsk.core.ValueInput.createByReal(mm * MM)


def corpo(root, nome):
    for b in root.bRepBodies:
        if b.name == nome:
            return b
    raise RuntimeError('corpo nao encontrado: ' + nome)


def existe(root, nome):
    for b in root.bRepBodies:
        if b.name == nome:
            return True
    return False


def plano_z(root, z, nome):
    pl = root.constructionPlanes
    pi = pl.createInput()
    pi.setByOffset(root.xYConstructionPlane, vr(z))
    p = pl.add(pi)
    p.name = nome
    return p


def plano_y(root, y, nome):
    pl = root.constructionPlanes
    pi = pl.createInput()
    pi.setByOffset(root.xZConstructionPlane, vr(y))
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
        a = pr.areaProperties().area
        if a > area:
            melhor, area = pr, a
    col = adsk.core.ObjectCollection.create()
    col.add(melhor)
    return col


def retangulo(sk, cx, cy, lx, ly):
    return sk.sketchCurves.sketchLines.addTwoPointRectangle(
        pt(cx - lx / 2.0, cy - ly / 2.0), pt(cx + lx / 2.0, cy + ly / 2.0))


def extrudar(root, perfis, alvo, dist, op, nome=None):
    """dist negativo = sentido negativo do eixo do plano. alvo=None -> novo corpo."""
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
    ei = ext.createInput(perfis, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ei.participantBodies = [alvo]
    d = (adsk.fusion.ExtentDirections.NegativeExtentDirection if negativo
         else adsk.fusion.ExtentDirections.PositiveExtentDirection)
    ei.setAllExtent(d)
    return ext.add(ei)


NOVO = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
CORTE = adsk.fusion.FeatureOperations.CutFeatureOperation
JUNTA = adsk.fusion.FeatureOperations.JoinFeatureOperation


def bloco(root, nome, cx, cy, z0, lx, ly, lz):
    """Bloco-envelope de um componente comprado."""
    p = plano_z(root, z0, 'P_' + nome)
    sk = root.sketches.add(p)
    sk.name = 'S_' + nome
    retangulo(sk, cx, cy, lx, ly)
    extrudar(root, perfil_maior(sk), None, lz, NOVO, nome)


# ============================================================================
# BLOCO 1 - massa do gabinete (perfil lateral com painel inclinado)
# ============================================================================

def gabinete(root, log):
    y_f = -P['prof'] / 2.0          # frente
    y_t = +P['prof'] / 2.0          # tras
    z_p = P['z_prateleira']
    y_p = y_f + P['prof_prateleira']            # fundo da prateleira
    recuo = (P['alt'] - z_p) * math.tan(math.radians(P['ang_painel']))

    # perfil lateral no plano YZ: sketch local X = Y global, local Y = Z global
    sk = root.sketches.add(root.yZConstructionPlane)
    sk.name = 'S00_Perfil_Lateral'
    v = [(y_f, 0.0), (y_f, z_p), (y_p, z_p),
         (y_p + recuo, P['alt']), (y_t, P['alt']), (y_t, 0.0)]
    linhas = sk.sketchCurves.sketchLines
    for i in range(len(v)):
        a, b = v[i], v[(i + 1) % len(v)]
        linhas.addByTwoPoints(pt(a[0], a[1]), pt(b[0], b[1]))

    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfil_maior(sk), NOVO)
    ei.setSymmetricExtent(vr(P['larg']), True)
    f = ext.add(ei)
    body = f.bodies.item(0)
    body.name = '01_Gabinete'

    # ocar
    col = adsk.core.ObjectCollection.create()
    col.add(body)
    sh = root.features.shellFeatures
    si = sh.createInput(col, False)
    si.insideThickness = vr(P['t_parede'])
    sh.add(si)

    log.append("BLOCO 1 - gabinete")
    log.append("  envelope        : %.0f x %.0f x %.0f mm" % (P['larg'], P['prof'], P['alt']))
    log.append("  prateleira em Z = %.0f, profundidade %.0f" % (z_p, P['prof_prateleira']))
    log.append("  recuo do painel : %.1f mm (%.0f graus)" % (recuo, P['ang_painel']))
    log.append("  volume da casca : %.0f cm3" % (body.volume / 1000.0))
    return y_f, y_p, recuo


# ============================================================================
# BLOCO 2 - berco de duas posicoes
# ============================================================================

def berco(root, y_f, log):
    z_p = P['z_prateleira']
    y_c = y_f + P['prof_prateleira'] / 2.0    # centro da prateleira em Y

    # rasgo de curso: o berco corre entre POSICAO 1 e POSICAO 2
    largura_rasgo = P['sep_posicoes'] + BERCO['larg'] + 2 * P['folga']
    sk = root.sketches.add(plano_z(root, z_p, 'P_Prateleira'))
    sk.name = 'S01_Rasgo_Curso'
    retangulo(sk, 0.0, y_c, largura_rasgo, BERCO['prof'] + 2 * P['folga'])
    extrudar(root, perfil_maior(sk), corpo(root, '01_Gabinete'),
             -(BERCO['alt'] + BERCO['parede']), CORTE)

    # o berco propriamente dito, parado na POSICAO 1 (leitura)
    z0 = z_p - BERCO['alt'] - BERCO['parede']
    sk = root.sketches.add(plano_z(root, z0, 'P_BercoBase'))
    sk.name = 'S02_Berco_Corpo'
    retangulo(sk, X_POS1, y_c, BERCO['larg'] + 2 * BERCO['parede'],
              BERCO['prof'] + 2 * BERCO['parede'])
    extrudar(root, perfil_maior(sk), None, BERCO['alt'] + BERCO['parede'], NOVO, '02_Berco')

    # cavidade onde a etiqueta encaixa
    sk = root.sketches.add(plano_z(root, z0 + BERCO['parede'], 'P_BercoCav'))
    sk.name = 'S03_Berco_Cavidade'
    retangulo(sk, X_POS1, y_c, BERCO['larg'], BERCO['prof'])
    cortar_tudo(root, perfil_maior(sk), corpo(root, '02_Berco'))

    # batente assimetrico: forca uma unica orientacao da etiqueta
    sk = root.sketches.add(plano_z(root, z0 + BERCO['parede'], 'P_Batente'))
    sk.name = 'S04_Batente'
    retangulo(sk, X_POS1 + BERCO['larg'] / 2.0 - 4.0, y_c + BERCO['prof'] / 2.0 - 4.0, 8.0, 8.0)
    extrudar(root, perfil_maior(sk), corpo(root, '02_Berco'), BERCO['alt'] - 4.0, JUNTA)

    # rasgo lateral por onde passa o tecido
    sk = root.sketches.add(plano_z(root, z0 + BERCO['parede'] + 3.0, 'P_RasgoTecido'))
    sk.name = 'S05_Rasgo_Tecido'
    retangulo(sk, X_POS1, y_c - BERCO['prof'] / 2.0 - BERCO['parede'] / 2.0,
              BERCO['larg'] * 0.7, BERCO['parede'] + 2.0)
    extrudar(root, perfil_maior(sk), corpo(root, '02_Berco'), BERCO['rasgo_tecido'], CORTE)

    log.append("")
    log.append("BLOCO 2 - berco de duas posicoes")
    log.append("  POSICAO 1 (leitura)  em X = %+.0f" % X_POS1)
    log.append("  POSICAO 2 (destrave) em X = %+.0f" % X_POS2)
    log.append("  curso do came        : %.0f mm" % P['sep_posicoes'])
    log.append("  cavidade             : %.0f x %.0f x %.0f"
               % (BERCO['larg'], BERCO['prof'], BERCO['alt']))
    log.append("  rasgo do tecido      : %.0f mm" % BERCO['rasgo_tecido'])
    return y_c, z0


# ============================================================================
# BLOCO 3 - recortes do painel frontal
# ============================================================================

def painel(root, y_f, recuo, log):
    z_p = P['z_prateleira']
    z_painel = z_p + (P['alt'] - z_p) / 2.0
    y_painel = y_f + P['prof_prateleira'] + recuo / 2.0
    g = corpo(root, '01_Gabinete')

    # furos abertos ao longo de Y, atravessando o painel inclinado.
    # A 20 graus a abertura fica levemente eliptica - aceitavel num esboco.
    pl = plano_y(root, y_painel - 40.0, 'P_Painel')

    sk = root.sketches.add(pl)
    sk.name = 'S06_Painel_Recortes'
    # no sketch do plano XZ deslocado: local X = X global, local Y = Z global
    c = sk.sketchCurves
    # janela do OLED
    retangulo(sk, -70.0, z_painel + 22.0, COMP['oled'][0], COMP['oled'][1])
    # furo do botao arcade - CORTE de 25, nao os 60 da moldura
    c.sketchCircles.addByCenterRadius(pt(80.0, z_painel), PAINEL['furo_botao'] * MM / 2)
    # LEDs
    for i in range(PAINEL['n_leds']):
        x = -10.0 + i * PAINEL['passo_led']
        c.sketchCircles.addByCenterRadius(pt(x, z_painel + 30.0), PAINEL['furo_led'] * MM / 2)
    # saida de som
    c.sketchCircles.addByCenterRadius(pt(110.0, z_painel + 34.0), PAINEL['furo_som'] * MM / 2)
    cortar_tudo(root, todos_perfis(sk), g, negativo=True)

    # viseira sobre o OLED
    sk = root.sketches.add(plano_z(root, z_painel + 40.0, 'P_Viseira'))
    sk.name = 'S07_Viseira'
    retangulo(sk, -70.0, y_painel - 40.0 - PAINEL['viseira'] / 2.0,
              COMP['oled'][0] + 24.0, PAINEL['viseira'])
    extrudar(root, perfil_maior(sk), corpo(root, '01_Gabinete'), 5.0, JUNTA)

    log.append("")
    log.append("BLOCO 3 - painel frontal")
    log.append("  janela OLED   : %.0f x %.0f em X=-70" % (COMP['oled'][0], COMP['oled'][1]))
    log.append("  furo do botao : Ø%.0f  (moldura Ø%.0f - NAO furar 60)"
               % (PAINEL['furo_botao'], PAINEL['moldura_botao']))
    log.append("  %d LEDs Ø%.0f, passo %.0f" % (PAINEL['n_leds'], PAINEL['furo_led'],
                                                PAINEL['passo_led']))
    log.append("  viseira       : %.0f mm sobre o OLED" % PAINEL['viseira'])


# ============================================================================
# BLOCO 4 - calha, boca de coleta e gaveta
# ============================================================================

def coleta(root, y_f, y_c, log):
    g = corpo(root, '01_Gabinete')
    z_p = P['z_prateleira']
    x_col = -P['larg'] / 2.0 + P['t_parede'] + COMP['coletora'][0] / 2.0 + P['folga']

    # boca da gaveta na face frontal
    sk = root.sketches.add(plano_y(root, y_f, 'P_Frente'))
    sk.name = 'S08_Boca_Gaveta'
    retangulo(sk, x_col, COMP['coletora'][2] / 2.0 + 10.0,
              COMP['coletora'][0] + 2 * P['folga'], COMP['coletora'][2] + 2 * P['folga'])
    extrudar(root, perfil_maior(sk), g, P['t_parede'] + 2.0, CORTE)

    # duto de queda: do berco (POSICAO 1) ate a coletora
    dz = z_p - (COMP['coletora'][2] + 14.0)
    dy = dz / math.tan(math.radians(P['ang_calha']))
    sk = root.sketches.add(root.yZConstructionPlane)
    sk.name = 'S09_Calha'
    v = [(y_c, z_p), (y_c + dy, z_p - dz), (y_c + dy + 40.0, z_p - dz), (y_c + 40.0, z_p)]
    linhas = sk.sketchCurves.sketchLines
    for i in range(len(v)):
        a, b = v[i], v[(i + 1) % len(v)]
        linhas.addByTwoPoints(pt(a[0], a[1]), pt(b[0], b[1]))
    ext = root.features.extrudeFeatures
    ei = ext.createInput(perfil_maior(sk), CORTE)
    ei.participantBodies = [corpo(root, '01_Gabinete')]
    ei.setSymmetricExtent(vr(BERCO['larg']), True)
    ext.add(ei)

    log.append("")
    log.append("BLOCO 4 - coleta")
    log.append("  gaveta        : %.0f x %.0f x %.0f interno (~200 tags)" % COMP['coletora'])
    log.append("  calha a %.0f graus, queda de %.0f mm" % (P['ang_calha'], dz))
    log.append("  AVISO: a boca antirretorno (aba de silicone) NAO esta no CAD -")
    log.append("         e' peca flexivel, especificada em texto. Sem ela o cliente")
    log.append("         pega a etiqueta de volta e leva uma hard tag armada.")
    return x_col


# ============================================================================
# BLOCO 5 - componentes comprados, como blocos-envelope
# ============================================================================

def componentes(root, y_f, y_c, x_col, log):
    z_p = P['z_prateleira']
    y_tras = P['prof'] / 2.0 - P['t_parede']

    # --- compartimento inferior ---
    bloco(root, '90_Desacoplador', X_POS2, y_c,
          z_p - P['t_parede'] - COMP['desacoplador'][2] - 2.0, *COMP['desacoplador'])
    bloco(root, '91_Blindagem', X_POS1, y_c, z_p - P['t_parede'] - 12.0, *COMP['blindagem'])
    bloco(root, '92_RC522', X_POS1, y_c, z_p - P['t_parede'] - COMP['rc522'][2] - 1.0,
          *COMP['rc522'])
    bloco(root, '93_Coletora', x_col, y_f + COMP['coletora'][1] / 2.0 + P['t_parede'] + 2.0,
          8.0, *COMP['coletora'])

    # --- atuadores ---
    bloco(root, '94_Servo_MG995', 0.0, y_c,
          z_p - P['t_parede'] - COMP['servo_mg995'][2] - 30.0, *COMP['servo_mg995'])
    bloco(root, '95_Servo_MG90S_ejetor', X_POS1 + 45.0, y_c,
          z_p - P['t_parede'] - COMP['servo_mg90s'][2] - 4.0, *COMP['servo_mg90s'])
    bloco(root, '96_Servo_MG90S_portinhola', X_POS1 - 45.0, y_c,
          z_p - P['t_parede'] - COMP['servo_mg90s'][2] - 4.0, *COMP['servo_mg90s'])
    bloco(root, '97_Solenoide', X_POS1, y_c - BERCO['prof'] / 2.0 - 20.0,
          z_p + 4.0, *COMP['solenoide'])

    # --- compartimento eletronico (fundo, longe do ima) ---
    y_e = y_tras - 40.0
    bloco(root, '80_ESP32', -100.0, y_e, 20.0, *COMP['esp32'])
    bloco(root, '81_LM2596_a', -40.0, y_e, 20.0, *COMP['lm2596'])
    bloco(root, '82_LM2596_b', 5.0, y_e, 20.0, *COMP['lm2596'])
    bloco(root, '83_Protoboard', 0.0, y_e - 45.0, 20.0, *COMP['protoboard'])
    bloco(root, '84_Bornes', 100.0, y_e, 20.0, *COMP['bornes'])
    bloco(root, '85_Buzzer', 110.0, y_c, z_p + 20.0, *COMP['buzzer'])

    # --- interface ---
    z_painel = z_p + (P['alt'] - z_p) / 2.0
    bloco(root, '86_OLED', -70.0, y_f + P['prof_prateleira'] - 6.0, z_painel + 8.0,
          COMP['oled'][0], COMP['oled'][2], COMP['oled'][1])

    n = 0
    for b in root.bRepBodies:
        if b.name[0].isdigit() and int(b.name[0]) >= 8:
            n += 1
    log.append("")
    log.append("BLOCO 5 - componentes comprados")
    log.append("  %d blocos-envelope posicionados" % n)
    log.append("  nenhum foi detalhado: sao pecas de prateleira")


# ============================================================================
# PRINCIPAL
# ============================================================================

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        erros, avisos, vao = verificar()
        if erros:
            ui.messageBox('PARAMETROS INVALIDOS - nada foi modelado:\n\n'
                          + '\n\n'.join(erros), 'Estacao Tag&Go')
            return

        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent

        log = []
        y_f, y_p, recuo = gabinete(root, log)
        y_c, z0 = berco(root, y_f, log)
        painel(root, y_f, recuo, log)
        x_col = coleta(root, y_f, y_c, log)
        componentes(root, y_f, y_c, x_col, log)

        log.append("")
        log.append("VERIFICACOES")
        log.append("  tag <-> borda do ima na POSICAO 1: %.0f mm (alvo >= %.0f)"
                   % (vao, P['sep_min_ima']))
        log.append("  vao maximo de guarda             : %.0f mm" % P['vao_max_guarda'])
        log.append("  parede                           : %.0f mm (MDF)" % P['t_parede'])
        for a in avisos:
            log.append("")
            log.append("  AVISO: " + a.replace("\n", "\n  "))

        log.append("")
        log.append("CORPOS NO MODELO")
        for b in root.bRepBodies:
            log.append("   %-28s %8.1f cm3" % (b.name, b.volume / 1000.0))

        log.append("")
        log.append("O QUE ESTE ESBOCO NAO RESOLVE")
        log.append("  - dimensao real do desacoplador (fornecedor nao publica): MEDIR")
        log.append("  - o came do MG995 nao esta modelado, so o curso de 110 mm")
        log.append("  - a boca antirretorno da coletora e' peca flexivel, fora do CAD")
        log.append("  - furos de painel cortados na horizontal: a 20 graus ficam")
        log.append("    levemente elipticos. Aceitavel em esboco, refazer no detalhamento")

        ui.messageBox('\n'.join(log), 'Estacao Tag&Go - relatorio')

    except:
        if ui:
            ui.messageBox('FALHOU:\n{}'.format(traceback.format_exc()),
                          'Estacao Tag&Go - erro')
