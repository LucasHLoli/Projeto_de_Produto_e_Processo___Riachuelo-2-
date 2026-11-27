# Um ESP32 a pilhas destrava o Tag&Go

O MVP mínimo do Tag&Go é um **ESP32 DevKit com os pinos já soldados**, alimentado por **4 pilhas AA recarregáveis (NiMH) num suporte com chave**, que comanda um **micro servo MG90S**. O servo empurra uma **lingueta com mola impressa em PETG**, e é essa lingueta que prende um **prego de aço de 4 mm com uma ranhura**. O cliente aponta a câmera do celular para um QR e abre uma página estática no GitHub Pages. Lá ele faz um pagamento simulado (Pix ou cartão), e a página manda o comando de destravar por um **broker MQTT público** (HiveMQ, com o EMQX de reserva). Esse é o único caminho sem app que funciona igual no iPhone e no Android, porque o Safari não tem Web Bluetooth. Quanto à tela, **ela não precisa ficar ligada**: um e-paper mantém o QR sem gastar energia. O OLED, ao contrário, apaga quando desliga e mostra um QR pequeno demais. Por isso o MVP usa **um QR impresso como base**, e o e-paper de 1,54" entra como melhoria: vale encomendar já, mas um atraso na entrega não derruba a demo. As peças somam **entre R$ 380 e R$ 540**, já com placa e servo de reserva. Não há ferro de solda, bateria de lítio nem servidor próprio. O cronograma deixa o núcleo funcionando na protoboard até o fim de outubro e a etiqueta montada na carcaça no começo de novembro. As semanas finais ficam para ensaios. Os três riscos que mais derrubam demos parecidas são o reset do ESP32 quando o servo arranca, o Wi-Fi da universidade e o broker público fora do ar. Os três têm prevenção barata e plano B.

## Oito escolhas fecham a arquitetura sem solda e sem servidor

O MVP tem quatro blocos físicos: placa, energia, trava e sinalização. Tem também dois blocos na web: a página de pagamento e o broker, que leva a mensagem da página até a etiqueta. As notas de pesquisa discordam em vários pontos. A tabela abaixo fixa uma posição para cada um, sempre pelo critério do enunciado: alunos sem experiência em eletrônica, nada de solda, R$ 600 de orçamento e uma demo que não pode falhar em 07/12/2026.

| Divergência nas notas | Posição para o MVP | Por quê, em uma frase |
|---|---|---|
| MQTT público × página servida pelo próprio ESP32 | Página no GitHub Pages + broker MQTT público (HiveMQ, reserva EMQX). A página servida pelo ESP32 fica como plano B offline | É o único caminho em que qualquer celular abre a página só lendo o QR, no 4G e sem trocar de Wi-Fi. A página local obriga o cliente a entrar na rede da etiqueta, o que é frágil no iPhone |
| e-paper × OLED × adesivo | QR impresso como base, e-paper 1,54" preto e branco como melhoria, OLED não | O impresso é o que lê melhor e não gasta nada. O e-paper é a única tela que mantém o QR sem energia. O OLED apaga e mostra um QR pequeno demais |
| ESP32 DevKit × ESP32-C3 | ESP32 DevKit (WROOM-32) com pinos soldados, duas unidades | O DevKit dispensa solda, aceita as 4 pilhas direto no VIN e é a placa dos tutoriais e do exemplo do e-paper. O C3 exige soldar bateria ou pinos |
| LiPo × pilhas AA × power bank | 4 pilhas AA NiMH num suporte com chave. Power bank só como reserva | Sem carregador nem conversor dentro da caixa impressa, não há nada para calibrar e nada que possa pegar fogo |
| Servo × solenoide | Micro servo MG90S de 180°, com um SG90 de reserva | O servo liga com três fios. O solenoide exige MOSFET, diodo e picos de 2 A |
| Lingueta com mola × braço do servo direto na ranhura | Lingueta com mola, que o servo só empurra para abrir | A mola trava sozinha e o puxão vai para as paredes da caixa, não para as engrenagens do servo |
| Pino EAS comercial × prego com ranhura | Prego ou vergalhão de aço de Ø4 mm com uma ranhura | O pino EAS, de cerca de 1,2 mm, é fino demais para uma lingueta de plástico |
| Nonce dentro do QR × nonce guardado no broker | Nonce publicado como mensagem retida no broker. O nonce no QR só entra se o e-paper entrar | Dá a mesma proteção de uso único com um QR impresso |

### A placa DevKit e quatro pilhas AA dispensam ferro de solda

A placa recomendada é um **ESP32 DevKit (módulo ESP32-WROOM-32) vendido com os pinos já soldados**, como o DevKitC S1 da Eletrogate, por **R$ 59,90** ([Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-devkitc-s1)). Ela recebe 5 V pelo regulador da própria placa. A lógica é de 3,3 V, os pinos (GPIOs) **não toleram 5 V**, e o Wi-Fi funciona **só em 2,4 GHz** ([Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-38-pinos-usb-tipo-c)).

O ESP32-C3 perde por um motivo prático. O XIAO ESP32-C3 consome só 44 µA dormindo e já tem carregador de bateria de lítio, mas a bateria se liga em pontos que precisam de solda, e os pinos vêm soltos ([Seeed](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)). O C3 SuperMini gasta cerca de 600 µA dormindo, 90% disso só no LED de energia, e não é um projeto oficial da Espressif ([Random Nerd Tutorials](https://randomnerdtutorials.com/getting-started-esp32-c3-super-mini/)). O C3 serve para uma versão 2 menor, não para este MVP. Comprem **duas placas iguais** e gravem o mesmo firmware na segunda, para ter uma reserva pronta.

A energia vem de **4 pilhas AA NiMH num suporte fechado com chave liga/desliga**. O regulador AMS1117 do DevKit precisa de um pouco mais de 4,5 V na entrada VIN. Quatro NiMH dão 4,8 V nominais e cerca de 5,6 V logo depois da recarga, o que fica "perto do limite" ([Arduino Forum](https://forum.arduino.cc/t/esp32-using-4-aa-batteries/1219432)). Por isso a regra é começar a demo com pilhas recém-carregadas e levar um segundo jogo, que se troca em 30 segundos. Três pilhas não bastam. A mesma pilha alimenta o servo diretamente, sem conversor no meio.

A alternativa com bateria de lítio (LiPo), carregador TP4056 e conversor elevador MT3608 é menor, mas traz três problemas:

| Problema da rota LiPo | Detalhe |
|---|---|
| Calibração obrigatória | O MT3608 é ajustável até 28 V e precisa ser calibrado com multímetro antes de ligar qualquer coisa ([Eletrogate](https://www.eletrogate.com/regulador-de-tensao-ajustavel-mt3608-auto-boost-step-up)) |
| Solda | Os módulos têm pontos de solda |
| Risco de incêndio | Uma bateria de lítio furada por um parafuso dentro da carcaça pode pegar fogo ([Adafruit](https://learn.adafruit.com/li-ion-and-lipoly-batteries/conclusion)) |

O power bank fica só como reserva, porque muitos desligam sozinhos quando a corrente consumida é baixa ([aeq-web](https://www.aeq-web.com/arduino-nodemcu-esp-powerbank-dummyload-automatic-shutdown-problem/)).

A conta de energia tem folga. Com o Wi-Fi conectado e em repouso (modem sleep), o ESP32 clássico gasta de 30 a 68 mA, com picos de 180 a 240 mA quando transmite ([Last Minute Engineers](https://lastminuteengineers.com/esp32-sleep-modes-power-consumption/)). Somando placa, LED e servo parado, a média fica entre 90 e 150 mA. Assim, **4 horas de demo com cerca de 50 destravamentos consomem de 360 a 600 mAh**, entre um quarto e um terço de um jogo de NiMH de 2000 mAh. O servo gasta menos de 10 mAh no dia inteiro. O ponto fraco do DevKit é o consumo dormindo: o regulador e o chip USB puxam de 5 a 11 mA mesmo em deep sleep ([Hubble](https://hubble.com/community/guides/esp32-deep-sleep-current-what-the-datasheet-says-vs-what-you-ll-actually-measure/)), o que esgotaria as pilhas em 6 a 7 dias. No MVP isso não pesa: o Wi-Fi fica ligado durante a demo, para destravar na hora, e a chave do suporte fica desligada entre os ensaios.

### O celular fala com a etiqueta por um broker MQTT, não por Bluetooth

O requisito "sem app, no iPhone e no Android" elimina o Bluetooth. Em agosto de 2026, o Safari do iOS continua **sem Web Bluetooth**, e o único jeito de contornar isso é instalar uma extensão ou outro navegador ([caniuse](https://caniuse.com/web-bluetooth)). O Web NFC só existe no Chrome do Android ([caniuse](https://caniuse.com/webnfc)). Sobra a web.

Uma página hospedada no GitHub Pages usa HTTPS e, por isso, só consegue abrir conexões seguras do tipo `wss://` ([MQTT.js](https://github.com/mqttjs/MQTT.js)). Ela não pode chamar o ESP32 direto em `http://192.168.x.x` por dois motivos. Primeiro, o navegador bloqueia conteúdo misto, isto é, uma página segura chamando um endereço sem segurança ([MDN](https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content)). Segundo, desde a versão 142 o Chrome pede permissão para acessar a rede local ([Chrome for Developers](https://developer.chrome.com/blog/local-network-access)). O intermediário mais simples é um broker MQTT público, um servidor gratuito que repassa mensagens entre a página e a etiqueta.

```
[QR na etiqueta] --câmera--> https://usuario.github.io/tg/?t=K7Q9-3FXA
                             (Safari ou Chrome, no 4G ou em qualquer Wi-Fi)

Página (mqtt.js) --wss://broker.hivemq.com:8884/mqtt--> [broker público] <--TCP 1883-- ESP32 DevKit
  assina  taggo/K7Q9-3FXA/state (estado retido + nonce)                                 (hotspot 2,4 GHz)
  publica taggo/K7Q9-3FXA/cmd   {"c":"unlock","n":"a91f3c"}                              LED, servo, lingueta
```

A página usa a biblioteca mqtt.js pelo endereço `wss://broker.hivemq.com:8884/mqtt`. O ESP32 conversa com o mesmo broker pela porta TCP **1883, sem criptografia e sem certificado** ([HiveMQ](https://www.mqtt-dashboard.com/)). Isso elimina o erro mais comum de quem está começando, que é justamente configurar certificados. O HiveMQ não garante que o serviço fique no ar, então o firmware e a página usam o **EMQX como reserva** (`wss://broker.emqx.io:8084/mqtt` na página e `broker.emqx.io:1883` no ESP32) ([EMQX](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)).

A página é um único arquivo `index.html` num repositório público, com o GitHub Pages ligado. É gratuito, e cada mudança leva até 10 minutos para ser publicada ([GitHub Docs](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)). Fixem o mqtt.js na versão 5 e copiem o arquivo para dentro do repositório, para não depender de outro site no dia da demo.

O ESP32 se conecta ao **hotspot de 2,4 GHz do celular de alguém da equipe**. No iPhone, a opção "Maximizar compatibilidade" do Acesso Pessoal precisa estar ligada ([SensorPush](https://support.sensorpush.com/hc/en-us/articles/4404419632023-Why-can-t-I-connect-to-the-Personal-Hotspot-on-my-iPhone)). Nunca usem o eduroam: o ESP32 tem falhas conhecidas nesse tipo de rede, e seria preciso gravar no firmware a senha USP de alguém ([arduino-esp32 #5027](https://github.com/espressif/arduino-esp32/issues/5027)). O celular que paga não precisa estar na mesma rede. Basta ter internet, de preferência 4G.

Uma página servida pelo próprio ESP32 é mais simples de programar, mas obriga o celular do cliente a entrar na rede da etiqueta e a ficar sem internet. O melhor portal cativo de código aberto funciona no iPhone e no Android, mas aceita no máximo 4 aparelhos ao mesmo tempo, e alguns celulares precisam desligar os dados móveis para conectar ([CDFER](https://github.com/CDFER/Captive-Portal-ESP32)). Por isso essa página vira o **plano B offline**: o celular do apresentador entra na rede "TagGo-Offline" e abre `http://192.168.4.1`, sem broker e sem internet. Não é trabalho extra. É o primeiro firmware que a equipe vai escrever de qualquer jeito, seguindo o tutorial de servidor web com servo do Random Nerd Tutorials ([RNT](https://randomnerdtutorials.com/esp32-servo-motor-web-server-arduino-ide/)).

A segurança do MVP é simples e deve ser apresentada com honestidade. Cada etiqueta tem um ID aleatório de 8 caracteres, que vira o nome do tópico (`taggo/K7Q9-3FXA/...`). O protocolo funciona assim:

| Etapa | Quem age | O que acontece |
|---|---|---|
| 1 | ESP32 | Ao ligar e depois de cada venda, sorteia um código de uso único (nonce) com `esp_random()`. A função só gera números de fato aleatórios com o Wi-Fi ligado ([Espressif](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/random.html)) |
| 2 | ESP32 | Publica o nonce como mensagem retida em `.../state`. O broker guarda essa mensagem e a entrega a quem conectar depois |
| 3 | Página | Ao abrir, recebe o nonce |
| 4 | Página | Depois do pagamento, publica `{"c":"unlock","n":"<nonce>"}` em `.../cmd` |
| 5 | ESP32 | Só aceita se o nonce bater. Destrava, responde `{"s":"unlocked"}` e sorteia outro nonce |
| 6 | Página | Só mostra "Liberado" depois dessa resposta. Sem resposta em cerca de 5 s, tenta mais uma vez e depois mostra erro |

Esse esquema bloqueia comandos acidentais, mensagens repetidas e brincadeiras. Mas não é criptografia: num broker público, "qualquer um pode estar ouvindo" ([test.mosquitto.org](https://test.mosquitto.org/)). Na apresentação, digam que no produto real o comando seria assinado pelo sistema de pagamento.

O pagamento é uma tela feita pela própria equipe, com uma faixa fixa: "Demonstração — nenhum pagamento real é processado". O cliente escolhe entre Pix (um QR ilustrativo e o botão "Simular confirmação do Pix") e cartão (com um número de teste já preenchido). Depois vêm 1,5 s de "Processando…" e o comando de destravar. Pix de verdade não cabe no MVP. No ambiente de testes do Mercado Pago, o Pix "não pode ser testado por compras simuladas", só por uma chamada de API ([Mercado Pago Developers](https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/integration-test/pix)). Além disso, o aviso de pagamento (webhook) exige um servidor público entre o banco e o ESP32, como faz a máquina de vendas brasileira que serve de referência para o slide de "próxima etapa" ([maquina-vending-esp32](https://github.com/eduardowakim-lab/maquina-vending-esp32)). O Stripe em modo de teste redireciona o cliente de volta para a página, mas, sem um servidor para conferir o pagamento, ele continua tão simulado quanto a tela própria ([Stripe](https://docs.stripe.com/payment-links/post-payment)).

### A lingueta com mola trava sozinha e o servo só abre

A trava é uma **lingueta deslizante com mola**, como a de uma porta. Ao entrar, o pino empurra a lingueta pelo chanfro de 45°. A lingueta estala dentro da ranhura, e a etiqueta fica travada **sem energia e sem nenhum comando**. O puxão no pino vai para as paredes impressas, não para o servo. Para abrir, o braço do servo empurra uma aba da lingueta por cerca de 1,5 s, volta à posição de repouso e tem o sinal desligado (o comando `detach`). Um servo comum mantém a posição pelo atrito das engrenagens mesmo sem sinal ([tomservo](https://github.com/ripred/tomservo)).

A força sobra. O MG90S tem torque de 1,8 kgf·cm a 4,8 V ([Eletrogate](https://www.eletrogate.com/micro-servo-towerpro-mg90s-metalico-t-rex)), o que dá cerca de 18 N num braço de 10 mm. Mesmo um SG90 genérico, com 1,2 kgf·cm ([Usinainfo](https://usinainfo.com.br/servo-motores/micro-servo-motor-9g-sg90-180-2299.html)), dá cerca de 12 N, contra 3 a 5 N de mola e atrito. Comprem servos **de 180°**, porque também se vendem versões de rotação contínua, que não servem ([Saravati](https://www.saravati.com.br/micro-servo-motor-mg90s-2-2kg-cm-engrenagens-de-metal-360.html)). E não usem varetas entre o servo e a trava: a caixa com trava IoT de rubenwardy falhou justamente com um servo ligado por vareta e com uma garra sob carga ([rubenwardy](https://blog.rubenwardy.com/2023/03/16/lockbox/)).

O pino não é o de uma etiqueta comercial. Os pinos antifurto comerciais (EAS) têm haste de cerca de 1,2 mm e ranhuras rasas, feitas para uma garra de esferas de aço que segura até 80 lbf, cerca de 356 N ([US9053623B2](https://patents.google.com/patent/US9053623B2/en)). Uma lingueta de plástico escorregaria nesse pino. Usem um **prego ou vergalhão de aço de Ø4 mm com uma ranhura de degrau reto** (núcleo de Ø2,5 mm e largura de 4 mm). Dá para fazer a ranhura girando o prego preso na furadeira contra uma lima. Uma arruela de EVA de 2 a 3 mm sob a cabeça do prego compensa a espessura do tecido. A meta honesta do MVP é aguentar **50 N**, um puxão firme, e não os 356 N do produto comercial.

As demais peças da trava:

| Peça | Especificação |
|---|---|
| Mola | De caneta, de metal. Molas impressas em PLA deformam com o tempo e perdem força ([Hackaday](https://hackaday.com/2026/04/27/the-challenges-of-3d-printing-reliable-springs/)) |
| Lingueta | PETG, impressa deitada, 100% de preenchimento, 30 × 8 × 3 mm, curso de 4 mm |
| Canal da lingueta | Folga de 0,3 mm ([Snapmaker](https://www.snapmaker.com/blog/3d-printing-tolerances/)) |
| Reservas | Imprimam três linguetas a mais |

Nenhum modelo 3D pronto de trava de etiqueta foi encontrado. Esta é a parte original do projeto e também a mais arriscada. As referências mais próximas são o trinco com mola e servo "Geocache Box Servo Latch" ([Printables](https://www.printables.com/model/134411-servo-latch-geocache-box-servo-latch)) e o "Servo-Lock" de 12 peças ([MyMiniFactory](https://www.myminifactory.com/object/3d-print-servo-lock-365536)).

Ficam duas consequências de projeto. A primeira: a etiqueta continua travada quando perde a rede. É o oposto da caixa de entregas benjskinner, que se abre sozinha depois de 8 s sem conexão ([esp32-smart-lockbox](https://github.com/benjskinner/esp32-smart-lockbox)). A segunda: ela será maior que uma etiqueta real. O suporte de 4 pilhas mede 65 × 70 × 20 mm ([Fermarc](https://www.fermarc.com/produto/suporte-para-4-pilhas-aa-com-chave-ligadesliga)), quase toda a caixa de 90 × 70 mm que o mecanismo pede. A solução é uma cápsula de pilhas presa por baixo ou uma caixa mais comprida. Meçam as peças reais antes de modelar. A tampa presa com 4 parafusos M3 faz duas funções: impede que o cliente abra a etiqueta e permite que a equipe a abra numa emergência.

## A tela não precisa ficar ligada: o e-paper guarda o QR com energia zero

A resposta direta: **não, a tela não precisa ficar ligada, desde que seja um e-paper**. O e-paper (a mesma tecnologia dos leitores de livro digital) mantém a imagem sozinho. Depois de desenhado, o QR continua visível com a placa dormindo, ou mesmo com a chave das pilhas desligada. O módulo de 1,54" (200 × 200 pixels) gasta menos de 0,01 µA parado e cerca de 26 mW durante os cerca de 2 s de atualização ([Waveshare](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_Manual)). A biblioteca GxEPD2 registra 2,6 s para uma atualização completa ([GxEPD2](https://github.com/ZinggJM/GxEPD2)). Cada QR novo custa cerca de 0,006 mAh, nada perto do Wi-Fi. O que precisa ficar ligado na demo é o rádio do ESP32, não a tela.

O OLED funciona ao contrário. Ele só mostra imagem enquanto está energizado, e a corrente cresce com o número de pixels acesos: cerca de 1,4 mA com a tela apagada, mais 0,054 mA por ponto percentual de pixels acesos ([hsel.co.uk](https://hsel.co.uk/2018/12/04/ssd1306-power-consumption/)). Com só 64 pixels de altura, o maior QR que cabe mede cerca de 10 mm no OLED de 0,96". Isso fica abaixo dos cerca de 2 × 2 cm que os celulares leem com folga ([useqrkit](https://useqrkit.com/blog/qr-code-minimum-size)). Há ainda relatos de pixels marcados (burn-in) depois de 2 a 4 meses exibindo a mesma imagem ([esphome #624](https://github.com/esphome/feature-requests/issues/624)).

| | e-paper 1,54" P&B | OLED 0,96" | QR impresso |
|---|---|---|---|
| Mantém o QR sem energia | Sim | Não, apaga | Sim |
| Consumo para exibir | ~0 (só ~2,6 s por QR novo) | 1,4 a 7 mA enquanto aceso | 0 |
| Tamanho do QR | 18 a 20 mm | cerca de 10 mm | 25 a 30 mm |
| Fios até a placa | 8 (SPI, 3,3 V) | 4 (I2C) | 0 |
| Preço | ≈ R$ 55–65 no AliExpress; R$ 153,89 na Amazon.com.br | R$ 26,90 na Eletrogate | quase zero |
| Mostra "PAGO – LIBERADA" na etiqueta | Sim | Sim, enquanto aceso | Não (o LED faz esse papel) |
| Principal risco | Prazo de entrega, fita flexível frágil, pino BUSY | QR pequeno, marca na tela | Nenhum |

Os preços da tabela vêm de [AliExpress WeAct](https://www.aliexpress.com/item/1005006291142235.html), [Amazon.com.br](https://www.amazon.com.br/polegadas-Interface-compat%C3%ADvel-eletr%C3%B4nico-prateleira/dp/B072Q4WTWH) e [Eletrogate](https://www.eletrogate.com/display-oled-128x64-0.96-i2c-branco).

A posição para o MVP é esta: **QR impresso como base, e-paper de 1,54" preto e branco como melhoria, OLED não**. O QR impresso, com 2,5 a 3 cm e margem branca, é o que lê mais rápido e não depende de código. Com o protocolo do nonce guardado no broker, ele já dá à etiqueta a proteção de uso único. O LED RGB informa o estado: travada, liberada ou sem conexão. O e-paper é a única tela que atende à ideia da equipe sem custo de energia. Encomendem agora; se ele chegar até o início de novembro, entra na etiqueta. Se não chegar, a demo não muda. Mesmo com a tela funcionando, colem um QR impresso no verso da etiqueta.

Se a tela entrar, estes são os cuidados:

| Cuidado | Detalhe |
|---|---|
| Qual módulo | WeAct 1,54" preto e branco (controlador SSD1681). No código, a classe é `GxEPD2_154_D67`, e os pinos são os do exemplo oficial da WeAct ([WeAct](https://github.com/WeActStudio/WeActStudio.EpaperModule/blob/master/Example/EpaperModuleTest_Arduino_ESP32/EpaperModuleTest_Arduino_ESP32.ino)) |
| Tensão | Só 3,3 V. Nunca ligar a tela em 5 V ([GxEPD2](https://github.com/ZinggJM/GxEPD2)) |
| Atualização | Completa a cada QR novo. A parcial só para a linha de status. Chamar `display.hibernate()` depois de cada desenho |
| Biblioteca de QR | Renomear os arquivos da biblioteca QRCode, que têm o mesmo nome de um arquivo interno do ESP32 ([ricmoo/QRCode #35](https://github.com/ricmoo/QRCode/issues/35)) |
| Tamanho da URL | Até 53 caracteres, para caber num QR de versão 3 ([ricmoo/QRCode](https://github.com/ricmoo/QRCode)). `https://usuario.github.io/tg/?t=K7Q9-3FXA` tem 41 |
| Cores | Preto e branco. As telas de 3 cores atualizam bem mais devagar |
| Primeiro teste | Se nada aparece na tela, confiram primeiro o fio do pino BUSY |

Com a tela, dá também para colocar o nonce dentro do próprio QR e redesenhá-lo depois de cada venda. É o "QR dinâmico": um print de um QR antigo deixa de funcionar.

## Cerca de R$ 380 a R$ 540 compram tudo, com placa e servo de reserva

A lista abaixo cobre uma etiqueta completa, mais uma placa e um servo de reserva. Os cinco primeiros itens têm preço lido na loja (somam **R$ 202,42**). O e-paper tem preço de anúncio ainda não conferido no carrinho. As linhas marcadas como estimativa **não têm preço verificado** e precisam ser conferidas antes da compra.

| Item | Qtd | Onde | Preço | Subtotal |
|---|---|---|---|---|
| ESP32 DevKitC (WROOM-32), pinos soldados | 2 (1 de reserva) | [Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-devkitc-s1) | R$ 59,90 (R$ 56,90 no Pix) | R$ 119,80 |
| Micro servo MG90S, engrenagem metálica, 180° | 1 | [WJ Componentes](https://www.wjcomponentes.com.br/servo-90g) | R$ 25,27 | R$ 25,27 |
| Micro servo SG90, 180° (reserva) | 1 | [Eletrogate](https://www.eletrogate.com/micro-servo-9g-sg90-towerpro) | R$ 14,90 | R$ 14,90 |
| Suporte 4×AA com chave + 4 pilhas (servem de jogo de emergência) | 1 | [PowerVolt](https://www.powervolt.com.br/produtos/suporte-para-4-pilhas-aa-com-chave-liga-desliga-4-pilhas/) | R$ 30,55 | R$ 30,55 |
| Protoboard de 830 pontos | 1 | [Eletrogate](https://www.eletrogate.com/categorias) | R$ 11,90 | R$ 11,90 |
| e-paper 1,54" 200×200 P&B WeAct (SSD1681) | 1 | [AliExpress WeAct](https://www.aliexpress.com/item/1005006291142235.html) | cerca de US$ 8–9 + ICMS | ≈ R$ 55–65 |
| 8 pilhas AA NiMH + carregador | 1 kit | loja local | estimativa | R$ 80–150 |
| Kit de jumpers macho-macho, macho-fêmea e fêmea-fêmea | 1 | loja local | estimativa | R$ 20–30 |
| LED RGB de catodo comum (ou módulo) + 3 resistores de 220–330 Ω + botão + microchave de alavanca | 1 de cada | loja local | estimativa | R$ 10–15 |
| Capacitor eletrolítico 1000 µF / 16 V | 3 | loja local | estimativa | R$ 5 |
| Prego ou vergalhão de aço Ø4 mm, folha de EVA, parafusos M3, arruelas M4 | — | loja de ferragens | estimativa | R$ 10–20 |
| Multímetro | 1 | loja local ou emprestado do laboratório | estimativa | R$ 0–50 |
| Mola de caneta, filamento PETG/PLA (menos de 100 g), cabo USB-C de dados, power bank, 2 celulares para hotspot | — | já disponíveis | — | — |
| **Total** | | | | **≈ R$ 380–540** |

A faixa de preço depende de a equipe já ter multímetro e pilhas recarregáveis. No pior caso, sobram cerca de R$ 60 para frete e imprevistos. Comprem no Brasil, esta semana, tudo o que é crítico. O AliExpress fica só para o e-paper, que não é crítico. Em maio de 2026, a MP 1.357/2026 zerou o imposto federal de importação para compras de até US$ 50 no programa Remessa Conforme, mas o ICMS continua sendo cobrado. A MP também precisava ser votada pelo Congresso em 120 dias ([Agência Senado](https://www12.senado.leg.br/noticias/materias/2026/05/13/medida-provisoria-zera-taxa-das-blusinhas-para-importacoes-de-ate-us-50)). Esse prazo venceu por volta de setembro, então confiram o imposto na tela de pagamento. Se o e-paper não chegar e a equipe ainda quiser a tela, a unidade vendida no Brasil (R$ 153,89) só cabe no orçamento se o multímetro for emprestado e alguém já tiver as pilhas NiMH. Se algum anúncio disser "pinos não soldados", escolham outro.

## A pilha alimenta a placa e o servo em paralelo; todo o resto é 3,3 V

O único ponto de atenção elétrica é a distribuição de energia. As pilhas vão para a placa e para o servo **em paralelo**, com um capacitor grande junto ao servo e todos os fios de terra (GND) ligados entre si. Assim, o pico de corrente do servo não passa pelo regulador da placa. Todo o resto (tela, LED, botão) funciona em 3,3 V.

```
[4×AA NiMH + chave] (+) ──┬── VIN (ou 5V) do ESP32
                          ├── servo, fio vermelho
                          └── capacitor 1000 µF, perna (+)
                    (−) ──┴── GND do ESP32 = servo marrom = capacitor (faixa) = LED = botão = e-paper
ESP32 3V3 ──────────────────── e-paper VCC   (nada mais usa 3V3 como alimentação)
```

| Componente e fio | Liga em | Cuidado |
|---|---|---|
| Suporte de pilhas, fio vermelho (+), depois da chave | Trilho + da protoboard (o "barramento da pilha") | Só pilhas NiMH, cerca de 5,6 V quando carregadas |
| Suporte de pilhas, fio preto (−) | Trilho − (GND) | |
| Trilho + | Pino **VIN** (placa de 30 pinos) ou **5V** (DevKitC) | **Nunca** no 3V3 |
| Trilho − | Pino **GND** da placa | Terra comum para tudo |
| Capacitor 1000 µF, perna + | Trilho +, ao lado do fio vermelho do servo | A faixa marca o negativo. Ligado ao contrário, o capacitor pode estourar |
| Capacitor 1000 µF, perna − (faixa) | Trilho − | |
| Servo, fio vermelho | Trilho + | Direto da pilha, não da placa |
| Servo, fio marrom | Trilho − | |
| Servo, fio laranja (sinal) | **GPIO 13** | Biblioteca ESP32Servo |
| LED RGB, pernas R / G / B | **GPIO 25 / 26 / 27**, cada perna com um resistor de 220–330 Ω | Um módulo de LED dispensa os resistores |
| LED RGB, perna comum (catodo) | GND | |
| Botão | **GPIO 33** e GND | `INPUT_PULLUP`. Segurar por 3 s liga o modo offline |
| Microchave "pino presente" (opcional) | **GPIO 32** e GND | `INPUT_PULLUP`. O pino aperta a microchave no fim do curso |
| e-paper VCC / GND | **3V3** / GND | Nunca 5 V |
| e-paper DIN (SDA) / CLK (SCL) | **GPIO 23 / GPIO 18** | Barramento SPI padrão (VSPI) |
| e-paper CS / DC / RST / BUSY | **GPIO 5 / 17 / 16 / 4** | Sigam os `#define` do exemplo da WeAct (o comentário do arquivo tem DC e RST trocados) |
| USB-C da placa | Notebook (para gravar) ou power bank (reserva) | Desliguem a chave das pilhas antes de ligar o USB |

Os números de GPIO são os mesmos nas placas de 30 e de 38 pinos. Evitem estes pinos: 6 a 11 (ligados à memória flash), 34 a 39 (só entrada, sem resistor interno) e 0, 2 e 12 (interferem no boot). O GPIO 32 da microchave foi escolhido por estar livre e ter resistor interno; as notas não fixavam um pino para ela.

A proteção contra o reset por queda de tensão (brownout) segue a receita documentada: um capacitor de 470 a 1000 µF perto da carga, o motor com alimentação própria e terra comum ([ESPBoards](https://www.espboards.dev/troubleshooting/issues/power/esp32-brownout-reset/)). Mesmo um único SG90 passa do limite do regulador da placa ([Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/powering-sg90-servo-from-arduino-direct-5v-rail-design-guide)).

Na montagem, a protoboard serve só como barramento da pilha. O DevKit é largo, então liguem jumpers fêmea-fêmea direto dos pinos da placa aos módulos. Montem tudo com a chave desligada e confiram a polaridade com o multímetro antes de ligar. Dentro da carcaça, colem ou prendam com fita cada jumper, porque conector solto é a falha mais comum quando a etiqueta passa de mão em mão.

No firmware, o servo segue sempre a mesma sequência: `attach`, mover, esperar 1,5 s, voltar ao repouso, esperar 400 ms e `detach`. E nunca mover o servo no mesmo instante em que o Wi-Fi está conectando.

## Sete passos levam do QR ao pino solto

| Passo | O que a pessoa faz | O que a etiqueta e a página fazem |
|---|---|---|
| 0. Ligar | A equipe liga a chave das pilhas | O ESP32 entra no hotspot, conecta ao broker, sorteia o nonce e publica o estado retido. O LED pisca azul e depois fica vermelho fixo (travada e online). Com e-paper, a tela mostra o QR e "TRAVADA" |
| 1. Prender | O vendedor empurra o pino pela peça até ouvir o clique | A lingueta entra na ranhura sozinha. A microchave (opcional) confirma que o pino está presente |
| 2. Ler | O cliente aponta a câmera do iPhone ou do Android para o QR | O celular abre `https://usuario.github.io/tg/?t=K7Q9-3FXA` no Safari ou no Chrome, sem app |
| 3. Conferir | O cliente vê o produto e o preço | A página conecta ao broker, recebe o estado retido e mostra "Etiqueta conectada". Se a etiqueta estiver fora do ar, mostra "Etiqueta offline" |
| 4. Pagar | Toca em "Pagar", escolhe Pix ou cartão (simulados) e confirma | Mostra "Processando…" por 1,5 s e publica `{"c":"unlock","n":"<nonce>"}` |
| 5. Liberar | Espera o LED ficar verde, sem puxar | O ESP32 confere o nonce, acende o verde, gira o servo cerca de 40°, segura por 1,5 s, volta ao repouso, publica `{"s":"unlocked"}` e sorteia outro nonce. Com e-paper, a tela mostra "PAGO – LIBERADA" |
| 6. Soltar | Lê "Pagamento aprovado · Etiqueta liberada" e puxa o pino | A página só mostra essa frase depois da confirmação da etiqueta. Sem resposta em cerca de 5 s, tenta mais uma vez e depois mostra erro. Ao reinserir o pino, a etiqueta trava de novo e o QR antigo não abre mais nada |

O roteiro da demo precisa dizer, com todas as letras, "solte, depois puxe". Se alguém puxar o pino enquanto o servo se move, o atrito aumenta e a lingueta pode não sair.

## Dez semanas bastam se o núcleo funcionar até o fim de outubro

O calendário do próprio grupo (em `prototipo/plano-prototipo.md`) tem o R3 em 04/11, o R4 em 23/11 e uma prova em 25/11. Por isso a construção se concentra em outubro, e as duas últimas etapas antes da demo são só de ensaio. A trava corre **em paralelo** ao firmware desde a primeira semana, porque é a parte sem modelo pronto.

| Etapa | Datas | O que fazer | Pronto quando |
|---|---|---|---|
| 0. Comprar e simular | 29/09–04/10 | Fazer os pedidos no Brasil e o do e-paper no AliExpress. No simulador Wokwi, montar ESP32 + LED + servo + broker público ([Wokwi](https://wokwi.com/projects/381829353297474561)). Criar o repositório com GitHub Pages. Imprimir um teste de folgas de 0,2, 0,3 e 0,4 mm | O LED do Wokwi muda de cor com uma mensagem enviada pelo mqtt-dashboard |
| 1. Placa funcionando | 05/10–11/10 | Piscar o LED RGB, ler o botão e mover o servo (attach/detach). Seguir o tutorial de servo com servidor web do RNT, que vira o plano B. Usar o Arduino Uno como bancada para medir a corrente do servo | O servo se move pelo celular na mesma rede |
| 2. Celular fala com a etiqueta | 12/10–18/10 | Firmware com PubSubClient no hotspot. `index.html` com o mqtt.js 5 salvo no repositório. Testar num iPhone e num Android, no 4G | O LED muda de cor por um celular no 4G do outro lado da sala |
| 3. Trava na bancada | 12/10–25/10 | Imprimir um bloco de teste de 40 × 40 mm com canal, lingueta e furo. Fazer 3 ou 4 pinos com ranhura. Testar puxões de 30, 50 e 100 N com balança de bagagem | 20 inserções e liberações sem marcas na lingueta |
| 4. Fluxo completo | 19/10–01/11 | Pagamento simulado, nonce retido e confirmação. Duas redes cadastradas (WiFiMulti) e broker reserva. Tudo rodando na pilha, não no USB. 100 ciclos de travar e destravar | 100 ciclos na pilha sem nenhum reset |
| 5. Carcaça | 26/10–08/11 | Medir as peças reais, modelar, imprimir em PETG/PLA, montar e colar os jumpers | A etiqueta fechada funciona na mão de alguém que não a montou |
| 6. Extras | 09/11–15/11 | Modo offline pelo botão, e-paper (se chegou), microchave, segunda etiqueta montada | A demo roda sem internet |
| 7. Congelar e ensaiar | 16/11–22/11 | Não mudar mais o firmware. Fazer 20 ensaios completos e medir o tempo de resposta | 20 ensaios seguidos sem falha |
| 8. Ensaio geral | 23/11–06/12 | Ensaiar no local e no horário da demo, com os celulares que serão usados. Gravar o vídeo de reserva. Montar o kit da demo e carregar as pilhas | Vídeo gravado e kit conferido |
| Demo | 07/12 | Pilhas recém-carregadas, hotspot em 2,4 GHz, pagamento feito no 4G | — |

## Reset do servo, Wi-Fi e broker são os riscos, e cada um tem plano B

As falhas mais documentadas em projetos parecidos são quatro: o reset por queda de tensão quando o motor liga, o Wi-Fi corporativo ou com página de login, o broker público fora do ar e o Web Bluetooth no iPhone ([ESPBoards](https://www.espboards.dev/troubleshooting/issues/power/esp32-brownout-reset/); [arduino-esp32 #4229](https://github.com/espressif/arduino-esp32/issues/4229); [HiveMQ](https://www.mqtt-dashboard.com/)). A última já foi eliminada pela arquitetura. As outras e as falhas mecânicas estão na tabela.

| Risco | Como aparece | Prevenção | Plano B no dia |
|---|---|---|---|
| Reset quando o servo arranca | O ESP32 reinicia bem na hora de destravar | Capacitor de 1000 µF, servo direto na pilha, terra comum, testes sempre na pilha. Não desligar o detector de brownout | Power bank no USB-C com as pilhas desligadas; etiqueta reserva |
| ESP32 não entra no Wi-Fi | O LED azul pisca sem parar | Hotspot em 2,4 GHz, "Maximizar compatibilidade" no iPhone, nada de eduroam, dois celulares cadastrados no WiFiMulti | Segundo hotspot; modo offline |
| Broker público fora do ar ou lento | A página mostra "Etiqueta offline" | Dois brokers (HiveMQ e EMQX), com a escolha por parâmetro na URL (`?b=2`) | Modo offline em `http://192.168.4.1` |
| Rede da sala bloqueia a porta 8884 | A página não conecta no Wi-Fi da sala | O celular que paga usa 4G | O mesmo |
| Jumper se solta com o manuseio | Falhas que vêm e vão | Colar ou prender com fita todos os conectores | Etiqueta reserva |
| Lingueta agarra ou deforma | Não trava ou não solta | Folga de 0,3 mm, grafite de lápis no canal, linguetas de reserva, "solte, depois puxe" | Abrir os 4 parafusos e empurrar a lingueta com o dedo |
| Pilhas fracas | Resets, servo sem força | NiMH recém-carregadas, tensão medida com multímetro na manhã da demo | Jogo reserva (30 s para trocar) |
| Servo de rotação contínua comprado por engano | O braço gira sem parar | Conferir "180°" no anúncio | Servo reserva |
| e-paper não chega ou não liga | Tela em branco | Conferir o fio BUSY e renomear a biblioteca de QR | QR impresso (já é a base) |
| Tudo falha | — | — | Mostrar o mecanismo abrindo os parafusos e passar o vídeo gravado |

A ordem dos planos precisa estar ensaiada. O **plano A** é a página no 4G com o broker público. O **plano B** é o celular do apresentador na rede "TagGo-Offline", pagando pela página servida pelo ESP32. O **plano C** é abrir a tampa e mostrar a lingueta, dizendo abertamente o que falhou. O **plano D** é o vídeo. Nenhum destes pontos foi medido por alguma fonte: o tempo de resposta de ponta a ponta, a queda de tensão das pilhas NiMH sob o pico do servo (as fontes divergem entre 250 mA e 1,3 A de corrente com o servo travado) e o comportamento do Safari quando a câmera passa a página para o navegador. Os ensaios da etapa 7 são essa medição. A página deve reconectar sozinha quando volta a ficar visível na tela.

## Um projeto aberto quase idêntico e três tutoriais fazem metade do trabalho

O modelo principal é o **smart-security-tag**: uma etiqueta com ESP32, servo e buzzer, em que o QR abre uma página "Pay Now" com pagamento simulado e um servidor Flask manda o comando de destravar por HTTP. A licença é MIT ([GitHub](https://github.com/kishoreSpandiyan/smart-security-tag)). O Tag&Go do MVP troca o Flask pelo broker público e ganha o nonce, mas o fluxo e a narrativa são os mesmos. Nenhum projeto encontrado traz arquivos 3D de uma trava de etiqueta.

| Projeto | O que é | O que reaproveitar |
|---|---|---|
| [RNT – ESP32 Servo Motor Web Server](https://randomnerdtutorials.com/esp32-servo-motor-web-server-arduino-ide/) | Servidor web no ESP32 que move um servo no GPIO 13 com a ESP32Servo | Primeiro firmware e plano B offline |
| [RNT – ESP32 MQTT Publish/Subscribe](https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/) | PubSubClient com reconexão a cada 5 s | Base do código de Wi-Fi + MQTT |
| [EMQX – MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) | Cliente MQTT no navegador | Base da página |
| [smartlocker](https://github.com/MicaellaSalili/smartlocker/blob/main/ESP32_SmartLocker_Code.ino) | ESP32 + PubSubClient, um tópico por armário (`.../{ID}/unlock`, `status`), MIT | Estrutura dos tópicos |
| [ESP32-MQTT-Servo-Control](https://github.com/Levantosina/ESP32-MQTT-Servo-Control) e [Wokwi + HiveMQ](https://wokwi.com/projects/381829353297474561) | Servo controlado por MQTT, rodando no simulador | Testar antes de o hardware chegar |
| [Exemplo WeAct](https://github.com/WeActStudio/WeActStudio.EpaperModule/blob/master/Example/EpaperModuleTest_Arduino_ESP32/EpaperModuleTest_Arduino_ESP32.ino), [ePaper-writer](https://github.com/ftjuh/ePaper-writer), [ESP32-e-paper-QRcode-generator](https://github.com/G6EJD/ESP32-e-paper-QRcode-generator) | e-paper + GxEPD2 + QR no ESP32 | A etapa da tela |
| [Geocache Box Servo Latch](https://www.printables.com/model/134411-servo-latch-geocache-box-servo-latch), [Servo-Lock](https://www.myminifactory.com/object/3d-print-servo-lock-365536) | Trincos impressos com servo e mola | Geometria da lingueta |
| [maquina-vending-esp32](https://github.com/eduardowakim-lab/maquina-vending-esp32) | Pix pelo Mercado Pago → Cloudflare Worker → MQTT com TLS → ESP32, com consulta HTTP de reserva; sem licença declarada | Só a arquitetura, para o slide de Pix real. Não copiar o código |
| [Embarcados – ESP32-C6 na Prática: MQTT](https://embarcados.com.br/esp32-c6-na-pratica-comunicacao-mqtt/) | Tutorial em português com PubSubClient e brokers públicos | Leitura para quem prefere português |

Para a banca, a ideia já tem referências comerciais. A **rapitag** manda "um código identificador único para a etiqueta via Bluetooth após o pagamento" no app do varejista e fez um piloto na Saturn em 2018 ([iXtenso](https://ixtenso.com/technology/rfid-tags-with-features-for-the-cashierless-store.html)). A **Sensormatic** se juntou à **Zliide** em 2023 numa etiqueta que o próprio cliente solta pelo celular ([BusinessWire](https://www.businesswire.com/news/home/20230116005044/en/Sensormatic-Solutions-by-Johnson-Controls-collaborates-with-Zliide-to-reimagine-self-checkout)). A **MishiPay** desativa a etiqueta RFID pelo app "Scan & Go" ([RFID Journal](https://www.rfidjournal.com/news/self-checkout-solution-employs-rfid-for-security-purchasing/199029/)). A frase de posicionamento sai sozinha: elas usam Bluetooth e app nativo; o Tag&Go usa QR e uma página web, sem instalar nada.

## Conclusão

A pesquisa mostra onde está o risco de verdade. A eletrônica tem tutorial pronto para cada peça. A dúvida sobre a tela se resolve de duas formas: o e-paper mantém o QR sem energia, e o QR impresso torna a tela opcional. As duas incógnitas reais são a lingueta impressa, que não tem modelo pronto e por isso precisa de um bloco de teste já nas primeiras semanas, e a conectividade da sala, resolvida com hotspot próprio, 4G e um modo offline ensaiado. Quem só estudar o Arduino e deixar a trava para novembro vai descobrir o problema tarde demais.

O plano atual do grupo (`prototipo/plano-prototipo.md`) aposta justamente em três escolhas que estas notas desaconselham para iniciantes: Web Bluetooth (que no iPhone exige instalar o app Bluefy), bateria LiPo com carregador TP4056 e placa ESP32-C3 SuperMini. Ele prevê ainda um Cloudflare Worker, que é mais uma peça que pode falhar ao vivo. Como o pedido na Eletrogate está marcado para 01/10, vale decidir entre as duas rotas antes de pagar. Uma saída razoável é apresentar a versão completa como conceito do produto e usar este MVP como a prova física que precisa funcionar em 07/12.
