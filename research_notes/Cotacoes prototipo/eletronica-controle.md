# Cotações: eletrônica de controle do protótipo

Levantamento feito em 19/10/2026, com as páginas abertas no navegador. Frete calculado para a Poli-USP, CEP 05508-010 (São Paulo, SP).

Regra usada: cada linha tem o custo do item **comprado sozinho** naquela loja, já com o frete. Retirada na loja não conta.

Como li os preços:
- **Pix**: preço à vista no Pix/boleto mostrado na página.
- **Cartão**: preço cheio ou parcelado sem juros.
- **Frete**: a opção mais barata com entrega, para 1 unidade, salvo outra indicação. As placas pesam cerca de 10 a 25 g, então o frete de 2 unidades deve ficar igual ou bem perto.
- **Total**: quantidade × preço Pix + frete.

Não usei AliExpress, Shopee nem anúncios de "Compra Internacional". O Mercado Livre pediu login antes de mostrar a busca, por isso ficou de fora.

---

## Item 1. Placa ESP32 DevKit V1, 30 pinos, ESP-WROOM-32, USB-C, conversor CP2102 (quantidade 2)

Consegui o mesmo produto em 3 lojas com estoque: USB-C, CP2102, 30 pinos e módulo ESP-WROOM-32 ou 32D. Não precisei cair para micro-USB.

| Loja | Produto | Link | Preço Pix (un.) | Preço cartão (un.) | Estoque | Frete (item sozinho) | Total com frete (2 un., Pix) | Observação |
|---|---|---|---|---|---|---|---|---|
| Amazon.com.br (vendido por Mercado Misto, **enviado pela Amazon**) | Esp32 Doit Devkit Com Esp32-Wroom-32 USB-C Placa de Desenvolvimento 30 Pinos Soldado Processador 2 Em 1 WiFi e Bluetooth 2.4GHz | https://www.amazon.com.br/dp/B0GZ4G9984 | R$ 46,05 | R$ 48,48 (2x de R$ 24,24) | Em estoque | **Grátis**, entrega 20/10 para o CEP 05508-010 | **R$ 92,10** (cartão: R$ 96,96) | Os destaques do anúncio confirmam USB-C, CP2102 e 30 pinos. O vendedor é nacional e o estoque fica na Amazon Brasil. Garantia de 30 dias. A nota fiscal é do vendedor, Mercado Misto. |
| Saravati (Santa Ifigênia, SP) | Placa ESP32 WiFi / Bluetooth DEVKit V1 30 Pinos TIPO-C | https://www.saravati.com.br/placa-esp32-wifi-bluetooth-devkit-v1-30-pinos-tipo-c.html | R$ 58,41 | R$ 64,90 (6x de R$ 10,82) | Em estoque (95 un.) | SEDEX R$ 10,93, até 2 dias úteis (PAC R$ 17,00; Envios Flex R$ 14,90) | **R$ 127,75** (cartão: R$ 140,73) | ESP32-WROOM-32, CP2102, USB-C, 30 pinos. A página atende compras institucionais (FAPESP, universidades). |
| Usinainfo | Placa ESP32-WROOM-32 DevKit V1 NodeMCU 30 Pinos CP2102 WiFi Bluetooth – USB-C | https://www.usinainfo.com.br/esp32/esp32-wifi-e-bluetooth-com-usb-c-30-pinos-e-cp2102-9114.html | R$ 62,49 | R$ 65,78 | **"Últimas unidades"** | J&T Express R$ 11,77, 4 a 7 dias úteis (simulado no carrinho com 1 un.; JADLOG R$ 23,69; SEDEX R$ 51,22) | **R$ 136,75** (cartão: R$ 143,33) | ESP32-WROOM-32D, CP2102, USB-C. **O preço subiu**: a cotação anterior era R$ 56,81 Pix / R$ 59,80. |
| *(sem estoque)* Curto Circuito | Placa DOIT ESP32-WROOM-32D - USB C | https://curtocircuito.com.br/placa-doit-esp32-wroom-32d-usb-c.html | — | R$ 67,00 | **Esgotado** | — | — | É o mesmo produto (WROOM-32D, CP2102, USB-C, 30 pinos), mas está sem estoque. Fica só como referência. |

Alternativas que **não** são o mesmo produto (deixei só para registro):
- Smart Kits, "Placa ESP32 WiFi Bluetooth USB Tipo C": R$ 56,90 à vista / R$ 59,90, frete mais barato R$ 23,19. É USB-C e 30 pinos, mas o conversor é **CH340C**. https://www.smartkits.com.br/placa-esp32-wifi-bluetooth-usb-tipo-c
- Usinainfo também vende uma versão USB-C com CH340 (R$ 54,95 no cartão).
- Versão micro-USB, se precisar trocar: Eletrogate "Módulo WiFi ESP32 Bluetooth 30 pinos", R$ 52,16 Pix / R$ 54,90, frete Jadlog R$ 10,90, total para 2 un. R$ 115,22. https://www.eletrogate.com/modulo-wifi-esp32-bluetooth-30-pinos. A mesma versão existe na Mamute, "ESP32 Módulo DOIT ESP Wroom 32 Dual Core 30 Pinos - Micro USB", por R$ 59,66 Pix / R$ 62,80.

---

## Item 2. Placa expansora (shield) para ESP32 DevKit 30 pinos: fileiras de pinos, USB-C + micro-USB e conector P4 (quantidade 1)

As três placas são o mesmo modelo genérico (Q67 / "ESP32EXP"): encaixe para 30 pinos, entradas USB-C e micro-USB de 5 V, conector P4 de 6,5 a 16 V, regulador AMS1117 e jumper para escolher 3,3 V ou 5 V.

| Loja | Produto | Link | Preço Pix | Preço cartão | Estoque | Frete (item sozinho) | Total com frete (Pix) | Observação |
|---|---|---|---|---|---|---|---|---|
| Magalu (vendido por Rms Robótica, entregue por Magalu) | Modulo expansor para esp32 30 pinos - com terminais de alimentacao | https://www.magazineluiza.com.br/modulo-expansor-para-esp32-30-pinos-com-terminais-de-alimentacao/p/adhg39671a/et/eace/ | R$ 24,94 | R$ 29,00 | Disponível | **Grátis**, "Receba hoje". Apareceu na busca com o endereço Av. Prof. Luciano Gualberto, SP, já salvo no navegador. A página do produto pedia o CEP de novo e não repetiu o valor. | **R$ 24,94** (cartão: R$ 29,00) | A descrição bate: micro-USB, USB-C e P4 de 6,5 a 16 V. Atenção: a loja tem nota 2,6 na Magalu e o atendimento aparece como "Demora para responder". |
| Mamute Eletrônica (Centro, SP) | Placa Shield Expansão de Módulo ESP32 WROOM-32 Wifi e Bluetooth - 30 Pinos e USB Micro/Tipo C | https://www.mamuteeletronica.com.br/placa-shield-expansao-de-modulo-esp32-wroom-32-wifi-e-bluetooth-30-pinos-e-usb-micro-tipo-c-22386 | R$ 21,76 | R$ 22,90 | Em estoque | SEDEX R$ 9,94, 1 dia útil após o envio (PAC R$ 15,45; motoboy R$ 28,90) | **R$ 31,70** (cartão: R$ 32,84) | Pinos de 3,3 V, 5 V e Vin; P4 de 6,5 a 16 V. |
| Usinainfo | Expansor para ESP32 DevKit V1 30 Pinos - USB-C e Micro | https://www.usinainfo.com.br/expansores-shields/expansor-para-esp32-devkit-v1-30-pinos-usb-c-e-micro-8795.html | R$ 21,19 | R$ 22,30 | Disponível | **Estimativa: cerca de R$ 17** (J&T). O carrinho do navegador tinha outro item leve; com os dois juntos, deu J&T R$ 17,09 e SEDEX R$ 56,82. | **≈ R$ 38,20** (estimativa; cartão ≈ R$ 39,30) | Modelo Q67, P4 de 7 a 16 V. O preço Pix é o mesmo da referência. |
| *(4ª opção)* Saravati | Placa Shield Expansão ESP32 ESP-WROOM-32 Micro USB / USB-C | https://www.saravati.com.br/placa-shield-expansao-esp32-esp-wroom-32-micro-usb-usb-c.html | R$ 26,91 | R$ 29,90 | Em estoque (187 un.) | O simulador só ofereceu **retirada na loja** para o item sozinho. Não deu para cotar entrega. | — | É o mesmo modelo (P4 de 6,5 a 16 V, USB-C e micro). Ficou de fora porque não tem entrega para o item avulso. |

Não encontrei esse expansor na Eletrogate. A MakerHero só vende a versão com bornes, que é outro produto.

---

## Item 3. Capacitor eletrolítico 1000 µF, 16 V ou 25 V (quantidade 2)

Aqui o frete é maior que o produto em todas as lojas que cobram entrega. Comprado sozinho, o frete fica de 7 a 11 vezes o preço dos dois capacitores.

| Loja | Produto | Link | Preço Pix | Preço cartão | Estoque | Frete (item sozinho) | Total com frete (2 un., Pix) | Observação |
|---|---|---|---|---|---|---|---|---|
| Eletrogate | Capacitor Eletrolítico 1000uF x 16V | https://www.eletrogate.com/capacitor-eletrolitico-1000uf-x-16v | R$ 0,71 / un. | R$ 0,75 / un. | Disponível | Jadlog Econômico R$ 15,90, 5 dias úteis (PAC R$ 21,65; SEDEX R$ 32,10) | **R$ 17,32** (cartão: R$ 17,40) | O frete é cerca de 11 vezes o produto. A loja dá frete grátis acima de um mínimo que muda por estado (R$ 199 a R$ 599). |
| Amazon.com.br (vendido por Smartcomp, **enviado pela Amazon**) | SMART COMPONENTES ELETRÔNICOS - Kit de 10 Capacitores Eletrolíticos 1000uF 25V 105°C Redondos Genéricos | https://www.amazon.com.br/dp/B09V1PPP5B | R$ 22,22 (kit com 10) | R$ 22,22 | Em estoque | **Grátis**, entrega 20/10 para o CEP 05508-010 | **R$ 22,22** | É um kit com 10 peças de 25 V; só 2 serão usadas. Não depende de cupom de primeira compra. |
| Usinainfo | Capacitor Eletrolítico 1000uF 16V | https://www.usinainfo.com.br/capacitor-eletrolitico/capacitor-eletrolitico-1000uf-16v-3052.html | R$ 2,13 / un. | R$ 2,24 / un. | Disponível | **Estimativa: cerca de R$ 16,92** (J&T). É o valor que o carrinho mostrou para um item leve parecido; não simulei o capacitor sozinho. | **≈ R$ 21,18** (estimativa; cartão ≈ R$ 21,40) | O preço subiu: a referência era R$ 1,94. A versão de 25 V custa R$ 2,08 no Pix. |
| *(sem entrega avulsa)* Mamute Eletrônica | Capacitor Eletrolítico 1000uF 16V 17x10mm 105 graus | https://www.mamuteeletronica.com.br/capacitor-eletrolitico-1000uf-16v-caneca-10x11mm-105-316 | — | R$ 1,10 / un. | Em estoque | O simulador só ofereceu retirada ou motoboy sem valor para o item sozinho | — | Ficou de fora porque não dá para cotar a entrega do item avulso. |

Também na Amazon: "Capacitor Eletrolítico 1000uF 16V - Kit 10 Peças" por R$ 18,87 (https://www.amazon.com.br/dp/B09V1PSLX9). O frete grátis desse kit vale **só no primeiro pedido**, por isso não entrou na tabela.

---

## Loja de menor custo total por item (item comprado sozinho, com frete, no Pix)

| Item | Qtd. | Loja mais barata | Total com frete | 2º lugar | 3º lugar |
|---|---|---|---|---|---|
| 1. ESP32 DevKit V1 30 pinos USB-C CP2102 | 2 | **Amazon (Mercado Misto, enviado pela Amazon)** | **R$ 92,10** | Saravati R$ 127,75 | Usinainfo R$ 136,75 |
| 2. Expansor ESP32 30 pinos (USB-C/micro/P4) | 1 | **Magalu (Rms Robótica)** | **R$ 24,94** | Mamute R$ 31,70 | Usinainfo ≈ R$ 38,20 (estimativa) |
| 3. Capacitor 1000 µF 16 V/25 V | 2 | **Eletrogate** | **R$ 17,32** | Usinainfo ≈ R$ 21,18 (estimativa) | Amazon, kit com 10, R$ 22,22 |

Soma dos mais baratos: **R$ 134,36** no Pix.

## Pontos de atenção

- **A Usinainfo subiu os preços** desde a referência. A ESP32 USB-C passou de R$ 56,81 para R$ 62,49 no Pix e está com aviso de "Últimas unidades". O capacitor passou de R$ 1,94 para R$ 2,13.
- **As placas da Amazon e da Magalu vêm de vendedores parceiros.** A nota fiscal sai em nome do vendedor (Mercado Misto e Rms Robótica), não da Amazon nem da Magalu. Nos dois casos o estoque está no Brasil e a entrega é feita pela própria plataforma.
- **Fretes estimados.** Os valores da Usinainfo para o expansor e o capacitor são estimativas. O carrinho do navegador era compartilhado e já tinha outro item. Para fechar o número exato, basta simular com o carrinho vazio.
- **Capacitor:** comprado sozinho, o frete pesa muito mais que a peça. Se a regra da disciplina deixar, vale comprar os capacitores na mesma loja de outro item; aí o custo da linha cai para menos de R$ 5.
- **Não consegui cotar no Mercado Livre**, porque o site pediu login para mostrar a busca.
