# Verificação automática da versão A

Gerado por `prototipo/impressao-3d/verificar.py`. Rodar de novo depois de qualquer mudança.

## ✅ Folgas dos encaixes

- Eixo A7 na garra e na dobradiça: 3.60 para 3.20 → folga +0.20 mm por lado (gira solto)
- Pino C5 no canto C3: 3.00 para 3.00 → folga +0.00 mm por lado (justo: segura a tampa)
- Pino C5 na tampa: 3.20 para 3.00 → folga +0.10 mm por lado (passa)
- Haste A2c no corpo e no garfo: 4.30 para 4.00 → folga +0.15 mm por lado
- Haste A2c no rasgo do chão (largura): 4.80 para 4.00 → folga +0.40 mm por lado
- Pino A3b no rasgo do garfo: 3.40 para 3.00 → folga +0.20 mm por lado
- Pino A3b no furo do A3 (colar): 3.10 para 3.00 → folga +0.05 mm por lado
- Corpo A2a entre as paredes do trilho: 6.80 para 5.60 → folga +0.60 mm por lado
- Garra entre as orelhas da dobradiça: 29.00 para 28.40 → folga +0.30 mm por lado
- Placa da chave entre as abas: 14.30 para 13.70 → folga +0.30 mm por lado
- Corpo do servo no berço (largura): 13.00 para 12.40 → folga +0.30 mm por lado
- Corpo do servo no berço (comprimento): 23.30 para 22.70 → folga +0.30 mm por lado
- Expansor no suporte C7 (largura): 54.00 para 53.40 → folga +0.30 mm por lado
- Prateleira na caixa (comprimento): 224.00 para 223.40 → folga +0.30 mm por lado
- Prateleira na caixa (largura): 86.00 para 85.40 → folga +0.30 mm por lado
- Power bank entre os batentes (comprimento): 151.00 para 149.00 → folga +1.00 mm por lado
- Degrau da carcaça de PLA: 1.80 para 1.50 → folga +0.15 mm por lado

## ✅ Trava: lingueta no entalhe

- Servo em 40°: a lingueta entra 2.0 mm no gancho (o entalhe tem 2,1 mm de fundo)
- Servo em 90°: a lingueta fica 2.6 mm longe do gancho (a garra abre livre)
- Sem pano a garra desce 1.5 mm: a lingueta ainda entra (sobra 0.4 mm)
- Pano grosso: trava com até 4.1 mm de pano embaixo da garra
- Travada, a garra sobe no máximo 1.9 mm e para no topo do entalhe

## ✅ Chave fim de curso

- Garra fechada com pano: o gancho aperta a alavanca 2.8 mm (a micro chave aciona com ~3 ± 1,2 mm)
- Sem pano: 4.3 mm (a alavanca de metal flexiona; sem dano)
- Garra aberta: a alavanca fica solta (checado na varredura abaixo)

## ✅ Movimento sem colisão (garra 0 a 60°, servo 40 a 90°, fios, peças compradas)

- Garra de 3 em 3° e servo de 5 em 5°: nenhuma peça encosta em outra
- Alavanca solta com a garra aberta e apertada com a garra fechada

## ✅ Montagem da lingueta (na ordem)

- Corpo A2a, por cima: entra sem encostar
- Garfo A2b, de lado (+x): entra sem encostar
- Haste A2c, por cima: entra sem encostar
- Pino A3b, por cima: entra sem encostar

## ✅ Pior caso: peças compradas 0,6 mm maiores

- Power bank 0,6 mm maior: cabe
- ESP32 no expansor 0,6 mm maior: cabe
- Servo SG90 0,6 mm maior: cabe
- Chave fim de curso 0,6 mm maior: cabe
- Semáforo 0,6 mm maior: cabe
- Receptor Qi 0,6 mm maior: cabe
- Encaixes justos de propósito (servo no berço, chave nas abas, expansor no suporte, power bank nos batentes) estão nas folgas acima

## ✅ Arquivos de impressão

- Extra_calcos_so_se_precisar/extra_calcos_do_servo_so_se_precisar.stl: 38 × 48 × 3 mm, cabe na mesa, malha fechada
- Lote1_teste_10min/mesa0_teste_de_folga.stl: 56 × 14 × 14 mm, cabe na mesa, malha fechada
- Lote2_pecas_pequenas/mesa1_pecas_pequenas.stl: 195 × 30 × 12 mm, cabe na mesa, malha fechada
- Lote3_garra_e_base_do_servo/mesa2_garra_e_base_do_servo.stl: 81 × 108 × 48 mm, cabe na mesa, malha fechada
- Lote4_pes_batentes_suporte_pinos/mesa3_pes_batentes_e_suporte_do_esp32.stl: 134 × 74 × 18 mm, cabe na mesa, malha fechada
- Lote5_carcaca_PLA_so_se_for_PLA/mesa4_caixa_esquerda.stl: 168 × 92 × 72 mm, cabe na mesa, malha fechada
- Lote5_carcaca_PLA_so_se_for_PLA/mesa5_caixa_direita.stl: 72 × 92 × 72 mm, cabe na mesa, malha fechada
- Lote5_carcaca_PLA_so_se_for_PLA/mesa6_tampa_e_prateleira_esquerda.stl: 168 × 185 × 9 mm, cabe na mesa, malha fechada
- Lote5_carcaca_PLA_so_se_for_PLA/mesa7_tampa_e_prateleira_direita.stl: 72 × 185 × 9 mm, cabe na mesa, malha fechada
- Lote6_reposicao_100porcento/mesa8_reposicao_pecas_frageis.stl: 183 × 32 × 18 mm, cabe na mesa, malha fechada
- Cada peça sai inteira (um pedaço só por peça)
