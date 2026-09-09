# FUSION 360 via MCP — BLOCO 4 de 7
## Mecanismo de acionamento: bucha, cursor com rampa, guias e fios SMA

**Pré-requisito:** Blocos 1 a 3 concluídos. Câmara de atuação livre, direção −Y desobstruída.

---

## O mecanismo, em uma frase

Dois fios de nitinol contraem 1,68 mm e puxam um **cursor** para a cauda; a **rampa** na parte
de baixo do cursor empurra uma **bucha** 1,2 mm para dentro da garra; a gaiola cede e o pino sai.

```
          teto (Z=16) — o cursor desliza encostado nele
   ___________________________________
   |///////|  cursor  |==== 2 fios SMA ====> puxa para -Y
   |  rampa \_________|
   |         |
        [bucha]  desce 1,2 mm
           |
      [ GARRA ]  gaiola cede
           |
        --pino sai--
```

---

## ⚠️ A pergunta que o CAD não responde

Este bloco assume que a gaiola libera sendo **empurrada para baixo**. Isso varia por fabricante.

**Descubra desmontando a hard tag doadora** (parte 03, semana 1). Se a sua liberar sendo
**puxada para cima**, o Bloco 4 muda assim — e só assim:

| O que muda | Como |
|---|---|
| Sentido da rampa | inverte: fina na frente, grossa atrás |
| Bucha | vira **gancho**, precisa agarrar a gaiola em vez de só encostar |
| Resto (guias, fios, âncoras, cursor) | **não muda** |

Não é retrabalho grande, mas é retrabalho. Meça antes de imprimir.

---

## As contas (refaça com os seus números medidos)

| Grandeza | Fórmula | Valor |
|---|---|---|
| Curso de cada fio | 4% × `L_sma` = 4% × 42 mm | **1,68 mm** |
| Ângulo da rampa | `atan(curso_garra / curso_sma)` = atan(1,2/1,68) | **35,5°** |
| Ganho de força | `1 / tan θ` | 1,40× |
| Eficiência com atrito (μ ≈ 0,3) | `tan θ / tan(θ + arctan μ)` = tan35,5°/tan52,2° | 0,554 |
| Força de tração, 2 fios | 2 × 3,2 N | 6,4 N |
| **Força na garra** | 6,4 × 1,40 × 0,554 | **4,96 N** |
| **Margem sobre a mola (2,5 N)** | | **1,98×** ✔ |

Elétrico: R por fio = 50 Ω/m × 0,042 m = 2,1 Ω; dois em paralelo = 1,05 Ω;
I = 0,82 A; P = 0,71 W; em 1,5 s → **1,06 J**. Desprezível para a fonte de 5 W da Estação.

> **A maior incerteza é o μ = 0,3.** É estimativa, não medição. Meça a força de saída real da
> rampa na bancada. Se a margem cair abaixo de 1,5×, acrescente um terceiro fio — é a correção
> mais barata (não muda geometria nenhuma, só o furo da âncora).

---

# ⬇️ COPIE DAQUI PARA BAIXO E COLE NO MCP

Continue o documento `TagAndGo_Prototipo`. Não crie documento novo. Execute na ordem.
Ao terminar, responda o relatório do Passo 8.

## Contexto

Estou modelando o mecanismo que destrava uma etiqueta antifurto. Dois fios de liga com memória
de forma puxam um cursor; a rampa do cursor empurra uma bucha para baixo; a bucha aciona uma
garra de esferas **comprada**, que eu não modelo.

Sistema de coordenadas já estabelecido: origem no eixo do pino, **+Z** para cima, **−Y** do
lobo para a cauda. Teto interno em Z = 16, topo da garra em Z = 12.

## Passo 1 — Parâmetros

**Atualize** este parâmetro existente:

| Nome | Novo valor | Era |
|---|---|---|
| `L_sma` | **42** | 50 |

**Apague** estes parâmetros, que ficaram obsoletos (nenhuma geometria os usa):
`braco_sma`, `braco_garra`, `d_pivo`, `t_alavanca`.
Se o Fusion recusar a exclusão, deixe-os e reporte.

**Crie** estes, como expressões sempre que houver fórmula:

| Nome | Expressão | Valor esperado |
|---|---|---|
| `n_sma` | 2 | 2 (adimensional) |
| `curso_sma` | `L_sma * 0.04` | 1,68 mm |
| `x_sma` | 4.0 | 4,0 mm |
| `z_teto_camara` | `h_corpo - t_parede` | 16,0 mm |
| `t_cursor_fino` | 2.0 | 2,0 mm |
| `t_cursor_grosso` | `t_cursor_fino + curso_garra` | 3,2 mm |
| `run_rampa` | `curso_sma` | 1,68 mm |
| `w_cursor` | 10.0 | 10,0 mm |
| `y_cursor_frente` | 5.0 | 5,0 mm |
| `y_cursor_tras` | -10.0 | −10,0 mm |
| `w_garfo` | `d_furo_pino + 2 * folga_impressao` | 3,0 mm |
| `d_bucha_ext` | 6.0 | 6,0 mm |
| `d_bucha_int` | `d_furo_pino + folga_impressao` | 2,7 mm |
| `h_bucha` | `z_teto_camara - t_cursor_fino - t_parede - h_garra` | 2,0 mm |
| `d_poste` | 3.0 | 3,0 mm |
| `y_poste` | `y_cursor_tras - L_sma` | −52,0 mm |

Confirme `h_bucha` = 2,0 e `y_poste` = −52,0 antes de seguir. Se divergirem, pare e reporte.

## Passo 2 — Componente `04_Bucha_Empurradora`

Crie um **novo componente** com este nome.

1. Plano de construção `P_TopoGarra`: offset de XY em +Z por `t_parede + h_garra` (= 12,0).
2. Sketch `S10_Bucha` em `P_TopoGarra`: dois círculos concêntricos na origem,
   Ø`d_bucha_ext` e Ø`d_bucha_int`. Perfil = a coroa entre eles.
3. *Extrude* em +Z por `h_bucha`. Corpo de Z = 12,0 a Z = 14,0.
4. Chanfro 0,3 mm nas arestas externas superior e inferior.

A face inferior encosta na gaiola da garra. A face superior recebe a rampa do cursor.
O furo central deixa a ponta do pino passar.

## Passo 3 — Componente `03_Cursor_Rampa`

Crie um **novo componente** com este nome. É a peça mais delicada do bloco — siga à risca.

### 3.1 Planta

Sketch `S11_Cursor_Planta` no plano `P_Split`, com a planta do cursor:

- retângulo de largura `w_cursor`, centrado em X = 0
- de `y_cursor_tras` (−10) até `y_cursor_frente` (+5)
- **rasgo de garfo**: fenda de largura `w_garfo`, centrada em X = 0, entrando pela borda
  **+Y** (frente) e indo até Y = −4

O resultado é um **U**: duas hastes (garfo) apontando para +Y, unidas por um corpo em −Y.
As hastes abraçam o eixo do pino, uma de cada lado, e é nelas que fica a rampa.

Sketch totalmente restringido.

### 3.2 Perfil da rampa

Sketch `S12_Cursor_Perfil` no plano **YZ**, com o perfil lateral do cursor. Do topo para baixo,
**a face superior é plana em Z = `z_teto_camara`** (encosta no teto). A face **inferior** varia:

| Trecho em Y | Espessura | Cota Z da face inferior |
|---|---|---|
| de `y_cursor_tras` (−10) até 0 | `t_cursor_fino` (2,0) | 14,0 |
| de 0 até `run_rampa` (+1,68) | **rampa linear**, 2,0 → 3,2 | 14,0 → 12,8 |
| de `run_rampa` até `y_cursor_frente` (+5) | `t_cursor_grosso` (3,2) | 12,8 |

> **Confira o sentido:** o cursor é **fino atrás** (−Y) e **grosso na frente** (+Y). Ao ser
> puxado para −Y, material mais grosso passa por cima da bucha e a empurra para baixo. Se você
> modelar ao contrário, o mecanismo trava em vez de liberar.

### 3.3 Corpo

*Extrude* da planta `S11_Cursor_Planta`, cortando pelo perfil `S12_Cursor_Perfil`
(use *Extrude* da planta e depois *Split/Cut* pelo perfil, ou *Loft* — escolha o caminho que o
Fusion aceitar e **reporte qual usou**).

Arredonde com fillet R0,5 todas as arestas vivas da rampa e das pontas do garfo.

### 3.4 Fixação dos fios

Na traseira do cursor (face em `y_cursor_tras`), dois furos Ø0,8 mm passantes em Y,
em X = ±`x_sma`, na meia altura do corpo. São os pontos de crimpagem dos fios.

## Passo 4 — Guias do cursor, em `01_Carcaca_Superior`

O cursor corre na metade **superior**, encostado no teto. Crie as guias ali.

1. Sketch `S13_Guias` em `P_Split`: dois retângulos, um de cada lado do cursor,
   nas faces internas em X = ±(`w_cursor`/2 + `folga_impressao`) = ±5,3,
   com 1,5 mm de espessura, de Y = `y_cursor_tras` até Y = 0.
2. *Extrude* com **Start: Offset** = `t_parede + h_garra - h_split` (= 4,0),
   direção +Z, extensão **To Object** (teto interno), operação **Join** em `01_Carcaca_Superior`.
3. *Mirror* pelo plano YZ, se você modelou só um lado.

As guias impedem o cursor de girar e de sair do lugar. Não devem tocar a bucha.

## Passo 5 — Batente de curso, em `01_Carcaca_Superior`

Uma nervura transversal que limita o recuo do cursor a **exatamente** `curso_sma`:

- posicionada em Y = `y_cursor_tras - curso_sma` (= −11,68)
- largura `w_cursor` + 2 mm, espessura 1,5 mm
- mesma extensão vertical das guias

Sem ela, o fio SMA continua puxando depois que a garra já liberou, e se rompe por
sobre-contração. **Este batente é item de segurança do mecanismo, não acabamento.**

## Passo 6 — Âncoras dos fios, em `01_Carcaca_Superior`

Dois postes cilíndricos:

- Ø`d_poste`, em X = ±`x_sma`, Y = `y_poste` (= −52)
- da face interna do teto para baixo, altura 3 mm
- furo transversal Ø0,8 mm em cada um, na direção X, para crimpar o fio
- operação **Join** em `01_Carcaca_Superior`

Confirme que a distância entre o furo do poste e o furo traseiro do cursor é **`L_sma`** (42 mm).
Se não for, corrija `y_poste` — não corrija o cursor.

## Passo 7 — Verificações de espaço

Confirme e reporte:

1. O cursor, na posição de repouso **e** recuado de `curso_sma`, não colide com: as 3 apoios de
   retenção do Bloco 3, as 4 torres, os 4 tubos, as guias, o batente.
2. Existe um **poço livre** para a ponta do pino: cilindro Ø`d_bucha_int` no eixo, de Z = 14,0
   até o teto, sem obstrução. O rasgo do garfo tem de deixar essa região aberta.
3. A folga entre o topo do cursor e o teto é zero (ele desliza encostado) e entre a base da
   bucha e o topo da garra é zero na posição de repouso.

Se alguma falhar, **reporte qual e onde**. Não corrija por conta própria.

## Passo 8 — Relatório

1. Valores calculados de `curso_sma`, `h_bucha`, `t_cursor_grosso`, `y_poste`.
2. Qual caminho você usou para o corpo do cursor (§3.3) — *Extrude+Cut* ou *Loft*.
3. Espessura do cursor medida em Y = −5, em Y = 0 e em Y = +3.
   (esperado: **2,0** / **2,0** / **3,2** mm)
4. Distância medida entre o furo da âncora e o furo traseiro do cursor. (esperado: **42,0 mm**)
5. Resultado das três verificações do Passo 7.
6. Volume de `03_Cursor_Rampa` e de `04_Bucha_Empurradora`.
7. Todos os sketches deste bloco ficaram totalmente restringidos? Sim ou não.
8. Ambiguidades que você resolveu por conta própria, e como.

## O que NÃO fazer neste bloco

- Não modele alavanca, pivô nem garfo articulado — o mecanismo é **cursor com rampa**, sem peça
  que gira. Se você viu "bell crank" em alguma versão anterior, está obsoleto.
- Não modele a garra, o pino, as esferas nem a mola da garra — são comprados.
- Não coloque poste, roldana ou desvio no caminho dos fios. Eles são **retos**, e é de propósito:
  cada desvio de 180° custa ~1,9× de força por atrito de capstan.
- Não invente mola de retorno neste bloco. (Ver nota abaixo.)
- Não mexa na eletrônica — é o Bloco 5.

# ⬆️ FIM DO QUE COLAR

---

## Como validar antes de pedir o Bloco 5

| Verificação | Esperado |
|---|---|
| Espessura do cursor em Y = −5 / 0 / +3 | 2,0 / 2,0 / 3,2 mm |
| Vão âncora ↔ cursor | 42,0 mm |
| Cursor recuado 1,68 mm | bucha desce 1,2 mm, sem colisão |
| Poço do pino | livre, Ø2,7 do topo da bucha ao teto |
| Batente | presente, em Y = −11,68 |

**Teste do sentido:** empurre o cursor mentalmente para −Y. A bucha tem que **descer**. Se
subir, a rampa está invertida — é o erro mais provável deste bloco.

---

## Mola de retorno — decisão deixada em aberto de propósito

Com rampa de 35,5° e μ = 0,3: `tan 35,5° = 0,714 > 0,3`, então o mecanismo **não é
autotravante**. Em tese a própria mola da garra empurra a bucha para cima e devolve o cursor
quando o fio esfria.

"Em tese" porque a margem sobre o autotravamento é de 2,4× e depende do μ estimado. **Verifique
na bancada** antes de decidir:

| Resultado do ensaio | O que fazer |
|---|---|
| O cursor volta sozinho ao esfriar | não precisa de mola. Uma peça a menos |
| Volta devagar ou trava | mola de compressão leve (~0,5 N) entre o batente e a traseira do cursor |

Se precisar da mola, a força disponível cai de 4,96 N para ~4,2 N — margem ainda de 1,7×.
Por isso não é urgente decidir agora, e por isso o Passo 5 já deixa o batente pronto para
receber a mola se ela for necessária.
