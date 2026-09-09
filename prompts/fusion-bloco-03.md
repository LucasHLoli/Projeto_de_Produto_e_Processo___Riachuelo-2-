# FUSION 360 via MCP — BLOCO 3 de 7
## Alojamento da garra, furo do pino e retenção

**Pré-requisito:** Blocos 1 e 2 concluídos — 2 corpos ocos, parede 2 mm, 4 torres e 4 tubos.

---

## ⚠️ Leia antes de rodar: este bloco usa valores ainda não medidos

`d_garra`, `h_garra` e `d_furo_pino` hoje são estimativas. Você tem duas opções:

**(a) Rodar agora com os valores provisórios.** A geometria fica certa em topologia e errada
em escala; ao medir a peça real, você troca os números na tabela de parâmetros e o modelo se
atualiza sozinho. **É o caminho recomendado** — adianta trabalho sem custo de retrabalho.

**(b) Esperar a medição.** Só se a dupla da parte 03 já tiver as hard tags em mãos.

Em qualquer caso, leia a **§ Sensibilidade** no fim: há **um** valor que, se a peça real
divergir, não se resolve trocando parâmetro.

---

## A pilha vertical (entenda antes de executar)

| Z (mm) | O que ocupa |
|---|---|
| 0 | face inferior externa — encosta no tecido |
| 0 → 2 | piso, `t_parede`, com o furo Ø`d_furo_pino` do pino |
| **2** | **assento da garra** (`P_Assento`) |
| 2 → 12 | **garra canibalizada** (`h_garra` = 10) |
| **8** | **plano de partição** — a garra atravessa as duas metades |
| 12 → 12,3 | folga vertical (`folga_impressao`) |
| 12,3 → 16 | **câmara de atuação** — reservada, fica vazia neste bloco |
| 16 → 18 | teto, `t_parede` |

Dois pontos que costumam confundir:

1. **A garra atravessa o plano de partição.** Ela tem 10 mm e a metade inferior só tem 8. Isso
   é intencional: a metade superior a captura ao fechar.
2. **Não há corte a fazer na metade superior.** O interior dela já ficou vazio no *Shell* do
   Bloco 2. O que falta lá é o contrário — **adicionar** três apoios que prendem a garra por cima.

---

# ⬇️ COPIE DAQUI PARA BAIXO E COLE NO MCP

Continue o documento `TagAndGo_Prototipo`. Não crie documento novo. Execute na ordem, sem
improvisar geometria. Ao terminar, responda o relatório do Passo 7.

## Contexto

Estou modelando a carcaça de um protótipo de etiqueta antifurto. Ela aloja uma **garra de
esferas canibalizada de uma etiqueta comercial** — peça comprada, que eu **não** modelo. Este
bloco abre o alojamento dessa garra, o furo de entrada do pino, e cria os apoios que a prendem.

**Não modele a garra, o pino, a eletrônica nem o mecanismo de acionamento.**

## Passo 1 — Novos parâmetros

Crie estes Parâmetros de Usuário, **como expressões**, não como números digitados:

| Nome | Expressão | Valor esperado |
|---|---|---|
| `d_alojamento` | `d_garra + folga_impressao` | 12,3 mm |
| `z_assento` | `t_parede` | 2,0 mm |
| `z_topo_garra` | `t_parede + h_garra + folga_impressao` | 12,3 mm |
| `d_camara` | 8.0 | 8,0 mm |
| `w_apoio` | 3.0 | 3,0 mm |

Confirme os valores calculados antes de seguir. Se `z_topo_garra` não der 12,3, pare e reporte.

## Passo 2 — Plano de assento

Crie um plano de construção **`P_Assento`**: *Offset Plane* a partir do plano **XY**,
distância = `z_assento` em **+Z**.

## Passo 3 — Furo de entrada do pino

Sketch no plano **XY**, nome **`S02_Furo_Pino`**:

- uma circunferência Ø`d_furo_pino`, centrada na **origem**
- *Extrude Cut*, direção **+Z**, extensão **All** (passante), alvo `02_Carcaca_Inferior`

É por aqui que a haste do pino entra, vinda de baixo, atravessando o tecido.

## Passo 4 — Alojamento da garra

Sketch no plano **`P_Assento`**, nome **`S03_Alojamento_Garra`**:

- uma circunferência Ø`d_alojamento`, centrada na **origem**
- *Extrude Cut*, direção **+Z**, extensão **All**, alvo **`02_Carcaca_Inferior`**

O corte remove material de Z = 2 até o topo da metade inferior (Z = `h_split`). O piso de 2 mm
abaixo **permanece** e é o assento onde a garra apoia. Confirme que o piso não foi removido.

## Passo 5 — Apoios de retenção (metade superior)

Sketch no plano **`P_Split`**, nome **`S04_Apoios_Garra`**.

Desenhe **3 setores anulares**, todos com raio externo = `d_alojamento / 2` e raio interno =
`d_camara / 2`, cada um com largura angular correspondente a `w_apoio`, centrados nestas direções:

| Apoio | Direção | Ângulo |
|---|---|---|
| `A1` | **+X** | 0° |
| `A2` | **−X** | 180° |
| `A3` | **+Y** | 90° |

> **Por que só três, e por que assim:** a direção **−Y** (270°) fica deliberadamente livre. É
> por ela que o mecanismo de acionamento vai entrar, no Bloco 4. Não coloque apoio em −Y.

*Extrude* dos 3 setores:

- **Start: Offset**, distância = `z_topo_garra - h_split` (esperado: 4,3 mm)
- direção **+Z**, extensão **To Object**, alvo = a face interna do teto do `01_Carcaca_Superior`
- operação: **Join**, alvo `01_Carcaca_Superior`

> Se *To Object* falhar, use *Distance* = `h_corpo - t_parede - z_topo_garra` (≈ 3,7 mm) e
> reporte que usou o caminho alternativo.

Assim os apoios ocupam de Z = 12,3 até o teto, e a garra fica presa entre o piso (Z = 2) e a
face inferior deles, com `folga_impressao` de folga vertical.

## Passo 6 — Não obstruir a câmara de atuação

Confirme que a região abaixo — **a câmara de atuação** — está **completamente vazia**:

- de Z = `z_topo_garra` (12,3) até a face interna do teto (≈ 16)
- num cilindro de Ø`d_camara` (8) centrado na origem
- e em todo o setor na direção **−Y**, da origem até a parede da cauda

Se algum apoio, torre ou tubo invadir essa região, **reporte quais e onde**. Não corrija por
conta própria.

## Passo 7 — Relatório

1. Valores calculados de `d_alojamento`, `z_topo_garra` e do offset do Passo 5.
2. Volume de `02_Carcaca_Inferior` **antes e depois** deste bloco, e a diferença.
   (esperado: redução de aproximadamente **600 a 800 mm³**)
3. Volume de `01_Carcaca_Superior` antes e depois. (esperado: pequeno **aumento**, dos apoios)
4. O piso de 2 mm sob a garra permanece intacto, com apenas o furo Ø`d_furo_pino`? Sim ou não.
5. O *To Object* do Passo 5 funcionou, ou usou a distância alternativa?
6. Resultado da verificação do Passo 6: a câmara está livre? Se não, o que a invade?
7. Rode *Section Analysis* pelo plano **YZ** e descreva a pilha vertical que você vê no eixo,
   de Z = 0 a Z = 18.
8. Todos os sketches deste bloco ficaram totalmente restringidos? Sim ou não.
9. Qualquer ambiguidade que você resolveu por conta própria, e como.

## O que NÃO fazer neste bloco

- Não modele a garra de esferas — ela é **comprada**. Você abre o buraco onde ela entra, só isso.
- Não modele o pino, a alavanca, o cursor, o fio SMA nem a eletrônica.
- Não coloque apoio de retenção na direção **−Y**.
- Não corte nada na metade superior — o interior dela já está vazio desde o *Shell* do Bloco 2.
- Não crie parâmetro fora da lista do Passo 1.
- Não mexa nas 4 torres nem nos 4 tubos do Bloco 2.

# ⬆️ FIM DO QUE COLAR

---

## Como validar antes de pedir o Bloco 4

| Verificação | Esperado |
|---|---|
| Piso sob a garra | intacto, 2 mm, só com o furo Ø2,4 |
| Alojamento | Ø12,3 de Z = 2 até Z = 8 |
| Apoios de retenção | 3, em +X, −X e +Y — **nenhum em −Y** |
| Câmara de atuação | vazia, Ø8 de Z = 12,3 até o teto |
| Volume da metade inferior | caiu 600–800 mm³ |
| Sketches | totalmente restringidos |

**Teste visual:** vista de baixo, você vê **um** furo pequeno no centro (Ø2,4) e nada mais.
Se aparecer um buraco grande, o Passo 4 comeu o piso — o corte começou no plano errado.

---

## Sensibilidade — o que acontece quando você medir a peça real

| Parâmetro | Se mudar | Consequência |
|---|---|---|
| `d_garra` | até ~18 mm | **seguro** — só redimensiona. Acima disso, colide com a torre F1 |
| `d_furo_pino` | qualquer | **seguro** |
| `curso_garra` | qualquer | **não afeta este bloco** — entra no Bloco 4 |
| **`h_garra`** | **até 10,7 mm** | **seguro** |
| **`h_garra`** | **acima de 10,7 mm** | ⚠️ **quebra o modelo** |

### O único valor que pode quebrar

A câmara de atuação precisa de pelo menos **3 mm** de altura para o cursor caber. Com o teto
interno em Z = 16:

```
t_parede + h_garra + folga_impressao  <=  13
2 + h_garra + 0,3 <= 13   ->   h_garra <= 10,7 mm
```

**Se a garra real for mais alta que 10,7 mm**, não adianta trocar parâmetro: é preciso aumentar
`h_corpo` (hoje 18 mm) na mesma medida, e refazer os Blocos 1 a 3. Custa uns 20 minutos, mas
só se você souber que precisa.

> **Por isso `h_garra` é a primeira medida a tirar** quando as hard tags chegarem — antes até
> de `curso_garra`. É a única que pode mandar você voltar ao Bloco 1.

---

## O que vem no Bloco 4 (e por que ele espera)

O Bloco 4 é o mecanismo de acionamento: cursor com rampa, guias, âncoras do fio SMA.
Ele precisa de dois números medidos que ainda não existem:

| Medida | Como tirar |
|---|---|
| `curso_garra` | empurrar a gaiola com um pino de aço até o tack sair; medir o deslocamento |
| `forca_mola_garra` | dinamômetro, ou empilhar pesos até a gaiola ceder |

E de **uma observação**, que nenhum catálogo responde: **a gaiola libera empurrando para baixo
ou puxando para cima?** Varia por fabricante. Descubra desmontando, e anote — é o que define
o sentido da rampa.

Este bloco já deixou a câmara pronta para os dois casos.
