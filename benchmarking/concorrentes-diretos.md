# Tag&Go: concorrentes diretos

Pergunta do grupo: a ideia já existe? Quem faz isso ou algo parecido, se deu certo e o que sobra de novo para o Tag&Go.

Data da conferência: 30/09/2026. Tudo aqui foi conferido em página aberta. O que não foi confirmado está na lista do fim. Os números entre colchetes remetem às fontes da seção 8.

Escala de semelhança: 3 = faz o fluxo central (pagar no celular e a própria etiqueta soltar); 2 = faz boa parte, mas falta uma peça importante (por exemplo, a soltura acontece numa estação); 1 = só toca no tema (autoatendimento, RFID, trava que abre depois de pagar).

## 1. A ideia já existe?

Sim, o fluxo central já existe. A Zliide (Dinamarca) e a rapitag (Alemanha) venderam etiquetas rígidas que se soltam sozinhas depois de o cliente pagar no celular, e a Zliide ainda recolhia a etiqueta numa caixa na loja para reusar [11][12][2]. As duas não deram certo: a rapitag entrou em insolvência em 2025 e a Zliide teve os ativos vendidos por valor simbólico no mesmo ano [1][11]. O mecanismo e o fluxo também estão em patentes, algumas vigentes nos EUA e na Europa até 2035 ou 2036 (Sensormatic) e uma vigente na China até 2035 (JD.com), que já descreve QR na etiqueta, pagamento no celular e servidor mandando a etiqueta abrir [58][60][75]. O que não encontramos em nenhum lugar é a combinação de Pix, página web sem app, etiqueta de roupa no Brasil e volta da etiqueta pela logística de reposição de uma rede verticalizada.

## 2. Quem faz exatamente isso (semelhança 3)

| Nome | País | Como a etiqueta recebe a liberação | Precisa de app? | Status hoje | Link |
|---|---|---|---|---|---|
| Zliide (etiqueta Bluetooth para roupa) | Dinamarca | Sinal Bluetooth (BLE) enviado à etiqueta depois que o pagamento no celular é aprovado. A fonte não diz se quem envia é o celular do cliente. O cliente deixa a etiqueta num coletor e ela é reutilizada. | Sim, na origem (app Zliide) | Encerrada como empresa. Ativos (marca, patentes, software, clientes) vendidos à Touchtech AB por valor simbólico em 14/07/2025, sem funcionários | [11], [12] |
| Secure Mobile Self-Checkout (Sensormatic com Zliide) | EUA e Dinamarca | Etiqueta de peça única com pino que abre depois da compra feita no celular, na arara. Depois o cliente deposita a etiqueta numa caixa perto da saída. | A Sensormatic anunciou em 2023 que não é preciso baixar app. Como isso funciona não foi verificado | Mostrado na NRF e na EuroShop em 2023 e oferecido à venda em jan/2024. Nenhum varejista citado. Situação em 2026 não verificada | [13], [15], [17] |
| rapitag (Fashiontag, Safer Tag, Spider) | Alemanha | Chave digital enviada por Bluetooth do celular à etiqueta depois do pagamento no app. No piloto de 2024 as etiquetas abriam sozinhas no caixa e no self-checkout, sem destacador. | Sim | Insolvente. O administrador declarou massa insuficiente em 02/10/2025 | [1], [2], [4] |
| Saturn Smartpay (MediaMarktSaturn com rapitag) | Alemanha | Bluetooth. O cliente paga no app e aproxima o celular da etiqueta "spider", que destrava. A etiqueta ia para um recipiente na loja e era reutilizada. | Sim, app Saturn Smartpay com cadastro | Piloto encerrado. Set a nov/2018, uma loja no shopping PEP, em Munique, só com fones de ouvido | [3], [7], [8] |

Além desses produtos, o fluxo inteiro aparece em patentes. A mais próxima é a CN105389924B, da JD.com: a etiqueta mostra um QR, o cliente paga no celular e o servidor manda um sinal que abre a trava [75]. Ver a seção 5.

## 3. Quem faz quase isso (semelhança 2) e o que falta a cada um

| Nome | País | O que faz | O que falta em relação ao Tag&Go | Link |
|---|---|---|---|---|
| Paytag | Israel | O cliente escaneia a etiqueta, paga no app e leva a peça a uma pequena estação que só solta a etiqueta depois de o servidor autorizar. Em uso comercial em Israel em jan/2026. | A etiqueta não se solta sozinha. Exige app. Não tem Pix. | [20], [21], [72] |
| QueueHop | EUA | Estação com leitor RFID lia a etiqueta, conferia o pagamento e soltava o pino. A etiqueta caía numa caixa de descarte e era reutilizada. Usada na loja da Rebecca Minkoff, em Nova York (dez/2016). | A soltura era na estação. Pagamento no celular era só opção. Empresa encerrada. | [22], [23], [24] |
| Secure Mobile Shopping Kiosk (Tyco/Sensormatic com Shopic) | EUA e Israel | Compra no celular e quiosque com destacador RFID que solta a etiqueta de pino integrado. | Soltura no quiosque. Só demonstração em 2018; venda não verificada. | [26], [27] |
| Piloto da rapitag em varejista alemão não nomeado | Alemanha | 6 lojas e mais de 3.500 etiquetas que abrem sozinhas depois do pagamento no caixa ou no self-checkout (nota de 29/11/2024). | O gatilho é o caixa, sem pagamento no celular do cliente. Sem métricas. Só fonte da própria empresa. | [4] |
| Decathlon Scan & Go (MishiPay) | Holanda e Alemanha | O cliente paga no app e a segurança RFID do item é desativada automaticamente. Chegou a todas as lojas da Holanda (2019) e começou nas 81 lojas da Alemanha (2020). | Não há trava física. Exige app. Não tem Pix. | [28], [29], [30], [31] |
| smart-security-tag (projeto de estudante no GitHub) | Não verificado | ESP32 com servidor Flask. O cliente abre uma página web por QR, faz um pagamento simulado e um servo destrava a etiqueta. | Pagamento real, recarga, urna e reuso. Mostra que a arquitetura técnica do protótipo do Tag&Go já está publicada. | [33] |

Casos de semelhança 1 que importam para o Brasil:

- Lojas Renner: totens com RFID que leem as peças e retiram o alarme. Eram 742 terminais em 213 lojas no fim de 2023, com cerca de 38% dos pagamentos nas lojas que têm totem [43][44][45]. No Pague Digital o cliente paga no app, mas um colaborador tira o alarme [46].
- Riachuelo: pop-up em Pinheiros (dez/2025) e loja de Curitiba (abr/2026) com 100% self-checkout e etiquetas RFID. Nenhuma fonte explica como o alarme é retirado [47][48][50]. A rede já tem RFID em fábricas, CDs e 343 lojas [49].
- Decathlon Brasil: checkout RFID em 50 lojas (press release de 28/08/2025) [51].
- RedGo e Gela Smart: geladeiras autônomas em que o cliente paga por Pix numa página aberta por QR, sem app, e a trava da porta abre [52][53]. É o mesmo padrão de pagamento do Tag&Go, aplicado a uma porta.

## 4. O que aconteceu com eles

Quem fechou ou foi vendido:

- QueueHop (EUA). Lançada em 2016, primeiro cliente em dez/2016 e parceria com a fabricante TrustTag em abr/2017 [22][25]. Em out/2018 o CB Insights já a chamava de extinta [24]. O fundador disse ao TechCrunch que era difícil escalar um produto que obriga o lojista a repensar todo o fluxo da loja. Ele entrevistou cerca de 150 lojistas e mudou para carrinho inteligente (Caper) [23]. É o único motivo de fechamento confirmado em fonte.
- rapitag (Alemanha). Fundada em 2017. O CB Insights registra só US$ 10 mil captados e 14 patentes depositadas [10]. Fez o piloto na Saturn (2018), o piloto de 6 lojas (2024) e um piloto no Japão com 200 etiquetas numa loja (2024) [3][4][5]. Nenhum piloto publicou números de furto ou de conversão. Declarou massa insuficiente em out/2025 [1]. O motivo da falência não foi verificado.
- Zliide (Dinamarca). Captou US$ 4,48 milhões em 5 rodadas, a última em 16/09/2021 [18]. Em jan/2021 estava em 10 pequenas lojas, com 41% dos compradores usando o app [12]. A Cre8tek produziu as primeiras 100 mil etiquetas em dez/2021, usadas em lojas Weekday e Bestseller [17]. A Bestseller testou em Aarhus e em Copenhague e previa mais 4 lojas em 2022 [16]. Em 2023 veio a parceria com a Sensormatic [13]. Em jul/2025 os ativos foram vendidos por valor simbólico, sem funcionários [11]. Nenhum resultado de venda ou de perda foi publicado. O motivo não foi verificado.
- Nexite (Israel). Etiqueta Bluetooth sem bateria, com pagar e sair previsto para 2023 [38]. Hoje o site só oferece análise do comportamento do cliente [39].

Quem cresceu (todos sem etiqueta que se solta sozinha):

- MishiPay (Reino Unido). Diz estar em mais de 2.000 lojas e 35 marcas e anunciou nova captação de 4,4 milhões de libras em 2025 [34][37]. Na Mango de Londres (fim de 2018), o pagamento no celular chegou a 43% das transações diárias no pico, mas a etiqueta rígida continuava sendo tirada por um funcionário [35]. Num teste da Saturn em Innsbruck, a diferença de inventário ficou igual à média da empresa [6].
- Renner. Passou de 13 lojas com autoatendimento em 2021 para 213 lojas no fim de 2023 [43][45].
- Paytag. Levantou US$ 2 milhões com investidores-anjo em 2024 e tinha 8 funcionários em jan/2026 [20].
- Zara (Inditex). Trocou a etiqueta rígida por RFID invisível; o sistema estava totalmente operacional na Zara no ano fiscal 2024 [40][42]. Em set/2023 houve relatos de ladrões arrancando os chips e de alarmes falsos com devoluções online [41].
- Riachuelo. Em set/2026 relatou melhora de tíquete, NPS, tempo de permanência e recompra no novo modelo de loja, sem números. A avaliação completa fica para abr/2027 [48].

Dados sobre tirar a barreira física (fonte da Sensormatic, que vende etiqueta rígida): num varejista a perda mais que dobrou em 1 ano depois de retirar a etiqueta rígida; em outro subiu de 40% a 70% em 7 semanas em alguns departamentos [55]. A Sensormatic também cita que a rede Wegmans fechou seu app de pagamento pelo celular por causa de perdas [93]. Em 2018 a própria Sensormatic disse que sua etiqueta InFuzion preparava a base para comprar pelo app com destacamento automático, sem produto lançado com esse nome [56].

Padrão observado, sem dado de mercado que o prove: as startups de etiqueta que se solta sozinha fecharam ou foram vendidas, e as que cresceram evitaram etiqueta ativa (RFID lógico ou estação central).

## 5. Patentes que pesam

Nenhuma das patentes abaixo tem membro brasileiro na família listada pelo Google Patents, com uma exceção (Samsung). A busca no INPI não foi feita, e pedidos depositados depois de mar/2025 ainda estão em sigilo. Isto é leitura de reivindicações, sem valor de parecer jurídico.

Vigentes e mais próximas do Tag&Go:

| Patente | Titular | O que cobre | Validade | Brasil |
|---|---|---|---|---|
| US10121339B2 [58] | Sensormatic (na capa, Tyco) | Etiqueta recebe comando sem fio depois da compra verificada e o pino recolhe para dentro, sem destacador | EUA até 21/10/2035, 8º ano pago em 28/04/2026. Família com EP, CN e ES | Sem membro BR visto |
| US10522016B2 [59] e EP3265631B1 [60] | Sensormatic | Pino retido, sinal sem fio, mola recolhe o pino sem ajuda externa. É a reivindicação mais ampla da família | EUA até 04/03/2035 (outra base diz 2036). EP ativa, anuidades de 2026 pagas no Reino Unido, Alemanha e França, até 02/03/2036 | Sem membro BR visto |
| US10121338B2 [57] | Sensormatic | Rearme do pino por pinhão e cremalheira, com lingueta | EUA até 20/01/2036, 8º ano pago em 28/04/2026 | Sem membro BR visto |
| US11694529B1 [69] | rapitag (insolvente) | Infraestrutura sem fio da loja detecta as etiquetas e envia o comando de liberar. Uma arquitetura com Wi-Fi e servidor da loja pode cair nela nos EUA | EUA até 13/06/2042. Taxa que vence até 04/01/2027 não verificada | Sem membro BR visto |
| CN105389924B [75] | JD.com | QR gerado pela etiqueta, pagamento no celular, servidor em nuvem manda sinal e um eletroímã abre a trava | China até 26/11/2035 | Só China |
| US8963717B2 [64] | Sensormatic | Celular envia dados de compra a um sistema remoto e depois passa à etiqueta a chave de soltar por curto alcance. No Tag&Go o servidor fala direto com a etiqueta | EUA até 10/08/2033 se a taxa do 12º ano for paga (não verificado) | Sem membro BR |
| US9117355B2 [65] e US9852596B2 [66] | Sensormatic (na capa da segunda, Tyco) | App no celular recebe a autorização e manda o comando ou o código de desbloqueio à etiqueta | EUA até 01/03/2033 e 10/11/2035 | Sem membro BR visto |
| US9460597B1 [67] e US10325464B1 [68] | Sensormatic | Código de uso único por etiqueta; código assinado com chave própria de cada etiqueta | EUA até 19/06/2035 e 05/04/2038 (esta com EP e CN ativos) | Sem membro BR visto |
| US10354507B1 [70] | Mastercard | Associar etiqueta e peça por foto e soltar depois do pagamento. Um recadastro sem imagem tende a ficar fora | EUA até 02/01/2038 (status de hoje não reconferido) | Sem membro BR visto |
| EP3740631B1 [19] | Zliide (ativos comprados pela Touchtech) | Mecânica da etiqueta de duas partes com trava de pino e alavanca | Europa até 17/01/2039, anuidades de 2025 pagas em 6 países | Sem membro BR |
| US12101138B2 [61], US9978236B2 [62], US10497238B2 [63] | Sensormatic | Etiqueta que se solta com energia vinda de fora (ressonância ou estação com contato) | EUA até 2040 e 2036 | Sem membro BR visto |
| US10586228B2 [77] e BR102014004206A2 [78] | Samsung Eletrônica da Amazônia | App recebe do servidor uma chave e desliga o alarme da etiqueta. Não solta pino | EUA até 15/04/2034. No INPI: indeferido em 10/05/2022, com recurso em 28/06/2022 e desfecho não verificado | Único pedido BR da área que pode estar vivo |

Estações e destacadores, com peso menor para o Tag&Go: US10186128B2 da QueueHop, hoje com a Instacart, até 2037 [71]; US12277471B2 da Paytag, até 2042 [72]; US11414895B2 da Sensormatic, destacador que despeja a etiqueta num recipiente, até 2040 [73]; US11417186B2 da Kohl's, até 2040 [74]; US10134209B2 da Exaqtworld, até 2033 [76]; ES2574354B1 da Buy Yourself, na Espanha até 2035 [79].

Já caíram e são de uso livre:

- US7564360B2 (Checkpoint): etiqueta rígida que abre por sinal de rádio. Caducou em 2017 [80].
- US7450013B2 (Checkpoint): soltar a etiqueta no caixa só se o banco de dados confirmar a venda. Expirou em 2025 [81].
- CN110512964A e CN211342251U (inventor chinês): código de pagamento na etiqueta, rádio que recebe a ordem do servidor e atuador que solta um pino travado por mola e esfera. O pedido foi rejeitado em 24/06/2025 e o modelo de utilidade foi extinto em 2024 [82][83]. É o núcleo técnico do Tag&Go, publicado e livre.
- KR101714006B1 (Coreia): servidor manda destravar depois do pagamento no terminal do cliente. Extinta em 2024 [84].
- CN107204057A (China): pagamento por página web aberta a partir do rótulo da etiqueta. Rejeitado em 2021 [89].
- CN109035660B (China): fecho de pino que abre e trava de novo por comando remoto. Extinta em 2024 [87].
- EP3038066A1 (Polônia), WO2017155485A1 (Turquia), WO2015121833A1 (Visa), GB2503720A (Reino Unido) e BR102017012133A2 (Brasil): pedidos retirados, encerrados ou arquivados [85][86][88][91][90].
- US20180374327A1 (EUA): app de autoatendimento, trava que abre depois do pagamento e travas deixadas na loja para reuso. Publicado em 2018; o abandono não foi reconferido [92].

## 6. O que o Tag&Go tem de novo de verdade

O que já existe e por isso não serve como diferencial:

- Etiqueta rígida com pino que se solta sozinha depois do pagamento: Zliide com Sensormatic e rapitag [13][15][4], além das patentes da Sensormatic [58][59].
- Servidor mandando a etiqueta abrir, sem o celular do cliente como ponte: patentes CN105389924B, CN110512964A e US11694529B1 [75][82][69].
- QR na etiqueta, página web e "sem baixar app": patentes chinesas [75][89] e o anúncio da Sensormatic com a Zliide em 2023 [13].
- Caixa ou urna de devolução com reuso na loja: Zliide, QueueHop e Saturn [12][22][7].
- Recirculação de etiquetas pela cadeia até a fábrica: a Sensormatic já faz isso com etiquetas comuns, mais de 2,5 bilhões em cerca de 2 anos [54].
- A arquitetura do protótipo (ESP32, QR, página web, servidor, atuador): projeto de estudante publicado no GitHub [33].
- LED verde de confirmação: não pesquisado, e é um detalhe fácil de copiar.

Diferenciais possíveis:

1. Ciclo de reuso de uma etiqueta eletrônica pela logística de reposição da rede verticalizada (loja, CD e fábrica), com recarga da bateria e recadastro em outra peça. Evidência: a Zliide e a QueueHop só recolhiam a etiqueta na própria loja [12][22], e a recirculação da Sensormatic é de etiqueta sem eletrônica ativa [54]. Nenhuma fonte descreve recarga e volta de etiqueta ativa pela cadeia. A Riachuelo já tem RFID em fábricas, CDs e lojas para rastrear essa volta [49]. Situação: a confirmar.
2. Pagamento por Pix numa página web aberta por QR para liberar etiqueta de roupa. Evidência: nenhum concorrente de etiqueta com Pix foi encontrado. O mesmo padrão já libera portas de geladeiras no Brasil (RedGo e Gela Smart) [52][53], e a ideia de página web está em patente chinesa rejeitada [89]. É diferencial de mercado no Brasil, sem novidade para patente. Situação: a confirmar.
3. Autoatendimento de moda no Brasil sem totem e sem funcionário, mantendo a barreira física do pino. Evidência: Renner, Decathlon Brasil e Riachuelo usam totem com RFID [43][51][47], e no Pague Digital da Renner um colaborador tira o alarme [46]. Nenhuma etiqueta que se solta sozinha foi encontrada no Brasil. Lá fora isso já existiu e não se sustentou (seção 4). Situação: a confirmar no Brasil.

## 7. Como isso entra no Relatório 2

Item B (diferenciação): O fluxo de pagar no celular e a etiqueta soltar sozinha já foi testado na Europa pela Zliide e pela rapitag, as duas encerradas em 2025, então a diferenciação do Tag&Go está em levar esse fluxo ao varejo de moda brasileiro com Pix e página web sem app e em fazer a etiqueta voltar, ser recarregada e reusada pela logística de reposição da Riachuelo, o que não encontramos em nenhum concorrente.

Item D (aproveitamento técnico): O projeto pode reaproveitar soluções já publicadas e sem proteção no Brasil, como o pino travado por mola e esfera que solta por comando sem fio (CN110512964A e CN211342251U, já caídas, e US7564360B2, caducada) e o código de uso único por etiqueta (US9460597B1, vigente só nos EUA), deixando para verificar no INPI a situação da Samsung e, se houver exportação, as patentes da Sensormatic vigentes nos EUA e na Europa.

## 8. Fontes

1. Insolvenz-Radar, rapitag GmbH: https://insolvenz-radar.de/firmeninsolvenz/hrb+235416/m%C3%BCnchen/d2601/
2. etailment, rapitag: https://etailment.de/news/stories/warensicherung-diebstahl-smart-payment-21985
3. Munich Startup, rapitag e MediaMarktSaturn: https://www.munich-startup.de/40129/parcellab-rapitag-mediamarktsaturn/
4. EuroCIS, piloto da rapitag (29/11/2024): https://www.eurocis-tradefair.com/en/Visit/What_to_expect/Exhibitor_News/Transforming_Retail_rapitag%60s_Pilot_Program_Proves_Successful
5. SCE, rapitag no Japão: https://www.sce.de/en/news-details/rapitag-introduces-smart-anti-theft-tags-in-japan.html
6. stores+shops, Saturn e MishiPay: https://www.stores-shops.de/technology/security/self-checkout-der-kunde-entsichert-selbst/
7. stores+shops, Saturn Smartpay: https://www.stores-shops.de/technology/mobile-self-checkout-spinne-statt-schlange/
8. Stadt Bremerhaven, Saturn Smartpay: https://stadt-bremerhaven.de/saturn-smartpay-kassenloses-bezahlen-wird-aktuell-in-muenchener-filiale-getestet/
9. iXtenso, etiquetas RFID: https://ixtenso.com/technology/rfid-tags-with-features-for-the-cashierless-store.html
10. CB Insights, rapitag: https://www.cbinsights.com/company/rapitag
11. MarketScreener, Touchtech compra a Zliide: https://www.marketscreener.com/quote/stock/TOUCHTECH-AB-149016198/news/Touchtech-Acquires-Rare-Competitor-Zliides-No-Staff-Transition-Involved-50503076/
12. RFID Journal, etiqueta BLE da Zliide: https://www.rfidjournal.com/news/ble-hard-tag-allows-in-store-shoppers-to-buy-goods-via-smartphone/188639/
13. Sensormatic, NRF 2023 com Zliide: https://www.sensormatic.com/resources/pr/2023/nrf-2023-zliide
14. Sensormatic, EuroShop 2023 com Zliide: https://www.sensormatic.com/en_au/resources/pr/2023/euroshop-2023-zliide
15. Sensormatic, NRF 2024: https://www.sensormatic.com/resources/pr/2024/nrf-2024-pre-nrf
16. FashionNetwork, Bestseller testa a Zliide: https://ww.fashionnetwork.com/news/Bestseller-tests-zliide-digital-tech-solution-for-its-brands,1339874.html
17. Cre8tek, produção das etiquetas Zliide: https://cre8tek.com/cases/cre8tek-has-upscaled-zliides-production-of-their-iot-security-tags/
18. Tracxn, Zliide: https://tracxn.com/d/companies/zliide/__fGdhJwo8ySuCAocs7_ggG_pjYiYjbdEThoSkqgEA5mA
19. EP3740631B1 (Zliide): https://patents.google.com/patent/EP3740631B1/en
20. Ctech, Paytag (21/01/2026): https://www.calcalistech.com/ctechnews/article/5i583v2fg
21. Mako, Paytag (2023): https://www.mako.co.il/nexter-news/Article-9da4c9b80da5681027.htm
22. RFID Journal, QueueHop na Rebecca Minkoff: https://www.rfidjournal.com/news/rebecca-minkoff-brings-self-service-to-its-soho-store-with-rfid-2/70732/
23. TechCrunch, Caper (2019): https://techcrunch.com/2019/01/10/caper-shopping-cart/
24. CB Insights, varejo sem caixa (2018): https://www.cbinsights.com/research/cashierless-retail-technologies-companies-trends/
25. TrustTag e QueueHop: https://www.trusttag.com/anti-theft-device/rfid-tags/trusttag-and-queuehop-announce-a-partnership-in-self-checkout-technology/
26. Sensormatic, NRF 2018: https://www.sensormatic.com/resources/pr/2018/trs-enables-connected-shopper-engagement
27. Sensormatic, RILA 2018: https://www.sensormatic.com/resources/pr/2018/media-alert-rila
28. MishiPay, Decathlon Scan & Go: https://mishipay.com/mishipay-decathlon-scan-and-go/
29. NFCW, Decathlon Holanda (2019): https://www.nfcw.com/2019/06/10/362880/decathlon-to-introduce-scan-and-go-to-all-stores-in-the-netherlands/
30. Dutch Tech, Decathlon (2019): https://www.dutch-tech.nl/2019/10/decathlon-introduceert-scan-go-in-alle-winkels.html
31. MishiPay, Decathlon Alemanha: https://mishipay.com/decathlon-deutschland-launches-scan-go-with-mishipay/
32. MishiPay, estudo de caso de varejista de esportes: https://mishipay.com/casestudy/leading-sports-retailer/
33. GitHub, smart-security-tag: https://github.com/kishoreSpandiyan/smart-security-tag
34. MishiPay, site: https://mishipay.com/
35. MishiPay, caso Mango: https://mishipay.com/case-study/mango/
36. NFCW, Decathlon Alemanha (2020): https://www.nfcw.com/2020/05/14/366529/decathlon-rolls-out-mobile-self-checkout-to-81-stores-across-germany/
37. MishiPay, captação de 4,4 milhões de libras: https://mishipay.com/mishipay-raises-4-4m-in-expansion-capital-to-revolutionise-in-store-retail/
38. RFID Journal, Nexite: https://www.rfidjournal.com/news/passive-ble-brings-real-time-data-to-apparel-retailers/197265/
39. Nexite, site: https://www.nexite.io/
40. Inditex, resultados do ano fiscal 2024: https://www.inditex.com/itxcomweb/aq/en/press/news-detail/6f8d8db5-4d7a-43db-91b9-0c38065aec1e/fy2024-results
41. FashionNetwork, falhas do sistema da Zara: https://uk.fashionnetwork.com/news/Zara-finds-shoplifters-able-to-outsmart-its-new-security-system,1555245.html
42. Infobae, Zara sem alarme físico: https://www.infobae.com/espana/agencias/2025/03/12/zara-estrena-un-sistema-de-pago-sin-pasar-por-caja-y-sin-alarmas-fisicas-antirrobo/
43. Lojas Renner, autoatendimento com RFID: https://www.lojasrennersa.com.br/imprensa-destaques/renner-acelera-implantacao-de-caixas-de-autoatendimento-com-tecnologia-rfid/
44. Sensormatic, caso Renner: https://www.sensormatic.com/pt_br/resources/cs/2022/renner
45. Mercado&Consumo, Renner (jan/2024): https://mercadoeconsumo.com.br/31/01/2024/destaque-do-dia/renner-investe-em-caixas-de-autoatendimento-para-melhorar-experiencia-de-compra/
46. Blog Lojas Renner, app e Pague Digital: https://blog.lojasrenner.com.br/2022/11/vem-aprender-como-usar-o-aplicativo-renner/
47. Mercado&Consumo, pop-up da Riachuelo: https://mercadoeconsumo.com.br/08/12/2025/noticias/riachuelo-revela-loja-pop-up-em-sp-que-servira-de-modelo-para-mais-de-300-unidades-da-rede/
48. Economic News Brasil, novo modelo da Riachuelo (24/09/2026): https://economicnewsbrasil.com.br/2026/09/24/novo-modelo-riachuelo-retorno-lojas/
49. TI Inside, RFID da Riachuelo (2022): https://tiinside.com.br/20/01/2022/riachuelo-acelera-gestao-de-estoques-com-tecnologia-rfid/
50. FashionNetwork Brasil, Riachuelo testa self-checkout: https://br.fashionnetwork.com/news/Em-fase-de-rebranding-riachuelo-testa-novo-modelo-de-loja-com-self-checkout-e-provador-inteligente,1791297.html
51. Sensormatic, Decathlon Brasil: https://www.sensormatic.com/resources/pr/2025/decathlon-brasil-press-release
52. RedStore, RedGo: https://redstore.com.br/redgo
53. Gela Smart, geladeira autônoma: https://www.gelasmart.com/franquia-geladeira-autonoma
54. Sensormatic, recirculação de etiquetas rígidas: https://www.sensormatic.com/resources/ar/2024/hard-tag-recirculation-among-stevie-awards-sustainability-initiatives-of-the-year
55. Sensormatic, retirada da etiqueta rígida: https://www.sensormatic.com/resources/ar/2024/hard-tag-removal-blog-2
56. PR Newswire, lançamento do InFuzion (2018): https://www.prnewswire.com/news-releases/new-sensormatic-infuzion-anti-theft-tag-helps-boost-operational-efficiencies-and-profitability-with-revolutionary-new-design-300659370.html
57. US10121338B2: https://patents.google.com/patent/US10121338B2/en
58. US10121339B2: https://patents.google.com/patent/US10121339B2/en
59. US10522016B2: https://patents.google.com/patent/US10522016B2/en
60. EP3265631B1: https://patents.google.com/patent/EP3265631B1/en
61. US12101138B2: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12101138
62. US9978236B2: https://patents.google.com/patent/US9978236B2/en
63. US10497238B2: https://patents.google.com/patent/US10497238B2/en
64. US8963717B2: https://patents.google.com/patent/US8963717B2/en
65. US9117355B2: https://patents.google.com/patent/US9117355B2/en
66. US9852596B2: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9852596
67. US9460597B1: https://patents.google.com/patent/US9460597B1/en
68. US10325464B1: https://patents.google.com/patent/US10325464B1/en
69. US11694529B1: https://patents.google.com/patent/US11694529B1/en
70. US10354507B1: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10354507
71. US10186128B2: https://patents.google.com/patent/US10186128B2/en
72. US12277471B2: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12277471
73. US11414895B2: https://patents.google.com/patent/US11414895B2/en
74. US11417186B2: https://patents.google.com/patent/US11417186B2/en
75. CN105389924B: https://patents.google.com/patent/CN105389924B/en
76. US10134209B2: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10134209
77. US10586228B2: https://patents.google.com/patent/US10586228B2/en
78. BR102014004206A2: https://patents.google.com/patent/BR102014004206A2/en
79. ES2574354B1: https://patents.google.com/patent/ES2574354B1/en
80. US7564360B2: https://patents.google.com/patent/US7564360B2/en
81. US7450013B2: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7450013
82. CN110512964A: https://patents.google.com/patent/CN110512964A/en
83. CN211342251U: https://patents.google.com/patent/CN211342251U/en
84. KR101714006B1: https://patents.google.com/patent/KR101714006B1/en
85. EP3038066A1: https://patents.google.com/patent/EP3038066A1/en
86. WO2017155485A1: https://patents.google.com/patent/WO2017155485A1/en
87. CN109035660B: https://patents.google.com/patent/CN109035660B/en
88. WO2015121833A1: https://patents.google.com/patent/WO2015121833A1/en
89. CN107204057A: https://patents.google.com/patent/CN107204057A/en
90. BR102017012133A2: https://patents.google.com/patent/BR102017012133A2/en
91. GB2503720A: https://patents.google.com/patent/GB2503720A/en
92. US20180374327A1: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20180374327
93. Sensormatic, blog sobre self-checkout seguro: https://www.sensormatic.com/pt_br/resources/ar/2023/secure-retail-self-checkout-blog

## Não verificado

- Patentes que não abriram na conferência: WO2024042478A1 (Free Sesame Ltd), CN106056822A (Lupuda), WO2025125078A1 (rapitag, alocação entre etiqueta e mercadoria) e CN206805732U (South China University of Technology).
- Motivo da falência da rapitag e da venda da Zliide.
- Como funciona o "sem baixar app" anunciado pela Sensormatic com a Zliide em 2023, e se chegou a alguma loja.
- Se a Touchtech continua vendendo as etiquetas da Zliide.
- Clientes da Zliide citados nas buscas (Moss Copenhagen, Perry Ellis, Quint).
- Desfecho do recurso da Samsung no INPI e existência de pedidos brasileiros da Sensormatic (falta busca no INPI).
- Como a Riachuelo retira o alarme no self-checkout e se "caixa mobile" quer dizer o celular do cliente. Vale perguntar ao contato da Riachuelo.
- Falha no self-checkout da Zara no Pátio Higienópolis em 2025 (cliente retido depois de pagar).
- Geladeiras da market4u que destravariam por Bluetooth depois do pagamento.
- Valor captado pela QueueHop (o número do CB Insights pode incluir a Caper).
- Datas de administração provisória e de abertura do processo da rapitag.
