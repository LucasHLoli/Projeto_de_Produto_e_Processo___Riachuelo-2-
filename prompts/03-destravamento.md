# PARTE 03 — DESTRAVAMENTO ⭐ NÚCLEO DO PROJETO
## Como a etiqueta abre sem operador?

> Esta é a **única parte com engenharia de verdade** e o **caminho crítico** do projeto.
> Se ela falhar, nenhuma outra parte importa. Comece na semana 1.

---

## 0. Papel

Você é engenheiro mecatrônico. Sua tarefa é fazer uma etiqueta antifurto rígida **abrir
sozinha**, sem operador e sem bateria, em menos de 3 segundos.

---

## 1. Contexto mínimo (autossuficiente)

Hoje, para tirar a etiqueta rígida de uma peça de roupa, um funcionário do caixa encosta um
**destravador magnético**. Dentro da etiqueta há uma **garra de esferas**: três esferas de aço
presas numa gaiola com mola, apertadas contra a haste do pino por uma parede cônica. O ímã
afasta as esferas, o pino sai.

Enquanto só o funcionário puder fazer isso, existirá fila. Seu trabalho é substituir o
funcionário por um atuador dentro da própria etiqueta, acionado só depois do pagamento.

**Patente-base:** US 7.564.360 B2 (Checkpoint Systems) — etiqueta que se libera por sinal de
RF, sem bateria, com energia vinda de um interrogador dedicado.

---

## 2. Você recebe

De `CONTRATOS.md`:
- tempo máximo de destravamento: **3 s**;
- alimentação: **5 V por contatos elétricos**, vinda da Estação de Liberação;
- consumo em repouso: **zero** — a etiqueta não tem bateria;
- alvo de reuso: **500 ciclos**.

Da parte 05: o token chega validado. Você só recebe um sinal "pode abrir". **Não implemente
criptografia** — isso é da parte 05.

Você **entrega** para a parte 01: o espaço interno disponível para o inlay UHF.
Diga esse número cedo, senão eles compram um inlay que não cabe.

---

## 3. Você entrega

1. **Ensaio de bancada** provando que o atuador vence a garra (§5.2). É o entregável nº 1.
2. **Balanço de energia** justificando a escolha do atuador e da fonte (§5.3).
3. **Escolha do atuador** com matriz de decisão.
4. **CAD da carcaça** (ver `prompt-fusion360.md`).
5. **Protótipo físico** que abre de verdade, no mínimo 3 unidades.
6. **Ensaio de vida**: quantos ciclos aguenta antes de falhar.
7. Texto para `2-conteudo/2-metodologia.tex` (o balanço de energia é método) e dados para
   `4-resultados.tex`.

---

## 4. Restrições inegociáveis

- **Você não projeta a garra.** Compre hard tags comerciais e canibalize a garra delas.
  Projeto de mecanismo de esferas é trabalho de meses e não é o ponto do trabalho.
  Ganho colateral: o sistema fica compatível com o parque de etiquetas já instalado na loja.
- **Sem bateria.** A etiqueta é inerte fora da estação.
- **Sem operador.** Se sua solução exige que alguém encoste alguma coisa manualmente, ela não
  resolve o problema — só muda quem está na fila.
- A carcaça do protótipo pode ser **maior** que a do produto final. É protótipo, não DFM.

---

## 5. Método passo a passo

### 5.1 Semana 1 — comprar e desmontar

1. Compre **10 hard tags comerciais** baratas (R$ 3–5 cada) e **1 destravador magnético**.
2. Desmonte uma com serra ou dremel. Fotografe cada etapa — vira figura do relatório.
3. **Meça e anote:**

| Medida | Como | Vai virar o parâmetro |
|---|---|---|
| Ø externo da garra | paquímetro | `d_garra` |
| Altura da garra | paquímetro | `h_garra` |
| **Curso para liberar** | empurre a gaiola com um pino até o tack sair; meça o deslocamento | `curso_garra` |
| **Força da mola** | dinamômetro, ou empilhe pesos até a gaiola ceder | `forca_mola_garra` |
| Ø da haste do pino | paquímetro | `d_pino` |

> **`curso_garra` e `forca_mola_garra` são os dois números que definem todo o resto.**
> Sem eles medidos, qualquer projeto é chute.

### 5.2 Semana 2 — o ensaio que mata o projeto se for para morrer

**Faça isto antes de qualquer CAD, carcaça ou impressão.**

Montagem: garra presa numa morsa, fonte de bancada, atuador ligado direto. Sem carcaça,
sem microcontrolador, sem nada.

Teste três atuadores candidatos e preencha:

| Atuador | Força | Curso | Tempo | Energia | Cabe? | Custo |
|---|---|---|---|---|---|---|
| Fio SMA (nitinol) Ø0,15 mm | ~3,2 N `[VERIFICAR datasheet]` | 4% do comprimento | ~1,5 s | ~0,6 J | sim, ocupa quase nada | R$ 120/m |
| Micro servo SG90 | ~15 N·cm | angular | ~0,3 s | ~1 J | **não** — 29 mm de altura | R$ 15 |
| Micromotor N20 + came | alto | ilimitado | ~1 s | ~2 J | apertado | R$ 25 |
| Eletroímã / solenoide | baixo p/ o tamanho | ~2 mm | instantâneo | alto | talvez | R$ 20 |

**Critério de aprovação:** o atuador libera o pino em ≤ 3 s, com margem de força ≥ 1,5× sobre
`forca_mola_garra`, e cabe num envelope de 48 × 80 × 18 mm.

Se **nenhum** passar, pare e reporte ao time — é hora de rever o conceito, não de insistir.
Descobrir isso na semana 2 custa R$ 150 e uma tarde. Descobrir na semana 10 custa o trabalho.

### 5.3 O balanço de energia — o resultado mais forte do relatório

Energia necessária para um acionamento de SMA (Ø 0,15 mm, 50 mm, ~0,41 A, ~2,5 Ω, ~1,5 s):

**P = I²R = 0,41² × 2,5 = 0,42 W → E ≈ 0,63 J**

Compare com o que cada fonte entrega:

| Fonte | Potência realista | Tempo para 0,63 J | Veredito |
|---|---|---|---|
| RF ambiente (antena ~9 cm², ~0,1–1 µW/cm²) | ~5 µW | **~35 horas** | inviável, erra por 10⁵ |
| Campo NFC de leitor dedicado | ~6 mW | ~105 s | inviável pela experiência |
| Indução dedicada tipo Qi, 5 W | 5 W | ~1,5 s | viável |
| **Contatos elétricos (pogo pins)** | 5 W+ | ~1,5 s | **viável e trivial** |

**Conclusão a escrever no relatório:** o gargalo nunca foi a energia total — 0,63 J é
pouquíssimo. O gargalo é a **potência instantânea**. Isso obriga a etiqueta a receber energia
de uma fonte **dedicada e próxima**. Ou seja: **a Estação de Liberação não é conveniência de
projeto, é imposição física.**

> Isso contraria a patente? Não. O diagrama da US 7.564.360 inclui um *Tag Interrogation
> Device* — um interrogador dedicado. "Ambient RF" ali significa o campo do interrogador, não
> rádio do ambiente urbano. O que você fez foi **dimensionar** esse campo.

**Refaça esta conta com os seus números medidos.** A tabela acima é o roteiro, não o resultado.

### 5.4 Semana 3 — converter o movimento

Problema geométrico: o fio SMA precisa de comprimento **reto** (contrai só 4% do comprimento),
então fica deitado no plano da etiqueta. Mas a garra se move **na vertical**. Alguém tem que
converter.

> ### ⚠️ Correção — a alavanca *bell crank* foi descartada
>
> A primeira versão deste projeto usava uma alavanca bell crank com braços de 20 e 12 mm.
> **Não cabe:** para converter tração horizontal em movimento vertical, o braço de 20 mm
> precisaria ficar **em pé**, e a etiqueta tem só 18 mm de altura. A aritmética estava certa,
> a geometria não.
>
> Se você viu os números 20 mm / 12 mm / 5,3 N em alguma versão anterior, **ignore-os**.

**Solução adotada: dois fios SMA retos e paralelos + cursor com rampa.**

> Uma versão intermediária propunha um **laço de ~140 mm** passando por postes. Foi descartada:
> cada volta de 180° num poste multiplica a tensão por e^(μπ) ≈ 1,9 (efeito capstan), e duas
> voltas consomem 3,5× da força. O laço perde mais do que ganha. **Fios retos, sem poste.**

| | Bell crank | Laço de 140 mm | **2 fios retos** |
|---|---|---|---|
| Roteamento | alavanca com pivô | 2 postes, 180° cada | **nenhum desvio** |
| Perda por atrito de guia | — | ~3,5× | **nenhuma** |
| Cabe nos 18 mm de altura? | **não** | sim | sim |
| Curso | 2,0 mm | 5,6 mm (teórico) | 1,68 mm |
| Rampa | — | 12° | 35,5° |
| Força na garra | 5,3 N (irreal) | 5,8 N (irreal) | **4,96 N** |
| Margem sobre a mola | — | — | **1,98×** ✔ |

Contas, para você refazer com os seus números:

- curso de cada fio = 4% × 42 mm = **1,68 mm**
- ângulo da rampa: `tan θ = curso_garra / curso_sma` = 1,2 / 1,68 → **θ = 35,5°**
- ganho de força = `1 / tan θ` = **1,40×**
- eficiência com atrito (μ ≈ 0,3 entre PETG e aço):
  `tan θ / tan(θ + arctan μ)` = tan 35,5° / tan 52,2° = **0,554**
- força de tração de 2 fios = 2 × 3,2 N = 6,4 N
- força na garra = 6,4 × 1,40 × 0,554 = **4,96 N**
- margem sobre a mola de 2,5 N: **1,98×** ✔

Dois fios em paralelo dobram a força sem precisar de comprimento — e sem desvio nenhum.

Custo elétrico: R por fio = 50 Ω/m × 0,042 m = 2,1 Ω; dois em paralelo = 1,05 Ω;
I = 0,82 A; P = 0,71 W; em 1,5 s → **1,06 J**. O balanço da §5.3 não muda de conclusão.

**Meça `curso_garra` e `forca_mola_garra` e refaça estas seis linhas.** Se a margem cair abaixo
de 1,5×, acrescente um **terceiro fio** — é a correção mais barata: não muda geometria nenhuma,
só o furo da âncora. Não mude o envelope da carcaça.

> **O atrito é o item a verificar na bancada.** μ = 0,3 é estimativa. Meça a força real de
> saída da rampa antes de fechar o projeto — é a maior incerteza deste mecanismo.

### 5.5 Semanas 4–6 — carcaça e integração

Use `prompt-fusion360.md` (v2). Ele já está escrito para projetar **só** a carcaça e a
alavanca, em torno das peças compradas. Substitua os valores estimados da §3.2 daquele
arquivo pelos que você mediu na §5.1 daqui.

### 5.6 Semanas 7–8 — ensaio de vida

Cicle o mecanismo repetidamente e registre em que ciclo aparece a primeira falha. Alvo: 500.
Anote **o modo de falha**, não só o número — fio rompido, alavanca quebrada, garra gasta,
inserto solto. O modo de falha vale mais no relatório que o número de ciclos.

---

## 6. Perguntas que seu entregável precisa responder

1. Qual `curso_garra` e qual `forca_mola_garra`, medidos?
2. Qual atuador foi escolhido e por quê, com a matriz de decisão?
3. Quanta energia um acionamento consome, e qual fonte consegue entregar isso em 3 s?
4. Por que a colheita de RF ambiente **não** funciona? (a conta, não a opinião)
5. Em quanto tempo a etiqueta destrava, medido?
6. Quantos ciclos aguenta, e como falha?
7. Quanto custa a etiqueta protótipo, e quanto custaria em escala?

---

## 7. Critérios de aceite

- [ ] 10 hard tags compradas e uma desmontada e fotografada.
- [ ] `curso_garra` e `forca_mola_garra` **medidos**, não estimados.
- [ ] Ensaio de bancada (§5.2) executado, com os três candidatos comparados.
- [ ] Balanço de energia refeito com números próprios.
- [ ] Cinemática da alavanca verificada: curso e força conferem.
- [ ] Espaço interno para o inlay UHF informado à parte 01.
- [ ] 3 protótipos montados que destravam de verdade.
- [ ] Tempo de destravamento medido ≤ 3 s.
- [ ] Ensaio de vida executado, com modo de falha identificado.

---

## 8. O que NÃO fazer

- **Não projete a garra de esferas.** Se parecer que ficaria melhor projetada, você saiu do escopo.
- Não coloque bateria.
- Não implemente criptografia nem validação de token — parte 05.
- Não faça o app nem a interface — parte 02.
- Não comece pelo CAD. O CAD é a **semana 4**, depois do ensaio de bancada. Modelar antes de
  medir é o erro mais caro possível aqui.
- Não use dimensão estimada onde você pode medir a peça real.
- Não troque o atuador escolhido sem refazer o balanço de energia.
