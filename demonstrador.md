# O DEMONSTRADOR — o que vocês compram e montam de verdade
## Estação de Liberação Tag&Go

> Este documento substitui a abordagem anterior como **plano de construção**.
> O CAD da etiqueta integrada (`fusion/TagAndGo.py`) continua válido — mas como
> **projeto do produto futuro**, não como o que vocês montam neste semestre.
> Preços são ordem de grandeza para conferir no dia da compra.

---

## 1. O erro que eu estava cometendo

Eu vinha projetando uma etiqueta de 48 × 80 × 18 mm com fio de nitinol, microcontrolador e
cursor com rampa lá dentro. Isso é **engenharia de produto para produção em escala** — meses
de trabalho, e ainda assim um protótipo frágil.

O que o trabalho pede é **demonstrar o processo**: pagou → reconheceu → liberou. E para isso
a inteligência pode ficar na **estação**, não na etiqueta.

### A pergunta que reorganiza tudo

> A etiqueta precisa ser inteligente, ou basta a **estação** ser inteligente?

Se basta a estação, então:

- a etiqueta continua sendo a **hard tag comum de R$ 3** que a loja já usa;
- não há eletrônica, bateria nem fio SMA por etiqueta;
- o sistema é **compatível com o parque instalado** — a Riachuelo não troca nada;
- o custo desaba.

### A conta, para uma loja com 5.000 peças etiquetadas

| | Etiqueta inteligente | **Estação inteligente** |
|---|---|---|
| Custo por etiqueta | R$ 25 (em escala) | **R$ 3** (a atual) |
| 5.000 etiquetas | R$ 125.000 | **R$ 15.000** |
| Estações por loja | 6 × R$ 400 = R$ 2.400 | 6 × R$ 1.500 = R$ 9.000 |
| **Total por loja** | **R$ 127.400** | **R$ 24.000** |

**Fator 5 de diferença.** E a estação ainda dispensa a troca de todo o estoque de etiquetas.

> Essa comparação é um dos resultados mais fortes que o trabalho pode ter. Ela não sai de
> catálogo — sai de perguntar *onde* colocar a inteligência. Coloquem no relatório.

### E a patente?

A US 7.564.360 é **referência, não amarra**. O que ela ensina é o princípio:
*a liberação deixa de depender de um operador e passa a depender de um sinal autorizado*.
Esse princípio vale nos dois arranjos. Onde fica o atuador é decisão de projeto de vocês —
e vocês têm o direito de decidir diferente da patente, desde que justifiquem. A conta acima
**é** a justificativa.

---

## 2. O fluxo, exatamente como você descreveu

```
1. cliente pega a peca
2. encosta o celular na etiqueta (NFC) ou le o QR
3. app mostra produto e preco -> cliente PAGA
4. cliente apoia a peca na ESTACAO
5. estacao LE a etiqueta e pergunta ao servidor: "esta paga?"
6. LED VERDE acende + display diz "Pago. Pode liberar"
7. cliente APERTA O BOTAO
8. servo aproxima o ima -> a garra abre -> PINO SOLTA
9. etiqueta cai na caixa de coleta; cliente sai com a peca
```

Se não estiver paga: **LED vermelho**, buzzer curto, display diz o motivo. O botão não faz nada.

### Por que o botão existe

Não é enfeite. Ele resolve três coisas:

1. **Segurança** — nada se move até a pessoa estar com a mão na peça, posicionada.
2. **Clareza** — o cliente entende que ele está no controle, não a máquina.
3. **Sincronismo** — a etiqueta pode estar mal encaixada; o botão dá tempo de ajeitar.

Um botão grande, tipo arcade, iluminado. Na demonstração, é o momento que a banca lembra.

---

## 3. Como a estação destrava — a decisão central

A garra de esferas da hard tag abre com **ímã**. Hoje quem encosta o ímã é o funcionário do
caixa. Três formas de tirar o funcionário do meio:

| Opção | Como | Custo | Risco | Veredito |
|---|---|---|---|---|
| **(a) Destravador comercial + servo** | um servo aproxima o destravador magnético que a loja já usa | R$ 60–140 | **baixo** | **escolhida** |
| (b) Eletroímã | bobina que faz o campo eletricamente | R$ 40–90 | médio — força e calor | alternativa |
| (c) Fio SMA dentro da etiqueta | o que eu vinha projetando | R$ 60+/etiqueta | alto | **só no produto futuro** |

**A (a) é a certa para o demonstrador**, e o argumento é bonito no relatório:

> *"O gesto que o operador fazia com a mão passa a ser feito por um servo, condicionado a uma
> autorização criptográfica em vez de à presença de um funcionário."*

Funciona na primeira tentativa, usa peça que já existe, e não depende de nenhuma medição fina.

---

## 4. Lista de compras — Mercado Livre / Shopee

Os termos entre aspas são **o que digitar na busca**.

### 4.1 Estação de Liberação

| # | Item | Buscar por | Qtd | R$ |
|---|---|---|---|---|
| 1 | Microcontrolador com WiFi | `"ESP32 DevKit V1 30 pinos"` | 1 | 35–60 |
| 2 | Leitor NFC/RFID 13,56 MHz | `"módulo RFID RC522"` | 1 | 15–30 |
| 3 | **Destravador magnético de etiqueta** | `"destravador etiqueta antifurto"` ou `"detacher magnético 12000GS"` | 1 | 50–120 |
| 4 | Servo para mover o ímã | `"servo MG996R metálico"` | 1 | 30–50 |
| 5 | Botão grande iluminado | `"botão arcade 60mm LED"` | 1 | 12–25 |
| 6 | LED indicador | `"anel LED WS2812 16 LEDs"` | 1 | 20–35 |
| 7 | Display | `"display OLED 0.96 I2C"` | 1 | 20–35 |
| 8 | Buzzer | `"buzzer ativo 5V"` | 1 | 5–10 |
| 9 | Fonte | `"fonte chaveada 5V 3A"` | 1 | 25–45 |
| 10 | Protoboard e jumpers | `"kit protoboard 830 jumpers"` | 1 | 30–50 |
| 11 | Caixa | `"caixa patola PB-207"` ou MDF cortado | 1 | 30–70 |
| | | | **Total** | **≈ R$ 270–530** |

> **Item 3 é o coração e o de maior risco de compra.** Confirme na descrição que serve para
> *hard tag / etiqueta tipo concha*, e não só para etiqueta macia. Comprem **um** e testem à mão
> antes de montar qualquer coisa em volta.

### 4.2 Etiquetas e insumos

| # | Item | Buscar por | Qtd | R$ |
|---|---|---|---|---|
| 12 | Hard tags com pino | `"etiqueta antifurto concha com pino"` | 10 | 3–8 cada |
| 13 | Adesivo NFC | `"tag NFC NTAG213 adesivo 25mm"` | 20 | 2–4 cada |
| 14 | Caixa coletora | qualquer caixa com tampa | 1 | 20 |
| | | | **Total** | **≈ R$ 130–200** |

### 4.3 Opcional — pórtico de saída (só se sobrar tempo)

| # | Item | Buscar por | R$ |
|---|---|---|---|
| 15 | Leitor UHF | `"módulo leitor UHF RFID 915MHz UART"` | 150–400 |
| 16 | Inlay UHF | `"etiqueta RFID UHF adesiva 915"` | 2–5 cada |

### Total realista

| Escopo | Custo | Por pessoa (8) |
|---|---|---|
| **Estação + etiquetas** (recomendado) | **R$ 400–730** | **R$ 50–91** |
| Com pórtico | R$ 600–1.200 | R$ 75–150 |

---

## 5. Ligações

```
ESP32
 |
 +-- RC522 (SPI)         SDA->D5  SCK->D18  MOSI->D23  MISO->D19  RST->D4   3V3
 +-- Servo MG996R        sinal->D13     alimentacao 5V DIRETO DA FONTE (nao do ESP32)
 +-- Botao arcade        contato->D14 (INPUT_PULLUP, aciona em LOW)
 +-- LED do botao        ->D27 via resistor 220R
 +-- Anel WS2812         data->D26
 +-- OLED (I2C)          SDA->D21  SCL->D22
 +-- Buzzer              ->D25
 |
 +-- WiFi -> backend
```

**Dois erros que queimam placa — evitem:**

1. **Nunca alimente o servo pelo pino 5V do ESP32.** O MG996R puxa mais de 1 A no pico e
   derruba a placa. Fonte separada, **GND comum** entre fonte e ESP32.
2. **Capacitor de 1000 µF** entre 5 V e GND perto do servo, senão o ESP32 reinicia toda vez
   que o servo se mexe. É o bug mais comum e o mais chato de diagnosticar.

---

## 6. O que o firmware faz

```
loop:
  se ha etiqueta no leitor RFID:
      uid = ler_uid()
      LED = amarelo, display = "Verificando..."
      resposta = GET /tag/<uid>/status        <- backend

      se resposta == PAGO:
          LED = VERDE, botao acende
          display = "Pago. Aperte o botao"
          espera o botao (ate 30 s)
          se apertou:
              servo.write(ANGULO_LIBERA)      <- ima encosta
              delay(1500)
              servo.write(ANGULO_REPOUSO)     <- ima recua
              buzzer curto, LED = azul
              POST /tag/<uid>/liberada
              display = "Liberado. Deixe a etiqueta na caixa"
      senao:
          LED = VERMELHO, buzzer duplo
          display = motivo ("nao pago" / "sem internet")
```

Bibliotecas: `MFRC522`, `ESP32Servo`, `Adafruit_NeoPixel`, `Adafruit_SSD1306`, `HTTPClient`.
Todas instaláveis pelo gerenciador da IDE Arduino, todas gratuitas.

---

## 7. Ordem de montagem — não pule a etapa 1

| Semana | O que fazer | Por quê |
|---|---|---|
| **1** | Comprar o destravador e **abrir uma etiqueta com ele, na mão** | Se o destravador não abrir a etiqueta que vocês compraram, nada mais importa. R$ 100 e uma tarde |
| 2 | Servo + destravador numa base de papelão, abrindo a etiqueta sozinho | prova o acionamento sem eletrônica |
| 3 | RC522 lendo o UID do adesivo NFC | prova o reconhecimento |
| 4 | ESP32 + WiFi + backend falso (responde sempre "pago") | prova a comunicação |
| 5 | Fluxo completo com LED, botão, display | **demonstrador pronto** |
| 6 | App e pagamento em sandbox ligados de verdade | fecha a ponta do cliente |
| 7 | Caixa, acabamento, vídeo | apresentação |

> **A etapa 1 é o portão.** Se o destravador não abrir a etiqueta, troquem de modelo de
> etiqueta (ou de destravador) na semana 1, não na semana 6.

---

## 8. O que fica de cada coisa no relatório

| Seção | O que entra |
|---|---|
| `1-diagnostico` | a fila medida em loja; o gargalo é a etiqueta, não o pagamento |
| `2-metodologia` | a fusão de patentes; **a decisão de onde colocar a inteligência** (§1) |
| `3-proposta` | a estação, o fluxo, o protocolo de autorização, e o **produto futuro** (o CAD da etiqueta integrada) |
| `4-resultados` | o demonstrador funcionando, tempo medido, **a comparação de custo do §1** |
| `1-conclusao` | limitações: um só modelo de etiqueta testado, sem pórtico se não der tempo |

O CAD que já está pronto (`fusion/TagAndGo.py`) **não foi trabalho perdido** — ele vira a
figura da seção "produto futuro" e mostra que vocês pensaram a versão de produção, não só a
maquete. É exatamente o que se espera num projeto de produto: o demonstrador prova o
processo, o CAD mostra para onde ele evolui.
