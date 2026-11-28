# Versão A: o que imprimir e cortar

Duas pastas:

- **`PLA/`**: a impressora 3D, separada em lotes na ordem de impressão.
- **`MDF_laser/`**: a carcaça de MDF, numerada de 1 a 3, só com linhas de corte.

A carcaça é de PLA (lote 5) **ou** de MDF (laser). O resto é sempre PLA.

Para montar, você precisa de:

- cola: super bonder em gel ou epóxi no PLA, cola branca no MDF;
- cola quente para o semáforo e a placa da chave;
- os parafusos que vêm com o servo.

Nenhum prego.

Arquivos de apoio:

- [VERIFICACAO.md](VERIFICACAO.md): os 7 testes automáticos (todos passando).
- [REVISAO.md](REVISAO.md): o que foi corrigido nas 2 revisões.
- A maquete mostra a montagem animada e os testes rodando.

## Antes de começar

1. **Medir o servo** (antes do lote 3). Meça a altura do topo do braço plástico até a face de baixo da orelha.
   - O desenho reserva 19 mm.
   - Se der menos, use os calços (pasta Extra) até o topo do braço plástico ficar a 35 mm da prateleira.
2. **Medir o MDF** (só se a carcaça for de MDF). O desenho usa chapa de 3,0 mm e aceita até 3,2.
3. **Medir onde a chave fim de curso clica.** Aperte a ponta da alavanca com o dedo e meça quanto ela desce até o clique. O desenho aperta 4,4 mm.

## Pasta `PLA/`: um lote por vez

Cada pasta tem o arquivo `.stl` com as peças já arrumadas e viradas, e um `O_QUE_CONFERIR.txt`. Abra o STL no Cura, fatie e imprima. Depois confira as peças antes de passar para o lote seguinte.

| Lote | O que tem | Suporte |
|---|---|---|
| `Lote1_teste_10min` | furos e pinos de teste, em pé e deitados | não |
| `Lote2_pecas_pequenas` | lingueta (corpo, garfo e haste), braço do servo e pino, dobradiça, eixo da garra, cantos da tampa | não |
| `Lote3_garra_e_base_do_servo` | garra com dentes; base do servo com o trilho e a coluna da chave | **sim, "em todo lugar"** |
| `Lote4_pes_batentes_suporte_pinos` | suporte do expansor do ESP32, 4 pés da prateleira, 5 batentes do power bank, 2 pinos da tampa | não |
| `Lote5_carcaca_PLA_so_se_for_PLA` | 4 mesas: caixa, tampa e prateleira em metades (pule se a carcaça for de MDF) | não |
| `Lote6_reposicao_100porcento` | peças de reserva das que quebram primeiro | não |
| `Extra_calcos_so_se_precisar` | 12 pastilhas para baixo das orelhas do servo | não |

**Configuração do Cura:** PLA, camada de 0,2 mm, 3 paredes, 20% de preenchimento, aderência "saia" (skirt). Ajuste por lote:

- **Lote 5:** 4 paredes.
- **Lote 6:** 100% de preenchimento.

## Pasta `MDF_laser/`

| Arquivo | O que tem |
|---|---|
| `1_tampas_3_chapas.svg` | as 3 chapas da tampa. Cole na ordem 3, 2, 1, de baixo para cima, com os furos alinhados. |
| `2_prateleira_e_fundo.svg` | prateleira (com o furo do cabo e o furo do servo) e fundo |
| `3_paredes.svg` | 4 paredes. A curta 1 tem o furo do USB do power bank; a longa 2, o furo do botão. |

**Escala:** confira no programa do laser. A tampa tem que medir 230 × 92 mm.

**Posição da dobradiça** (não há gravação para marcar):
- a base (14 × 37 mm) fica na mesma linha dos 4 furos dos dentes, 10 mm antes do primeiro furo;
- ela começa a 6 mm da borda curta e a 4,5 mm da borda longa.
