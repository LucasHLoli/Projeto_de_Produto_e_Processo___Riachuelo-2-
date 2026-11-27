# Peças para imprimir (Ender, PLA) e cortar (MDF)

Os STL estão em `stl/`, já deitados na posição de imprimir. O SVG do MDF está em `mdf/`.
As medidas da etiqueta (copinho de metal e pino) são estimativas até alguém medir. Por isso a ordem abaixo importa.

## Configuração da Ender (Cura)

- PLA, bico 0,4 mm, camada 0,2 mm, preenchimento 20 %, 3 paredes.
- Mesa 60 °C, bico 200 °C.
- Suporte: **desligado** em todas, menos onde está escrito.
- Aderência: saia (skirt). Na caixa e na tampa use borda (brim) de 5 mm para não descolar a ponta.

## Ordem de impressão

| # | Arquivo | Tempo aprox. | Para quê | Observação |
|---|---|---|---|---|
| 1 | `01_teste_encaixe.stl` | 40 min | Descobrir qual furo serve para o copinho e para os ímãs | Imprima **antes de tudo**. Os entalhes na borda dizem o furo: 1 risco = mais justo |
| 2 | `02_calcos_servo.stl` | 10 min | Calços de 0,5 a 2 mm para acertar a altura do servo | — |
| 3 | `04_braco_imas.stl` | 15 min | Leva os 3 ímãs até embaixo do copinho | Encaixa por cima do braço plástico do servo |
| 4 | `03b_berco_embreagem.stl` | 20 min | Segura o copinho de metal sobre uma parede de 0,8 mm | A face lisa (prateleira) fica na mesa |
| 5 | `03_mecanismo.stl` | 2 h 30 | Segura o servo e a torre do berço | — |
| 6 | `07_garra.stl` | 1 h | Garra que leva o pino e prende a roupa | — |
| 7 | `09_pino_chave.stl` | 5 min | Pino que a garra empurra para acionar a chave | Imprima 2 |
| 8 | `08_prateleira_esp32.stl` | 1 h 30 | Prateleira do ESP32 por cima do power bank | Já vem de cabeça para baixo |
| 9 | `06_tampa.stl` | 4 h | Tampa com furo do pino, janela dos LEDs, QR e dobradiça | Orelhas da dobradiça para cima |
| 10 | `05_caixa.stl` | 9 a 11 h | Caixa de 210 × 76 × 61 mm | Deixar de noite. Brim 5 mm |

Tempos são estimativas para 50 mm/s; o Cura mostra o real.

## Depois de medir a etiqueta

1. Meça o copinho, o pino e a cabeça do pino com paquímetro.
2. Abra `gerar_pecas.py` e troque as linhas marcadas `MEDIR` no topo.
3. Rode `python gerar_pecas.py` (precisa de `pip install manifold3d trimesh matplotlib`). Os STL são refeitos.
4. Se o furo certo da peça de teste foi o 3 ou o 4, aumente `EMBREAGEM_D` em 0,3 ou 0,6.

## MDF (`mdf/base_exposicao.svg`)

- MDF 3 mm. Vermelho = cortar, preto = gravar.
- Duas placas de 300 × 200 mm. A de cima tem o recorte da base Qi (216 × 92 mm) e o rasgo do cabo. Cole a de cima sobre a de baixo com cola branca e prenda com grampos por 1 h.

## Parafusos que vocês precisam

- 4 × M3 de 8 mm: mecanismo no fundo da caixa.
- 1 × M3 de 12 mm: berço da embreagem na torre.
- 2 × M3 de 12 mm: tampa na caixa.
- 1 × M3 de 40 mm com porca: eixo da garra.
- Os 2 parafusos pequenos que vêm com o servo: servo no mecanismo.
