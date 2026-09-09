# Esboço do conceito — Fusão: antifurto autoliberável + checkout por NFC/QR

> Documento de trabalho (não entra no PDF). Base para preencher
> `2-conteudo/1-diagnostico.tex`, `2-metodologia.tex`, `3-proposta.tex`, `4-resultados.tex`.
> Marcações `[VERIFICAR]` = número ou afirmação que precisa de fonte antes de entrar no relatório.

---

## 0. Tese do projeto (uma frase)

O tempo de fila em loja de moda é imposto pelo **antifurto**, não pelo pagamento: a *hard tag*
só pode ser removida por um operador com destravador magnético no caixa. Logo, qualquer
autoatendimento em vestuário depende de resolver a **liberação da tag**. A patente
US 7.564.360 B2 torna a tag capaz de se autoliberar por sinal de RF — fundindo isso com
identificação e pagamento por NFC/QR no celular, o caixa deixa de ser ponto obrigatório do fluxo.

---

## 1. Diagnóstico (`1-diagnostico.tex`)

### 1.1 O problema observado
- Fila em horário de pico na Riachuelo: cliente com a peça na mão, decisão de compra já tomada,
  aguardando apenas a operação de caixa. `[VERIFICAR: tempo médio de fila — medir em campo]`
- Abandono de compra por fila (*queue abandonment*). `[VERIFICAR: taxa, literatura de varejo]`
- Perda por furto (quebra operacional) no varejo de vestuário brasileiro. `[VERIFICAR: ABRAS/IDV]`

### 1.2 Decomposição do tempo de caixa

| Etapa | Quem executa | Automatizável hoje? |
|---|---|---|
| Identificar item (código de barras) | operador | **Sim** — QR/NFC no celular |
| Calcular total, aplicar promoção | PDV | **Sim** — app |
| Receber pagamento | operador + pinpad | **Sim** — Pix / carteira digital |
| **Remover a hard tag antifurto** | **operador + destravador** | **Não** — gargalo real |
| Ensacar | operador | Sim (autosserviço) |

**Conclusão do diagnóstico:** 4 das 5 etapas já têm solução madura. A quinta é o que mantém o
caixa obrigatório. É esse o problema a atacar.

### 1.3 Conflito central (formulação tipo TRIZ)
- Para **não perder mercadoria**, o item precisa estar travado até o pagamento.
- Para **não ter fila**, ninguém pode depender de um funcionário para destravar.
- → A trava precisa ser condicionada ao **pagamento**, não à **presença de um operador**.

---

## 2. Metodologia — a fusão (`2-metodologia.tex`)

### 2.1 Patentes e tecnologias de origem

**Patente A — US 7.564.360 B2** (Cote e Abadi; Checkpoint Systems; 2009)
*RF Release Mechanism for Hard Tag*. Elementos reivindicados relevantes:

- mecanismo de travamento com liberação, para prender a tag à peça;
- circuito ressonante EAS **ou** circuito RFID (resposta a sinal de RF);
- **circuito de colheita de energia de RF ambiente** (tag sem bateria);
- circuito detector do sinal de liberação, alimentado pela colheita de energia;
- **atuador eletromecânico** que abre a trava ao receber o sinal de liberação.

**Tecnologia B — identificação e pagamento pelo próprio cliente**

- NFC (ISO 14443 / NDEF) e/ou QR Code no item, lidos pelo smartphone;
- pagamento no app (Pix, carteira digital, Riachuelo Card);
- backend emitindo autorização criptográfica de liberação.

### 2.2 O que a fusão cria que nenhuma das partes tem

| Capacidade | Patente A sozinha | Tecnologia B sozinha | **Fusão** |
|---|---|---|---|
| Identifica o produto para o cliente | não | sim | sim |
| Cobra sem operador | não | sim | sim |
| Libera a tag sem operador | sim, mas sem saber se pagou | não | **sim, condicionado ao pagamento** |
| Protege contra furto | sim | não | sim |

A fusão se sustenta porque A resolve a **atuação física** e B resolve a **autorização**, e
nenhuma das duas resolve o problema sozinha. O elo novo — e a contribuição de engenharia do
grupo — é o **vínculo criptográfico entre a confirmação de pagamento e o sinal de liberação**,
que a patente A não trata: nela o sinal de liberação é aberto.

### 2.3 Métodos de apoio a usar no relatório
- Observação em loja e cronoanálise da fila (dado primário).
- Diagrama de causa-efeito / árvore do problema.
- QFD simplificado (voz do cliente → requisitos técnicos).
- Matriz de decisão para as alternativas de liberação (§3.3).
- FMEA das falhas e fraudes (§5).

---

## 3. Proposta — o produto (`3-proposta.tex`)

### 3.1 Nome de trabalho
**Riachuelo Tag&Go** (alternativa: *Passe Livre*) — é um sistema, não apenas uma tag.

### 3.2 Arquitetura em quatro camadas

```
[1] TAG HIBRIDA (produto fisico)
    corpo + pino | antena UHF RFID (EPC Gen2) | antena NFC 13,56 MHz
    RF harvesting -> supercapacitor | detector de sinal de liberacao (autenticado)
    atuador (liga SMA ou solenoide) -> destrava o pino
              |
[2] APP DO CLIENTE (smartphone)
    le NFC/QR -> mostra produto, preco, tamanho, disponibilidade
    carrinho -> pagamento (Pix / cartao / Riachuelo Card)
              |
[3] BACKEND
    valida pagamento -> emite TOKEN DE LIBERACAO assinado, atrelado ao EPC do item,
    de validade curta e uso unico -> registra a venda no ERP/PDV
              |
[4] LOJA
    Estacao de Liberacao (pad de baixo custo, sem funcionario)
    Portico de saida: le os EPCs via UHF e confere contra as vendas do minuto
```

### 3.3 Decisão de projeto crítica — quem destrava?

| Alternativa | Energia disponível | Custo | Risco | Nota |
|---|---|---|---|---|
| **(a) O próprio celular** (campo NFC alimenta a tag) | poucos mW — provavelmente **insuficiente** para o atuador `[VERIFICAR: cálculo]` | zero infra | alto | elegante, mas pode não fechar a conta de energia |
| **(b) Estação de liberação** (pad de RF dedicado, sem operador) | alta, dimensionável | baixo (n unidades por loja) | baixo | **recomendada** — é o cenário que a US 7.564.360 pressupõe |
| (c) Híbrida: o celular autoriza, o pad energiza | alta | baixo | baixo | separa autorização de energia — boa saída |

→ O **balanço de energia** é o principal cálculo de engenharia do trabalho: energia para
acionar o atuador (uma liga SMA pede da ordem de mJ a J) contra a energia colhida por RF
(µW a mW) e o tempo de carga do supercapacitor. Esse número decide se (a) é viável ou se a
resposta é (b)/(c) — e é ele que dá densidade técnica à proposta.

### 3.4 Fluxo do cliente (processo)

1. Pega a peça na arara.
2. Encosta o celular na tag → o app abre com produto, preço, tamanhos disponíveis.
3. Prova a peça — a tag continua travada; o antifurto nunca é desligado antes da hora.
4. Paga no app.
5. Passa a peça na Estação de Liberação → a tag destrava e vai para a caixa de coleta.
6. Sai pelo pórtico: a leitura UHF confere item contra venda → liberação silenciosa.

**Tempo alvo:** `[VERIFICAR/estimar]` s no fluxo novo contra o tempo de fila medido hoje.

### 3.5 Requisitos

**Funcionais**

- RF-01 — A tag só destrava mediante token válido, assinado, de uso único e vinculado ao EPC.
- RF-02 — A tag é reutilizável por N ciclos. `[VERIFICAR: definir N]`
- RF-03 — O pórtico distingue item pago de não pago sem intervenção humana.
- RF-04 — O app funciona com QR como *fallback* quando o celular não tem NFC.
- RF-05 — Existe caminho de compra assistida para quem não tem celular, app ou internet.

**Não funcionais**

- RNF-01 — Custo unitário da tag compatível com o reuso. `[VERIFICAR: alvo × hard tag comum]`
- RNF-02 — Tempo de destravamento inferior a 3 s.
- RNF-03 — Falso negativo do pórtico < 0,5%; alarme indevido < 1% — o alarme indevido é o que
  mais destrói a experiência, e é o requisito mais difícil.
- RNF-04 — Tag sem bateria (requisito ambiental e de manutenção, herdado da patente A).
- RNF-05 — Conformidade com a LGPD para dados de compra e de permanência do cliente na loja.

---

## 4. Processo e operação na loja

- **Aplicação das tags:** no CD (preferível — o item chega pronto para a arara) ou na loja.
- **Logística reversa das tags:** caixas de coleta na Estação de Liberação e na saída. A tag
  precisa voltar ao ciclo, senão o custo por uso explode. É um ponto de processo tão importante
  quanto o produto, e merece subseção própria.
- **Layout:** a loja perde as filas de caixa e ganha estações distribuídas, liberando área de venda.
- **Papel do funcionário:** deixa de operar caixa e passa a atendimento, prova e exceções.
- **Exceções a tratar:** sem celular; sem internet; troca e devolução; item sem tag; pagamento
  recusado após a liberação — que não pode ocorrer, pois só se destrava após confirmação.

---

## 5. Riscos e fraudes (base do FMEA)

| # | Falha ou fraude | Efeito | Mitigação |
|---|---|---|---|
| 1 | Replay do sinal de liberação | furto em escala | token de uso único e *challenge-response* na tag — o que a patente A **não** tem |
| 2 | Arrancar a tag à força | furto | tinta ou alarme sonoro na tag; o pórtico ainda lê a etiqueta RFID costurada na peça |
| 3 | Pagar item barato e destravar item caro | furto | token vinculado ao EPC específico |
| 4 | Alarme indevido no pórtico | cliente que pagou é constrangido | tolerância de leitura e fluxo de resolução sem exposição |
| 5 | Tag não retorna ao ciclo | custo | incentivo por devolução e coleta na saída |
| 6 | Cliente sem smartphone | exclusão | caixa assistido mantido, em número reduzido |

---

## 6. Resultados a demonstrar (`4-resultados.tex`)

- Tempo de atendimento **antes e depois** (cronoanálise + simulação de filas M/M/c).
- Capacidade de atendimento no pico com a mesma área de loja.
- Quebra por furto projetada — a proteção não piora, pois a trava só sai após o pagamento.
- Custo de tags, estações, pórticos e app contra a economia de horas de caixa → **payback**.
- Análise de sensibilidade nos parâmetros incertos (custo da tag, taxa de adoção do app).

---

## 7. Pendências para o grupo

1. Fazer o **balanço de energia** da tag (§3.3) — é o que dá densidade técnica ao trabalho.
2. Escolher e ler a **segunda patente** (lado NFC/pagamento) para formalizar a fusão como par
   A + B. As citadas na própria US 7.564.360 (Mickle et al., US 6.856.291) servem de ponto de
   partida da busca.
3. Medir a fila real em uma loja Riachuelo — dado primário pesa na avaliação.
4. Levantar o custo atual de hard tag e de destravador para a comparação econômica.
