# FUSION 360 via MCP — BLOCO 5 de 7
## Eletrônica: baias, contatos, rádios e indicador

**Pré-requisito:** Blocos 1 a 4 concluídos.

---

## Três conflitos que apareceram ao posicionar a eletrônica

Modelar este bloco esbarrou em coisas já ocupadas. Duas resolvidas, uma em aberto.

### ⚠️ 1. Os contatos elétricos mudaram da face inferior para a superior

`CONTRATOS.md` §5 dizia "2 discos na **face inferior**". **Está errado, e por um motivo físico:**
a face inferior é a que encosta no tecido. Contato ali fica prensado contra a roupa e os pinos
da Estação nunca alcançam.

**Correção: contatos na face SUPERIOR.** A Estação passa a ser um **encaixe** onde a etiqueta
entra com o topo para cima, e os pinos descem de dentro do encaixe.

> Isso melhora outra coisa de graça: resolve o requisito da parte 06 (a etiqueta não pode sair
> destravada da Estação). Entrando num encaixe, ela destrava e cai direto na caixa de coleta.
> Um requisito de processo virou consequência da geometria.

**Avise as partes 05 e 06** — muda o projeto da Estação, não só o da etiqueta.

### ⚠️ 2. A placa auxiliar do driver encolheu de 15 × 15 para 12 × 12

Com 15 × 15 ela colidia com a torre de parafuso F4, em (0, −49). Como essa placa é um pedaço de
perfboard **que vocês mesmos cortam** (não é peça comprada de tamanho fixo), encolher é
legítimo. Cabem os 3 componentes do driver (MOSFET + 2 resistores) em 12 × 12.

### ⚠️ 3. O inlay UHF fica sobre a eletrônica — problema em aberto

O inlay precisa de comprimento para ter alcance, e o único lugar com 44 mm livres fica **logo
acima ou abaixo da placa do microcontrolador**. O plano de terra da placa **dessintoniza a
antena UHF** e derruba o alcance.

Três saídas. **Não decida no CAD — decida no ensaio da parte 04:**

| Saída | Custo | Consequência |
|---|---|---|
| **(a) Inlay *on-metal*** — categoria de produto feita exatamente para montagem sobre metal | R$ 8–15 (vs R$ 2) | **recomendada** — resolve sem mudar geometria |
| (b) Inlay curto (30 mm) longe da placa, na cauda | R$ 2 | perde alcance; a parte 04 pode não chegar a 1 m |
| (c) Inlay comum, aceitar a perda | R$ 2 | medir antes de assumir que funciona |

Este bloco **reserva uma área plana** de 46 × 14 mm na face inferior e **não corta rebaixo**,
porque inlay *on-metal* é colado na superfície e tem espessura própria. Se vocês escolherem
(b) ou (c), aí sim vale cortar um rebaixo — e aí é uma alteração de 5 minutos.

---

## Mapa de ocupação (o que já está tomado)

**Metade inferior, cavidade Z = 2 a 8:**

| Ocupado por | Onde |
|---|---|
| Alojamento da garra | Ø12,3 na origem |
| Torres de parafuso | Ø6 em (0, 17), (±15, −8), (0, −49) |

**Metade superior, cavidade Z = 8 a 16:** apoios de retenção, tubos de parafuso, guias do
cursor, batente, postes de âncora e os fios SMA em X = ±4. **Não invada.**

---

# ⬇️ COPIE DAQUI PARA BAIXO E COLE NO MCP

Continue o documento `TagAndGo_Prototipo`. Não crie documento novo. Execute na ordem.
Ao terminar, responda o relatório do Passo 8.

## Contexto

Estou modelando os alojamentos da eletrônica de uma etiqueta antifurto. As placas, os adesivos
de rádio e os contatos são **peças compradas** — eu abro os espaços, não modelo as peças.
Origem no eixo do pino, +Z para cima, −Y do lobo para a cauda.

## Passo 1 — Parâmetros

**Atualize** estes parâmetros existentes:

| Nome | Novo valor | Era | Motivo |
|---|---|---|---|
| `L_driver` | **12** | 15 | colidia com a torre F4 |
| `W_driver` | **12** | 15 | idem |
| `L_inlay` | **44** | 70 | 70 mm não cabe no envelope |
| `W_inlay` | **12** | 16 | idem |

**Crie** estes:

| Nome | Expressão | Valor |
|---|---|---|
| `y_mcu` | -20.0 | −20,0 mm |
| `y_driver` | -39.5 | −39,5 mm |
| `y_nfc` | -25.0 | −25,0 mm |
| `y_qr` | 2.0 | 2,0 mm |
| `lado_qr` | 20.0 | 20,0 mm |
| `prof_rebaixo` | 0.4 | 0,4 mm |
| `x_pogo` | 8.0 | 8,0 mm |
| `y_pogo` | -8.0 | −8,0 mm |
| `d_pogo_rebaixo` | `d_pogo + 0.5` | 6,5 mm |
| `prof_pogo` | 0.6 | 0,6 mm |
| `d_led` | 3.2 | 3,2 mm |
| `y_led` | -44.0 | −44,0 mm |
| `y_inlay` | -26.0 | −26,0 mm |
| `d_canal` | 3.0 | 3,0 mm |

## Passo 2 — Baia do microcontrolador, em `02_Carcaca_Inferior`

Plano `P_Piso`: offset de XY em +Z por `t_parede` (= 2,0). *(Se você já criou `P_Assento` no
Bloco 3 nessa mesma cota, reutilize-o em vez de criar outro.)*

Sketch `S20_Baia_MCU` em `P_Piso`:

- retângulo `L_mcu` + 2×`folga_impressao` (Y) por `W_mcu` + 2×`folga_impressao` (X)
- centrado em `(0, y_mcu)`
- cantos com fillet R1

*Extrude Cut* em +Z por `H_mcu` + 0.5, alvo `02_Carcaca_Inferior`.

> Confira: a baia **não** pode tocar o alojamento da garra (Ø12,3 na origem) nem as torres
> F2/F3 em (±15, −8). Folga esperada: ~2,6 mm para a garra, ~3 mm para as torres.

## Passo 3 — Baia da placa do driver, em `02_Carcaca_Inferior`

Sketch `S21_Baia_Driver` em `P_Piso`:

- quadrado `L_driver` + 2×`folga_impressao`, centrado em `(0, y_driver)`
- cantos com fillet R1

*Extrude Cut* em +Z por `H_driver` + 0.5.

> Confira: folga de ~0,5 mm para a torre F4 em (0, −49) e ~2,2 mm para a baia do MCU.
> Se colidir, **reporte** — não mova por conta própria.

## Passo 4 — Canais de fiação, em `02_Carcaca_Inferior`

1. Canal Ø`d_canal` ligando a baia do MCU à baia do driver, ao longo do eixo Y, profundidade
   2 mm a partir de `P_Piso`.
2. **Duas passagens verticais** para a fiação cruzar o plano de partição: entalhes de
   4 mm (Y) × 2 mm (X) na borda superior da parede da metade inferior, em X = ±10, Y = −20.
   Corte também os entalhes correspondentes em `01_Carcaca_Superior`, na mesma posição.

Sem essas passagens, os fios do driver não alcançam os fios SMA, que estão na metade superior.

## Passo 5 — Face superior de `01_Carcaca_Superior`

Sketch `S22_Face_Superior` na face externa do topo. Crie os quatro elementos e corte cada um:

| Elemento | Geometria | Centro | Profundidade |
|---|---|---|---|
| Rebaixo do adesivo NFC | círculo Ø`d_nfc` + 1 | `(0, y_nfc)` | `t_nfc` + 0.2 |
| Rebaixo do QR Code | quadrado `lado_qr`, cantos R2 | `(0, y_qr)` | `prof_rebaixo` |
| Rebaixos dos contatos | 2 círculos Ø`d_pogo_rebaixo` | `(±x_pogo, y_pogo)` | `prof_pogo` |
| Furo do LED | círculo Ø`d_led` | `(0, y_led)` | passante |

Nos dois rebaixos de contato, acrescente um **furo passante Ø2 mm** no centro, para o fio
descer até a eletrônica.

Verifique que nenhum deles invade os rebaixos de cabeça de parafuso em (0, 17), (±15, −8) e
(0, −49). Folga mínima esperada: 1,3 mm (entre o LED e a torre F4).

## Passo 6 — Texto em relevo

Na face superior, texto **"Tag&Go"** em relevo, altura 4 mm, extrusão 0,3 mm para fora, fonte
sem serifa, posicionado em `(0, 12)`. Não sobreponha o rebaixo do QR nem a torre F1.

## Passo 7 — Área reservada do inlay UHF (face inferior)

**Não corte nada.** Apenas verifique e reporte:

- existe, na face **inferior externa**, uma área **plana e livre** de 46 mm (Y) × 14 mm (X),
  centrada em `(0, y_inlay)`?
- ela está livre do furo do pino (Ø`d_furo_pino` na origem) e de qualquer outro elemento?

Se houver obstrução, **diga qual e onde**.

## Passo 8 — Relatório

1. Valores atualizados de `L_driver`, `L_inlay` e criados de `y_mcu`, `y_driver`.
2. Volume de `02_Carcaca_Inferior` antes e depois deste bloco.
   (esperado: redução de aproximadamente **2.000 a 2.600 mm³**)
3. Folga medida entre a baia do MCU e: o alojamento da garra; as torres F2/F3.
4. Folga medida entre a baia do driver e: a torre F4; a baia do MCU.
5. Profundidade restante de material sob cada baia. (a face inferior tem `t_parede` = 2,0 mm —
   as baias **não** podem tê-la perfurado. Confirme.)
6. Resultado da verificação do Passo 7.
7. Todos os sketches ficaram totalmente restringidos? Sim ou não.
8. Ambiguidades que você resolveu por conta própria, e como.

## O que NÃO fazer neste bloco

- Não modele as placas, os adesivos NFC/UHF, os discos de contato nem o LED — são comprados.
  Você abre os espaços onde eles entram.
- Não coloque contato elétrico na face **inferior** — é a face que encosta no tecido.
- Não corte rebaixo para o inlay UHF neste bloco. (Ver conflito 3, acima.)
- Não invada a metade superior acima de Z = 12, onde correm o cursor e os fios SMA.
- Não perfure o piso de 2 mm ao cortar as baias.
- Não mova nada do Bloco 4. Se algo colidir, **reporte**.

# ⬆️ FIM DO QUE COLAR

---

## Como validar antes de pedir o Bloco 6

| Verificação | Esperado |
|---|---|
| Baia do MCU | 22,8 × 18,3, prof. 4,5, centrada em (0, −20) |
| Folga MCU ↔ garra | ~2,6 mm |
| Folga driver ↔ torre F4 | ~0,5 mm |
| Piso sob as baias | intacto, 2,0 mm |
| Contatos | 2, na face **superior**, em (±8, −8) |
| Área do inlay | 46 × 14 livre na face inferior |

**Teste visual:** vista de cima, a face superior tem — do lobo para a cauda — o texto em relevo,
o QR, dois contatos, o círculo do NFC, o furo do LED, e quatro rebaixos de parafuso. Nada
sobreposto.

---

## O que este bloco manda para as outras partes

| Para | Recado |
|---|---|
| **Parte 01** | O inlay UHF tem de caber em **44 × 12 mm**. Não compre os 70 mm que estavam no contrato. E leia o conflito 3: provavelmente vocês precisam de um inlay ***on-metal***. |
| **Parte 05** | Os contatos mudaram para a face **superior**. A Estação vira um encaixe com pinos descendo, não uma bancada com pinos subindo. |
| **Parte 06** | O encaixe da Estação resolve o retorno da etiqueta por geometria — ela destrava dentro e cai na caixa. É o mecanismo que vocês queriam. |
| **Parte 04** | O alcance UHF depende da decisão do conflito 3. Testem o inlay **montado na etiqueta**, não solto no ar. |
