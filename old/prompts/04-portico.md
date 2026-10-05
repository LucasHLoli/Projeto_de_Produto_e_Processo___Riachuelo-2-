# PARTE 04 — PÓRTICO DE SAÍDA
## Como saber que ninguém levou item não pago?

---

## 0. Papel

Você é engenheiro de sistemas de RF. Sua tarefa é decidir — **com número, não com opinião** —
se o pórtico de saída entra no protótipo, e se entrar, construí-lo.

**Sua primeira entrega não é um pórtico. É a decisão de construir ou não.**

---

## 1. Contexto mínimo (autossuficiente)

No sistema proposto, o cliente paga pelo celular e destrava a etiqueta antifurto sozinho, numa
estação de autoatendimento. Ninguém confere nada na saída.

Isso abre um buraco: como saber que a pessoa não está levando uma peça que **não** pagou?

Resposta: um **pórtico** na saída que lê por UHF RFID todas as etiquetas que passam e confere
contra as vendas dos últimos minutos. Item lido e pago → silêncio. Item lido e não pago →
alerta.

**Custo é o problema.** Pórticos comerciais custam dezenas de milhares de reais. Módulos
baratos existem, mas com alcance e confiabilidade discutíveis. Sua parte é descobrir se dá.

---

## 2. Você recebe

De `CONTRATOS.md`:
- alcance mínimo de leitura: **1,0 m**;
- falso alarme aceitável: **< 1%**;
- rota `POST /gate/check`, que devolve os `item_id` pagos nos últimos **5 min**;
- formato do evento de venda.

Da parte 01: os inlays UHF e a curva de alcance que eles mediram. **Trabalhem juntos no ensaio
de alcance** — é o mesmo experimento, não façam duas vezes.

---

## 3. Você entrega

1. **Decisão fundamentada**: construir o pórtico, ou simular? Com orçamento e prazo.
2. Se construir: **pórtico funcionando** com leitura ≥ 1 m.
3. **Matriz de confusão** medida: falso positivo e falso negativo, com N ≥ 100 passagens.
4. **Análise do modo de falha do alarme indevido** — o que acontece com o cliente que pagou e
   o pórtico apita.
5. **Estimativa de custo** de um pórtico de produção por loja.
6. Texto e dados para `2-conteudo/4-resultados.tex`.

---

## 4. Restrições

- Faixa **902–928 MHz** (ANATEL, Brasil). Módulo de 868 MHz é europeu e perde alcance aqui.
- Potência irradiada dentro do limite legal para equipamento de radiação restrita. `[CITAR ANATEL]`
- **Falso alarme é pior que falso negativo.** Deixar passar uma peça custa o preço da peça.
  Acusar um cliente que pagou custa o cliente. Dimensione o sistema com esse peso.
- Não gaste mais que o orçamento definido na parte 07 sem aprovação do time.

---

## 5. Método passo a passo

### 5.1 Primeiro: a decisão (faça isto na primeira semana)

Cote três opções e compare:

| Opção | Custo | Prazo | O que demonstra | Risco |
|---|---|---|---|---|
| **A — Pórtico real** com módulo UHF barato | R$ 400–800 `[COTAR]` | 6–8 sem | sistema completo | **alto** — alcance pode não chegar a 1 m |
| **B — Bancada UHF** sem estrutura de pórtico: leitor em cima da mesa, peça passa por perto | R$ 250–400 | 2–3 sem | que a leitura UHF funciona | baixo |
| **C — Simulação**: pórtico como caixa preta em software, com taxas da literatura | R$ 0 | 1 sem | a lógica, não o RF | nenhum |

**Recomendação de partida: opção B.** Ela prova o que precisa ser provado (o inlay é lido a
distância e o sistema confere contra a venda) sem gastar semanas montando estrutura. A
estrutura física do pórtico não acrescenta argumento de engenharia — só aparência.

Leve a decisão ao time com os três números na mão. **Não decida sozinho.**

### 5.2 Se for construir — seleção do módulo

| Requisito | Valor |
|---|---|
| Protocolo | EPC Gen2 / ISO 18000-6C |
| Faixa | 902–928 MHz |
| Interface | UART ou USB |
| Potência | ajustável até ~30 dBm |
| Alcance declarado | ≥ 2 m (na prática entrega bem menos) |
| Antena | circular polarizada, 3–6 dBi — **confirme se vem inclusa** |
| Preço esperado | R$ 150–400 o módulo `[COTAR]` |

> **Armadilha de compra:** muitos módulos baratos anunciam alcance com etiqueta ideal, no ar,
> alinhada. Com etiqueta em tecido, mal orientada, o alcance real cai para uma fração. Compre
> **um** módulo e teste antes de comprar o resto.

### 5.3 Ensaio de alcance (fazer junto com a parte 01)

Meça a distância máxima de leitura em cada condição:

| # | Condição | Alcance medido |
|---|---|---|
| 1 | etiqueta no ar, alinhada com a antena | |
| 2 | etiqueta girada 90° | |
| 3 | etiqueta a 45° | |
| 4 | etiqueta encostada em tecido dobrado | |
| 5 | etiqueta dentro de sacola de papel | |
| 6 | etiqueta dentro de sacola plástica | |
| 7 | etiqueta encostada em arara metálica | |
| 8 | pessoa carregando a peça junto ao corpo | |

A condição **8 é a real** — é assim que o cliente sai da loja. As outras são diagnóstico.

> A água do corpo humano absorve UHF. Etiqueta prensada entre a peça e o corpo lê muito pior
> que etiqueta no ar. Se o alcance na condição 8 for insuficiente, **é um resultado legítimo do
> trabalho** — escreva isso, não esconda.

### 5.4 Matriz de confusão

Faça **no mínimo 100 passagens** pelo ponto de leitura, misturando:

- 50 passagens com item **pago**;
- 30 com item **não pago**;
- 20 sem item nenhum.

| | Sistema disse "pago" | Sistema disse "não pago" |
|---|---|---|
| **Era pago** | acerto | **falso alarme** ← o caro |
| **Não era pago** | **falso negativo** | acerto |

Calcule as duas taxas. Meta do contrato: falso alarme < 1%.

### 5.5 O alarme indevido

Especifique o que acontece quando o pórtico apita num cliente que pagou:

- O alarme é **sonoro para a loja inteira** ou discreto? (recomendação: discreto)
- Quem aborda o cliente, e com que roteiro?
- Como o cliente prova que pagou em 5 segundos? (tela do app com o comprovante)
- O sistema registra o incidente para análise?

> Este item parece "de processo", mas é **requisito de projeto**. Um pórtico que constrange
> cliente pagante destrói mais valor do que o furto que ele evita. Trate com o mesmo cuidado
> que você trata o alcance de leitura.

---

## 6. Perguntas que seu entregável precisa responder

1. Construir ou simular? Com que orçamento e prazo?
2. Qual o alcance real na condição 8 (pessoa carregando a peça)?
3. Qual a taxa de falso alarme medida, com N ≥ 100?
4. O sistema lê várias etiquetas simultâneas, ou perde peças numa sacola cheia?
5. Quanto custa um pórtico de produção por loja? `[COTAR]`
6. O que acontece com o cliente que pagou e o alarme dispara?

---

## 7. Critérios de aceite

- [ ] Decisão construir/simular tomada com os três orçamentos na mão e aprovada pelo time.
- [ ] Se construir: leitura funcionando e alcance medido nas 8 condições.
- [ ] Matriz de confusão com N ≥ 100 passagens.
- [ ] Taxa de falso alarme calculada e comparada com a meta de 1%.
- [ ] Ensaio com múltiplas etiquetas simultâneas.
- [ ] Protocolo de tratamento do alarme indevido escrito.
- [ ] Custo de produção por loja estimado.

---

## 8. O que NÃO fazer

- Não compre a estrutura física do pórtico antes de provar que o módulo lê a 1 m. A estrutura
  é a parte fácil e a última.
- Não compre módulo de 868 MHz.
- Não projete antena UHF — compre pronta.
- Não esconda alcance ruim. Se o inlay não é lido a 1 m na condição real, esse é um **resultado
  do trabalho** e deve estar nas conclusões e nas limitações.
- Não mexa no app nem no backend — parte 02. Você só consome `POST /gate/check`.
- Não deixe esta parte virar o gargalo do cronograma. Ela é a primeira a cortar se o tempo
  apertar, e o projeto continua defensável sem ela.
