# Projetos parecidos com o Tag&Go (pagar no celular e a etiqueta/trava se solta): catálogo, reúso e lições para o MVP

Escopo: projetos maker, estudantis e comerciais próximos da arquitetura "ESP32 + tela com QR + microservo + LED + botão; o celular lê o QR, abre uma página, 'paga' e a etiqueta recebe o comando de destravar (Wi-Fi/MQTT ou Bluetooth)". Pesquisa feita em 29/09/2026. Onde uma informação vem só do resumo de um buscador (página não aberta), isso está indicado.

---

## 1. Projetos open-source análogos (link, arquitetura, peças, o que dá para reaproveitar, dificuldade)

### Takeaway
Existe um projeto no GitHub quase idêntico ao Tag&Go: o **smart-security-tag** (ESP32 + servo + buzzer + página de pagamento simulada em Flask, licença MIT). Ele serve de modelo direto. O projeto brasileiro **maquina-vending-esp32** (Mercado Pago + webhook + MQTT, atualizado em ago/2026) é a melhor referência de arquitetura para uma versão futura com Pix de verdade. Não encontrei **nenhum** projeto com arquivos 3D de uma trava de etiqueta. A carcaça e o trinco vão ter que ser projetados pela equipe.

### Cited Findings

**A. kishoreSpandiyan/smart-security-tag: o mais próximo do Tag&Go**
- Etiqueta de segurança IoT com ESP32 que detecta violação por um laço de fio (se o fio é cortado, o buzzer toca). Depois do pagamento validado via QR, um servo destrava a etiqueta — [GitHub](https://github.com/kishoreSpandiyan/smart-security-tag)
- Fluxo: celular → interface de pagamento por QR → servidor Flask → verificação do pagamento → sinal de destravar por HTTP para o ESP32 → servo solta. O usuário lê o QR, abre a página e clica em "Pay Now" — [GitHub](https://github.com/kishoreSpandiyan/smart-security-tag)
- Peças: ESP32, servo, buzzer, protoboard e jumpers, laço de fio antiviolação — [GitHub](https://github.com/kishoreSpandiyan/smart-security-tag)
- Arquivos: pasta `esp32_sketch` (firmware), `app.py` (Flask), `database.db` (SQLite), `templates/static` (HTML/CSS/JS), `requirements.txt`. Não há arquivos 3D nem esquemático. Licença MIT, 3 commits. Entre as "melhorias futuras" estão "geração real de QR" e "integração com APIs de pagamento reais", ou seja, o pagamento é simulado — [GitHub](https://github.com/kishoreSpandiyan/smart-security-tag)

**B. eduardowakim-lab/maquina-vending-esp32: máquina de vendas brasileira com Pix via Mercado Pago**
- ESP32 com 4 motores de passo (drivers A4988). O backend é um Cloudflare Worker integrado ao Mercado Pago (checkout redirecionado e "Payment Brick" com Pix/cartão dentro da própria página). O ESP32 só recebe o comando de dispensar depois que o **webhook** confirma o pagamento aprovado — [GitHub](https://github.com/eduardowakim-lab/maquina-vending-esp32)
- Comunicação: MQTT com TLS no broker EMQX (porta 8883), tópico `vending/machine-001/down/command`, QoS 1. **Se o broker ficar mais de 30 s fora do ar, o firmware passa a consultar por HTTP a cada 3 s**. Publica status a cada 15 s — [GitHub](https://github.com/eduardowakim-lab/maquina-vending-esp32)
- Bibliotecas: WiFiManager e PubSubClient. Tem OTA (baixa `firmware.bin` quando há versão nova). Os segredos (token do Mercado Pago, MQTT) ficam fora do repositório. Última atualização documentada em 30/08/2026. **Não há licença declarada** — [GitHub](https://github.com/eduardowakim-lab/maquina-vending-esp32)

**C. MicaellaSalili/smartlocker: armário inteligente com QR**
- Frontend em Flutter, backend Node.js/Express + MongoDB, arquivo `ESP32_SmartLocker_Code.ino`, `qr-generator.html` e documentação `SECURE_QR_IMPLEMENTATION.md`. Licença MIT, 50 commits — [GitHub](https://github.com/MicaellaSalili/smartlocker)
- Segundo o resumo do buscador, o usuário lê um QR e o ESP32 recebe um comando UNLOCK via MQTT. A página aberta não detalha o broker — [GitHub (arquivo .ino)](https://github.com/MicaellaSalili/smartlocker/blob/main/ESP32_SmartLocker_Code.ino)
- A documentação cita dificuldades com conexão ao MongoDB, CORS, rede emulador→localhost e unicidade de telefone — [GitHub](https://github.com/MicaellaSalili/smartlocker)

**D. minhtran324/SE42_SmartLocker (projeto estudantil)**
- Segundo o resumo do buscador (repositório não aberto): viajantes reservam, pagam e acessam armários em estações sem atendente via QR/OTP/PIN ou reconhecimento facial. As fechaduras são solenoides controladas por ESP32 via MQTT — [GitHub](https://github.com/minhtran324/SE42_SmartLocker)

**E. benjskinner/esp32-smart-lockbox: caixa de entregas com link QR de uso único**
- ESP32 com relé de trava (GPIO 26), sensor PIR (GPIO 27) e LED (GPIO 2). Configuração de Wi-Fi por BLE (NimBLE), WebSocket para o servidor e links QR de uso único para visitantes sem instalar app. Licença MIT, 3 commits, sem arquivos CAD — [GitHub](https://github.com/benjskinner/esp32-smart-lockbox)
- Fallback offline: "se a conexão WebSocket cair por mais de 8 segundos, a caixa destrava sozinha para não prender os itens" (fail-open). Há ainda uma carência de 45 s após destravar antes de travar de novo — [GitHub](https://github.com/benjskinner/esp32-smart-lockbox)

**F. Outros firmwares de trava por MQTT (vistos só no resumo do buscador)**
- se-05-sdlms/smart-locking-esp32: firmware que assina tópicos MQTT para receber comandos de destravar — [GitHub](https://github.com/se-05-sdlms/smart-locking-esp32)
- elvandry13/esp32-smart-door-lock: RFID + relé + fechadura solenoide, com log por MQTT e aviso por Telegram — [GitHub](https://github.com/elvandry13/esp32-smart-door-lock)
- Levantosina/ESP32-MQTT-Servo-Control: controla um servo via MQTT, com botões, **testado no simulador Wokwi** — [GitHub](https://github.com/Levantosina/ESP32-MQTT-Servo-Control)

**G. Tutoriais de base: servo + servidor web e MQTT**
- Random Nerd Tutorials, "ESP32 Servo Motor Web Server": servidor web no próprio ESP32 com um slider que move o servo. Usa a biblioteca ESP32Servo e o GPIO 13 (evitar os GPIOs 9, 10 e 11, ligados à flash). O código é gratuito — [Random Nerd Tutorials](https://randomnerdtutorials.com/esp32-servo-motor-web-server-arduino-ide/)
- O mesmo tutorial diz que um servo pequeno (S0009) pode ser alimentado direto pelo ESP32. Com mais de um servo, ou outro modelo, "provavelmente será preciso uma fonte externa", com o GND do servo ligado ao GND do ESP32 e ao da fonte — [Random Nerd Tutorials](https://randomnerdtutorials.com/esp32-servo-motor-web-server-arduino-ide/)
- Random Nerd Tutorials, "ESP32 MQTT Publish Subscribe" e "ESP32 Access Point (AP) Web Server": base para MQTT e para o ESP32 criar a própria rede — [RNT MQTT](https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/); [RNT AP](https://randomnerdtutorials.com/esp32-access-point-ap-web-server/)
- SunFounder (ESP32 Starter Kit, vídeo 30): servo controlado pela web via MQTT com Adafruit IO — [SunFounder](https://docs.sunfounder.com/projects/esp32-starter-kit/en/latest/arduino_video_course/video_30_servo_mqtt.html)
- ESP32 Web Bluetooth (alternativa BLE): guia de introdução — [Random Nerd Tutorials](https://randomnerdtutorials.com/esp32-web-bluetooth/)

**H. QR em e-paper / OLED (etiqueta digital)**
- ftjuh/ePaper-writer: sketch para ESP32 que escreve imagens, texto e **QR codes** num e-paper a partir de uma interface no navegador. Usa GxEPD2 e foi testado no WeAct 2.13" — [GitHub](https://github.com/ftjuh/ePaper-writer)
- G6EJD/ESP32-e-paper-QRcode-generator: gera e mostra QR em e-paper. Um único `.ino`, 12 estrelas, 4 commits — [GitHub](https://github.com/G6EJD/ESP32-e-paper-QRcode-generator)
- geprc/QRcode_EPD: biblioteca de QR para e-paper (Arduino, testada em ESP32). ZinggJM/GxEPD2 é a biblioteca padrão de e-paper — [QRcode_EPD](https://github.com/geprc/QRcode_EPD); [GxEPD2](https://github.com/ZinggJM/GxEPD2)
- yoprogramo/ESP_QRcode: gerador de QR para ESP32 compatível com SSD1306, SH1106, TFT e e-ink — [GitHub](https://github.com/yoprogramo/ESP_QRcode)
- PhillipJacobsen/Generate_Display_QRcode_ESP32_OLED_TFT: demo de QR em OLED/TFT. Pelo resumo do buscador, o QR pode ser ampliado 2× (cada módulo do QR vira 4 pixels) e lê melhor com fundo aceso — [GitHub](https://github.com/PhillipJacobsen/Generate_Display_QRcode_ESP32_OLED_TFT)
- Ubique IoT: tutorial de configuração de Wi-Fi com SoftAP e **display e-ink** (a tela mostra os dados de conexão) — [Ubique IoT](https://www.ubiqueiot.com/posts/esp32-wifi-provisioning-with-soft-ap-and-eink-display)

**I. Portal cativo / ESP32 como ponto de acesso**
- CDFER/Captive-Portal-ESP32: "um exemplo de portal cativo para ESP32 que realmente funciona" (AsyncTCP, SoftAP sem senha, DNS que redireciona para a página) — [GitHub](https://github.com/CDFER/Captive-Portal-ESP32)

### Inferences
- **Grau de reúso:**
  - smart-security-tag (MIT): dá para usar o fluxo inteiro e as páginas HTML, citando a fonte.
  - RNT servo web server: base mais simples, só com o ESP32, sem backend.
  - maquina-vending-esp32: sem licença, então serve só como **referência de arquitetura**. Não copiar o código literalmente.
  - smartlocker (Flutter + Node + MongoDB): pesado demais para iniciantes.
- **Dificuldade estimada:**
  - Tutorial RNT servo web: fácil.
  - smart-security-tag: fácil a médio (exige Python/Flask).
  - Projetos com MQTT: médio.
  - maquina-vending-esp32 (TLS, Cloudflare, webhook): médio a difícil.
  - smartlocker: difícil.
- Nenhum projeto encontrado traz STL/CAD de trinco ou carcaça de etiqueta. O mecanismo impresso em 3D (servo empurrando um pino/lingueta) é a parte original do projeto e também a de maior risco.
- O fallback fail-open do lockbox (destrava ao perder a conexão) é o **oposto** do que uma etiqueta antifurto precisa. O Tag&Go deve ser fail-secure (continua travado sem conexão) e ter um destravamento local de emergência (botão escondido ou sequência de botão) para a demo.

### Gaps
- Não encontrei projetos no Hackster ou Instructables tão próximos quanto o smart-security-tag. As buscas trouxeram sobretudo GitHub. Printables/Thingiverse ("servo latch", "micro servo lock") não foram pesquisados, então não sei se há trincos imprimíveis prontos.
- As datas do último commit do smart-security-tag, do SE42_SmartLocker e do smartlocker não apareceram nas páginas abertas.
- Os repositórios C.2, D e F foram vistos apenas pelo resumo do buscador. A arquitetura exata deles não foi conferida.
- Não achei vídeos no YouTube (em português ou inglês) que mostrem exatamente "pagar no celular → etiqueta abre" com código público.

---

## 2. Referências comerciais para citar como inspiração

### Takeaway
A ideia já existe no varejo: **rapitag** (Alemanha, destrava por Bluetooth depois de pagar no app, piloto na Saturn em 2018) e **Sensormatic + Zliide** (etiqueta que se solta sozinha com o celular, 2023) são as referências diretas. **MishiPay** mostra o "scan & go" que desativa a etiqueta RFID. No Brasil, vending machines com Pix (Pix2U, Pixmaq) usam a mesma lógica de "paga e libera".

### Cited Findings
- **rapitag** (Munique, fundada em ago/2017 por Alexander Gaab e Sebastian M. Czich): etiqueta antifurto IoT patenteada. O cliente escaneia o produto com o celular, paga no app do varejista e a etiqueta destrava sozinha — [Dealroom via busca](https://app.dealroom.co/companies/rapitag); [rapitag – How it works](https://rapitag.com/how-it-works/)
- rapitag: "a solução envia um código identificador único para a etiqueta via Bluetooth após o pagamento". As etiquetas não podem ser abertas com ímã como as convencionais. Slogan: "Easier to shop, harder to steal" — [iXtenso](https://ixtenso.com/technology/rfid-tags-with-features-for-the-cashierless-store.html); [rapitag](https://rapitag.com/how-it-works/)
- Piloto "Saturn Smartpay" (MediaMarktSaturn) em Ingolstadt, set/2018, com PayPal e cartão. Usava a etiqueta "Spider", pensada para itens mais caros — [iXtenso](https://ixtenso.com/technology/rfid-tags-with-features-for-the-cashierless-store.html)
- A rapitag tem uma linha para moda, a "Fashiontag" (página do produto não carregou) — [rapitag Fashiontag](https://rapitag.com/products-fashiontag/)
- **Sensormatic Solutions + Zliide** (jan/2023, NRF 2023): o cliente compra na loja e **ele mesmo solta a etiqueta usando o celular**, pela experiência de compra móvel da Zliide. A etiqueta é de uma peça, se solta sozinha e tem o pino integrado. Há versões AM, RF e RFID — [BusinessWire](https://www.businesswire.com/news/home/20230116005044/en/Sensormatic-Solutions-by-Johnson-Controls-collaborates-with-Zliide-to-reimagine-self-checkout); [Sensormatic NRF 2023](https://www.sensormatic.com/resources/pr/2023/nrf-2023-zliide); [Loss Prevention Media](https://losspreventionmedia.com/key-steps-to-securing-self-checkout/)
- **MishiPay**: app "Scan & Go" (lê QR/código de barras do produto, paga no app e sai). O app desativa a etiqueta RFID automaticamente, sem ninguém tirar a etiqueta rígida. Também tem um quiosque RFID de autoatendimento — [RFID Journal](https://www.rfidjournal.com/news/self-checkout-solution-employs-rfid-for-security-purchasing/199029/); [MishiPay app](https://mishipay.com/us/the-mishipay-app/); [Kiosk Marketplace](https://www.kioskmarketplace.com/news/mishipay-intros-rfid-enabled-self-checkout-kiosk/)
- **Vending com Pix no Brasil**:
  - Pix2U gera o QR Pix em tempo real numa tela colorida, direto com o Mercado Pago, valida em segundos e libera o pulso/temporizador da máquina — [Pix2U](https://pix2u.com/)
  - Pixmaq oferece telemetria e Pix com vários adquirentes, entre eles o Mercado Pago — [Pixmaq](https://pixmaq.com.br/)
  - Há catracas Pix para máquinas de bolinhas — [Rafael Aquino (resultado de busca; a página deu 404 ao abrir)](https://www.rafaelaquino.com.br/2025/08/catraca-eletronica-com-pagamento-via.html)

### Inferences
- Para a apresentação, a comparação natural é: "rapitag/Zliide fazem isso com Bluetooth + app nativo; o Tag&Go faz com QR + página web, sem instalar app".
- A existência de soluções comerciais de Pix para vending (Pix2U, Pixmaq) mostra que "Pix confirma → microcontrolador libera" é um padrão maduro no Brasil. Isso reforça que a integração real é possível num produto, mesmo que fique fora do MVP.

### Gaps
- **Amazon Locker e armários com QR** e **etiquetas eletrônicas de prateleira (ESL) em e-paper** (VusionGroup/SES-imagotag, Pricer, Hanshow) não foram pesquisados nesta rodada. Não há fontes aqui para citá-los.
- Duração de bateria, preço por etiqueta e varejistas de moda que usam rapitag ou Zliide hoje não foram encontrados (as páginas de produto da rapitag não carregaram).

---

## 3. Lições de builds parecidos: falhas comuns em demo ao vivo e como mitigar

### Takeaway
Os riscos mais bem documentados são quatro:
- **reset por brownout quando o servo liga**;
- **Wi-Fi da universidade (WPA2-Enterprise/eduroam) ou com portal cativo**;
- **broker público fora do ar**;
- **Web Bluetooth não funciona no iPhone**.

As mitigações comprovadas são um capacitor grande e alimentação separada para o servo, hotspot próprio ou ESP32 em modo AP, fallback de HTTP quando o MQTT cai, e página web em vez de BLE.

### Cited Findings
**Energia / servo**
- Quando o servo liga, a placa pode resetar por brownout: o ESP32 detecta queda de tensão e se reinicia — [Universal Solder](https://www.universal-solder.ca/troubleshooting-esp32-brownout/); [espboards](https://www.espboards.dev/troubleshooting/issues/power/esp32-brownout-reset/)
- A correção mais eficaz é um eletrolítico de 470–1000 µF de baixo ESR entre VCC e GND, o mais perto possível do ESP32, mais um cerâmico de 0,1 µF. Também ajuda alimentar servos e motores por uma fonte separada e caprichar no aterramento — [resultados de busca: Universal Solder / PCBVault / Embedded Prep](https://www.universal-solder.ca/troubleshooting-esp32-brownout/); [PCBVault](https://pcbvault.com/electronics-troubleshooting/esp32-keeps-resetting.html)
- Existe o "atalho" de desativar o detector de brownout, com um artigo dedicado a isso — [robmiles.com](https://www.robmiles.com/journal/2020/1/20/disabling-the-esp32-brownout-detector)

**Bateria**
- Com Wi-Fi ativo o ESP32 consome cerca de 80–240 mA, com picos de ~200 mA na transmissão. Em deep sleep, o módulo nu consome ~5–10 µA, mas **uma placa de desenvolvimento pode consumir 1–5 mA** por causa dos periféricos (resumo do buscador; não verificado página a página) — [Zbotic](https://zbotic.in/esp32-deep-sleep-long-battery-life-for-remote-sensors/); [Last Minute Engineers](https://lastminuteengineers.com/esp32-sleep-modes-power-consumption/)
- Em cada ciclo, reconectar ao Wi-Fi e ao MQTT/TLS custa energia. Se a conexão leva 10 s em vez de 2 s, a autonomia muda muito — [resultado de busca, Zbotic/DeepBlue](https://deepbluembedded.com/esp32-sleep-modes-power-consumption/)

**Rede no local da demo**
- O ESP32 tem suporte a WPA2-Enterprise (eduroam), mas há muitos relatos de falha:
  - issue "Can't connect to eduroam WPA2 Enterprise network" — [arduino-esp32 #4229](https://github.com/espressif/arduino-esp32/issues/4229)
  - "WiFiClientEnterprise.ino does not work for some Eduroam networks" — [#1891](https://github.com/espressif/arduino-esp32/issues/1891)
  - falhas de conexão a redes Enterprise — [#5027](https://github.com/espressif/arduino-esp32/issues/5027)
  - erros de alocação e Guru Meditation, e conexão de até ~6 s — [ESP32 Forum](https://www.esp32.com/viewtopic.php?t=24545)
  - existe um repositório dedicado só a fazer isso funcionar — [martinius96/ESP32-Eduroam](https://github.com/martinius96/ESP32-Eduroam)
- Portal cativo é a página de login que aparece ao entrar no Wi-Fi de hotéis, aeroportos e cafés — [CDFER/Captive-Portal-ESP32](https://github.com/CDFER/Captive-Portal-ESP32); [iotespresso](https://iotespresso.com/create-captive-portal-using-esp32/)
- O ESP32 pode criar a própria rede (modo Access Point) e servir a página localmente, sem internet — [RNT ESP32 AP Web Server](https://randomnerdtutorials.com/esp32-access-point-ap-web-server/)
- Armadilha com iPhone: chamar `WiFi.scanNetworks()` com o SoftAP ligado faz aparelhos Apple perderem a rede. Faça o scan antes de subir o AP (resumo do buscador sobre portais cativos ESP32) — [CDFER/Captive-Portal-ESP32](https://github.com/CDFER/Captive-Portal-ESP32)

**Broker / nuvem**
- A máquina de vendas brasileira passa a consultar por HTTP a cada 3 s quando o broker MQTT fica mais de 30 s indisponível — [eduardowakim-lab](https://github.com/eduardowakim-lab/maquina-vending-esp32)
- Tutoriais para iniciantes usam brokers públicos gratuitos (broker.emqx.io, HiveMQ) — [Embarcados](https://embarcados.com.br/esp32-c6-na-pratica-comunicacao-mqtt/); [EMQ](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker); [Cytron](https://www.cytron.io/tutorial/getting-started-esp32-and-nodered)

**Bluetooth vs. página web**
- Web Bluetooth não funciona em nenhuma versão do Safari no iOS, nem no Firefox. Funciona em Chrome, Edge e Opera no Android/Windows. No iPhone o contorno é o navegador Bluefy — [Can I use](https://caniuse.com/web-bluetooth); [Bluefy](https://apps.apple.com/pa/app/bluefy-web-ble-browser/id1492822055?l=es-MX)

**Tela / leitura do QR**
- E-paper: a atualização completa leva uns 2–4 s (preto e branco) e a parcial 200–500 ms. Atualizações parciais repetidas deixam fantasma (ghosting), então é preciso uma atualização completa a cada 5–10 ciclos (resumo do buscador) — [Zbotic](https://zbotic.in/e-paper-partial-refresh-faster-updates-for-dynamic-content/); [esp32s.com](https://www.esp32s.com/blog/mastering-esp32-e-paper-displays-a-developers-guide-to-low-power-high-impact-iot-visuals/); [Waveshare docs](https://docs.waveshare.com/ESP32-Peripheral-Tutorials/Display/E-Paper)
- Um módulo 2.13" "fast refresh" (GDEY0213B74) anuncia 1,5 s rápida, 3 s completa e 0,4 s parcial (dado do vendedor) — [buy-lcd](https://www.buy-lcd.com/products/fast-refresh-213-inch-hd-250x122-eink-display-esp32-module-small-screen-spi-epaper-gdey0213b74esp32-lc02)
- OLED 0,96" (128×64): ampliar o QR 2× e usar fundo aceso melhora a leitura — [PhillipJacobsen](https://github.com/PhillipJacobsen/Generate_Display_QRcode_ESP32_OLED_TFT)

**Falha segura**
- O lockbox destrava sozinho se perder o WebSocket por mais de 8 s (fail-open) — [benjskinner](https://github.com/benjskinner/esp32-smart-lockbox)

### Inferences
- **Brownout é o risco nº 1 de hardware** num dispositivo a bateria com servo. O pico do servo coincide com o momento-chave da demo (destravar). Mitigação: capacitor de 470–1000 µF perto do ESP32; servo alimentado direto da bateria/5 V e não do pino 3,3 V; GND comum; e **testar sempre na bateria, não no USB do notebook**.
- **Não contar com o Wi-Fi do local.** A USP provavelmente usa eduroam (WPA2-Enterprise, não verificado), em que o ESP32 é instável, e redes com portal cativo não funcionam para o ESP32. Plano A: hotspot 2.4 GHz de um celular da equipe (SSID/senha fixos no firmware). Plano B: ESP32 em modo AP servindo a própria página de pagamento.
- **Broker público é bom para desenvolver, arriscado na demo.** Opções: rodar um Mosquitto local no notebook ligado ao mesmo hotspot, ou nem usar broker (ESP32 servindo a página, como no tutorial RNT). Usar um tópico único (ex.: `taggo/<id-aleatório>/unlock`) para não colidir com outros usuários do broker público.
- **Página web em vez de Bluetooth.** Como Web Bluetooth não funciona no iPhone, um avaliador com iPhone não conseguiria "pagar" pelo navegador. Wi-Fi + página funciona em qualquer celular.
- **QR estático.** No e-paper, desenhe o QR uma vez no boot. A imagem fica mesmo sem energia e os 2–4 s de atualização não atrapalham. URL curta (poucos caracteres → QR de versão baixa, módulos maiores), quiet zone branca e teste com iPhone e Android. O e-paper é reflexivo (sem brilho próprio), o que tende a ajudar sob luz forte. Não há fonte específica sobre reflexo.
- **Fail-secure + override.** O MVP deve ficar travado se perder a conexão, com um destravamento local (botão escondido ou sequência de cliques) para não travar a peça do avaliador.

### Gaps
- Não achei relatos em primeira pessoa de "a demo falhou por X" em projetos parecidos (post-mortems). As lições acima vêm de documentação técnica e de issues, não de relatos de feiras.
- Não há fonte sobre leitura de QR sob reflexo em telas brilhantes vs. e-paper, nem sobre a qualidade da câmera do celular.
- Não há dados medidos de autonomia de um ESP32 + servo + e-paper numa etiqueta pequena. A equipe terá que medir.
- A política de Wi-Fi da sala da apresentação (USP/Riachuelo) não foi verificada.

---

## 4. Pix real (Mercado Pago/PagSeguro sandbox + webhook + ESP32): viável para iniciantes?

### Takeaway
É viável tecnicamente, mas **não para o MVP de iniciantes**. O Pix de teste do Mercado Pago só pode ser validado por chamada de API (não dá para "pagar" de verdade com o celular em sandbox). Além disso, o webhook exige um servidor público na internet entre o Mercado Pago e o ESP32. **Recomendação: manter o pagamento simulado** e, no máximo, citar a arquitetura real (webhook → servidor → MQTT → ESP32) como próxima etapa.

### Cited Findings
- Documentação do Mercado Pago: o Pix "não pode ser testado por compras simuladas como os outros meios". O teste é criar uma ordem pela API `/v1/orders` com o Access Token de teste. Com `payer.first_name = "APRO"` a ordem nasce `action_required` e o pagamento vira `approved` automaticamente. "Só será possível verificar o funcionamento da integração por meio de uma requisição, não simulando uma compra" — [Mercado Pago Developers](https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/integration-test/pix)
- Há um conflito: o resumo de um buscador afirmou que pagamentos Pix "não podem ser feitos com credenciais de teste", enquanto a documentação oficial acima diz que podem ser testados via API (com APRO), mas não via compra simulada. A documentação oficial é a que vale — [Mercado Pago Developers](https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/integration-test/pix)
- É preciso criar pelo menos dois usuários de teste (vendedor e comprador) — [DEV Community (resultado de busca)](https://dev.to/tadeubdev/integrando-mercado-pago-checkout-pro-com-contas-de-teste-problemas-reais-e-como-resolvi-343c)
- O título do artigo acima fala em "problemas reais" de integrar o Checkout Pro com contas de teste — [DEV Community](https://dev.to/tadeubdev/integrando-mercado-pago-checkout-pro-com-contas-de-teste-problemas-reais-e-como-resolvi-343c)
- Um projeto real brasileiro que faz isso precisou de um backend na nuvem (Cloudflare Worker) para criar o checkout e receber o webhook, e de um broker MQTT com TLS para avisar o ESP32 — [eduardowakim-lab](https://github.com/eduardowakim-lab/maquina-vending-esp32)
- Há gente contratando freelancer para uma "Interface PIX com ESP32 e Mercado Pago" (ESP32 com Wi-Fi, display e token do MP para gerar o Pix) — [99freelas](https://www.99freelas.com.br/project/interface-pix-com-esp32-e-mercado-pago-580852)
- O próprio smart-security-tag deixa "integração com APIs de pagamento reais" como melhoria futura — [GitHub](https://github.com/kishoreSpandiyan/smart-security-tag)

### Inferences
- O ESP32 fica atrás do NAT do hotspot e não recebe um webhook diretamente. Então a arquitetura real sempre precisa de um servidor público (Cloudflare Worker, Railway ou similar) + MQTT ou polling. São mais duas peças que podem falhar ao vivo.
- Em sandbox não existe um "pagar com o app do banco" que dê para mostrar ao vivo. Seria preciso cobrar um Pix real de R$ 0,01–1,00 em produção, o que envolve credenciais de produção, conta verificada e segurança do token. É risco e esforço desproporcionais para o MVP.
- Um meio-termo apresentável: a página simulada mostra um "QR Pix" ilustrativo e o botão "Confirmar pagamento". No backend, opcionalmente, uma chamada de teste com APRO para mostrar o status "approved" na documentação, fora do caminho crítico da demo.

### Gaps
- PagSeguro/PagBank sandbox para Pix não foi pesquisado.
- Não verifiquei se a exigência de assinatura do webhook (x-signature) do Mercado Pago complica o backend de teste.

---

## 5. Tutoriais brasileiros (em português) para a equipe seguir

### Takeaway
Os melhores achados em português são do **Embarcados** (ESP32 + MQTT com página HTML embarcada, 2025) e do **Curto Circuito** (MQTT com app, teste de servo). Não localizei tutoriais específicos de MakerHero, Eletrogate ou Usinainfo sobre ESP32 + MQTT + servo nesta rodada. Os tutoriais em inglês do Random Nerd Tutorials continuam sendo a base mais didática.

### Cited Findings
- **Embarcados, "ESP32-C6 na Prática: Comunicação MQTT"** (Guilherme Fernandes, 28/07/2025): controle de LED via MQTT com brokers públicos (broker.emqx.io ou HiveMQ), biblioteca PubSubClient, interface HTML/JS embarcada no firmware (configura o broker via WebSocket sem regravar), tarefas FreeRTOS para o botão e código completo no GitHub. O autor avisa que HTML/JS pode ser difícil no início — [Embarcados](https://embarcados.com.br/esp32-c6-na-pratica-comunicacao-mqtt/)
- **Embarcados, "101 – Integrando o ESP32 ao Home Assistant com MQTT"** — [Embarcados](https://embarcados.com.br/bancada/101-integrando-o-esp32-ao-home-assistant-com-mqtt/)
- **Curto Circuito**: "Monitoramento e Controle por Aplicativo – MQTT" e "Como testar um Servo Motor" — [Curto Circuito MQTT](https://curtocircuito.com.br/blog/Categoria%20IoT/monitoramento-e-controle-por-aplicativo-mqtt); [Curto Circuito servo](https://curtocircuito.com.br/blog/servo-motor/como-testar-um-servo-motor)
- **Máquina de vendas Pix com ESP32** (README em português, referência de arquitetura) — [eduardowakim-lab](https://github.com/eduardowakim-lab/maquina-vending-esp32)
- Em inglês, mas muito didáticos para iniciantes:
  - ESP32 Servo Web Server — [RNT](https://randomnerdtutorials.com/esp32-servo-motor-web-server-arduino-ide/)
  - ESP32 MQTT — [RNT](https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/)
  - Access Point Web Server — [RNT](https://randomnerdtutorials.com/esp32-access-point-ap-web-server/)
  - ESP32 MQTT — [esp32io](https://esp32io.com/tutorials/esp32-mqtt)
  - ESP32 Servo — [esp32io](https://esp32io.com/tutorials/esp32-servo-motor)

### Inferences
- Trilha sugerida para iniciantes:
  1. RNT servo web server (move o servo pelo celular na mesma rede);
  2. RNT Access Point (sem roteador);
  3. se for usar MQTT, o Embarcados ESP32-C6 MQTT em português;
  4. só então QR no display (ESP_QRcode / GxEPD2).

### Gaps
- Buscas com filtro em makerhero.com, blog.eletrogate.com e usinainfo.com.br não trouxeram tutoriais de ESP32 + MQTT + servo ou ESP32 + e-paper. Pode haver conteúdo que o buscador não indexou. Vale procurar direto nos sites (ex.: "Eletrogate e-paper ESP32", "MakerHero ESP32 servo").
- Não localizei vídeos no YouTube em português sobre ESP32 + QR + servo com código aberto.

---

## 6. Recomendação: projetos-modelo e as 10 principais lições para o MVP

### Takeaway
Usar como **modelo principal o kishoreSpandiyan/smart-security-tag** (mesmo conceito, MIT, pagamento simulado, código ESP32 + Flask) e como **base mínima de firmware o tutorial RNT "ESP32 Servo Motor Web Server"** (tudo dentro do ESP32, sem backend). A **maquina-vending-esp32** fica como referência para explicar a versão com Pix real e o fallback MQTT→HTTP. Nenhum dos três traz 3D: a trava impressa é trabalho da equipe.

### Cited Findings
- smart-security-tag: ESP32 + servo + buzzer + Flask + página "Pay Now" que destrava por HTTP; MIT — [GitHub](https://github.com/kishoreSpandiyan/smart-security-tag)
- RNT Servo Web Server: página servida pelo próprio ESP32 controla o servo; ESP32Servo; código gratuito — [Random Nerd Tutorials](https://randomnerdtutorials.com/esp32-servo-motor-web-server-arduino-ide/)
- maquina-vending-esp32: webhook Mercado Pago → Cloudflare → MQTT/TLS → ESP32, com fallback de polling HTTP — [GitHub](https://github.com/eduardowakim-lab/maquina-vending-esp32)
- Levantosina/ESP32-MQTT-Servo-Control: exemplo de servo + MQTT testado no simulador Wokwi — [GitHub](https://github.com/Levantosina/ESP32-MQTT-Servo-Control)

### Inferences
**Arquitetura sugerida em camadas de risco (a demo precisa funcionar mesmo se as camadas de cima falharem):**
- **Nível 1, obrigatório:** o ESP32 conecta ao hotspot do celular da equipe (ou cria a própria rede AP) e serve a página `/pagar`. O QR na tela aponta para essa URL. O botão "Pagar" chama `/unlock`, o servo gira e o LED fica verde. Sem nuvem, sem broker. É a base do RNT servo web server.
- **Nível 2, desejável:** notebook no mesmo hotspot rodando Flask (como o smart-security-tag) + Mosquitto local. A página "paga", o backend registra e publica `unlock` no MQTT, e o ESP32 destrava. Mostra a separação "pagamento ↔ etiqueta" do produto real.
- **Nível 3, apresentação:** slide com a arquitetura real (Pix Mercado Pago → webhook → servidor → MQTT → etiqueta), citando a máquina de vendas brasileira como prova de viabilidade.

**Top 10 lições para o MVP Tag&Go:**
1. **Copie o fluxo do smart-security-tag e a base do RNT servo web.** Não comece do zero nem por uma stack pesada (Flutter/Node/MongoDB como o smartlocker).
2. **Servo x brownout:** capacitor de 470–1000 µF perto do ESP32, servo alimentado pela bateria/5 V e não pelo 3,3 V, GND comum. Teste o destravamento **rodando na bateria**, não no USB.
3. **Não use o Wi-Fi da universidade nem de eventos** (eduroam/WPA2-Enterprise instável no ESP32; portal cativo não funciona). Leve um celular dedicado como hotspot 2.4 GHz, com SSID e senha fixos no firmware, e tenha o modo AP como plano B.
4. **Página web, não Bluetooth.** Web Bluetooth não funciona no Safari do iPhone. O QR deve abrir uma URL que funcione em qualquer celular.
5. **Evite depender de broker público na demo.** Mosquitto local no notebook ou HTTP direto ao ESP32. Se usar broker público, tópico único e fallback para HTTP (padrão da máquina de vendas).
6. **Fail-secure + override local.** A etiqueta continua travada sem rede (o contrário do lockbox), mas tem um destravamento de emergência (botão escondido ou sequência) para nunca "prender" a peça do avaliador.
7. **QR estático, grande e curto.** URL curta, QR ampliado (2× no OLED), fundo claro com margem. No e-paper, desenhe uma vez no boot (a atualização de 2–4 s não importa). Teste com iPhone e Android na luz da sala.
8. **Pagamento simulado.** O Pix do Mercado Pago em sandbox só é testável por API (APRO), não por um pagamento ao vivo no celular. Mostre a integração real só como arquitetura.
9. **Bateria e sobressalentes.** Wi-Fi ativo consome da ordem de 100–200 mA e a placa de desenvolvimento gasta mA até dormindo. Não otimize sono no MVP: leve baterias carregadas extras, um power bank e um cabo USB para rodar na tomada se preciso.
10. **Simule e ensaie antes.** Valide a lógica no Wokwi, faça um ensaio completo no local e horário da apresentação com os celulares que serão usados, e grave um vídeo de backup da demo funcionando.

### Gaps
- Faltam fontes sobre arquivos 3D de trinco/lingueta por servo (Printables/Thingiverse) e sobre o tamanho mínimo de carcaça para ESP32 + bateria + servo 9 g. Vale uma busca dedicada.
- A lição 10 (ensaio e vídeo de backup) é boa prática geral, não veio de uma fonte específica.
- O custo das peças no Brasil (ESP32, e-paper 2.13", SG90, LiPo) frente ao orçamento de R$ 600 não foi pesquisado aqui.
