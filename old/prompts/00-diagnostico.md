# PARTE 00 — DIAGNÓSTICO
## O problema existe? Custa quanto?

---

## 0. Papel

Você é analista de operações. Sua tarefa é **provar com número** que a fila em loja de moda é
um problema que vale resolver — ou descobrir que não é. As duas respostas são resultados
válidos; a inválida é achismo.

---

## 1. Contexto mínimo (autossuficiente)

O projeto propõe eliminar a fila do caixa em lojas Riachuelo, permitindo que o cliente pague
pelo celular e destrave sozinho a etiqueta antifurto da peça. Antes de propor qualquer coisa,
alguém precisa medir o tamanho do problema.

Hipótese central a testar: **o gargalo do caixa não é o pagamento, é a remoção da etiqueta
antifurto** — e por isso o autoatendimento que funciona em supermercado não funciona em moda.

---

## 2. Você recebe

Nada de outras partes. Esta é a única parte totalmente independente — pode começar hoje.

---

## 3. Você entrega

1. **Cronoanálise de campo** — tabela bruta de tempos medidos em loja.
2. **Decomposição do tempo de caixa** por etapa, com média e desvio.
3. **Modelo de fila** M/M/c calibrado com os dados medidos.
4. **Curva tempo de espera × horário do dia**, mostrando o pico.
5. **Custo estimado da fila**: vendas perdidas por desistência + custo de mão de obra de caixa.
6. **Custo da quebra** (furto) no varejo de vestuário — pesquisa bibliográfica.
7. Texto pronto para `2-conteudo/1-diagnostico.tex`, com figuras e tabelas.

---

## 4. Restrições

- **Dado primário vale mais que dado de internet.** Uma tarde com cronômetro numa loja vale
  mais na avaliação que dez citações.
- Se não conseguir medir em loja Riachuelo, meça em **qualquer** loja de vestuário com
  etiqueta antifurto rígida e declare isso como limitação.
- Todo número sem fonte medida ou citada vira `[MEDIR]` ou `[CITAR]`. Não invente.
- Não proponha solução nesta parte. Diagnóstico é diagnóstico.

---

## 5. Método passo a passo

### 5.1 Protocolo de medição em campo

Vá em **três janelas distintas**: um dia útil de manhã, um dia útil no fim da tarde, e um
sábado à tarde. Mínimo de **30 atendimentos observados por janela**.

Para cada cliente atendido, cronometre e anote:

| Campo | Como medir |
|---|---|
| `hora` | relógio, minuto cheio |
| `n_fila` | quantas pessoas na fila quando o cliente entrou nela |
| `t_espera` | da entrada na fila até chegar ao caixa |
| `t_scan` | do início da leitura do primeiro item até o último |
| `t_etiqueta` | **tempo só removendo etiquetas rígidas** — cronometrar separado |
| `t_pagamento` | do total fechado até a aprovação |
| `t_embalagem` | ensacar e entregar |
| `n_itens` | quantas peças |
| `n_etiquetas` | quantas tinham etiqueta rígida |
| `caixas_abertos` | quantos operadores atendendo naquele momento |

**`t_etiqueta` é a medida mais importante do trabalho.** É ela que testa a hipótese central.
Cronometre com cuidado e separadamente das outras etapas.

Registre também **desistências**: pessoas que entraram na fila e saíram sem comprar. Conte-as
por janela de 15 minutos.

### 5.2 Tratamento dos dados

1. Média, desvio-padrão e histograma de cada tempo.
2. **Fração do tempo de caixa gasta em etiqueta**: `t_etiqueta / (t_scan + t_etiqueta + t_pagamento + t_embalagem)`.
3. Regressão de `t_etiqueta` contra `n_etiquetas` — deve ser aproximadamente linear; o
   coeficiente angular é o **tempo por etiqueta**, o número que o projeto ataca.
4. Taxa de chegada `λ` por janela (clientes/min) e taxa de serviço `μ` (1 / tempo médio de atendimento).

### 5.3 Modelo de fila

Use **M/M/c** com `c` = número de caixas abertos:

- Intensidade de tráfego: `ρ = λ / (c·μ)`
- Tempo médio de espera `Wq` pela fórmula de Erlang C
- Rode o modelo **duas vezes**: com o `t_etiqueta` medido, e com `t_etiqueta = 0`
  (cenário do projeto). A diferença entre os dois `Wq` **é o benefício do projeto**.

Ferramenta: planilha ou Python. Documente a fórmula usada.

### 5.4 Custo

- **Venda perdida** = (desistências/hora) × (ticket médio) × (horas de pico/ano) × (nº de lojas).
  Ticket médio: relatório anual da Riachuelo (empresa de capital aberto, dados públicos). `[CITAR]`
- **Mão de obra de caixa** = (nº de caixas) × (horas) × (custo-hora com encargos). `[CITAR]`
- **Quebra por furto**: busque índice de perdas do varejo de vestuário brasileiro em
  publicações setoriais. `[CITAR]`

---

## 6. Perguntas que seu entregável precisa responder

1. Qual a fração do tempo de caixa gasta só removendo etiqueta antifurto?
2. Quantos segundos por etiqueta?
3. Qual o tempo médio de espera no pico, hoje?
4. Quanto esse tempo cairia se `t_etiqueta` fosse zero?
5. Quantas vendas se perdem por desistência de fila?
6. O problema é grande o bastante para justificar o projeto? **Responda com sim ou não.**

---

## 7. Critérios de aceite

- [ ] Mínimo de 90 atendimentos cronometrados, em 3 janelas distintas.
- [ ] `t_etiqueta` medido **separadamente** das outras etapas.
- [ ] Desistências contadas, não estimadas.
- [ ] Modelo de fila rodado nos dois cenários, com a fórmula documentada.
- [ ] Todo número tem fonte: medição própria ou citação.
- [ ] A pergunta 6 está respondida com sim ou não, sem rodeio.
- [ ] Texto e figuras prontos para `1-diagnostico.tex`.

---

## 8. O que NÃO fazer

- Não proponha a solução — isso é das partes 01 a 06.
- Não use estatística de varejo americano ou europeu como se fosse brasileira.
- Não meça só um horário: sem o contraste pico × vale, não há curva e não há argumento.
- Não fotografe pessoas nem grave áudio na loja. Cronômetro e anotação bastam, e evitam
  problema de privacidade.
- Se a medição mostrar que a fila **não** é problema, escreva isso. Um diagnóstico que
  desmonta a própria hipótese é um resultado honesto e defensável.
