# PARTE 06 — LOGÍSTICA DA ETIQUETA
## A etiqueta volta pro ciclo?

> Esta parte parece secundária e **não é**. Uma etiqueta que custa R$ 60 e não volta destrói a
> economia do projeto inteiro. É aqui que a proposta ganha ou perde viabilidade financeira.

---

## 0. Papel

Você é engenheiro de produção e processos. Sua tarefa é desenhar o **ciclo de vida da
etiqueta** dentro da operação da loja e provar, com uma conta, que ele fecha.

---

## 1. Contexto mínimo (autossuficiente)

Hoje, a etiqueta antifurto rígida é removida pelo operador do caixa e cai num pote ao lado da
máquina registradora. O funcionário garante o retorno — sem esforço, porque ela nunca sai da
mão dele.

No sistema proposto, **não há funcionário**. O cliente destrava sozinho numa estação de
autoatendimento e pode simplesmente sair com a etiqueta na sacola, jogá-la fora, ou levá-la
para casa sem perceber.

A etiqueta proposta é **muito mais cara** que a atual (tem eletrônica dentro). Se a taxa de
retorno cair, o custo por uso explode e o projeto não se paga.

**Este é o risco de negócio número um do projeto.** Não é o risco técnico — é o econômico.

---

## 2. Você recebe

De `CONTRATOS.md`:
- taxa de retorno alvo: **95%**;
- ciclos de reuso alvo: **500**;
- os estados da etiqueta, incluindo `DESTRAVADA` → `LIVRE`.

Da parte 03: o custo unitário real da etiqueta protótipo e a estimativa em escala.
Da parte 00: o volume de peças vendidas por loja por dia.

Se esses números ainda não existirem, **trabalhe com faixas** e faça análise de sensibilidade.
Não fique parado esperando.

---

## 3. Você entrega

1. **Fluxograma do ciclo de vida** da etiqueta, do CD à devolução, com os pontos de perda.
2. **Modelo de custo por uso** em função da taxa de retorno — a conta central desta parte.
3. **Taxa de retorno mínima** para o projeto se pagar (o ponto de equilíbrio).
4. **Mecanismos de incentivo** ao retorno, comparados.
5. **Desenho da estação de devolução** e da sua posição no layout da loja.
6. **Plano de aplicação** das etiquetas: no CD ou na loja?
7. Texto para `2-conteudo/1-diagnostico.tex` (seção de processo) e `4-resultados.tex`.

---

## 4. Restrições

- **Não pode depender de boa vontade do cliente.** "O cliente devolve porque é legal" não é
  projeto de processo, é torcida. Todo mecanismo precisa de um motivo concreto.
- Não pode reintroduzir um funcionário no fluxo — isso recriaria a fila que o projeto elimina.
- Não pode constranger quem esquecer. Multa ou cobrança automática destrói a experiência que o
  projeto vende.
- A etiqueta destravada **não pode sair da loja sem ser notada** — mas a solução tem que ser
  suave, não policial.

---

## 5. Método passo a passo

### 5.1 Fluxograma do ciclo

Mapeie e desenhe, marcando **onde a etiqueta pode se perder**:

```
CD: etiqueta LIVRE -> aplicada na peca -> TRAVADA
        |
        v
   loja: arara -> provador -> arara  (ciclo interno, sem perda)
        |
        v
   cliente paga -> AUTORIZADA
        |
        v
   Estacao de Liberacao -> DESTRAVADA   <- PONTO DE PERDA 1
        |
        v
   caixa de devolucao -> LIVRE          <- PONTO DE PERDA 2
        |
        v
   volta ao CD ou reaplica na loja      <- PONTO DE PERDA 3
```

Para cada ponto de perda, estime a probabilidade e proponha a contramedida.

### 5.2 A conta central — custo por uso

```
custo_por_uso = custo_etiqueta / numero_esperado_de_usos

numero_esperado_de_usos = 1 / (1 - taxa_retorno)     [ate o limite de 500 ciclos]
```

Monte esta tabela com o custo real vindo da parte 03:

| Taxa de retorno | Usos esperados | Custo por uso (etiqueta de R$ 60) | Custo por uso (R$ 25 em escala) |
|---|---|---|---|
| 50% | 2 | R$ 30,00 | R$ 12,50 |
| 80% | 5 | R$ 12,00 | R$ 5,00 |
| 90% | 10 | R$ 6,00 | R$ 2,50 |
| 95% | 20 | R$ 3,00 | R$ 1,25 |
| 99% | 100 | R$ 0,60 | R$ 0,25 |
| 99,8% | 500 (teto) | R$ 0,12 | R$ 0,05 |

> Repare no formato da curva: entre 50% e 90% o ganho é enorme, e depois de 99% quase não muda.
> **A taxa de retorno é o parâmetro mais sensível do modelo econômico inteiro.** Diga isso no
> relatório e mostre a curva — é uma das melhores figuras que o trabalho pode ter.

Compare com o custo atual: etiqueta comum a R$ 3–5, com retorno ~100% porque o funcionário
segura. `[COTAR]`

**Ponto de equilíbrio:** com que taxa de retorno o custo por uso iguala o da operação atual
somado à economia de mão de obra de caixa (número que vem da parte 00)?

### 5.3 Mecanismos de retorno — compare, não escolha por gosto

| Mecanismo | Como funciona | Eficácia esperada | Custo | Risco |
|---|---|---|---|---|
| **Retorno forçado pela geometria** | a etiqueta só destrava **dentro** da estação, e cai por gravidade numa caixa fechada; o cliente sai com a peça, nunca com a etiqueta | **alta** | baixo | exige projeto da estação |
| Desconto por devolução | R$ 1 de crédito no app por etiqueta devolvida | média | R$ 1/uso | fraudável |
| Caução no preço | valor devolvido ao devolver a etiqueta | alta | atrito na compra | cliente odeia |
| Aviso no app | "não esqueça de deixar a etiqueta" | baixa | zero | é só torcida |
| Detecção no pórtico | pórtico avisa se uma etiqueta destravada está saindo | média | já existe (parte 04) | falso alarme |

> **Recomendação forte: o primeiro.** Resolva por **projeto**, não por incentivo. Se a etiqueta
> fisicamente não puder sair da estação destravada, a taxa de retorno vira ~100% e a conta da
> §5.2 deixa de ser um risco. Um problema de comportamento resolvido por geometria é sempre
> melhor que um resolvido por incentivo.
>
> Isto é um **requisito para a parte 03**: avise-os cedo, porque muda o projeto da estação.

### 5.4 Estação de devolução e layout

- Onde fica, no caminho natural entre provador e saída?
- Quantas por loja, em função do volume da parte 00?
- Capacidade da caixa coletora: quantas etiquetas antes de precisar esvaziar?
- Quem esvazia, com que frequência, e isso é trabalho novo para a loja?
- **Comparação de layout**: planta da loja hoje (com fila de caixas) × planta proposta.
  Quanta área de venda é liberada?

### 5.5 Aplicação das etiquetas

| Onde | Vantagem | Desvantagem |
|---|---|---|
| No CD | peça chega pronta para a arara; trabalho concentrado | logística reversa CD↔loja para as etiquetas |
| Na loja | ciclo curto, etiqueta não viaja | trabalho manual na loja |

Escolha e justifique com a conta do transporte reverso.

---

## 6. Perguntas que seu entregável precisa responder

1. Qual o custo por uso da etiqueta, em função da taxa de retorno?
2. Qual a taxa de retorno **mínima** para o projeto se pagar?
3. Qual mecanismo garante essa taxa — e ele depende de comportamento do cliente ou de geometria?
4. Quantas estações por loja, e onde no layout?
5. Aplicar no CD ou na loja?
6. Quanta área de venda a loja ganha ao perder a fila de caixas?
7. O que acontece com a etiqueta que sai da loja mesmo assim?

---

## 7. Critérios de aceite

- [ ] Fluxograma completo com os pontos de perda marcados.
- [ ] Tabela e **curva** de custo por uso × taxa de retorno.
- [ ] Ponto de equilíbrio calculado, com o dado de mão de obra vindo da parte 00.
- [ ] Os 5 mecanismos comparados, com um escolhido e justificado.
- [ ] Requisito de retorno forçado comunicado à parte 03, se for essa a escolha.
- [ ] Layout antes × depois desenhado.
- [ ] Decisão CD × loja justificada com conta.

---

## 8. O que NÃO fazer

- Não assuma taxa de retorno sem justificar de onde veio o número.
- Não proponha multa nem cobrança automática de quem esquecer.
- Não recoloque um funcionário no fluxo — seria admitir a derrota do projeto.
- Não projete a estação mecanicamente — isso é da parte 03. Você entrega o **requisito**
  ("a etiqueta não pode sair destravada da estação"), eles resolvem como.
- Não trate isto como seção de enchimento. A curva da §5.2 é um dos resultados mais fortes que
  o trabalho tem para mostrar.
