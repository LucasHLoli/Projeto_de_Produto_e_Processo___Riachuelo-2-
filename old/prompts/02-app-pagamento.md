# PARTE 02 — APP E PAGAMENTO
## Como cobrar sem caixa?

---

## 0. Papel

Você é desenvolvedor de produto digital. Sua tarefa é construir o **aplicativo do cliente** e
o **backend** que o sustenta: da leitura da etiqueta até o pagamento confirmado.

---

## 1. Contexto mínimo (autossuficiente)

O cliente pega uma peça na loja, encosta o celular na etiqueta antifurto (ou lê um QR),
confere o produto, paga, e depois destrava a etiqueta numa estação de autoatendimento. Sem
caixa, sem fila.

Sua parte cobre da leitura até o **pagamento confirmado**. O que acontece depois — emitir o
token e destravar a etiqueta — é da parte 05, e você **não** deve fazer.

---

## 2. Você recebe

De `CONTRATOS.md`:
- a URL que a etiqueta expõe: `https://tagandgo.app/i/<item_id>`;
- o formato do `item_id` (EPC-96, 24 hex);
- as rotas de API que você precisa implementar (`/i/<id>`, `/cart`, `/pay`);
- o evento de venda que você precisa gerar.

Da parte 01: confirmação de que a leitura NFC funciona, e em quais celulares. **Enquanto isso
não chega, desenvolva com QR** — o contrato diz que os dois caminhos levam à mesma URL.

---

## 3. Você entrega

1. **PWA funcionando** (aplicativo web instalável), não protótipo de tela.
2. **Backend** com as rotas do contrato, hospedado e acessível pela internet.
3. **Banco de produtos** com no mínimo 10 SKUs fictícios, com foto e preço.
4. **Pagamento em sandbox** funcionando fim a fim.
5. **Teste de usabilidade** com 5 pessoas que nunca viram o app.
6. Vídeo de 60 s do fluxo completo, para a apresentação.
7. Texto para `2-conteudo/3-proposta.tex`.

---

## 4. Restrições

- **Nunca use dinheiro real.** Use exclusivamente o ambiente *sandbox* do provedor de
  pagamento. Trabalho acadêmico com transação real cria problema de conformidade sem ganho
  nenhum de demonstração.
- **O app nunca pede o token de liberação.** Quem pede é a Estação (parte 05). Se o app
  pudesse pedir, um celular modificado emitiria autorizações sozinho. Este é o ponto de
  segurança mais importante do sistema — não o contorne por conveniência.
- **QR é o caminho obrigatório, NFC é o bônus.** Web NFC só existe no Chrome de Android; iOS
  não expõe leitura NFC para navegador. Se você depender de NFC, metade da banca não consegue
  testar no próprio celular.
- Sem instalação de app de loja. PWA aberto por link — a fricção de instalar mata a demo.

---

## 5. Método passo a passo

### 5.1 Stack sugerida (troque se souber melhor, mas justifique)

| Camada | Sugestão | Por quê |
|---|---|---|
| Front | HTML + JS puro ou React, servido como PWA | roda em qualquer celular, sem loja de apps |
| Leitura | `BarcodeDetector` / biblioteca de QR pela câmera; Web NFC onde houver | QR funciona em todo lugar |
| Backend | Firebase, Supabase ou Node em serviço gratuito | camada gratuita basta para a demo |
| Pagamento | Mercado Pago **sandbox** ou equivalente com Pix de teste | Pix é o meio que o cliente brasileiro usa |

### 5.2 Telas mínimas

1. **Abertura** — botão grande "Ler etiqueta", câmera aberta em um toque.
2. **Produto** — foto, nome, preço, tamanho, botão "Adicionar".
3. **Sacola** — lista, total, remover item.
4. **Pagamento** — Pix (QR + copia-e-cola) e cartão.
5. **Confirmação** — "Pago. Leve a peça até a Estação de Liberação." **Com instrução visual de
   onde fica a estação** — essa tela é a ponte para a parte 03 e costuma ser esquecida.
6. **Erro** — pagamento recusado, item já vendido, sem internet.

### 5.3 Sequência a implementar

```
1. cliente le etiqueta      -> app extrai <item_id> da URL
2. GET /i/<item_id>         -> backend devolve nome, preco, foto, tamanho
3. POST /cart               -> item entra na sacola
4. POST /pay                -> inicia cobranca no sandbox
5. webhook do provedor      -> backend confirma e grava o EVENTO DE VENDA (contrato, §7)
6. app mostra confirmacao   -> FIM DA SUA PARTE
```

O passo 6 é a fronteira. Da confirmação em diante, é a parte 05.

### 5.4 Casos de erro que você **precisa** tratar

| Caso | Comportamento exigido |
|---|---|
| Sem internet no provador | mensagem clara, sacola preservada localmente |
| Pagamento recusado | item continua travado, sem cobrança |
| `item_id` desconhecido | "peça não cadastrada, procure um atendente" |
| Item já vendido | bloquear — evita pagar duas vezes pela mesma peça |
| Cliente paga e vai embora sem destravar | detectar, e a parte 06 define o que fazer |

### 5.5 Teste de usabilidade

Cinco pessoas que nunca viram o app, cada uma sozinha, sem você explicar nada. Meça:

- tempo da abertura até o pagamento concluído;
- quantas travaram, e em qual tela;
- quantas encontraram a instrução da Estação de Liberação sem ajuda.

**A terceira medida é a mais importante.** Um app perfeito que não leva o cliente até a
estação não resolve o problema — ele só move a fila de lugar.

---

## 6. Perguntas que seu entregável precisa responder

1. Quanto tempo leva do "ler etiqueta" ao "pago", com usuário real?
2. Quantos dos 5 testados concluíram sem ajuda?
3. Quantos entenderam sozinhos que precisam ir à Estação?
4. O fluxo funciona em iPhone? E em Android básico?
5. Qual o custo por transação em produção (taxa do Pix, hospedagem)? `[COTAR]`

---

## 7. Critérios de aceite

- [ ] PWA abre por link, sem instalação.
- [ ] QR funciona em iPhone **e** Android.
- [ ] Pagamento em sandbox conclui e dispara webhook.
- [ ] Evento de venda gravado no formato do contrato §7.
- [ ] Todas as rotas do contrato §6 implementadas — inclusive as que a parte 05 vai consumir.
- [ ] Os 5 casos de erro da §5.4 tratados.
- [ ] Teste com 5 usuários feito e documentado.
- [ ] Zero transação com dinheiro real.

---

## 8. O que NÃO fazer

- Não implemente o `/release-token` — é da parte 05. Deixe a rota existindo e devolvendo
  `501 Not Implemented`, para não travar a integração.
- Não faça app nativo Android/iOS. Loja de apps, certificado e build são semanas perdidas
  para um trabalho de um semestre.
- Não use dinheiro real, nem "só pra testar com R$ 1".
- Não invente dado de produto sem marcar como fictício — não use catálogo real da Riachuelo
  como se o sistema estivesse em produção.
- Não trate a etiqueta física — hardware é das partes 01 e 03.
