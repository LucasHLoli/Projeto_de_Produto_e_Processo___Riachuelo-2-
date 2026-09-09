# Índice dos prompts — Riachuelo Tag&Go
## Dividir para conquistar

Cada arquivo desta pasta é um **prompt independente e autossuficiente**. Quem receber um
deles não precisa ler os outros — o contexto necessário está dentro.

O que **todos** precisam ler antes: **`CONTRATOS.md`**. É o que garante que as partes encaixem.

---

## As partes

| # | Arquivo | Problema | Dificuldade | Tipo de trabalho |
|---|---|---|---|---|
| 00 | `00-diagnostico.md` | A fila custa quanto? O problema existe? | baixa | campo + estatística |
| 01 | `01-identificacao.md` | Como o celular sabe qual peça é? | baixa | eletrônica passiva |
| 02 | `02-app-pagamento.md` | Como cobrar sem caixa? | média | software |
| 03 | `03-destravamento.md` | **Como a tag abre sem operador?** | **alta** | **mecânica + energia** |
| 04 | `04-portico.md` | Como saber que ninguém levou item não pago? | média | RF + decisão de custo |
| 05 | `05-autorizacao.md` | Como amarrar "pagou" a "destrava"? | média | protocolo/segurança |
| 06 | `06-logistica-tag.md` | A tag volta pro ciclo? | baixa | processo + custo |
| 07 | `07-escopo-entrega.md` | O que o trabalho tem que entregar? | — | gestão |

**A parte 03 é a única com engenharia de verdade.** As outras são importantes, mas 01/02/05
usam tecnologia pronta, 04 é decisão de orçamento, 06 é processo e 00/07 são levantamento.
Se o tempo apertar, é a 03 que não pode ser cortada.

---

## Ordem de dependência

```
07 (escopo)  ->  define ate onde vai tudo
                     |
   +-----------------+------------------+
   |                 |                  |
  00              03 (nucleo)          01
diagnostico     destravamento      identificacao
   |                 |                  |
   |                 v                  v
   |                05  <-------------  02
   |            autorizacao          app/pagamento
   |                 |
   |                 v
   +--------------> 04  ->  06
                  portico   logistica
```

- **07 primeiro** — sem decidir o escopo, todo mundo trabalha no vazio.
- **03 é caminho crítico** — comece na semana 1, é o que pode matar o projeto.
- **00, 01 e 02 rodam em paralelo** desde o início, não dependem de nada.
- **04 e 06 são os últimos** e são os primeiros a cortar se faltar tempo.

---

## Sugestão de divisão para 8 pessoas (4 duplas)

| Dupla | Partes | Arquivo LaTeX que escreve |
|---|---|---|
| **A** | 00 Diagnóstico + 06 Logística | `2-conteudo/1-diagnostico.tex` |
| **B** | **03 Destravamento** (parte maior, dupla mais técnica) | `2-conteudo/2-metodologia.tex` |
| **C** | 01 Identificação + 02 App + 05 Autorização | `2-conteudo/3-proposta.tex` |
| **D** | 04 Pórtico + consolidação dos resultados | `2-conteudo/4-resultados.tex` |

A parte **07** é de quem estiver coordenando — uma pessoa, não uma dupla.

---

## Como usar um prompt

1. Leia `CONTRATOS.md`.
2. Abra o prompt da sua parte.
3. Cole na ferramenta de IA que estiver usando, **ou** use como roteiro de trabalho manual —
   os dois funcionam, os prompts estão escritos como especificação, não como conversa.
4. A seção "Critérios de aceite" de cada prompt é o que define quando sua parte está pronta.
5. A seção "O que NÃO fazer" existe para você não invadir a parte de outra dupla.

---

## Regra para todos

Quando um prompt pedir um número que você não tem, **não invente**. Escreva
`[MEDIR]` ou `[COTAR]` e siga. Um número inventado num relatório de engenharia é pior
que um espaço em branco declarado.
