# CONTRATOS — interfaces entre as partes
## Leia isto antes de qualquer prompt

Este arquivo define **o que atravessa a fronteira entre as partes**. Enquanto cada dupla
respeitar o que está aqui, pode trabalhar sozinha sem falar com as outras.

**Regra:** se você precisar mudar algo deste arquivo, avise o time inteiro. Nada aqui é
decisão de uma dupla só.

---

## 1. Identificadores

| Nome | Formato | Exemplo | Quem gera |
|---|---|---|---|
| `item_id` | EPC-96, 24 caracteres hexadecimais | `3034F4D2AC1E4A0000000001` | backend, no cadastro do produto |
| `tag_id` | 8 hex, serial da etiqueta física | `A17F03C2` | gravado na etiqueta na fabricação |
| `sku` | código de produto da Riachuelo | `CAM-AZ-M-0042` | ERP |

Uma `tag_id` está associada a **no máximo um** `item_id` por vez. A associação é feita
quando a etiqueta é aplicada na peça e desfeita quando a etiqueta é devolvida ao ciclo.

---

## 2. O que a etiqueta expõe para o celular (parte 01 → parte 02)

**NDEF gravado no NTAG213**, um único registro do tipo URI:

```
https://tagandgo.app/i/<item_id>
```

Nada mais. Sem preço, sem nome do produto, sem `tag_id` — esses vêm do backend. A etiqueta
física é **burra e pública**: qualquer pessoa pode ler, e ler não autoriza nada.

**QR Code impresso** codifica exatamente a mesma URL. Todo caminho que funciona por NFC tem
que funcionar por QR — a parte 02 não pode assumir NFC.

---

## 3. Estados da etiqueta

```
LIVRE  --aplicada na peca-->  TRAVADA  --pagamento ok-->  AUTORIZADA
                                 ^                             |
                                 |                             v
                                 +----- devolvida ------  DESTRAVADA
```

| Estado | Significado | Quem muda |
|---|---|---|
| `LIVRE` | sem peça associada, no estoque de etiquetas | operação |
| `TRAVADA` | presa numa peça, pino cravado | operação |
| `AUTORIZADA` | pagamento confirmado, token válido emitido | backend (parte 05) |
| `DESTRAVADA` | pino solto, aguardando devolução | estação (parte 03) |

O estado **oficial** vive no backend. A etiqueta física não guarda estado entre acionamentos
(ela fica sem energia). Isso é intencional.

---

## 4. Token de liberação (parte 05 → parte 03)

Emitido pelo backend após confirmação de pagamento. JSON, transportado da estação para a
etiqueta:

```json
{
  "tag_id":  "A17F03C2",
  "item_id": "3034F4D2AC1E4A0000000001",
  "nonce":   "9F2C7A10",
  "exp":     1757433600,
  "hmac":    "<HMAC-SHA256 dos campos acima, chave da tag_id>"
}
```

Regras inegociáveis:

- **uso único** — o `nonce` nunca se repete para a mesma `tag_id`;
- **validade curta** — `exp` no máximo 120 s após a emissão;
- **vinculado à etiqueta específica** — token de uma `tag_id` não abre outra;
- a chave HMAC é **por etiqueta**, gravada na fabricação, nunca trafega.

> Isto é a contribuição original do projeto: a patente-base US 7.564.360 usa sinal de
> liberação **aberto**, sem autenticação. Quem escrever a parte 05 precisa saber disso.

---

## 5. Interface física etiqueta ↔ estação (parte 03 ↔ parte 05)

| Item | Especificação |
|---|---|
| Alimentação | 5 V, até 2 A, por **contatos elétricos** (pogo pins) |
| Contatos | 2 discos de latão Ø6 mm na face **superior** da etiqueta, em (±8, −8), distantes 16 mm |
| Formato da Estação | **encaixe**: a etiqueta entra com o topo para cima e os pinos descem de dentro |
| Dados | UART 115200 8N1 sobre os mesmos contatos, ou 2 contatos adicionais |
| Tempo total do ciclo | **≤ 3 s** da colocação na estação até o pino livre |
| Consumo em repouso | **zero** — a etiqueta não tem bateria |

> ### ⚠️ Correção — os contatos ficam na face SUPERIOR
>
> Uma versão anterior deste contrato dizia "face inferior". **Errado por motivo físico:** a face
> inferior é a que encosta no tecido; contato ali fica prensado contra a roupa e os pinos da
> Estação não alcançam.
>
> Consequência de projeto: a Estação deixa de ser bancada com pinos subindo e vira **encaixe**
> com pinos descendo. Isso resolve de graça o requisito da parte 06 — entrando num encaixe, a
> etiqueta destrava lá dentro e cai direto na caixa de coleta, sem depender do cliente devolver.

A etiqueta só liga quando está na estação. Fora dela, é um objeto inerte com dois adesivos
de rádio passivos colados.

---

## 6. API do backend (parte 02 ↔ parte 05 ↔ parte 04)

| Método | Rota | Quem chama | Devolve |
|---|---|---|---|
| `GET` | `/i/<item_id>` | app do cliente | nome, preço, tamanho, foto |
| `POST` | `/cart` | app | carrinho atualizado |
| `POST` | `/pay` | app | status do pagamento |
| `POST` | `/release-token` | **estação**, nunca o app | o token da §4 ou `403` |
| `POST` | `/gate/check` | pórtico | lista de `item_id` pagos nos últimos 5 min |

**Detalhe de segurança que não pode ser trocado:** quem pede o token é a **estação**, não o
celular do cliente. Se o app pudesse pedir o token, um cliente com o celular modificado
emitiria tokens sozinho.

---

## 7. Evento de venda (parte 05 → parte 04 e ERP)

```json
{
  "item_id":   "3034F4D2AC1E4A0000000001",
  "tag_id":    "A17F03C2",
  "sku":       "CAM-AZ-M-0042",
  "valor":     89.90,
  "pago_em":   "2026-09-09T14:32:07Z",
  "loja":      "RCH-SP-0142"
}
```

O pórtico (parte 04) consulta os eventos dos últimos 5 minutos para decidir se libera
silenciosamente ou alerta.

---

## 8. Números compartilhados

Estes valores aparecem em mais de uma parte. Se alguém mudar, avisa o time.

| Grandeza | Valor | Onde importa |
|---|---|---|
| Tempo máximo de destravamento | 3 s | partes 03, 05 |
| Validade do token | 120 s | partes 03, 05 |
| Janela de consulta do pórtico | 5 min | partes 04, 05 |
| Alcance mínimo de leitura UHF | 1,0 m | parte 04 |
| **Tamanho máximo do inlay UHF** | **44 × 12 mm** | partes 01, 03, 04 |
| Ciclos de reuso alvo da etiqueta | 500 | partes 03, 06 |
| Taxa de retorno alvo da etiqueta | 95% | parte 06 |
| Falso alarme aceitável no pórtico | < 1% | parte 04 |

---

## 9. Vocabulário — use estes termos, não sinônimos

| Termo | Significa |
|---|---|
| **Etiqueta** | o dispositivo antifurto rígido (não "tag", não "lacre") |
| **Garra** | o mecanismo de esferas que prende o pino |
| **Pino** | a haste de aço que atravessa o tecido (*tack*) |
| **Estação de Liberação** | o equipamento de bancada que destrava (não "caixa", não "totem") |
| **Pórtico** | o detector da saída |
| **Token** | a autorização criptográfica da §4 |

Consistência de vocabulário num relatório de 8 autores é metade da nota de redação.
