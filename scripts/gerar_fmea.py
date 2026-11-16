# Gera 2-conteudo/25-fmea.tex (Entrega 4), com os NPR calculados a partir de S, O e D.
# Uso: python scripts/gerar_fmea.py. Para mudar um índice ou uma ação, altere as listas D (produto) e P (processo).
D = [
 ("Reter a peça (TG-200)","O pino sai da embreagem ou da garra com menos de 120~N","A peça é levada sem pagamento, e a loja perde a confiança no dispositivo",8,"Embreagem fora da especificação, ou pino com dureza baixa, revenido na fundição da garra (M2)",4,"Ensaio de arrancamento por amostragem (operação 4.4)",5,"Medir a dureza do pino depois da fundição e ensaiar a extração (ficha da garra, operação 70). Fazer o ensaio E12 em cinco exemplares antes de congelar o projeto. Alternativa: pino prensado",(8,2,3)),
 ("Reter a peça (TG-200)","A garra é arrancada dos mancais da tampa","A peça é levada sem pagamento",8,"Os mancais de PC/ABS cedem ao esforço de alavanca na garra (M7)",5,"Nenhum. A verificação da M7 está pendente",6,"Ensaiar o arrancamento com alavanca na garra. Se reprovar, voltar ao eixo metálico (TG-212) da versão anterior ao DFMA",(8,2,4)),
 ("Liberar a peça (TG-300)","A embreagem não abre depois do pagamento confirmado","O cliente pagou e não consegue levar a peça. A compra termina pela via humana (E08 e E09)",7,"Campo insuficiente sob a embreagem: folga acima do limite, ímã fraco ou prateleira empenada",5,"Gaussímetro no recebimento. Teste de todos os subconjuntos (operação 1.6) e teste funcional (operação 4.3)",3,"Fazer o ensaio do campo antes de congelar o projeto. Gabarito FD-01 e batente da prensa. Características críticas do suporte no plano de controle. Alternativa: lingueta de plástico",(7,2,2)),
 ("Liberar a peça (TG-300)","A embreagem abre sem ordem do servidor","A peça é levada sem pagamento",9,"Um ímã externo forte, como o de um destacador comercial, abre a embreagem pela face da tampa",6,"Chave da garra. Antifurto da saída da loja, que não pertence ao produto",6,"Registrar no servidor toda abertura da garra sem ordem de liberação e avisar a equipe da loja. Avaliar uma blindagem de aço na tampa, sobre a embreagem, no ensaio do campo",(9,5,3)),
 ("Liberar a peça (TG-300)","O ímã não volta à posição de repouso","O dispositivo fica destravado e não retém a próxima peça",8,"Falha do microatuador ou tensão baixa da célula durante o giro",3,"Teste funcional (operação 4.3), só na montagem",5,"O \\textit{firmware} só gira se a tensão da célula estiver acima do mínimo e só informa o estado travado depois de comandar o retorno com a garra fechada. Na dúvida, informa erro",(8,2,3)),
 ("Identificar o dispositivo (código 2D)","O celular não lê o código","O cliente não inicia a compra e vai ao caixa",5,"Gravação riscada ou com pouco contraste depois de vários ciclos de uso",4,"Leitura de todos os códigos no Posto~0 (operação 0.3)",3,"Ensaiar a abrasão da gravação e ler o código depois. Reler o código no recondicionamento",(5,3,2)),
 ("Indicar o estado (TG-400)","O estado não é visto ou é confundido","O cliente não sabe se a peça foi liberada",5,"Guia de luz desalinhada do LED, ou luz ambiente forte",3,"Teste funcional (operação 4.3)",3,"Repetir o estado na página do celular, como segundo canal (E16)",(5,2,3)),
 ("Comunicar com o servidor (TG-511)","A ordem de liberação não chega ao dispositivo","O cliente espera, e a compra termina pela via humana",6,"Cobertura de rádio insuficiente no salão ou interferência",5,"Nenhum ensaio em loja",4,"Medir a cobertura na loja piloto. Tempo-limite na página de compra, com mensagem e chamada da via humana (E08)",(6,3,3)),
 ("Suprir energia (TG-520)","A célula descarrega antes do fim do ciclo de 168 dias (E13)","O dispositivo não libera a peça",7,"Corrente de espera acima da prevista",4,"Nenhum. A corrente de espera ainda não foi medida",5,"Medir a corrente de espera no protótipo. Aviso de carga baixa ao servidor, para a recarga na loja",(7,2,3)),
 ("Suprir energia (TG-520)","A célula aquece ou é danificada","Risco de fogo no salão ou no estoque",10,"Aquecimento de peças metálicas pela indução durante a recarga, ou esmagamento em tentativa de arrombamento",2,"Circuito de proteção da célula. Afastamento de 33~mm entre o ímã e a bobina",5,"Ensaio térmico da recarga. Célula certificada pela IEC 62133-2. Sensor de temperatura na placa, que interrompe a recarga",(10,1,3)),
 ("Preservar a peça de roupa (TG-210)","A garra marca ou rasga o tecido","Peça danificada e devolvida, com custo para a loja",6,"Dentes e pino agressivos para tecidos leves, ou mola forte demais",4,"Nenhum ensaio em tecido",5,"Ensaiar em tecido leve, em malha e em jeans da Riachuelo. Avaliar a variante com o pino ao lado do tecido",(6,3,3)),
 ("Proteger o mecanismo (TG-100)","A tampa é aberta por terceiros","Acesso ao mecanismo e liberação da peça sem pagamento",8,"Dois parafusos de fenda comum",3,"Chave da garra, depois da abertura",6,"Parafusos de fenda hexalobular, já na especificação. Avaliar a versão de segurança, com pino central. Abertura sem ordem registrada no servidor",(8,2,5)),
]
P = [
 ("Injeção do suporte (ficha TG-113, operação 20)","Prateleira empenada ou fora da espessura","Folga do ímã fora da tolerância. O dispositivo não libera",7,"Contração do poliacetal e resfriamento desigual do molde",5,"Inspeção das características críticas (operação 50)",4,"\\textit{Try-out} com 30 peças e cálculo da capacidade do processo. Medição depois de 24~h. Plano de controle da Seção~\\ref{sec:controle_qualidade}",(7,3,2)),
 ("Fundição da garra (ficha TG-211, operações 10 e 20)","Pino revenido ou inclinado","A retenção cai, ou o pino não entra no furo da tampa",8,"Calor do alumínio sobre o pino. Bucha de posição do molde gasta",4,"Visual",6,"Dureza, perpendicularidade e extração do pino na operação 70. Troca programada da bucha",(8,2,3)),
 ("Usinagem do braço (ficha TG-312, operações 30 e 40)","Distância de 16,00~mm fora da tolerância","O ímã para fora do eixo da embreagem",6,"Placa solta depois do faceamento",2,"Fixação única. Projetor de perfil por amostragem (operação 80)",3,"Manter o plano",(6,2,3)),
 ("Colagem do ímã (operações 0.4 a 0.6)","O ímã descola em uso","O dispositivo não libera, e o ímã fica solto na carcaça",7,"Alojamento sujo, dose errada de adesivo ou cura incompleta",4,"Nenhum",6,"Desengraxar o braço. Rugosidade do alojamento no desenho DE-05. Ensaio de cisalhamento por lote de colagem. Tempo de cura registrado",(7,2,3)),
 ("Colagem do ímã (operação 0.5)","Altura do conjunto fora da tolerância","Folga do ímã fora da tolerância",7,"Ímã fora do fundo do ninho, ou adesivo curado no ninho",4,"Teste do subconjunto (operação 1.6)",3,"Gabarito FD-01, com pastilha de aço e limpeza dos ninhos. Conferência de um braço por placa",(7,2,3)),
 ("Prensagem do braço (operação 1.4)","Braço fora da altura ou solto no eixo","Folga fora da tolerância, ou braço que se desloca em uma queda",7,"Batente desregulado, ou interferência insuficiente no furo (M3)",4,"Teste do subconjunto (operação 1.6)",3,"Aferir o batente a cada turno. Ensaiar o torque de arraste do braço no eixo por amostragem. Ensaio de queda do dispositivo",(7,2,3)),
 ("Montagem da célula (operação 3.3)","Célula perfurada ou esmagada","Risco de fogo",10,"Ferramenta pontiaguda, ou célula fora das nervuras de posição",2,"Visual",4,"Nervuras de posição na base (DE-01). Procedimento de manuseio, sem ferramenta metálica no posto",(10,1,4)),
 ("Ligação dos conectores (operação 3.6)","Conector trocado ou mal encaixado","O dispositivo não funciona",5,"Quatro conectores parecidos, ligados à mão",4,"Testes de todas as unidades no Posto~4",2,"Conectores polarizados e de tamanhos diferentes, na especificação da placa",(5,2,2)),
 ("Aperto dos parafusos (operação 3.8)","Rosca espanada na torre de PC/ABS","A tampa abre com pouco esforço",6,"Torque acima do limite da torre",4,"Parafusadeira com controle de torque",4,"Definir o torque em ensaio com a base injetada. Aferir a parafusadeira a cada turno",(6,2,3)),
 ("Gravação do código 2D (operação 0.2)","Código gravado diferente do endereço registrado","O cliente paga por um dispositivo e outro é liberado",9,"Erro na fila de gravação",2,"Leitura de todos os códigos (operação 0.3) e vínculo no cadastro (operação 4.2)",2,"Manter o plano",(9,2,2)),
 ("Cadastro do dispositivo (operação 4.2)","Código vinculado à placa de outro dispositivo","O cliente paga por um dispositivo e outro é liberado",9,"Dois dispositivos na bancada no momento do vínculo",3,"Teste funcional (operação 4.3)",3,"O \\textit{software} de cadastro acende o LED do dispositivo vinculado, e o teste funcional é comandado pelo código lido. Um dispositivo por vez na bancada",(9,2,2)),
]
def linhas(rows, pref):
    out=[]; resumo=[]
    for i,r in enumerate(rows,1):
        f,m,e,S,c,O,ctl,Dt,ac,(s2,o2,d2)=r
        npr=S*O*Dt; n2=s2*o2*d2
        cod=f"{pref}{i:02d}"
        out.append(f"    {cod} & {f} & {m} & {e} & {S} & {c} & {O} & {ctl} & {Dt} & \\textbf{{{npr}}} & {ac} & {s2} & {o2} & {d2} & \\textbf{{{n2}}} \\\\")
        resumo.append((cod,f,m,S,npr,n2))
    return "\n    \\addlinespace\n".join(out), resumo
cols = r"""@{}
    >{\RaggedRight\arraybackslash}p{0.65cm}
    >{\RaggedRight\arraybackslash}p{2.0cm}
    >{\RaggedRight\arraybackslash}p{2.3cm}
    >{\RaggedRight\arraybackslash}p{2.5cm}
    c
    >{\RaggedRight\arraybackslash}p{3.1cm}
    c
    >{\RaggedRight\arraybackslash}p{2.7cm}
    c c
    >{\RaggedRight\arraybackslash}p{4.9cm}
    c c c c@{}"""
head = r"\textbf{Nº} & \textbf{%s} & \textbf{Modo de falha} & \textbf{Efeito} & \textbf{S} & \textbf{Causa} & \textbf{O} & \textbf{Controle atual} & \textbf{D} & \textbf{NPR} & \textbf{Ação recomendada ou já tomada} & \textbf{S} & \textbf{O} & \textbf{D} & \textbf{NPR} \\"
def tabela(rows, pref, cap, lab, col2):
    body,res = linhas(rows,pref)
    h = head % col2
    return rf"""\begingroup
\scriptsize
\setlength{{\tabcolsep}}{{3pt}}
\renewcommand{{\arraystretch}}{{1.2}}
\begin{{longtable}}{{{cols}}}
    \caption{{{cap}}}\label{{{lab}}}\\
    \toprule
    & & & & & & & & & & & \multicolumn{{4}}{{c}}{{\textbf{{Previsto após a ação}}}} \\
    \cmidrule(l){{12-15}}
    {h}
    \midrule
    \endfirsthead
    \toprule
    & & & & & & & & & & & \multicolumn{{4}}{{c}}{{\textbf{{Previsto após a ação}}}} \\
    \cmidrule(l){{12-15}}
    {h}
    \midrule
    \endhead
    \bottomrule
    \endfoot
{body}
\end{{longtable}}
\endgroup
\begin{{center}}
    \footnotesize Fonte: Elaborado pelos autores (2026). S: severidade. O: ocorrência. D: detecção. NPR: número de prioridade de risco. Índices estimados pela equipe.
\end{{center}}""", res
td, rd = tabela(D,'D',"FMEA de produto do Tag\\&Go","tab:fmea_produto","Função")
tp, rp = tabela(P,'P',"FMEA de processo do Tag\\&Go","tab:fmea_processo","Operação")
allr = rd+rp
import json, os, tempfile
json.dump(allr, open(os.path.join(tempfile.gettempdir(), 'fmea_resumo.json'),'w'), ensure_ascii=False, indent=1)

for r in sorted(allr,key=lambda x:-x[4]): print(r[0],r[3],r[4],'->',r[5], '|', r[2][:50])
print('soma antes',sum(r[4] for r in allr),'depois',sum(r[5] for r in allr), 'n>=100:',sum(r[4]>=100 for r in allr),'depois',sum(r[5]>=100 for r in allr))

intro = r"""\section{FMEA DE PRODUTO E DE PROCESSO (ENTREGA 4)}\label{sec:fmea}

% Tabelas geradas por script: os NPR são o produto S x O x D de cada linha.
% TODO (equipe): rever os índices em reunião, com o resultado dos ensaios. Os índices de ocorrência são julgamento, não frequência medida.

Esta seção aplica a análise dos modos de falha e seus efeitos (FMEA) ao Tag\&Go, para definir os pontos críticos do produto e do processo e as providências para eliminá-los ou administrá-los. No projeto detalhado, o FMEA faz parte da avaliação dos sistemas, subsistemas e componentes: para cada função, a equipe levanta os modos de falha, os efeitos e as causas, pontua a severidade, a ocorrência e a detecção e usa o produto dos três índices para priorizar as ações \cite{rozenfeld2006gestao}.

\subsection{Método e escalas}
\label{subsec:fmea_metodo}

A equipe fez duas análises. O FMEA de produto percorre as funções dos cinco sistemas da estrutura (Tabela~\ref{tab:dfma_estrutura}) e a função de identificação, que não tem sistema próprio. O FMEA de processo percorre as operações das fichas de processo (Seção~\ref{sec:planos_processo}) e do plano macro de montagem (Tabela~\ref{tab:plano_macro}). Cada linha recebe um código, com a letra D para o produto e a letra P para o processo.

Os três índices vão de 1 a 10, pelas escalas da Tabela~\ref{tab:fmea_escalas}. O número de prioridade de risco (NPR) é o produto dos três. A equipe adotou dois critérios de ação: tratar todo modo de falha com NPR igual ou superior a 100 e tratar todo modo de falha com severidade igual ou superior a 9, qualquer que seja o NPR.

\begin{table}[htbp]
    \centering
    \caption{Escalas de severidade, ocorrência e detecção}
    \label{tab:fmea_escalas}
    \footnotesize
    \renewcommand{\arraystretch}{1.3}
    \begin{tabularx}{\textwidth}{@{}
        c
        >{\RaggedRight\arraybackslash}X
        >{\RaggedRight\arraybackslash}X
        >{\RaggedRight\arraybackslash}X@{}}
        \toprule
        \textbf{Índice} & \textbf{Severidade (S)} & \textbf{Ocorrência (O)} & \textbf{Detecção (D)} \\
        \midrule
        1 a 2 & O cliente e a loja não percebem & Remota. Falha improvável & O controle atual detecta quase sempre, em todas as unidades \\
        3 a 4 & Incômodo leve, sem perda da compra & Baixa. Falha rara & Detecção provável, em teste de todas as unidades \\
        5 a 6 & A compra termina pelo caixa ou pela via humana, ou há custo para a loja & Moderada. Falha ocasional & Detecção por amostragem ou por inspeção visual \\
        7 a 8 & A função principal se perde: a peça paga não é liberada, ou a peça não paga é levada & Alta. Falha frequente & Detecção improvável. O controle é indireto ou está pendente \\
        9 a 10 & Furto sem registro, cobrança errada ou risco à segurança das pessoas & Muito alta. Falha quase certa & Não há controle, ou a falha só aparece no uso \\
        \bottomrule
    \end{tabularx}
    \source{Elaborado pelos autores (2026).}
\end{table}

Os índices são estimativas da equipe. O produto ainda não tem histórico de falhas, e nenhum ensaio foi feito, de modo que a ocorrência expressa julgamento, e não frequência medida. As colunas da direita das tabelas trazem os índices previstos depois das ações. Eles são metas: só valem quando a ação for executada e o ensaio confirmar o efeito.

\subsection{FMEA de produto}
\label{subsec:fmea_produto}

A Tabela~\ref{tab:fmea_produto} apresenta o FMEA de produto. Os códigos de operação citados na coluna de controle são os do plano macro.

\begin{landscape}
"""
mid = r"""
\end{landscape}

\subsection{FMEA de processo}
\label{subsec:fmea_processo}

A Tabela~\ref{tab:fmea_processo} apresenta o FMEA de processo, com as operações de fabricação dos três itens críticos e as operações de montagem que podem gerar os modos de falha do produto.

\begin{landscape}
"""
top = sorted(allr, key=lambda x: -x[4])
n100 = [r for r in allr if r[4] >= 100]
s9 = [r for r in allr if r[3] >= 9 and r[4] < 100]
print('>=100', [r[0] for r in n100]); print('S>=9 <100', [r[0] for r in s9])
fim = r"""
\end{landscape}

\subsection{Pontos críticos}
\label{subsec:fmea_criticos}

Dos 23 modos de falha, 13 têm NPR igual ou superior a 100, e outros três entram pelo critério de severidade: a célula perfurada na montagem (P07), o código gravado diferente do registrado (P10) e o vínculo errado no cadastro (P11). A Tabela~\ref{tab:fmea_criticos} ordena os oito maiores.

\begin{table}[htbp]
    \centering
    \caption{Oito modos de falha de maior NPR}
    \label{tab:fmea_criticos}
    \footnotesize
    \renewcommand{\arraystretch}{1.3}
    \begin{tabularx}{\textwidth}{@{}
        c
        >{\RaggedRight\arraybackslash}X
        c c c@{}}
        \toprule
        \textbf{Nº} & \textbf{Modo de falha} & \textbf{S} & \textbf{NPR atual} & \textbf{NPR previsto} \\
        \midrule
"""
for r in top[:8]:
    fim += f"        {r[0]} & {r[2]} & {r[3]} & {r[4]} & {r[5]} \\\\\n"
fim += r"""        \bottomrule
    \end{tabularx}
    \source{Elaborado pelos autores (2026).}
\end{table}

A leitura das duas tabelas leva a quatro pontos críticos.

\textbf{Abertura por ímã externo (D04).} É o maior risco e o único que continua acima de 100 depois da ação. A embreagem de esferas abre com qualquer campo forte o bastante, e os destacadores de etiquetas rígidas são vendidos livremente \cite{cablematic2026xy021}. O Tag\&Go herda essa fragilidade das etiquetas atuais, porque usa o mesmo princípio de retenção. A diferença é que o dispositivo sabe quando foi aberto: a chave da garra informa a abertura, e o servidor distingue a abertura com ordem da abertura sem ordem. A ação reduz a detecção, e não a ocorrência. A blindagem de aço sobre a embreagem, que reduziria a ocorrência, compete com o campo do próprio ímã do dispositivo e só pode ser avaliada no ensaio.

\textbf{Mudanças do DFMA ainda não ensaiadas (D01, D02 e P02).} Três dos cinco maiores riscos vêm das mudanças M2 e M7, que integraram o pino à garra fundida e trocaram o eixo metálico por munhões em mancais de plástico. As duas reduziram o número de peças e o tempo de montagem, e as duas atuam sobre a retenção, a função que a loja mais cobra. O FMEA confirma a ressalva da Entrega~3: elas só entram no produto depois do ensaio de arrancamento, e a versão anterior fica como alternativa.

\textbf{Folga do ímã (D03, P01, P05 e P06).} A liberação depende de uma folga de 0,20~mm que resulta de três cotas (Tabela~\ref{tab:des_cadeia}). Os quatro modos de falha ligados a ela têm detecção boa, porque o subconjunto do mecanismo é testado em todas as unidades antes de fechar a carcaça. As ações atuam na ocorrência: o gabarito FD-01, o batente da prensa e o plano de controle do suporte.

\textbf{Colagem do ímã (P04).} A colagem não tinha controle. O ímã descolado não é detectado na montagem e aparece no uso, quando o dispositivo deixa de liberar. O ensaio de cisalhamento por lote de colagem passa a ser exigência do processo.

\subsection{Providências já tomadas}
\label{subsec:fmea_providencias}

Parte das ações já está incorporada aos documentos desta entrega. A Tabela~\ref{tab:fmea_providencias} separa o que foi feito do que depende de ensaio.

\begin{table}[htbp]
    \centering
    \caption{Situação das ações do FMEA}
    \label{tab:fmea_providencias}
    \footnotesize
    \renewcommand{\arraystretch}{1.3}
    \begin{tabularx}{\textwidth}{@{}
        >{\RaggedRight\arraybackslash}p{2.6cm}
        >{\RaggedRight\arraybackslash}X
        >{\RaggedRight\arraybackslash}p{4.4cm}@{}}
        \toprule
        \textbf{Modos de falha} & \textbf{Providência} & \textbf{Situação} \\
        \midrule
        D03, P05 & Gabarito de colagem FD-01, que fixa a altura do ímã & Projetado (Seção~\ref{sec:projeto_dispositivo}) \\
        D03, P01 & Características críticas do suporte, com plano de controle & Incorporado ao desenho DE-03 e à Seção~\ref{sec:controle_qualidade} \\
        D01, P02 & Dureza, perpendicularidade e extração do pino na inspeção da garra & Incorporado à ficha de processo (Tabela~\ref{tab:proc_garra}) \\
        D10, P08 & Sensor de temperatura e conectores polarizados na placa & Incorporado à especificação (Tabela~\ref{tab:ext_lista}) \\
        D10, P07 & Célula certificada e nervuras de posição na base & Incorporado à especificação e ao desenho DE-01 \\
        D12 & Parafusos de fenda hexalobular & Incorporado à especificação \\
        P04 & Rugosidade do alojamento do ímã & Incorporado ao desenho DE-05 \\
        \midrule
        D01, D02, D03, D04 & Ensaio do campo e ensaio de arrancamento (E12) & A fazer, antes de congelar o projeto \\
        D04, D05, D08, P11 & Regras do \textit{firmware} e do \textit{software} de cadastro & A implementar no protótipo \\
        D06, D09, D11, P04, P09 & Ensaios de abrasão, de corrente de espera, em tecido, de cisalhamento e de torque & A fazer, no protótipo \\
        D08 & Medição da cobertura de rádio & A fazer, na loja piloto \\
        \bottomrule
    \end{tabularx}
    \source{Elaborado pelos autores (2026).}
\end{table}

As ações previstas levam a soma dos NPR de %d para %d, e apenas o modo D04 continua acima de 100. Esse resultado é uma previsão. O FMEA deve ser refeito depois do ensaio do campo e do ensaio de arrancamento, com os índices de ocorrência apoiados em medições.
""" % (sum(r[4] for r in allr), sum(r[5] for r in allr))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2-conteudo', '25-fmea.tex'),'w',encoding='utf-8').write(intro+td+mid+tp+fim)
