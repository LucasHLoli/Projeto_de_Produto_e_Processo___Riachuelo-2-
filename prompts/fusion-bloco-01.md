# FUSION 360 via MCP — BLOCO 1 de 7
## Parâmetros de usuário + contorno mestre + sólido mestre

---

## Por que dividir em blocos

Um agente MCP executando 200 linhas de CAD de uma vez erra no meio e você não descobre onde.
Cada bloco abaixo é curto, termina num estado **verificável**, e só depois você manda o próximo.

| Bloco | Conteúdo | Depende de medição? |
|---|---|---|
| **1** | **parâmetros + contorno mestre + sólido mestre** | **não — pode rodar hoje** |
| 2 | casca, divisão em duas metades, fechamento por parafuso | não |
| 3 | alojamento da garra | **sim** — precisa de `d_garra`, `h_garra` |
| 4 | berço da alavanca + âncoras do fio SMA | sim — precisa de `curso_garra` |
| 5 | baias da eletrônica, contatos, rasgo do inlay | sim — precisa medir as placas |
| 6 | alavanca bell crank + haste empurradora | sim |
| 7 | montagem, juntas, verificações, exportação | — |

Blocos 1 e 2 rodam **agora**. Do 3 em diante, só depois do ensaio da semana 1 (`03-destravamento.md`, §5.1).

---

# ⬇️ COPIE DAQUI PARA BAIXO E COLE NO MCP

Você está operando o Autodesk Fusion 360. Execute exatamente os passos abaixo, na ordem.
Não improvise geometria. Ao terminar, responda com o relatório do item 5.

## Contexto

Estou modelando a carcaça de um protótipo de etiqueta antifurto de roupa. Este é o primeiro
de sete blocos: só a geometria mestra do envelope externo. Não modele nada além do pedido.

## Passo 1 — Criar o documento

Crie um novo documento de projeto chamado **`TagAndGo_Prototipo`**.
Unidades: **milímetro**. Mantenha o histórico (timeline) ativo.

## Passo 2 — Criar os Parâmetros de Usuário

Em *Modify → Change Parameters → User Parameters*, crie **todos** os parâmetros abaixo, com
estes nomes exatos. Todos em milímetro, exceto os marcados como adimensionais.

**Envelope da carcaça:**

| Nome | Valor |
|---|---|
| `r_lobo` | 24 |
| `r_cauda` | 11 |
| `d_lobo_cauda` | 45 |
| `h_corpo` | 18 |
| `h_split` | 8 |
| `t_parede` | 2.0 |
| `r_pillow` | 5 |
| `r_pillow_inf` | 2 |
| `folga_impressao` | 0.3 |

**Peças compradas — valores provisórios, serão substituídos por medição:**

| Nome | Valor |
|---|---|
| `d_garra` | 12.0 |
| `h_garra` | 10.0 |
| `curso_garra` | 1.2 |
| `d_furo_pino` | 2.4 |
| `L_mcu` | 22.5 |
| `W_mcu` | 18.0 |
| `H_mcu` | 4.0 |
| `L_driver` | 15.0 |
| `W_driver` | 15.0 |
| `H_driver` | 3.0 |
| `d_nfc` | 25.0 |
| `t_nfc` | 0.2 |
| `L_inlay` | 70.0 |
| `W_inlay` | 16.0 |
| `d_pogo` | 6.0 |

**Atuador e alavanca:**

| Nome | Valor / expressão |
|---|---|
| `d_sma` | 0.15 |
| `L_sma` | 50 |
| `curso_sma` | `L_sma * 0.04` |
| `braco_sma` | 20 |
| `braco_garra` | 12 |
| `d_pivo` | 2.0 |
| `t_alavanca` | 3.0 |

**Montagem:**

| Nome | Valor |
|---|---|
| `n_parafusos` | 4 (adimensional) |
| `d_inserto` | 3.2 |
| `h_inserto` | 4.0 |
| `d_parafuso_passante` | 2.4 |
| `d_cabeca_parafuso` | 4.2 |

Confirme que `curso_sma` calculou **2,0 mm**. Se não calculou, pare e reporte.

## Passo 3 — Sketch `S00_Contorno_Mestre`

Crie um sketch no plano **XY**, com o nome `S00_Contorno_Mestre`.

Origem = eixo do pino. **−Y** aponta do lobo largo para a cauda estreita.

1. Circunferência de **construção** `C_lobo`: centro na **origem**, raio = `r_lobo`.
2. Circunferência de **construção** `C_cauda`: centro em `(0, -d_lobo_cauda)`, raio = `r_cauda`.
3. Duas retas **tangentes externas** ligando as duas circunferências, uma de cada lado do eixo Y.
   Restrinja cada reta com *Tangent* nas duas extremidades, e aplique *Symmetry* entre as duas
   retas em relação ao eixo Y.
4. *Trim* nos arcos internos, deixando **um único perfil fechado**: arco externo do lobo,
   tangente esquerda, arco externo da cauda, tangente direita.
5. O sketch deve ficar **totalmente restringido** (todas as curvas pretas).

**Se o sketch não fechar totalmente restringido, pare e reporte qual restrição faltou.**
Não force com cota manual.

### Valores de conferência (calcule e confirme antes de seguir)

| Grandeza | Valor esperado |
|---|---|
| Comprimento total em Y | `r_lobo + d_lobo_cauda + r_cauda` = **80 mm** |
| Largura total em X | `2 × r_lobo` = **48 mm** |
| Comprimento de cada reta tangente | `sqrt(d_lobo_cauda² − (r_lobo − r_cauda)²)` = **43,08 mm** |

Se algum divergir, a geometria está errada. Pare e reporte.

## Passo 4 — Sólido mestre `B00_Solido_Mestre`

1. *Extrude* do `S00_Contorno_Mestre` em **+Z** por `h_corpo`, operação **New Body**.
   Nomeie o corpo `B00_Solido_Mestre`.
2. *Fillet* em todas as arestas do **topo**, raio = `r_pillow`.
3. *Fillet* em todas as arestas da **base**, raio = `r_pillow_inf`.
4. **NÃO aplique ângulo de saída (draft).** A peça é impressa em 3D, não injetada.

Renomeie cada item da timeline de forma descritiva. Nada pode ficar como "Extrude1" ou "Fillet2".

## Passo 5 — Relatório

Responda com:

1. Confirmação de que todos os parâmetros foram criados, e o valor calculado de `curso_sma`.
2. Se o `S00_Contorno_Mestre` ficou totalmente restringido — **sim ou não**.
3. Os três valores de conferência do Passo 3, medidos no modelo.
4. Volume e área de superfície do `B00_Solido_Mestre`.
5. Nomes dos itens da timeline, em ordem.
6. Qualquer ambiguidade que você resolveu por conta própria, e como.

## O que NÃO fazer neste bloco

- Não aplique *Shell*, não divida o corpo, não crie componentes.
- Não modele garra, pino, eletrônica, alavanca ou furo nenhum.
- Não aplique ângulo de saída.
- Não crie parâmetro fora da lista do Passo 2.

# ⬆️ FIM DO QUE COLAR

---

## Como validar antes de pedir o Bloco 2

1. O contorno é uma **lágrima**: lobo largo em cima (Ø48), afinando para a cauda embaixo (Ø22).
2. Envelope **48 × 80 × 18 mm**.
3. Sketch **totalmente restringido** — se o agente disser "não", não avance: peça para corrigir.
4. Um corpo só, sem furo nenhum.

Se os três valores de conferência baterem, o Bloco 2 pode ir.
