# Plano de construção do protótipo Tag&Go (Grupo 4, PRO3474)

Data-base: 29/09/2026 (terça). Marcos: R3 em 04/11 (qua), R4 em 23/11 (seg), prova em 25/11 (qua), protótipo e apresentação em 07/12 (seg) e 09/12 (qua).

Os preços foram consultados em 29/09/2026. Os da Eletrogate, Smart Kits, Fermarc e AliExpress foram lidos na página da loja. Os do Mercado Livre (ML) vieram do título indexado pelo buscador, com confiança média: confira no carrinho antes de pagar. Onde aparece "(estimativa)", o número não foi medido nem publicado.

---

## 0. Resposta curta: o que é preciso

1. Duas versões do protótipo.
   - Uma bancada: grande, ajustável, comandada pelo Arduino, para medir a garra e o atuador.
   - Uma etiqueta compacta: carcaça impressa de 98 x 82 x 26 mm, com ESP32-C3, LiPo, micromotor N20 e a garra real de 3 esferas tirada de uma etiqueta comercial.
2. Compras (pior caso, com as 100 etiquetas compradas no ML):
   - Lista essencial: R$ 525,94 (R$ 87,66 por aluno). Reserva: R$ 74,06 (12,3%), que precisa cobrir o frete da Smart Kits (R$ 20 a 35, estimativa) e sobrar pelo menos R$ 40.
   - Essencial + recomendados (N20 298:1 e 2ª LiPo): R$ 588,64, reserva de R$ 11,36. Só compre os recomendados se a reserva depois dos fretes reais continuar em R$ 40 ou mais.
   - Se a Riachuelo ceder 10 ou mais etiquetas usadas com pinos até 02/10, as etiquetas saem da lista: essencial R$ 382,20; com recomendados R$ 444,90 e reserva de R$ 155,10.
3. O destacador não cabe no orçamento (R$ 140,86 ou mais) e deve ser pedido emprestado à Riachuelo.
4. Três pontos ainda não verificados podem derrubar o mecanismo. A bancada decide cada um antes de qualquer carcaça:
   - o sentido de acionamento: o carretel precisa ser PUXADO para cima, por um garfo sob um colar; empurrar por cima trava ainda mais;
   - a margem de força do N20 100:1 com came e rampa, que pela conta fica entre 1,1x e 3,1x, abaixo da meta E04 >= 3 no pior caso;
   - o curso e a força reais da garra.
5. Esta semana: inventário de ferramentas até 30/09, e-mail à Riachuelo até 30/09, pedido da Eletrogate em 01/10, pedidos da Smart Kits e do ML em 02/10, teste do Web Bluetooth em 3 celulares até 04/10.
6. Regra de ouro dos documentos do grupo: comprar e medir antes de fechar o CAD, e provar o acionamento com a garra presa na bancada antes de qualquer carcaça.

---

## 1. Escopo do protótipo

Justificativa:
- Na Aula 14, o professor aceita implementar parte das funções no protótipo (o exemplo foi 2 de 10), desde que a concepção apresentada seja a completa.
- Na Aula 06, ele pede que o protótipo mostre a funcionalidade principal do produto físico, e desestimula reduzir o projeto a algo pequeno.
- Com R$ 600, o dinheiro vai todo para o núcleo físico: reter, autorizar, sinalizar e liberar.
- O R3 (04/11) é o projeto DETALHADO do PRODUTO, não um relatório do protótipo. Por isso o plano abre uma frente de produto a partir da S3 (seção 4).

| Função (R2) | No protótipo | Como |
|---|---|---|
| F1 Reter a peça (pino + garra de 3 esferas) | Real | Garra metálica canibalizada de mini tag comercial (copo, esferas, carretel e mola), numa sede impressa em PETG |
| F5/F10 Receber a autorização pelo celular | Real | QR de 28 mm, página web (GitHub Pages, HTTPS) com Web Bluetooth, pagamento simulado, token HMAC-SHA256 emitido por um Cloudflare Worker gratuito e repassado por BLE |
| F11 Sinalizar | Real | LED RGB (vermelho/verde) e buzzer ativo com transistor, 4 padrões |
| F6 Liberar pelo botão | Real | 2º aperto: N20, came, garfo que LEVANTA o carretel ~1,2 mm (a medir) e o pino sai |
| Energia própria | Real | LiPo de 400 mAh com PCM e TP4056. A célula de 150 mAh fica só no desenho do produto (ver risco 5) |
| Liberador de Balcão | Simulado, recomendado se houver tempo | Arduino Uno fala o mesmo protocolo por UART, usando só GND e dados. É o caminho de contingência do iPhone prometido no R2. O 5 V do terceiro contato fica para a Bandeja de Recarga (seção 2.5) |
| NFC NTAG213 com ferrite | Opcional | Adesivo NTAG215 (R$ 20,10) sob o QR, se sobrar reserva |
| C1.10 EAS | Só físico, sem ensaio | Reaproveitar o elemento RF 8,2 MHz da mini tag dentro da carcaça. Não há antena de portal para testar |
| Compra Rápida no iPhone (App Clip) | Tela no Figma e demonstração pelo app Bluefy | O App Clip exige Apple Developer (US$ 99/ano, fora do orçamento); a conta gratuita não tem App Clip. Declarar no relatório que o go/no-go do Core Bluetooth no App Clip não foi feito |
| Jornada Completa (app) | Telas no Figma | Fluxo navegável, sem código |
| Coletor de Etiquetas, Bandeja de Recarga, Estação de Cadastro | Fora | Renderização do CAD e fluxograma |
| Logística reversa (SS5) | Fora | Fluxograma e estimativas do R2 |
| E11 (desacoplador de até 12.000 GS) | Fora | A garra canibalizada tem carretel ferromagnético e reprovaria. Explicar que o produto exige carretel não ferromagnético. Se a Riachuelo emprestar o destacador, rodar as 20 tentativas e registrar o resultado honestamente |
| Aparência do produto final | Modelo não funcional | Etiqueta impressa, lixada e pintada, com QR e pictograma, ao lado da etiqueta funcional, mais a vista explodida do produto (150 mAh, placa única, carcaça injetada). Assim a banca vê o PRODUTO, não só as placas de desenvolvimento |

---

## 2. Arquitetura do protótipo

### 2.1 Visão geral

```
[Celular Android/Chrome]  --HTTPS + CORS-->  [Cloudflare Worker: HMAC(K_tag, tag_id|nonce|transacao)]
      |  lê QR -> página github.io -> "Pagar" (simulado) -> pede token
      |  Web Bluetooth (GATT)
      v
[Etiqueta: ESP32-C3 SuperMini] -- DRV8833 (nSLEEP em GPIO) --> N20 -> came -> garfo -> colar do carretel
      |- LED RGB + buzzer (BC337) + botão (acorda) + fim de curso
      |- LiPo 400 mAh (PCM) -> chave deslizante -> VM do motor e diodo -> 5V do ESP32
      '- 3 contatos na face: GND e UART <-- [Arduino Uno = Liberador de Balcão simulado]
                             5 V -> IN+ do TP4056 (recarga)

[Bancada: Arduino Uno + HX711 + célula de 5 kg + N20/SG90] -> mede mola, liberação, torque, atuador, ciclos
```

### 2.2 Versão (a): bancada de mecanismo

- O que é: uma base impressa em PLA ou PETG, de tamanho livre (algo como 150 x 100 mm, estimativa), com:
  - um berço que prende a garra real (copo, esferas, carretel, mola) retirada da mini tag;
  - trilhos para o garfo e o cursor;
  - suporte do motor com furos oblongos, para ajustar a posição;
  - pares intercambiáveis de (excêntrico, rampa) com o MESMO curso vertical de ~1,2 mm, em vez de 3 ângulos soltos (ver 2.4):
    - A: excêntrico e = 4 mm, cursor com curso de 8 mm e rampa de 8,5° (geometria do R2);
    - B: excêntrico e = 2 mm, cursor com curso de 4 mm e rampa de ~17°;
    - C: came direto sob o colar do carretel, sem cursor (subida de 1,2 mm).
- Atuadores ensaiados: N20 100:1 com DRV8833 (atuador do R2) e SG90 como referência e plano B.
- Instrumentação: HX711 com célula de 5 kg (~49 N). Não passe de 4 kg (~40 N). Se o atuador passar disso, a margem já é >= 5x e o teste está aprovado.
- Para que serve: tirar os números do R3, que hoje são todos estimados:
  - curso do carretel e força da mola;
  - força de liberação;
  - atrito PETG-aço;
  - torque travado do N20 a 3,7 V e a 3,4 V (braço de 10 mm apoiado no HX711);
  - força entregue no carretel por cada par e a margem E04.

### 2.3 Versão (b): etiqueta compacta de 98 x 82 x 26 mm

- Carcaça: parâmetros do `fusion/Antifurto.py` (parede de 2,4 mm, partição em Z = 13 mm, cantos com raio de 8 mm, folga de 0,6 mm), em PETG, fechada com parafusos M3 e porcas sextavadas embutidas (seção 6).
- Sentido de acionamento (go/no-go da S2): na embreagem comercial, o destacador PUXA o carretel para longe da entrada do pino, comprimindo a mola. Um cursor que corre por cima da bucha tende a EMPURRAR o carretel para baixo e trava ainda mais. Por isso:
  - o cursor vira um GARFO que entra sob um colar ou degrau do carretel e o levanta;
  - se a tag serrada não tiver colar acessível, colar com epóxi uma arruela de latão ou alumínio no carretel, ou usar uma haste de tração que atravesse a mola;
  - essa decisão entra no CAD antes da v1.
- Retorno do garfo: com o came preso numa fenda do garfo (retorno positivo) e o DRV8833 invertendo o motor, a mola de retorno é dispensável. Para testes, use mola de caneta.
- Atuador padrão: micromotor N20 com came, como escolhido no R2. Caixa de redução de 12 x 10 mm (dado da Fermarc para N20); deitado, ocupa ~10 mm de altura.
  - O fim de curso é uma das chaves táteis 6x6. O R2 pede fim de curso (I4) e o motor não pode ficar travado: um N20 puxa até 0,67 A travado (dado Pololu para o 298:1).
- Plano B: SG90 deitado, com ~12 mm de altura. Cabe nos 26 mm junto com o ESP32-C3 e a LiPo (confirmar no CAD).
- Eletrônica: ESP32-C3 SuperMini, DRV8833, LED RGB, buzzer com BC337, botão, fim de curso, LiPo de 400 mAh (4 x 30 x 40,7 mm), TP4056 USB-C, chave deslizante SS12F46 e diodos 1N5819.

### 2.4 Atuadores: números revisados

A força a vencer ainda não foi medida. O R2 estima 2,5 N; a patente All-Tag (US 11.859.412) indica 5 a 7 N para a mola, e ~7 N de atração total na trava DURALTAG. As contas abaixo usam 5 a 7 N e atrito PETG-aço μ = 0,30 (estimado, φ = 16,7°).

Fórmula corrigida da cunha: o cursor tem atrito nas DUAS faces (rampa e apoio de trás), então F_carretel = F_horizontal / (tan(α + φ) + μ). O `Antifurto.py` só considera a face da rampa, F = F_h / tan(α + φ), e superestima a força.

| Atuador | Conta | Força no carretel | Margem contra 5 a 7 N | Decisão |
|---|---|---|---|---|
| MG90S com braço de 20 mm e rampa de 8,5° (referência do `Antifurto.py`) | O script usa 36 N no braço (0,72 N.m, 7,3 kgf.cm). O MG90S real tem 1,8 a 2,2 kgf.cm, ou 8,8 a 10,8 N no braço | 18,7 N sem o atrito de trás; 11,4 N com ele | 1,6x a 2,3x (e não 30,6x) | Não comprado (esgotado na Eletrogate). Corrigir `MEC['came']['forca']` para ~9 N no script |
| N20 100:1 + excêntrico e = 4 mm + rampa de 8,5° (par A, geometria do R2) | Torque 0,8 kgf.cm a 6 V (Piscaled; não diz se é nominal ou travado; medir na S3) cai para ~0,49 kgf.cm (0,048 N.m) a 3,7 V (estimativa proporcional). F_h = 0,048 / 0,004 = 12 N | 15,7 N travado; ~7,9 N a 50% do travamento | 1,1x a 3,1x: E04 >= 3 NÃO garantido | Testar, mas não é o favorito |
| N20 100:1 + excêntrico e = 2 mm + rampa de ~17° (par B) | F_h = 24 N; tan(33,4°) + 0,30 = 0,96 | 25 N travado; ~12,5 N a 50% | 3,6x a 5x travado; 1,8x a 2,5x a 50% | Favorito para a etiqueta com o 100:1 |
| N20 100:1 + came direto (par C) | Excêntrico de 0,6 mm sob o colar, sem cursor | > 50 N travado (estimativa) | > 7x (estimativa) | Mais força; exige alinhar came e colar no eixo |
| N20 298:1 (recomendado) | ~2,4 kgf.cm travado a 6 V (Pololu), ~1,5 kgf.cm a 3,7 V (estimativa), cerca de 3x o 100:1 | Par A: ~47 N travado, ~24 N a 50% | 3,4x a 4,7x a 50% | Seguro de torque, mesmo envelope N20 (confirmar comprimento no anúncio). ~0,7 s por meia volta a 3,7 V, dentro de E03 <= 3 s |
| SG90 | 1,2 a 1,8 kgf.cm a 4,8 V (a ProtoSupplies mediu 1,7); ~0,9 a 1,4 kgf.cm a 3,7 V (estimativa). Came direto com raio de 8 mm | 11 a 17 N | 1,6x a 3,4x | Plano B; com MT3608 (5 V) a margem sobe ~30% |
| Solenoide 5 V | 0,8 N a 3 mm e 1,1 A (Adafruit). O JF-0530B só foi achado em 6/12/24 V | < 1 N | < 1x | Descartado |
| SMA (Flexinol) | Dois fios de 42 mm: 5,0 N. Precisa de 42 mm retos e só há 5 mm | 5 N | ~1x | Descartado; fica como proposta para o produto |

Conclusões:
- Com a rampa, a força no carretel vale aproximadamente torque x eficiência / subida de 1,2 mm. A eficiência melhora com rampas MAIS íngremes. Uma "rampa mais suave" com o mesmo curso do cursor pede excêntrico maior e dá MENOS força. Não use esse plano B.
- Quem decide é a bancada: margem E04 >= 3 medida a 50% do travamento e com a LiPo a 3,4 V (o torque cai ~10%), até 21/10.
- No R3, apresentar as margens como estimativa conservadora, nunca como 30x.

### 2.5 Ligações da etiqueta compacta

Energia:
- LiPo -> B+/B- do TP4056. OUT+ -> chave deslizante SS12F46 -> trilho BAT.
- Trilho BAT -> VM do DRV8833 (motor direto na bateria, sem diodo).
- Trilho BAT -> 1N5819 -> pino 5V do ESP32-C3 (entrada do LDO).
- Contato de 5 V da face -> IN+ do TP4056 (o contato vira recarga) e também -> 1N5819 -> pino 5V do ESP32-C3. Os dois diodos formam um OU: a placa liga pelos contatos mesmo com a célula descarregada (requisito I3), e nenhum 5 V externo entra na LiPo sem passar pelo TP4056.
- O mesmo OU protege contra o USB-C do ESP32: o VBUS está ligado direto ao pino 5V, mas o diodo impede que ele alimente a bateria. Mesmo assim, desligue a chave ao gravar.
- Limitação do OU: o Schottky derruba 0,3 a 0,4 V. Com a LiPo abaixo de ~3,5 V, o ESP32 pode reiniciar (estimativa). A maior parte da carga útil da LiPo fica acima disso; registre a tensão mínima medida no E06.
- Nunca ligue a LiPo no pino 3V3: o máximo absoluto do ESP32-C3 é 3,6 V.
- Capacitor de 1000 µF / 16 V entre VM e GND, perto do motor, para evitar reset por queda de tensão.

Motor e sinais:
- DRV8833 AOUT1/AOUT2 -> N20. O pino nSLEEP (no módulo pode aparecer como SLP ou EEP; confirmar) vai a um GPIO e fica em nível baixo fora da atuação, para não gastar no sono.
- LED RGB: o verde (InGaN) tem Vf de ~2,7 a 3,2 V. Com 330 Ω a 3,3 V ele fica apagado ou muito fraco. Use 47 Ω no verde (~6 a 13 mA) e 150 Ω no vermelho (~9 mA). Confira no datasheet o limite de corrente do GPIO do C3 (o padrão é 20 mA). Teste na S2 à luz do dia.
- Buzzer ativo de 5 V (funciona de 3,5 a 5 V) no trilho BAT, chaveado por um BC337 (base com 1 kΩ no GPIO), para ter volume.
- Botão e fim de curso entre o GPIO e o GND, com pull-up interno.
- Pinos: botão numa RTC IO (GPIO0 a GPIO5, a confirmar no datasheet) para acordar do sono. Evite os pinos de strapping (GPIO2, GPIO8 e GPIO9, a confirmar no datasheet); o LED da placa fica no GPIO8 e o BOOT no GPIO9. UART do Liberador em GPIO20/21.
- IDE Arduino: placa "ESP32C3 Dev Module" com "USB CDC On Boot" ativado. Depois de entrar em deep sleep, para regravar é preciso segurar BOOT e apertar RESET.

TP4056:
- O R3 do módulo é SMD (0603 ou 0805) e vale 1,2 kΩ, o que dá 1 A de carga, alto demais para 400 mAh.
- Retire o R3 original (duas pontas do ferro, ou estanho em excesso) ANTES de soldar o de 10 kΩ do kit (~100 a 130 mA). Pôr outro resistor em paralelo AUMENTA a corrente. Com 2,7 a 3 kΩ a carga fica em ~400 mA (1C), se quiserem carga mais rápida.
- A LiPo da Smart Kits tem 3 fios: o terceiro (NTC) fica solto; isole com termorretrátil.
- Faça a primeira carga com o multímetro em série para confirmar a corrente.

Desenhe esse esquema completo antes da solda da S4.

### 2.6 Firmware e servidor

- Bibliotecas: NimBLE-Arduino v2 para o BLE e mbedTLS (`mbedtls/md.h`, já no core) para o HMAC-SHA256. ESP32Servo só no plano B.
- Estados: LIVRE, TRAVADA, AUTORIZADA, DESTRAVADA e REPROVADA. De AUTORIZADA, volta a TRAVADA após 120 s sem o botão.
- Protocolo do R2:
  1. O 1º aperto acorda a etiqueta, que gera um nonce de 128 bits (`esp_random`) e o expõe por GATT.
  2. A página envia tag_id, nonce e transação ao Worker.
  3. O Worker devolve o HMAC.
  4. A etiqueta confere o token em tempo constante e o aceita uma única vez, com menos de 120 s.
  5. LED verde; o 2º aperto liga o motor até o fim de curso e o pino sai.
- Chave: no protótipo, fica na NVS em vez de eFuse, e isso deve ser declarado no relatório.
- Worker:
  - conta gratuita da Cloudflare criada com o e-mail do grupo, não de uma pessoa;
  - a K_mestra fica como secret do Worker e documentada FORA do repositório;
  - CORS obrigatório, porque a página no github.io chama o workers.dev: responder `Access-Control-Allow-Origin` com o domínio github.io do grupo e tratar o OPTIONS.
- Página: GitHub Pages, com HTTPS automático. `requestDevice` exige um toque do usuário e filtro `namePrefix = tag_id`.
- Riscos do Web Bluetooth, a verificar na S1:
  - muitos leitores de QR abrem o link numa WebView própria, sem Web Bluetooth; só o Chrome e o Samsung Internet funcionam. Na demo, oriente a abrir no Chrome;
  - o Android pede Bluetooth e localização ligados e mostra o seletor de dispositivos;
  - no iPhone, só pelo app Bluefy (gratuito).
- Pagamento: tela simulada. O Stripe em modo teste fica como bônus. Nada de dinheiro real.
- Modo offline de reserva: HMAC no navegador via SubtleCrypto, com a chave exposta no JS. Aceitável só como plano B para a demo.
- Rede da demo: hotspot de celular. Nunca eduroam ou portal cativo.

### 2.7 O papel do Arduino

- Uno R3 (assumido) ou Nano clássico: não têm BLE e trabalham com lógica de 5 V, então não podem ser a etiqueta. Servem para:
  1. bancada de ensaio: HX711, comando do N20 via DRV8833 e do SG90, torque travado, cronometragem do E03 e contagem de ciclos do E06;
  2. Liberador de Balcão simulado. Use SoftwareSerial (por exemplo, D10/D11) a 9600 bps, e deixe o Serial de hardware (D0/D1) livre para o log da bancada no USB. O TX de 5 V do Uno passa por um divisor (1 kΩ em série e dois de 1 kΩ em série para o GND, 5 x 2/3 = 3,33 V) antes do RX do ESP32-C3. O TX de 3,3 V do ESP32 é lido direto pelo Uno.
  - Alimente o motor e o servo por power bank, com GND comum ao Uno, e não pelo 5 V da placa.
- Se for Nano clássico: nada muda.
- Se for ESP32 DevKit: tem BLE e roda o mesmo código (NimBLE, mbedTLS). Comece o firmware BLE já na S1, antes de o C3 chegar. Mesmo assim, mantenha os 2 ESP32-C3: é o C3 que cabe no envelope. A bancada pode ficar no próprio DevKit (cuidado: lógica de 3,3 V; o HX711 aceita).
- Se for Nano 33 BLE: tem BLE (ArduinoBLE) e HMAC pela biblioteca Crypto do rweather. É 3,3 V e não tolera 5 V. Serve para começar a página Web Bluetooth já na S1, mas o firmware não é o mesmo da etiqueta.

---

## 3. Lista de compras

Legenda de prioridade: E = essencial, R = recomendado, O = opcional.

Regras:
- No máximo 3 pedidos com frete: Eletrogate, Smart Kits e ML. O AliExpress (recomendado) tem frete grátis.
- Calcule os fretes no carrinho ANTES de fechar o primeiro pedido.
- Meta: reserva de pelo menos R$ 40 depois dos fretes reais.

### 3.1 Pedido 1: Eletrogate (01/10)

Frete grátis em SP a partir de R$ 299. Preços abaixo no cartão; no Pix há ~5% de desconto. Com Pix, este carrinho cai para R$ 296,69, abaixo do mínimo. No carrinho, veja se o frete grátis continua. Se não continuar, pague no cartão ou boleto (R$ 312,30), ou acrescente a célula de carga de 20 kg (R$ 17,90, útil para o E02): 330,20 no cartão ou 313,69 no Pix.

| Item | Para que serve | Qtd | Unit. (R$) | Subtotal (R$) | Link | Prior. |
|---|---|---|---|---|---|---|
| ESP32-C3 Mini Tipo-C (SuperMini, BLE 5.0) | Cérebro da etiqueta, uma por unidade | 2 | 42,90 | 85,80 | https://www.eletrogate.com/esp32-c3-mini-tipo-c | E |
| Mini motor redutor N20 6 V 100:1 150 RPM | Atuador do R2, um por unidade | 2 | 34,90 | 69,80 | https://www.eletrogate.com/mini-motor-redutor-dc-6v-n20-1001-150rpm | E |
| Driver ponte H dupla DRV8833 | Liga, inverte e freia o N20 | 2 | 9,90 | 19,80 | https://www.eletrogate.com/driver-ponte-h-dupla-drv8833-2a | E |
| Micro servo SG90 | Referência na bancada e plano B do atuador | 1 | 14,90 | 14,90 | https://www.eletrogate.com/micro-servo-9g-sg90-towerpro | E |
| TP4056 USB-C com proteção | Carrega a LiPo (trocar o R3) | 2 | 4,90 | 9,80 | https://www.eletrogate.com/modulo-carregador-de-baterias-de-litio-tp4056-com-protecao-usb-c | E |
| Step-up MT3608 | 5 V para o SG90 se a margem for baixa (plano B do risco 1) | 1 | 6,90 | 6,90 | https://www.eletrogate.com/regulador-de-tensao-ajustavel-mt3608-auto-boost-step-up | E |
| LED RGB difuso 5 mm, cátodo comum | Sinal vermelho/verde | 4 | 0,80 | 3,20 | https://www.eletrogate.com/led-rgb-5mm-catodo-comum | E |
| Chave tátil 6x6x5 | Botão e fim de curso | 10 | 0,15 | 1,50 | https://www.eletrogate.com/push-button-chave-tactil-6x6x5mm | E |
| Mini chave deslizante SS12F46 (3 terminais) | Liga/desliga da bateria (a chave tátil é momentânea e não serve) | 3 | 0,50 | 1,50 | https://www.eletrogate.com/chave-ss12f46-3-terminais | E |
| Kit de componentes, 95 peças | Resistores 330 Ω, 1 kΩ, 10 kΩ, buzzer, capacitores, diodos, 30 jumpers M/M | 1 | 18,90 | 18,90 | https://www.eletrogate.com/kit-componentes-eletronicos | E |
| Jumpers M/F, 40 unidades de 20 cm | Ligações da bancada ao ESP32 e módulos | 1 | 8,90 | 8,90 | https://www.eletrogate.com/jumpers-macho-femea-40-unidades-de-20-cm | E |
| Protoboard 400 pontos | Montar e testar antes de soldar | 1 | 8,90 | 8,90 | https://www.eletrogate.com/protoboard-400-pontos | E |
| Placa ilhada 5x7 dupla face | Placa soldada da etiqueta | 2 | 4,90 | 9,80 | https://www.eletrogate.com/placas-pcb | E |
| Cabo JST PH 2 pinos | Conector da LiPo, para trocar a célula entre as unidades | 4 | 2,90 | 11,60 | https://www.eletrogate.com/cabo-com-conector-macho-femea-jst-2-pinos | E |
| Capacitor eletrolítico 1000 µF / 16 V | Anti-reset junto ao motor | 4 | 0,75 | 3,00 | https://www.eletrogate.com/capacitor-eletrolitico-1000uf-x-16v | E |
| Buzzer ativo 5 V (3,5 a 5 V) | Sinal sonoro (o kit traz só 1) | 2 | 2,50 | 5,00 | https://www.eletrogate.com/buzzer-ativo-5v | E |
| Diodo 1N5819, 10 unidades | OU de alimentação (bateria, contatos, USB) | 1 | 2,20 | 2,20 | https://www.eletrogate.com/diodo-1n5819-10-unidades | E |
| Transistor NPN BC337 | Aciona o buzzer | 4 | 0,45 | 1,80 | https://www.eletrogate.com/transistor-npn-bc337 | E |
| Resistor 47 Ω, 10 unidades | LED verde | 1 | 0,50 | 0,50 | https://www.eletrogate.com/resistor-47r-1-4w-10-unidades | E |
| Resistor 150 Ω, 10 unidades | LED vermelho | 1 | 0,70 | 0,70 | https://www.eletrogate.com/resistor-150r-1-4w-10-unidades | E |
| Módulo HX711 24 bits | Leitura da célula de carga | 1 | 8,90 | 8,90 | https://www.eletrogate.com/modulo-conversor-24bit-hx711-p-celula-de-carga | E |
| Célula de carga 5 kg | Mola, liberação, torque e força do atuador | 1 | 18,90 | 18,90 | https://www.eletrogate.com/peso-carga | E |
| Subtotal Eletrogate | | | | 312,30 | | |

A Eletrogate também cobre o HX711 e a célula de 5 kg (R$ 27,80), o que elimina a loja Casa da Robótica. Os jumpers M/M não entram porque o kit de 95 peças já traz 30.

### 3.2 Pedidos 2 e 3 e compra local

| Item | Para que serve | Qtd | Unit. (R$) | Subtotal (R$) | Link | Prior. |
|---|---|---|---|---|---|---|
| Pedido 2, Smart Kits (02/10): LiPo 3,7 V 400 mAh com PCM e NTC, 4 x 30 x 40,7 mm. O conector 51021-3P é trocado por JST | Energia da etiqueta 1 | 1 | 44,90 | 44,90 | https://www.smartkits.com.br/bateria-recarregavel-li-po-3-7v-400mah | E |
| Pedido 3, ML (02/10): mini tag rígida RF 8,2 MHz com pino, 100 unidades. SÓ se a Riachuelo não ceder etiquetas até 02/10 | Doadoras de garra, pinos, EAS e ensaios destrutivos | 1 | 143,74 | 143,74 | https://www.mercadolivre.com.br/etiqueta-antifurto-de-alarme-roupas-mini-tag-c-pino-100un/up/MLBU1164285336 | E (condicional) |
| Compra local (ferragem e papelaria): parafusos M3 x 10 com porcas (~16 de cada), cola CA, epóxi, lixa, termorretrátil, fita dupla face | Fechar a carcaça, fixar a garra metálica na sede, isolar e prender a LiPo | 1 | 25,00 (estimativa) | 25,00 | sem link (preço não levantado) | E |
| Total essencial | | | | 525,94 | | |

Frete: a Smart Kits cobra frete (R$ 20 a 35, estimativa; calcule no carrinho). O anúncio do ML provavelmente tem frete grátis por estar acima do mínimo, mas confira.

### 3.3 Recomendados (em ordem de prioridade)

| Item | Para que serve | Qtd | Unit. (R$) | Subtotal (R$) | Link | Prior. |
|---|---|---|---|---|---|---|
| N20 com redução 298:1, 6 V (AliExpress, frete grátis, chega ~11 a 26/10 se pedido em 02/10) | Seguro de torque: ~3x o 100:1, mesmo envelope | 1 | ~17,80 (R$ 14,24 + ~25% de ICMS; o preço varia com a versão, estimativa) | 17,80 | https://pt.aliexpress.com/item/1005004095310748.html | R1 |
| 2ª LiPo 400 mAh, no MESMO pedido da Smart Kits (sem frete extra) | Energia da etiqueta 2 (reserva da demo) | 1 | 44,90 | 44,90 | https://www.smartkits.com.br/bateria-recarregavel-li-po-3-7v-400mah | R2 |
| Total com recomendados | | | | 588,64 | | |

Sem a 2ª LiPo, a etiqueta 2 usa a célula da etiqueta 1 pelo conector JST, ou power bank. Sem o 298:1, a margem sai da geometria (pares B ou C da bancada). Alternativa nacional ao 298:1: N20 200:1 da Fermarc, 2 kgf.cm, R$ 42,50, em estoque, mas paga frete (grátis só acima de R$ 600): https://www.fermarc.com/produto/mini-motor-com-caixa-de-reducao-n20-6-v-com-100-rpm.html

### 3.4 Resumo do orçamento

| Cenário | Total (R$) | Reserva (R$) | Por aluno (R$) |
|---|---|---|---|
| Essencial, com as 100 etiquetas compradas | 525,94 | 74,06 (12,3%) | 87,66 |
| Essencial + recomendados, com etiquetas compradas | 588,64 | 11,36 (1,9%) | 98,11 |
| Essencial, etiquetas cedidas pela Riachuelo | 382,20 | 217,80 | 63,70 |
| Essencial + recomendados, etiquetas cedidas | 444,90 | 155,10 | 74,15 |

A reserva cobre, nesta ordem: frete da Smart Kits, frete do ML (se houver), paquímetro (se ninguém tiver) e ferramentas da seção 3.5.

Regra de compra dos recomendados: compre R1 e depois R2 só enquanto a reserva, depois dos fretes reais, continuar em R$ 40 ou mais. Se a Riachuelo ceder as etiquetas, compre os dois. Se o carrinho da Eletrogate mantiver o frete grátis com Pix, os R$ 15,61 de desconto pagam o R1.

### 3.5 Se faltar alguma ferramenta (módulos independentes)

Antes de comprar, peça emprestado no laboratório da Poli ou a colegas. Cada item abaixo só entra se faltar, e sai da reserva. Itens do ML abaixo do mínimo de frete grátis podem pagar frete.

| Item | Para que serve | Qtd | Unit. (R$) | Link | Prior. |
|---|---|---|---|---|---|
| PETG Masterprint 1,75 mm, 1 kg (ML) | Carcaças, garfo, came e sede | 1 | 68,16 | https://www.mercadolivre.com.br/filamento-masterprint-petg-3d-cor-preto-175mm-1kg-original/p/MLB24229494 | E se não houver nenhum |
| Kit ferro de solda 60 W com estanho, 127 V (ML) | Barra de pinos, JST, R3 do TP4056, placa ilhada | 1 | 35,89 | https://www.mercadolivre.com.br/kit-ferro-de-solda-60w-estanho-com-fluxo-de-solda-com-regulagem-de-temperatura-profissional-several-127-volts/p/MLB53197221 | E se não houver |
| Multímetro DT830B (ML, Full) | Tensões, corrente de carga e de sono (faixa de 200 µA) | 1 | 24,50 | https://www.mercadolivre.com.br/multimetro-digital-dt830b-amarelo-portatil-profissional-full/p/MLB22546763 | E se não houver |
| Paquímetro digital | Medir a garra na S2 e o E01 | 1 | 35 a 45 (estimativa, sem link) | a cotar | E se não houver |

Atenção: no pior caso (etiquetas compradas), o essencial mais o filamento dá R$ 594,10 e não fecha com os fretes. Se faltar filamento E a Riachuelo não ceder etiquetas, é preciso conseguir o filamento emprestado (laboratório ou colegas). Ferro, multímetro e paquímetro, isolados, cabem na reserva.

Por que não comprar 10 etiquetas no AliExpress: saem por R$ 102,28 com frete e impostos, mas chegam entre 16 e 27/10, depois da decisão do atuador (21/10). Toda a S2 e a S3 dependem da garra real. Uma alternativa a checar: lojas físicas na Santa Ifigênia ou na 25 de Março (mesmo dia, sem frete; preços não levantados).

### 3.6 Opcionais (só com sobra de reserva)

| Item | Para que serve | Preço (R$) | Link |
|---|---|---|---|
| Célula de carga 20 kg (Eletrogate) | E02 direto no HX711 (em vez do balde); também leva o carrinho da Eletrogate acima de R$ 299 no Pix | 17,90 | https://www.eletrogate.com/peso-carga |
| Adesivos NFC NTAG215, 10 unidades (ML) | NFC sob o QR | 20,10 | https://www.mercadolivre.com.br/kit-10-etiquetas-nfc-regravaveis-ntag215-1356mhz-compativel-celular-arduino/p/MLB61322148 |
| Insertos roscados M3 x 4, 50 unidades (ML) | Fechamento com mais ciclos de montagem | 39,27 | https://produto.mercadolivre.com.br/MLB-2610883919-inserto-metalico-de-rosca-m3-impressoes-3d-m3x4mm-50-pcs-_JM |
| Esferas de aço cromo de 4 a 10 mm, 10 de cada (ML) | Só se forem testar uma garra impressa em escala | 45,90 | https://produto.mercadolivre.com.br/MLB-3196556800-esferas-aco-cromo-4mm5mm6mm7mm8mm9mm10mm-10-de-cada-_JM |
| Destacador magnético (ML): NÃO cabe | Ensaio E11 | 140,86 | https://www.mercadolivre.com.br/removedor-magnetico-de-etiquetas-de-seguranca-antirroubo/p/MLB2001143427 |

Destacador: peça emprestado à Riachuelo, como já recomenda a SINTESE. A força de liberação e o curso podem ser medidos sem ele: basta serrar a tag e puxar o carretel com um gancho ligado ao HX711.

Alternativas se algum item estiver esgotado:
- ESP32-C3 na Fermarc por R$ 38,90: https://www.fermarc.com/placa-super-mini-esp32-c3-usb-c
- ESP32-C3 na Piscaled por R$ 27,40: https://www.piscaled.com.br/placa-super-mini-esp32-c3-wi-fi-e-ble
- Chave deslizante: mini chave gangorra KCD11 na Eletrogate (R$ 1,00), se a SS12F46 acabar.

### 3.7 A pedir emprestado ou já ter (sem preço levantado)

- Cabo USB-C DE DADOS (muitos cabos de celular só carregam): teste antes de gravar o ESP32.
- Morsa, arco de serra, alicate de corte, estilete e óculos de proteção.
- Power bank e cabos USB.
- Balança de cozinha e um balde (E02, se não comprarem a célula de 20 kg).
- Molas de caneta (testes de retorno e de mola da garra).

---

## 4. Plano semana a semana

As semanas vão de segunda a domingo; a S1 começa hoje (terça). Feriados: 12/10 (seg), 02/11 (seg) e 20/11 (sex).

| Semana | Entregas | Critério de pronto |
|---|---|---|
| S1: 29/09 a 04/10. Compra e preparação | Inventário de ferramentas e modelo do Arduino até 30/09. E-mail à Riachuelo até 30/09 (10 a 20 etiquetas usadas com pinos e empréstimo do destacador; resposta até 02/10). Pedido Eletrogate em 01/10; Smart Kits e ML em 02/10, fretes calculados antes. Exemplo Web BLE do Random Nerd Tutorials publicado no GitHub Pages e aberto em 3 celulares pelo leitor de QR nativo de cada um. Conta da Cloudflare com o e-mail do grupo. `Antifurto.py` atualizado: LiPo girada 90° ou deslocada para y ~ -17 (na posição atual ela invade a parede em ~0,75 mm), opção N20 + came + garfo, 3 contatos na face superior, alojamento de porca M3. Corpo de prova de tolerâncias impresso | Pedidos rastreáveis. Tabela de folgas reais medida. Tabela "qual app abre o link em WebView" nos 3 celulares |
| S2: 05 a 11/10. Estudo da etiqueta comercial e go/no-go do acionamento | Serrar 2 tags presas na morsa. GO/NO-GO: existe colar ou degrau acessível para um garfo por baixo do carretel? Se não, definir arruela colada ou haste de tração. Medir Ø e altura do copo, Ø das esferas, curso do carretel, força da mola com o HX711 (10 repetições) e força de extração do pino com o carretel erguido. Filmar 10 destravamentos em câmera lenta, se houver destacador. Imprimir a bancada v1. Começar o CAD paramétrico da etiqueta com as cotas [MEDIR] como parâmetros. Firmware: anúncio BLE, GATT (nonce, token, estado por notificação), LED testado à luz do dia, botão com wake. Testar BLE das 2 placas | Tabela "garra medida". Decisão do sentido de acionamento registrada. Celular Android conecta pela página e lê o nonce |
| S3: 12 a 18/10. Atuador na bancada | N20 100:1 nos pares A, B e C, e SG90, 10 repetições cada: força no carretel, tempo e corrente. Torque travado do N20 a 3,7 V e 3,4 V. Atrito PETG-aço pelo plano inclinado (μ = tan do ângulo de deslizamento, 10 repetições). Firmware: HMAC com mbedTLS, 120 s, uso único. Worker com CORS emitindo o token; fluxo QR -> conectar -> "Pagar" -> token -> escrita BLE. Frente de PRODUTO começa (pessoas 1 e 5): desenho de conjunto e vista explodida do produto de 150 mAh e placa única, processos (injeção de ABS/PC), BOM em escala, DFM | Planilha de margem por par. LED verde aceso a partir do celular, ponta a ponta |
| S4: 19 a 25/10. Decisão e integração na bancada | Decisão do atuador e do par até 21/10 (qua), com E04 >= 3 medido a 50% do travamento. Esquema elétrico completo (seção 2.5) desenhado antes da solda. CAD da etiqueta v1 atualizado com as cotas medidas; impressão da v1. Troca do R3 do TP4056 e solda na placa ilhada. ESP32-C3 aciona a garra real na bancada | Demo de bancada: celular paga -> verde -> botão -> pino sai, 10 em 10 vezes |
| S5: 26/10 a 01/11. Carcaça v1 e texto do R3 | Congelar a carcaça v1 em 28/10 (qua). Montar a v1 fechada. Usabilidade R03 a R05 começa (o fluxo pelo celular com LED já funciona desde a S3), com consentimento. Texto do R3: projeto detalhado do PRODUTO (formas, materiais, BOM detalhada, DFM, desenhos) mais resultados medidos no protótipo | Carcaça v1 fecha. R3 em revisão até 01/11 |
| S6: 02 a 08/11. R3 (04/11) e etiqueta v2 | Entregar o R3 em 04/11, sem nenhum parâmetro de força ou curso "estimado" que já tenha sido medido. Etiqueta v2 compacta: LiPo, TP4056, chave, fim de curso, OU de diodos. Firmware com todos os estados e timeout. Usabilidade com n >= 20 concluída até 08/11 | R3 entregue. Usabilidade tabulada |
| S7: 09 a 15/11. Ensaios da v2 | E01, E03, E09, S05 e S06. E02, E04 e E06. Página polida (erros, reconexão, modo offline). QR de 28 mm colado no rebaixo. Liberador de Balcão com o Uno, se estiver no prazo. Montar a 2ª etiqueta | Etiqueta fechada, sem USB, funciona 20 em 20 vezes |
| S8: 16 a 22/11. Congelamento e R4 | Congelar o hardware em 19/11 (qui). E05, E07/R06, E08, S09 e S10. 2ª etiqueta funcionando. Texto do R4 com desenhos finais, BOM final e resultados | Planilha de ensaios completa. 2 etiquetas funcionando |
| S9: 23 a 29/11. R4 (23/11) e prova (25/11) | Entregar o R4 na segunda. Semana leve. Vídeo de backup da demo (~2 min) | R4 entregue. Vídeo pronto. Daqui em diante, só correção de bug |
| S10: 30/11 a 06/12. Preparação da demo | Telas Figma (App Clip, Jornada Completa, Coletor, logística reversa). Modelo de aparência lixado e pintado. Roteiro. Ensaio geral em 03/12 (qui) com cronômetro, testando todos os planos B: hotspot, modo offline, 2ª etiqueta, power bank. Carregar as LiPo na véspera, com supervisão | Demonstração em 07/12 |

### Ensaios

| Espec. | Meta | Como medir | Semana |
|---|---|---|---|
| E01 | 98 x 82 x 26 ± 0,5 mm | Paquímetro, 3 medidas por eixo, nas 2 carcaças | S7 |
| E02 | Extração >= 120 N em TRAVADA | Pendurar pelo pino, atravessando um tecido, um balde com água pesado na balança (12,3 kg ~ 120 N), ou célula de 20 kg no HX711 se comprada. Subir a carga aos poucos e manter 10 s. Na unidade 2 ou num corpo de prova, não na unidade da demo | S7 |
| E03 | Liberação <= 3 s | `millis()` do 2º aperto até o fim de curso, 20 repetições, mais cronômetro | S7 |
| E04 | Margem >= 3 | Força do atuador no carretel ÷ força de liberação, ambas no HX711, a 50% do travamento e com a LiPo a 3,4 V | S3 e S7 |
| E05 | >= 168 dias | Corrente de sono e de anúncio com o multímetro em série (faixa de 200 µA). O DT830B tem shunt de ~1 kΩ nessa faixa: ponha um jumper ou chave em paralelo com o multímetro, fechado ao acordar e aberto só durante o sono, senão o ESP32 reinicia. Declarar que a placa SuperMini (LED e LDO, ~100 a 600 µA) não representa o consumo do produto | S8 |
| E06 | >= 200 liberações por carga | Modo ciclo no firmware (trava e destrava automaticamente) com a LiPo cheia; registrar falhas e a tensão mínima | S7 |
| E07 / R06 | 0 aceitações indevidas em >= 200 tentativas | Replay de token antigo, token forjado, token de outra tag_id, token com mais de 120 s e nonce já usado, pela página ou por script | S8 |
| E08 | 4 padrões de luz e som | 5 pessoas identificam os padrões, também com simulação de daltonismo, em sala iluminada | S8 |
| E09 | QR lido em <= 2 s a 10 a 25 cm em >= 95% das tentativas | 3 celulares, 20 leituras cada. NFC a <= 2 cm, se comprado | S7 |
| E11 | 0 aberturas em 20 tentativas | Só com destacador emprestado. Resultado esperado: reprova com a garra canibalizada, o que justifica o carretel não ferromagnético | Opcional |
| R03 / R05 | Mediana <= 45 s e p80 <= 60 s; >= 85% na 1ª tentativa | Usabilidade com n >= 20, cronometrada do "Pagar" à confirmação | S5 e S6 |
| S05 / S06 | Página <= 3 s em 4G; token <= 2 s após o pagamento | DevTools com 4G simulado; timestamps na página e no Worker | S7 |
| S09 / S10 | Liberador <= 60 s; 100% dos eventos registrados | Cronômetro; log do Worker | S8 |

Ficam fora da bancada: E10, E12, S01 a S03, S07, S08, R01 e R02. Explicar no R4 por quê.

---

## 5. Divisão do trabalho

| Pessoa | Frente | Entregas |
|---|---|---|
| 1 | Mecânica, CAD e impressão | `Antifurto.py` no padrão do R2; corpo de prova; bancada e pares (excêntrico, rampa); garfo; carcaça v1 a v3; modelo de aparência; desenhos do produto para o R3 e o R4 (com a pessoa 5) |
| 2 | Eletrônica | Compras e planilha de orçamento; esquema elétrico; soldas; troca do R3 do TP4056; OU de diodos; hardware do Liberador; regras de segurança da LiPo |
| 3 | Firmware | ESP32-C3 (BLE, estados, HMAC, motor com fim de curso, nSLEEP, sono); firmware do Uno (HX711, torque, ciclos, SoftwareSerial do Liberador) |
| 4 | Web e app | Teste Web BLE na S1; página no GitHub Pages; Worker com CORS e secret; QR; modo offline; teste no iPhone com Bluefy; telas Figma |
| 5 | Ensaios e produto | Estudo da etiqueta comercial (com a pessoa 1); planilha E/R/S; usabilidade n >= 20; frente de produto (processos, BOM em escala, DFM); integração do texto do R3 e do R4 |
| 6 | Apresentação e contato | Contato com a Riachuelo (etiquetas e destacador) e guarda do destacador; conta da Cloudflare do grupo; dono do cronograma; roteiro; vídeo de backup; fluxo de Coletor e logística; ensaio geral |

Todos participam dos ensaios da S3 e da S7.

---

## 6. Impressão e CAD

### CAD

- Partir do `fusion/Antifurto.py`, que é o arquivo mais próximo do R2. O CAD preferencial da disciplina é o Inventor; o Fusion não é proibido (confirmar com o professor).
- Pontos a atualizar:
  - Mecanismo: criar a opção "micromotor + came + garfo". O garfo entra sob o colar do carretel e o levanta; o came fica preso numa fenda do garfo, o que dá retorno positivo.
  - Força do MG90S: corrigir `MEC['came']['forca']` para ~9 N e incluir o atrito da face de trás, F_v = F_h / (tan(α + φ) + μ).
  - Componentes: LiPo de 400 mAh (4 x 30 x 40,7 mm), girada 90° ou em y ~ -17, com >= 1 mm de folga lateral e verificação de colisão; TP4056 de 26 x 17 x 5 mm; SG90 de 22,2 x 11,8 x 31 mm como alternativa.
  - Contatos: 3 pads de Ø4 mm na face superior, em vez de 2 embaixo. No protótipo, os pads podem ser cabeças de parafuso M3 com molas de caneta na base do Liberador; se não der tempo, declarar que o Liberador usa cabo.
  - Garra: trocar os valores [MEDIR] (Ø12,4 x 10 mm, curso de 1,2 mm, mola de 2,5 N) pelos medidos na S2.
  - Fechamento: o CAD prevê insertos M2, que não estão na lista. Troque por parafusos M3 x 10 com alojamento de porca sextavada na carcaça inferior (dispensa inserto e ferro). Valide a folga do alojamento no corpo de prova. Evite snap-fit, que quebra no reuso.
- A LiPo vai num berço com ~1 mm de folga lateral e folga na espessura para inchaço (estimativa), longe do came, do pino e de arestas.

### Material

- PETG na carcaça, no garfo, no came e na sede da garra: menos fluência sob carga que o PLA.
- PLA só na bancada.
- Não imprima o cone nem o contato das esferas: use o copo, as esferas e o carretel metálicos da tag, fixados na sede com epóxi se preciso.

### Tolerâncias

- Furos saem de 0,1 a 0,3 mm menores.
- Folga deslizante de 0,2 a 0,3 mm por lado, mais 0,05 mm no PETG.
- Interferência de 0,05 a 0,15 mm.
- O CAD usa 0,6 mm de folga geral: calibre pelo corpo de prova (furos de Ø2 a Ø12,5, pinos e alojamento de porca M3) antes da carcaça.

### Parâmetros do fatiador

| Peças | Camada | Paredes | Preenchimento |
|---|---|---|---|
| Carcaça | 0,2 mm | 3 a 4 (estimativa) | 20 a 30% |
| Garfo, came, bucha e sede da garra | 0,12 mm | 4 a 5 | 100% |

- Bico de 0,4 mm.
- PETG (referência GTMax): bico entre 225 e 270 °C, mesa entre 80 e 95 °C.
- Ligar compensação de pé de elefante (~0,2 mm), furos como polígono e compensação XY.

### Orientação

- Carcaças com a face externa na mesa: face plana para o QR, torres para cima.
- Garfo e cursor deitados, com a rampa para cima.
- Peças cilíndricas com o eixo em Z.

### Plano B de impressora

A Metamáquina do Departamento de Engenharia de Produção. O guia rápido está na pasta de ferramentas da disciplina.

---

## 7. Riscos técnicos e plano B

| Risco | Sinal | Plano B |
|---|---|---|
| 1. Atuador fraco (margem < 3) | Bancada da S3 | Excêntrico menor com rampa mais íngreme (par B) ou came direto (par C); N20 298:1 (R1) ou 200:1 da Fermarc; SG90 a 5 V pelo MT3608. NUNCA "rampa mais suave". Decisão até 21/10 |
| 2. Sentido de acionamento errado (o cursor empurra o carretel e trava) | Go/no-go da S2 | Garfo sob colar; arruela de latão ou alumínio colada com epóxi; haste de tração pela mola |
| 3. Esfera travando ou marcando o plástico, ou fluência do PETG | Pino não solta ou solta sozinho | Conjunto copo, esferas e carretel 100% metálico da tag, só a sede impressa. Corpo de prova com 3 folgas. Não deixar a etiqueta travada sob carga por dias |
| 4. BLE fraco ou lote ruim da SuperMini | Conexão cai a menos de 1 m | Testar as 2 placas na S2. Antena longe da LiPo e do motor. Plano B: ESP32 DevKit ou Nano 33 BLE fora da caixa, ligado por cabo |
| 5. Celular sem Web Bluetooth (iPhone, ou link aberto em WebView) | Página não mostra o seletor | Abrir no Chrome; Bluefy no iPhone; demo principal em Android; App Clip em Figma; Liberador de Balcão via UART |
| 6. Bateria: pico do motor (até 0,67 A travado) e reset | ESP32 reinicia ao acionar | LiPo de 400 mAh com PCM (a de 150 mAh não aguenta, por isso fica só no desenho); capacitor de 1000 µF; fim de curso; na demo, power bank |
| 7. TP4056 carrega a 1 A, alto para 400 mAh | | Retirar o R3 SMD e pôr 10 kΩ antes da primeira carga; primeira carga com multímetro em série |
| 8. LED verde fraco | Não se vê na sala | Resistor de 47 Ω; se ainda fraco, acionar por transistor a partir da LiPo |
| 9. Sem internet na sala | Worker inacessível | Hotspot; modo offline com HMAC no navegador |
| 10. Etiquetas ou peças atrasadas ou esgotadas | Rastreio | Etiquetas usadas da Riachuelo; Fermarc, Piscaled, Santa Ifigênia ou ML como alternativa |
| 11. Orçamento estoura com os fretes | Carrinho | Não comprar os recomendados; emprestar ferramentas; cortar o MT3608 só se o carrinho da Eletrogate continuar acima de R$ 299 |
| 12. Prazo | Checkpoints de 21/10, 28/10 e 19/11 não cumpridos | Cortar primeiro o Liberador e o NFC; nunca cortar o núcleo (reter, autorizar, sinalizar, liberar) |

---

## 8. Segurança e ética

### LiPo

- Só com proteção (PCM) e só com carregador CC/CV (TP4056).
- Carregar fora da caixa fechada, sobre superfície não inflamável e sempre sob supervisão.
- Carregar só entre 0 e 45 °C.
- Nunca furar, dobrar ou esmagar.
- Célula inchada sai de uso na hora e vai para um recipiente não inflamável.
- Chave liga/desliga obrigatória. Desligar a chave ao gravar pelo USB.
- Na apresentação: célula já carregada ou power bank.

### Solda e oficina

- Suporte para o ferro, ventilação e mãos lavadas depois.
- Nunca deixar o ferro ligado sem ninguém por perto.
- Óculos ao cortar terminais e ao serrar etiquetas: a mola pode saltar.
- Tag presa na morsa, nunca na mão.

### Ética

- O protótipo e o destacador são instrumentos de estudo de engenharia, não ferramentas para abrir etiquetas de lojas.
- Usar só as etiquetas compradas pelo grupo ou cedidas pela Riachuelo.
- O destacador emprestado fica sob a guarda da pessoa 6 e é devolvido.
- Não publicar o passo a passo de como vencer etiquetas comerciais. O resultado do E11 aparece no relatório como justificativa de projeto.

### Pagamentos e dados

- Pagamento só simulado ou em sandbox; nenhum dado real de cartão.
- Usabilidade com consentimento e dados anonimizados.
- Secret do Worker fora do repositório.
- As patentes US 11.417.186 e US 11.984.003 (Kohl's) e US 11.183.038 (Sensormatic) estão vigentes: citar no R3 e não copiar soluções delas.

---

## 9. Esta semana

### Os 5 primeiros passos

1. Até 30/09 (qua): inventário. Modelo do Arduino; quem tem filamento (e quanto), ferro de solda, multímetro com faixa de µA, paquímetro, morsa e cabo USB-C de dados; o que dá para pegar emprestado no laboratório da Poli.
2. Até 30/09 (qua): e-mail à Riachuelo pedindo 10 a 20 etiquetas rígidas usadas com pinos e o empréstimo do destacador, com resposta até 02/10.
3. 01/10 (qui): pedido da Eletrogate (R$ 312,30), conferindo no carrinho se o frete grátis continua com Pix; calcular também o frete da Smart Kits antes de pagar.
4. 02/10 (sex): pedido da Smart Kits (1 LiPo, ou 2 se a reserva permitir) e, se a Riachuelo não confirmar, das 100 etiquetas no ML. N20 298:1 no AliExpress se a reserva continuar >= R$ 40.
5. Até 04/10 (dom): exemplo Web BLE do Random Nerd Tutorials no GitHub Pages testado em 3 celulares pelo leitor de QR nativo; conta da Cloudflare do grupo criada; corpo de prova de tolerâncias impresso; `Antifurto.py` com a LiPo reposicionada.

### As 3 decisões da equipe

1. De onde vêm as etiquetas (até 02/10): cedidas pela Riachuelo ou as 100 do ML (R$ 143,74). Isso define se os recomendados entram.
2. O que comprar e o que emprestar (até 30/09): filamento, ferro, multímetro e paquímetro, e como ratear o dinheiro (~R$ 88 por aluno no essencial). Sem filamento e sem etiquetas da Riachuelo, o orçamento não fecha.
3. Mecanismo e atuador (sentido de acionamento na S2; atuador até 21/10): garfo sob colar, arruela colada ou haste de tração; e par B, par C, N20 298:1 ou SG90, conforme a margem medida.

### Ainda a confirmar

- Mapa de RTC IO e de strapping do ESP32-C3 no datasheet, antes de fixar os pinos.
- Se a barra de pinos do SuperMini vem soldada.
- Se o módulo DRV8833 da Eletrogate expõe o nSLEEP.
- Se o cabo JST da Eletrogate vem em par (macho e fêmea) ou é um só.
- Fretes reais no carrinho.
- Se o torque de 0,8 kgf.cm do N20 100:1 é nominal ou travado (medir na S3).

---

Fontes do acervo: `fusion/Antifurto.py`; `r2/3-contexto.tex`, `6-escala-valor.tex`, `8-concepcao.tex`, `9-desenhos.tex` e `11-consideracoes.tex`; `pesquisa/SINTESE-decisao-de-projeto.md`; `viabilidade-e-bom.md`. Preços: páginas das lojas citadas nas tabelas, consultadas em 29/09/2026. Dados de atuadores: Pololu (N20 298:1), ProtoSupplies e Handsontec (SG90), Adafruit (solenoide e LiPo), patente US 11.859.412 (All-Tag). ESP32-C3 SuperMini: Random Nerd Tutorials e sigmdel.ca.
