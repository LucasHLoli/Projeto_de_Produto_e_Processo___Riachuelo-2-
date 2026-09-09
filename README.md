# 📘 Guia do Projeto — PPP Riachuelo (Overleaf + LaTeX)

Este arquivo não entra no PDF final — é só documentação para o time. Leiam antes de começar a escrever, principalmente se nunca usaram Overleaf/LaTeX.

> ## ⚠️ PRIMEIRO PASSO OBRIGATÓRIO — sem isso o PDF não compila
> Quem criar/abrir o projeto pela primeira vez precisa trocar o compilador, **uma vez só, para o projeto inteiro**:
> **Menu → Settings → Compiler → troque de "pdfLaTeX" para "XeLaTeX" → Recompile.**
>
> Sem isso o Overleaf dá erro fatal `fontspec package requires either XeTeX or LuaTeX` e nenhum PDF é gerado — o preâmbulo usa a fonte Times New Roman (`fontspec`), que só funciona com XeLaTeX/LuaLaTeX. É configuração do projeto, não do código, e uma vez trocada vale para o time inteiro (não precisa repetir por pessoa).

## Índice
1. [O que é o Overleaf](#1-o-que-é-o-overleaf)
2. [Primeiros passos](#2-primeiros-passos)
3. [Como compilar o documento](#3-como-compilar-o-documento)
4. [Estrutura de pastas deste projeto](#4-estrutura-de-pastas-deste-projeto)
5. [Fluxo de trabalho do time (8 pessoas)](#5-fluxo-de-trabalho-do-time-8-pessoas)
6. [Cheat sheet de comandos LaTeX](#6-cheat-sheet-de-comandos-latex)
7. [Citações, referências e bibliografia](#7-citações-referências-e-bibliografia)
8. [Erros comuns de compilação](#8-erros-comuns-de-compilação)
9. [Como usar IA para ajudar a escrever](#9-como-usar-ia-para-ajudar-a-escrever)
10. [Checklist antes de entregar](#10-checklist-antes-de-entregar)

---

## 1. O que é o Overleaf

O Overleaf é um editor **LaTeX online e colaborativo** — como um Google Docs, mas em vez de formatar visualmente (negrito, tamanho de fonte etc. no clique do mouse), você escreve **código** (`.tex`) que descreve a formatação, e o Overleaf **compila** esse código em um PDF pronto, já formatado.

Duas coisas importantes de entender antes de tudo:

- **Você não edita o PDF diretamente.** Você edita arquivos `.tex` (texto puro com comandos), e o PDF é gerado a partir deles toda vez que compila.
- **A edição é em tempo real**, tipo Google Docs: todo mundo que estiver com o projeto aberto vê o cursor dos outros e as mudanças aparecem instantaneamente. Não existe "salvar" separado — está sempre salvo.

## 2. Primeiros passos

1. **Acessar o projeto**: quem for dono do projeto compartilha o link de convite (Menu → Share). Cada pessoa deve entrar com sua própria conta (não dividam login).
2. **Interface**: à esquerda fica a **lista de arquivos** (é essa estrutura de pastas que organizamos). Ao clicar em um arquivo `.tex`, ele abre no **editor** (meio da tela). À direita fica o **PDF compilado** (preview).
3. **Editor de texto**: onde você escreve o código LaTeX. Cada seção do trabalho é um arquivo separado (ver seção 4).
4. **Chat e comentários**: existe um chat lateral e é possível selecionar um trecho de texto e adicionar um comentário (ícone de balão) — útil para pedir revisão sem editar o texto do colega direto.
5. **Histórico de versões**: Menu → History mostra tudo que já foi mudado, por quem, e permite voltar uma versão anterior se alguém quebrar algo sem querer. **Isso é o nosso "salva-vidas"** — se der ruim, dá pra restaurar.

## 3. Como compilar o documento

- O botão verde **"Recompile"** (canto superior do PDF) gera o PDF atualizado. Atalho: `Ctrl+Enter` (Windows) ou `Cmd+Enter` (Mac).
- O Overleaf recompila automaticamente pouco tempo depois de você parar de digitar, mas é bom compilar manualmente antes de sair, pra garantir que não quebrou nada.
- **Importante para este projeto**: o preâmbulo usa a fonte Times New Roman via pacote `fontspec`, que **só funciona com o compilador XeLaTeX** (não com o pdfLaTeX padrão). Confiram em Menu → Settings → Compiler se está selecionado **XeLaTeX**. Se estiver como "pdfLaTeX", vai dar erro de compilação.
- O arquivo que é compilado é sempre o `documento.tex` (é ele quem "puxa" todos os outros via `\input{}`). Menu → Settings → Main document confirma que é esse o arquivo raiz.

## 4. Estrutura de pastas deste projeto

```
/
├── documento.tex          ⚠️ arquivo mestre — só quem organiza o sumário mexe aqui
├── bibliografia.bib       📚 todas as referências bibliográficas do trabalho
├── 1-pre/                 elementos pré-textuais
│   ├── 1-preambulo.tex    ⚠️ configuração geral (fonte, margens, ABNT) — só 1 pessoa "dona" mexe
│   ├── 2-capa.tex
│   ├── 3-resumo.tex
│   ├── 4-abstract.tex
│   └── 5-introducao.tex
├── 2-conteudo/            desenvolvimento do trabalho — 1 arquivo por dupla
│   ├── 1-diagnostico.tex
│   ├── 2-metodologia.tex
│   ├── 3-proposta.tex
│   └── 4-resultados.tex
├── 3-pos/                 elementos pós-textuais
│   ├── 1-conclusao.tex
│   └── 2-referencias.tex
└── imagens/                todas as figuras usadas no documento
    ├── Poli.png            (logo, usado só na capa)
    ├── diagnostico/
    ├── metodologia/
    ├── proposta/
    └── resultados/
```

**Por que dividir assim?** No Overleaf não existe "puxar/enviar" como no Git — é tudo em tempo real. Se 3 pessoas abrem o *mesmo* arquivo ao mesmo tempo para editar parágrafos diferentes, funciona, mas fica confuso e aumenta o risco de alguém apagar sem querer o que o outro está escrevendo. Por isso: **1 arquivo = 1 dupla responsável**, ninguém abre o arquivo de conteúdo de outra dupla para editar.

## 5. Fluxo de trabalho do time (8 pessoas)

- **4 duplas, 1 arquivo de conteúdo cada** (`1-diagnostico.tex`, `2-metodologia.tex`, `3-proposta.tex`, `4-resultados.tex`).
- **`documento.tex` e `1-preambulo.tex`** só devem ser editados por quem estiver organizando a estrutura geral (o ideal é 1, no máximo 2 pessoas fixas) — são arquivos de configuração; um erro de sintaxe ali quebra a compilação **para o time inteiro**.
- **Nomeação de labels com prefixo da seção**, para não haver duplicidade quando várias pessoas criam referências ao mesmo tempo:
  - Figuras: `fig:diagnostico-01`, `fig:metodologia-02`...
  - Tabelas: `tab:proposta-01`...
  - Seções: `sec:diagnostico`, `subsec:diagnostico`...
  - (Os arquivos de conteúdo já seguem esse padrão nos exemplos — usem como modelo.)
- **Imagens**: cada dupla salva as próprias imagens dentro da subpasta correspondente em `imagens/` (ex.: `imagens/diagnostico/fig01-fluxograma-atual.png`), com nome descritivo — nunca "Captura de tela.png" ou "imagem1.png".
- **Bibliografia compartilhada**: todo mundo edita o mesmo `bibliografia.bib`. Para não duplicar referência, usem sempre a chave no padrão `sobrenomeAno` (ex.: `kotler2016`, `riachuelo2023`) — antes de adicionar uma referência nova, dê um `Ctrl+F` no arquivo pra conferir se ela já não existe com outra chave.
- **Marcação de pendências**: usem `% TODO: o que falta` como comentário no texto (tudo depois de `%` em uma linha é ignorado na compilação, não aparece no PDF).
- **Antes de sair**, compilem e confiram que o PDF ainda gera sem erro — se você quebrar a compilação e sair, ninguém mais consegue ver o PDF atualizado até alguém achar o erro.

## 6. Cheat sheet de comandos LaTeX

> **Sobre "instalar" recursos no Overleaf**: diferente de outros programas, no Overleaf não existe instalar plugin/extensão. Praticamente todo pacote LaTeX que existe já está disponível — usar um recurso novo é só adicionar uma linha `\usepackage{nome}` no preâmbulo (`1-pre/1-preambulo.tex`) e ele funciona na hora, sem baixar nada. Todos os pacotes usados nos exemplos abaixo **já foram adicionados** no preâmbulo deste projeto — podem copiar e colar os exemplos direto, sem precisar mexer em mais nada.

### Estrutura de texto
```latex
\section{Título de Seção}
\subsection{Título de Subseção}
\textbf{negrito}
\textit{itálico}
\uline{sublinhado}
\sout{tachado}
\emph{ênfase (fica em itálico)}
```

### Cores e destaque de texto
```latex
\textcolor{red}{texto em vermelho}
\colorbox{yellow}{texto com fundo amarelo (tipo marca-texto)}
```
Cores prontas: `red`, `blue`, `green`, `yellow`, `gray`, `orange`, `purple`, `black`... Dá pra ajustar intensidade, ex. `gray!30` (30% de cinza, mais claro).

### Parágrafo e quebras
```latex
Um parágrafo termina com uma linha em branco.

Isso já começa um parágrafo novo.

\newpage    % força quebra de página
\clearpage  % quebra de página + "descarrega" figuras/tabelas pendentes
```

### Notas de rodapé
```latex
O texto principal continua aqui\footnote{Isso aparece como nota no rodapé da página.}.
```

### Listas
```latex
\begin{itemize}       % lista com marcadores (bullet points)
    \item Primeiro item
    \item Segundo item
    \begin{itemize}    % lista aninhada (sub-itens)
        \item Sub-item A
        \item Sub-item B
    \end{itemize}
\end{itemize}

\begin{enumerate}     % lista numerada (1, 2, 3...)
    \item Primeiro item
    \item Segundo item
\end{enumerate}

\begin{description}   % lista de termo + definição
    \item[Termo A] Explicação do termo A.
    \item[Termo B] Explicação do termo B.
\end{description}
```

Para mudar o marcador da lista (ex.: usar traço em vez de bolinha), o pacote `enumitem` já está carregado:
```latex
\begin{itemize}[label=--]
    \item Item com marcador de traço
\end{itemize}
```

### Tabela simples (padrão ABNT do template, sem linhas verticais)
```latex
\begin{table}[h!]
    \centering
    \caption{Legenda da tabela}
    \begin{tabular}{cccc}
        \toprule
        \textbf{Coluna 1} & \textbf{Coluna 2} & \textbf{Coluna 3} & \textbf{Coluna 4}\\
        \midrule
        a & b & c & d\\
        \bottomrule
    \end{tabular}
    \label{tab:minha-tabela}
    \source{Elaborado pelos autores}
\end{table}
```
`c` = coluna centralizada, `l` = alinhada à esquerda, `r` = à direita — pode misturar, ex. `{lccr}`.

### Tabela com coluna de largura fixa e texto que quebra linha
Útil quando uma coluna tem texto longo (ex.: descrição) e não pode esticar a tabela para fora da página:
```latex
\begin{table}[h!]
    \centering
    \caption{Tabela com coluna de texto longo}
    \begin{tabular}{l p{7cm} c}
        \toprule
        \textbf{Item} & \textbf{Descrição} & \textbf{Status}\\
        \midrule
        1 & Texto longo que quebra automaticamente dentro dos 7cm definidos & OK\\
        \bottomrule
    \end{tabular}
    \label{tab:largura-fixa}
\end{table}
```

### Tabela com células mescladas (linhas ou colunas)
```latex
\begin{table}[h!]
    \centering
    \caption{Tabela com células mescladas}
    \begin{tabular}{lcc}
        \toprule
        \multirow{2}{*}{\textbf{Categoria}} & \multicolumn{2}{c}{\textbf{Resultado}}\\
        \cmidrule(lr){2-3}
         & \textbf{2025} & \textbf{2026}\\
        \midrule
        Item A & x1 & y1\\
        Item B & x2 & y2\\
        \bottomrule
    \end{tabular}
    \label{tab:mesclada}
\end{table}
```
`\multirow{2}{*}{...}` mescla 2 linhas na mesma célula; `\multicolumn{2}{c}{...}` mescla 2 colunas.

### Tabela grande que quebra entre páginas
Uma `table` comum não pode ultrapassar uma página — se a tabela for grande (ex.: base de dados do diagnóstico), use `longtable` em vez de `table`+`tabular`:
```latex
\begin{longtable}{lcc}
    \caption{Tabela longa que quebra página automaticamente}
    \label{tab:longa}\\
    \toprule
    \textbf{Item} & \textbf{Coluna 2} & \textbf{Coluna 3}\\
    \midrule
    \endfirsthead
    \toprule
    \textbf{Item} & \textbf{Coluna 2} & \textbf{Coluna 3}\\
    \midrule
    \endhead
    linha 1 & a & b\\
    linha 2 & c & d\\
    ... & ... & ...\\
    \bottomrule
\end{longtable}
```

### Figura simples
```latex
\begin{figure}[h!]
    \centering
    \caption{Legenda da imagem}
    \includegraphics[width=0.6\textwidth]{imagens/diagnostico/fig01-exemplo.png}
    \label{fig:minha-figura}
    \source{Elaborado pelos autores}
\end{figure}
```

### Texto correndo ao redor de uma imagem (em vez de imagem sozinha no meio do texto)
```latex
\begin{wrapfigure}{r}{0.4\textwidth} % r = imagem à direita, l = à esquerda
    \centering
    \includegraphics[width=0.38\textwidth]{imagens/diagnostico/fig01-exemplo.png}
    \caption{Legenda}
    \label{fig:wrap-exemplo}
\end{wrapfigure}
O texto deste parágrafo passa a contornar a imagem, em vez de a imagem ocupar a largura toda sozinha — bom para não desperdiçar espaço quando a imagem é pequena.
```

### Equação
```latex
\begin{equation}
    E = mc^2
    \label{eq:minha-equacao}
\end{equation}
```

### Sistema de equações / equação em várias linhas
```latex
\begin{align}
    a &= b + c \\
    d &= e - f
\end{align}
```

### Matriz
```latex
\begin{equation}
    M = \begin{bmatrix}
        1 & 0 \\
        0 & 1
    \end{bmatrix}
\end{equation}
```

### Bloco de código-fonte formatado
Útil se o trabalho mostrar pseudocódigo, query, trecho de configuração etc.:
```latex
\begin{lstlisting}[language=Python, caption={Legenda do código}, label={cod:exemplo}]
def exemplo():
    return "código com numeração de linha e fundo cinza"
\end{lstlisting}
```
Troque `language=Python` por `SQL`, `Java`, `C` etc. conforme o caso (ou remova a opção para código genérico sem realce de sintaxe).

### Símbolos e caracteres especiais
Estes caracteres têm significado especial em LaTeX e precisam de `\` na frente para aparecerem literalmente: `% & _ # $ { }`. Ex.: para escrever "50%", use `50\%`.

Símbolos matemáticos comuns (dentro de `$...$` ou de `equation`): `\alpha \beta \gamma \Delta \sum \int \leq \geq \neq \approx \rightarrow \infty`.

## 7. Citações, referências e bibliografia

- Toda referência bibliográfica vai no `bibliografia.bib`, no formato BibTeX. Existem 3 exemplos prontos no arquivo (livro, artigo, site) — copiem a estrutura e troquem os dados.
- No texto, cite com `\cite{chave}` — ele vira automaticamente `(AUTOR, ano)` no padrão ABNT.
- Para referenciar uma seção, figura, tabela ou equação que tem `\label{...}`, use `\autoref{...}` — ele gera "Seção X", "Figura Y" etc. automaticamente e ainda vira link clicável no PDF.
- **Referências cruzadas (`\autoref`) só atualizam depois de compilar duas vezes** — se acabou de criar um label novo e a referência aparece como `??`, recompile de novo.

## 8. Erros comuns de compilação

| Mensagem / sintoma | Causa provável | Solução |
|---|---|---|
| `Undefined control sequence` | Comando digitado errado ou pacote não carregado | Confira a grafia do comando; veja se falta `\usepackage{...}` no preâmbulo |
| Referência aparece como `??` | Ainda não recompilou depois de criar o label | Recompile mais uma vez |
| `Citation ... undefined` | Chave usada em `\cite{}` não existe no `.bib`, ou tem erro de digitação | Confira se a chave bate exatamente (case-sensitive) |
| Erro relacionado a `fontspec` / `setmainfont` | Projeto compilando com pdfLaTeX em vez de XeLaTeX | Menu → Settings → Compiler → XeLaTeX |
| `File not found` numa imagem | Caminho ou nome do arquivo errado (maiúscula/minúscula importa) | Confira se o arquivo está na pasta certa e o nome bate exatamente |
| `Missing $ inserted` | Uso de símbolo especial (`_`, `^`, `%`) fora de modo matemático | Escape o caractere (`\_`, `\%`) ou coloque entre `$...$` se for matemática |
| "Overfull hbox" (linha ultrapassando a margem) | Palavra muito longa ou tabela/imagem larga demais | Normalmente é só aviso, não erro — mas se estourar visualmente, reduza `width` da imagem/tabela |

Quando o erro não é óbvio, o log de compilação (aba "Logs and output files") mostra a linha exata e o arquivo onde ocorreu — sempre olhem ali primeiro.

## 9. Como usar IA para ajudar a escrever

IA (ChatGPT, Claude etc.) pode acelerar bastante o trabalho em LaTeX — usem como apoio, não como substituto de revisão. Exemplos de uso prático:

- **Gerar código LaTeX a partir de dado bruto**: cole uma tabela de Excel/planilha e peça "transforme isso em uma tabela LaTeX no padrão ABNT (`\toprule`/`\midrule`/`\bottomrule`, sem linhas verticais)".
- **Explicar e corrigir erro de compilação**: copie a mensagem de erro do log do Overleaf e cole na IA perguntando o que significa e como resolver — geralmente acerta de primeira.
- **Ajustar texto**: peça para revisar concordância, clareza ou reduzir um parágrafo para caber no limite de palavras (ex.: resumo de até 250 palavras).
- **Formato BibTeX**: cole um link de artigo/site e peça para gerar a entrada `.bib` correspondente no formato usado neste projeto.
- **Explicar um comando LaTeX** que apareceu no template e vocês não conhecem (`\autoref`, `\numberwithin` etc.).

**Cuidados importantes:**
- **Sempre confiram o que a IA gerar antes de aceitar** — compilem e leiam o resultado; IA erra sintaxe de LaTeX às vezes.
- **Nunca aceitem uma referência bibliográfica "inventada" por IA sem checar se ela existe de verdade** — modelos de linguagem podem alucinar autor, título ou ano de uma fonte. Confirmem a referência na fonte original antes de citar.
- **Não colem dados internos sensíveis da Riachuelo** (números confidenciais, dados de cliente, informação sob NDA) em ferramentas de IA públicas sem verificar antes com o professor/orientador se isso é permitido.
- IA é ótima para *gerar esqueleto* e *resolver erro técnico*; o argumento, a análise e as conclusões do trabalho continuam sendo vocês.

## 10. Checklist antes de entregar

- [ ] Todos os `TITULO DA SECAO` e `Titulo da Subsecao` genéricos foram substituídos por títulos reais
- [ ] Todos os placeholders `\textit{[Texto de exemplo --- substituir pelo conteúdo real...]}` foram substituídos pelo texto real (dê `Ctrl+F` por `Texto de exemplo` em cada arquivo de `2-conteudo/` para achar todos)
- [ ] Capa preenchida (departamento, disciplina, professor, título, nomes e NUSP de todos, mês/ano)
- [ ] Resumo (até 250 palavras) e Abstract preenchidos, com 3 palavras-chave cada
- [ ] Todas as referências fictícias (`exemploLivro`, `exemploArtigo`, `exemploWeb`) substituídas por referências reais no `bibliografia.bib`
- [ ] Todas as figuras/tabelas têm `\caption`, `\label` e `\source` (fonte)
- [ ] Compilador configurado como **XeLaTeX** (Settings → Compiler)
- [ ] PDF final compila sem erros nem referências `??`
- [ ] Sumário, lista de figuras e lista de tabelas conferidas no PDF final (gerados automaticamente, mas vale checar se bateram com o conteúdo)
