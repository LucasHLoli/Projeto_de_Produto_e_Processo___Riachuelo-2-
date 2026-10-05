# DECISÃO DE PROJETO — ESTAÇÃO DE LIBERAÇÃO
### Consolidação das 6 frentes, já com as correções dos céticos aplicadas

---

## 1. ARQUITETURA DECIDIDA

### 1.1 Trava e destravamento

**Escolhido:** desacoplador magnético **comercial pronto** (10.000 GS), montado **fixo** dentro da estação, com o **movimento relativo feito pela PEÇA, não pelo ímã** — um berço deslocado por **came/excêntrico acionado por servo MG995**, com retorno assistido por mola.

Por quê: o único subsistema que o grupo não consegue projetar em um semestre é o **circuito magnético** do destravador — o achado do cético é que "12.000 GS" de catálogo não é campo útil na superfície de trabalho, e que um eletroímã de hobby de 3 W (P20/15, 25 N a entreferro zero) não reproduz esse circuito através da carcaça de ABS. **Opção (b) eletroímã e opção (c) solenoide empurrando a gaiola estão formalmente REPROVADAS** — a segunda por motivo geométrico, não de força: a gaiola é selada dentro do ABS e não há caminho para o êmbolo.

A mudança em relação à pesquisa original: **não compramos o atuador linear de R$326,49**. O segundo maior risco declarado era vencer a atração magnética no recuo, e o atuador foi dimensionado "por margem, não por dado" (a própria página declara 36 g de peso para 100 N, número implausível, e não especifica corrente). O cético apontou os três contornos clássicos que a pesquisa não considerou: **(a) mover a tag em vez do ímã, (b) came/excêntrico que dá vantagem mecânica crescente exatamente no início do recuo, onde a atração é máxima, (c) shunt de aço deslizante que curto-circuita o campo em vez de afastar o ímã.** Adotamos (a)+(b) como base e mantemos (c) como plano de contingência barato (uma placa de aço-carbono de 3 mm).

Sobre o passo 8 do briefing: mantemos os **três movimentos** da patente da Kohl's (US11417186B2 / US11984003B2, vigentes) como hipótese de projeto — (1) ímã libera a embreagem, (2) algo extrai o pino, (3) algo empurra o corpo da tag para fora do ímã. **Mas registramos a contra-evidência**: a descrição comercial da Canal Automação afirma que o desacoplador "extrai o pino" das mini tags. Em mini tag o pino é de aço e o ímã o atrai — a extração pode ser parcial ou totalmente magnética. **Isso se resolve no primeiro teste de bancada, não por leitura de patente.** Orçamos o servo ejetor (MG90S, R$23,90) porque é barato; se o teste mostrar que o pino sai sozinho, é economia, não retrabalho.

Referência de projeto em **domínio público**: US 7.450.013 B2 (Checkpoint, expirada em 15/05/2025, prioridade 20/02/2004) descreve exatamente ímã permanente movido por motor sob o balcão, liberado após o POS autorizar. Ela entrega de graça três decisões: **ímã propositalmente pesado** (para que ímãs de bolso não abram a tag), **velocidade de aproximação calibrada** (para não apagar tarja de cartão do cliente) e **posição padrão sem energia que permite destravamento manual de emergência**. Adotamos as três.

**Risco número 1 que pode matar tudo:** se a Riachuelo usar trava **Multipolar** (exige ímã bipolar proprietário) ou trava **mecânica** (SuperTag/VST, Gator, Alpha S3 — só abrem com gancho/chave), nenhum ímã genérico abre e o projeto pivota. Ressalva honesta do cético: a taxonomia "4 níveis" é nomenclatura comercial de um fornecedor australiano, não padrão de indústria, e **não há evidência de Multipolar no parque brasileiro**. Isso se responde em 10 minutos numa loja.

### 1.2 Eletrônica de controle

**Escolhido:** **ESP32 DevKit 30 pinos** (R$44,85, Eletrogate E28-001, confirmado e em estoque), **duas unidades**.

Por quê: metade do preço do Pico W (R$83,60, confirmado), Pi Zero 2W esgotado na RoboCore sem previsão (resposta de ago/2026, confirmada), e volume incomparável de tutorial em português. **Correção do cético:** o argumento de que o Pi Zero 2W "não tem PWM em hardware confiável" é **falso** — ele tem dois canais em GPIO12/13/18/19. A decisão de descartá-lo continua certa, mas pelos outros dois motivos.

Arquitetura elétrica: **uma fonte 12V/5A bivolt → três domínios.** 12V direto para a fechadura solenoide e para o LED do botão arcade (que é **12V, não 5V** — confirmado na Casa da Robótica); um LM2596 ajustado para 5,5–6,0V dedicado aos servos; um LM2596 ajustado para 5,0V entrando no VIN do ESP32. **Nunca alimentar servo pelo pino 5V da DevKit.** O número "AMS1117 satura em 600 mA" é folclore de comunidade (a fonte citada diz 1 A e contém erro grosseiro), mas a conclusão prática vale por trilha fina, dissipação e queda de tensão.

Armadilhas confirmadas e incorporadas ao pinout: **módulo MOSFET IRF520 não funciona com 3,3V** — o próprio suporte da RoboCore responde na página "esse módulo não é compatível com 3,3 V, ele só pode ser controlado por níveis lógicos de 5 V". Usamos **IRLZ44N avulso** (R$5,90 na SmartKits, achado do cético, mais barato que a faixa estimada). **GPIO 6–11 são a flash SPI.** **GPIO 0, 2, 5, 12, 15 são strapping — o botão arcade nunca vai neles** (GPIO12 em nível alto no boot configura a flash para 1,8V e pode danificá-la). **GPIO 34–39 não têm pull-up interno** — o botão exige 10k externo. **ADC2 morre com o WiFi ligado.** **Anti-brownout obrigatório**: 1000 µF + 100 nF colados nos pinos de alimentação; nunca desabilitar o detector por software.

Correções de preço aplicadas: protoboard é **R$11,90**, não R$12,90.

### 1.3 Identificação da peça

Esta é a decisão que mais mudou em relação às pesquisas originais, porque **a lacuna mais grave de todo o conjunto foi apontada por dois céticos independentes**: uma hard tag EAS RF 8,2 MHz é um **circuito LC ressonante de 1 bit**. Todas as etiquetas da loja são eletricamente idênticas e **não carregam número de série**. O passo 4 do briefing ("a Estação LÊ a etiqueta e pergunta se AQUELA peça está paga") **é fisicamente impossível** com a etiqueta burra sozinha.

**Escolhido — arquitetura de dois caminhos com pareamento:**

- **Cliente → QR Code impresso no hangtag de papel.** Nível de correção H, **mínimo 2,5 × 2,5 cm** (correção do cético: a própria fonte Scanova diz 1 polegada, não 2 cm; e o módulo mínimo da ISO 18004 é 0,25 mm, não 0,4 mm), URL curta, zona de silêncio de 4 módulos. Motivo duro: o Brasil é 75,45% Android (StatCounter, ago/2026) e a faixa de entrada — que é o cliente da Riachuelo — frequentemente **não tem antena NFC**. QR é a única tecnologia com cobertura de 100% da base instalada. **Custo incremental: R$0,00.**
- **Estação → adesivo NTAG213 colado na HARD TAG REUTILIZÁVEL**, lido pelo RC522 via UID de 7 bytes de fábrica.

Por que na hard tag e não no hangtag: o cético matou a combinação que a pesquisa original recomendava. Ela rejeitou a etiqueta UHF on-metal a R$6-7,50/un com o argumento correto de que custa mais que a hard tag — e depois recomendou NTAG213 a R$2,03/un **consumível por peça vendida**, enquanto a hard tag é reutilizável dezenas de vezes. Por peça vendida, era a combinação mais cara disponível. **Colado na hard tag, o adesivo é amortizado pelo mesmo número de ciclos da própria etiqueta.**

O pareamento (hard tag UID ↔ peça) é feito no momento em que a loja prende a etiqueta. Isso também **fecha o vetor de fraude (d) "pagar barato e liberar caro"**: a Estação não pergunta "esta etiqueta está paga?", ela pergunta "a peça pareada a esta hard tag está paga?". Se o cliente trocar hangtags, o pareamento continua sabendo qual peça é aquela.

**Riscos assumidos e declarados:**
- **Detuning por metal.** O pino de aço, as esferas e o plunger ferromagnético estão a milímetros do adesivo. Mitigação: adesivo anti-metal com ferrite, posicionado no lado plástico mais distante da embreagem. **Isso é teste de semana 1, não premissa.** O número "30 mm com ferrite, 61 mm após casamento" do estudo citado **não é transferível** — a linha de base daquele setup era 78 mm, e a nossa é 10–20 mm. Citar só o mecanismo.
- **UID clonável.** O cético derrubou a afirmação "usar o UID elimina o risco de alguém regravar a tag": existem **magic NTAG213 com UID regravável** vendidos abertamente (KSEC Gen2/Gen3, Lab401), alguns clonáveis pelo próprio celular. Mitigação em duas camadas: (i) o backend só aceita um UID que esteja **pareado a uma peça paga naquele instante**, com autorização de **uso único e TTL curto** — um clone só serve para abrir a peça que já foi paga; (ii) na versão de produção, validar a **ECC originality signature** do NTAG213, que está no mesmo datasheet e a pesquisa original nunca mencionou.
- **RC522 vs PN532.** Correção do cético: **o datasheet do MFRC522 declara os mesmos 50 mm nominais** do PN532, e o CI suporta SPI, I²C **e** UART (a limitação a SPI é do estrapamento da placa breakout). A comparação "2 cm vs 5 cm" era peras com bananas. O que manda no alcance é a antena da tag (23 mm reais no adesivo de 25 mm) e a sintonia da placa. Por isso compramos **3 RC522** de fornecedores diferentes e comparamos em bancada (custo total R$44,70), em vez de apostar o semestre numa placa de R$15 que pode ter capacitor errado ou CI falsificado.

**UHF 915 MHz fica FORA do escopo.** O módulo mais concreto (M5Stack JRD-4035) custa US$79, dá ~1 m real e não é vendido em loja brasileira. Documentamos a faixa legal (**902–907,5 e 915–928 MHz** — o Brasil **não** tem 902–928 contínuo, Ato ANATEL 14448/2017) e o alerta de nunca comprar módulo europeu de 868 MHz. Isso demonstra domínio técnico sem gastar orçamento.

### 1.4 Pagamento e SaaS

**Escolhido:** **Pagar.me sandbox** (gateway) + **Supabase Free** (Postgres + Edge Function + Realtime) + backend próprio como fonte de verdade.

Mudança em relação à pesquisa original, por refutação direta: a pesquisa colocou o Pagar.me em terceiro lugar com a frase "não ganha de Asaas/Efi" — escrita sobre uma página que o pesquisador **declarou não ter conseguido abrir**. O cético abriu: o **simulador de Pix do Pagar.me auto-confirma transações de até R$500,00** (`pending → paid` em segundos, sem intervenção), entregando o mesmo ciclo completo da Efi **sem certificado mTLS .p12, sem conta em banco e sem chamada de confirmação**. Única restrição documentada: não funciona junto com o produto Split.

Backup: **Asaas sandbox**, que ganhou um endpoint dedicado descoberto pelo cético — `POST /v3/sandbox/payment/{id}/confirm` — automatizável, sem clicar no painel.

**Mercado Pago está descartado para a demo.** A doc oficial é explícita: com credenciais de teste "só será possível verificar o funcionamento da sua integração por meio de uma requisição, e não simulando uma compra". O QR nunca vira `approved`, o webhook nunca dispara, o LED verde nunca acende.

**Decisão de arquitetura que domina a experiência do usuário:** a Estação **não pergunta "está pago?" no momento do botão**. O handshake TLS no ESP32 custa **2 a 6 segundos** (relatos de ~2,2 s a ~6,2 s medidos em issue da Espressif — o cético corrigiu a faixa para cima, o que **reforça** o argumento). Portanto: assim que o webhook confirma, o backend **empurra** por Realtime "tag X autorizada até T+120 s"; a Estação cacheia; o aperto do botão decide **offline e instantaneamente**. Isso tira a rede do caminho crítico e torna a queda de WiFi entre pagar e apertar não-fatal.

**Segurança:** o celular do cliente **só paga**. Ele nunca carrega, exibe ou repassa o token de liberação — nem por QR, nem por BLE, nem por NFC. No modelo de ameaça, o dono do celular **é** o adversário. Desafio-resposta com **nonce gerado pela Estação** + HMAC-SHA256 com segredo K na NVS; o nonce vale mais que o timestamp porque o timestamp depende de NTP e NTP depende de internet. Mantemos o HMAC de aplicação **mesmo com HTTPS**, porque na prática o grupo vai acabar em `setInsecure()` sob pressão de prazo, e aí só o HMAC impede que alguém na rede forje "está pago".

**Rede:** hotspot de celular como SSID primário. Nunca planejar a demo em cima do eduroam (WPA2-Enterprise, histórico de issues no arduino-esp32) nem de rede com portal cativo, que é **impossível** para um ESP32 sem navegador.

**LGPD:** base legal é **execução de contrato (art. 7º, V)**, não consentimento — não porque a revogação "derrubaria o direito de destravar" (argumento fraco, corrigido pelo cético), mas porque quando o tratamento é **necessário** para executar o contrato, consentimento é base inadequada por construção e cria um direito de revogação que não deveria existir sobre o núcleo do serviço. A Estação responde **um booleano sobre um ID de peça**, sem CPF, sem log local de dado pessoal (art. 6º, III — **necessidade**, que é o termo brasileiro; "minimização" é vocabulário do GDPR). Riachuelo é controladora, o SaaS é operador (art. 39). **Falta no escopo e precisa entrar: transferência internacional (Cap. V, arts. 33–36) se o SaaS estiver hospedado fora, encarregado (art. 41) e comunicação de incidente (art. 48).**

### 1.5 Interface

**Escolhido:** **display OLED 0.96" I²C SSD1306** (R$26,90, confirmado, opera 2,2–5,5V, dispensa level shifter) + **botão arcade iluminado de 60 mm** (R$19,99, confirmado, LED 12V, microswitch KW1-103) + **3 LEDs discretos de 5 mm** (verde/amarelo/vermelho, ~R$3 total) + **buzzer ativo** (R$4,50, confirmado).

O anel WS2812 está **fora**: esgotado, sem preço na página, exige 5V, puxa 480 mA em branco pleno, e o requisito do sistema é "LED verde acende", não animação colorida.

O buzzer não é enfeite: **NBR 9050:2020, item 9.4.3.8** exige instruções e informações **visuais E auditivas OU táteis** em máquinas de autoatendimento. **LED verde sozinho não cumpre a norma** — essa é uma exigência que nenhuma das seis pesquisas tinha, e foi extraída pelo cético do mesmo PDF que a pesquisa original alegou não conseguir ler.

Cotas obrigatórias, agora com números (NBR 9050:2020, 9.4.3):
- **9.4.3.5** — controles entre **0,80 m e 1,20 m** do piso, profundidade máx. **0,30 m** da face frontal
- **9.4.3.6** — dispositivos de inserção/retirada entre **0,40 m e 1,20 m**, cor contrastante
- **9.4.3.4** — Módulo de Referência para aproximação frontal
- **9.4.3.3** — proteção contra luz ambiente e solar (isso conversa direto com o falso positivo do sensor óptico e com a leitura do QR)
- **9.4.3.1** — ao menos uma máquina acessível por tipo de serviço, em rota acessível

Base legal adicional que faltava: **Lei 13.146/2015 (LBI), art. 63** dá força de lei à acessibilidade em autoatendimento — não é só norma técnica.

---

## 2. LISTA DE COMPRAS FINAL

Todos os preços "CONFIRMADO" foram lidos em página de produto por um dos verificadores. Todo preço vindo de snippet de busca ou de página que retornou 403/404 está marcado **ESTIMADO**, sem exceção — foi exatamente aí que a verificação derrubou mais coisa (três URLs mortas, duas páginas vivas sem preço, uma esgotada).

### Bloco A — Núcleo eletrônico (obrigatório)

| # | Item | Termo de busca (Mercado Livre) | Qtd | Unit. | Total | Status | Para que serve |
|---|---|---|---|---|---|---|---|
| 1 | ESP32 DevKit 30 pinos | `esp32 wroom 30 pinos devkit wifi bluetooth` | 2 | R$ 44,85 | R$ 89,70 | **CONFIRMADO** (Eletrogate E28-001) | Cérebro + sobressalente. Segunda placa cobre queimar uma na semana da entrega |
| 2 | Kit RFID RC522 13,56 MHz | `kit modulo rfid rc522 13.56mhz` | 3 | R$ 14,90 | R$ 44,70 | **CONFIRMADO** (Curto Circuito) | Leitor de UID. Três unidades de fornecedores diferentes por causa de placas mal sintonizadas e CIs falsificados |
| 3 | Adesivo NFC NTAG213 25 mm | `tag nfc ntag213 adesivo 25mm` | 20 | R$ 2,03 | R$ 40,60 | **CONFIRMADO** (SmartKits) | Serial da hard tag. Antena real = 23 mm |
| 4 | Módulo PN532 (contingência) | `modulo rfid nfc pn532 13.56mhz` | 1 | R$ 38,46 | R$ 38,46 | **CONFIRMADO** (WJ Componentes, 43×40 mm / 5V) | Só se o RC522 não der alcance. Note: **é a variante pequena**, não a de 78×50 mm |
| 5 | Display OLED 0.96" I²C SSD1306 | `display oled 0.96 128x64 i2c ssd1306` | 1 | R$ 26,90 | R$ 26,90 | **CONFIRMADO** (Eletrogate H2-009) | Mensagens ao cliente |
| 6 | Botão arcade iluminado 60 mm | `botao arcade fliperama iluminado 60mm` | 1 | R$ 19,99 | R$ 19,99 | **CONFIRMADO** (Casa da Robótica) | Passo 6. LED 12V, furo de painel 24–28 mm |
| 7 | Módulo buzzer ativo 5V | `modulo buzzer ativo 5v arduino` | 1 | R$ 4,50 | R$ 4,50 | **CONFIRMADO** (Eletrogate) | Sinalização auditiva — **requisito NBR 9050 9.4.3.8** |
| 8 | Fonte chaveada 12V 5A bivolt | `fonte chaveada 12v 5a bivolt 60w` | 1 | R$ 54,90 | R$ 54,90 | **CONFIRMADO** (Benluz; Curto Circuito R$41,60 **esgotado**) | Alimentação única. Verificar selo Inmetro |
| 9 | Step-down LM2596 ajustável | `modulo regulador step down lm2596 ajustavel` | 2 | R$ 8,90 | R$ 17,80 | **CONFIRMADO** (Eletrogate) | Um rail 5,0V p/ ESP32, um rail 5,5–6,0V p/ servos |
| 10 | Servo MG995 metal 180° | `servo motor mg995 metal 180 graus` | 2 | R$ 42,60 | R$ 85,20 | **CONFIRMADO** (Curto Circuito) | Came do berço + sobressalente. **MG996R está esgotado nas duas lojas** |
| 11 | Servo MG90S metal | `servo motor mg90s micro metal` | 2 | R$ 23,90 | R$ 47,80 | **CONFIRMADO** (Curto Circuito) | Ejetor da tag + portinhola. **Nunca SG90 sob carga** |
| 12 | MOSFET IRLZ44N logic-level | `mosfet irlz44n canal n to-220` | 3 | R$ 5,90 | R$ 17,70 | **CONFIRMADO** (SmartKits) | Driver do solenoide e do LED 12V. **Nunca IRF520** |
| 13 | Fechadura solenoide 12V | `fechadura trava eletrica solenoide 12v arduino` | 1 | R$ 54,90 | R$ 54,90 | **CONFIRMADO** (Bitmaker; 4 un em estoque) | **Trava a portinhola**, não destrava a tag. Máx. 10 s contínuos |
| 14 | Protoboard 830 pontos | `protoboard 830 pontos` | 1 | R$ 11,90 | R$ 11,90 | **CONFIRMADO** (Eletrogate — corrigido de R$12,90) | Bancada. Nunca passar corrente de atuador por ela |
| 15 | Kit jumpers M/M, M/F, F/F | `kit jumpers macho femea 20cm arduino` | 1 | R$ 15,00 | R$ 15,00 | ESTIMADO | Ligações de sinal |
| 16 | Diodo 1N5408 (3A) | `diodo 1n5408 3a retificador` | 5 | R$ 0,50 | R$ 2,50 | ESTIMADO | Flyback. **Correção: 1N4007 é 1A e não aguenta o pico da bobina** |
| 17 | Porta-fusível 5×20 + fusíveis | `porta fusivel 5x20mm kit fusivel` | 1 | R$ 6,00 | R$ 6,00 | ESTIMADO (base R$0,32–1,15 confirmada) | Fusível na linha 12V do atuador |
| 18 | Capacitores 1000 µF/25V + 100 nF | `capacitor eletrolitico 1000uf 25v kit` | 1 | R$ 12,00 | R$ 12,00 | ESTIMADO | **Anti-brownout.** Item de R$3 que decide se o projeto funciona |
| 19 | Transistores BC337 + resistores | `kit transistor bc337 resistor 1k 10k` | 1 | R$ 10,00 | R$ 10,00 | ESTIMADO | Adaptação de nível, LED 12V do botão, pull-ups externos |
| 20 | Par IR barreira ou microchave | `sensor optico barreira infravermelho par emissor receptor` | 1 | R$ 15,00 | R$ 15,00 | ESTIMADO | Confirma que a etiqueta caiu. **Não usar TCRT5000 — ele é REFLEXIVO, não barreira** |
| | **Subtotal A** | | | | **R$ 615,55** | | |

### Bloco B — Estrutura e coleta

| # | Item | Termo de busca | Qtd | Unit. | Total | Status | Para que serve |
|---|---|---|---|---|---|---|---|
| 21 | MDF 6 mm cortado a laser + parafusos M3/M4 + cantoneiras | `chapa mdf 6mm corte laser` / serviço local | 1 | R$ 120,00 | R$ 120,00 | ESTIMADO | Gabinete, berço, came |
| 22 | Caixa/cofre com fechadura para coleta | `cofre pequeno com chave caixa organizadora com fechadura` | 1 | R$ 50,00 | R$ 50,00 | ESTIMADO | Caixa coletora trancada com boca antirretorno |
| | **Subtotal B** | | | | **R$ 170,00** | | |

### Bloco C — Consumíveis EAS (tentar obter da Riachuelo antes de comprar)

| # | Item | Termo de busca | Qtd | Unit. | Total | Status | Para que serve |
|---|---|---|---|---|---|---|---|
| 23 | Mini tag rígida RF 8,2 MHz c/ pino, 100 un | `etiqueta antifurto rigida mini tag rf 8.2mhz com pino 100 unidades` | 1 | R$ 170,00 | R$ 170,00 | **ESTIMADO** — os dois preços da pesquisa (R$159,90 e R$735/milheiro) estão em **URLs mortas (404 / DNS inexistente)**. Único milheiro vivo: R$854 (Canal Automação, ≈R$0,85/un) | Corpo de prova |
| 24 | Desacoplador magnético 10.000 GS | `desacoplador de etiqueta tag eas antifurto 10.000gs` | 1 | R$ 300,00 | R$ 300,00 | **CONFIRMADO** (Canal Automação, cód. U100000000077, R$300 Pix/boleto, R$315,79 cartão, frete grátis) | **Coração da estação** |
| | **Subtotal C** | | | | **R$ 470,00** | | |

### Totais

| Cenário | Total | Por aluno (8) | Cabe no orçamento? |
|---|---|---|---|
| **A — Riachuelo fornece desacoplador + etiquetas** (A + B) | **R$ 785,55** | **R$ 98,19** | Sim, com folga de R$414 |
| **B — comprando tudo** (A + B + C) | **R$ 1.255,55** | R$ 156,94 | **Não — estoura o teto de R$1.200** |
| **B' — comprando tudo, cortando contingências** (−PN532, −2º ESP32, −2º MG995) | **R$ 1.129,64** | **R$ 141,21** | Sim, mas **sem nenhum sobressalente** |

**Recomendação: perseguir o Cenário A.** A Riachuelo é a parceira e tem desacoplador e etiquetas em qualquer loja. Isso não é economia de conveniência — é a mitigação de um risco de aquisição real: **duas páginas de produto da Canal Automação declaram "esse produto será faturado somente para CNPJs que possuam atividades compatíveis com sistemas antifurto. Pedidos feitos por CPF ou CNPJs que não se enquadram serão cancelados".** Oito alunos comprando com CPF têm o pedido cancelado, e a "primeira compra do semestre" vira um mês perdido.

**Fora da lista, com justificativa registrada:**

| Item | Preço | Por que NÃO |
|---|---|---|
| Atuador linear 12V 100N | R$ 326,49 (confirmado) | 30–40% do orçamento; 100 N não verificado (página declara 36 g de peso); corrente não especificada; "últimas unidades". Substituído por came + servo |
| Ímã de neodímio N52 50×50×25 | R$ 296,00 (não confirmado) | Custa mais que o desacoplador pronto e não traz o circuito magnético. Perigo físico real |
| Eletroímã 12V 2,5 kg (P20/15) | indisponível | 3 W não reproduz o circuito magnético através do ABS. **Reprovado** |
| Solenoide push-pull 15 N / 10 mm | não verificável (Amazon HTTP 500) | Sem caminho físico até a gaiola selada. **Reprovado por geometria** |
| Anel WS2812 8 LEDs | esgotado, sem preço | Requisito é "LED verde acende" |
| Módulo UHF M5Stack JRD-4035 | US$ 79 | 36–96% do orçamento, ~1 m real, sem venda no Brasil |
| Leitor QR embarcado GM65/GM66 | não verificável | NFC faz o mesmo por R$15. Sem câmera na Estação |
| Gaussímetro | R$ 200–600 (não confirmado) | O magnetômetro do celular mede bem em 0,5–1 mT (a região de interesse) e satura só perto do polo. Declarar o método |
| RTC DS3231 | R$ 18,24 (Eletrogate — corrigido de "R$29,90–68,13") | Dispensável: o nonce já garante o anti-replay |

---

## 3. ESQUEMA DE LIGAÇÃO — ESP32 DevKit 30 pinos

### 3.1 Sinais

| GPIO | Vai para | Modo | Observação |
|---|---|---|---|
| **18** | RC522 `SCK` | SPI CLK | VSPI |
| **19** | RC522 `MISO` | SPI MISO | |
| **23** | RC522 `MOSI` | SPI MOSI | |
| **5** | RC522 `SDA/SS` | Saída (CS) | Strapping, mas é **saída** dirigida pelo ESP32 e tem pull-up interno no boot — seguro |
| **27** | RC522 `RST` | Saída | |
| **21** | OLED `SDA` | I²C | |
| **22** | OLED `SCL` | I²C | Rodar I²C scanner: endereço 0x3C **ou** 0x3D |
| **25** | Servo MG995 (came do berço) — fio de sinal | LEDC PWM 50 Hz | Alimentação **do rail 5,5–6V**, nunca da placa |
| **26** | Servo MG90S (ejetor da tag) — fio de sinal | LEDC PWM 50 Hz | |
| **14** | Servo MG90S (portinhola) — fio de sinal | LEDC PWM 50 Hz | |
| **33** | Gate do IRLZ44N (fechadura solenoide) | Saída | Resistor de gate 220 Ω + **pull-down 10k** |
| **4** | Base do BC337 via 1k → LED 12V do botão arcade | Saída | Transistor **inverte a lógica** |
| **32** | LED verde 5 mm + 220 Ω | Saída | |
| **16** | LED amarelo 5 mm + 220 Ω | Saída | |
| **17** | LED vermelho 5 mm + 220 Ω | Saída | |
| **13** | Módulo buzzer ativo `I/O` | Saída | `digitalWrite HIGH` basta |
| **34** | Microswitch KW1-103 do botão arcade (NO) → GND | **Entrada, pull-up EXTERNO 10k** | Input-only, **sem pull-up interno**. 100 nF em paralelo com o contato + debounce 20–50 ms em software |
| **35** | Sensor de queda (barreira IR / microchave) | **Entrada, pull-up EXTERNO 10k** | Confirma que a etiqueta caiu na caixa |
| **36 (VP)** | Reservado: sensor de presença da peça (analógico) | Entrada ADC1 | **ADC1** — ADC2 retorna lixo com WiFi ligado |
| 1, 3 | — | UART0 | Não usar (USB/debug) |
| 0, 2, 12, 15 | — | — | **Strapping. Não usar.** GPIO12 alto no boot pode danificar a flash |
| 6–11 | — | — | **Flash SPI. Travam a placa.** |

### 3.2 Alimentação

```
Rede 127/220V ──► FONTE EXTERNA 12V/5A (selo Inmetro) ──► [nada de rede dentro do gabinete]
                                      │
                          ┌───────────┴────────────┐
                          │   BARRA DE BORNES 12V  │
                          │   (com FUSÍVEL 3A)     │
                          └───┬────┬────┬────┬─────┘
                              │    │    │    │
        LM2596 #1 (5,0V) ◄────┘    │    │    └──► Anodo LED 12V do botão
             │                     │    │              └► catodo ► coletor BC337 (GPIO4)
             │                     │    │
             ├─► VIN do ESP32      │    └──► + da fechadura solenoide
             ├─► 1000µF/25V        │              └► retorno pelo dreno do IRLZ44N (GPIO33)
             └─► 100nF cerâmico    │              └► 1N5408 em ANTIPARALELO (faixa no +)
                                   │
        LM2596 #2 (5,5–6,0V) ◄─────┘
             ├─► fio vermelho dos 3 servos
             └─► 1000µF/25V

RC522 e OLED: alimentados pelo pino 3V3 do ESP32 (consumo 13–26 mA e ~20 mA, cabe)
```

**Regra de ouro do GND:** fonte, dois LM2596, ESP32, os três servos, IRLZ44N, botão e sensor — **todos** na mesma barra de bornes de GND, em estrela. GND não comum entre ESP32 e servo é a segunda causa mais comum de servo que treme.

**Ajustar a saída dos LM2596 com multímetro ANTES de conectar qualquer coisa.** O trimpot vem de fábrica em posição arbitrária.

---

## 4. FLUXO DE SOFTWARE

### 4.1 Firmware da Estação (pseudocódigo)

```
// ===== CONSTANTES DE SEGURANÇA =====
PULSO_MAX_MS        = 500      // came + ejetor
TRAVA_MAX_MS        = 8000     // fechadura: página declara máx 10 s contínuos
TTL_AUTORIZACAO_MS  = 20000    // janela do LED verde
TIMEOUT_REDE_MS     = 5000

setup():
    // ORDEM É REQUISITO DE SEGURANÇA, NÃO ESTILO
    pinMode(PIN_TRAVA, OUTPUT);   digitalWrite(PIN_TRAVA, TRAVADO)
    pinMode(PIN_LED_VERDE, OUTPUT); digitalWrite(PIN_LED_VERDE, LOW)
    servo_came.attach(25);   servo_came.write(POS_RECUADO)   // ímã LONGE
    servo_ejetor.attach(26); servo_ejetor.write(POS_REPOUSO)
    // só agora:
    watchdog_enable(8s)
    nvs_ler(SEGREDO_K, STATION_ID)
    wifi_conectar(lista_ssid)        // hotspot primeiro
    realtime_conectar()              // UMA conexão TLS, mantida aberta
    estado = IDLE

// ===== CANAL DE PUSH (roda em paralelo) =====
onRealtimeMessage(msg):
    // backend empurrou pré-autorização
    se verificar_hmac(msg, SEGREDO_K) E msg.station_id == STATION_ID:
        cache[msg.tag_uid] = { peca_id, exp_ts, assinatura }

// ===== MÁQUINA DE ESTADOS =====
loop():
    watchdog_feed()

    caso IDLE:
        led(VERMELHO); oled("Apoie a peca")
        uid = rfid_ler_uid()                    // POSIÇÃO 1, ímã longe
        se uid != NULL:
            uid_travado = uid; t0 = millis()
            estado = CONSULTANDO

    caso CONSULTANDO:
        led(AMARELO_PULSANTE); oled("Verificando...")
        se cache[uid_travado] existe E não expirou:
            estado = AUTORIZADO                 // decisão LOCAL, 0 ms de rede
        senão:
            nonce = esp_random()                // 16 bytes
            req = { STATION_ID, uid_travado, nonce, ts }
            req.hmac = HMAC_SHA256(K, req)
            resp = https_post("/v1/estacao/autorizar", req, TIMEOUT_REDE_MS)
            se resp.ok
               E verificar_hmac(resp, K)
               E resp.nonce == nonce            // ANTI-REPLAY: eco do MEU nonce
               E resp.decisao == LIBERAR:
                estado = AUTORIZADO
            senão:
                estado = NEGADO                 // FAIL-CLOSED

    caso AUTORIZADO:
        led(VERDE); buzzer_beep(1); oled("Pago. Aperte o botao")
        t_verde = millis()
        enquanto millis() - t_verde < TTL_AUTORIZACAO_MS:
            se botao_pressionado_debounced():
                // RELEITURA OBRIGATÓRIA: fecha a janela de troca de peça
                se rfid_ler_uid() != uid_travado:
                    estado = NEGADO; log("troca_de_peca_detectada"); sair
                estado = ACIONANDO; sair
        se timeout: estado = IDLE

    caso ACIONANDO:
        digitalWrite(PIN_TRAVA, DESTRAVADO); t_trava = millis()
        servo_came.write(POS_AVANCADO)          // berço leva a tag ao ímã (POSIÇÃO 2)
        delay(400)
        servo_ejetor.pulso(POS_EJETA, PULSO_MAX_MS)  // empurra corpo p/ fora do ímã
        servo_came.write(POS_RECUADO)           // came dá vantagem no recuo
        estado = CONFIRMANDO

    caso CONFIRMANDO:
        se sensor_queda_disparou() dentro de 3 s:
            oled("Pronto! Bom passeio"); buzzer_beep(2)
            enviar_log("liberado", uid_travado, peca_id, ts)   // best-effort
        senão:
            led(VERMELHO); oled("Falha. Chame um atendente")
            enviar_log("falha_separacao", ...)
        cache.remover(uid_travado)               // USO ÚNICO
        digitalWrite(PIN_TRAVA, TRAVADO)
        estado = IDLE

    caso NEGADO:
        led(VERMELHO); buzzer_beep(3); oled("Nao identificado. Va ao caixa")
        delay(3000); estado = IDLE

// ===== INTERTRAVAMENTOS DE HARDWARE (fora da máquina de estados) =====
watchdog_isr():        tudo para estado seguro, reset
se millis()-t_trava > TRAVA_MAX_MS: digitalWrite(PIN_TRAVA, TRAVADO)   // bobina não queima
se wifi_caiu E cache vazio: estado permanece NEGADO                    // FAIL-CLOSED
```

**Regras não negociáveis:**
- Todo `http.begin()` pareado com `http.end()` — sem isso a heap fragmenta e a Estação para de conectar depois de horas, exatamente durante o teste com a Riachuelo.
- `setCACert()` / `setCACertBundle()` na versão final. `setInsecure()` só em bancada.
- **Ler a tag ANTES de energizar o atuador, nunca durante.** O chaveamento da bobina injeta EMI no barramento SPI e a massa ferromagnética do ímã dessintoniza a antena do RC522. Este é o modo de falha "funcionou na bancada, falhou dentro da caixa" que nenhuma das seis pesquisas levantou.

### 4.2 Rotas do backend

| Método | Rota | Quem chama | O que faz |
|---|---|---|---|
| `POST` | `/webhook/pagarme` | Gateway | **Valida a assinatura do webhook antes de qualquer coisa.** A Edge Function precisa de `--no-verify-jwt` / `auth: none` para receber, o que torna a URL pública — sem validar, qualquer um POSTa "peça 42 está paga". Marca `pedido.status = pago` **somente em evento de liquidação**, nunca de mera autorização. Dispara o push |
| `POST` | `/v1/pareamento` | App do funcionário | Vincula `hardtag_uid ↔ peca_id` no momento da etiquetagem. Exige auth de funcionário |
| `POST` | `/v1/estacao/autorizar` | Estação | Recebe `{station_id, tag_uid, nonce, ts, hmac}`. Valida HMAC, janela de ts ±60 s, ineditismo do nonce, e responde `{nonce_ecoado, decisao, exp, hmac}`. **Ecoar o nonce é o que mata replay** |
| `POST` | `/v1/estacao/confirmar` | Estação | Log auditável: estação, tag, peça, pedido, horário, resultado. Este log é provavelmente o que a Riachuelo mais valoriza — prevenção de perdas |
| `POST` | `/v1/estacao/override` | Chave física / PIN de funcionário | Destravamento manual de emergência, registrado como `override`. A loja real também vai precisar disso |
| `GET` | `realtime: canal estacao:{id}` | Estação (WebSocket persistente) | Push da pré-autorização `{tag_uid, peca_id, exp, hmac}` assim que o webhook liquida |
| `POST` | `/v1/estorno` | Gateway (`PAYMENT_REFUNDED`) | **Rota que faltava em todas as pesquisas.** Revoga autorização ainda não usada e marca o item para conciliação. Se a etiqueta já caiu, gera alerta — não há como desfazer fisicamente |
| `GET` | `/health` | Cron externo (1×/dia) | Impede a pausa do projeto Supabase após 7 dias sem requisição |

---

## 5. AS 5 MAIORES INCERTEZAS QUE SOBRARAM

| # | Incerteza | Por que é grave | Teste barato que resolve |
|---|---|---|---|
| **1** | **A Riachuelo ainda usa hard tag EAS magnética, ou já migrou para RFID mole?** A rede fez implantação item-level de RFID com a Mozaiko/Stefanini; a pop-up "Incrivelmente Brasil" (rua dos Pinheiros, SP, 240 m², aberta desde 12/12/2025 por um ano) roda self-checkout e provador inteligente por RFID. **Nenhuma das fontes ligadas à Riachuelo menciona hard tag ou destravamento** | Se migrou, o "parque instalado" que o projeto promete respeitar não existe. O projeto vira ponte de transição, não solução | **Visita à pop-up da rua dos Pinheiros + 1 entrevista.** Custo: R$0 e duas horas. Perguntas: (a) nas lojas com self-checkout, ainda há funcionário com destravador? (b) fabricante/frequência/modelo da etiqueta rígida? (c) roadmap de RFID na peça? É a única loja do país onde dá para observar o problema em operação, e fica a poucos quilômetros da Poli |
| **2** | **Qual o nível de trava das etiquetas reais** — magnética de embreagem de esferas, ou mecânica (SuperTag/VST, Gator, Alpha S3)? | Se for mecânica, **ímã nenhum abre**, só gancho. Toda a arquitetura cai | Pedir **5 a 10 etiquetas reais** na loja parceira. Testar com o desacoplador. **Serrar uma ao meio** — resolve a dúvida em 15 minutos e vira uma ótima foto para o relatório |
| **3** | **Força de atração no recuo, em newtons.** Nenhuma fonte publica esse número. A pesquisa dimensionou 100 N "por margem, não por dado" | Define came, servo, mola e estrutura inteira. Se a atração real for maior que o torque do MG995 na alavanca escolhida, o berço trava | **Balança de cozinha digital + barbante.** Apoiar o desacoplador na balança, encostar a tag, puxar e ler o pico. Custo: R$0 (a balança já existe). Repetir 10 vezes com tags diferentes |
| **4** | **Destravar é separar, ou não?** A patente da Kohl's diz que precisa de 3 movimentos. A descrição comercial da Canal Automação diz que o desacoplador "extrai o pino... com muita facilidade" | Se o pino sai sozinho, economizamos o ejetor e simplificamos a mecânica. Se não sai, orçar só o movimento (1) garante falha de demo | **10 destravamentos filmados em câmera lenta** com o desacoplador na horizontal. Observar: o pino sai sozinho? Sai parcialmente? A tag fica pendurada? Custo: R$0 |
| **5** | **Detuning do NTAG213 colado na hard tag, e EMI do atuador sobre o RC522.** Ninguém mediu | É o modo de falha "funcionou na bancada, falhou dentro da caixa". Se o adesivo não ler colado na tag, a arquitetura de identificação inteira pivota para o hangtag (com a brecha de fraude que isso reabre) | **Colar um NTAG213 comum e um anti-metal (ferrite) em posições diferentes da hard tag e medir a distância máxima de leitura com os 3 RC522.** Depois repetir com o desacoplador a 5, 10 e 20 cm, e com o servo acionando. Custo: já está na lista de compras |

**Incertezas menores que ficam declaradas, não resolvidas:** se a rede WiFi de uma loja Riachuelo permite dispositivo IoT sem portal cativo; homologação ANATEL de leitor NFC 13,56 MHz vendido no Brasil (o art. 83, I da Res. 715/2019 alcança o **uso**, não só a venda, e não há artigo de dispensa para protótipo — a Res. 715 foi ainda alterada pela Res. 780/2025, que não foi verificada); e o preço de qualquer desacoplador automático pronto (Sensormatic power detacher, Alien D302/D303, Sensor Tag STRONG ST de embutir — **todos "sob consulta"**).

---

## 6. O TESTE DA SEMANA 1

**Nome:** *Ensaio de destravamento e leitura — o teste que reprova o projeto.*

### O que comprar (antes de qualquer CAD, qualquer código, qualquer reunião de design)

| Item | Custo | De onde |
|---|---|---|
| Desacoplador magnético 10.000 GS | R$ 300,00 (ou **R$0** se a Riachuelo emprestar) | Canal Automação — **atenção: só fatura para CNPJ com atividade compatível.** Tentar pela Riachuelo primeiro |
| 100 mini tags RF 8,2 MHz com pino | ~R$ 170,00 (ou **R$0** da Riachuelo) | Marketplace — **reconferir o preço manualmente, os dois anúncios da pesquisa estão fora do ar** |
| 5 a 10 etiquetas **reais da loja Riachuelo** | R$ 0,00 | Pedir na loja parceira. **Insubstituível** |
| 3 × RC522 + 20 adesivos NTAG213 | R$ 85,30 | Já na lista |
| Balança de cozinha digital, barbante, serra de arco, celular com câmera lenta e app de magnetômetro | R$ 0,00 | Já existem |

**Investimento máximo do teste: R$ 555,30 — e provavelmente R$ 85,30 se a Riachuelo fornecer o EAS.**

### O que fazer, em ordem

1. **Compatibilidade (30 min).** Apoiar cada uma das etiquetas — as 100 compradas **e** as 5–10 reais da Riachuelo — no desacoplador. Contar quantas abrem em 20 tentativas cada.
2. **Distância crítica (30 min).** Com uma régua, encontrar a **distância máxima** em que o desacoplador ainda destrava. Anotar em milímetros. Este número define o curso do came.
3. **Força de recuo (30 min).** Balança de cozinha + barbante. Destravar, e medir o **pico de força** para separar a tag do desacoplador. Repetir 10 vezes. Anotar média e máximo em gramas-força → converter para newtons.
4. **Destravar é separar? (30 min).** Filmar 10 destravamentos em câmera lenta. O pino sai sozinho, sai parcialmente, ou a tag fica pendurada?
5. **Teardown (30 min).** Serrar uma etiqueta comprada e uma real ao meio. Fotografar o interior. É embreagem de 3 esferas + mola + plunger ferromagnético, como descreve a US 7.190.272 B2 e o estado da arte da US 7.564.360 B2? Ou é outra coisa?
6. **Leitura NFC (60 min).** Colar NTAG213 em três posições diferentes da hard tag. Medir a distância máxima de leitura de UID com cada um dos 3 RC522. Repetir com o desacoplador a 5, 10 e 20 cm da antena.
7. **Campo magnético (15 min).** Com o app de magnetômetro do celular, medir o campo a 5, 10, 20 e 30 cm do desacoplador. Declarar modelo do aparelho e método. **O alvo é ficar abaixo de 5–10 gauss (0,5–1 mT) na região acessível ao público** — limites publicados por Medtronic (5 G) e Boston Scientific (10 G) para dispositivos cardíacos implantados; há estudo *in vitro* (PMID 18334784) com interferência a até 24 cm.

### O que REPROVA o projeto

| Resultado | Significa | Ação |
|---|---|---|
| As etiquetas **reais da Riachuelo** não abrem com o desacoplador de 10.000 GS | Trava Multipolar, HyperLock ou mecânica | **Pivô obrigatório.** Extrator mecânico (gancho motorizado) ou desacoplador proprietário. A arquitetura de ímã morre |
| O teardown mostra trava **mecânica** (sem plunger ferromagnético) | Ímã nenhum abre, nunca | **Pivô total.** Refazer a frente de trava do zero |
| A força de recuo passa de ~40 N | O MG995 (≈11 kgf·cm) não vence nem com came razoável | Voltar ao atuador linear (R$326,49, estoura o orçamento) **ou** adotar o shunt de aço, que elimina o problema em vez de vencê-lo por força bruta |
| O NTAG213 **não lê** colado na hard tag em nenhuma posição, nem com ferrite | Identificação na hard tag é inviável | Recuar para o hangtag de papel (opção A) **e declarar a brecha de fraude no relatório**, ou pedir à Riachuelo hard tags EAS+RFID |
| O campo a 20 cm passa de 10 gauss e não há como blindar | Risco a portador de marca-passo num equipamento de autoatendimento tocado por clientes | Circuito magnético fechado (yoke de aço envolvendo o ímã) + berço que impeça a mão de chegar ao polo. Se não resolver, **atuador magnético descoberto está reprovado por requisito de segurança** |

**Sem esses sete números, qualquer escolha de atuador, came, servo ou geometria é chute.** Nada de CAD antes deste teste.

---

## 7. REQUISITOS DA CAIXA DA ESTAÇÃO PARA O CAD

### 7.1 Dimensões externas e cotas normativas

| Parâmetro | Valor | Origem |
|---|---|---|
| Gabinete (L × P × A) | **300 × 280 × 250 mm** | Projeto. Profundidade **≤ 300 mm** é exigência da NBR 9050 9.4.3.5 |
| Altura da superfície de apoio da peça (berço) | **950 mm** do piso | Dentro da faixa 0,80–1,20 m da NBR 9050 9.4.3.5 |
| Altura do centro do botão arcade | **1.000 mm** do piso | NBR 9050 9.4.3.5 |
| Altura da boca da caixa coletora | **450 mm** do piso | NBR 9050 9.4.3.6 (0,40–1,20 m) |
| Área livre frontal | **0,80 × 1,20 m** (Módulo de Referência) | NBR 9050 9.4.3.4, aproximação frontal para cadeirante |
| Cor da boca de coleta e dos controles | **contrastante com o fundo** | NBR 9050 9.4.3.6 |
| Proteção do display contra luz | **viseira/aba de 30 mm** sobre o OLED | NBR 9050 9.4.3.3 — e resolve o falso positivo do sensor óptico |
| Fixação | **parafusada ao balcão** (4 × M6) | Antifurto do próprio equipamento — um gabinete solto contendo um destravador legitimado é, para o ladrão, um destravador universal montado |

Se o protótipo for de bancada (provável), o gabinete vai sobre um pedestal ou sobre o balcão da apresentação; as cotas acima são medidas **do piso**, não da base do gabinete.

### 7.2 O que precisa caber dentro

| Peça | Dimensões (mm) | Posição | Observação |
|---|---|---|---|
| Desacoplador magnético 10.000 GS | **reservar 130 × 100 × 60** | Compartimento inferior, **fixo** | **Dimensão real desconhecida** — a página não publica. Medir no ato do recebimento e refazer o CAD. Este é o maior risco dimensional do projeto |
| Blindagem de aço-carbono 3 mm | 120 × 100 × 3 | Entre o desacoplador e o RC522 | Reduz dessintonia e EMI. Também serve de shunt de contingência |
| Módulo RC522 | 60 × 39 × 5 (antena útil ~40 × 40) | **Imediatamente sob a POSIÇÃO 1** do berço, a ≤ 8 mm | Distância mínima, porque o alcance real com adesivo de 23 mm é 1–2 cm |
| ESP32 DevKit 30 pinos | 52 × 28 × 20 (com pinos) | Compartimento eletrônico, lateral | Longe do desacoplador e dos servos |
| 2 × LM2596 | 43 × 21 × 14 cada | Compartimento eletrônico | Trimpots acessíveis sem desmontar |
| Servo MG995 (came) | 40,7 × 19,7 × 42,9 | Sob o berço | Eixo alinhado ao came |
| 2 × Servo MG90S (ejetor + portinhola) | 22,8 × 12,2 × 28,5 cada | Um junto ao berço, um na portinhola | |
| Fechadura solenoide 12V | 55 × 24 × 28 | Na portinhola do berço | **Máx. 10 s energizada** — timeout por firmware |
| Display OLED 0.96" | 27 × 27 × 4 (PCB), área visível 22 × 11 | Painel frontal inclinado 20° | Legível a 30 cm, não a 2 m |
| Botão arcade 60 mm | **furo de painel 24–28 mm**; moldura Ø 60; êmbolo Ø 50; profundidade atrás do painel ~40 | Painel frontal, à direita do berço | **A moldura tem 60 mm mas o corte é de ~25 mm** — nuance dimensional que derruba CAD |
| 3 LEDs 5 mm | furos Ø 5 | Painel frontal, acima do berço | |
| Buzzer ativo | 33 × 15 × 12 | Interno, com furo de saída de som Ø 6 | |
| Protoboard 830 / placa perfurada | 165 × 55 × 10 | Compartimento eletrônico | **Migrar para placa soldada antes da demo final** |
| Barra de bornes 12V + GND estrela + porta-fusível | 80 × 25 × 25 | Compartimento eletrônico, junto à entrada do plug | Nenhuma tensão de rede entra no gabinete — só 12V SELV |
| Sensor de queda (par IR barreira) | 2 × (10 × 8 × 5) | Atravessando a boca do funil | **Não usar TCRT5000** — ele é reflexivo e não detecta queda livre |
| Caixa coletora | **150 × 120 × 100 interno** (≈200 tags) | Compartimento inferior frontal, gaveta com fechadura | Ver 7.5 |

**Reserva de 20% de volume livre** para cabeamento, alívios de tração e o inevitável componente esquecido.

### 7.3 O berço — a peça mais importante do CAD

**Decisão de layout que resolve três problemas de uma vez:** o berço tem **duas posições**, e o came do MG995 desloca a peça entre elas.

```
  ┌─────────────────────────────────────────────┐
  │  POSIÇÃO 1 — LEITURA          POSIÇÃO 2 —   │
  │  (ímã a ≥ 80 mm)              DESTRAVAMENTO │
  │        ▼                            ▼       │
  │  ┌──────────┐   ── came ──►   ┌──────────┐  │
  │  │ cavidade │                 │ ímã sob  │  │
  │  │  em V    │                 │ a tag    │  │
  │  └────┬─────┘                 └────┬─────┘  │
  │    RC522                    DESACOPLADOR    │
  │  (blindado)                                 │
  └─────────────────────────────────────────────┘
```

Isso resolve simultaneamente: **(a)** a dessintonia do RC522 pela massa do ímã, **(b)** a EMI do acionamento sobre o SPI (lê antes, aciona depois), e **(c)** o *gating* de segurança por **distância física** — sem autorização, o ímã está a 80 mm da tag e ela não abre nem por acidente nem de propósito. É o argumento de segurança mais forte disponível, e não depende de software.

**Geometria da cavidade:**
- Mini tag confirmada: **48 × 42 mm** (não 53 × 42; a Loja Automação Comercial declara 4,8 × 4,2 cm). Espessura ~13–15 mm — **medir**.
- Cavidade: **55 × 50 × 20 mm**, em V, com **batente assimétrico** que força uma **única orientação** — o adesivo NFC sempre para baixo, sobre o RC522.
- Precedente industrial: a US 11.183.038 B2 (Sensormatic, vigente) descreve a *alignment feature* como uma **porção côncava** do detacher. Há forma pronta para copiar.
- Abertura para o tecido: rasgo de **4 mm** na lateral do berço, por onde passa a roupa. A peça fica pendurada do lado de fora, só a etiqueta entra.
- **Guarda mecânica:** nenhuma abertura pode permitir a entrada de um dedo adulto na região do came ou do ímã. Vão máximo de 8 mm em qualquer direção de acesso.

### 7.4 Portinhola

Tampa basculante sobre o berço, mantida **travada pela fechadura solenoide** até o LED verde. Isso garante fisicamente que o cliente só alcança o assento do ímã depois da autorização — resolve o requisito antifurto sem depender apenas de software, e é argumento forte na defesa perante a Riachuelo.

Existe, aliás, produto comercial para exatamente essa função: **"Trava para Desacoplador de Etiquetas Antifurto AM e RF", Canal Automação, R$149,00** — vale citar como benchmark de que o setor já trata esse risco.

### 7.5 Caixa coletora

- Interno **150 × 120 × 100 mm**, capacidade ≈200 tags.
- **Trancada com chave.** Esvaziada apenas por funcionário.
- **Boca antirretorno** (aba de silicone ou lâmina basculante): só entra, não sai. Sem isso, o cliente pega a etiqueta de volta e a estação vira distribuidora de hard tags armadas, que disparam pórticos de outras lojas.
- Boca a **450 mm do piso**, cor contrastante (NBR 9050 9.4.3.6).
- Calha inclinada a **35°** do berço até a boca, para a etiqueta cair por gravidade.
- Par IR em barreira atravessando a boca, confirmando a queda.

**Correção importante da justificativa:** a pesquisa de normas afirmou que "cada hard tag contém um ímã e um pino de aço", e construiu sobre isso todo o risco de ingestão de múltiplos ímãs de neodímio. **Isso é falso** — a hard tag é embreagem de esferas: esferas de aço + mola + plunger ferromagnético, e **o ímã está no destravador, fora da etiqueta**. O requisito de caixa trancada **sobrevive**, mas por outro motivo: **pino de aço pontiagudo, esferas soltas e mola ao alcance de criança**, num varejo de moda que vende infantil. Se o relatório mantiver a justificativa errada, é demolido por qualquer pessoa que abra uma hard tag.

### 7.6 Painel frontal — layout

```
        ┌──────────────────────────────────────────┐
        │            [ viseira 30 mm ]             │
        │   ┌──────────────────────┐               │  ← 1.030 mm do piso
        │   │  OLED 128×64         │   ● ● ●       │
        │   └──────────────────────┘  VM AM VD     │
        │                                          │
        │   ┌────────────┐         ╭─────────╮     │  ← 950 mm (berço)
        │   │  BERÇO     │         │ BOTÃO   │     │  ← 1.000 mm (botão)
        │   │  (tampa)   │         │ Ø60/25  │     │
        │   └────────────┘         ╰─────────╯     │
        │                                          │
        │        ▓▓▓ boca de coleta ▓▓▓            │  ← 450 mm
        └──────────────────────────────────────────┘
```

---

## O QUE NÃO FECHOU — declarado

- **Preço de etiqueta EAS e de qualquer desacoplador automático pronto.** Três URLs mortas, duas páginas vivas sem preço publicado, uma esgotada. O único preço de desacoplador verificado em página com botão de compra é **R$300,00 (Canal Automação, 10.000 GS)** — e a própria descrição diz que **10.000 GS é o modelo de MENOR potência da categoria**, não a "margem de força para cobrir SuperLock" que a pesquisa afirmou.
- **A premissa de R$3/etiqueta do briefing não foi derrubada.** Os dois preços que a derrubariam (R$0,74 e R$1,60) estão em páginas fora do ar. O único milheiro verificável é R$854 (≈R$0,85/un), e ainda assim a comparação é de categoria errada: se a Estação precisa **ler** a peça, a etiqueta comparável não é a EAS burra e sim uma hard tag EAS+RFID, cujo preço está justamente na faixa dos R$3. **Não trocar a premissa por um número não verificado** — pior que usar R$3 é usar R$0,85 e a banca pedir a fonte.
- **Números de perda em self-checkout.** Os "3,5% vs 0,21%" que circulam **não estão no estudo do ECR** — vêm de agregadores, são de varejo alimentar e a NRF descontinuou sua pesquisa de shrink em 2024. O que o estudo real diz: 2,87% das transações auditadas com ao menos um erro; perda líquida de 4,68% das vendas de Scan and Go em auditoria completa; lojas com self-checkout fixo com perdas 33% a 147% maiores. E o mecanismo é outro — no supermercado a perda é o cliente **não escanear** itens; aqui o pagamento é no app antes e a máquina só libera o que o backend autorizou.
- **Liberdade de operação no Brasil.** Todas as 15+ patentes levantadas são americanas e **não produzem efeito aqui**. Não houve busca no INPI. A US 7.564.360 B2 está expirada desde 2017 e **não tem membro brasileiro na família**, o que é bom para citar como referência conceitual — mas ela põe o solenoide **dentro** da etiqueta, ou seja, é a arquitetura **oposta** à nossa. E o relatório precisa reconhecer que a US 11.417.186 B2 e a US 11.984.003 B2 (Kohl's), das quais copiamos os três movimentos, estão **vigentes**: citar só a patente conveniente é uma assimetria visível para qualquer banca.
- **Vetores de fraude sem tratamento:** **estorno depois da liberação** (cliente paga, a etiqueta cai, a peça sai, e só então vem o chargeback ou a devolução de Pix — janela estrutural que o caixa com funcionário não tem) e **devolução/troca** (a peça volta sem etiqueta e precisa ser re-etiquetada por alguém que não existe mais no fluxo). Ambos são tão "genuinamente novos" quanto o "pagar barato e liberar caro", e nenhuma das seis pesquisas os levantou.
- **O contra-argumento mais perigoso, que vem da própria pesquisa:** desacoplador magnético de 10.000–12.000 GS é vendido abertamente a pessoa física no Brasil. Se qualquer um compra o ímã, **a Estação não adiciona segurança nenhuma** — a tese de valor tem que ser **fila e tempo de atendimento**, não prevenção de perdas. Há inclusive fonte primária e citável para isso: a própria US 7.564.360 B2, no estado da arte, registra que *"thieves sometimes carry magnets strong enough to remove the tags"*.
- **Não há uma única medida do problema.** Nenhuma das seis frentes mediu tempo de fila, tempo de destravagem por peça, ou proporção do atendimento gasto na hard tag. **Sem baseline não existe métrica de sucesso** — e essa medição custa um cronômetro e uma tarde numa loja.