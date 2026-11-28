# Plano de desenvolvimento do software do protótipo

Versão 0.1, de 27/11/2026. É uma proposta: nada aqui foi testado ainda. Quem precisar mudar o contrato (seção 4) muda **primeiro neste arquivo**, avisa a outra pessoa e sobe o número da versão.

Este plano substitui, só na parte de software, as arquiteturas anteriores (MQTT + GitHub Pages no relatório do MVP e FastAPI + Railway em `mvp-trava-pronta.md`). A escolha agora é **Flask rodando no notebook, com o ESP32 consultando o servidor a cada 1 s**.

## 1. O que vamos demonstrar

1. O vendedor prende a peça. A chave fim de curso avisa o ESP32, que avisa o servidor. A etiqueta fica **travada** e o LED fica vermelho.
2. O cliente aponta a **câmera normal do celular** para o QR da tampa. O celular abre `http://<ip-do-notebook>:5000/pagar/TAG-01` no navegador.
3. A página mostra o produto e o preço. O cliente escolhe Pix ou cartão e clica em **Pagar** (pagamento simulado).
4. O servidor registra o pagamento e cria um comando "liberar" para a etiqueta.
5. Na consulta seguinte (em até 1 s), o ESP32 recebe o comando, move o servo e confirma. O LED fica verde e a página mostra **"Pode retirar a peça"**.
6. O vendedor usa o painel para resetar a etiqueta para a próxima demonstração.

Meta: do clique em "Pagar" ao servo se mexer em **no máximo 3 s**.

## 2. Arquitetura

```
 Celular do cliente              Notebook (servidor)                   Etiqueta
 ┌──────────────────┐   HTTP    ┌──────────────────────────┐   HTTP   ┌──────────────────┐
 │ Navegador        │ ───────►  │ Flask  (porta 5000)      │ ◄──────  │ ESP32            │
 │ /pagar/TAG-01    │ ◄───────  │  ├─ páginas (Pessoa A)   │  ──────► │ consulta a cada  │
 └──────────────────┘           │  ├─ API JSON (Pessoa B)  │          │ 1 s: POST /sync  │
 ┌──────────────────┐           │  └─ SQLite   (Pessoa B)  │          │ servo, LED, chave│
 │ Painel (notebook)│ ◄───────► └──────────────────────────┘          └──────────────────┘
 └──────────────────┘
        Todos no mesmo Wi-Fi 2,4 GHz (roteador do celular)
```

- **Um só programa Flask** serve as páginas e a API. Como tudo vem do mesmo endereço, não há CORS para tratar.
- **O servidor é a fonte da verdade.** O ESP32 só informa o que a chave lê e executa comandos. A página só mostra o que o servidor diz.
- **O ESP32 sempre pergunta; nunca recebe conexões.** Ele não precisa ter IP conhecido.
- **Sem comando, não abre.** Se o Wi-Fi ou o servidor caírem, a etiqueta continua travada.

## 3. Quem faz o quê

### Pessoa A: aplicativo de pagamento (nome: Matheus Ono)

Entrega as páginas em HTML, CSS e JavaScript puro, sem framework e sem etapa de build. Os arquivos ficam em `servidor/templates/` e `servidor/static/`.

| Entrega                            | Detalhe                                                                                                                                              |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Página do cliente `pagar.html`  | Todo o fluxo da seção 5.1: produto, escolha do método, pagamento, espera e resultado                                                              |
| Painel do vendedor `painel.html` | Lista das etiquetas com estado e produto, botão "Resetar", troca de produto e histórico (seção 5.2)                                              |
| Visual                             | Celular primeiro (360 a 430 px de largura), com cara de app: logo, botões grandes e a faixa "Demonstração — nenhum pagamento real é processado" |
| Fotos dos produtos                 | Em `static/produtos/<sku>.jpg`, no máximo 200 KB cada                                                                                             |

Esforço estimado: **10 a 17 h** (app de 6 a 12 h, painel de 3 a 5 h).

### Pessoa B: servidor, banco de dados e ESP32 (nome: Pedro Tinoco)

| Entrega                                     | Detalhe                                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Servidor Flask `app.py`                   | Todas as rotas da seção 4, regras de estado da seção 4.5, rota do QR                    |
| Banco SQLite `db.py`                      | Tabelas da seção 6, com produtos e etiquetas de exemplo carregados na primeira execução |
| Simulador `simular_esp32.py`              | Script que faz o papel do ESP32 (seção 8). A Pessoa A usa para testar sem hardware        |
| Firmware `firmware/tagandgo/tagandgo.ino` | Comportamento da seção 7                                                                  |

Esforço estimado: **13 a 25 h** (servidor de 4 a 8 h, simulador de 1 h, firmware de 8 a 16 h).

### Juntas

Integração e testes da seção 10: **6 a 12 h**. O ensaio geral exige as duas pessoas presentes.

### Pastas

```
prototipo/software/
├── plano-desenvolvimento.md   ← este arquivo
├── servidor/
│   ├── app.py                 (B)
│   ├── db.py                  (B)
│   ├── config.py              (B)  IP, porta, chaves das etiquetas
│   ├── simular_esp32.py       (B)
│   ├── requirements.txt       (B)  flask, qrcode[pil]
│   ├── templates/             (A)  pagar.html, painel.html
│   └── static/                (A)  css, js, imagens
└── firmware/
    └── tagandgo/tagandgo.ino  (B)
```

Cada pessoa só edita os próprios arquivos. A única exceção é a rota que entrega cada página: ela fica no `app.py` (B) e só chama `render_template` (seção 4.1).

## 4. Contrato entre as partes

### 4.1 Regras gerais

| Regra                     | Valor                                                                                                        |
| ------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Endereço                 | `http://<ip-do-notebook>:5000`. Sem HTTPS                                                                  |
| Formato                   | JSON em UTF-8, com cabeçalho `Content-Type: application/json` em pedidos e respostas                      |
| Nomes de campos           | `snake_case`, sem acentos (`preco_centavos`, não `preço`)                                            |
| Valores de estado         | Minúsculos e sem acento: `livre`, `travada`, `paga`, `liberada`                                     |
| Dinheiro                  | **Inteiro em centavos** (`12990` = R$ 129,90). Nunca número com vírgula. Quem formata é a página |
| Data e hora               | Texto ISO 8601 com fuso: `"2026-11-27T14:03:22-03:00"`                                                     |
| Identificador da etiqueta | `tag_id`: `TAG-` + dois dígitos, maiúsculo (`TAG-01`)                                                |
| Identificador do produto  | `sku`: texto curto, maiúsculo (`CAM-001`)                                                               |
| Erros                     | Código HTTP + corpo `{"erro": "codigo_curto", "mensagem": "Texto para mostrar ao usuário"}`              |

Rotas de página (HTML), que ficam no `app.py`:

| Rota                    | Devolve                                                | Dono do conteúdo |
| ----------------------- | ------------------------------------------------------ | ----------------- |
| `GET /pagar/<tag_id>` | `render_template("pagar.html", tag_id=tag_id)`       | A                 |
| `GET /painel`         | `render_template("painel.html")`                     | A                 |
| `GET /`               | Redireciona para `/painel`                           | B                 |
| `GET /qr/<tag_id>`    | Imagem PNG do QR com `URL_BASE + "/pagar/" + tag_id` | B                 |

### 4.2 Objetos

**Produto**

```json
{
  "sku": "CAM-001",
  "nome": "Camisa de linho manga curta",
  "preco_centavos": 12990,
  "tamanho": "M",
  "cor": "Azul",
  "imagem_url": "/static/produtos/CAM-001.jpg"
}
```

**Etiqueta**

```json
{
  "tag_id": "TAG-01",
  "estado": "travada",
  "online": true,
  "pino_presente": true,
  "ultimo_contato": "2026-11-27T14:03:22-03:00",
  "produto": { "...": "objeto Produto, ou null se não houver produto associado" }
}
```

- `online` é calculado pelo servidor: `true` se o último contato do ESP32 foi há **5 s ou menos**.
- `ultimo_contato` é `null` se o ESP32 nunca se conectou.

### 4.3 Rotas usadas pela página e pelo painel (Pessoa A consome, Pessoa B implementa)

| Método e rota                               | Corpo enviado                                     | Resposta de sucesso                                    | Erros                                                                                                                                      |
| -------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `GET /api/etiquetas/<tag_id>`              | —                                                | `200` + Etiqueta                                     | `404 etiqueta_nao_encontrada`                                                                                                            |
| `POST /api/etiquetas/<tag_id>/pagamentos`  | `{"metodo": "pix"}` ou `{"metodo": "cartao"}` | `201` + Pagamento (abaixo)                           | `400 metodo_invalido`, `404 etiqueta_nao_encontrada`, `409 etiqueta_offline`, `409 sem_peca`, `409 sem_produto`, `409 ja_paga` |
| `GET /api/etiquetas`                       | —                                                | `200` + lista de Etiquetas                           | —                                                                                                                                         |
| `POST /api/etiquetas/<tag_id>/resetar`     | `{}`                                            | `200` + Etiqueta                                     | `404 etiqueta_nao_encontrada`                                                                                                            |
| `PUT /api/etiquetas/<tag_id>/produto`      | `{"sku": "CAM-002"}`                            | `200` + Etiqueta                                     | `404 etiqueta_nao_encontrada`, `404 produto_nao_encontrado`, `409 etiqueta_em_uso` (estado `paga`)                                 |
| `GET /api/produtos`                        | —                                                | `200` + lista de Produtos                            | —                                                                                                                                         |
| `GET /api/eventos?tag_id=TAG-01&limite=50` | —                                                | `200` + lista de Eventos, do mais novo ao mais velho | —                                                                                                                                         |

**Pagamento** (resposta do `POST .../pagamentos`)

```json
{
  "pagamento_id": 15,
  "tag_id": "TAG-01",
  "metodo": "pix",
  "valor_centavos": 12990,
  "criado_em": "2026-11-27T14:05:10-03:00",
  "estado_etiqueta": "paga"
}
```

O pagamento só é aceito com a etiqueta no estado `travada` e `online: true`. Caso contrário, o servidor responde com o erro `409` correspondente e **não cria** pagamento nem comando. As condições são verificadas nesta ordem, e vale o primeiro erro encontrado:

| Situação                         | Erro                 |
| ---------------------------------- | -------------------- |
| ESP32 sem contato há mais de 5 s  | `etiqueta_offline` |
| Estado `livre` (sem peça presa) | `sem_peca`         |
| Etiqueta sem produto associado     | `sem_produto`      |
| Estado `paga` ou `liberada`    | `ja_paga`          |

**Evento**

```json
{
  "id": 42,
  "tag_id": "TAG-01",
  "tipo": "pagamento",
  "detalhe": "pix, R$ 129,90",
  "criado_em": "2026-11-27T14:05:10-03:00"
}
```

Tipos de evento: `pino_inserido`, `pino_removido`, `pagamento`, `comando_enviado`, `liberada`, `remocao_sem_pagamento`, `reset`, `produto_trocado`.

### 4.4 Rota usada pelo ESP32 (Pessoa B nos dois lados)

Uma única rota faz tudo: o ESP32 informa o que vê e recebe o que fazer.

`POST /api/esp/<tag_id>/sync`, com o cabeçalho `X-Tag-Key: <chave da etiqueta>` (definida em `config.py` e no firmware).

Pedido:

```json
{
  "pino_presente": true,
  "ultimo_comando_executado": 6,
  "rssi": -58,
  "uptime_s": 312
}
```

- `ultimo_comando_executado`: id do último comando que o ESP32 terminou de executar, ou `null` se ainda não executou nenhum desde que ligou. Vai em **todas** as consultas.
- `rssi` (força do sinal Wi-Fi) e `uptime_s` (segundos desde que ligou) servem só para o painel e para achar problemas.

Resposta `200`:

```json
{ "estado": "paga", "comando": { "id": 7, "acao": "liberar" } }
```

ou, sem nada a fazer:

```json
{ "estado": "travada", "comando": null }
```

Erros: `401 chave_invalida`, `404 etiqueta_nao_encontrada`.

A única `acao` por enquanto é `"liberar"`. O ESP32 deve ignorar ações que não conhece.

### 4.5 Estados da etiqueta e quem muda cada um

```
            pino entra                   pagamento aceito
   livre ──────────────► travada ───────────────────────► paga
     ▲                     │                                │
     │   pino sai          │                                │ ESP32 confirma
     └─────────────────────┘                                ▼  o comando
     ▲                                                   liberada
     └──────────────────── pino sai ───────────────────────┘
```

| De           | Para                     | O que provoca                                                                                                        | Evento                             |
| ------------ | ------------------------ | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `livre`    | `travada`              | `sync` com `pino_presente: true`                                                                                 | `pino_inserido`                  |
| `travada`  | `paga`                 | `POST .../pagamentos` aceito. Cria um comando `liberar` pendente                                                 | `pagamento`, `comando_enviado` |
| `paga`     | `liberada`             | `sync` com `ultimo_comando_executado` igual ao id do comando pendente                                            | `liberada`                       |
| `liberada` | `livre`                | `sync` com `pino_presente: false`                                                                                | `pino_removido`                  |
| `travada`  | `livre`                | `sync` com `pino_presente: false` **sem pagamento**                                                        | `remocao_sem_pagamento`          |
| qualquer     | `travada` ou `livre` | `POST .../resetar`. Cancela comandos pendentes. Vai para `travada` se o pino estiver presente; senão, `livre` | `reset`                          |

Regras de robustez:

- **O servidor reenvia o comando pendente em toda consulta** até receber a confirmação. Se a resposta se perder, o ESP32 recebe de novo.
- **O ESP32 não repete um comando que já executou**: compara o id recebido com o `ultimo_comando_executado`. Se o ESP32 reiniciar e executar duas vezes, não há problema, porque liberar duas vezes não faz mal.
- **Confirmações repetidas são ignoradas** pelo servidor.
- Se o pino sair com o estado `paga` (antes do servo agir), o servidor vai para `livre` e registra `pino_removido`.

## 5. Requisitos do app (Pessoa A)

### 5.1 Página do cliente `/pagar/<tag_id>`

O `tag_id` chega na página pela variável do template (`{{ tag_id }}`).

| Tela                   | Quando aparece                                                 | O que mostra                                                                                                                                   |
| ---------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Carregando             | Enquanto o primeiro `GET /api/etiquetas/<tag_id>` não volta | Indicador de carregamento                                                                                                                      |
| Produto                | `estado: "travada"` e `online: true`                       | Foto, nome, tamanho, cor, preço e o botão **Pagar**                                                                                    |
| Etiqueta offline       | `online: false`                                              | "Etiqueta sem conexão. Procure um atendente." Botão de pagar desabilitado                                                                    |
| Sem peça              | `estado: "livre"`                                            | "Esta etiqueta não está presa a nenhuma peça."                                                                                              |
| Já paga               | `estado: "paga"` ou `"liberada"` ao abrir                  | "Esta peça já foi paga."                                                                                                                     |
| Escolher método       | Depois de clicar em Pagar                                      | **Pix:** QR ilustrativo e botão "Simular confirmação do Pix". **Cartão:** número de teste já preenchido e botão "Confirmar" |
| Processando            | Logo após confirmar                                           | Botão desabilitado (evita pagar duas vezes) enquanto o `POST` não volta                                                                    |
| Aguardando liberação | `POST` respondeu `201`                                     | "Pagamento aprovado. Liberando a etiqueta…" e consulta `GET /api/etiquetas/<tag_id>` **a cada 1 s**                                   |
| Sucesso                | `estado: "liberada"`                                         | "Pode retirar a peça" e o comprovante (produto, valor, método, hora)                                                                         |
| Demorou                | Mais de **15 s** sem `liberada`                        | "O pagamento foi aprovado, mas a etiqueta não respondeu. Procure um atendente."                                                               |
| Erro                   | Resposta com erro ou falha de rede                             | O texto de `mensagem` do erro e um botão "Tentar de novo"                                                                                   |

Requisitos:

- Preço formatado a partir de centavos: `(c / 100).toLocaleString("pt-BR", {style: "currency", currency: "BRL"})`.
- A página **nunca decide o estado sozinha**: sempre mostra o que o servidor respondeu.
- Chamadas com `fetch` para caminhos relativos (`/api/...`), nunca com IP escrito no código.
- Sem bibliotecas de CDN: tudo o que a página usa fica em `static/`, porque o hotspot pode estar sem internet.
- Testar no Chrome (Android) e no Safari (iPhone).

### 5.2 Painel do vendedor `/painel`

- Tabela com todas as etiquetas (`GET /api/etiquetas`), atualizada a cada 2 s: `tag_id`, estado (com cor igual à do LED), online/offline, produto, preço e último contato.
- Botão **Resetar** por etiqueta (`POST .../resetar`).
- Seletor de produto por etiqueta (`GET /api/produtos` + `PUT .../produto`).
- Histórico dos últimos eventos (`GET /api/eventos`).
- Link para `/qr/<tag_id>`, para imprimir o QR.
- Roda no notebook; não precisa ser bonito no celular.

## 6. Requisitos do servidor e do banco (Pessoa B)

- Python 3.11 ou mais novo, Flask 3, `sqlite3` da biblioteca padrão e `qrcode[pil]` para o QR.
- Rodar com `python app.py`, que chama `app.run(host="0.0.0.0", port=5000, threaded=True)`. O `0.0.0.0` é obrigatório para o celular e o ESP32 alcançarem o notebook.
- `python app.py --reset` apaga o banco e recarrega os dados de exemplo.
- `config.py` concentra o que muda de um lugar para outro:

```python
URL_BASE = "http://192.168.43.10:5000"   # IP do notebook no hotspot (ver seção 9)
LIMITE_ONLINE_S = 5
CHAVES_ETIQUETAS = {"TAG-01": "troque-esta-chave"}
```

Tabelas:

| Tabela         | Colunas                                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `produtos`   | `sku` (chave), `nome`, `preco_centavos`, `tamanho`, `cor`, `imagem_url`                                    |
| `etiquetas`  | `tag_id` (chave), `sku` (pode ser nulo), `estado`, `pino_presente`, `ultimo_contato`, `rssi`, `uptime_s` |
| `pagamentos` | `id`, `tag_id`, `sku`, `metodo`, `valor_centavos`, `criado_em`                                             |
| `comandos`   | `id`, `tag_id`, `acao`, `status` (`pendente`, `executado`, `cancelado`), `criado_em`, `executado_em` |
| `eventos`    | `id`, `tag_id`, `tipo`, `detalhe`, `criado_em`                                                               |

Dados de exemplo: 3 produtos e a etiqueta `TAG-01` já associada ao primeiro.

- O valor do pagamento é copiado do produto **no momento do pagamento** (se o preço mudar depois, o comprovante não muda).
- Todas as mudanças de estado passam por uma única função, que aplica a tabela da seção 4.5 e grava o evento. Isso evita regras espalhadas pelo código.

## 7. Requisitos do firmware do ESP32 (Pessoa B)

Bibliotecas: `WiFi.h` e `HTTPClient.h` (já vêm no pacote do ESP32), `ArduinoJson` (versão 7) e `ESP32Servo`, as duas pelo Gerenciador de Bibliotecas da Arduino IDE.

Bloco de configuração no topo do arquivo:

```cpp
const char* WIFI_REDE     = "NomeDoHotspot";
const char* WIFI_SENHA    = "senha";
const char* SERVIDOR_URL  = "http://192.168.43.10:5000";   // igual ao URL_BASE do config.py
const char* TAG_ID        = "TAG-01";
const char* TAG_CHAVE     = "troque-esta-chave";           // igual ao config.py
const int   INTERVALO_MS  = 1000;                           // consulta a cada 1 s
const int   TIMEOUT_MS    = 3000;                           // tempo máximo de cada requisição
```

Pinos, iguais aos do `guia-montagem.md`:

| Peça                                    | Pino                                  |
| ---------------------------------------- | ------------------------------------- |
| Servo (sinal)                            | GPIO 13                               |
| Chave fim de curso "pino presente" (OUT) | GPIO 27                               |
| Semáforo: vermelho                      | GPIO 26                               |
| Semáforo: amarelo                       | GPIO 33 (novo, o guia ainda não tem) |
| Semáforo: verde                         | GPIO 25                               |

Comportamento:

1. Ao ligar: conectar ao Wi-Fi com `WiFi.setSleep(false)` (evita que o power bank desligue por consumo baixo). Enquanto não conecta, amarelo piscando.
2. A cada 1 s: ler a chave (com 50 ms de debounce) e enviar o `sync` (seção 4.4).
3. Se a resposta trouxer `comando` com `acao: "liberar"` e `id` diferente do último executado: fazer a sequência do servo, guardar o `id` em `ultimo_comando_executado` e enviá-lo na consulta seguinte.
4. Sequência do servo: `attach` → ir para o ângulo de liberar (90°, ajustar na montagem) → esperar 2 s → voltar a 0° → esperar 400 ms → `detach`. Nunca mover o servo enquanto o Wi-Fi está conectando.
5. Se o Wi-Fi cair: `WiFi.reconnect()` e continuar tentando. **Nunca liberar sem comando.**
6. Escrever no Monitor Serial (115200) cada consulta, resposta e ação, para depuração.

LEDs:

| Situação                                            | LED                    |
| ----------------------------------------------------- | ---------------------- |
| Sem Wi-Fi ou sem resposta do servidor há mais de 3 s | Amarelo piscando       |
| `livre`                                             | Verde piscando devagar |
| `travada`                                           | Vermelho fixo          |
| `paga` (liberando)                                  | Amarelo fixo           |
| `liberada`                                          | Verde fixo             |

Antes de programar a chave: medir com o Monitor Serial se o módulo dá `HIGH` ou `LOW` com a chave apertada, e escrever isso numa constante `NIVEL_PINO_PRESENTE`.

## 8. Testar cada lado sem o outro

**A Pessoa A não precisa do ESP32.** O `simular_esp32.py` faz as mesmas consultas que o firmware:

```
python simular_esp32.py TAG-01            # pino presente, confirma comandos automaticamente
python simular_esp32.py TAG-01 --sem-pino # simula a peça retirada
```

Com o simulador desligado, a etiqueta fica offline em 5 s, o que serve para testar essa tela.

**A Pessoa B não precisa da página** para testar o servidor. No PowerShell:

```powershell
Invoke-RestMethod http://localhost:5000/api/etiquetas/TAG-01
```

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/etiquetas/TAG-01/pagamentos -ContentType "application/json" -Body '{"metodo":"pix"}'
```

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/api/etiquetas/TAG-01/resetar -ContentType "application/json" -Body '{}'
```

**Primeira entrega da Pessoa B (marco 1):** o `app.py` com todas as rotas da seção 4 já respondendo no formato certo, mesmo que com regras incompletas. A partir daí a Pessoa A trabalha contra o servidor de verdade.

## 9. Rede

| Item                | Combinado                                                                                                            |
| ------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Rede                | Roteador (hotspot) do celular de ________, em **2,4 GHz**. No iPhone, ligar "Maximizar compatibilidade"        |
| Quem entra nela     | Notebook, ESP32 e o celular do cliente. Testar também se o próprio celular do hotspot abre a página               |
| Firewall do Windows | Na primeira vez que o Python rodar, permitir acesso em **rede privada**. Marcar a rede do hotspot como privada |
| IP do notebook      | `ipconfig`, linha "Endereço IPv4" do adaptador Wi-Fi                                                              |

**Risco principal:** o IP do notebook pode mudar quando o hotspot é religado (o Android recente sorteia a faixa de IPs). Quando mudar, é preciso atualizar três coisas: `URL_BASE` no `config.py`, `SERVIDOR_URL` no firmware (gravar de novo) e o QR impresso (pegar o novo em `/qr/TAG-01`). Por isso:

- No dia da apresentação, ligar o hotspot, conferir o IP e **só então** gravar o ESP32 e imprimir o QR.
- Ter um QR reserva aberto na tela do notebook, em `/qr/TAG-01`.
- O QR impresso na tampa precisa ter de 25 a 30 mm com margem branca.

## 10. Marcos e testes de integração

| Marco                     | Data        | Pronto quando                                                                                                                                                                                               |
| ------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M0. Contrato fechado      | __/__ | As duas pessoas leram este arquivo e concordaram com a seção 4                                                                                                                                            |
| M1. Esqueleto do servidor | __/__ | Todas as rotas da seção 4 respondem no formato certo; `simular_esp32.py` funciona                                                                                                                       |
| M2. Cada lado sozinho     | __/__ | **A:** fluxo completo no celular contra o servidor real com o simulador. **B:** ESP32 na bancada (protoboard) troca LED com a chave e move o servo quando um pagamento é feito pelo PowerShell |
| M3. Integração          | __/__ | Celular paga e o servo do ESP32 real se mexe em até 3 s                                                                                                                                                    |
| M4. Ensaio geral          | __/__ | Testes abaixo passando com a caixa montada, no power bank e no hotspot do dia                                                                                                                               |

Testes de integração (M3 e M4):

| #  | Teste                                                 | Resultado esperado                                                          |
| -- | ----------------------------------------------------- | --------------------------------------------------------------------------- |
| 1  | Ler o QR com a câmera do celular                     | Abre a página do produto certo                                             |
| 2  | Pagar com Pix e com cartão                           | Servo se mexe em até 3 s; página mostra "Pode retirar a peça"; LED verde |
| 3  | Clicar em Pagar duas vezes rápido                    | Só um pagamento registrado no painel                                       |
| 4  | Abrir a página de novo depois de pagar               | Mostra "Esta peça já foi paga"                                            |
| 5  | Desligar o ESP32 e tentar pagar                       | Página mostra offline em até 5 s e não deixa pagar                       |
| 6  | Reiniciar o ESP32 logo depois do pagamento            | Ao voltar, ele libera (comando reenviado)                                   |
| 7  | Tirar o pino sem pagar                                | Painel registra `remocao_sem_pagamento`                                   |
| 8  | Resetar pelo painel e repetir                         | Etiqueta volta a `travada` e o fluxo funciona de novo                     |
| 9  | 10 ciclos seguidos (prender, pagar, liberar, resetar) | Nenhuma falha e nenhum reinício do ESP32                                   |
| 10 | Deixar tudo ligado 10 min sem usar                    | Power bank não desliga; etiqueta continua online                           |

## 11. Fora do escopo

Pagamento real (Pix ou cartão de verdade), login de usuário, servidor na nuvem e várias lojas. No relatório, isso entra como o caminho para o produto real.

## 12. Opcionais, se sobrar tempo

| Opcional                                                            | Dono | Esforço | Observação                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------- | ---- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Leitor de QR dentro do app** (botão "Escanear" na página) | A    | 4 a 6 h  | Usar a biblioteca `html5-qrcode`. O QR lido contém a URL `/pagar/<tag_id>`; o app extrai o `tag_id` e abre a página. **Exige HTTPS**, porque o navegador só libera a câmera em páginas seguras: seria preciso um túnel como o ngrok, que depende de internet no hotspot. Por isso fica fora do fluxo principal, que usa a câmera nativa do celular |
| Alarme de remoção sem pagamento                                   | B    | 1 a 2 h  | LED vermelho piscando rápido e alerta no painel                                                                                                                                                                                                                                                                                                                      |
| QR Pix ilustrativo mais realista                                    | A    | 1 h      | Imagem com o valor da compra                                                                                                                                                                                                                                                                                                                                          |
| Mais de uma etiqueta                                                | B    | 1 h      | Já previsto no contrato: basta cadastrar `TAG-02` e gravar outro ESP32                                                                                                                                                                                                                                                                                             |
| Tabela de estoque                                                   | B (A mostra) | 2 a 3 h | Seção 12.1 |
| Histórico de leituras e sugestão de produtos                        | B (A mostra) | 4 a 8 h | Seção 12.2. Depende do estoque, para não sugerir o que acabou |

### 12.1 Estoque (opcional)

Nova tabela e duas colunas novas em `produtos`. Nada muda nas rotas que já existem.

| Tabela | Colunas |
|---|---|
| `estoque` | `sku` (chave, ligado a `produtos`), `quantidade` (inteiro, nunca negativo), `atualizado_em` |
| `produtos` (colunas novas) | `modelo` (agrupa tamanhos e cores da mesma peça, ex.: `CAM-LINHO`), `categoria` (ex.: `camisa`, `calca`, `acessorio`) |

Regras:
- Um pagamento aceito tira 1 do estoque do `sku`, na mesma operação que grava o pagamento.
- O estoque não bloqueia o pagamento: a peça já está na mão do cliente.
- Dados de exemplo: de 8 a 15 produtos, em 3 ou 4 modelos, com tamanhos e cores diferentes, e alguns com estoque zero.

Rotas novas:

| Método e rota | Corpo enviado | Resposta de sucesso | Erros |
|---|---|---|---|
| `GET /api/estoque` | — | `200` + lista de `{"sku": "CAM-001", "quantidade": 4, "atualizado_em": "..."}` | — |
| `PUT /api/estoque/<sku>` | `{"quantidade": 10}` | `200` + o item atualizado | `404 produto_nao_encontrado`, `400 quantidade_invalida` |

No objeto Produto passam a vir também `modelo`, `categoria` e `quantidade_estoque`. Na página do cliente, a Pessoa A pode mostrar "Outros tamanhos disponíveis" (mesmo `modelo`, estoque maior que zero); no painel, uma aba de estoque editável.

### 12.2 Histórico de leituras e sugestão (opcional)

**Como identificar o cliente sem login:** na primeira visita, a página gera um identificador aleatório (`crypto.randomUUID()`) e o guarda no `localStorage` do celular. É anônimo: não há nome, e-mail ou telefone. Se a pessoa limpar o navegador, vira um "cliente novo". No relatório, citar que no produto real isso exigiria consentimento (LGPD).

**Nova tabela:**

| Tabela | Colunas |
|---|---|
| `leituras` | `id`, `cliente_id`, `tag_id`, `sku` (copiado da etiqueta no momento da leitura), `pagou` (0 ou 1), `criado_em` |

**Rotas novas:**

| Método e rota | Corpo enviado | Resposta de sucesso | Erros |
|---|---|---|---|
| `POST /api/leituras` | `{"cliente_id": "8f3c…", "tag_id": "TAG-01"}` | `201` + `{"leitura_id": 31}` | `404 etiqueta_nao_encontrada`, `400 cliente_id_invalido` |
| `GET /api/sugestoes?sku=CAM-001&cliente_id=8f3c…&limite=3` | — | `200` + lista de Produtos, cada um com o campo extra `motivo` | `404 produto_nao_encontrado` |

- A página chama `POST /api/leituras` **uma vez** ao abrir, antes de mostrar o produto. Falha nessa chamada não pode travar a página.
- O `POST .../pagamentos` passa a aceitar `cliente_id` (opcional) no corpo. Com ele, o servidor marca `pagou = 1` na última leitura desse cliente naquela etiqueta.
- `motivo` é um texto curto para mostrar: `"Outros clientes também olharam"`, `"Mesmo modelo, outro tamanho"` ou `"Combina com camisas"`.

**Algoritmo (simples e explicável na apresentação):**

1. **Co-leitura:** entre os clientes que leram o `sku` atual, contar quais outros `sku` eles também leram. Compras pesam 3; leituras sem compra pesam 1.
2. **Mesmo modelo:** se houver poucos resultados, completar com o mesmo `modelo` em outro tamanho ou cor.
3. **Mesma categoria ou categoria complementar:** se ainda faltar, completar com produtos de uma tabela fixa de combinações (ex.: camisa → calça, calça → cinto).
4. **Filtros:** tirar o próprio `sku`, os que o cliente já comprou e os com estoque zero.
5. Ordenar pela pontuação e devolver os `limite` primeiros.

Como a demonstração começa sem histórico, carregar no banco de exemplo umas 50 leituras falsas de 10 clientes fictícios, para a sugestão ter o que mostrar. Na página, a Pessoa A mostra as sugestões abaixo do produto e na tela de sucesso ("Você também pode gostar").
