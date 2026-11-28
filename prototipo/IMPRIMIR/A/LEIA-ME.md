# Versão A: o que imprimir e cortar

Duas pastas:

- **`PLA/`**: tudo que vai para a impressora 3D. A carcaça de PLA fica em `PLA/carcaca_PLA/`.
- **`MDF_laser/`**: a carcaça de MDF, só com linhas de corte.

A carcaça é uma ou outra. O resto é sempre PLA.

Para montar, você precisa de:

- cola: super bonder em gel ou epóxi no PLA, cola branca no MDF;
- cola quente, só para o semáforo;
- os parafusos que vêm com o servo.

Nenhum prego e nenhum parafuso extra. A montagem passo a passo está animada na maquete, nas abas "Montar · carcaça PLA" e "Montar · carcaça MDF".

O que foi revisado e o que ainda precisa ser medido está em [REVISAO.md](REVISAO.md).

## Antes de imprimir: medir 3 coisas

1. **Servo.** Meça a altura do topo do braço plástico (já no eixo) até a face de baixo da orelha.
   - O desenho reserva 19 mm.
   - Se der menos, compense com os calços C1 (0,5, 1, 1,5, 2 e 3 mm) embaixo das orelhas, até o topo do braço plástico ficar a 35 mm da prateleira.
2. **MDF** (só se a carcaça for de MDF). Meça a espessura da chapa.
   - O desenho usa 3,0 mm.
   - O fundo e a prateleira já têm 0,3 mm de folga por lado, então a chapa pode ter até 3,3 mm.
3. **Semáforo.** Não precisa medir: ele é colado com cola quente, e a tampa só tem o rasgo dos fios.

## Pasta `PLA/`: impressora 3D (Ender, mesa 220 × 220)

Cada `mesa*.stl` já vem com as peças arrumadas e viradas do jeito certo. Abra no Cura, fatie e imprima uma mesa por vez.

| Ordem | Arquivo | O que tem | Suporte |
|---|---|---|---|
| 0 | `mesa0_teste_de_folga.stl` | furos de 3,6, 3,2 e 3,0 mm em pé e deitados; pinos de 3,2 e 3,0 mm | não |
| 1 | `mesa1_pecas_pequenas.stl` | lingueta (corpo, garfo e haste), braço do servo e pino, dobradiça, eixo da garra, cantos da tampa | não |
| 2 | `mesa2_garra_e_base_do_servo.stl` | garra com dentes; base do servo com o trilho e a coluna da chave (uma peça só) | sim, "tocando a mesa" |
| 3 | `mesa3_pes_batentes_e_suporte_do_esp32.stl` | suporte do expansor do ESP32, 4 pés da prateleira, 5 batentes do power bank, 2 pinos da tampa | não |
| extra | `extra_calcos_do_servo_so_se_precisar.stl` | calços para subir o servo | não |
| reserva | `mesa8_reposicao_pecas_frageis.stl` | 1 jogo a mais das peças que quebram primeiro: eixo (2), pinos da tampa, braço do servo, pino do braço (2), lingueta, dobradiça | não |

**Configuração do Cura:** PLA, camada de 0,2 mm, 3 paredes, 20% de preenchimento, aderência "saia" (skirt). Na mesa 8, use 100% de preenchimento.

**A mesa 0 vai primeiro (cerca de 10 min). Confira:**
- o pino de 3,2 mm gira solto no furo de 3,6 mm, deitado (é o eixo da garra);
- o pino de 3,0 mm entra justo no furo de 3,0 mm (são os pinos da tampa).

Se algum não encaixar, avise antes de imprimir o resto: a folga se ajusta no desenho.

### Carcaça de PLA (`PLA/carcaca_PLA/`)

A caixa tem 230 mm e a mesa da Ender tem 220. Por isso caixa, tampa e prateleira saem em 2 metades. As metades se encaixam num degrau de 10 mm, com 0,3 mm de folga, e são coladas. O corte fica depois da garra e do QR.

| Ordem | Arquivo | O que tem | Suporte |
|---|---|---|---|
| 4 | `mesa4_caixa_esquerda.stl` | metade esquerda da caixa, com o furo do USB do power bank | não |
| 5 | `mesa5_caixa_direita.stl` | metade direita da caixa | não |
| 6 | `mesa6_tampa_e_prateleira_esquerda.stl` | metade esquerda da tampa (de cabeça para baixo) e da prateleira | não |
| 7 | `mesa7_tampa_e_prateleira_direita.stl` | metade direita da tampa e da prateleira (de cabeça para baixo) | não |

Configure o Cura com 4 paredes e 20% de preenchimento. Os cantos C3 (mesa 1) são colados depois da prateleira, igual no MDF.

## Pasta `MDF_laser/`: corte a laser (MDF 3 mm)

Os arquivos têm só as linhas de corte, sem gravação e sem textos. O QR é impresso em papel e colado por cima.

| Arquivo | O que tem |
|---|---|
| `laser1_tampas_3_chapas.svg` | as 3 chapas da tampa. Cole na ordem 3, 2, 1, de baixo para cima, com os furos alinhados. |
| `laser2_prateleira_e_fundo.svg` | prateleira e fundo (223,4 × 85,4 mm, com folga) |
| `laser3_paredes.svg` | 2 paredes longas e 2 curtas. A curta 1 tem o furo do USB do power bank. |

**Escala:** confira no programa do laser. A tampa tem que medir 230 × 92 mm.

**Posição da dobradiça** (não há gravação para marcar):
- a base (14 × 37 mm) fica na mesma linha dos 4 furos dos dentes, 10 mm antes do primeiro furo;
- ela começa a 6 mm da borda curta da tampa e a 4,5 mm da borda longa.
