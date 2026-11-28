# Ligações do protótipo (v3)

Tudo sem solda, com os jumpers fêmea-fêmea do pedido e o cabo do próprio servo.
O expansor tem, para cada GPIO, uma coluna de 3 pinos: **S** (sinal), **V** (tensão) e **G** (terra).

## Antes de ligar

1. **Jumper de tensão do expansor em 5 V.** É o V que alimenta o servo.
2. **O power bank liga no USB-C do expansor**, e não no do ESP32. O expansor alimenta o ESP32 e o 5 V do servo.
3. **A fileira de cada pino:** confira na serigrafia do expansor qual é S, V e G. Em geral a ordem, de dentro para fora, é S, V, G.

## Tabela

| Peça | Fio da peça | Vai em | Observação |
|---|---|---|---|
| Servo SG90 | laranja | S do GPIO 13 | o conector do servo já encaixa nas 3 vias |
| Servo SG90 | vermelho | V do GPIO 13 | 5 V |
| Servo SG90 | marrom | G do GPIO 13 | |
| Chave fim de curso | OUT | S do GPIO 27 | |
| Chave fim de curso | GND | G do GPIO 27 | |
| Chave fim de curso | VCC | **não ligar** | O V está em 5 V, e o ESP32 queima com 5 V no pino. O firmware usa o pull-up interno. |
| Semáforo | R | S do GPIO 26 | |
| Semáforo | Y | S do GPIO 33 | |
| Semáforo | G | S do GPIO 25 | |
| Semáforo | GND | G do GPIO 26 | |
| Capacitor 1000 µF | + (perna longa) | V do GPIO 12 | Segura o pico de corrente do servo. A faixa branca é o −. |
| Capacitor 1000 µF | − (lado da faixa) | G do GPIO 12 | |
| Power bank | USB-A | USB-C do expansor | Cabo USB-A para USB-C de uns 30 cm, passando pelo furo da prateleira. |
| Receptor Qi | micro-USB | entrada micro-USB do power bank | Folha embaixo do power bank. |

Os pinos são os mesmos do plano de software (`prototipo/software/plano-desenvolvimento.md`).

## Onde cada fio passa (maquete)

- **Semáforo:** fica parafusado **em cima** da tampa, com 2 parafusos M3 e porca. Os 4 jumpers descem pelo rasgo ao lado dele e correm encostados na parede de trás.
- **Chave (versão A):** fica colada embaixo da tampa, com a alavanca embaixo do pino da chave. Os 2 fios correm pela frente da prateleira.
- **Cabo do servo:** sai pela ponta do berço e corre pela frente da prateleira até o GPIO 13.
- **Capacitor:** fica deitado na prateleira, atrás do expansor.

A simulação confere que nenhum fio encosta na garra, no braço do servo, na lingueta ou nos ímãs em todo o movimento.

## Primeiro teste

Grave `prototipo/firmware/teste_bancada/teste_bancada.ino`, abra o Monitor Serial a 115200 e siga a ordem:

1. Os LEDs piscam vermelho, amarelo e verde.
2. Ao apertar a chave, aparece "chave: apertada". Se aparecer ao contrário, troque `NIVEL_APERTADA`.
3. **Versão A:** fechar a garra trava sozinho (40°, LED vermelho). Digitar `l` libera (90°, LED verde).
4. **Versão B:** digitar `l` leva os ímãs para baixo da embreagem (120°) e `t` volta para o repouso.

**Atenção (versão A) para o Pedro:** depois de liberar, o servo deve **ficar** em 90° até a garra abrir e fechar de novo. Se ele voltar para 40° sozinho, ele trava a garra outra vez. Isso difere do passo 4 do plano de software, que manda voltar a 0°.
