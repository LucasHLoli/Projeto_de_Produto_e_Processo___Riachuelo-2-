# Guia de montagem do protótipo (sem solda)

Versão de 07/10/2026. Nada aqui foi montado nem testado ainda. As medidas são ponto de partida para o modelo 3D.

## O que o protótipo faz

1. O pino atravessa a roupa e entra na embreagem de uma etiqueta de loja. Fica preso sem gastar energia.
2. Um sensor avisa o ESP32 que o pino entrou. O LED fica vermelho, e o servidor registra "travado".
3. O cliente encosta o celular no adesivo NFC, abre a página e paga.
4. O servidor manda soltar. O servo aproxima um ímã da embreagem, e o pino sai. O LED fica verde.
5. A caixa vai para a base de indução e recarrega.

## Lista de compra

| # | Item | Qtd | Preço | Loja |
|---|---|---|---|---|
| 1 | Etiquetas rígidas com pino, 20 un. | 1 | R$ 67,78 | https://www.amazon.com.br/dp/B0GP6ZF16R |
| 2 | Ímãs de neodímio N50 10 x 4 mm, 10 un. | 1 | R$ 21,48 | https://www.usinainfo.com.br/imas-de-neodimio-e-acessorios-magneticos/ima-de-neodimio-n50-super-forte-10mm-x-4mm-kit-com-10-unidades-5012.html |
| 3 | ESP32 com USB-C | 1 | R$ 56,81 | https://www.usinainfo.com.br/esp32/esp32-wifi-e-bluetooth-com-usb-c-30-pinos-e-cp2102-9114.html |
| 4 | Microservo SG90 | 2 | R$ 28,32 | https://www.usinainfo.com.br/servo-motores/micro-servo-motor-9g-sg90-180-16kgfcm-de-posicao-2299.html |
| 5 | Módulo chave fim de curso | 2 | R$ 9,58 | https://www.usinainfo.com.br/sensor-de-vibracao/modulo-chave-fim-curso-sensor-de-impacto-para-projetos-4618.html |
| 6 | Semáforo de LED | 1 | R$ 7,78 | https://www.usinainfo.com.br/outros-modulos-arduino/semaforo-led-33v5v-8mm-s3-5466.html |
| 7 | Jumpers macho-fêmea | 1 | R$ 8,46 | https://www.eletrogate.com/jumpers-macho-femea-40-unidades-de-20-cm |
| 8 | Jumpers fêmea-fêmea | 1 | R$ 7,50 | https://www.eletrogate.com/jumpers-femea-femea-40-unidades-de-20-cm |
| 9 | Protoboard 400 pontos | 1 | R$ 8,46 | https://www.eletrogate.com/protoboard-400-pontos |
| 10 | Receptor Qi (micro USB ou USB-C, conforme o power bank) | 1 | R$ 24,90 ou R$ 67,93 | Kabum (micro USB) ou Magalu (USB-C) |
| 11 | Base de carregador sem fio | 1 | R$ 28,69 | https://www.magazineluiza.com.br/carregador-por-inducao-15w-sem-fio-usb-acompanha-cabo-usb-c-le520-lelong/p/ke9dh49dk3/te/accp/ |
| 12 | Adesivos NFC, 10 un. | 1 | R$ 23,90 | https://www.amazon.com.br/dp/B0CKTK9HSJ |
| 13 | Kit de parafusos e porcas M2 a M5 | 1 | R$ 18,72 | https://www.amazon.com.br/dp/B0GS5M3LC5 |
| 14 | Travas magnéticas avulsas (opcional) | 1 | R$ 91,86 | https://www.amazon.com.br/dp/B07GZH682Y |

Total sem o item 14 e com receptor micro USB: cerca de R$ 312. Fretes à parte.

Já devem ter: power bank pequeno, carregador de celular, cabo USB-C, fita dupla face, cola instantânea.

Preços: itens 2, 4, 5, 13 e 14 vistos em 06 e 07/10. Os demais, em 29 e 30/09. O item 14 só foi visto pelo título do anúncio.

## Etapa 0: teste de bancada (antes de imprimir qualquer coisa)

Precisa só dos itens 1 e 2.

1. Prenda uma etiqueta num pedaço de tecido. Puxe e veja que não solta.
2. Encoste um ímã na parte abaulada da etiqueta e puxe o pino. Se não sair, empilhe dois, três, quatro ímãs.
3. Anote quantos ímãs foram precisos e a que distância ainda funciona (0, 1, 2, 3 mm).
4. Abra uma etiqueta (serra ou alicate, com óculos de proteção). Tire a embreagem inteira: é um copinho de metal com esferas, uma peça central e uma mola.
5. Repita o teste do ímã direto na embreagem, sem o plástico.

Deu certo quando: o pino sai com os ímãs encostados na embreagem. Isso decide o projeto.
Se não sair de jeito nenhum: o plano muda para a lingueta com gancho (ver `montagem-sem-solda.png`).

## Etapa 1: eletrônica na protoboard

Ligações, todas com jumper:

| Peça | Pino da peça | Pino do ESP32 |
|---|---|---|
| Servo | fio marrom (terra) | GND |
| Servo | fio vermelho (5 V) | VIN |
| Servo | fio laranja (sinal) | GPIO 13 |
| Chave fim de curso | VCC | 3V3 |
| Chave fim de curso | GND | GND |
| Chave fim de curso | OUT | GPIO 27 |
| Semáforo | GND | GND |
| Semáforo | R (vermelho) | GPIO 26 |
| Semáforo | G (verde) | GPIO 25 |

O ESP32 é alimentado pelo cabo USB-C, primeiro no notebook e depois no power bank.

Teste nesta ordem, um por vez:
1. LED vermelho e verde piscando.
2. Apertar a chave fim de curso troca o LED de verde para vermelho.
3. O servo vai de 0 a 90 graus e volta.

Deu certo quando: os três funcionam juntos com o ESP32 ligado no power bank, sem o ESP32 reiniciar quando o servo se mexe.

## Etapa 2: servidor e página

O que o servidor precisa ter:
- cadastro: caixa, produto e preço;
- página do cliente, aberta pelo adesivo NFC, com o produto e o botão de pagar;
- pagamento simulado (um botão) e, se sobrar tempo, Pix de teste;
- fila de comandos: a caixa pergunta a cada 1 a 2 s se há ordem;
- painel: estado de cada caixa (travada, paga, liberada, fora do ar) e histórico.

Os prompts para gerar o servidor e o firmware estão em `mvp-trava-pronta.md`. Troque a parte do relé e da fechadura por: "ao receber o comando de soltar, mover o servo do GPIO 13 para 90 graus por 2 s e voltar a 0".

Deu certo quando: apertar "pagar" no celular faz o servo se mexer em até 3 s.

## Etapa 3: peças impressas em 3D

Imprima primeiro só as peças 1 e 2, para acertar o mecanismo. A caixa vem depois.

| # | Peça | Função | Medida de partida |
|---|---|---|---|
| 1 | Berço da embreagem | Segura a embreagem parada, com o furo do pino para cima | Furo com o diâmetro da embreagem mais 0,3 mm de folga |
| 2 | Braço do ímã | Encaixa no eixo do servo e leva o ímã até encostar na embreagem | Braço de 15 a 20 mm, com rebaixo de 10 x 4 mm para o ímã |
| 3 | Suporte do servo | Fixa o servo ao lado do berço | O SG90 mede cerca de 23 x 12 x 29 mm |
| 4 | Apoio da chave fim de curso | Põe a chave onde a ponta do pino encosta | Ajustar depois de medir o pino |
| 5 | Base da caixa | Recebe tudo. Fundo fino sobre o receptor de indução | Cerca de 110 x 75 x 45 mm. Fundo de 1,5 a 2 mm na área do receptor |
| 6 | Tampa | Furo do pino, janelas dos LEDs, lugar do adesivo NFC | Mesma planta da base |

Cuidados:
- O ímã, em repouso, fica longe da embreagem. Quanto longe? O valor medido na etapa 0, mais uma folga.
- O ímã e a embreagem ficam afastados do receptor de indução (pelo menos 3 cm). Metal e ímã perto da bobina atrapalham a carga.
- Meça as peças de verdade com paquímetro antes de modelar. As medidas acima são aproximadas.
- Conte com duas ou três impressões das peças 1 e 2.

Deu certo quando: com a embreagem no berço, o servo leva o ímã, o pino sai, o servo volta e o pino trava de novo ao ser empurrado.

## Etapa 4: indução

1. Ligue o receptor Qi na entrada de carga do power bank.
2. Ponha o receptor sobre a base, com uma chapa de plástico de 2 mm no meio.
3. Veja se o power bank indica que está carregando.
4. Repita com o ESP32 ligado na saída do power bank.

Deu certo quando: o power bank carrega através do plástico e o ESP32 continua ligado (ou reinicia e volta sozinho).

## Etapa 5: juntar tudo

1. Cole o receptor Qi no fundo da caixa, por dentro, com fita dupla face.
2. Fixe o power bank e o ESP32 (com a protoboard) na base.
3. Parafuse o berço da embreagem, o suporte do servo e o apoio da chave.
4. Passe os jumpers e prenda os fios longe do braço do servo.
5. Feche a tampa. Cole o adesivo NFC e grave nele o endereço da página daquela caixa.
6. Faça o ciclo completo dez vezes seguidas: prender, cadastrar, pagar, soltar, recarregar.

Deu certo quando: os dez ciclos passam sem abrir a caixa.

## O que este protótipo não é

- Não é do tamanho de uma etiqueta. É uma caixa de uns 11 x 7,5 x 4,5 cm.
- Um destacador de loja abre a embreagem por fora. No produto final, o carretel não magnético e o came mecânico resolvem isso.
- Não mede o nível da bateria.
- Depende de Wi-Fi.
