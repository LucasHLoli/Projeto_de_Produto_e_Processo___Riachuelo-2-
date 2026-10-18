# Carga por indução na Tag&Go

Pesquisa feita em 30/09/2026. Preços e estoque mudam rápido. Confiram de novo antes de comprar.

Palavras usadas aqui:
- Qi: padrão de carregador sem fio de celular. Uma bobina na base (transmissor) cria um campo magnético, e outra bobina dentro do aparelho (receptor) transforma esse campo em energia.
- Receptor Qi: plaquinha fina com bobina e um plugue USB. Faz um celular sem carga sem fio passar a ter.
- FOD: detecção de objeto estranho. A base desliga se achar metal entre as bobinas.
- Buck: plaquinha que baixa a tensão, por exemplo de 12 V para 5 V.
- Pass-through: o power bank carregar e fornecer energia ao mesmo tempo.

## 1. Dá para fazer?

Sim. Um receptor Qi de celular (5 V, até cerca de 1 A) dentro da caixa, apoiada num carregador sem fio na urna, recarrega a Tag&Go sem plugar cabo, e os anúncios falam em 2 a 6 mm de distância, o que cobre uma parede fina de PLA. O porém é que o power bank atual (FAM L10018) só recebe carga pela USB-C, que hoje já alimenta a fechadura, então é preciso trocar de power bank ou mudar a ligação. A carga é lenta (5 W no máximo, uns 3 a 4 W na prática), então a urna repõe o gasto de um empréstimo, mas não enche um power bank vazio durante a demo.

## 2. Como fica no MVP

Hoje:

```
[Power bank FAM L10018]
   USB-C (PD 12 V) ---> [gatilho PD 12 V] ---> [relé] ---> [fechadura SARY 12 V]
   USB-A (5 V) -------> [ESP32] ---> [LEDs] e sinal do relé
```

Problema: a USB-C é a única entrada de carga da FAM, e está ocupada.

Opção A (mais simples, sem solda): trocar o power bank por um que tenha entrada micro USB separada.

```
URNA                                   CAIXA TAG&GO (fundo com 1,5 a 2 mm de PLA sob a bobina)
[tomada] -> [fonte USB 5 V 2 A]        [receptor Qi micro USB]
   -> [carregador Qi]  ~~ campo ~~>        |
   (berço que centraliza a caixa)          v
                                       [entrada micro USB do power bank novo]
                                       [power bank novo]
                                          USB-C PD 12 V -> [gatilho PD] -> [relé] -> [fechadura]
                                          USB-A 5 V -----> [ESP32] -> [LEDs]
```

Opção B (mantém a FAM, dá mais trabalho):

```
[receptor Qi USB-C] -> USB-C da FAM (agora só entrada)
FAM USB-A 12 V -> [gatilho QC 12 V] -> [relé] -> [fechadura]
                                 \-> [buck 12 V para 5 V] -> [ESP32] -> [LEDs]
```

Regras de montagem:
- Ordem de fora para dentro: urna, fundo fino de PLA, bobina, blindagem da bobina, power bank.
- Nada de metal ou ímã sobre a área da bobina: fechadura, parafusos, porcas e o lado magnético da FAM.
- Um berço ou encaixe na urna para a caixa cair sempre centrada.

## 3. Lista de compra

Só itens com página aberta e preço conferido em 30/09/2026. Todos precisam de uma fonte USB de parede de 5 V e 2 A (um carregador de celular comum serve; não pesquisamos um modelo).

| Item | Para que | Preço | Link | Conferido? |
|---|---|---|---|---|
| Receptor Qi tipo C, Brasil Home (Magazine Luiza) | Vai dentro da caixa. Plugue USB-C, saída 5 V / 1 A. Serve para a Opção B (entrada USB-C da FAM) | R$ 67,93 no PIX (R$ 78,99 no cartão). Frete grátis até 05/10 para São Paulo | https://www.magazineluiza.com.br/adaptador-sem-fio-wireless-qi-inducao-receptor-universal-tipo-c-brasil-home/p/gkj66889f8/in/usba/ | Sim, 30/09. Nota 3,0 com 6 avaliações |
| Receptor Qi Comtac 9353 micro USB (Kabum, vendedor RAICROM) | Vai dentro da caixa. Plugue micro USB, 5 V / 1 A. Serve para a Opção A (power bank com entrada micro USB) | R$ 24,90 no PIX, sem frete | https://www.kabum.com.br/produto/177521/receptor-de-carregador-sem-fio-padrao-qi-comtac-conector-micro-usb-para-smartphone-antigo-9353 | Sim, 30/09. Frete não consultado |
| Carregador sem fio Lelong LE-520 15 W (Magazine Luiza) | Base pronta para a urna. Lista saída de 5 V / 1 A, o modo que o receptor usa. Vem com cabo USB-C, sem fonte | R$ 28,69 | https://www.magazineluiza.com.br/carregador-por-inducao-15w-sem-fio-usb-acompanha-cabo-usb-c-le520-lelong/p/ke9dh49dk3/te/accp/ | Sim, 30/09. Distância não informada |
| Módulo transmissor Qi HW-225 (Usinainfo) | Alternativa à base pronta: bobina de 50 mm para embutir no fundo da urna impressa. 5 V, 1 A, 5 W, com FOD | R$ 29,77 no PIX (R$ 31,34 no cartão). "Últimas unidades" | https://www.usinainfo.com.br/carregador-de-bateria/modulo-carregador-sem-fio-por-inducao-qi-wpc-5v-1a-universal-com-micro-usb-hw225-5757.html | Sim, 30/09. Distância não informada |

Compra mínima para começar o teste de bancada hoje: um receptor e uma base, cerca de R$ 97 (Brasil Home + Lelong) ou cerca de R$ 54 (Comtac + Lelong).

Alternativas (também conferidas em 30/09):
- Receptor Sanpyl tipo C (Amazon, vem do exterior): R$ 89,09 mais R$ 8,90 de frete, entrega em 15/10, só 2 em estoque. É o anúncio mais completo: 5 V, 2 a 6 mm, 85 x 45 x 0,55 mm. https://www.amazon.com.br/carregamento-smartphone-compat%C3%ADvel-carregadores-habilitados/dp/B09LR6DMW9
- Base Geonav QI10WG (Amazon): R$ 84,59, só 1 em estoque. Declara saída de 5 V / 1 A e alcance de até 10 mm, o maior da lista. Certificação Qi e Anatel. https://www.amazon.com.br/dp/B07YBKP3L7
- Base Xiaomi 10 W (Kabum): R$ 94,86 no PIX. Alcance de só 4 mm. https://www.kabum.com.br/produto/347003/carregador-sem-fio-10w-xiaomi-preto
- Base ELG Safemag WQ2WH 15 W (Kabum): R$ 98,91 no PIX. Magnética. O ímã atrai o aço da fechadura, então deixem a fechadura longe. https://www.kabum.com.br/produto/379755/carregador-magnetico-wireless-p-smartphone-15w-branco-elg
- Transmissor Xixian 5 W (Amazon): R$ 76,61, entrega de 13 a 22/10, alcance de 2 a 8 mm. Plano B do HW-225. https://www.amazon.com.br/dp/B0H35WKP8R
- Receptor RC1 Lightning (Usinainfo): R$ 7,55 no PIX. Exige cortar o plugue e soldar num plugue USB. Só se alguém do grupo souber soldar. https://www.usinainfo.com.br/carregador-de-bateria/adaptador-para-carregamento-por-inducao-lightning-qi-wireless-5v-1a-para-iphone-8276.html
- AliExpress: placa receptora 5 W por R$ 6,99 mais cerca de R$ 34 de frete (https://pt.aliexpress.com/item/1005010502517248.html) e transmissor por R$ 12,13 (https://pt.aliexpress.com/item/1005008936388405.html). Entrega em 2 a 4 semanas. Só como reserva.

Ainda não verificado (falta pesquisar antes de comprar):
- Power bank com entrada micro USB e saída USB-C PD 12 V em estoque. Os dois achados (Baseus 10000 mAh 20 W e iWill Speed 20 W, na Kabum) estavam esgotados em 30/09.
- Gatilho QC 12 V e buck 12 V para 5 V da Opção B.
- Se a USB-A da FAM entrega 12 V fora do protocolo QC.
- Conector magnético de 2 pinos (pogo pin), plano B sem indução. A página da Amazon deu erro.

## 4. Limites

| Limite | Número | Fonte |
|---|---|---|
| Potência | Receptores simples: 5 V e 1 A, ou seja, 5 W no máximo. Uma base de 10 ou 15 W cai para esse modo básico com um receptor simples | Anúncios da Usinainfo, Sanpyl e Brasil Home; nota do chip KTE7000 (eeNews Europe) |
| Corrente real | Corrente de carga de 800 mA (anúncio RC1). Um módulo parecido foi medido entregando 0,5 a 0,8 A | Usinainfo; ElectroDragon |
| Perda | Carga sem fio gastou 39% mais energia que com fio, e 80% a mais com a bobina desalinhada. A Geonav declara eficiência de até 75% | Wikipedia (Inductive charging); anúncio Geonav |
| Tempo de carga | 10.000 mAh com carregador com fio de 5 V e 1 A: 6 a 10 h (Anker). Por Qi, com 2,5 a 4 W úteis: 10 a 17 h do zero. Esta faixa é estimativa nossa, não medida | Anker; estimativa |
| Gasto por uso | Pulso da fechadura: 12 V x 1,4 A x 0,2 s, cerca de 3,4 J (quase nada). O que gasta é o ESP32 ligado com Wi-Fi, ainda não medido. Se puxar 0,5 W, 1 h de uso volta em uns 10 min na urna (estimativa) | Cálculo nosso |
| Distância | Receptor Sanpyl: 2 a 6 mm. Bases: Xiaomi até 4 mm, Xixian 2 a 8 mm, Geonav até 10 mm. Anker: capa de menos de 3 mm não atrapalha; acima de 5 mm a carga cai bastante. No Qi as bobinas ficam tipicamente a 5 mm | Anúncios; Anker; Wikipedia (Qi) |
| Alinhamento | Desalinhar mais de 3 cm pode derrubar muito a potência. A Apple pede para centralizar o estojo na base | Wikipedia (Inductive charging); Apple |
| Metal | Em teste da WPC com carregadores não certificados, uma moeda entre as bobinas chegou a 96,1 °C em 51 s. Bases com FOD desligam a carga. Ímãs podem saturar o núcleo de ferrite da bobina (0,2 a 0,5 T) | WPC; hsmagnet |
| Calor | O PLA amolece entre 55 e 60 °C; PETG aguenta cerca de 85 °C. Um comprador do Sanpyl relatou falhas com o receptor quente. Limite prático sugerido de 45 a 50 °C no fundo da caixa (estimativa nossa) | FacFox; avaliações Sanpyl |
| Queda de energia | Ao começar a carregar, a saída de um power bank sumiu por cerca de 125 ms em um teste, e por 960 ms em outro. O ESP32 pode reiniciar quando a caixa for posta na urna | Gough's Tech Zone |

## 5. Teste de bancada em 4 passos

1. Receptor na base, sem caixa. Liguem a base na fonte de 5 V, pluguem o receptor no power bank e apoiem o receptor centrado na base.
   Deu certo quando: o indicador de carga do power bank acende e continua aceso por 10 minutos.

2. Através do PLA. Imprimam uma placa de teste com 1,5 mm e outra com 2 mm. Coloquem entre o receptor e a base. Depois desloquem 1 cm para os lados.
   Deu certo quando: o power bank segue carregando nas duas espessuras e com 1 cm de desalinhamento. Anotem até onde funciona para desenhar o berço da urna.

3. Caixa montada, com ESP32 e fechadura ligados. Coloquem e tirem a caixa da urna 10 vezes. Depois de cada vez, mandem abrir a fechadura.
   Deu certo quando: a fechadura abre nas 10 vezes e, se o ESP32 reiniciar, ele volta sozinho e reconecta em menos de 30 s. Se o gatilho de 12 V parar de funcionar durante a carga, o teste falhou.

4. Calor. Deixem a caixa fechada na urna por 1 h, carregando. Meçam a temperatura do fundo e do power bank no fim (termômetro de contato ou infravermelho).
   Deu certo quando: o fundo fica abaixo de 45 °C, o PLA não deforma e a carga não parou sozinha.

## 6. Como contar isso no relatório

A recarga por indução segue o que já existe no mercado: escovas de dente elétricas e estojos de fones sem fio são produtos fechados, sem conector, que carregam apoiados numa base, e a patente Sensormatic US12101138B2 descreve uma etiqueta antifurto que recebe energia de um pad indutivo para soltar a trava. No MVP, usamos o padrão Qi de celular (5 W) com um receptor ligado ao power bank, e a urna repõe a energia gasta em cada empréstimo; a patente vale até 2040 e precisaria de análise num produto comercial, mas não impede o protótipo acadêmico.

## 7. Fontes

Todas abertas em 30/09/2026 pela equipe de pesquisa, salvo indicação.

Produtos:
- Receptor Brasil Home tipo C: https://www.magazineluiza.com.br/adaptador-sem-fio-wireless-qi-inducao-receptor-universal-tipo-c-brasil-home/p/gkj66889f8/in/usba/
- Receptor Comtac 9353: https://www.kabum.com.br/produto/177521/receptor-de-carregador-sem-fio-padrao-qi-comtac-conector-micro-usb-para-smartphone-antigo-9353
- Receptor Sanpyl: https://www.amazon.com.br/carregamento-smartphone-compat%C3%ADvel-carregadores-habilitados/dp/B09LR6DMW9
- Receptor RC1 Lightning: https://www.usinainfo.com.br/carregador-de-bateria/adaptador-para-carregamento-por-inducao-lightning-qi-wireless-5v-1a-para-iphone-8276.html
- Transmissor HW-225: https://www.usinainfo.com.br/carregador-de-bateria/modulo-carregador-sem-fio-por-inducao-qi-wpc-5v-1a-universal-com-micro-usb-hw225-5757.html
- Base Lelong LE-520: https://www.magazineluiza.com.br/carregador-por-inducao-15w-sem-fio-usb-acompanha-cabo-usb-c-le520-lelong/p/ke9dh49dk3/te/accp/
- Base Geonav QI10WG: https://www.amazon.com.br/dp/B07YBKP3L7
- Base Xiaomi 10 W: https://www.kabum.com.br/produto/347003/carregador-sem-fio-10w-xiaomi-preto
- Base ELG WQ2WH: https://www.kabum.com.br/produto/379755/carregador-magnetico-wireless-p-smartphone-15w-branco-elg
- Transmissor Xixian: https://www.amazon.com.br/dp/B0H35WKP8R
- AliExpress receptor: https://pt.aliexpress.com/item/1005010502517248.html
- AliExpress transmissor: https://pt.aliexpress.com/item/1005008936388405.html
- FAM L10018 (portas): https://www.m2ptech.com.br/5uxazaiz9-carregador-portatil-power-bank-10000mah-marca-fam-modelo-l10018
- Baseus 10000 mAh 20 W (esgotado): https://www.kabum.com.br/produto/635754/carregador-portatil-powerbank-baseus-10000mah-20w-turbo-preto
- iWill Speed 20 W (esgotado): https://www.kabum.com.br/produto/481191/speed-20w-power-bank-iwill-10000mah-com-usb-c-pd-preto

Técnicas:
- Receptor em base de maior potência (KTE7000): https://eenewseurope.com/en/5w-wireless-power-receiver-ic-conforms-to-wpc-qi-bpp
- Medição de módulo receptor: https://www.electrodragon.com/product/wireless-charge-receiver-board-qi/
- Tempo de carga de 10.000 mAh: https://www.anker.com/ca/blogs/power-banks/how-long-to-charge-10000mah-power-bank
- Capas e distância: https://www.anker.com/blogs/wireless-chargers/can-wireless-charging-work-with-case
- Carga por indução (perdas, alinhamento, calor): https://en.wikipedia.org/wiki/Inductive_charging
- Padrão Qi (distância típica): https://en.wikipedia.org/wiki/Qi_(standard)
- Centralizar na base (Apple): https://support.apple.com/en-us/119912
- Metal e segurança (WPC): https://www.wirelesspowerconsortium.com/media/xfmb4vsh/qi-certified_expanded_information_brochure_web.pdf
- Ímãs e ferrite: https://hsmagnet.com/2025/11/26/do-magnets-affect-wireless-charging/
- Chip receptor com desligamento térmico: https://www.ti.com/product/BQ51013A
- Temperatura do PLA e do PETG: https://facfox.com/docs/kb/glass-transition-temperatures-of-pla-petg
- Queda de saída do power bank: https://goughlui.com/2021/09/03/note-potential-issues-of-using-a-usb-powerbank-as-a-ups/

Mercado:
- Patente Sensormatic US12101138B2: https://patents.google.com/patent/US12101138B2/en
- Carregador de escova Oral-B: https://www.epanorama.net/blog/2024/02/02/oral-b-toothbrush-charger/
- Etiquetas de prateleira sem bateria: https://www.onio.com/article/batteryless-electronic-shelf-labels.html
