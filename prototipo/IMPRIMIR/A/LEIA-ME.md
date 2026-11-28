# Versão A: o que imprimir e cortar

Tudo que não foi comprado é impresso em PLA. A carcaça tem duas opções: PLA (pasta `carcaca_PLA/`) ou MDF no laser. Para montar: cola e os 2 parafusos que vêm com o servo. Nenhum prego, nenhum parafuso extra.

A montagem passo a passo está animada na maquete (abas "Montar · carcaça PLA" e "Montar · carcaça MDF").

## Impressora 3D (Ender, PLA)

Cada `mesa*.stl` já vem com as peças arrumadas e viradas: abra no Cura e fatie. Uma mesa por vez.

| Ordem | Arquivo | O que tem | Suporte |
|---|---|---|---|
| 0 | `mesa0_teste_de_folga.stl` | teste: furos de 3,6, 3,2 e 3,4 mm e um pino de 3,2 mm | não |
| 1 | `mesa1_pecas_pequenas.stl` | lingueta (2 partes), braço, dobradiça, eixo, cantos da tampa, pinos da tampa e do semáforo | não |
| 2 | `mesa2_garra_e_base_do_servo.stl` | garra com dentes e base do servo com trilho | sim, "tocando a mesa" |
| 3 | `mesa3_pes_batentes_e_suporte_do_esp32.stl` | suporte do expansor do ESP32, 4 pés da prateleira, 6 batentes do power bank | não |
| só se precisar | `extra_calcos_do_servo_so_se_precisar.stl` | calços para subir o servo | não |

**Mesa 0 primeiro (10 min).** O pino de 3,2 mm tem que girar solto no furo de 3,6 (é o eixo da garra) e entrar justo no de 3,2. Se não entrar no de 3,6, avise antes de imprimir o resto: dá para ajustar a folga.

Cura: PLA, camada 0,2 mm, preenchimento 20%, 3 paredes, aderência "saia" (skirt).

Antes da mesa 2, meça com o paquímetro a altura do topo do braço plástico do servo até a base da orelha. O desenho usa no máximo 17 mm. Se der mais, avise antes de imprimir.

### Carcaça de PLA (pasta `carcaca_PLA/`)

A caixa tem 230 mm e a mesa da Ender tem 220, então caixa, tampa e prateleira saem em 2 metades, que encaixam num degrau de 10 mm e são coladas (super bonder em gel ou epóxi).

| Ordem | Arquivo | O que tem | Suporte |
|---|---|---|---|
| 4 | `mesa4_caixa_esquerda.stl` | metade esquerda da caixa (lado da garra), já com o canto do pino da tampa | não |
| 5 | `mesa5_caixa_direita.stl` | metade direita da caixa | não |
| 6 | `mesa6_tampa_e_prateleira_esquerda.stl` | metade esquerda da tampa (de cabeça para baixo) e da prateleira | não |
| 7 | `mesa7_tampa_e_prateleira_direita.stl` | metade direita da tampa e da prateleira (de cabeça para baixo) | não |

Paredes de 3 mm: no Cura, 4 paredes e 20% de preenchimento. Com a carcaça de PLA os cantos C3 da mesa 1 sobram (já vêm na caixa).

## Laser (MDF 3 mm), se a carcaça for de MDF

Os arquivos têm só as linhas de corte. O QR é impresso em papel e colado por cima depois.

| Arquivo | O que tem |
|---|---|
| `laser1_tampas_3_chapas.svg` | as 3 chapas da tampa (cole na ordem 3, 2, 1, de baixo para cima, com os furos alinhados) |
| `laser2_prateleira_e_fundo.svg` | prateleira e fundo |
| `laser3_paredes.svg` | 2 paredes longas e 2 curtas |

Confira a escala no programa do laser: a tampa tem que medir 230 × 92 mm. Sem gravação, a dobradiça se posiciona assim: a base (14 × 37 mm) fica alinhada com os 4 furos dos dentes, na mesma linha, a 10 mm antes do primeiro furo. Ela começa a 6 mm da borda curta da tampa e a 4,5 mm da borda longa.
