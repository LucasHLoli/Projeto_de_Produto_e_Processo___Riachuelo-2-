# MVP Tag&Go: trava pronta + ESP32 + servidor

Versão de 29/09/2026. Demo em 07/12/2026. Preços no pix, consultados em 29/09/2026.

## 1. O MVP em 5 linhas

1. **O que é:** uma caixa (tamanho livre) com uma **fechadura de armário "bico de papagaio" pronta** (SARY 12 V), um ESP32, um relé, um semáforo de LEDs e power bank.
2. **Como trava:** o gancho de aço vai preso numa tampa impressa em 3D, atravessa a roupa por um ilhós ou casa de botão e é **empurrado** na fenda da caixa. A fechadura prende sozinha, sem energia. O sensor da própria fechadura avisa "travada" e o LED fica vermelho.
3. **Como libera:** o cliente lê o QR, paga (simulado) e o servidor manda liberar. O ESP32 dá um pulso de 200 ms no relé, a mola ejeta o gancho e o LED fica verde.
4. **Como reutiliza:** o funcionário empurra o gancho na próxima peça (trava), abre a página da etiqueta no celular e escolhe o produto. O servidor só aceita o recadastro se o sensor disser "travada".
5. **Onde roda o software:** servidor Python (FastAPI + SQLite) na Railway, um container na nuvem que faz o papel da "máquina virtual", com painel de todos os dados. Plano B: o mesmo código no notebook.

## 2. Desenho em blocos

```
[Celular do cliente] --QR--> https://tagandgo.up.railway.app/t/TAG-01
        |                                  |
        |  paga (simulado)                 v
        +--------------------> [SERVIDOR: FastAPI + SQLite + painel]
                                           ^
                                           |  HTTPS, o ESP32 pergunta a cada 1 s ("tem comando?")
                                           |
[Power bank B ou notebook] --USB 5V--> [ESP32] --GPIO26--> [RELÉ 3,3 V] --12 V, 200 ms--> [FECHADURA SARY]
                                        |  ^                    ^                              |
                                        |  +---- GPIO27 <-------|------ sensor "travada" ------+
                                        +--> [SEMÁFORO LED]     |
[Power bank A (USB-C PD)] --> [GATILHO PD 12 V] ----------------+
```

## 3. Lista de compras

| # | Item | Para que serve | Qtd | Preço (pix) | Loja / link | Riachuelo empresta? | Conferido em 29/09 |
|---|---|---|---|---|---|---|---|
| 1 | Fechadura 12 V SARY 50 mm com detecção de abertura | A trava (empurra e trava, pulso solta, sensor) | 2 | 2 × 45,89 = 91,78 | [Usinainfo](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-sary-50mm-com-deteccao-de-abertura-8416.html) | Não | OK: 12 V, 1,4 A (bobina 9 Ω), com detecção, "últimas unidades". A página não diz quantos fios são nem, com todas as letras, que trava ao empurrar sem energia: confirmar na bancada |
| 2 | Fechadura 12 V XG07E 73 mm com detecção, corpo plástico (reserva) | Reserva, só com a fonte 12 V de tomada (4 fios) | 1 | 33,16 | [Usinainfo](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-0-8a-4-fios-com-deteccao-de-abertura-8693.html) | Não | Atenção (30/09): a página diz 0,8 A, mas também diz bobina de 6 Ω, e 12 V ÷ 6 Ω dá 2 A (a Hestore vende a mesma família como 2 A). Passa dos 1,5 A do power bank. 4 fios (sensor amarelo e azul). "Últimas unidades" |
| 3 | ESP32 DevKit V1 USB-C 30 pinos CP2102 | Cérebro com Wi-Fi (o Uno não tem Wi-Fi) | 1 | 56,81 | [Usinainfo](https://www.usinainfo.com.br/esp32/esp32-wifi-e-bluetooth-com-usb-c-30-pinos-e-cp2102-9114.html) | Não | Preço, USB-C, CP2102 e 30 pinos OK, "últimas unidades". Pinos soldados: **não verificado** (a página não diz) |
| 4 | Módulo relé 1 canal **3,3 V** com optoacoplador | Chave que liga os 12 V na fechadura | 2 | 2 × 13,59 = 27,18 | [Usinainfo](https://www.usinainfo.com.br/rele-arduino/modulo-rele-3v-10a-1-canal-com-optoacoplador-para-esp32-5997.html) | Não | OK: alimentação e sinal de 3,3 V, optoacoplador, jumper High/Low, 10 A. "Últimas unidades" |
| 5 | Semáforo LED com resistores (verm./amar./verde) | Mostra o estado | 2 | 2 × 7,78 = 15,56 | [Usinainfo](https://www.usinainfo.com.br/outros-modulos-arduino/semaforo-led-33v5v-8mm-s3-5466.html) | Não | OK: 3,3 a 5 V, resistores integrados. "Últimas unidades" |
| 6 | Diodo 1N4007 (10 un.) | Protege o ESP32 do pico da bobina | 1 | 1,89 | [Usinainfo](https://www.usinainfo.com.br/diodos/diodo-retificador-1n4007-kit-com-10-unidades--3008.html) | Não | OK: 10 un. "Últimas unidades" |
| 7 | Jumpers fêmea-fêmea 20 cm (40) | ESP32 → relé e semáforo, sem solda | 1 | 7,50 | [Eletrogate](https://www.eletrogate.com/jumpers-femea-femea-40-unidades-de-20-cm) | Não | OK, disponível |
| 8 | Jumpers macho-fêmea 20 cm (40) | Fios do sensor da fechadura → ESP32 | 1 | 8,46 | [Eletrogate](https://www.eletrogate.com/jumpers-macho-femea-40-unidades-de-20-cm) | Não | OK, disponível |
| 9 | Protoboard 400 pontos | Ponto de emenda dos fios soltos da fechadura | 1 | 8,46 | [Eletrogate](https://www.eletrogate.com/protoboard-400-pontos) | Não | OK, disponível |
| 10 | Gatilho USB-C PD fixo 12 V, 5 A (pacote com 3) | Tira 12 V do power bank PD | 1 | não visível; reservar 50,00 | [Amazon](https://www.amazon.com.br/GuiPQS-M%C3%B3dulo-gatilho-Gatilho-Chamariz/dp/B09BZTXHY8) | Não | Produto OK (12 V fixo, 5 A, 3 un.). Preço e estoque: **não verificado** (a Amazon não mostra sem navegador) |
| 11 | Power bank 20 W com **USB-C PD 12V⎓1,5A** (FAM L10018) | Alimenta a fechadura | 1 | 237,40 | [M2P Tech](https://www.m2ptech.com.br/5uxazaiz9-carregador-portatil-power-bank-10000mah-marca-fam-modelo-l10018) | Não (vejam antes se alguém da equipe já tem) | Corrigido: R$ 237,40 no pix (antes, reserva de 150). Disponível. USB-C PD 12 V/1,5 A confirmado; o SARY puxa 1,4 A, então a margem é pequena |
| | **Subtotal plano A** | | | **R$ 538,20** | | | |
| 12 | Plano B: trava solenoide FEC-91 12 V NF | Trava alternativa (seção 7) | 1 | 46,17 | [Usinainfo](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletrica-solenoide-12v-nf-compacta-fec-91-lingueta-inferior-4687.html) | Não | OK: 12 V, 0,5 A, NF, pulso de até 10 s. "Últimas unidades" |
| 13 | Plano B: cabo USB elevador 5→12 V com visor KWS-912V | 12 V a partir de qualquer power bank | 1 | 28,45 | [Usinainfo](https://www.usinainfo.com.br/regulador-de-tensao/cabo-usb-p4-com-regulador-de-tensao-5v-para-9v-ou-12v-dc-step-up-e-voltimetro-adaptador-kws-912v-15-a-2a-5487.html) | Não | OK, com ressalva: seletor 9/12 V e visor. A página diz até 1,5 A em 12 V, mas a entrada é USB 5 V com no máximo 2 A (10 W), então em 12 V sai no máximo ~0,8 A. Serve para a FEC-91 (0,5 A), mas não para o SARY (1,4 A). Plugue de saída 2,5 × 5,2 mm. "Últimas unidades" |
| 14 | ~~Plano B: P4 fêmea com borne~~ | Não comprar | 0 | 0 (era 4,66) | [Usinainfo](https://www.usinainfo.com.br/conectores-e-adaptadores/jack-p4-femea-com-borne-a-parafuso-21x55mm-2843.html) | Não | Retirado: o jack é 2,1 × 5,5 mm e o plugue do KWS-912V é 2,5 × 5,2 mm, as medidas não casam. Cortar o plugue do cabo e prender os dois fios direto nos bornes (sem solda) |
| 15 | Desacoplador + etiqueta antifurto de loja | Só para comparar lado a lado na demo | 1 | 0 (R$ 169,90 se comprar) | [referência](https://www.loja.allcard.com.br/MLB-2864877330-desacoplador-alarme-antifurto-tag-bolacha-5300-gs-_JM) | **Sim: pedir emprestado** | **Não verificado**: o site não abriu em 29/09. O R$ 169,90 aparece só no título do resultado de busca |
| | **Total com plano B** | | | **R$ 612,82 + fretes** | | | |

Riachuelo também pode emprestar: as peças de roupa da demo (com casa de botão ou ilhós) e uma arara. Se alguém já tiver power bank PD 12 V, o total cai para R$ 375,42. Hospedagem: US$ 0 no trial da Railway (criar conta em ~10/11) ou ~US$ 15 no cartão. **Comprar até 03/10**: quase todos os itens da Usinainfo estão como "últimas unidades". Concentrem num carrinho só na Usinainfo (itens 1 a 6, 12 e 13) e outro na Eletrogate (7 a 9). O preço do item 10 só aparece abrindo a página da Amazon no navegador.

## 4. Ligações (sem solda, tudo borne ou jumper)

1. Power bank A (USB-C) → gatilho PD 12 V. Saída **+12 V** → borne **COM** do relé.
2. Borne **NA** do relé → fio **+** da bobina da fechadura. Fio **−** da bobina → **−** do gatilho PD.
3. Diodo 1N4007 nos mesmos bornes: **listra no +** da bobina (borne NA), outra ponta no **−**.
4. Relé → ESP32 (fêmea-fêmea): VCC → **3V3**, GND → **GND**, IN → **GPIO26**. Jumper do relé em **High**.
5. Os 2 fios do **sensor** da fechadura → protoboard → macho-fêmea: um no **GPIO27**, outro no **GND**. (A página do SARY não diz quantos fios ele tem. Se vierem só 3, com um fio comum entre bobina e sensor, ligar também o GND do ESP32 no **−** do gatilho PD. Conferir com multímetro na bancada.)
6. Semáforo → ESP32: GND → **GND**, vermelho → **GPIO25**, amarelo → **GPIO33**, verde → **GPIO32**.
7. ESP32 → power bank B (ou notebook) pelo cabo USB. Não usem GPIO 0, 2, 12 e 15.
8. **Antes de montar a caixa:** testar na bancada que empurrar o gancho trava e que um pulso solta. Medir a lâmina do gancho antes de desenhar a tampa 3D.

## 5. Fluxos

**Cliente:** lê o QR da caixa → vê produto e preço → "Pagar (simulado)" → LED amarelo piscando (liberando) → pulso → **LED verde** → puxa a tampa com o gancho → o sensor vê "aberta" → venda concluída no painel.

**Funcionário:** empurra o gancho pela nova peça até o clique → sensor "travada" → **LED amarelo fixo** (travada, sem produto) → escaneia o QR com o celular e toca em "Sou funcionário" (senha) → escolhe o produto → Vincular → **LED vermelho** (à venda).

LEDs: vermelho = travada com produto; amarelo fixo = travada sem produto; amarelo piscando = liberando; verde = aberta/liberada; qualquer cor piscando devagar = sem servidor (**continua travada**).

## 6. Software

- **Stack:** Python 3.12 + FastAPI + SQLite (sqlite3 puro) + HTML/JS puro. Firmware na IDE Arduino 2.x (core esp32 + ArduinoJson).
- **Comunicação:** o ESP32 pergunta ao servidor a cada 1 s (HTTP polling por HTTPS). Mais simples de gerar por IA e de testar pelo navegador.
- **Onde hospedar:** Railway (deploy pelo GitHub, HTTPS e domínio fixo automáticos, SQLite num Volume em `/data`). Plano B: `uvicorn app:app --host 0.0.0.0 --port 8000` no notebook, no mesmo hotspot 2,4 GHz do ESP32.
- **Ordem:** S1 servidor + simulador local; S2 ESP32 com LED e sensor; S3 fechadura; S5 Railway; congelar em 30/11.
- Wi-Fi: hotspot de celular em **2,4 GHz** (iPhone: "Maximizar Compatibilidade"). Nunca eduroam.

### Prompt 1: servidor e páginas (colar no Claude Code)

```
Crie do zero o projeto "tagandgo-server": servidor de um MVP acadêmico (Poli-USP, parceria Riachuelo) de etiqueta antifurto REUTILIZÁVEL. Somos iniciantes: explique cada passo, rode os testes no final e não adicione nada além do pedido. Pagamento SIMULADO: nenhum dado de cartão, nenhum gateway.

STACK (não trocar)
- Python 3.12, FastAPI, Uvicorn, sqlite3 da biblioteca padrão (SEM ORM), qrcode[pil]. pytest e httpx só para testes.
- Front-end: HTML + CSS + JS puro em static/, sem React, sem build, sem CDN. Textos em português do Brasil, layout para celular.
- Variáveis de ambiente: PORT (padrão 8000), DB_PATH (padrão ./data/tagandgo.db; criar a pasta), ADMIN_USER (padrão admin), ADMIN_PASSWORD (obrigatória se DEV != "1"), PUBLIC_BASE_URL (usada nos QR), OFFLINE_APOS_S=10, COMANDO_EXPIRA_S=60, DEV ("1" liga /docs).
- Start: uvicorn app:app --host 0.0.0.0 --port $PORT. Criar tabelas e dados de exemplo na primeira execução.

ARQUIVOS
app.py, db.py, auth.py, static/cliente.html, static/cliente.js, static/painel.html, static/painel.js, static/funcionario.html, static/estilo.css, simulador_etiqueta.py, tests/test_fluxo.py, requirements.txt, railway.json (startCommand acima, healthcheckPath "/saude"), .gitignore (data/, .env, __pycache__/), README.md (rodar local; deploy na Railway com Volume em /data e as variáveis; roteiro da demo; plano B no notebook).

DOMÍNIO
- Etiqueta = caixa com ESP32 e uma fechadura de armário com sensor. Id fixo ("TAG-01", "TAG-02"). O gancho atravessa a roupa e TRAVA sozinho quando empurrado; o sensor informa travada=1/0. Um pulso de relé solta o gancho. O ESP32 fala SÓ por HTTP polling: ele chama o servidor, o servidor nunca chama o ESP32.
- Estados: ABERTA (gancho fora), TRAVADA (gancho preso; "à venda" se houver vínculo, "sem produto" se não), LIBERANDO (comando enviado), LIBERADA (pulso dado, cliente pode tirar), ALERTA (gancho saiu sem liberação). Online = poll nos últimos OFFLINE_APOS_S s.
- Vínculo = qual produto está em qual etiqueta. Recadastrar = encerrar o vínculo atual e criar outro.

ESQUEMA SQLite (PRAGMA foreign_keys=ON; datas UTC ISO 8601)
produtos(id INTEGER PK AUTOINCREMENT, sku TEXT UNIQUE NOT NULL, nome TEXT NOT NULL, preco_centavos INTEGER NOT NULL CHECK>0, tamanho TEXT, cor TEXT, foto_url TEXT, status TEXT NOT NULL DEFAULT 'DISPONIVEL' CHECK IN ('DISPONIVEL','VENDIDO'), criado_em TEXT NOT NULL)
etiquetas(id TEXT PK, token TEXT NOT NULL, estado TEXT NOT NULL DEFAULT 'ABERTA' CHECK IN ('ABERTA','TRAVADA','LIBERANDO','LIBERADA','ALERTA'), travada INTEGER NOT NULL DEFAULT 0, visto_em TEXT, rssi INTEGER, ip TEXT, fw TEXT, criado_em TEXT NOT NULL)
vinculos(id INTEGER PK AUTOINCREMENT, etiqueta_id TEXT NOT NULL FK, produto_id INTEGER NOT NULL FK, inicio_em TEXT NOT NULL, fim_em TEXT, motivo_fim TEXT CHECK IN ('VENDIDO','TROCA','DESVINCULADO'), feito_por TEXT) + UNIQUE INDEX parcial em (etiqueta_id) WHERE fim_em IS NULL e outro em (produto_id) WHERE fim_em IS NULL
compras(id TEXT PK uuid4, etiqueta_id TEXT NOT NULL, produto_id INTEGER NOT NULL, vinculo_id INTEGER NOT NULL, valor_centavos INTEGER NOT NULL, status TEXT NOT NULL CHECK IN ('PAGA','LIBERADA','FALHOU'), criada_em TEXT NOT NULL, paga_em TEXT, liberada_em TEXT, retirado_em TEXT)
comandos(id INTEGER PK AUTOINCREMENT, etiqueta_id TEXT NOT NULL, tipo TEXT NOT NULL CHECK IN ('LIBERAR'), nonce TEXT UNIQUE NOT NULL, compra_id TEXT, origem TEXT NOT NULL CHECK IN ('COMPRA','MANUAL'), status TEXT NOT NULL CHECK IN ('PENDENTE','ENTREGUE','CONCLUIDO','FALHOU','EXPIRADO'), criado_em TEXT NOT NULL, expira_em TEXT NOT NULL, entregue_em TEXT, concluido_em TEXT)
eventos(id INTEGER PK AUTOINCREMENT, etiqueta_id TEXT, tipo TEXT NOT NULL, detalhe TEXT, criado_em TEXT NOT NULL)

ROTAS
Público:
- GET /t/{id} -> página do cliente
- GET /api/publico/etiquetas/{id} -> {etiqueta_id, estado, online, produto:{nome,tamanho,cor,foto_url,preco_centavos}|null, vinculo_id, pode_comprar, motivo}
- POST /api/publico/etiquetas/{id}/checkout body {vinculo_id} -> {compra_id}
- GET /api/publico/compras/{compra_id} -> {status, estado_etiqueta}
- GET /saude -> {"ok": true}
Dispositivo (header Authorization: Bearer <token>; achar a etiqueta pelo token com hmac.compare_digest; 401 se inválido):
- GET /api/dispositivo/poll?estado=&travada=0|1&rssi=&fw= -> {"vinculada": bool, "comando": null | {"id": int, "tipo": "LIBERAR", "nonce": str, "expira_em_s": int}}
- POST /api/dispositivo/eventos body {tipo: "BOOT"|"TRAVOU"|"ABRIU", estado}
- POST /api/dispositivo/ack body {comando_id, nonce, ok: bool, estado, detalhe}
Funcionário (HTTP Basic ADMIN_USER/ADMIN_PASSWORD):
- GET /painel ; GET /api/admin/resumo (etiquetas com online, "visto há X s", RSSI, produto; produtos; últimas 50 compras; últimos 100 eventos; indicadores)
- GET /f/{id} -> página de recadastro para celular (funcionario.html), aberta pelo link "Sou funcionário" da página do cliente
- GET/POST /api/admin/produtos ; PUT /api/admin/produtos/{id}
- POST /api/admin/etiquetas {id} -> cria com token = secrets.token_hex(16) e devolve ; POST /api/admin/etiquetas/{id}/novo-token
- POST /api/admin/etiquetas/{id}/vincular {produto_id} ; POST /api/admin/etiquetas/{id}/desvincular
- POST /api/admin/etiquetas/{id}/liberar (comando MANUAL, sem compra)
- GET /api/admin/etiquetas/{id}/qr.png (QR de PUBLIC_BASE_URL + "/t/" + id)
- GET /api/admin/exportar/{tabela}.csv ; POST /api/admin/reset-demo (apaga compras, comandos, eventos e vínculos; produtos voltam a DISPONIVEL; mantém etiquetas e tokens)

REGRAS
1. Checkout só se: etiqueta TRAVADA, travada=1, online, vínculo ativo igual ao vinculo_id enviado, produto DISPONIVEL, nenhum comando PENDENTE/ENTREGUE não expirado. Senão 409 com mensagem amigável. Usar BEGIN IMMEDIATE.
2. Checkout cria compra PAGA e comando LIBERAR (nonce=secrets.token_hex(16), expira em COMANDO_EXPIRA_S, origem COMPRA); etiqueta -> LIBERANDO; registrar eventos.
3. Poll: atualiza visto_em, rssi, ip, fw, travada. Expira comandos vencidos (EXPIRADO; compra FALHOU; etiqueta volta a TRAVADA se travada=1). Devolve o comando PENDENTE/ENTREGUE mais antigo não expirado (marca ENTREGUE na 1a entrega) até o ack ou expirar.
4. Ack: exige mesma etiqueta, id e nonce iguais, status ENTREGUE, não expirado; senão 409 (nonce usado nunca vale de novo). ok=true: comando CONCLUIDO, etiqueta LIBERADA, compra LIBERADA (liberada_em), vínculo encerrado VENDIDO, produto VENDIDO. ok=false: comando e compra FALHOU, etiqueta TRAVADA (cliente pode tentar de novo).
5. Eventos: TRAVOU -> TRAVADA (de qualquer estado). ABRIU: se LIBERADA -> ABERTA e preenche retirado_em da última compra LIBERADA; se TRAVADA ou LIBERANDO -> ALERTA (possível furto, destacar em vermelho). BOOT -> só registra.
6. Vincular: SÓ se a etiqueta estiver TRAVADA e travada=1 (senão 409 "empurre o gancho até travar"); só produto DISPONIVEL e sem outra etiqueta; encerra vínculo anterior com TROCA; registrar feito_por.
7. Métricas: segundos entre paga_em e liberada_em, e entre liberada_em e retirado_em; médias no painel.
8. Horários em America/Sao_Paulo; preços em R$ no formato brasileiro.

PÁGINAS
- /t/{id}: cabeçalho "Tag&Go"; foto, nome, tamanho, cor, preço; botão grande "Pagar R$ X (simulado)". Depois: "Pagamento aprovado, liberando..." (polling 1 s); LIBERADA -> tela verde "Pronto! Puxe o gancho"; FALHOU -> "Não liberou, tente de novo ou chame um vendedor". Mensagens para sem produto, offline, vendida, ALERTA. Link discreto "Sou funcionário" -> /f/{id}. Rodapé: "Protótipo acadêmico, nenhum pagamento real".
- /f/{id} (Basic Auth): estado do sensor ao vivo; se não travada, "Empurre o gancho até o clique"; se travada, select de produtos disponíveis e botão Vincular; botões Desvincular e Liberar manual.
- /painel: atualiza a cada 2 s. Cartões por etiqueta (cor do estado, online, RSSI, produto, botões Recadastrar, Desvincular, Liberar, Ver QR, Mostrar token); produtos (tabela e formulário); compras (hora, etiqueta, produto, valor, status, s até liberar, s até retirar); eventos (ALERTA em destaque); indicadores do dia (vendas, faturamento, tempo médio de liberação, recadastros); Exportar CSV; Reset demo com confirmação.

SEED: TAG-01 e TAG-02 com token aleatório (imprimir no console e mostrar no painel); 6 produtos fictícios de vestuário.

SIMULADOR: simulador_etiqueta.py --url http://localhost:8000 --token XXX imita o ESP32 (mesmo contrato; ao receber LIBERAR espera 1 s, manda ack ok=true, ignora nonce repetido). Teclas: t = travar, a = abrir, f = falhar a próxima liberação.

TESTES (pytest + TestClient, banco temporário): fluxo feliz (travar -> vincular -> checkout -> poll -> ack -> abrir); checkout bloqueado (offline, sem vínculo, vinculo_id antigo, vendido, compra em andamento); vincular com etiqueta aberta -> 409; replay de nonce -> 409; token errado -> 401; comando expirado -> compra FALHOU; recadastro com histórico; ALERTA ao abrir sem compra.

No fim, rode os testes, suba servidor e simulador juntos e me mostre o roteiro de uso do README.
```

### Prompt 2: firmware do ESP32 (colar no Claude Code)

```
Escreva o firmware da etiqueta Tag&Go para ESP32 DevKit V1 na IDE Arduino 2.x (pacote "esp32" da Espressif, placa "ESP32 Dev Module"). Somos iniciantes: código comentado em português, arquivos TagAndGo.ino + config.exemplo.h (eu copio para config.h, que fica no .gitignore). Use millis(); nenhum delay() maior que 50 ms no loop, exceto o pulso do relé. Bibliotecas: WiFi, WiFiMulti, WiFiClientSecure, HTTPClient (vêm com o core) e ArduinoJson v7.

HARDWARE
- Fechadura de armário 12 V "bico de papagaio" (SARY) com bobina acionada por MÓDULO RELÉ 3,3 V (IN no GPIO26, ativo em HIGH). O gancho trava sozinho quando empurrado; um pulso curto de 12 V solta e a mola ejeta o gancho. A BOBINA QUEIMA se ficar ligada: pulso de PULSO_MS=200, NUNCA mais que 300 ms (trave isso no código com um limite fixo), e intervalo mínimo de 10 s entre pulsos.
- Sensor da fechadura: contato seco entre GPIO27 e GND, INPUT_PULLUP. Constante SENSOR_NIVEL_TRAVADA (padrão LOW = travada), porque posso descobrir que é o contrário. Debounce de 50 ms.
- Semáforo de LEDs com resistores: vermelho GPIO25, amarelo GPIO33, verde GPIO32 (HIGH acende).

CONFIG (config.h): TAG_ID "TAG-01"; DEVICE_TOKEN "..."; FW_VERSION "1.0.0"; até 3 redes Wi-Fi para o WiFiMulti; SERVIDORES[] = {"https://SEU-APP.up.railway.app", "http://192.168.43.10:8000"} (usa o primeiro; após 5 falhas seguidas passa ao próximo, circular, e loga qual está em uso); POLL_MS 1000; PULSO_MS 200.

PROTOCOLO (contrato fixo com o servidor; não mudar nomes)
- Toda requisição: header "Authorization: Bearer DEVICE_TOKEN", timeout 3 s, JSON.
- A cada POLL_MS: GET {base}/api/dispositivo/poll?estado=<ESTADO>&travada=<0|1>&rssi=<WiFi.RSSI()>&fw=<FW_VERSION>. Resposta: {"vinculada": true|false, "comando": null} ou {"vinculada": true, "comando": {"id": 12, "tipo": "LIBERAR", "nonce": "<32 hex>", "expira_em_s": 55}}.
- POST {base}/api/dispositivo/eventos {"tipo": "BOOT"|"TRAVOU"|"ABRIU", "estado": "<ESTADO>"}. Se falhar, guardar numa fila circular de 8 e reenviar depois.
- POST {base}/api/dispositivo/ack {"comando_id": 12, "nonce": "...", "ok": true|false, "estado": "<ESTADO>", "detalhe": "..."}.
- HTTPS: WiFiClientSecure com setInsecure() (comentar: cifrado mas sem validar certificado, só para a demo); HTTPClient com setReuse(true); http.end() após qualquer erro. URL "http://" usa WiFiClient comum. HTTP 401 = erro de configuração (todos os LEDs piscando e log).

LÓGICA
- Estados: ABERTA, TRAVADA, LIBERANDO, LIBERADA, ALERTA. No boot: relé DESLIGADO antes de tudo; ler sensor (travada -> TRAVADA, senão ABERTA); mandar BOOT.
- Sensor mudou para travada -> TRAVADA + evento TRAVOU. Mudou para aberta: se LIBERADA -> ABERTA + ABRIU; senão -> ALERTA + ABRIU (vermelho piscando rápido por 10 s).
- LIBERAR recebido: se o nonce for igual ao último executado (em RAM), só reenviar o ack, sem pulso. Se expira_em_s <= 0, ignorar. Senão: LIBERANDO -> pulso de PULSO_MS no relé (respeitando o intervalo de 10 s) -> esperar 500 ms e ler o sensor: se aberta ou se o gancho saiu -> LIBERADA + ack ok=true; se ainda travada -> TRAVADA + ack ok=false, detalhe "gancho não soltou".
- LIBERADA: se em 20 s o sensor ainda estiver travada (cliente empurrou de volta), voltar a TRAVADA.
- Sem Wi-Fi ou servidor: NUNCA dar pulso sozinho; manter o estado; tentar reconectar; o LED do estado pisca a 1 Hz. 60 s sem Wi-Fi -> ESP.restart().
- LEDs: TRAVADA com vinculada=true -> vermelho fixo; TRAVADA com vinculada=false -> amarelo fixo; LIBERANDO -> amarelo piscando 4 Hz; LIBERADA ou ABERTA -> verde fixo; ALERTA -> vermelho piscando rápido.
- Serial 115200: log de cada mudança de estado, requisição e erro. Comandos pela Serial: "s" = status, "p" = pulso de teste (respeitando os limites), "r" = reiniciar.

ENTREGUE TAMBÉM: tabela de ligações (pino -> componente; diodo 1N4007 em paralelo com a bobina, listra no +; relé com COM no +12 V e NA no + da bobina); passo a passo para instalar a placa e as bibliotecas na IDE; checklist de teste: 1) só LEDs e sensor, com servidor local http://IP-do-notebook:8000; 2) com o relé e a fechadura; 3) com a Railway.
```

## 7. Plano B da trava

Se o SARY não travar ao empurrar no teste de bancada, esgotar, ou se o power bank não tiver PD 12 V:

- **B1 (mesmo tipo de fechadura):** trocar pela XG07E (item 2). Pela bobina de 6 Ω ela deve puxar cerca de 2 A, mais que o power bank A entrega, então só usar com a fonte 12 V 2 A de tomada ou se passar no teste de bancada sem o power bank desligar. Tem 4 fios (2 da bobina, 2 do sensor, amarelo e azul). Nada muda no código.
- **B2 (solenoide de lingueta):** trava FEC-91 12 V NF (itens 12 e 13), 0,5 A, alimentada pelo **cabo KWS-912V** em qualquer power bank comum (chave em 12 V, conferir no visor). Cortar o plugue P4 do cabo e prender os dois fios direto nos bornes, sem solda (o jack P4 com borne da loja é de outra medida). A lingueta chanfrada fica perpendicular ao pino; o pino é uma **lâmina impressa em PETG com uma janela** onde a lingueta encaixa. O pino entra, empurra o chanfro e trava. Para saber se travou, colar uma microchave (fim de curso) no fundo da caixa, ligada no GPIO27. No firmware: `PULSO_MS=1500`, limite 2 s (a FEC-91 aceita até 10 s). Conferir nas fotos se o chanfro está virado para o lado certo antes de comprar.
- **B3 (sem Wi-Fi ou sem ESP32):** o Arduino Uno que vocês já têm, ligado por USB ao notebook, com relé 5 V; um script Python no notebook faz a ponte com o servidor. A parte de 12 V é a mesma.
- **Última linha:** liberação manual pelo painel e vídeo de backup da demo.
