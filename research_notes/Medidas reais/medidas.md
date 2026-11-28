# Medidas reais das peças compradas

Pesquisa feita em 28/11/2026, partindo da aba "Medidas x projeto" de `prototipo/pedido-materiais-PRO3474-grupo4-v2.xlsx`. Todas as medidas em mm.

Tipo de fonte em cada número:

- **[F]** fabricante (site, datasheet ou imagem oficial da marca)
- **[L]** anúncio de loja
- **[C]** comunidade (medição publicada por usuário, footprint KiCad, biblioteca OpenSCAD)
- **[E]** estimativa nossa, tirada de foto ou desenho com escala. Serve para rascunho, não para furar.

Quando as fontes discordam, todos os valores aparecem. "não encontrado" quer dizer que nenhuma fonte trouxe o número.

## Resumo para o CAD

| Peça | Medida externa (C × L × A) | Furos de fixação | Conectores e o que sai para fora | Confiança |
|---|---|---|---|---|
| ESP32 DevKit V1 30 pinos USB-C | 51,5 a 51,8 × 28,2 a 28,3; PCB 1,6 | 4 furos Ø2,8 a 3,0; centros a 23,0 × 46,0 [C] | Fileiras a 25,4 [C]; USB-C no centro de uma ponta curta, sai ~1 mm além da borda [C/E]; pinos por baixo ~8,5 [E] | média, medir furos |
| Expansor ESP32 30 pinos (Mamute) | 68,6 × 53,4 [L]; altura 16 com barras [L] | 4 furos Ø3,4; distâncias 50,81 / 52,52 / 27,96 / 48,39 [L] | P4, micro-USB e USB-C na mesma ponta curta [L foto] | boa (desenho de loja do mesmo modelo) |
| Servo SG90 | corpo 22,2 a 22,7 × 11,8 a 12,4; topo do corpo 26,4 a 27; até topo do eixo 29,4 a 31 | orelhas 32,2 a 32,4; furos Ø2,6 a 27,94 entre centros [C] | eixo a ~5,1 da ponta do corpo [C]; base da orelha a 15,6 a 17 do fundo | boa |
| Servo MG90S | corpo 22,5 a 22,9 × 12 a 12,4; topo do corpo 28,4; até topo do eixo 32,5 | orelhas 32,1 a 32,5; furos Ø2,2 a 28,32 entre centros [C] | eixo a ~5,3 da ponta do corpo [C]; base da orelha a 18,3 a 21 do fundo | boa |
| Chave fim de curso YL-99 | 25 × 13,7 × 5,8 [L] | 1 furo (Ø não encontrado) | 3 pinos retos (VCC, GND, OUT) na ponta oposta à chave; haste passa da borda | baixa, medir |
| Semáforo LED 8 mm | 56 × 21 × 11 [F distribuidor] | furos Ø3 [F distribuidor] | 4 pinos retos (GND, R, Y, G) saindo da ponta; LEDs a ~12 a 13 entre centros [E] | média |
| Power bank ELG PB102BK | 149 × 69 × 15 [L Amazon] | não tem | USB-A, USB-C, USB-A na face curta de cima; micro-USB na lateral longa esquerda perto do topo; botão na lateral direita [F imagem] | boa no tamanho, posição só por foto |
| Receptor Qi Comtac 9353 | ~75 × 45, fino (~1) | não tem | rabicho de flex com micro-USB numa ponta curta | baixa, medir |
| Base HyperX ChargePlay | 215,05 × 90,91 × 17,36 [F] | não tem | 2 bobinas a ~47 de cada ponta, no meio da largura, ~121 entre centros [E sobre desenho F] | boa no tamanho, bobinas estimadas |
| Capacitor 1000 µF 16 V | Ø10 × 16 (mais comum) ou Ø10 × 20 | não tem | terminais radiais a 5 entre si | média, medir o comprado |
| Ímã neodímio 15 × 5 | Ø15 × 5, ±0,1 | não tem | não tem | boa |
| Pino de etiqueta antifurto | haste Ø~1,2; comprimento 16 ou 19; cabeça Ø12 a 13 | não tem | não tem | média |

O que ainda precisa de paquímetro antes de imprimir: furos e altura do ESP32 com pinos, altura total do conjunto ESP32 + expansor, haste e furo do YL-99, distância entre LEDs do semáforo, receptor Qi (tamanho, espessura e comprimento do rabicho), capacitor comprado, garra antifurto.

## 1. ESP32 DevKit V1, 30 pinos, ESP-WROOM-32, USB-C, CP2102

Anúncio comprado: https://www.amazon.com.br/dp/B0GZ4G9984 (fabricante "Leixinrui Eletronicos", 15 g). O anúncio não traz medidas. As fotos mostram a placa DOIT de 30 pinos com USB-C no meio de uma ponta curta, botões EN e BOOT um de cada lado do USB, CP2102 e regulador 1117 do mesmo lado do módulo, e 4 furos nos cantos.

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Placa C × L | 51,8 × 28,2 | https://forum.fritzing.org/t/doit-esp32-devkit-v1/6158/9 (usuário noiasca, medido) | C |
| Placa C × L | 51,8 × 28,2 | https://mischianti.org/doit-esp32-dev-kit-v1-high-resolution-pinout-and-specs/ (resposta do autor) | C |
| Placa C × L | 51,45 × 28,33 | https://www.espboards.dev/esp32/esp32doit-devkit-v1/ | C |
| Placa C × L | 51,5 × 28,3 (contorno do silk) | footprint KiCad corrigido https://github.com/syauqibilfaqih/ESP32-DevKit-V1-DOIT (ESP32_30pin.kicad_mod) | C |
| Placa C × L × A | 51,4 × 28,5 × 15 | https://tinkered.ai/components/esp32-devkit-v1 | C |
| Distância entre fileiras de pinos | 25,40 (centro a centro) | footprint KiCad syauqibilfaqih (pinos em x = −11,93 e +13,47) | C |
| Distância entre fileiras de pinos | 25,40 (pinos em x = ±12,7) | https://github.com/davidkleymann/doit-esp32-devkit-kicad | C |
| Passo dos pinos | 2,54; 15 pinos por fileira (35,56 do primeiro ao último) | footprint KiCad syauqibilfaqih | C |
| Primeiro pino até a borda | 8,1 do lado do USB e 7,9 do lado da antena (KiCad); 10,3 e 6,7 (noiasca) | KiCad syauqibilfaqih; fórum Fritzing | C, discordam |
| Furos de fixação | 4 furos Ø3,0; centros 23,0 entre si na largura e 46,0 no comprimento; centro a ~2,5 a 3,0 da borda | footprint KiCad syauqibilfaqih (Edge.Cuts) | C |
| Furos de fixação | Ø2,8; 0,8 da borda do furo até a borda da placa; "43,9 entre os furos de cima e de baixo" (não diz se é entre bordas ou centros) | fórum Fritzing, noiasca | C |
| Módulo ESP-WROOM-32 | 18,00 × 25,50 × 3,10 (±0,10) | datasheet Espressif, https://documentation.espressif.com/esp32-wroom-32_datasheet_en.pdf | F |
| Espessura da PCB | não encontrado (padrão de mercado 1,6) | | |
| USB-C | centrado na ponta curta oposta à antena; o corpo do conector passa ~1 da borda | footprint KiCad (retângulo do USB vai até 1,0 além da borda); fotos do anúncio | C/E |
| Altura do lado de cima (PCB + módulo) | ~4,7 (1,6 + 3,1); o USB-C fica na mesma faixa | soma das linhas acima | E |
| Pinos por baixo | não encontrado no anúncio; barra 2,54 comum deixa ~2,5 de plástico + ~6 de pino abaixo da PCB, ~8,5 no total | valor típico de barra de pinos | E, medir |

Observação: placas "DevKit V1" são clones e os furos variam entre fabricantes (por isso as fontes discordam em 0,5 a 1 mm). As fileiras a 25,4 batem nas duas fontes.

## 2. Placa expansora ESP32 30 pinos com S/V/G, micro-USB, USB-C e P4

Anúncio comprado: https://www.mamuteeletronica.com.br/placa-shield-expansao-de-modulo-esp32-wroom-32-wifi-e-bluetooth-30-pinos-e-usb-micro-tipo-c-22386 . Fabricante indicado: "IMP". O mesmo modelo (foto igual, texto "ESP32 ESP32S 30P Expansion board") tem desenho de cotas na loja Makers Electronics.

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Dimensões | 16 × 54 × 69 (aprox.); 24 g | Mamute (link acima) | L |
| Dimensões | 68,6 × 53,4 | desenho de cotas, https://makerselectronics.com/product/expansion-board-for-esp32-30p-usb-c/ (imagem ESP32-EXP-2-1.jpg) | L (outro vendedor, mesmo modelo) |
| Dimensões | 68 × 53,5 | mesma loja, outra imagem | L |
| Dimensões | 72 × 55 × 10 | listagem citada em busca (vendedor indiano, robu.in) | L, discorda |
| Furos | 4 furos Ø3,4 | desenho Makers Electronics | L |
| Posição dos furos (desenho em vista por baixo, conectores à esquerda) | par do lado dos conectores: 48,39 entre centros; par do lado oposto: 27,96 entre centros; na horizontal 52,52 (par de cima) e 50,81 (par de baixo) | desenho Makers Electronics | L |
| Comparação | o contorno 68,6 × 53,4 e os furos (27,96 / 50,81) batem com o padrão do Arduino Uno. Vale conferir com o desenho oficial do Uno se for usar um suporte padrão | dedução nossa | E |
| Conectores | P4 (DC 6,5 a 16 V), micro-USB e USB-C, todos na mesma ponta curta; o P4 passa da borda da placa | fotos da Mamute e da Makers Electronics | L (foto) |
| Fileiras de soquete fêmea para o ESP32 | não encontrado em número; deve casar com 25,4 do ESP32 | | medir |
| Altura do soquete fêmea | não encontrado (barra fêmea 2,54 comum tem ~8,5) | | E |
| Altura com o ESP32 encaixado | não encontrado. Conta aproximada: PCB 1,6 + soquete 8,5 + PCB do ESP32 1,6 + módulo 3,1 ≈ 15 acima da face de baixo do expansor, mais as pontas de solda por baixo (~2) | soma de valores típicos | E, medir |
| Jumper 5 V / 3,3 V e pinos S/V/G | ao lado das fileiras, pinos machos para cima | fotos | L |

## 3. Micro servo SG90 (TowerPro)

Anúncio comprado: https://www.saravati.com.br/micro-servo-motor-9g-sg90.html (marca "CF Sunbird / Tower Pro", cabo 200, 10 g, "32 largura × 12 profundidade × 32 altura", vem com 3 braços).

Letras do desenho oficial TowerPro (https://www.towerpro.com.tw/product/sg90-7/ e imagem-chave http://torqpro.com/wp-content/uploads/2014/07/小馬達尺寸標示圖B.jpg): A = fundo até o topo do eixo; B = comprimento do corpo; C = fundo até o topo da caixa (sem o eixo); D = largura; E = comprimento com as orelhas; F = fundo até a orelha.

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Corpo C × L | 22,7 × 12,2 (B, D) | TowerPro site | F |
| Corpo C × L | 22,2 × 11,8 | datasheet TowerPro clássico (cópia em https://tams.informatik.uni-hamburg.de/lehre/2023ss/vorlesung/es/doc/sg90.pdf) | F |
| Corpo C × L | 22,62 × 12,38 | biblioteca OpenSCAD com servos medidos, https://github.com/GetBurning/servo_lib (servos/sg90_clone.scad) | C |
| Dimensão geral | 23 × 12,2 × 29 | TowerPro site (linha "Dimension") | F |
| Altura até o topo da caixa (C) | 27 | TowerPro site | F |
| Altura até o topo da caixa | 26,36 (15,56 + 2,46 + 8,34) | servo_lib medido | C |
| Altura até o topo do eixo (A) | 30,3 | TowerPro site | F |
| Altura até o topo do eixo | 31 | datasheet clássico | F |
| Altura até o topo do eixo | 29,44 (eixo sobe 3,08 acima da caixa) | servo_lib medido | C |
| Altura (loja) | 32 | Saravati | L |
| Orelhas de ponta a ponta (E) | 32,3 / 32,2 / 32,38 | TowerPro site / datasheet clássico / servo_lib | F / F / C |
| Fundo até a orelha (F) | 17 (site) ou 16 (datasheet clássico) | TowerPro | F, discordam |
| Fundo até a face de baixo da orelha | 15,56 | servo_lib | C |
| Espessura da orelha | 2,46 | servo_lib | C |
| Espessura da orelha | 2,5 | https://microservomotor.com/common-specifications-and-parameters/micro-servo-mounting-pattern.htm (site de conteúdo, confiável pouco) | C |
| Furos das orelhas | Ø2,6, centros a ±13,97 do meio do corpo (27,94 entre centros) | servo_lib medido | C |
| Furos das orelhas | "cerca de 27,5 a 28 entre centros"; parafuso autoatarraxante ST2,2 | https://kapycad.com/en/academy/standards/motor-mounts | C |
| Furos | são ranhuras abertas para fora (U), não furos fechados | desenho TowerPro | F |
| Posição do eixo | centro do eixo a 6,19 do meio do corpo, isto é ~5,1 da ponta mais próxima do corpo | servo_lib medido | C |
| Eixo estriado | Ø4,0 (servo_lib), 20 dentes | servo_lib | C |
| Eixo estriado | Ø~4,8 com dentes, 21 dentes "na maioria" | kapycad; https://www.kpower.com/insight_driver/7062.html | C, discordam no nº de dentes |
| Braço simples | furos Ø1,4 a cada 2, do 5 ao 17 a partir do centro do eixo; espessura da chapa 2; altura do cubo 5; cubo Ø6 | https://kernelcad.com/standards/servo-horn/ (de FreeCAD library) | C |
| Comprimento total do braço simples | não encontrado (pelo item acima, ~19 a 20 do centro do eixo até a ponta) | | E |
| Saída do cabo | pela face curta do lado do eixo, junto do fundo | desenho-chave TowerPro | F |
| Altura da saída do cabo | não encontrado | | medir |
| Cabo | 200 (Saravati); conector fêmea 3 vias 2,54 | Saravati | L |

## 4. Micro servo MG90S (TowerPro)

Anúncio comprado: https://www.makerhero.com/produto/micro-servo-mg90s-towerpro/ ("35,5 × 32,5 × 12", cabo ~175, 13,4 g, vem com 3 braços).

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Corpo C × L | 22,8 × 12,4 (B, D) | https://www.towerpro.com.tw/product/mg90s-3/ | F |
| Corpo C × L | 22,5 × 12 | datasheet TowerPro (cópia em https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf) | F |
| Corpo C × L | 22,92 × 12,38 | https://github.com/GetBurning/servo_lib (servos/mg90s_clone.scad) | C |
| Dimensão geral | 22,8 × 12,2 × 28,5 | TowerPro site | F |
| Altura até o topo da caixa (C) | 28,4 | TowerPro site | F |
| Altura até o topo da caixa | 28,46 (18,31 + 2,53 + 7,62) | servo_lib | C |
| Altura até o topo do eixo (A) | 32,5 | TowerPro site | F |
| Altura até o topo do eixo | 32,46 (eixo sobe 4,0) | servo_lib | C |
| Altura com braço | 35,5 | datasheet TowerPro e MakerHero | F / L |
| Orelhas (E) | 32,1 / 32,5 / 32,38 | TowerPro site / datasheet / servo_lib | F / F / C |
| Fundo até a orelha (F) | 18,5 (site); 21 (datasheet antigo, cota até a orelha) | TowerPro | F, discordam |
| Fundo até a face de baixo da orelha | 18,31 | servo_lib | C |
| Espessura da orelha | 2,53 | servo_lib | C |
| Furos das orelhas | Ø2,2, centros a ±14,16 do meio do corpo (28,32 entre centros) | servo_lib | C |
| Posição do eixo | 6,19 do meio do corpo, ~5,3 da ponta mais próxima | servo_lib | C |
| Eixo estriado | metálico, Ø4,7, 20 dentes; furo roscado no topo (foto oficial MG90S-b.jpg) | servo_lib; TowerPro | C / F |
| Braço simples | não encontrado específico do MG90S | | medir |
| Saída do cabo | igual ao SG90 (face curta, lado do eixo, junto do fundo) | desenho TowerPro | F |
| Cabo | ~175 | MakerHero | L |

## 5. Módulo chave fim de curso com LED, 3 pinos

Anúncio comprado: https://curtocircuito.com.br/modulo-chave-fim-de-curso.html . A foto mostra a placa azul "YL-99": micro chave preta "2A 125V AC" com haste metálica na ponta, LED SMD, dois resistores, 1 furo de fixação no meio da placa e 3 pinos machos retos (VCC, GND, OUT) saindo na ponta oposta à chave, paralelos à placa.

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Dimensões | 25 × 13,7 × 5,8; 3 g; 3 a 12 V | Curto Circuito | L |
| Dimensões | 32 × 10 × 10 (aprox.), 2 furos | https://docs.cirkitdesigner.com/component/2c0228c7-c5f8-40ec-a836-ebf4c49a9722/yl-99-limit-switch-and-led | C, pouco confiável |
| Dimensões | 27 × 10 × 10, furo Ø2 | https://docs.cirkitdesigner.com/component/c17e9b65-9483-473d-8619-9befa424461c/yl-99-limit-switch | C, pouco confiável |
| Furo de fixação | 1 furo, perto do centro (foto da Curto); diâmetro não encontrado | foto | L |
| Comprimento e altura da haste | não encontrado | | medir |
| Posição da chave | na ponta oposta aos pinos, ocupando toda a largura da placa | foto | L |
| Pinos | 3 pinos 2,54 retos, apontando para fora na ponta curta, no plano da placa | foto | L |

A medida 25 × 13,7 bate com a planilha anterior e cabe no espaço reservado. Haste e furo ficam para medir.

## 6. Módulo semáforo LED 8 mm

Anúncio comprado: https://www.makerhero.com/produto/modulo-semaforo-led/ (LED 8 mm difuso, 5 V ou 3,3 V, pinos GND, R, Y, G; sem medidas). A foto mostra placa em "T": faixa dos LEDs e, na ponta, uma cabeça mais larga com 2 furos e os 4 pinos retos apontando para fora no plano da placa.

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Dimensões | 56 × 21 × 11 | datasheet AZ-Delivery, https://cdn.shopify.com/s/files/1/1509/1638/files/LED_Ampel_Modul_Datenblatt_AZ-Delivery_Vertriebs_GmbH.pdf | F (distribuidor que vende como produto próprio) |
| Dimensões | 56 × 21 × 11 | https://www.berrybase.de/en/led-traffic-light-module-with-3x-8mm-led-red-yellow-green-5v | L |
| PCB | 56 × 13 (faixa dos LEDs) | https://protosupplies.com/product/traffic-light-led-module/ | L |
| Furos | Ø3 (2 furos na cabeça do T, um de cada lado dos pinos) | AZ-Delivery; Berrybase; foto MakerHero | F / L |
| LED | Ø8 | MakerHero, AZ-Delivery | L / F |
| Distância entre centros dos LEDs | não encontrado; ~12 a 13 pela foto da MakerHero | foto | E, medir |
| Altura do LED acima da placa | não encontrado; o total de 11 inclui LED + placa | | medir |
| Pinos | 4 pinos 2,54 retos na ponta, ordem GND, R, Y, G | MakerHero | L |

## 7. Power bank ELG PB102BK 10.200 mAh

Anúncio comprado: https://www.magazineluiza.com.br/carregador-portatil-power-bank-elgpb102bk-10200mah-original-display-digital-pd20w-quick-charge-225w/p/fg519ed5gd/te/accp/ (a página bloqueia leitura automática; as medidas vieram do anúncio do mesmo modelo na Amazon).

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| C × L × A | 149 × 69 × 15 ("14,9C x 6,9L x 1,5 espessura cm") | https://www.amazon.com.br/dp/B0DJ3LHDG4 (modelo PB102BK, ANATEL 05169-19-11044) | L |
| Peso | ~280 g com embalagem (versão branca PB102WH) | https://www.kabum.com.br/produto/992904/ | L |
| Face curta de cima | USB-A (saída 1), USB-C (entrada/saída), USB-A (saída 2), da esquerda para a direita, USB-C no meio | imagens oficiais ELG no anúncio Amazon | F (imagem) |
| Micro-USB (só entrada) | na lateral longa esquerda, perto do topo | imagem oficial ELG ("Entrada Micro USB") | F (imagem) |
| Botão (liga o visor) | na lateral longa direita, a ~1/4 do comprimento a partir do topo | imagem oficial ELG | F (imagem), posição exata não encontrada |
| Visor | na face da frente, perto do topo, numa janela escura que ocupa ~1/3 do comprimento | imagem oficial ELG | F (imagem) |
| Distâncias das portas às bordas | não encontrado | | medir |
| Entradas e saídas | entrada micro-USB e USB-C 5 V/3 A, 9 V/2 A, 12 V/1,5 A; saída USB-C PD 20 W; USB-A QC 22,5 W | https://www.terabyteshop.com.br/produto/36002/ | L |

## 8. Receptor Qi Comtac 9353, micro-USB

Anúncio comprado: https://www.kabum.com.br/produto/177521/receptor-de-carregador-sem-fio-padrao-qi-comtac-conector-micro-usb-para-smartphone-antigo-9353 . Página da marca: https://comtacmg.com/produto/receptor-de-carregador-sem-fio/ (código 21149353, DC 5 V 1 A, "ultra fino"). Nenhuma das duas traz medidas. A foto mostra uma folha retangular preta com um rabicho de circuito flexível (não é cabo redondo) saindo de uma ponta curta, terminando no plugue micro-USB.

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Folha | 45 × 75 | planilha anterior ("ficha da Atera"); não consegui reabrir essa fonte | L, não reconfirmado |
| Folha | ~62 × 45 × 1,1 (receptor genérico do mesmo tipo) | https://www.cnx-software.com/2014/10/27/add-wireless-charging-to-almost-any-smartphone-or-tablet/ | C, outro fabricante |
| Folha | 70 × 45, 4 g (receptor Exbom parecido) | https://www.kabum.com.br/produto/526384/ | L, outro fabricante |
| Espessura | não encontrado ("ultra fino") | Comtac | |
| Comprimento do rabicho | não encontrado (a planilha anterior cita 3 cm, sem fonte) | | medir |
| Plugue | micro-USB macho; tamanho do plugue não encontrado | | medir |

## 9. Base de carga sem fio HyperX ChargePlay Base

Anúncio comprado: https://www.amazon.com.br/dp/B07ZFXTGS6

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| C × L × A | 215,05 × 90,91 × 17,36 | imagem de cotas oficial HyperX no anúncio Amazon (https://m.media-amazon.com/images/I/51mAZ75fvDL._AC_SL1428_.jpg) | F |
| C × L × A | 215,04 × 90,91 × 17,36; 135 g | https://memoryexpress.com/Products/MX00120812 | L |
| C × L × A | 21,5 × 9,09 × 1,74 cm; 254 g | Amazon (ficha) | L |
| Formato | estádio (pontas em meio círculo de raio ~45); calha central elevada de ~19 de largura, que é o ponto mais alto (17,36) | imagem de cotas | F / E |
| Altura da placa fora da calha | ~8,5 | medido sobre a imagem de cotas | E |
| Centros das bobinas | 2 bobinas, cada uma no meio de uma metade, no eixo da largura (a ~45,5 de cada borda longa) | anéis tracejados da imagem oficial | F (imagem) |
| Centro da bobina até a ponta curta | ~47 (esquerda 47,2; direita 47,0) | medido em pixels na imagem oficial (escala 5,47 px/mm) | E |
| Distância entre centros das bobinas | ~121 | idem | E |
| Diâmetro do anel marcado | ~42 (é o alvo desenhado na superfície, não o tamanho real da bobina) | idem | E |
| Potência | até 10 W por lado, 15 W no total; fonte 24 W; cabo USB-C 1,8 m | Memory Express; https://www.ldlc.com/en/product/PB00278056.html | L |

## 10. Capacitor eletrolítico 1000 µF 16 V

A MakerHero não informa o tamanho. Valores de peças de catálogo com essa especificação:

| Peça | Tamanho | Fonte | Tipo |
|---|---|---|---|
| Panasonic ECA-1CM102 | Ø10 × 16, terminais a 5 | https://octopart.com/part/panasonic/ECA1CM102 | F (via distribuidor) |
| Nichicon UVR1C102MPD | Ø10 × 16, terminais a 5 | https://www.arrow.com/en/products/uvr1c102mpd/nichicon | F (via distribuidor) |
| Nichicon UHV1C102MPD | Ø10 × 16 | https://www.arrow.com/en/products/uhv1c102mpd/nichicon | F (via distribuidor) |
| Panasonic EEU-FM1C102 (105 °C) | Ø10 × 20 | https://www.arrow.com/en/products/eeu-fm1c102/panasonic.html | F (via distribuidor) |

Para o CAD: reservar Ø10,5 × 21 (cobre os dois casos) e medir o que chegou. O terminal sai uns 15 a 20 a mais, a cortar.

## 11. Extras

### Ímã de neodímio disco 15 × 5 N50

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Ø × altura | 15 × 5, tolerância ±0,1 | https://enesmagnets.pl/en/permanent-magnets/neodymium-sintered/cylindrical-magnets/d15-x-5-n38-neodymium-magnet-ndfeb.html (N38) | F |
| Força | ~4,75 kg (N38, contra aço polido, sem folga). Valor de N50 15 × 5 não encontrado; deve ser um pouco maior | Enes Magnets | F |
| Força | 4,34 kg (Eclipse N35, 15 × 5) | https://uk.rs-online.com/web/p/neodymium-magnets/8734981 | F (via distribuidor) |
| Revestimento | Ni-Cu-Ni, magnetização axial | Enes Magnets | F |

Para encaixe impresso: furo Ø15,2 a 15,3 com 5,2 de fundo.

### Etiqueta antifurto rígida (garra e pino)

| Item | Valor | Fonte | Tipo |
|---|---|---|---|
| Diâmetro da haste do pino | ~1,2 ("padrão da indústria"; ranhuras circulares) | patente US9053623B2, https://patents.google.com/patent/US9053623 ; patente CA 2403400, https://brevets-patents.ic.gc.ca/opic-cipo/cpd/eng/patent/2403400/summary.html | C (patente) |
| Comprimento da haste | 16 (mais comum); 19 também existe | https://www.vitag.com.au/products/metal-pin-grooved/ ; listagem chinesa citada em busca | L |
| Cabeça do pino | Ø12 (metal liso), Ø15 (metal abaulado), Ø20 (plástico), Ø13 (listagem chinesa) | https://www.vitag.com.au/products/metal-pin-grooved/ ; https://www.vitag.com.au/products/metal-pin-smooth | L |
| Pino "16 × 11" | 16 de comprimento, 11 provavelmente da cabeça | https://cablematic.com/en/products/pin-anti-theft-eas-rf-82mhz-16x11mm-100-units-XX092/ | L |
| Garra de esferas (ball clutch) | três esferas; graus "Standard, Super, Hyper" | resultados de busca de fornecedores | L |
| Diâmetro e altura da garra (insert) | não encontrado | | medir uma etiqueta real |
| Etiqueta tipo "lápis" | não encontrado | | medir |

## O que mudou em relação à planilha "Medidas x projeto"

- ESP32: a planilha estimava 53 × 28 pela foto. As fontes dão 51,5 a 51,8 × 28,2 a 28,3, com fileiras a 25,4 (agora confirmado por dois footprints KiCad).
- Expansor: a planilha tinha só 16 × 54 × 69. Agora há desenho com 68,6 × 53,4, 4 furos Ø3,4 e as distâncias entre furos.
- SG90 e MG90S: somei furos (27,94 e 28,32 entre centros), espessura da orelha (~2,5), altura da orelha e posição do eixo, de servos medidos (servo_lib).
- Semáforo: a planilha dizia "não informa". Há 56 × 21 × 11 e furos Ø3 no datasheet AZ-Delivery. Falta a distância entre LEDs.
- Power bank: confirmado 149 × 69 × 15 e a posição das portas pela imagem oficial.
- HyperX: confirmado 215 × 91 × 17,4 pela imagem oficial, com bobinas a ~47 de cada ponta.
- Receptor Qi: o 45 × 75 da planilha não foi reconfirmado; tratar como a medir.
