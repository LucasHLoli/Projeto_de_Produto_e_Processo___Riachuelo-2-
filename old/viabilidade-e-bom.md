# Viabilidade, balanço de energia e lista de compras
## Riachuelo Tag&Go — do conceito ao protótipo construível

> Este documento existe para responder a uma pergunta só: **o que dá para comprar e montar
> de verdade, com orçamento de trabalho de graduação?**
> Todos os preços são **ordem de grandeza para conferir** — cote antes de fechar o orçamento.

---

## 1. O erro que quase entrou no projeto

A primeira versão do produto assumia que a etiqueta colheria energia de **RF ambiente** para
acionar um atuador mecânico. A conta abaixo mostra que isso está errado por cinco ordens de
grandeza — e é exatamente o tipo de furo que um avaliador encontra na apresentação.

### 1.1 Energia necessária para destravar

Atuador escolhido: fio de liga com memória de forma (SMA), nitinol tipo Flexinol, Ø 0,15 mm.

| Grandeza | Valor | Origem |
|---|---|---|
| Força de tração | ~3,2 N | datasheet Dynalloy Flexinol 150 µm `[CONFIRMAR no datasheet]` |
| Resistência elétrica | ~50 Ω/m | idem |
| Comprimento adotado | 50 mm | escolha de projeto |
| Resistência do trecho | 2,5 Ω | 50 Ω/m × 0,05 m |
| Corrente de acionamento | ~0,41 A | datasheet |
| Potência | **0,42 W** | I²R = 0,41² × 2,5 |
| Tempo de aquecimento | ~1,5 s | datasheet |
| **Energia por acionamento** | **≈ 0,63 J** | P × t |
| Curso obtido | 2,0 mm | contração de 4% × 50 mm |
| Curso necessário na garra | ~1,2 mm | medir na hard tag doadora |

Margem de curso: 1,7×. Confortável.

### 1.2 Energia disponível, por fonte

| Fonte | Potência realista | Tempo para 0,63 J | Veredito |
|---|---|---|---|
| RF ambiente (antena de ~9 cm², densidade ~0,1–1 µW/cm²) | ~5 µW | **~35 horas** | **Inviável** |
| Campo NFC de leitor dedicado (ex. saída de *energy harvesting* do ST25DV) | ~6 mW | ~105 s | Inviável pela experiência do cliente |
| Indução dedicada, padrão Qi 5 W | 5 W | ~1,5 s (limitado pelo aquecimento do fio, não pela energia) | **Viável** |
| Contatos elétricos diretos (pogo pins) | 5 W ou mais | ~1,5 s | **Viável e trivial** |

> **Conclusão que vale ouro no relatório:** o gargalo nunca foi a energia total (0,63 J é
> pouquíssimo), e sim a **potência instantânea**. Isso obriga a etiqueta a receber energia de
> uma **fonte dedicada e próxima** — ou seja, **a Estação de Liberação não é uma conveniência
> de projeto, é uma imposição física.** Esse é o resultado de engenharia mais forte do trabalho.

### 1.3 Isso contraria a patente-base?

Não. Relendo a US 7.564.360 B2, o diagrama do sistema inclui um *Tag Interrogation Device* —
um interrogador dedicado que emite o campo. A expressão "ambient RF" na patente refere-se ao
campo do interrogador, não a rádio-frequência do ambiente urbano. O que fizemos foi
**dimensionar** esse campo e concluir que ele precisa ser de acoplamento próximo.

---

## 2. Princípio de projeto: não projete o que dá para comprar

| Subsistema | Projetar do zero | **Comprar / canibalizar** |
|---|---|---|
| Garra de esferas que prende o pino | meses de projeto de precisão | **hard tag comercial (R$ 3–5)** — a garra já é exatamente a peça desejada |
| Pino (tack) | torneamento, tratamento | vem junto com a hard tag |
| Identificação para o celular | projeto de antena NFC | **adesivo NTAG213 (R$ 2)** |
| Leitura no pórtico | projeto de antena UHF | **inlay UHF EPC Gen2 (R$ 2)** |
| Lógica e autenticação | PCB customizada | **ESP32-C3 (R$ 25)**, HMAC em software |
| Energia | circuito de harvesting | **pogo pins ou módulo Qi receptor** |
| Carcaça | molde de injeção (R$ 30 mil+) | **impressão 3D** |

**Ganho colateral para o relatório:** usar a garra de hard tags comerciais significa que o
sistema é **compatível com o parque de etiquetas já instalado** na Riachuelo. Isso reduz o
custo de adoção e é um argumento comercial forte, não uma gambiarra.

---

## 3. Duas trilhas — separe explicitamente no relatório

### Trilha A — Produto de produção (o que vai na seção "Proposta")
Etiqueta integrada, injetada, com garra própria, SMA embutido, acoplamento indutivo,
envelope 42 × 67 × 15,5 mm, alvo de custo por unidade em escala.
É o **projeto de produto**. Não precisa ser construído.

### Trilha B — Protótipo funcional (o que vocês constroem e demonstram)
Peças de prateleira, carcaça impressa, garra canibalizada, alimentação por contato.
Envelope maior (≈ 52 × 80 × 18 mm) — **e tudo bem**. O protótipo prova o **conceito e o
fluxo**, não a manufatura.

> Deixar essa distinção explícita é prática normal de desenvolvimento de produto
> (*proof of concept* × *design for manufacturing*) e evita a crítica de "isso não é fabricável".

---

## 4. Arquitetura do protótipo (Trilha B)

```
CELULAR                    ETIQUETA                  ESTACAO DE LIBERACAO         PORTICO
-------                    --------                  --------------------         -------
le NTAG213 (NFC)  <----->  adesivo NTAG213           ESP32 + fonte 5V             modulo UHF
ou le QR                   (passivo, sem energia)    pogo pins 5V                 + antena
   |                            |                    LED de estado                    |
   v                            v                         |                           v
 PWA / app                 ESP32-C3 (so liga                v                    confere EPC
   |                       quando na estacao)          valida token com          contra vendas
   v                       verifica HMAC               o backend                 do minuto
 pagamento                 aciona SMA                       |                         |
 (Pix sandbox)                  |                           v                         v
   |                            v                     energiza os pinos          verde / alerta
   v                       garra abre,                somente se pago
 BACKEND -> token          pino sai
```

**Segurança sem complicar:** o ESP32 da etiqueta guarda uma chave própria. A estação envia
um desafio; a etiqueta responde com HMAC-SHA256. Só então aciona o SMA. Isso impede clonagem
por repetição de sinal — que é justamente o que a patente-base **não** resolve, e portanto é
contribuição original do grupo.

---

## 5. Lista de compras (BOM)

> Fontes típicas: Mercado Livre, AliExpress, Baú da Eletrônica, Robocore, Curto Circuito.
> Preços de **ordem de grandeza** — cotar.

### 5.1 Etiqueta protótipo — fazer **3 unidades**

| Item | Especificação | Qtd/un | R$/un | Observação |
|---|---|---|---|---|
| Hard tag comercial (doadora) | tipo concha, pino de aço | 1 | 3–5 | comprar **10** para ter sobra e peças de teste |
| Fio SMA Flexinol | Ø 0,15 mm, 1 m | 0,05 m | 120 / m | um metro serve para todas as unidades |
| Microcontrolador | ESP32-C3 Super Mini | 1 | 25 | 22,5 × 18 × 4 mm — **medir a peça real** |
| MOSFET + resistores | canal N logic-level, ex. AO3400 | 1 | 3 | driver do SMA |
| Adesivo NFC | NTAG213, Ø 25 mm | 1 | 2 | colado na face superior |
| Inlay UHF | EPC Gen2, ≤ 70 mm de comprimento | 1 | 2 | **conferir o comprimento**, inlays longos não cabem |
| Pogo pads | discos de latão Ø 6 mm | 2 | 3 | na face inferior |
| Filamento / resina | carcaça em 2 partes | — | 15 | PETG ou resina rígida |
| Insertos térmicos M2 | + parafusos M2 × 6 | 4 | 4 | substituem os snap fits |
| **Subtotal por etiqueta** | | | **~R$ 60** | fora o carretel de SMA |

**3 etiquetas + 1 m de SMA + 10 hard tags doadoras ≈ R$ 350**

### 5.2 Estação de liberação — 1 unidade

| Item | Especificação | R$ |
|---|---|---|
| ESP32 DevKit (WiFi) | comunica com o backend | 30 |
| Fonte 5 V / 3 A | — | 30 |
| Pogo pins | mola, Ø 2 mm, 4 unid. | 20 |
| Anel de LED | WS2812, 12 LEDs | 25 |
| Carcaça impressa 3D | ~200 g de filamento | 40 |
| Cabos, conectores, protoboard | — | 30 |
| **Subtotal** | | **~R$ 175** |

### 5.3 Pórtico de saída — 1 unidade *(opcional, ver §6)*

| Item | Especificação | R$ |
|---|---|---|
| Módulo leitor UHF RFID | UART, alcance ~1 m (ex. família R200 / JRD-4035) | 150–400 `[COTAR]` |
| Antena UHF circular | 3–6 dBi, se não vier junta | 100–200 |
| Raspberry Pi ou ESP32 | lógica do pórtico | 30–250 |
| Estrutura | perfil de alumínio, PVC ou MDF | 100 |
| **Subtotal** | | **~R$ 400–800** |

### 5.4 Software

| Item | Custo |
|---|---|
| App do cliente — PWA (Web NFC no Chrome/Android; QR como *fallback* em iOS) | R$ 0 |
| Backend — Firebase / Supabase, camada gratuita | R$ 0 |
| Pagamento — Mercado Pago ou Gerencianet em **sandbox** | R$ 0 |

> **Não use dinheiro real na demo.** Sandbox faz o Pix inteiro sem transação verdadeira,
> e evita problema de conformidade num trabalho acadêmico.

---

## 6. Plano em níveis — escolha até onde ir

Cada nível é uma demonstração completa por si só. Subam de nível só depois que o anterior
estiver funcionando.

| Nível | O que demonstra | Custo | Esforço | Risco |
|---|---|---|---|---|
| **0 — Maquete** | vídeo do fluxo, telas do app, hard tag cortada mostrando a garra | ~R$ 50 | 1 semana | nenhum |
| **1 — Destrava** | etiqueta que abre ao ser posta na estação; celular lê o NFC e mostra o produto | ~R$ 300 | 3 semanas | baixo |
| **2 — Fluxo completo** | + pagamento em sandbox + token HMAC + a estação só libera se pago | ~R$ 500 | 5 semanas | médio |
| **3 — Com pórtico** | + leitura UHF na saída conferindo item contra venda | ~R$ 1.100 | 8 semanas | alto — o UHF é a parte que mais dá trabalho |

**Recomendação:** mirar o **Nível 2** e tratar o pórtico como Nível 3 opcional. O Nível 2 já
demonstra a tese inteira do trabalho (o antifurto se resolve sem operador), e o pórtico é a
parte com maior chance de consumir tempo sem agregar argumento novo.

Dividido por 8 pessoas, o Nível 2 dá cerca de **R$ 65 por integrante**.

---

## 7. Riscos técnicos reais e como reduzir

| # | Risco | Probabilidade | Mitigação |
|---|---|---|---|
| 1 | O SMA não vence a mola da garra doadora | média | **medir a força da mola antes de projetar** (dinamômetro ou pesos); se faltar força, usar alavanca 2:1 ou dois fios em paralelo |
| 2 | Curso do SMA insuficiente | baixa | curso = 4% do comprimento — basta alongar o fio (já há margem de 1,7×) |
| 3 | SMA não esfria e não rearma | média | ciclo de trabalho baixo (1 acionamento a cada ~10 s) é suficiente para o uso real |
| 4 | Inlay UHF não cabe na carcaça | média | escolher inlay curto **antes** de fechar o CAD; parametrizar no Fusion |
| 5 | iPhone não lê NFC como esperado | média | QR Code como caminho principal na demo; NFC como diferencial em Android |
| 6 | Módulo UHF barato com alcance pequeno | alta | é o motivo de o pórtico ser Nível 3; testar o módulo isolado antes de montar a estrutura |
| 7 | Carcaça impressa não fecha por tolerância | alta | folga de 0,3 mm em impressão FDM (não 0,15 mm como em injeção); imprimir um corpo de prova de encaixe primeiro |

---

## 8. Sequência de trabalho recomendada

1. **Comprar primeiro, desenhar depois.** Compre as hard tags doadoras, o ESP32 e o SMA
   **antes** de fechar o CAD.
2. **Desmonte uma hard tag** e meça: diâmetro e altura da garra, curso necessário, força da mola.
3. **Prove o acionamento na bancada**, sem carcaça nenhuma: fonte de laboratório + SMA + garra
   presa numa morsa. Se isso não funcionar, nada mais importa — descubra na semana 1, não na 6.
4. **Só então** preencha os parâmetros do CAD com os valores medidos e imprima a carcaça.
5. App e backend em paralelo, por outra dupla, desde o início.

> O passo 3 é o **teste que mata o projeto se for para morrer**. Faça-o primeiro e barato.

---

## 9. O que muda no relatório

| Seção | Conteúdo novo |
|---|---|
| `1-diagnostico` | inalterado — o gargalo continua sendo a destravação da tag |
| `2-metodologia` | acrescentar o **balanço de energia** (§1) como método de decisão |
| `3-proposta` | Trilha A (produto) **e** Trilha B (protótipo), explicitamente separadas; tabela de decisão da fonte de energia |
| `4-resultados` | resultado do teste de bancada (§8.3), tempo medido de destravamento, BOM e custo |
| `3-pos/1-conclusao` | limitações honestas: envelope maior no protótipo, pórtico não implementado se ficarem no Nível 2 |

Declarar as limitações **antes** que perguntem é o que separa um trabalho maduro de um
trabalho otimista.
