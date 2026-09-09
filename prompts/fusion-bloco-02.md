# FUSION 360 via MCP — BLOCO 2 de 7
## Casca, divisão em duas metades e fechamento por parafuso

**Pré-requisito:** Bloco 1 concluído, com `S00_Contorno_Mestre` totalmente restringido e
`B00_Solido_Mestre` com 48 × 80 × 18 mm. Se o Bloco 1 não fechou restringido, **conserte antes**
— todo bloco seguinte herda o erro.

Depois deste bloco, os blocos 3 a 6 dependem de **medir as peças reais**
(ver `03-destravamento.md`, §5.1). Bloco 2 é o último que roda sem medição.

---

# ⬇️ COPIE DAQUI PARA BAIXO E COLE NO MCP

Continue o documento `TagAndGo_Prototipo`, criado no bloco anterior. Não crie documento novo.
Execute os passos na ordem. Não improvise geometria. Ao terminar, responda o relatório do Passo 10.

## Contexto

Estou modelando a carcaça de um protótipo de etiqueta antifurto de roupa, impressa em 3D e
fechada por parafuso M2 com inserto térmico. Este bloco transforma o sólido maciço em duas
metades ocas parafusáveis. **Não modele garra, eletrônica, alavanca nem furo além dos pedidos.**

## Passo 1 — Ocar o sólido

*Shell* no `B00_Solido_Mestre`:

- espessura **interna** = `t_parede`
- **nenhuma face removida** — o resultado é uma casca fechada, oca por dentro

## Passo 2 — Plano de partição

Crie um plano de construção chamado **`P_Split`**: *Offset Plane* a partir do plano **XY**,
distância = `h_split` em **+Z**.

## Passo 3 — Dividir em duas metades

*Split Body* do corpo ocado, usando `P_Split` como ferramenta de corte. Resultam **2 corpos**.

Renomeie provisoriamente:

- corpo **inferior** (de Z = 0 a Z = `h_split`) → `B02_Inferior`
- corpo **superior** (de Z = `h_split` a Z = `h_corpo`) → `B01_Superior`

## Passo 4 — Sketch da furação

Crie um sketch no plano **`P_Split`**, com o nome **`S01_Furacao`**.

Desenhe **4 circunferências de Ø6 mm**, centradas exatamente nestes pontos:

| Ponto | Coordenada (X, Y) | Onde fica |
|---|---|---|
| `F1` | `(0, 17)` | lobo, acima do futuro alojamento da garra |
| `F2` | `(-15, -8)` | lateral esquerda |
| `F3` | `(15, -8)` | lateral direita |
| `F4` | `(0, -49)` | cauda |

Aplique *Symmetry* entre `F2` e `F3` em relação ao eixo Y. Sketch totalmente restringido.

> Estes quatro pontos são **zona proibida** para os blocos seguintes: a eletrônica do Bloco 5
> tem de ser posicionada em volta deles.

## Passo 5 — Torres de inserto (metade inferior)

*Extrude* das 4 circunferências do `S01_Furacao`:

- direção: **−Z** (para baixo), de `P_Split` até o plano XY
- operação: **Join**, alvo `B02_Inferior`

## Passo 6 — Tubos de passagem (metade superior)

*Extrude* das mesmas 4 circunferências:

- direção: **+Z** (para cima)
- extensão: **To Object**, alvo = a face interna do teto do `B01_Superior`
- operação: **Join**, alvo `B01_Superior`

> Se *To Object* falhar, use *Distance* = `h_corpo - h_split - t_parede` e reporte que usou o
> caminho alternativo.

## Passo 7 — Furos do inserto térmico (metade inferior)

Nas 4 torres, a partir da face superior de cada uma (no plano `P_Split`), para **baixo**:

- Ø = `d_inserto`
- profundidade = `h_inserto`
- operação: Cut, alvo `B02_Inferior`

## Passo 8 — Furos de passagem do parafuso (metade superior)

Nos 4 tubos, passantes:

- Ø = `d_parafuso_passante`
- de `P_Split` atravessando o tubo **e** a parede superior, até sair na face externa do topo
- operação: Cut, alvo `B01_Superior`

## Passo 9 — Rebaixo da cabeça do parafuso

Na **face externa superior** do `B01_Superior`, nos mesmos 4 centros:

- Ø = `d_cabeca_parafuso`
- profundidade = **2 mm**
- operação: Cut

Renomeie os corpos definitivamente:

- `B01_Superior` → **`01_Carcaca_Superior`**
- `B02_Inferior` → **`02_Carcaca_Inferior`**

Em seguida, *Create Components from Bodies* nos dois. Renomeie os itens da timeline de forma
descritiva — nada pode ficar como "Extrude1" ou "Shell1".

## Passo 10 — Relatório

Responda com:

1. Quantos corpos existem ao final. (esperado: **2**)
2. Volume de `01_Carcaca_Superior` e de `02_Carcaca_Inferior`, em mm³.
3. Volume somado das duas. (esperado: entre **10.000 e 15.000 mm³**)
4. Se o `S01_Furacao` ficou totalmente restringido — sim ou não.
5. Se o *To Object* do Passo 6 funcionou, ou se usou a distância alternativa.
6. Rode *Inspect → Section Analysis* pelo plano YZ e confirme: a parede é uniforme e mede
   `t_parede` em toda a extensão? Onde ela não medir, diga onde.
7. Confirme que as 4 torres encostam no plano `P_Split` e que os 4 tubos encostam no teto interno.
8. Nomes dos itens da timeline, em ordem.
9. Qualquer ambiguidade que você resolveu por conta própria, e como.

## O que NÃO fazer neste bloco

- Não crie o alojamento da garra, o furo do pino nem qualquer baia de eletrônica.
- Não crie a alavanca nem âncoras do fio SMA.
- Não aplique ângulo de saída (draft) — a peça é impressa, não injetada.
- Não use snap fit. O fechamento é por parafuso, porque snap impresso quebra na reutilização.
- Não crie parâmetro novo. Todos os que você precisa já existem do Bloco 1.

# ⬆️ FIM DO QUE COLAR

---

## Como validar antes de pedir o Bloco 3

| Verificação | Esperado |
|---|---|
| Nº de corpos | 2 |
| Volume somado | 10.000 a 15.000 mm³ (~12 a 19 g em PETG) |
| Parede na seção YZ | uniforme, 2,0 mm |
| Torres | 4, encostando no plano de partição |
| Tubos | 4, alinhados com as torres, encostando no teto |
| Sketch `S01_Furacao` | totalmente restringido |

Se o volume somado der muito acima de 15.000 mm³, provavelmente o *Shell* não rodou e o corpo
continua maciço — confira antes de seguir.

**Teste visual rápido:** esconda a metade superior. Você deve ver uma bandeja oca com 4 torres
furadas subindo até a borda. Nada mais.

---

## Antes do Bloco 3 — o que precisa estar medido

Os blocos 3 a 6 usam valores que hoje são chute. Antes de rodá-los, a dupla da parte 03 precisa
comprar as hard tags, desmontar uma e medir:

| Parâmetro | Como medir |
|---|---|
| `d_garra`, `h_garra` | paquímetro na garra canibalizada |
| `curso_garra` | empurrar a gaiola com um pino até o tack sair; medir o deslocamento |
| `d_furo_pino` | Ø da haste do pino + 0,4 mm |
| `L_mcu`, `W_mcu`, `H_mcu` | paquímetro na placa, **sem barras de pinos** |

Depois é só trocar os números na tabela de parâmetros — os blocos 1 e 2 se atualizam sozinhos.
É exatamente para isso que o modelo é paramétrico.
