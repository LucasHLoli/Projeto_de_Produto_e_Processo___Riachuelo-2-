# PARTE 07 — ESCOPO E ENTREGA
## O que o trabalho tem que entregar?

> **Faça esta parte primeiro.** Sem escopo decidido, sete duplas trabalham no vazio e a
> integração no fim não fecha. É a única parte que bloqueia todas as outras.

---

## 0. Papel

Você é o coordenador do projeto. Sua tarefa **não** é fazer engenharia — é decidir até onde o
grupo vai, garantir que as partes encaixem, e entregar o relatório montado no prazo.

Esta parte é de **uma pessoa**, não de uma dupla.

---

## 1. Contexto mínimo (autossuficiente)

Oito pessoas, um semestre, um relatório em LaTeX/Overleaf e uma apresentação. O projeto propõe
uma etiqueta antifurto que se destrava sozinha após o pagamento pelo celular, eliminando a fila
do caixa em lojas Riachuelo.

O trabalho está dividido em 7 partes técnicas (00 a 06), cada uma com seu prompt nesta pasta.
Elas se comunicam pelas interfaces de `CONTRATOS.md`.

O risco clássico deste formato: cada dupla entrega bem a sua parte, e no fim ninguém montou o
todo. Sua função é impedir isso.

---

## 2. Você recebe

- Os 7 prompts das partes técnicas e o `CONTRATOS.md`.
- O template LaTeX já estruturado em `1-pre/`, `2-conteudo/`, `3-pos/`.
- O `README.md` do projeto, com as regras de Overleaf que o time combinou.

---

## 3. Você entrega

1. **Decisão de escopo**: até que nível de protótipo o grupo vai.
2. **Orçamento aprovado**, com quem paga o quê.
3. **Cronograma** com marcos e o caminho crítico explícito.
4. **Matriz de responsabilidade**: quem faz o quê, quem revisa o quê.
5. **Plano do relatório**: qual seção recebe o resultado de qual parte.
6. **Rotina de integração**: como as partes se encontram antes da última semana.
7. **Roteiro da apresentação**.

---

## 4. Restrições

- Orçamento vem do bolso de 8 estudantes. Trate como restrição dura, não como detalhe.
- Prazo é o do semestre. Não existe prorrogar.
- **Escopo é a única variável livre.** Quando algo apertar, corta-se escopo — nunca qualidade
  do que já foi decidido fazer.

---

## 5. Método passo a passo

### 5.1 A decisão de escopo — leve isto à primeira reunião

| Nível | O que demonstra | Custo | Prazo | Recomendação |
|---|---|---|---|---|
| **0 — Maquete** | vídeo do fluxo, telas do app, hard tag cortada mostrando a garra | ~R$ 50 | 1 sem | piso, sempre entregue |
| **1 — Destrava** | etiqueta que abre de verdade na estação; celular lê e mostra o produto | ~R$ 300 | 3 sem | mínimo defensável |
| **2 — Fluxo completo** | + pagamento em sandbox + token autenticado + só libera se pago | ~R$ 500 | 5 sem | **alvo recomendado** |
| **3 — Com pórtico** | + leitura UHF na saída conferindo item contra venda | ~R$ 1.100 | 8 sem | só se sobrar tempo |

**Recomendação: mirar o Nível 2, tratar o 3 como opcional.** O Nível 2 já demonstra a tese
inteira do trabalho — que o antifurto se resolve sem operador. O pórtico consome muito tempo e
não acrescenta argumento novo; ele confirma algo que já é conhecido no varejo.

Dividido por 8 pessoas, o Nível 2 dá cerca de **R$ 65 por integrante**.

Leve as quatro linhas à reunião e **feche a decisão nela**. Escopo em aberto sangra semanas.

### 5.2 Cronograma — o caminho crítico é a parte 03

| Semana | Marco | Quem |
|---|---|---|
| 1 | escopo fechado; compras feitas | 07 |
| 1 | **hard tags compradas e desmontadas, garra medida** | 03 |
| 2 | **ensaio de bancada: o atuador vence a garra?** ← *go / no-go* | 03 |
| 2 | medição de fila em loja | 00 |
| 2–3 | NFC gravado e testado em 6 celulares | 01 |
| 3–5 | app + backend + sandbox | 02 |
| 4–6 | CAD, impressão, montagem da etiqueta | 03 |
| 5–6 | protocolo de autorização implementado | 05 |
| 6 | modelo de custo por uso | 06 |
| 6–7 | decisão e execução do pórtico | 04 |
| **7** | **integração 1: app → estação → etiqueta abre** | todos |
| 8 | ensaio de vida; matriz de confusão | 03, 04 |
| **9** | **integração 2: fluxo completo, ponta a ponta** | todos |
| 10 | escrita e revisão cruzada do relatório | todos |
| 11 | ensaio da apresentação | todos |

**O marco da semana 2 é um portão de decisão, não um item de lista.** Se o atuador não vencer
a garra, o grupo tem 9 semanas para mudar de rumo. Se essa descoberta vier na semana 8, não tem.

### 5.3 Responsabilidades

| Dupla | Partes | Escreve | Revisa |
|---|---|---|---|
| A | 00 Diagnóstico + 06 Logística | `1-diagnostico.tex` | dupla C |
| B | **03 Destravamento** | `2-metodologia.tex` | dupla D |
| C | 01 Identificação + 02 App + 05 Autorização | `3-proposta.tex` | dupla A |
| D | 04 Pórtico + consolidação | `4-resultados.tex` | dupla B |
| Coord. | 07 | `5-introducao.tex`, `1-conclusao.tex`, resumo, abstract | todos |

**Revisão cruzada é obrigatória.** Ninguém entrega texto que só a própria dupla leu.

### 5.4 Integração — o que faz projeto dividido não quebrar

Duas datas de integração marcadas no calendário desde a semana 1:

- **Semana 7 — integração parcial:** o app manda pagar, a estação pede o token, a etiqueta abre.
  Sem pórtico, sem carcaça bonita. Só provar que as interfaces do `CONTRATOS.md` funcionam.
- **Semana 9 — integração completa:** o fluxo inteiro, do cliente pegando a peça até sair pelo pórtico.

Entre elas, **reunião de 20 minutos por semana**, com uma pauta só:
"o que a sua parte precisa de outra dupla e ainda não recebeu?"

> Se alguém descobrir na semana 9 que o inlay UHF não cabe na carcaça, o problema não foi
> técnico — foi de coordenação. Essa pergunta semanal existe para pegar exatamente isso.

### 5.5 Plano do relatório

| Seção LaTeX | Recebe de | Conteúdo central |
|---|---|---|
| `5-introducao.tex` | 07 | problema, objetivo, estrutura do texto |
| `1-diagnostico.tex` | 00, 06 | cronoanálise, modelo de fila, custo da fila e da quebra |
| `2-metodologia.tex` | 03 | fusão de patentes, **balanço de energia**, matriz de decisão do atuador |
| `3-proposta.tex` | 01, 02, 05 | arquitetura, app, protocolo de autorização, CAD |
| `4-resultados.tex` | 03, 04, 00 | ensaios, tempo de destravamento, matriz de confusão, custo, payback |
| `1-conclusao.tex` | 07 | o que funcionou, **o que não funcionou**, limitações, próximos passos |

**A seção de limitações não é opcional.** Declarar antes que perguntem — envelope maior no
protótipo, pórtico não implementado, medição em uma loja só — é o que separa um trabalho
maduro de um otimista.

### 5.6 Apresentação

Roteiro em 5 blocos, com tempo:

1. **O problema** (2 min) — o número da fila medido pela parte 00. Comece com dado, não com slide de contexto.
2. **A descoberta** (2 min) — o gargalo é a etiqueta, não o pagamento. É a virada do argumento.
3. **A solução** (3 min) — a fusão de patentes, e o balanço de energia que obriga a Estação a existir.
4. **A demonstração** (3 min) — **ao vivo**, se o protótipo estiver estável; vídeo gravado como reserva.
5. **Os números** (2 min) — tempo de destravamento, custo por uso, payback, limitações.

> Sempre grave o vídeo da demo mesmo que vá apresentar ao vivo. Protótipo escolhe a pior hora
> para falhar.

---

## 6. Perguntas que seu entregável precisa responder

1. Qual nível de escopo o grupo fechou, e quando?
2. Quanto custa, e quem paga?
3. Qual o caminho crítico, e qual o portão de decisão?
4. Quem escreve e quem revisa cada seção?
5. Quando são as duas integrações?
6. O que o grupo faz se o portão da semana 2 reprovar?

### A resposta da pergunta 6 — decida antes de precisar

Se o atuador não vencer a garra na semana 2, os planos B, em ordem:

1. **Trocar de atuador** (servo ou micromotor no lugar do SMA), aceitando etiqueta mais grossa.
2. **Trocar de garra** — nem toda hard tag comercial tem a mesma mola; teste outro modelo.
3. **Mudar o ponto de ataque**: em vez de abrir a garra, cortar ou soltar o pino por outro meio.
4. **Assumir o Nível 0/1** e entregar o projeto como estudo de viabilidade, com o ensaio
   negativo como resultado. **Um "não funciona, e aqui está o porquê medido" é um trabalho de
   engenharia legítimo** — muito melhor que uma maquete que finge funcionar.

---

## 7. Critérios de aceite

- [ ] Escopo decidido em reunião, com as 4 linhas da §5.1 na mesa, e registrado por escrito.
- [ ] Orçamento fechado e o rateio combinado.
- [ ] Cronograma publicado, com o portão da semana 2 marcado.
- [ ] Matriz de responsabilidade com autor **e** revisor de cada seção.
- [ ] Duas datas de integração no calendário desde a semana 1.
- [ ] Reunião semanal de 20 min acontecendo, com a pauta da §5.4.
- [ ] Plano B da §6 decidido **antes** da semana 2.
- [ ] Vídeo da demo gravado antes da apresentação.

---

## 8. O que NÃO fazer

- Não faça engenharia. Se você está mexendo em CAD ou código, ninguém está coordenando.
- Não deixe o escopo em aberto "para ver como anda". Ele nunca fecha sozinho.
- Não marque a integração para a última semana. Integração é onde os problemas aparecem, e
  eles precisam de tempo para serem resolvidos.
- Não deixe uma dupla escrever sem revisor.
- Não aumente o escopo no meio do semestre porque "está indo bem". Está indo bem porque o
  escopo está fechado.
- Não esconda o que não funcionou. A seção de limitações é onde o trabalho ganha credibilidade.
