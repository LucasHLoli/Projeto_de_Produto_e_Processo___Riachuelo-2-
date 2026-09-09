# HIPER-PROMPT — Autodesk Fusion 360 (v2, orientado a peças compradas)

> ## ⚠️ OBSOLETO NA PARTE DO MECANISMO — leia antes de usar
>
> Este arquivo continua válido para **envelope, carcaça, regras de impressão 3D e lista de
> peças compradas**. Mas o **mecanismo de acionamento mudou**: a alavanca *bell crank*
> (`braco_sma` 20 mm / `braco_garra` 12 mm, componente `03_Alavanca_Bellcrank`) foi
> **descartada** — o braço de 20 mm precisaria ficar em pé, e a etiqueta tem 18 mm de altura.
>
> No lugar: **fio SMA em laço de ~140 mm + cursor com rampa de 12°**. Ver
> `prompts/03-destravamento.md`, §5.4.
>
> **Para executar o CAD, use os blocos** `prompts/fusion-bloco-01.md` em diante — eles já estão
> corrigidos e divididos para agente MCP. Este arquivo vale como referência de conjunto.

## "Riachuelo Tag&Go" — carcaça de protótipo funcional impressa em 3D

> **O que mudou da v1:** a v1 mandava projetar a garra de esferas, o pino e a carcaça
> injetada do zero. Isso não é construível num trabalho de graduação. A v2 projeta **apenas a
> carcaça e a alavanca**, em torno de componentes **comprados e medidos**. Ver
> `viabilidade-e-bom.md` para o balanço de energia e a lista de compras.
>
> Copie da seção 0 em diante e cole na ferramenta.

---

## 0. PAPEL E REGRAS DE EXECUÇÃO

Você é um projetista mecânico sênior operando o Autodesk Fusion 360. Construa o modelo CAD
paramétrico da **carcaça de um protótipo funcional** que aloja componentes comerciais.

Regras inegociáveis:

1. **Você não projeta componentes comprados.** A garra de travamento, o pino, a placa
   microcontroladora, o adesivo NFC e o inlay UHF são **peças de prateleira**. Modele cada uma
   apenas como um **sólido-envelope simplificado** com as dimensões da tabela §3.2, para
   verificar caimento e colisão. Não detalhe nenhuma delas.
2. **Todas** as cotas vêm dos Parâmetros de Usuário (§3). Nunca digite um número solto.
   Se precisar de um valor ausente, crie um parâmetro nomeado e registre no relatório final.
3. As peças que você **projeta de verdade** são apenas quatro:
   `01_Carcaca_Superior`, `02_Carcaca_Inferior`, `03_Alavanca_Bellcrank`, `04_Haste_Empurradora`.
4. O destino de fabricação é **impressão 3D (FDM ou resina)**, não injeção. Portanto:
   parede uniforme de `t_parede`, **sem ângulo de saída**, **sem snap fit** — a união é por
   **parafuso M2 com inserto térmico**, e a folga entre peças é `folga_impressao` (bem maior
   que folga de injeção).
5. Todo sketch deve ficar **totalmente restringido**. Se não fechar, pare e reporte qual
   restrição faltou — não force a geometria.
6. Nomeie cada sketch, feature, corpo, componente e junta como especificado. Nada pode ficar
   como "Sketch1" ou "Extrude3".
7. Ao terminar, produza o relatório de §11.

---

## 1. CONTEXTO (para entender a intenção, não para modelar)

Etiqueta antifurto de roupa que **se destrava sozinha**, sem o destravador do caixa, depois que
o cliente paga pelo celular. Elimina a fila mantendo a proteção contra furto.

Princípio de funcionamento do protótipo:

1. O cliente encosta o celular num **adesivo NFC** colado na etiqueta e paga no app.
2. Apoia a peça na **Estação de Liberação**, que energiza a etiqueta por **contatos elétricos**
   (a etiqueta **não tem bateria** e fica sem energia o resto do tempo).
3. O microcontrolador acorda, valida um token HMAC com a estação e aciona um **fio SMA**.
4. O fio contrai 2 mm e gira uma **alavanca bell crank**, que puxa a garra 1,2 mm para baixo.
5. A garra abre e o pino sai.

**Decisão de projeto central, já tomada — não reabra:** a garra de travamento **não é
projetada**. É a garra canibalizada de uma hard tag comercial. A carcaça existe para
segurá-la, alojar a eletrônica e converter o movimento do fio SMA em movimento da garra.

---

## 2. UNIDADES, ORIGEM E CONVENÇÕES

- Unidades: **milímetro**; massa em gramas; ângulos em graus.
- Origem = **eixo do pino**, no plano da face inferior externa da carcaça.
- **+Z** aponta do corpo para cima (para longe do tecido). O pino entra por baixo, subindo em +Z.
- **−Y** aponta do lobo largo (onde fica a garra) para a cauda estreita.
- Plano **XY** = face inferior externa. Plano **YZ** = plano de simetria.
- O produto é simétrico em relação a YZ. Sempre que possível use *Mirror* de features.

---

## 3. PARÂMETROS DE USUÁRIO

Crie todos em *Modify → Change Parameters → User Parameters*, com estes nomes exatos.

### 3.1 Envelope da carcaça (valores de projeto — pode ajustar)

| Nome | Expressão | Unid. | Comentário |
|---|---|---|---|
| `r_lobo` | 24 | mm | raio do lobo largo, centro na origem |
| `r_cauda` | 11 | mm | raio da ponta da cauda |
| `d_lobo_cauda` | 45 | mm | distância entre os centros |
| `h_corpo` | 18 | mm | altura total montada |
| `h_split` | 8 | mm | altura do plano de partição, a partir de XY |
| `t_parede` | 2.0 | mm | espessura de parede (mínimo prático em FDM) |
| `r_pillow` | 5 | mm | arredondamento superior |
| `r_pillow_inf` | 2 | mm | arredondamento inferior |
| `folga_impressao` | 0.3 | mm | folga entre peças móveis **em impressão 3D** |

> Envelope resultante: **48 × 80 × 18 mm**. É maior que o produto de produção
> (42 × 67 × 15,5 mm) e isso é **intencional e aceitável** — protótipo funcional, não DFM.

### 3.2 ⚠️ PEÇAS COMPRADAS — **MEDIR AS PEÇAS REAIS ANTES DE IMPRIMIR**

Os valores abaixo são **estimativas de partida**. Compre os componentes, meça com paquímetro
e **substitua** cada valor. O modelo é paramétrico exatamente para que isso custe minutos.

| Nome | Estimativa | Unid. | O que é / como medir |
|---|---|---|---|
| `d_garra` | 12.0 | mm | Ø externo da garra canibalizada da hard tag |
| `h_garra` | 10.0 | mm | altura da garra |
| `curso_garra` | 1.2 | mm | quanto a gaiola desce para liberar o pino — **medir empurrando com um pino de aço** |
| `forca_mola_garra` | 2.5 | N | força da mola da garra — **medir com dinamômetro ou pesos** |
| `d_furo_pino` | 2.4 | mm | Ø da haste do pino + 0,4 mm |
| `L_mcu` | 22.5 | mm | comprimento da placa ESP32-C3 Super Mini |
| `W_mcu` | 18.0 | mm | largura da placa |
| `H_mcu` | 4.0 | mm | altura da placa **sem barras de pinos** |
| `L_driver` | 15.0 | mm | placa auxiliar do MOSFET (perfboard) |
| `W_driver` | 15.0 | mm | idem |
| `H_driver` | 3.0 | mm | idem |
| `d_nfc` | 25.0 | mm | Ø do adesivo NTAG213 |
| `t_nfc` | 0.2 | mm | espessura do adesivo |
| `L_inlay` | 70.0 | mm | comprimento do inlay UHF — **escolher um inlay curto antes de fechar o CAD** |
| `W_inlay` | 16.0 | mm | largura do inlay |
| `d_pogo` | 6.0 | mm | Ø do disco de contato na face inferior |

### 3.3 Atuador SMA e alavanca (calculado — ver `viabilidade-e-bom.md` §1.1)

| Nome | Expressão | Unid. | Comentário |
|---|---|---|---|
| `d_sma` | 0.15 | mm | Ø do fio de nitinol |
| `L_sma` | 50 | mm | comprimento útil |
| `curso_sma` | L_sma * 0.04 | mm | contração de 4% → **2,0 mm** |
| `braco_sma` | 20 | mm | braço longo da alavanca (lado do fio) |
| `braco_garra` | 12 | mm | braço curto (lado da garra) |
| `d_pivo` | 2.0 | mm | Ø do pino de pivô da alavanca |
| `t_alavanca` | 3.0 | mm | espessura da alavanca |

**Verificação obrigatória de cinemática — confira antes de modelar:**

- Curso entregue à garra = `curso_sma × braco_garra / braco_sma` = 2,0 × 12/20 = **1,2 mm**
  → igual a `curso_garra`. ✔
- Força entregue à garra = 3,2 N × `braco_sma / braco_garra` = 3,2 × 20/12 = **5,3 N**
  → contra `forca_mola_garra` = 2,5 N. Margem **2,1×**. ✔

> Se ao medir a peça real `curso_garra` ou `forca_mola_garra` mudarem, **ajuste
> `braco_sma`/`braco_garra`** e refaça esta verificação. Não altere o envelope da carcaça.

### 3.4 Montagem

| Nome | Expressão | Unid. | Comentário |
|---|---|---|---|
| `n_parafusos` | 4 | — | parafusos de fechamento |
| `d_inserto` | 3.2 | mm | Ø do furo para inserto térmico M2 |
| `h_inserto` | 4.0 | mm | profundidade do furo do inserto |
| `d_parafuso_passante` | 2.4 | mm | passagem do M2 na carcaça superior |
| `d_cabeca_parafuso` | 4.2 | mm | rebaixo da cabeça |

---

## 4. ESTRUTURA DE COMPONENTES

Documento de montagem **`TagAndGo_Prototipo`**:

```
TagAndGo_Prototipo
├── PROJETADAS (voce modela de verdade)
│   ├── 01_Carcaca_Superior       impressa 3D
│   ├── 02_Carcaca_Inferior       impressa 3D
│   ├── 03_Alavanca_Bellcrank     impressa 3D ou usinada
│   └── 04_Haste_Empurradora      pino de aco 2 mm, cortado no comprimento
└── COMPRADAS (apenas solido-envelope simplificado)
    ├── 90_Garra_Doadora          canibalizada de hard tag comercial
    ├── 91_Pino_Tack              vem com a hard tag
    ├── 92_Placa_MCU              ESP32-C3 Super Mini
    ├── 93_Placa_Driver           perfboard com MOSFET
    ├── 94_Fio_SMA                nitinol 0,15 mm
    ├── 95_Adesivo_NFC            NTAG213
    ├── 96_Inlay_UHF              EPC Gen2
    └── 97_Contato_Pogo           x2, disco de latao
```

---

## 5. GEOMETRIA MESTRA

### 5.1 `S00_Contorno_Mestre` — sketch no plano XY

1. Circunferência de construção `C_lobo`: centro na **origem**, raio `r_lobo`.
2. Circunferência de construção `C_cauda`: centro em `(0, -d_lobo_cauda)`, raio `r_cauda`.
3. Duas retas **tangentes externas** ligando as duas, uma de cada lado de YZ. Restrinja com
   *Tangent* nas duas pontas de cada reta e *Symmetry* em relação ao eixo Y.
4. *Trim* nos arcos internos, deixando **um único perfil fechado**.
5. Confirme: sketch totalmente restringido; envelope ≈ 48 × 80 mm.

### 5.2 `B00_Solido_Mestre`

1. Extrude `S00_Contorno_Mestre` em +Z por `h_corpo` → **New Body** `B00_Solido_Mestre`.
2. Fillet nas arestas do topo: `r_pillow`. Fillet nas arestas da base: `r_pillow_inf`.
3. **Não aplique draft** — a peça é impressa, não injetada.

---

## 6. CARCAÇA

### 6.1 Casca e divisão

1. *Shell* em `B00_Solido_Mestre`, espessura interna `t_parede`, **sem remover face**.
2. Plano de construção `P_Split`: offset de XY em +Z por `h_split`.
3. *Split Body* pela `P_Split`. Corpo inferior → `02_Carcaca_Inferior`;
   superior → `01_Carcaca_Superior`. Promova ambos a componentes.

### 6.2 Alojamento da garra — em `02_Carcaca_Inferior`

Sketch `S01_Garra` no plano XY:

1. Círculo Ø`d_furo_pino` na origem → *Extrude Cut* passante. É por aqui que o pino entra.
2. Círculo Ø(`d_garra` + `folga_impressao`) na origem → *Extrude Cut* de XY em +Z por `h_garra`.
3. Rasgo de retenção: três nervuras 1,0 × 1,5 mm a 120°, para a garra não girar.
   *Circular Pattern*, 3 ocorrências em torno de Z.
4. **Rebaixo de passagem da haste**: canal de largura `d_pivo` + `folga_impressao` do topo do
   alojamento até a região da alavanca, para a `04_Haste_Empurradora` correr livre.

### 6.3 Berço da alavanca — em `02_Carcaca_Inferior`

1. Dois mancais paralelos, distantes `t_alavanca` + 2 × `folga_impressao`, com furo
   Ø`d_pivo` + `folga_impressao` passante, eixo **paralelo a X**, centro em
   `(0, -r_lobo + 4, h_split - 3)`.
2. Batente que limita o curso da alavanca ao ângulo correspondente a `curso_garra`.
3. Duas âncoras para o fio SMA na região da cauda: postes Ø3 mm com furo transversal Ø0,6 mm,
   posicionados de modo que o comprimento desenvolvido do fio seja **exatamente** `L_sma`.

> Faça o roteamento do fio **no plano XY** (o fio precisa dos 50 mm em comprimento reto), e
> deixe a alavanca converter esse movimento horizontal em movimento vertical da garra. Essa
> conversão é a razão de existir da alavanca.

### 6.4 Baias da eletrônica — em `02_Carcaca_Inferior`

1. Baia do MCU: bolsão `L_mcu` + 2×`folga_impressao` por `W_mcu` + 2×`folga_impressao`,
   profundidade `H_mcu` + 0,5 mm, centrado em `(0, -30)`, com quatro apoios de canto de 1 mm.
2. Baia do driver: idem, com `L_driver`/`W_driver`/`H_driver`, centrada em `(0, -52)`.
3. Canal de fiação Ø3 mm ligando as duas baias e a região da alavanca.
4. Dois furos Ø`d_pogo` na **face inferior**, em `(±8, -60)`, para os discos de contato,
   com rebaixo de 0,5 mm para o disco ficar rente.
5. Rasgo periférico para o inlay UHF: canal de `W_inlay` + 1 mm de largura por 1 mm de
   profundidade, correndo pela parede interna, com comprimento desenvolvido ≥ `L_inlay`.

### 6.5 Fechamento por parafuso

1. Em `02_Carcaca_Inferior`: `n_parafusos` torres Ø6 mm com furo Ø`d_inserto` × `h_inserto`
   para inserto térmico M2, distribuídas ao longo do contorno.
2. Em `01_Carcaca_Superior`: furos passantes Ø`d_parafuso_passante` coincidentes, com rebaixo
   Ø`d_cabeca_parafuso` × 2 mm na face superior.
3. Use *Circular* ou *Rectangular Pattern* — não modele os quatro individualmente.

### 6.6 Face superior — em `01_Carcaca_Superior`

1. Rebaixo circular Ø`d_nfc` + 1 mm, profundidade `t_nfc` + 0,2 mm, centrado em `(0, -30)`,
   para o adesivo NTAG213 ficar rente.
2. Rebaixo quadrado 20 × 20 mm, cantos R2, profundidade 0,4 mm, em `(0, -52)`, para a
   etiqueta de QR Code.
3. Texto em relevo **"Tag&Go"**, altura 4 mm, extrusão 0,3 mm, fonte sem serifa.
4. Furo Ø3 mm em `(0, -66)` para LED indicador.

---

## 7. PEÇAS PROJETADAS RESTANTES

### 7.1 `03_Alavanca_Bellcrank`

1. Sketch `S10_Alavanca` no plano YZ. Corpo em "L":
   - furo de pivô Ø`d_pivo` + `folga_impressao` no vértice;
   - braço longo de comprimento `braco_sma`, terminando num olhal Ø0,8 mm para o fio SMA;
   - braço curto de comprimento `braco_garra`, terminando num garfo que abraça a
     `04_Haste_Empurradora`.
2. *Extrude* simétrico por `t_alavanca`.
3. Fillet R1 em todos os cantos internos — é onde a peça impressa quebra.

### 7.2 `04_Haste_Empurradora`

Cilindro Ø`d_pivo`, comprimento da gaiola da garra até o garfo da alavanca, com um rebaixo
anular de 0,5 mm na extremidade superior para o garfo se engatar. Aço, cortado no comprimento.

---

## 8. PEÇAS COMPRADAS — SÓ ENVELOPE

Modele cada uma como **sólido primitivo simples**, sem detalhe interno:

| Componente | Geometria |
|---|---|
| `90_Garra_Doadora` | cilindro Ø`d_garra` × `h_garra`, furo central Ø2,2 mm |
| `91_Pino_Tack` | disco Ø14 × 1,2 mm + haste Ø2,0 × 16 mm com ponta cônica |
| `92_Placa_MCU` | caixa `L_mcu` × `W_mcu` × `H_mcu` |
| `93_Placa_Driver` | caixa `L_driver` × `W_driver` × `H_driver` |
| `94_Fio_SMA` | *sweep* de círculo Ø`d_sma` pelo caminho de roteamento, comprimento `L_sma` |
| `95_Adesivo_NFC` | disco Ø`d_nfc` × `t_nfc` |
| `96_Inlay_UHF` | lâmina `L_inlay` × `W_inlay` × 0,15 mm, deformada ao longo do canal |
| `97_Contato_Pogo` | disco Ø`d_pogo` × 1 mm, 2 ocorrências |

---

## 9. MONTAGEM, JUNTAS E VERIFICAÇÕES

### 9.1 Juntas

| Junta | Tipo | Entre | Limites |
|---|---|---|---|
| `J01_Carcacas` | Rigid | `01` ↔ `02` | face do split |
| `J02_Alavanca` | Revolute (eixo X) | `03` ↔ `02` | ângulo correspondente a `curso_garra` |
| `J03_Haste` | Slider (eixo Z) | `04` ↔ `02` | 0 a `curso_garra` |
| `J04_Garra` | Rigid | `90` ↔ `02` | — |
| `J05_Pino` | Slider (eixo Z) | `91` ↔ `02` | 0 a 16 mm |
| `J06_MCU` | Rigid | `92` ↔ `02` | — |
| `J07_Driver` | Rigid | `93` ↔ `02` | — |

Adicione um *Motion Link* entre `J02_Alavanca` e `J03_Haste` com a razão
`braco_garra / braco_sma`.

### 9.2 Materiais

| Componente | Material |
|---|---|
| `01`, `02`, `03` | PETG (ou resina rígida) |
| `04`, `91` | Aço inoxidável AISI 304 |
| `90` | ABS + aço (aproxime por ABS) |
| `92`, `93` | FR-4 |
| `94` | Nitinol — se ausente da biblioteca, crie custom com ρ = 6,45 g/cm³ |
| `97` | Latão |

### 9.3 Verificações obrigatórias

1. **Interferência** (*Inspect → Interference*) nas duas posições do mecanismo (travada e
   liberada). Exigido: **zero interferências não intencionais**.
2. **Animação**: gire `J02_Alavanca` de 0 ao limite e confirme que `04_Haste_Empurradora`
   percorre exatamente `curso_garra`. Se não bater, o erro está em `braco_sma`/`braco_garra`.
3. **Análise de seção** pelos planos YZ e XZ; capture as duas imagens.
4. **Propriedades físicas** da montagem sem o pino. Alvo: **≤ 70 g** (protótipo é mais pesado
   que o produto final — 45 g era alvo de produção). Se ultrapassar, reporte.
5. **Espessura de parede** ≥ 1,6 mm em toda a carcaça.
6. **Imprimibilidade**: verifique se cada uma das quatro peças projetadas tem uma orientação
   de impressão sem balanço acima de 45° em regiões funcionais. Reporte a orientação
   recomendada de cada peça e onde precisa de suporte.
7. **Acesso de montagem**: confirme que o fio SMA pode ser passado e crimpado **depois** da
   eletrônica estar no lugar. Se não puder, reporte — isso inviabiliza a montagem manual.

---

## 10. ENTREGÁVEIS

1. `TagAndGo_Prototipo.f3z` com timeline limpa e nomeada.
2. **STL** de `01`, `02` e `03`, já na orientação de impressão recomendada.
3. **STEP AP214** das quatro peças projetadas.
4. **Vista explodida** (Animation) com balões numerados.
5. **Renders** 1920 × 1080, fundo neutro: isométrica fechada; explodida; corte por YZ
   mostrando alavanca + garra; etiqueta aplicada numa peça de roupa simplificada.
6. **Desenho técnico 2D** de `01`, `02` e `03`: vistas frontal, superior, lateral,
   isométrica e um corte; cotas completas; tolerância geral ±0,2 mm (impressão, não usinagem).
7. Tabela de propriedades físicas por componente.

---

## 11. RELATÓRIO FINAL

- **Decisões adotadas**: toda ambiguidade que você resolveu e como.
- **Parâmetros criados** além da tabela §3, com justificativa.
- **Resultados das verificações** de §9.3, um a um, com o número obtido.
- **Orientação de impressão** recomendada por peça e necessidade de suporte.
- **Ordem de montagem** passo a passo, do vazio à etiqueta fechada.
- **Sensibilidade**: quais parâmetros de §3.2, se a medição real divergir muito da estimativa,
  quebram o modelo — e o que fazer em cada caso.

---

## 12. CRITÉRIOS DE ACEITE

- [ ] Todos os sketches totalmente restringidos.
- [ ] Nenhuma cota digitada solta.
- [ ] Nenhum item da timeline com nome genérico.
- [ ] Nenhuma peça comprada foi detalhada além do envelope.
- [ ] Zero interferências não intencionais, nas duas posições.
- [ ] A alavanca entrega **exatamente** `curso_garra` à haste.
- [ ] Todos os componentes comprados de §3.2 cabem no envelope, com `folga_impressao`.
- [ ] Massa da montagem sem o pino ≤ 70 g.
- [ ] Parede ≥ 1,6 mm em toda a carcaça.
- [ ] Cada peça projetada tem orientação de impressão viável, documentada.
- [ ] Todos os entregáveis de §10 gerados.

---

## 13. O QUE VOCÊ **NÃO** DEVE FAZER

- **Não projete a garra de esferas.** Ela é comprada. Se parecer que ficaria melhor
  projetada, você está fora do escopo.
- Não adicione compartimento de bateria — a etiqueta é energizada só na estação.
- Não substitua o fio SMA por solenoide ou servo sem reportar: a escolha veio do balanço de
  energia em `viabilidade-e-bom.md` §1.
- Não use snap fit — a união é por parafuso M2 com inserto térmico, porque snaps impressos
  quebram na reutilização.
- Não aplique ângulo de saída de injeção: a peça é impressa.
- Não altere o envelope externo para acomodar componentes. Se algo não couber, **reporte** —
  provavelmente a resposta é trocar o componente por um menor, não crescer a carcaça.

---

## APÊNDICE — Trilha A: o produto de produção (modelar só se sobrar tempo)

O modelo acima é o **protótipo**. Para as imagens da seção "Proposta" do relatório, um
segundo documento `TagAndGo_Produto.f3z` pode mostrar a versão de produção — **sem
mecanismo interno**, apenas o envelope estilizado:

- 42 × 67 × 15,5 mm, mesma silhueta em lágrima;
- superfície contínua, união por snap fit invisível, ângulo de saída de 1,5°;
- bobina de acoplamento indutivo no lugar dos contatos pogo;
- acabamento fosco grafite com um filete magenta na linha de partição.

Serve para render e para a comparação lado a lado "protótipo × produto" no relatório — que é,
por si só, uma boa figura para a seção de resultados.
