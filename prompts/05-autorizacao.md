# PARTE 05 — AUTORIZAÇÃO E SEGURANÇA
## Como amarrar "pagou" a "destrava"?

> Esta parte é a **contribuição original do projeto**. A patente-base US 7.564.360 destrava a
> etiqueta com um sinal de RF **aberto, sem autenticação nenhuma**. Quem clonar o sinal abre
> qualquer etiqueta da loja. Consertar isso é o que o trabalho acrescenta ao estado da arte.

---

## 0. Papel

Você é engenheiro de segurança de sistemas embarcados. Sua tarefa é garantir que a etiqueta
antifurto abra **se, e somente se**, o item foi pago.

---

## 1. Contexto mínimo (autossuficiente)

O cliente paga pelo celular e apoia a peça numa **Estação de Liberação** — um equipamento de
bancada sem funcionário, que energiza a etiqueta por contatos elétricos e manda o comando de
abrir.

A pergunta que você resolve: **o que impede alguém de construir uma estação falsa em casa e
abrir peças roubadas?**

Referência de comparação honesta: hoje, destravadores magnéticos são vendidos abertamente na
internet por poucas dezenas de reais e abrem qualquer etiqueta de qualquer loja. Qualquer
solução sua já será melhor que o estado atual — mas isso não é desculpa para não fazer direito.

---

## 2. Você recebe

De `CONTRATOS.md`:
- estrutura do token (`tag_id`, `item_id`, `nonce`, `exp`, `hmac`);
- uso único, validade ≤ 120 s, vinculado à `tag_id`;
- chave HMAC **por etiqueta**, gravada na fabricação, nunca trafega;
- **quem pede o token é a Estação, nunca o app**;
- interface física: 5 V + UART pelos contatos.

Da parte 02: backend com `/pay` funcionando e o evento de venda gravado.
Da parte 03: uma etiqueta com microcontrolador que aciona o atuador ao receber um sinal.

---

## 3. Você entrega

1. **Modelo de ameaças**: quem ataca, com que capacidade, com que ganho.
2. **Protocolo de autorização** especificado — diagrama de sequência, mensagem a mensagem.
3. **Implementação** nos dois lados: firmware da etiqueta e da estação, mais o `/release-token`.
4. **Gestão de chaves**: como a chave entra na etiqueta na fabricação e onde vive no backend.
5. **Ensaio de ataque**: você mesmo tenta quebrar, e documenta o resultado.
6. Texto para `2-conteudo/3-proposta.tex` — é aqui que mora a originalidade do trabalho.

---

## 4. Restrições

- **O app nunca recebe o token.** Se o celular do cliente pudesse pedir a autorização, um
  aparelho modificado emitiria autorizações sozinho. Esta regra não é negociável nem por
  conveniência de implementação.
- **A chave nunca trafega.** Nem cifrada. Só desafio e resposta.
- **A etiqueta não guarda estado entre acionamentos** — ela fica sem energia. Isso significa
  que ela **não consegue lembrar** de nonces já usados. Trate esse problema explicitamente
  (§5.3): é o ponto mais difícil da sua parte.
- Nada de criptografia inventada. Use HMAC-SHA256, que já existe pronto no ESP32.

---

## 5. Método passo a passo

### 5.1 Modelo de ameaças

Preencha honestamente:

| # | Atacante | Capacidade | Ganho | Prioridade |
|---|---|---|---|---|
| 1 | Cliente oportunista | celular, app | uma peça | **alta** — é o caso comum |
| 2 | Furtador com equipamento | estação falsa, osciloscópio | muitas peças | **alta** |
| 3 | Funcionário interno | acesso ao backend e às etiquetas | escala | média |
| 4 | Atacante remoto | internet, sem acesso físico | dados, fraude de pagamento | média |
| 5 | Atacante com força bruta | alicate | uma peça, danificando | **baixa — ignore** |

> A ameaça 5 é deliberadamente fora de escopo: quem arranca a etiqueta à força já é problema
> do pórtico e da etiqueta costurada, não do protocolo. Declare isso no relatório em vez de
> tentar resolver tudo.

### 5.2 Protocolo — sequência a implementar

```
1. cliente paga no app                    -> backend grava EVENTO DE VENDA
2. cliente apoia a peca na Estacao
3. Estacao energiza a etiqueta (5 V)
4. etiqueta acorda e envia:  tag_id
5. Estacao -> backend:  POST /release-token { tag_id }
6. backend verifica: existe venda paga para o item_id ligado a esta tag_id,
   nos ultimos 5 min?
      nao -> 403, fim
      sim -> gera nonce, exp = agora + 120 s,
             hmac = HMAC-SHA256(chave_da_tag, tag_id|item_id|nonce|exp)
7. backend -> Estacao -> etiqueta:  o token
8. etiqueta recalcula o hmac com a propria chave e compara
      diferente -> nao abre
      igual     -> aciona o atuador
9. etiqueta confirma abertura -> Estacao -> backend marca DESTRAVADA
```

Note que o celular **não aparece** dos passos 3 ao 9. É essa a defesa contra a ameaça 1.

### 5.3 O problema difícil: a etiqueta não lembra de nada

A etiqueta perde a energia entre um uso e outro. Logo, ela não consegue guardar uma lista de
nonces já usados, e um token capturado poderia ser reapresentado depois.

Você tem três saídas. **Escolha uma, justifique, e implemente:**

| Saída | Como funciona | Custo | Problema |
|---|---|---|---|
| **A — Desafio da etiqueta** | a etiqueta gera um número aleatório e **ela** desafia a estação; a resposta só serve para aquele desafio | precisa de gerador aleatório no chip | o melhor caminho — o ESP32 tem RNG por hardware |
| B — Contador em memória não volátil | a etiqueta grava um contador crescente na flash e rejeita valores menores | desgaste da flash em 500 ciclos é aceitável | mais simples que A, mas gasta escrita |
| C — Janela de tempo curta | confia só no `exp` de 120 s | zero | **insuficiente sozinho** — 120 s bastam para um replay |

> **Recomendação: A.** Inverter a direção do desafio resolve o problema sem memória e sem
> relógio na etiqueta. Se escolher B ou C, escreva por que A foi descartada.

### 5.4 Gestão de chaves

Responda, com procedimento, não com intenção:

1. Como a chave entra na etiqueta na fabricação?
2. Onde ela vive no backend — em claro, em HSM, cifrada com chave mestra?
3. O que acontece se uma etiqueta for aberta e a chave extraída? (deve comprometer **só** aquela)
4. Como revogar uma etiqueta comprometida?
5. Quem, na Riachuelo, teria acesso ao banco de chaves?

### 5.5 Ensaio de ataque — você ataca o seu próprio sistema

Execute e documente o resultado de cada tentativa:

| # | Ataque | Resultado esperado |
|---|---|---|
| 1 | Capturar o tráfego dos contatos e reapresentar (*replay*) | rejeitado |
| 2 | Usar token da etiqueta A na etiqueta B | rejeitado |
| 3 | Usar token depois de expirado | rejeitado |
| 4 | Estação falsa sem o backend | rejeitado |
| 5 | Pedir `/release-token` direto do celular | **rejeitado — este é o teste que mais importa** |
| 6 | Alimentar a etiqueta com 5 V e mandar lixo pela UART | não abre, não trava |
| 7 | Pagar um item barato e tentar abrir a etiqueta de um caro | rejeitado |

Se algum passar, conserte e documente **os dois estados** — o furo e a correção. Um relatório
que mostra o ataque encontrado e resolvido vale mais que um que só afirma ser seguro.

---

## 6. Perguntas que seu entregável precisa responder

1. Qual o modelo de ameaças, e o que está declaradamente fora de escopo?
2. Como o replay é impedido, dado que a etiqueta não tem memória nem relógio?
3. Onde vivem as chaves, e o que uma etiqueta comprometida derruba?
4. Os 7 ataques da §5.5 foram todos rejeitados? Se não, qual passou e como foi corrigido?
5. O sistema é mais seguro que o destravador magnético de hoje? **Em quê, concretamente?**

---

## 7. Critérios de aceite

- [ ] Modelo de ameaças escrito, com escopo e não-escopo explícitos.
- [ ] Diagrama de sequência do protocolo, mensagem a mensagem.
- [ ] Protocolo implementado nos dois lados e funcionando fim a fim.
- [ ] A escolha entre A, B e C da §5.3 feita e justificada.
- [ ] Chave nunca trafega, em nenhum momento do protocolo.
- [ ] O app nunca recebe o token — verificado no ataque 5.
- [ ] Os 7 ataques executados e documentados.
- [ ] Procedimento de revogação escrito.

---

## 8. O que NÃO fazer

- Não invente algoritmo de criptografia. Use HMAC-SHA256 da biblioteca.
- Não deixe o app pedir o token, nem "temporariamente para testar". Vira permanente.
- Não coloque a mesma chave em todas as etiquetas. Uma aberta abriria a loja inteira.
- Não trate o ataque de força bruta (alicate) — está fora de escopo e é do pórtico.
- Não mexa no mecanismo físico (parte 03) nem no app (parte 02). Você entrega o "pode abrir";
  a parte 03 obedece.
- Não afirme que o sistema é seguro sem ter tentado quebrá-lo. Afirmação sem ensaio é opinião.
