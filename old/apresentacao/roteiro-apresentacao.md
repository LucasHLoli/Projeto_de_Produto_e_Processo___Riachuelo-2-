# Roteiro da apresentação: Relatório 1

**Estudo analítico do varejo de moda: mercado, clientes e requisitos para um sistema de autoatendimento**
PRO3474 · Poli-USP · parceria Riachuelo

Duração sugerida: **12 minutos** + perguntas. Seis blocos, um por pessoa. Troquem os nomes à vontade; cada bloco tem de 1,5 a 2,5 minutos.

A história que amarra tudo: **a fila existe, mas nem todo cliente quer se livrar do vendedor.** O projeto começou com uma ideia de produto, foi ouvir o mercado e o cliente e saiu com uma solução mais madura do que a ideia inicial.

---

## Bloco 1 · A cena (abertura) · ~1,5 min
**Quem:** Lucas · **Slide:** foto de fila de caixa em loja de shopping + título

> Imaginem um sábado à tarde, promoção, fila de dez minutos no caixa. A pessoa já escolheu a peça, já decidiu comprar, e mesmo assim não consegue sair da loja. Tem gente que desiste ali.
>
> Nosso projeto com a Riachuelo partiu dessa cena. A ideia inicial era simples: e se o próprio cliente pagasse pelo aplicativo e liberasse a etiqueta antifurto sozinho, sem passar pelo caixa?
>
> Antes de desenhar qualquer produto, a gente quis responder três perguntas: esse mercado existe? O cliente quer isso? E, se quer, o que o produto precisa fazer? O relatório segue essas perguntas nessa ordem.

**Transição:** "Começando pela primeira: o mercado."

---

## Bloco 2 · O mercado · ~2 min
**Quem:** Danilo · **Slides:** números do setor; gráfico de receita; quadro TAM/SAM/SOM

- O varejo têxtil brasileiro faturou **R$ 427,1 bilhões em 2025**, mas é pulverizado: as 11 maiores empresas de capital aberto ficam com cerca de **15%**.
- O segmento-alvo é o **mass market / fast fashion que já usa self-checkout**. Nele, a fila pesa mais, porque o volume é alto e o tíquete é menor.
- Três redes em estágios diferentes:
  - **Renner**, a mais madura: **742 terminais em 213 lojas**, com cerca de **38% dos pagamentos** nessas lojas.
  - **C&A**, intermediária: código de barras na maior parte da rede e RFID no conceito Energia desde 2025.
  - **Riachuelo**, em piloto: loja conceito em Curitiba (abril de 2026) e plano de **15 a 20 lojas** ainda em 2026.
- **SOM:** essas 15 a 20 lojas. É a janela em que a Riachuelo está padronizando o checkout, o melhor momento para propor uma solução.

> Resumindo: existe mercado, e a Riachuelo está atrás dos concorrentes justamente no momento de decidir o que fazer.

**Transição:** "Mercado existe. Mas quem é o cliente que vai usar isso?"

---

## Bloco 3 · Quem é o cliente e como a gente ouviu · ~2 min
**Quem:** Gabriel · **Slides:** atores (B2B e loja); desenho da pesquisa

- O projeto tem **dois níveis**: a Riachuelo compra a solução (B2B), e o consumidor usa na loja. O relatório separa os dois o tempo todo.
- Pesquisa em duas frentes, que se completam:
  - **Survey com 142 respostas**: mede quantas pessoas sentem cada problema.
  - **11 entrevistas individuais**: explicam o porquê. A solução só era apresentada no final, para não contaminar o relato.
- Escolhemos entrevista individual e não grupo focal porque o assunto envolve orçamento e insegurança para decidir sozinho, temas que a pessoa suaviza na frente dos outros.

**Transição:** "E o que a gente descobriu mudou nossa leitura do problema."

---

## Bloco 4 · O que os dados mostraram (virada da história) · ~2,5 min
**Quem:** Mateus · **Slides:** gráfico dos 4 grupos; gráfico da confiança sem checagem por grupo; uma frase de entrevista

- A idade e o tipo de loja explicaram pouco. O que separou os clientes foram **duas coisas**: o quanto a pessoa já é autônoma com tecnologia e se ela sofre para achar tamanho e cor.
- A clusterização gerou **quatro grupos**:

| Grupo | % | Reação à compra sem checagem |
|---|---|---|
| Dependentes de atendimento | 39% | 96% rejeitam |
| Autônomos digitais | 21% | 100% aceitam |
| Frustrados com disponibilidade | 9% | quase todos neutros |
| Pragmáticos equilibrados | 31% | 91% neutros |

- **A virada:** só **24%** da amostra endossou a compra sem checagem. A ideia não serve para todo mundo.
- Para quem depende de ajuda, perder o vendedor pesa mais que a tecnologia falhar. Uma entrevistada disse que perder esse contato "é mais importante que a tecnologia funcionar direitinho".
- E a mesma pessoa pode querer autonomia para escolher a peça e ajuda para achar o tamanho.

> Aqui a gente mudou de postura: o produto não pode tirar o atendimento. Ele tem de oferecer uma via rápida para quem quer, sem tirar o vendedor de quem precisa.

**Transição:** "Então como a gente transforma isso em requisito de engenharia?"

---

## Bloco 5 · Do cliente ao requisito: casa da qualidade · ~2 min
**Quem:** D'Alessandro · **Slides:** 20 vozes → 7; casa da qualidade; benchmarking

- As entrevistas e o survey viraram **20 vozes do cliente** (8 necessidades, 7 desejos, 5 demandas). Sete foram para o QFD.
- **Benchmarking** contra Renner, C&A e Zara: a Riachuelo teve a menor nota justamente nas vozes de maior peso, a **espera no caixa** e a **via rápida sem perder o atendimento**.
- Com isso, a espera no caixa ficou com **33% do peso** das vozes.
- **Requisitos mais importantes:** liberação da peça só depois do pagamento confirmado, tempo de pagamento e clareza do fluxo no app. Os três somam **cerca de 71%**.
- **Telhado da casa:** atendimento humano **conflita** com rapidez e autonomia. Por isso ele fica como opção acionada pelo cliente, fora do fluxo principal.
- **Metas:** pagamento em até **45 s**, **100%** de liberação correta e atendimento disponível em **100%** das falhas.

**Transição:** "E como fica isso na mão do cliente?"

---

## Bloco 6 · O produto e o fechamento · ~2 min
**Quem:** Pedro · **Slides:** esboço à mão livre; detalhe do mecanismo; fluxo de uso em 4 passos

- **Dispositivo rígido de 98 × 82 × 26 mm**, preso à roupa como as etiquetas de hoje.
- **Na face:** código impresso, luz e botão.
- **Por dentro:** embreagem de esferas, a mesma lógica das etiquetas atuais. Um atuador interno libera o carretel no lugar do destravador do caixa.
- **Uso em 4 passos:**
  1. Lê o código com o celular.
  2. Paga no app.
  3. A luz passa de **vermelha a verde**.
  4. Aperta o botão e a peça solta.

  A autorização vai do celular para o dispositivo, então, se a internet da loja cair depois do pagamento, a compra continua.
- **Fechamento:**

> A gente começou querendo acabar com a fila. Terminou entendendo que o valor está em dar uma via rápida para quem já compra sozinho, sem tirar o vendedor de quem precisa dele. Os próximos passos são visitar as lojas para medir os concorrentes, testar esses encaixes com os clientes e construir o protótipo.

**Último slide:** "Obrigado", com as perguntas que ficam em aberto.

---

## Perguntas prováveis da banca e respostas curtas

**"Por que a Riachuelo não copia a Renner?"**
> A Renner usa terminal fixo com RFID, então o cliente ainda vai até um ponto e pode pegar fila no terminal. Na nossa proposta, a liberação acontece na própria peça, em qualquer lugar da loja. E a pesquisa mostrou que o valor está em manter caixa, vendedor e via rápida juntos.

**"Os valores do benchmarking técnico foram medidos?"**
> Não. As notas de 1 a 5 são avaliação da equipe, como o método prevê, e os tempos e percentuais dos concorrentes são estimativas baseadas nas fontes; o relatório diz isso. O único dado publicado é o 38% da Renner. As visitas às lojas estão planejadas para substituir as estimativas.

**"A amostra é representativa?"**
> Não dá para afirmar. São 142 respostas e 11 entrevistas, sem recrutamento aleatório documentado. Por isso tratamos os percentuais como padrões desta amostra, não como números da base de clientes da Riachuelo.

**"Só 24% aceitam. O produto faz sentido?"**
> Faz para um público definido: os autônomos digitais aceitaram 100% e são os que mais desistem por fila. Para os outros grupos, levantamos hipóteses de encaixe, como liberar vendedores do caixa para o salão e mostrar estoque no app. Elas ainda precisam ser testadas.

**"O destravador magnético vendido na internet não abre essa etiqueta?"**
> Abre, se o carretel continuar sendo de metal ferromagnético. Como o nosso acionamento é mecânico, dá para trocar essa peça por uma não magnética e ficar imune ao destravador comum. Isso está em avaliação.

**"Por que a meta de pagamento é 45 s?"**
> Porque 60 s só empataria com a estimativa de Renner e Zara. Uma meta que não supera o concorrente não gera vantagem.

---

## Checklist rápido antes de apresentar
- [ ] Todo mundo sabe a frase de transição do próprio bloco
- [ ] Slides com **uma ideia cada** e números grandes; nada de parágrafo no slide
- [ ] Cronometrar um ensaio completo (meta: 12 min)
- [ ] Levar o PDF do relatório aberto para mostrar a casa da qualidade se pedirem
- [ ] Combinar quem responde cada tipo de pergunta: mercado (Danilo), pesquisa (Gabriel/Mateus), QFD (D'Alessandro), produto (Lucas)
