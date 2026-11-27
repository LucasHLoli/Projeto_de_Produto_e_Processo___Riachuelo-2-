# Produtos para comprar e desmontar (engenharia reversa do Tag&Go)

Levantamento de 30/09/2026. A meta era gastar até cerca de R$ 300 com a sobra do orçamento. Os preços e o estoque dos itens da Amazon.com.br foram conferidos abrindo cada página nesse dia. O item do AliExpress não abriu (a página vem vazia para acesso automatizado), então o preço dele vem da listagem de busca e está marcado como **não verificado**.

## Resumo da cesta

| # | Produto | Preço (frete) | Link | O que ensina ao Tag&Go | Status do link |
|---|---|---|---|---|---|
| 1 | Cadeado com alarme antifurto 110 dB, sensor de movimento, LK-BL16 | R$ 23,69 (frete grátis) | https://www.amazon.com.br/dp/B0CXYW1L45 | Reter (trava ao empurrar), indicar estado (sensor de travado e de vibração), energia (pilhas LR44) | Verificado em 30/09: em estoque |
| 2 | Pacote com 20 etiquetas rígidas antifurto com pino (HTG-005, AM 58 kHz) | R$ 67,78 (frete grátis, entrega de 12 a 20/10) | https://www.amazon.com.br/dp/B0GP6ZF16R | Reter e liberar: a embreagem do pino, que é o mecanismo central da etiqueta | Verificado em 30/09: **só 1 em estoque** |
| 3 | Cadeado biométrico, liga de zinco, recarregável por USB, LED de status | R$ 82,74 + R$ 11,59 de frete | https://www.amazon.com.br/dp/B0FYJ5ZBR3 | Liberar (atuador eletrônico), energia (bateria e carga USB), indicar estado (LED), reutilizar (recarga) | Verificado em 30/09: em estoque, entrega de 13 a 16/10 |
| 4 | Tag rastreador Bluetooth com acelerômetro e alto-falante (clone Find My) | R$ 19,81 (frete grátis) | https://www.amazon.com.br/dp/B0CVH4FZ6K | Comunicação (BLE), energia (CR2032 e sono profundo), indicar estado (bip) | Verificado em 30/09: **só 4 em estoque** |
| 5 | Alarme de porta e janela com sensor magnético (reed), sirene 90 dB, 3 pilhas LR44 | R$ 17,06 + R$ 15,76 de frete | https://www.amazon.com.br/dp/B0GPXWLSV5 | Indicar estado: reed com ímã como sensor de "pino travado" | Verificado em 30/09: em estoque, entrega em 02/10 |
| 6 | Trava de gaveta inteligente Tuya, Bluetooth, sem chave, com cartão | R$ 44,49 na busca, mais imposto de importação | https://pt.aliexpress.com/item/1005005664273197.html | Comunicação e liberar: o celular autoriza por BLE e a trava solta; reutilizar (cadastro de usuários e chaves) | **Não verificado**: a página do item não abriu |

**Total**

- Itens 1 a 5 (Amazon, preço e estoque conferidos, frete incluído): **R$ 238,43**.
- Com o item 6: R$ 282,92 antes do imposto. Pelo Remessa Conforme incidem 20% de imposto de importação mais ICMS (cerca de 17 a 20%), o que dá uns R$ 20 a mais. O total fica **perto de R$ 300** (estimativa). Confiram o valor final no carrinho.

## Por que cada item e o que olhar ao desmontar

### 1. Cadeado com alarme LK-BL16 (R$ 23,69)

- **Por que comprar:** é o jeito mais barato de estudar, na mesma peça, a trava "empurra e prende" e a eletrônica que percebe que está travado. Travar a haste arma o alarme, como o Tag&Go deve reconhecer que o pino entrou.
- **O que desmontar e observar:**
  - A lingueta com mola que prende a haste e o perfil do entalhe da haste.
  - Como o circuito percebe a haste inserida: microchave, contato ou lâmina.
  - O sensor de vibração, que pode ser de mola ou de esfera.
  - O driver da sirene piezo.
  - O porta-pilhas LR44 e a vedação contra chuva.
- **Funções do Tag&Go:** reter, indicar estado, energia.
- **Atenção:** o corpo é metálico e costuma ser rebitado ou prensado. Pode precisar de micro-retífica.
- **Alternativa:** cadeado com alarme 110 dB por R$ 34,10, com 12 pilhas LR44 (https://www.amazon.com.br/dp/B0G72TMP7K). Preço conferido em 30/09, em estoque.

### 2. Pacote com 20 etiquetas rígidas com pino (R$ 67,78)

- **Por que comprar:** é o benchmark direto da parte mecânica. O pino atravessa a roupa e trava só de ser empurrado, exatamente a fixação do Tag&Go. Com 20 unidades dá para abrir algumas, cortar outras ao meio e ainda fazer ensaios de arrancamento e de queda.
- **O que desmontar e observar:**
  - A embreagem de esferas ou a garra com mola que prende o pino ranhurado: por que trava ao empurrar e não solta ao puxar.
  - A força da mola que o ímã do destacador precisa vencer. É a referência para dimensionar o atuador interno do Tag&Go.
  - O perfil das ranhuras do pino.
  - O ressonador acústico-magnético de 58 kHz: tiras magnetoestritivas e ímã de polarização. Mostra quanto espaço sobra para PCB e bateria.
  - A solda ultrassônica do ABS e a espessura de parede. A peça mede 46 x 12 x 17 mm.
- **Funções do Tag&Go:** reter, liberar (o que o atuador precisa vencer).
- **Atenção:** a equipe não terá destacador. A abertura será destrutiva, com serra fina, micro-retífica ou morsa.
- **Alternativas:**
  - O mesmo modelo com 50 unidades por R$ 85,94 (https://www.amazon.com.br/dp/B0GP6V5LYJ). Conferido em 30/09, também com só 1 em estoque.
  - Mini tag RF 8,2 MHz com pino, 100 unidades, R$ 161,40 na Amazon (https://www.amazon.com.br/dp/B0G6LG83DZ). Conferido em 30/09. O mesmo produto no Magazine Luiza sai R$ 134,16 no Pix, mas não foi reverificado porque a página devolveu erro 403.

### 3. Cadeado biométrico recarregável por USB (R$ 82,74 + frete)

- **Por que comprar:** tem a mesma base eletromecânica do Tag&Go. A haste trava ao ser empurrada, a liberação é eletrônica, a bateria é recarregável por USB e o LED mostra o estado. Só muda a origem da autorização: aqui é a digital, no Tag&Go é o celular.
- **O que desmontar e observar:**
  - O atuador de liberação (micromotor com came, pino ou solenoide) e a mola de retorno.
  - Quanto tempo e quanta corrente a liberação consome (medir com multímetro).
  - A bateria LiPo, o CI carregador e a placa de proteção.
  - O LED indicador e o MCU.
  - Como detecta a haste fechada.
  - A vedação da carcaça de zinco.
- **Funções do Tag&Go:** liberar, energia, indicar estado, reutilizar (recarga).
- **Alternativa mais barata, não verificada:** cadeado de digital em ABS com carga USB no AliExpress, R$ 39,39 na busca (https://pt.aliexpress.com/item/1005010169799568.html). A carcaça plástica é mais fácil de abrir.

### 4. Tag rastreador Bluetooth, clone Find My (R$ 19,81)

- **Por que comprar:** tem praticamente o tamanho e o orçamento de energia de uma etiqueta: SoC BLE, pilha CR2032, acelerômetro e alto-falante. É a menor eletrônica BLE comercial ao alcance.
- **O que desmontar e observar:**
  - Identificar o SoC BLE pela serigrafia.
  - A antena impressa na placa e o cristal.
  - O acelerômetro, que acorda o MCU por interrupção sem ficar consultando o sensor o tempo todo (o mesmo princípio vale para o sensor de violação do Tag&Go).
  - O buzzer.
  - Medir a corrente de sono e o pico de transmissão com um resistor shunt em série com a pilha.
  - A tampa em baioneta e o fechamento da carcaça.
- **Funções do Tag&Go:** comunicação, energia, indicar estado.
- **Alternativa:** tag Find My da DigiSpace BR, R$ 39,90 (https://www.amazon.com.br/dp/B0FRB5N576). Conferida em 30/09, em estoque. Serve se o primeiro esgotar.

### 5. Alarme de porta com sensor magnético (R$ 17,06 + frete)

- **Por que comprar:** mostra a arquitetura eletrônica mínima de uma etiqueta autoalarmante: pilha de botão, reed, buzzer e chave. O par reed e ímã é um candidato barato para o sensor de "pino travado" do Tag&Go, com um ímã no pino e o reed na placa.
- **O que desmontar e observar:**
  - A distância de acionamento do reed em relação ao ímã. Meça com paquímetro enquanto aproxima o ímã.
  - O consumo em repouso e com a sirene ligada.
  - O circuito do buzzer.
  - O porta-pilhas e a PCB de baixo custo.
  - Serve como primeiro exercício de engenharia reversa eletrônica da equipe.
- **Funções do Tag&Go:** indicar estado, energia.

### 6. Trava de gaveta Tuya Bluetooth com cartão (R$ 44,49, AliExpress)

- **Por que comprar:** é o único item barato que faz o fluxo completo do Tag&Go:
  - trava sozinha quando o gancho entra;
  - o app do celular autoriza por BLE;
  - o atuador libera;
  - o app gerencia usuários e chaves, o que lembra o recadastro da etiqueta.

  A carcaça é de ABS parafusada, fácil de abrir e fotografar.
- **O que desmontar e observar:**
  - O gancho com lingueta de mola.
  - O atuador que puxa a lingueta (solenoide ou micromotor).
  - A detecção de aberto ou fechado.
  - O módulo BLE com sua antena.
  - O leitor de cartão de 13,56 MHz com a bobina.
  - As pilhas AAA e o aviso de bateria fraca.
- **Funções do Tag&Go:** comunicação, liberar, reter, reutilizar.
- **Atenção:** o link não foi verificado. Confiram no carrinho o preço, o frete, o imposto e o prazo, em geral de 2 a 6 semanas. Algumas funções remotas pedem um gateway Tuya, mas o BLE direto pelo celular funciona sem ele.
- **Plano B nacional, verificado em 30/09:** fechadura eletrônica oculta RFID para armário, R$ 63,78 + R$ 13,01 de frete, importação já incluída (https://www.amazon.com.br/dp/B0HCKT9RPN). Tem o mesmo gancho, atuador e credencial externa, mas não tem app nem BLE. Com ela o total fica em cerca de R$ 315.

## O que ficou de fora e por quê

- **Mercado Livre e Shopee:** exigiram login ou verificação de tráfego, então nada deles foi verificado. Vale alguém da equipe buscar logado, por exemplo "etiqueta antifurto pino 10 unidades" e "cadeado bluetooth tuya".
- **Cadeados com app Tuya na Amazon:** custam R$ 140 ou mais e estouram o orçamento. No AliExpress há versões de R$ 59 a R$ 90, que também não foram verificadas.
- **Destacador magnético:** o de 5300 GS custa R$ 189 no Pix no Magazine Luiza. Ficou de fora pelo preço.
- **Spider wrap autoalarmante:** R$ 150 ou mais pelo lote de 10 no AliExpress. Também ficou de fora pelo preço.
- **Ideia de custo zero:** pedir à Riachuelo etiquetas quebradas ou de descarte (rígidas, super lock e autoalarmantes) e o empréstimo de um destacador. São os modelos exatos que a rede usa.

## Segurança ao desmontar

- **Baterias de lítio** (LiPo do item 3, CR2032 do item 4 e as que vierem no item 6):
  - retire ou desconecte a bateria antes de mexer na placa;
  - não perfure, dobre, esmague nem aqueça a célula, que pode pegar fogo;
  - isole os terminais com fita;
  - descarte em ponto de coleta de pilhas e baterias, nunca no lixo comum.
- **Proteção:** use óculos de proteção ao abrir peças com mola sob tensão (cadeados, garras de etiqueta) e ao cortar ABS ou metal com micro-retífica.
- **Ímãs de neodímio:** podem prender e ferir os dedos e danificam cartões e eletrônicos.

## Ética

- Desmontem apenas produtos comprados pela equipe, com nota fiscal ou registro do pedido.
- Não testem nada em etiquetas de loja nem em mercadorias de terceiros. O objetivo é entender o projeto do produto (trava, sensor, energia e comunicação), não abrir sistemas antifurto em uso.
- Registrem as desmontagens com fotos e medições no relatório, citando fabricante e modelo, sem copiar projeto protegido.
