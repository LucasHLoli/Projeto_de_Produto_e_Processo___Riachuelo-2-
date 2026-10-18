# Tag&Go: dá para criar? O que já vem pronto?

Pesquisa de 30/09/2026. Demo em 07/12/2026. Tudo o que está aqui foi aberto e conferido nessa data, salvo onde está escrito "não verificado".

## 1. É possível?

Sim, dá para criar o Tag&Go até 07/12 com peças e códigos que já existem. Nenhum projeto público faz o conjunto inteiro (trava na roupa, QR, pagamento, LED e recadastro), mas cada parte tem um produto pronto, um tutorial aberto ou um exemplo de código. A base mais completa continua sendo o plano de vocês (prototipo/mvp-trava-pronta.md), com o Prompt 1 e o Prompt 2, e o que achei serve para preencher os pedaços que faltam. Duas coisas só a bancada responde: se a fechadura trava ao empurrar sem energia e se o power bank segura os 12 V parado e no pulso.

## 2. O que já vem pronto

| Parte do Tag&Go | Base pronta | Link | O que falta |
|---|---|---|---|
| Trava por pressão | Fechadura de armário 12 V "bico de papagaio" com sensor. SARY: bobina de 9 Ω, 1,4 A, R$ 45,89. XG07E: 4 fios, R$ 33,16. As duas estão como "últimas unidades". | [SARY](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-sary-50mm-com-deteccao-de-abertura-8416.html), [XG07E](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-0-8a-4-fios-com-deteccao-de-abertura-8693.html), [Hestore](https://www.hestore.eu/en/prod_10051753.html) | Nenhuma página diz com todas as letras que trava ao empurrar sem energia. Testar na bancada antes de desenhar a peça 3D. Cuidado com a XG07E: a página diz 0,8 A, mas também diz bobina de 6 Ω, e 12 V ÷ 6 Ω dá 2 A. A Hestore vende a mesma família como 12 V e 2 A. Isso contradiz o item 2 do plano e passa dos 1,5 A do power bank. A peça que prende o gancho na roupa (ilhós ou casa de botão) é de vocês. |
| Liberação | Tutorial ESP32 + relé + trava 12 V. A ficha da Hestore (XG-07C, fabricante SARY) diz: bobina de pulso, no máximo 0,5 s ligada. A Tinytronics fala em 10 s de descanso. | [esp32io Solenoid Lock](https://esp32io.com/tutorials/esp32-solenoid-lock), [Hestore](https://www.hestore.eu/en/prod_10051753.html), [Tinytronics](https://www.tinytronics.nl/en/mechanics-and-actuators/locks/electronic-lock-with-feedback-plastic-5v-dc) | O código do tutorial deixa a trava ligada 5 s, dez vezes o limite da ficha: pode queimar a bobina. Usar o pulso de 200 ms do plano. O tutorial não usa diodo: manter o 1N4007 ([Adafruit explica por quê](https://www.adafruit.com/product/1512)). A Tinytronics bloqueou o acesso nesta revisão: os 10 s de descanso ficam como não verificado, mas o plano já usa e não custa nada. |
| Sensor de travado | Na XG07E, os fios amarelo e azul fecham quando está trancada. Na ficha da Hestore (XG-07C), o contato é azul e branco. Tutorial de sensor de porta com INPUT_PULLUP (resistor interno do ESP32 que deixa o pino em nível alto quando o contato está aberto). | [RNT Door Status](https://randomnerdtutorials.com/esp32-door-status-telegram/), [ficha XG07E](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-0-8a-4-fios-com-deteccao-de-abertura-8693.html) | No SARY, a página não diz quantos fios são nem as cores, e as cores mudam de um modelo para outro. Descobrir com multímetro (passo 4). Trocar o Telegram do tutorial pelo aviso ao servidor. |
| LED | Tutorial básico de saídas digitais. Projeto em português com LEDs verde e vermelho e fechadura. | [RNT Digital I/O](https://randomnerdtutorials.com/esp32-digital-inputs-outputs-arduino/), [Usinainfo Fechadura RFID](https://www.usinainfo.com.br/blog/projeto-esp32-fechadura-eletrica-com-rfid/) | A lógica das cores já está no Prompt 2. O projeto da Usinainfo usa o GPIO2 na tranca e o GPIO15 no buzzer, dois pinos de partida: não copiar esses pinos. |
| Comunicação etiqueta e servidor | Tutoriais de ESP32 fazendo GET e POST, HTTPS e leitura de JSON. Dois projetos com fila de comandos e confirmação de execução (ack). | [RNT HTTP](https://randomnerdtutorials.com/esp32-http-get-post-arduino/), [RNT HTTPS](https://randomnerdtutorials.com/esp32-https-requests/), [ArduinoJson + HTTPClient](https://arduinojson.org/v7/how-to/use-arduinojson-with-httpclient/), [Eletrogate](https://blog.eletrogate.com/cotacao-de-moedas-com-httpclient-e-esp32/), [maquina-vending-esp32](https://github.com/eduardowakim-lab/maquina-vending-esp32), [siestabox](https://github.com/KeyCoreSH/siestabox) | Juntar no protocolo do Prompt 2. Os dois repositórios não têm licença: servem só para ler e se inspirar. |
| Página do QR | smart-security-tag: página de pagamento, página de sucesso e painel em Flask. | [smart-security-tag](https://github.com/kishoreSpandiyan/smart-security-tag) | Não gera QR, não instala como está (requirements.txt com pacotes que não existem), só abre no próprio notebook e fala com o ESP32 por cabo USB. Licença ambígua. Serve só como ideia visual e como produto similar no benchmarking. O Prompt 1 gera essa página. |
| Pagamento | Pix de teste no Asaas Sandbox: cria a cobrança, mostra o QR e um botão confirma o pagamento sem dinheiro real. Segunda opção: Mercado Pago Orders API em modo teste, com SDK Python oficial. Exemplo em FastAPI + Railway com Pix do Mercado Pago. | [Asaas Pix](https://docs.asaas.com/docs/cobrancas-via-pix), [Asaas confirmar](https://docs.asaas.com/reference/confirmar-pagamento), [Mercado Pago teste Pix](https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/integration-test/pix), [pix-vending-machine](https://github.com/joaoromaodev/pix-vending-machine) | Criar a conta sandbox, a rota de webhook (aviso automático que o Asaas manda ao servidor quando o pagamento entra) e o botão "Simular pagamento (teste)". Se o Asaas aceita cadastro só com CPF: não verificado. O QR do sandbox só é pago por outra conta sandbox (FAQ do Asaas): app de banco de verdade, no iPhone ou no Android, não paga esse QR. Na demo, usar o botão. O pix-vending-machine não tem arquivo de licença e usa PostgreSQL, não SQLite: só referência. |
| Painel de dados | Painéis com status online pelo último contato, sinal do Wi-Fi, versão do firmware e vendas. | [clube14bis/geladeira](https://github.com/clube14bis/geladeira), [maquina-vending-esp32](https://github.com/eduardowakim-lab/maquina-vending-esp32) | Os dois não têm licença e usam outra stack. O Prompt 1 gera o painel; os dois servem de lista de ideias. |
| Recadastro | Nenhuma base pronta encontrada para "tirar a etiqueta de uma peça e vincular a outra". | (nenhum) | É só software no servidor, e o Prompt 1 já prevê: o servidor só aceita o novo vínculo se o sensor disser "travada". |

Sobre licenças: o único código que pode ser copiado sem dúvida é o [vending-machine-cyd](https://github.com/ViniciusCampeao/vending-machine-cyd) (licença MIT com arquivo LICENSE, mantendo o aviso de copyright). Os outros repositórios não têm arquivo de licença. Leiam, se inspirem e citem a fonte.

## 3. Caminhos possíveis

### Caminho A: plano atual (ESP32 + fechadura de armário) com Pix de teste como extra

- Custo: R$ 538,20 do plano, trocando os R$ 50 reservados do gatilho PD pelos R$ 100,23 vistos na Amazon na pesquisa anterior. Total de cerca de R$ 588 + fretes. Nesta revisão a Amazon bloqueou o acesso automático: conferir o preço no navegador antes de pagar. Para voltar perto dos R$ 540: comprar 1 SARY em vez de 2 (menos R$ 45,89) e ficar com SARY + XG07E, cerca de R$ 542. O Asaas Sandbox custa zero.
- Dificuldade: média. Tem fios, multímetro e firmware, mas cada passo tem tutorial e o código sai dos Prompts 1 e 2. O gatilho PD pode vir só com pads de solda (o tutorial da Zbotic fala em soldar ou prender no borne). Se vier assim, são 2 fios para alguém que saiba soldar.
- O que se perde: nada dos 7 requisitos. O risco é a bancada: a fechadura travar ao empurrar, e o power bank manter 12 V parado e aguentar o pulso. Plano B só para o dia da demo, fora da conta acima: [fonte 12 V 2 A de tomada](https://www.usinainfo.com.br/fonte-chaveada-usb-e-p4/fonte-de-alimentacao-chaveada-12vdc-2a-plug-p4-55x21mm-3921.html) (R$ 28,43) com o [jack P4 fêmea com borne](https://www.usinainfo.com.br/conectores-e-adaptadores/jack-p4-femea-com-borne-a-parafuso-21x55mm-2843.html) (R$ 4,66). É o item 14 que o plano retirou: ele não casa com o cabo KWS-912V, mas casa com essa fonte (as duas são 5,5 × 2,1 mm).

### Caminho B: cadeado inteligente pronto TTLock + gateway Wi-Fi

- Custo: kit cadeado + gateway por cerca de R$ 412 no AliExpress (chega de 16 a 28/10, com impostos estimados) ou cerca de R$ 551 na Amazon. Custo da conta de desenvolvedor: não verificado.
- Dificuldade: baixa no hardware (nada para ligar), média no software (login da API e espera pela aprovação manual da conta, sem prazo informado).
- O que se perde: o LED de vocês (o servidor não controla LED nenhum do cadeado; o estado teria de aparecer no celular). "Trava ao empurrar o arco": não verificado. O guia oficial do gateway dizia que abrir pode levar vários segundos e falhar com sinal fraco (o link deu erro 404 em 30/09: não verificado de novo). Depende de nuvem de terceiros.

### Caminho C: relé Wi-Fi Tuya de pulso no lugar do ESP32

- Custo: cerca de R$ 38 pelo relé (preço do AliExpress não conferido de novo nesta revisão), mantendo fechadura, gatilho PD e power bank. Economiza o ESP32, os relés de 3,3 V e o semáforo. Total estimado de cerca de R$ 527 + fretes.
- Dificuldade: baixa. Não há firmware, só 4 fios e uma chamada à API da Tuya no servidor.
- O que se perde: o sensor "travada" e o semáforo de LED, e com eles a trava de segurança do recadastro. Não verificado: se o pulso desce até 200 ms e quanto demora da nuvem até o relé. A conta gratuita da Tuya é só para uso não comercial.

### Recomendação

Caminho A. É o único que atende os 7 requisitos, inclusive LED e sensor. Deixem o pagamento simulado como padrão da demo e o Asaas Sandbox como extra. Guardem o Caminho B como plano "sem eletrônica" só se a bancada falhar até meados de outubro. Sobre a fechadura: o SARY fica como principal, como no plano. Pela bobina de 9 Ω, puxa cerca de 1,3 A e cabe nos 1,5 A do power bank, com pouca folga. A XG07E tem os fios documentados, mas a conta da bobina de 6 Ω dá 2 A, acima do power bank. Ela fica de reserva e só entra se passar no passo 6 sem o power bank desligar no pulso. Corrijam o item 2 e o B1 do plano, que dizem 0,8 A.

## 4. Passo a passo do Caminho A

1. Compras (até 03/10). Fechaduras, ESP32, relé 3,3 V, semáforo e diodo na [Usinainfo](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-0-8a-4-fios-com-deteccao-de-abertura-8693.html). Gatilho PD na [Amazon](https://www.amazon.com.br/GuiPQS-M%C3%B3dulo-gatilho-Gatilho-Chamariz/dp/B09BZTXHY8) (R$ 100,23 e entrega para 9/10 na pesquisa anterior; conferir no navegador). Nas fotos, ver se a saída do gatilho tem borne ou só pad de solda. Atualizar a planilha para cerca de R$ 588, ou R$ 542 com um SARY só. Deu certo quando: os pedidos estão confirmados.
2. Servidor no notebook (semana de 01/10). Colar o Prompt 1 de mvp-trava-pronta.md no Claude Code e rodar com o simulador. Deu certo quando: no navegador, o funcionário vincula um produto, o cliente paga (simulado) e o painel mostra a venda.
3. Pix de teste, só a API (outubro). Criar conta em sandbox.asaas.com ([FAQ do sandbox](https://docs.asaas.com/docs/faq-sandbox)), cadastrar uma chave Pix de teste e um cliente com CPF fictício, nunca um real. Criar uma cobrança e confirmá-la pela rota de sandbox ([confirmar pagamento](https://docs.asaas.com/reference/confirmar-pagamento)). Deu certo quando: a cobrança aparece como paga no painel do sandbox. Se o cadastro pedir CNPJ, testar o [Mercado Pago em modo teste](https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/integration-test/pix).
4. LEDs e sensor (quando o ESP32 chegar). Seguir [RNT Digital I/O](https://randomnerdtutorials.com/esp32-digital-inputs-outputs-arduino/) para os LEDs e [RNT Door Status](https://randomnerdtutorials.com/esp32-door-status-telegram/) para o sensor, com os dois fios do sensor no GPIO27 e GND. Na XG07E são o amarelo e o azul. No SARY, achar o par com o multímetro na escala de continuidade (a do apito): é o par que apita só com o gancho travado. Deu certo quando: empurrar e soltar o gancho muda "travada/aberta" no Monitor Serial e o LED troca de cor.
5. Gatilho PD. Seguir o passo a passo da [Zbotic](https://zbotic.in/usb-power-delivery-trigger-run-12v-from-usb-c-pd-charger/): se o gatilho vier só com pads, soldar os dois fios de saída antes. Ligar no power bank e medir com multímetro antes de ligar a fechadura. Deu certo quando: o multímetro marca 12,0 V e continua marcando 12 V depois de alguns minutos sem carga (se o power bank desliga parado: não verificado, por isso o teste). Fazer o mesmo teste com o power bank B e o ESP32 ligado por 30 min, porque alguns power banks desligam com consumo baixo (não verificado para os de vocês).
6. Relé, fechadura e diodo. Usar o [esp32io Solenoid Lock](https://esp32io.com/tutorials/esp32-solenoid-lock) como base de ligação, com pulso de 200 ms e 10 s de descanso ([Tinytronics](https://www.tinytronics.nl/en/mechanics-and-actuators/locks/electronic-lock-with-feedback-plastic-5v-dc)) e diodo com a listra no + da bobina. Testar primeiro com o SARY. Deu certo quando: o comando "p" na Serial solta o gancho, empurrar trava de novo, o ESP32 não reinicia e o power bank não desliga no pulso. Repetir com a XG07E: se o power bank desligar no pulso dela (2 A pela conta da bobina), ela sai do projeto.
7. Firmware completo com o servidor do notebook. Colar o Prompt 2 no Claude Code. Referências para o ESP32 conversar com o servidor: [RNT HTTP](https://randomnerdtutorials.com/esp32-http-get-post-arduino/), [RNT HTTPS](https://randomnerdtutorials.com/esp32-https-requests/) e [ArduinoJson + HTTPClient](https://arduinojson.org/v7/how-to/use-arduinojson-with-httpclient/). O IP do servidor no Prompt 2 (192.168.43.10) é só exemplo, de hotspot Android. Ver o IP real do notebook com ipconfig e trocar no config.h. Se o hotspot for de iPhone, ligar "Maximizar Compatibilidade" para ele ficar em 2,4 GHz. Deu certo quando: pagar no celular (mesmo hotspot 2,4 GHz) solta o gancho em cerca de 2 s, e o painel mostra a etiqueta online.
8. Caixa e peça 3D (depois do passo 6). Medir o gancho da fechadura escolhida e desenhar a tampa com passagem por ilhós ou casa de botão. Deu certo quando: dá para prender numa peça de roupa, empurrar até o clique e o sensor marcar "travada".
9. Servidor na Railway (por volta de 10/11). Subir pelo GitHub, com o SQLite num Volume em /data ([docs de volumes](https://docs.railway.com/volumes)) e a variável DB_PATH=/data/tagandgo.db. Sem essa variável, o Prompt 1 grava em ./data, que fica fora do Volume, e o banco some a cada deploy. O [pix-vending-machine](https://github.com/joaoromaodev/pix-vending-machine) mostra um deploy FastAPI na Railway com Procfile e nixpacks.toml (ele usa PostgreSQL, não SQLite). Deu certo quando: um celular no 4G, fora do hotspot, abre a página do QR e o ESP32 aparece online no painel.
10. Pix de teste com webhook (depois do passo 9). Cadastrar a URL da Railway como webhook no Asaas ([webhook de cobranças](https://docs.asaas.com/docs/webhook-para-cobrancas), [sobre webhooks](https://docs.asaas.com/docs/sobre-os-webhooks)). Deu certo quando: o botão "Simular pagamento (teste)" faz o Asaas avisar o servidor e o gancho soltar. Não tentar pagar o QR do sandbox com app de banco: ele só é pago por outra conta sandbox. Se falhar, a demo usa o modo simulado.
11. Congelar em 30/11. Não mudar mais código. Ensaio completo três vezes: recadastrar, vender, liberar. Gravar vídeo de reserva. Deu certo quando: os três ensaios passam sem mexer em nada.
12. Demo em 07/12. Levar power banks carregados, a fonte 12 V de tomada se comprarem, o notebook com o servidor local como plano B e o vídeo.

## 5. Prompt para colar no Claude Code

Nenhum repositório encontrado vale como base de código: os mais parecidos são fracos, usam outra stack ou não têm licença. A base é o código que o Prompt 1 e o Prompt 2 geram. Este prompt acrescenta o Pix de teste por cima dele, depois que o passo 2 estiver funcionando.

```
No servidor FastAPI do Tag&Go (gerado pelo Prompt 1 de prototipo/mvp-trava-pronta.md), acrescente pagamento Pix de teste sem mudar o protocolo do ESP32.

Variável PAGAMENTO=simulado|asaas (padrão simulado). Só no modo asaas, isto substitui a regra "nenhum gateway" do Prompt 1. Em asaas, use o Sandbox do Asaas (https://api-sandbox.asaas.com/v3) com httpx; a chave vem de ASAAS_API_KEY e nunca vai ao navegador. Na primeira cobrança, crie um cliente de teste (POST /customers) e guarde o id no banco. O checkout cria a cobrança PIX (POST /payments) e mostra o QR (GET /payments/{id}/pixQrCode). A compra ganha o estado AGUARDANDO: acrescente AGUARDANDO ao CHECK de compras.status e faça a migração do banco existente. Não crie segunda cobrança se já houver compra AGUARDANDO para o mesmo vínculo. A rota POST /webhooks/asaas confere o header asaas-access-token contra ASAAS_WEBHOOK_TOKEN, ignora eventos repetidos, responde 200 também aos eventos ignorados (o Asaas pausa a fila depois de 15 falhas seguidas) e, em PAYMENT_RECEIVED ou PAYMENT_CONFIRMED, marca a compra como PAGA e cria o comando LIBERAR (o mesmo que o checkout simulado cria hoje). Botão "Simular pagamento (teste)" na página do cliente chama o servidor, que chama POST /sandbox/payment/{id}/confirm. Enquanto a página do cliente estiver aberta, o servidor também consulta o status da cobrança a cada poucos segundos, para a demo funcionar se o webhook falhar. Mantenha o modo simulado como plano B da demo.

Documentação: https://docs.asaas.com/docs/cobrancas-via-pix , https://docs.asaas.com/reference/confirmar-pagamento , https://docs.asaas.com/docs/webhook-para-cobrancas . Não copie código de outros repositórios. Somos iniciantes: comente em português, acrescente testes para o webhook (token errado, evento repetido, pagamento aprovado) e atualize o README com o passo a passo para criar a conta sandbox e configurar as variáveis na Railway.
```

## 6. Links

Fechaduras e fichas
- Usinainfo XG07E: https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-0-8a-4-fios-com-deteccao-de-abertura-8693.html
- Usinainfo SARY: https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide/fechadura-eletronica-12v-sary-50mm-com-deteccao-de-abertura-8416.html
- Tinytronics (descanso entre pulsos; bloqueou acesso automático em 30/09): https://www.tinytronics.nl/en/mechanics-and-actuators/locks/electronic-lock-with-feedback-plastic-5v-dc
- Hestore XG-07C (SARY, 12 V, 2 A, pulso de no máximo 0,5 s): https://www.hestore.eu/en/prod_10051753.html
- Adafruit (diodo na solenoide): https://www.adafruit.com/product/1512

Tutoriais de ESP32
- esp32io Solenoid Lock: https://esp32io.com/tutorials/esp32-solenoid-lock
- esp32io Button Solenoid Lock: https://esp32io.com/tutorials/esp32-button-solenoid-lock
- RNT Door Status: https://randomnerdtutorials.com/esp32-door-status-telegram/
- RNT Digital I/O: https://randomnerdtutorials.com/esp32-digital-inputs-outputs-arduino/
- RNT Relé: https://randomnerdtutorials.com/esp32-relay-module-ac-web-server/
- RNT HTTP GET/POST: https://randomnerdtutorials.com/esp32-http-get-post-arduino/
- RNT HTTPS: https://randomnerdtutorials.com/esp32-https-requests/
- ArduinoJson com HTTPClient: https://arduinojson.org/v7/how-to/use-arduinojson-with-httpclient/
- Eletrogate, cotação com HTTPClient: https://blog.eletrogate.com/cotacao-de-moedas-com-httpclient-e-esp32/
- Usinainfo, fechadura com RFID: https://www.usinainfo.com.br/blog/projeto-esp32-fechadura-eletrica-com-rfid/
- MakerHero, trava com RFID (comentários sobre o Arduino que trava): https://www.makerhero.com/blog/acionando-trava-eletrica-com-rfid/
- Vídeo PCS3732, fechadura com ESP32-CAM (Poli-USP): https://www.youtube.com/watch?v=4unVPydu2CM
- Vídeo INPUT_PULLUP no ESP32 (Tiago Borsa): https://www.youtube.com/watch?v=t_deWnbanlY

Alimentação
- Gatilho PD 12 V na Amazon (preço a conferir no navegador): https://www.amazon.com.br/GuiPQS-M%C3%B3dulo-gatilho-Gatilho-Chamariz/dp/B09BZTXHY8
- Fonte 12 V 2 A de tomada, plano B da demo: https://www.usinainfo.com.br/fonte-chaveada-usb-e-p4/fonte-de-alimentacao-chaveada-12vdc-2a-plug-p4-55x21mm-3921.html
- Jack P4 fêmea com borne, para a fonte: https://www.usinainfo.com.br/conectores-e-adaptadores/jack-p4-femea-com-borne-a-parafuso-21x55mm-2843.html
- Zbotic, usar gatilho PD: https://zbotic.in/usb-power-delivery-trigger-run-12v-from-usb-c-pd-charger/
- Embarcados, USB-PD: https://embarcados.com.br/usando-um-carregador-usb-pd-na-sua-aplicacao/

Pagamento
- Asaas Pix: https://docs.asaas.com/docs/cobrancas-via-pix
- Asaas FAQ sandbox: https://docs.asaas.com/docs/faq-sandbox
- Asaas confirmar pagamento: https://docs.asaas.com/reference/confirmar-pagamento
- Asaas webhook de cobranças: https://docs.asaas.com/docs/webhook-para-cobrancas
- Asaas sobre webhooks: https://docs.asaas.com/docs/sobre-os-webhooks
- Mercado Pago, teste Pix (Orders API): https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/integration-test/pix
- Mercado Pago, notificações: https://www.mercadopago.com.br/developers/pt/docs/checkout-api-orders/notifications
- SDK Python do Mercado Pago: https://github.com/mercadopago/sdk-python

Repositórios de referência
- smart-security-tag (produto similar, licença ambígua): https://github.com/kishoreSpandiyan/smart-security-tag
- pix-vending-machine (FastAPI + Railway + Pix, sem arquivo de licença): https://github.com/joaoromaodev/pix-vending-machine
- vending-machine-cyd (MIT): https://github.com/ViniciusCampeao/vending-machine-cyd
- maquina-vending-esp32 (fila de comandos com ack, sem licença): https://github.com/eduardowakim-lab/maquina-vending-esp32
- clube14bis/geladeira (relé e painel, sem licença): https://github.com/clube14bis/geladeira
- siestabox (ack e simulador, sem licença): https://github.com/KeyCoreSH/siestabox

Caminhos B e C
- TTLock, destravar pela nuvem: https://euopen.ttlock.com/doc/api/v3/lock/unlock
- TTLock, consultar estado: https://euopen.ttlock.com/doc/api/v3/lock/queryOpenState
- TTLock, guia do gateway (deu erro 404 em 30/09): https://euopen.ttlock.com/document/doc?urlName=userGuide%2FgatewayEn.html
- Gateway G2 na Amazon: https://www.amazon.com.br/dp/B09BN9X8XM
- Cadeado TTLock na Amazon: https://www.amazon.com.br/dp/B0GDMZHV8X
- Kit TTLock no AliExpress: https://pt.aliexpress.com/item/1005009793017573.html
- Relé Wi-Fi Tuya de pulso: https://pt.aliexpress.com/item/1005005194763335.html
- Tuya, controle de dispositivo: https://developer.tuya.com/en/docs/cloud/device-control?id=K95zu01ksols7

Servidor
- Railway, volumes: https://docs.railway.com/volumes

Limites desta pesquisa: a busca na web bateu no limite da sessão, e parte das páginas foi lida por download direto. A busca de código foi feita só no GitHub; blogs, fóruns e Hackster ficaram de fora. Dos vídeos do YouTube, foram conferidos título, canal e descrição, sem assistir. Preços do Mercado Livre e tarifas de produção dos provedores de Pix: não verificados. Na revisão de 30/09, Amazon, Tinytronics e M2P Tech bloquearam o download direto, os preços do AliExpress não foram conferidos de novo e o guia do gateway TTLock deu 404. Os outros links abriram.
