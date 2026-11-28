# Revisão de qualidade da versão A (28/11/2026)

A revisão foi feita em duas frentes: um revisor independente leu o projeto do zero, e eu conferi com cálculo e checagem de colisão. A checagem final de colisão da versão A (peças compradas, fios, garra de 0 a 60° e servo de 40 a 90°) **não acusou nenhum problema**. A montagem da lingueta também foi simulada peça por peça, e todas entram pelo caminho previsto.

## Corrigido

| Problema | O que mudou |
|---|---|
| A lingueta não montava. O corpo não passava entre as abas e o garfo não entrava com o servo no lugar. | As abas saíram. A haste virou peça separada (A2c, quadrada, 4 × 4 mm) e o pino do braço também (A3b). Ordem: corpo por cima, garfo de lado, haste por cima, pino por cima. |
| A coluna da chave saía como peça solta, com as abas no ar e só 0,1 mm de folga para a placa. | A coluna agora é ligada à base por uma faixa e as abas nascem da própria coluna. A placa da chave tem 0,3 mm de folga por lado. |
| A trava só engatava com pano de certa espessura (entalhe de 3 mm). | Entalhe de 5,7 mm: engata sem pano, com pano fino e com pano grosso. |
| A chave fim de curso recebia só 1,3 mm de aperto, e a micro chave precisa de uns 3 mm. | Aperto de 2,8 mm. O trilho da lingueta subiu 1 mm para a alavanca passar por baixo. |
| A garra corria 4,5 mm de lado no eixo. | A junta da garra ficou mais larga (0,3 mm de folga para as orelhas). A base da dobradiça foi de 0,3 para 0,8 mm. |
| O desenho reservava 17 mm de altura para o servo; o medidas.md pede 19. | O desenho agora reserva 19 mm, e os calços C1 sobem o servo se ele for mais baixo. |
| O braço A3 não tinha encaixe no braço plástico. | O A3 ganhou um canal com o formato do braço plástico e um furo rebaixado para o parafuso pequeno do servo. |
| Os furos do semáforo estavam numa posição não confirmada. | Os furos saíram. O semáforo é colado com cola quente e a tampa fica só com o rasgo dos fios. |
| Fundo e prateleira tinham 224 × 86 mm, sem folga. | 223,4 × 85,4 mm: cabem até com MDF de 3,3 mm. |
| Na carcaça de PLA, os cantos bloqueavam a prateleira e havia partes no ar. | Os cantos ficaram separados (C3). Cada metade nasce na mesa. Folga de 0,3 mm. O corte foi movido para depois do QR. |
| O eixo A7 em pé (46 mm sobre Ø3,2) ia balançar na impressão. | Ele agora imprime deitado, com uma face plana. |
| A tampa ficava solta nos pinos. | Os furos dos cantos foram para 3,0 mm: o pino entra justo. |
| Não dava para carregar o power bank sem desmontar. | Furo de 14 × 10 mm na parede curta esquerda, na frente do USB-C do power bank. |
| Um batente tapava uma porta USB do power bank. | O batente saiu: agora são 5. |
| A peça de teste não testava furos deitados nem o pino de 3,0 mm. | O teste agora tem furos deitados de 3,6 e 3,2 mm e pinos de 3,2 e 3,0 mm. |
| A animação trocava as mesas (base e lingueta). | Corrigido. |

## Ainda depende de vocês (não dá para resolver só no desenho)

1. **Medir o servo** antes da mesa 2: a altura do braço plástico até a orelha. O desenho reserva 19 mm; com menos que isso, usem os calços.
2. **Sentido do servo.** Antes de colocar o garfo, testem com o firmware: o comando `t` (40°) tem que levar o pino do braço na direção do gancho. Se for para o outro lado, troquem no firmware para `ANG_TRAVA = 140` e `ANG_SOLTA = 90`.
3. **Chave fim de curso.** Ela deve dar o clique antes de a garra fechar por completo. Se não clicar, ponham papelão ou um calço fino embaixo da placa.
4. **Rabicho do receptor Qi:** precisa alcançar uns 25 a 30 mm até o micro-USB do power bank. Medir.
5. **Power bank:** testar 1 hora com o ESP32 ligado. Alguns power banks desligam sozinhos quando a corrente é baixa.
6. **Destravar sem bateria:** ligue um cabo USB no power bank pelo furo da parede e mande liberar pelo app ou pelo monitor serial.
7. **Versão B:** continua parada até chegar a etiqueta e passar no teste do ímã.
