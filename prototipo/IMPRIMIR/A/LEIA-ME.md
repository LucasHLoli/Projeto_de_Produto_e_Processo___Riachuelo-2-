# Versão A: o que imprimir e cortar

## Impressora 3D (Ender, PLA)

Cada arquivo `mesa*.stl` já vem com as peças arrumadas e viradas do jeito certo: é só abrir no Cura e fatiar. Imprima uma mesa por vez. Se algo der errado, você perde só aquela mesa.

| Ordem | Arquivo | O que tem | Suporte |
|---|---|---|---|
| 1 | `mesa2_pecas_pequenas.stl` | lingueta (2 partes), braço, dobradiça, eixo, cantos da tampa, pinos da tampa e do semáforo | não |
| 2 | `mesa1_garra_e_base.stl` | garra com dentes e base do servo com trilho | sim, "tocando a mesa" |
| 3 | `mesa3_pes_da_prateleira.stl` | 4 pés da prateleira | não |
| só se precisar | `extra_calcos_do_servo_so_se_precisar.stl` | calços para subir o servo | não |

A mesa 2 vai primeiro porque é rápida (menos de 5 cm³ de plástico) e serve de teste para a impressora.

Cura: PLA, camada 0,2 mm, preenchimento 20%, 3 paredes, aderência "saia" (skirt). O tempo de cada mesa aparece no Cura depois de fatiar.

Antes de imprimir a mesa 1, meça com o paquímetro a altura do topo do braço plástico do servo até a base da orelha. O desenho usa no máximo 17 mm. Se der mais, avise antes de imprimir.

## Carcaça: escolha MDF ou PLA

As duas têm as mesmas medidas (230 × 92 × 71,5 mm por fora, mais 9 mm de tampa). Por dentro muda nada.

### Carcaça de PLA (pasta `carcaca_PLA/`)

A caixa tem 230 mm e a mesa da Ender tem 220, então caixa, tampa e prateleira saem em 2 metades. As metades encaixam num degrau de 10 mm e você cola com cola de PLA (super bonder em gel ou epóxi).

| Ordem | Arquivo | O que tem | Suporte |
|---|---|---|---|
| 4 | `mesa4_caixa_esquerda.stl` | metade esquerda da caixa (lado da garra), já com o canto do pino da tampa | não |
| 5 | `mesa5_caixa_direita.stl` | metade direita da caixa | não |
| 6 | `mesa6_tampa_e_prateleira_esquerda.stl` | metade esquerda da tampa (de cabeça para baixo) e da prateleira | não |
| 7 | `mesa7_tampa_e_prateleira_direita.stl` | metade direita da tampa e da prateleira (de cabeça para baixo) | não |

Paredes de 3 mm: no Cura, use 4 paredes (0,4 mm cada) e 20% de preenchimento. As 4 mesas somam ~430 cm³ de peça; com 20% de preenchimento gasta bem menos que isso de filamento (o Cura mostra os gramas).

Com a carcaça de PLA não precisa dos cantos C3 da mesa 2 (eles já vêm na caixa). Pode imprimir assim mesmo e guardar.

## Laser (MDF 3 mm), se a carcaça for de MDF

Vermelho = cortar. Preto = gravar. Cada arquivo cabe numa chapa de cerca de 240 × 320 mm.

| Arquivo | O que tem |
|---|---|
| `laser1_tampas_3_chapas.svg` | as 3 chapas da tampa (cole na ordem 3, 2, 1, de baixo para cima) |
| `laser2_prateleira_e_fundo.svg` | prateleira e fundo |
| `laser3_paredes.svg` | 2 paredes longas e 2 curtas |

Ao abrir no programa do laser, confira se a escala ficou em milímetros: a tampa tem que medir 230 × 92 mm.
