# Gera 2-conteudo/25-fmea.tex (Entrega 4), com os NPR calculados a partir de S, O e D.
# Uso: python scripts/gerar_fmea.py. Para mudar um índice ou uma ação, altere as listas D (produto) e P (processo).
import os

# (função, modo de falha, efeito, S, causa, O, controle atual, D, ação, (S, O, D) previstos)
D = [
 ("Reter a peça", "O pino sai com menos de 120~N", "Peça levada sem pagamento", 8,
  "Embreagem fora da especificação ou pino revenido na fundição", 4, "Arrancamento por amostragem no Posto~4", 5,
  "Dureza e extração do pino na inspeção da garra (Tabela~\\ref{tab:proc_garra})", (8, 2, 3)),
 ("Reter a peça", "A garra sai dos mancais da tampa", "Peça levada sem pagamento", 8,
  "Mancais de PC/ABS cedem a uma alavanca (M7)", 5, "Nenhum", 6,
  "Ensaio de alavanca na homologação do produto. Eixo metálico TG-212 como reserva", (8, 2, 4)),
 ("Liberar a peça", "A embreagem não abre após o pagamento", "Cliente pagou e vai ao caixa", 7,
  "Folga acima do limite, ímã fraco ou prateleira empenada", 5, "Gaussímetro no recebimento. Teste de todos os subconjuntos", 3,
  "Gabarito FD-01, batente da prensa e plano de controle do suporte", (7, 2, 2)),
 ("Liberar a peça", "A embreagem abre sem ordem", "Peça levada sem pagamento", 9,
  "Ímã externo forte, como o de um destacador comercial", 6, "Antifurto da saída da loja", 6,
  "Chave da garra informa toda abertura sem ordem, e o servidor alerta a equipe da loja", (9, 5, 3)),
 ("Liberar a peça", "O ímã não volta ao repouso", "Dispositivo destravado na próxima peça", 8,
  "Microatuador falha ou célula com tensão baixa", 3, "Teste funcional na montagem", 5,
  "\\textit{Firmware} só gira com tensão acima do mínimo e confirma o retorno antes de informar travado", (8, 2, 3)),
 ("Identificar o dispositivo", "O celular não lê o código 2D", "Cliente vai ao caixa", 5,
  "Gravação gasta pelo uso", 4, "Leitura de todos os códigos no Posto~0", 3,
  "Releitura e regravação no recondicionamento", (5, 3, 2)),
 ("Comunicar com o servidor", "A ordem não chega ao dispositivo", "Compra termina pela via humana", 6,
  "Cobertura de rádio insuficiente no salão", 5, "Nenhum", 4,
  "Mapear a cobertura na instalação de cada loja. Tempo-limite na página de compra (E08)", (6, 3, 3)),
 ("Suprir energia", "A célula acaba antes de 168 dias (E13)", "Dispositivo não libera", 7,
  "Corrente de espera acima da prevista", 4, "Nenhum", 5,
  "Corrente de espera medida na homologação. Aviso de carga baixa ao servidor", (7, 2, 3)),
 ("Suprir energia", "A célula aquece ou é danificada", "Risco de fogo", 10,
  "Indução aquece peças metálicas, ou esmagamento", 2, "Proteção da célula", 5,
  "Célula IEC 62133-2 e sensor de temperatura que corta a recarga", (10, 1, 3)),
 ("Preservar a roupa", "A garra marca o tecido", "Peça devolvida, custo para a loja", 6,
  "Dentes agressivos ou mola forte", 4, "Nenhum", 5,
  "Homologar em tecido leve, malha e jeans da Riachuelo", (6, 3, 3)),
 ("Proteger o mecanismo", "A tampa é aberta por terceiros", "Liberação sem pagamento", 8,
  "Parafusos comuns", 3, "Chave da garra", 6,
  "Parafusos hexalobulares e registro de abertura sem ordem", (8, 2, 5)),
]
P = [
 ("Injeção do suporte (op.~20)", "Prateleira empenada ou fora da espessura", "Folga fora da tolerância", 7,
  "Contração do poliacetal, resfriamento desigual", 5, "Inspeção da op.~50", 4,
  "Cpk mínimo de 1,33 no \\textit{try-out}. Medição após 24~h", (7, 3, 2)),
 ("Fundição da garra (op.~10 e 20)", "Pino revenido ou inclinado", "Retenção cai ou o pino não entra na tampa", 8,
  "Calor do alumínio, bucha do molde gasta", 4, "Visual", 6,
  "Dureza, perpendicularidade e extração na op.~70. Troca programada da bucha", (8, 2, 3)),
 ("Colagem do ímã (op.~0.4 a 0.6)", "O ímã descola em uso", "Dispositivo não libera", 7,
  "Alojamento sujo, dose errada ou cura incompleta", 4, "Nenhum", 6,
  "Desengraxe, rugosidade no DE-05, cisalhamento por lote e registro da estufa", (7, 2, 3)),
 ("Colagem do ímã (op.~0.5)", "Altura do conjunto fora da tolerância", "Folga fora da tolerância", 7,
  "Ímã fora do fundo do ninho", 4, "Teste do subconjunto", 3,
  "Pastilha de aço no FD-01 e medição de um braço por placa", (7, 2, 3)),
 ("Prensagem do braço (op.~1.4)", "Braço fora da altura ou solto", "Folga fora da tolerância", 7,
  "Batente desregulado ou interferência baixa (M3)", 4, "Teste do subconjunto", 3,
  "Aferir o batente por turno. Torque de arraste por amostragem", (7, 2, 3)),
 ("Montagem da célula (op.~3.3)", "Célula perfurada", "Risco de fogo", 10,
  "Ferramenta pontiaguda ou célula fora de posição", 2, "Visual", 4,
  "Nervuras de posição na base. Posto sem ferramenta metálica", (10, 1, 4)),
 ("Aperto dos parafusos (op.~3.8)", "Rosca espanada na torre", "Tampa abre com pouco esforço", 6,
  "Torque acima do limite", 4, "Parafusadeira com torque", 4,
  "Torque definido na homologação. Aferição por turno", (6, 2, 3)),
 ("Cadastro (op.~4.2)", "Código vinculado a outra placa", "Cliente paga e outro dispositivo abre", 9,
  "Dois dispositivos na bancada", 3, "Teste funcional", 3,
  "O cadastro acende o LED do dispositivo vinculado. Um por vez na bancada", (9, 2, 2)),
]

cols = r"""@{}
    >{\RaggedRight\arraybackslash}p{0.6cm}
    >{\RaggedRight\arraybackslash}p{2.0cm}
    >{\RaggedRight\arraybackslash}p{2.6cm}
    >{\RaggedRight\arraybackslash}p{2.4cm}
    c
    >{\RaggedRight\arraybackslash}p{3.0cm}
    c
    >{\RaggedRight\arraybackslash}p{2.6cm}
    c c
    >{\RaggedRight\arraybackslash}p{4.6cm}
    c c c c@{}"""
head = (r"\textbf{Nº} & \textbf{%s} & \textbf{Modo de falha} & \textbf{Efeito} & \textbf{S} & \textbf{Causa} & "
        r"\textbf{O} & \textbf{Controle atual} & \textbf{D} & \textbf{NPR} & \textbf{Ação} & \textbf{S} & \textbf{O} & \textbf{D} & \textbf{NPR} \\")


def linhas(rows, pref):
    out, res = [], []
    for i, (f, m, e, S, c, O, ctl, Dt, ac, (s2, o2, d2)) in enumerate(rows, 1):
        npr, n2, cod = S * O * Dt, s2 * o2 * d2, f"{pref}{i:02d}"
        out.append(f"    {cod} & {f} & {m} & {e} & {S} & {c} & {O} & {ctl} & {Dt} & \\textbf{{{npr}}} & {ac} & {s2} & {o2} & {d2} & \\textbf{{{n2}}} \\\\")
        res.append((cod, m, S, npr, n2))
    return "\n    \\addlinespace\n".join(out), res


def tabela(rows, pref, cap, lab, col2):
    body, res = linhas(rows, pref)
    h = head % col2
    top = rf"""    \toprule
    & & & & & & & & & & & \multicolumn{{4}}{{c}}{{\textbf{{Após a ação}}}} \\
    \cmidrule(l){{12-15}}
    {h}
    \midrule"""
    return rf"""\begin{{landscape}}
\begingroup
\scriptsize
\setlength{{\tabcolsep}}{{3pt}}
\renewcommand{{\arraystretch}}{{1.2}}
\begin{{longtable}}{{{cols}}}
    \caption{{{cap}}}\label{{{lab}}}\\
{top}
    \endfirsthead
{top}
    \endhead
    \bottomrule
    \endfoot
{body}
\end{{longtable}}
\endgroup
\begin{{center}}
    \footnotesize Fonte: Elaborado pelos autores (2026). S: severidade. O: ocorrência. D: detecção. NPR: número de prioridade de risco.
\end{{center}}
\end{{landscape}}""", res


td, rd = tabela(D, 'D', "FMEA de produto do Tag\\&Go", "tab:fmea_produto", "Função")
tp, rp = tabela(P, 'P', "FMEA de processo do Tag\\&Go", "tab:fmea_processo", "Operação")
allr = rd + rp
antes, depois = sum(r[3] for r in allr), sum(r[4] for r in allr)
acima = [r for r in allr if r[3] >= 100]
sev = [r for r in allr if r[2] >= 9 and r[3] < 100]
resta = [r[0] for r in allr if r[4] >= 100]
for r in sorted(allr, key=lambda x: -x[3]):
    print(r[0], r[2], r[3], '->', r[4], '|', r[1])
print('soma', antes, depois, '| >=100:', len(acima), '| S>=9 abaixo de 100:', [r[0] for r in sev], '| restam:', resta)

intro = rf"""\section{{FMEA DE PRODUTO E DE PROCESSO (ENTREGA 4)}}\label{{sec:fmea}}

% Arquivo gerado por scripts/gerar_fmea.py. Não edite à mão: altere o script e rode de novo.

O FMEA entra no projeto detalhado como parte da avaliação dos sistemas, subsistemas e componentes. Para cada função do produto e cada operação do processo, levantam-se os modos de falha, os efeitos e as causas, pontuam-se a severidade (S), a ocorrência (O) e a detecção (D), e o produto dos três índices, o número de prioridade de risco (NPR), ordena as ações \cite{{rozenfeld2006gestao}}. A equipe usou escalas de 1 a 10 (Tabela~\ref{{tab:fmea_escalas}}) e tratou todo modo de falha com NPR de 100 ou mais e todo modo com severidade de 9 ou mais, qualquer que fosse o NPR.

\begin{{table}}[htbp]
    \centering
    \caption{{Escalas de severidade, ocorrência e detecção}}
    \label{{tab:fmea_escalas}}
    \footnotesize
    \renewcommand{{\arraystretch}}{{1.3}}
    \begin{{tabularx}}{{\textwidth}}{{@{{}}
        c
        >{{\RaggedRight\arraybackslash}}X
        >{{\RaggedRight\arraybackslash}}p{{3.2cm}}
        >{{\RaggedRight\arraybackslash}}X@{{}}}}
        \toprule
        \textbf{{Índice}} & \textbf{{Severidade}} & \textbf{{Ocorrência}} & \textbf{{Detecção}} \\
        \midrule
        1 a 2 & Ninguém percebe & Remota & Detectada em todas as unidades \\
        3 a 4 & Incômodo, sem perder a compra & Rara & Teste de todas as unidades \\
        5 a 6 & A compra termina no caixa, ou há custo para a loja & Ocasional & Amostragem ou inspeção visual \\
        7 a 8 & A peça paga não sai, ou a não paga é levada & Frequente & Controle indireto \\
        9 a 10 & Furto sem registro, cobrança errada ou risco às pessoas & Quase certa & Sem controle, aparece no uso \\
        \bottomrule
    \end{{tabularx}}
    \source{{Elaborado pelos autores (2026).}}
\end{{table}}

As Tabelas~\ref{{tab:fmea_produto}} e~\ref{{tab:fmea_processo}} trazem as duas análises. O FMEA de produto percorre as funções dos sistemas da estrutura revisada, e o de processo, as operações das fichas e do plano macro que podem gerar aquelas falhas.

"""

fim = rf"""

\subsection{{Pontos críticos e providências}}
\label{{subsec:fmea_criticos}}

Dos {len(allr)} modos de falha, {len(acima)} tinham NPR de 100 ou mais, e outros {len(sev)} entraram pela severidade. A Tabela~\ref{{tab:fmea_providencias}} resume as providências que já constam dos documentos desta entrega e as que ficam para a homologação do produto. Com elas, a soma dos NPR cai de {antes} para {depois}, e só um modo continua acima de 100.

\begin{{table}}[htbp]
    \centering
    \caption{{Providências do FMEA}}
    \label{{tab:fmea_providencias}}
    \footnotesize
    \renewcommand{{\arraystretch}}{{1.3}}
    \begin{{tabularx}}{{\textwidth}}{{@{{}}
        >{{\RaggedRight\arraybackslash}}p{{2.4cm}}
        >{{\RaggedRight\arraybackslash}}X
        >{{\RaggedRight\arraybackslash}}p{{4.6cm}}@{{}}}}
        \toprule
        \textbf{{Modos}} & \textbf{{Providência}} & \textbf{{Onde está}} \\
        \midrule
        D03, P04, P05 & Gabarito que fixa a altura do ímã e batente da prensa & Seção~\ref{{sec:projeto_dispositivo}} e DE-07 \\
        D03, P01 & Características críticas e plano de controle do suporte & DE-03 e Seção~\ref{{sec:controle_qualidade}} \\
        D01, P02 & Dureza, perpendicularidade e extração do pino & Ficha da garra, op.~70 \\
        D09, P06 & Célula certificada, sensor de temperatura e nervuras de posição & Tabela~\ref{{tab:ext_lista}} e DE-01 \\
        D11 & Parafusos hexalobulares & Tabela~\ref{{tab:ext_lista}} \\
        P03 & Rugosidade do alojamento e cura em estufa & DE-05 e Tabela~\ref{{tab:disp_uso}} \\
        \midrule
        D02, D08, D10, P07 & Ensaios de alavanca, corrente de espera, tecido e torque & Homologação do produto \\
        D04, D05, P08 & Regras do \textit{{firmware}} e do \textit{{software}} de cadastro & Especificação da placa \\
        D07 & Mapa de cobertura de rádio e tempo-limite na página de compra & Instalação de cada loja \\
        \bottomrule
    \end{{tabularx}}
    \source{{Elaborado pelos autores (2026).}}
\end{{table}}

O modo que sobra é a abertura da embreagem por um ímã externo (D04). Destacadores capazes de abrir etiquetas rígidas são vendidos livremente \cite{{cablematic2026xy021}}, e o Tag\&Go herda essa fragilidade porque retém a peça pelo mesmo princípio. A diferença é que ele percebe a abertura: a chave da garra avisa o servidor, que distingue a abertura com ordem da abertura sem ordem. A providência melhora a detecção, mas não a ocorrência. Uma blindagem de aço sobre a embreagem reduziria a ocorrência, só que ela também enfraquece o campo do próprio ímã do dispositivo, e a equipe preferiu não adotá-la sem medir esse efeito.

Três dos riscos maiores (D01, D02 e P02) vêm das mudanças M2 e M7 do DFMA, que integraram o pino à garra fundida e trocaram o eixo metálico por mancais de plástico. As duas reduziram peças e tempo de montagem, e as duas mexem na retenção, que é a função que a loja mais cobra. Por isso o eixo metálico da versão anterior ao DFMA (TG-212) ficou como reserva, caso o ensaio de alavanca da homologação reprove os mancais.
"""

open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2-conteudo', '25-fmea.tex'), 'w', encoding='utf-8').write(intro + td + "\n\n" + tp + fim)
