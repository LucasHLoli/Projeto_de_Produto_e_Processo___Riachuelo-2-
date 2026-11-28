# Protótipo v2: o que cortar, imprimir e montar

Esta é a versão a usar. As pastas `stl/`, `stl_mdf/`, `stl_cabo/`, `stl_lingueta/` e `stl_dentes/` são versões antigas.

Gerado por `tagandgo_v2.py`. Medidas das peças compradas e fontes: `research_notes/Medidas reais/medidas.md`.
O script simula todas as peças que se mexem e confere que nada bate em nada antes de gerar os arquivos.

## Caixa (as duas versões)

- MDF 3 mm. Interna 194 × 146 × 48,5 mm. Externa 200 × 152 × 51,5 mm.
- O fundo fica **dentro** das 4 paredes; as paredes curtas ficam entre as longas. Cola branca e fita crepe até secar.
- Dentro, nada fica empilhado:
  - power bank (149 × 69 × 15) deitado sobre o receptor Qi, com o USB virado para o espaço vazio da esquerda e o micro-USB virado para a parede da frente;
  - ESP32 no expansor (68,6 × 53,4) no canto de trás à esquerda;
  - mecanismo no canto de trás à direita;
  - semáforo colado embaixo da tampa, na janela dos LEDs.
- Os batentes (C2) colados no fundo seguram o power bank e o expansor.

## Versão A: garra com dentes (principal)

| Arquivo | Para quê | Como imprimir |
|---|---|---|
| `mdf/caixa_v2_A.svg` | 3 tampas, fundo e 4 paredes | laser; as 3 tampas têm furos diferentes (seguem o arco do dente). Colar na ordem 3, 2, 1 de baixo para cima |
| `A1_base_servo_e_trilho` | berço do servo, pilares e trilho da lingueta | como está |
| `A2a_lingueta_corpo` + `A2b_lingueta_garfo` | lingueta em 2 partes | colar a haste do garfo no furo quadrado do corpo |
| `A3_braco_biela` | braço com pino; vai em cima do braço plástico do servo | como está |
| `A4_garra_dentes` | garra com 4 dentes e gancho | já vem de cabeça para baixo |
| `A5_dobradica` | colada na tampa (marca gravada) | como está |
| `A6_pino_da_chave` | a garra empurra, ele aperta a chave por baixo da tampa | já vem de cabeça para baixo |

Eixo da garra: prego fino ou palito de churrasco de até 3 mm.
Chave fim de curso: colada embaixo da tampa, com a alavanca embaixo do pino da chave.
Servo: 40° trava, 90° solta. A lingueta anda 4,6 mm.

## Versão B: etiqueta de loja + ímãs (reserva)

| Arquivo | Para quê |
|---|---|
| `mdf/caixa_v2_B.svg` | 1 tampa, fundo e 4 paredes |
| `B5_teste_embreagem` | **imprimir primeiro**: 4 furos para descobrir o tamanho certo da embreagem |
| `B1_base_servo` | berço do servo |
| `B2_braco_imas` | braço; 2 ímãs 15 × 5 presos com parafuso M3 × 16 e porca embaixo |
| `B3_capsula_embreagem` + `B4_anel_capsula` | a embreagem fica dentro; o anel é colado por cima |

Servo: 0° repouso (ímãs a 31 mm da embreagem), 120° solta (ímãs a 0,2 mm embaixo do fundo da cápsula).

## Comuns

- `C1_calcos_servo`: 0,5 / 1 / 1,5 / 2 / 3 mm. Vão embaixo das orelhas do servo para acertar a altura do braço.
- `C2_batentes_x6`: param o power bank e o expansor.
- `C3_cantos_tampa_x2`: colados por dentro, na altura do topo da parede, para os 2 parafusos da tampa.

## Ender (Cura)

PLA, bico 0,4, camada 0,2, 20 % de preenchimento, 3 paredes, sem suporte, saia (skirt).

## Medir antes de imprimir (paquímetro)

O que a internet não respondeu. Se algum valor for diferente, mudar no topo de `tagandgo_v2.py` e rodar de novo.

1. **Servo:** altura do topo do braço plástico acima da base da orelha (o script usa no máximo 17 mm; se der menos, usar calços).
2. **Semáforo:** distância entre os LEDs (hoje a tampa tem uma janela única, que serve para qualquer distância).
3. **Chave fim de curso:** altura da alavanca.
4. **Receptor Qi:** tamanho da folha e comprimento do rabicho.
5. **Versão B:** diâmetro e altura da embreagem da etiqueta (usar o `B5_teste_embreagem`).
