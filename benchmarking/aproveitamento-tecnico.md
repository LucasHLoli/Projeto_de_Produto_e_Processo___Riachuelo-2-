# Tag&Go: benchmarking e aproveitamento técnico

Relatório 2, item D. Grupo 4, PRO3474, parceria Riachuelo. Pesquisa feita em set/2026.

## 1. Método

- Seis linhas de similaridade: (1) antifurto de varejo e suas patentes; (2) liberação pelo celular depois do pagamento; (3) travas de compartilhamento (bicicleta, patinete, power bank, armários de encomenda); (4) etiquetas eletrônicas de prateleira e rastreadores; (5) ativos retornáveis (etiquetas recirculadas, cabides, paletes, garrafas); (6) jornada do cliente na loja.
- Mais de 60 produtos, serviços e patentes, levantados em sites de fabricantes, Google Patents e imprensa especializada.
- Cada referência foi lida pelas funções do Tag&Go: como realiza, desempenho, o que aproveitar e o que não serve.
- Critério de aproveitamento: o princípio resolve uma função do Tag&Go, cabe no MVP ou no produto final e tem evidência (produto em uso, patente ou número publicado).

## 2. Matriz função x produto

| Função | Referência 1 | Referência 2 | Referência 3 | Referência 4 |
|---|---|---|---|---|
| Reter a peça e resistir a arrancamento | Hard tag Sensormatic (patente US7148805B2, expirada; família do SuperTag, "grampo patenteado"): pino ranhurado preso por grampo; 80 a 125 lbf (356 a 556 N) de arrancamento. A patente não cita o nome SuperTag, e o site não publica força | Patente US10121338 (Sensormatic): pino cativo, lingueta e mola; o solenoide só dispara | LimeLock (Lime) e Spider Wrap (Checkpoint): laço de cabo de aço | RFID da Zara (Inditex): sem retenção física; ladrões arrancaram os chips (contraexemplo) |
| Identificar a peça e iniciar a compra | NTAG 424 DNA (NXP): NFC que gera URL única a cada toque | Zliide: compra no app Zliide e etiqueta liberada por Bluetooth (RFID Journal, 2021); em 2023 a Sensormatic anunciou a versão sem download de app, sem detalhar como funciona | Renner: RFID em cada peça, lido em lote no quiosque | MishiPay: QR abre página web, sem download |
| Pagar e autorizar sem caixa | Patente Samsung BR US10586228: servidor libera a chave da etiqueta só após o pagamento; celular leva a chave | DHL Packstation (EP3410410): desafio-resposta via BLE; armário funciona offline | Patente Checkpoint US7450013 (expirada): estado por etiqueta no banco e log de cada liberação | rapitag: token único criptografado entregue por BLE |
| Liberar a retenção | Pedido Checkpoint US20070205902 (caducado): solenoide solta embreagem pré-carregada por mola | Kohl's e Sensormatic: detacher automático que recolhe pino e corpo | Patente Vbikes US10360745: só libera com celular a 10 a 20 cm | nextbike: se a trava não abre em 3 min, cancela e estorna |
| Indicar estado e alertar | Mini Alarming Lanyard (Sensormatic): 2 bipes = travou; pisca a cada 14 s = armada; alarme em 2 s se não travou | Alpha XT (Checkpoint): sirene de 95 dBA na violação e na saída | SoluM e Pricer (etiqueta de prateleira): LED de 7 cores com significado, inclusive bateria fraca e localizar | Bike Itaú (Tembici/PBSC): luz verde e bipe no instante da trava |
| Energia | ofo: pilha primária e supercapacitor para o pico do atuador | OMNI OZ35: LiPo de 700 mAh, 180 dias em espera com BLE | Patente Sensormatic US12101138: sem bateria; pad indutivo energiza só na liberação | Vusion: tela e-paper que dorme e acorda por rádio; até 15 anos de bateria |
| Reutilizar (recolher, recarregar, recadastrar, rastrear) | Recirculação Sensormatic: 2,5 bilhões de etiquetas em 2 anos; crédito por etiqueta devolvida (não verificado) | Cabides Mainetti e Braiform: coleta na loja, triagem central, volta com a reposição; 9 reusos em média | ChargeSPOT: o slot trava, identifica e recarrega; cobrança de €30 pré-autorizada se não devolver em 48 h | Brambles CHEP: serialização individual dos paletes (Serialisation+, já total no Chile, em teste na América do Norte e no Reino Unido) e rastreadores; perdas não compensadas ~50% menores que em FY21, pelo conjunto de ações de controle de ativos |
| Atendimento humano e liberação assistida | InVue OneKEY: credencial digital do funcionário, validade de até 24 h, revogação e log | Renner Pague Digital: cliente escaneia e paga no app e mostra o comprovante ao colaborador, que libera as peças | Clique Retire: reabertura em 60 s sem novo custo; suporte por WhatsApp | Market4u: revisão remota do alerta e cobrança posterior por link |
| Jornada do cliente | Zara Store Mode: estoque da loja em tempo real e localização da peça | Walmart e Home Depot: endereço de corredor casado com placa física | Nike Member Pass e Sephora: vínculo de fidelidade e coletor com pontos | Vusion ESway (L&T): etiqueta eletrônica por peça, localizada na loja |

## 3. Ideias a aproveitar

| Função | Ideia | De onde vem | Como entra no Tag&Go | Fonte |
|---|---|---|---|---|
| Reter a peça | Meta de arrancamento de pelo menos 356 N (80 lbf), verificada em ensaio de tração | Hard tag Sensormatic (patente US7148805B2, que dá 80 a 125 lbf; não cita o nome SuperTag) | MVP: ensaiar a caixa atual. Final: requisito na casa da qualidade | [link](https://patents.google.com/patent/US7148805B2/en) |
| Reter e liberar | Solenoide só como gatilho de uma trava pré-carregada por mola, com pino cativo | Checkpoint (US20070205902A1, livre); Sensormatic (US10121338B2, vigente) | Final: mecanismo compacto. O MVP já segue o princípio (fechadura push-to-lock) | [link](https://patents.google.com/patent/US20070205902A1/en) |
| Liberar e indicar estado | Sensor de posição do pino (Hall ou microchave); a venda só fecha quando a etiqueta confirma que abriu | OMNI OZ35; Bike Itaú (PBSC); nextbike | MVP: microchave no ESP32 reportando ao servidor | [link](https://www.omnismartiot.com/Smart-Lock/OZ35-cable-lock-for-micromobility.html) |
| Pagar e autorizar | Código de uso único emitido pelo servidor após o pagamento, levado pelo celular via BLE e validado na própria etiqueta, sem Wi-Fi | DHL Packstation (EP3410410A1); Amazon Hub Locker (US11600125B1); Samsung BR (US10586228B2) | MVP: token assinado e com validade no lugar do comando simples ao relé. Final: BLE | [link](https://patents.google.com/patent/EP3410410A1/en) |
| Pagar e autorizar | Estado de cada etiqueta no servidor (associada, paga, liberada, devolvida, em recarga); libera só se a etiqueta pertence à peça paga; log de tudo | Checkpoint (US7450013B2, expirada em 2025) | MVP: no servidor e no painel atuais | [link](https://patents.google.com/patent/US7450013B2/en) |
| Identificar a peça | NFC com URL que muda a cada toque, para impedir o uso de foto do QR; QR fica como alternativa | NTAG 424 DNA, NXP | Final | [link](https://www.nxp.com/products/rfid-nfc/nfc-hf/ntag-for-tags-and-labels/ntag-424-dna-424-dna-tagtamper-advanced-security-and-privacy-for-trusted-iot-applications:NTAG424DNA) |
| Identificar e pagar | Fluxo sem app: QR abre página web; várias peças numa sessão e um pagamento só | MishiPay; IKEA Scan & Go; geladeiras RedGo e Gela Smart (Pix por QR, sem app) | MVP: página web servida pelo servidor atual | [link](https://mishipay.com/scan-go-solution/) |
| Indicar estado | Linguagem de sinais: travou, armada, não travou, liberada, bateria fraca, localizar; sirene de cerca de 95 dBA na violação | Mini Alarming Lanyard (Sensormatic); Alpha XT (Checkpoint); Newton Pro (SoluM) | MVP: LED de cores e buzzer. Final: sirene | [link](https://docs.johnsoncontrols.com/sensormatic/api/khub/documents/DdXjy5eexQnxgaVw3SpH4g/content) |
| Indicar estado e alertar | Marcador passivo AM/RF ou RFID dentro da etiqueta: dispara o portal que a loja já tem, mesmo com a bateria morta | Gen7 dual (Checkpoint); Synergy (Sensormatic); Renner | Final | [link](https://www.checkpointsystems.ca/en/10141983) |
| Energia | Etiqueta que dorme e acorda por rádio; célula interna ou pilha com supercapacitor no lugar do power bank; autonomia declarada como "N liberações + D dias" | Vusion; teardown ofo; OMNI OZ35; AirTag (Apple) | MVP: medir consumo por liberação. Final: nova arquitetura de energia | [link](https://hackaday.com/2018/07/27/share-bike-surrenders-its-secrets-to-a-teardown/) |
| Reutilizar | Urna ou rack de devolução que lê o ID, dá baixa na frota e recarrega por contato | ChargeSPOT (INFORICH); patente EP4060854A1; Kohl's (US11417186B2) | MVP: urna simples e leitura do QR no painel. Final: rack com recarga | [link](https://eu.chargespot.global/en/faq) |
| Reutilizar | Ciclo fechado loja, CD, recondicionamento e reposição; urna sem triagem na loja; checklist de aceite | Recirculação Sensormatic; Pact e Prosegur; Mainetti Hangerloop | Final: aproveita a Riachuelo ser verticalizada (associação na fábrica ou no CD) | [link](https://www.mainetti.com/hangerloop/) |
| Reutilizar | Incentivo à devolução (pontos ou cashback) e indicador de perda por loja no painel | Garrafa Universal Coca-Cola (mais de 90% de retorno); Sephora; Brambles | MVP: indicador no painel. Final: pontos no Cartão Riachuelo/Midway | [link](https://www.ellenmacarthurfoundation.org/pt/exemplos-circulares/embalagem-desenhada-reutilizacao-diversas-marcas-garrafa-universal) |
| Atendimento humano | Credencial digital do funcionário (PIN, validade curta, revogação, log); botão "chamar ajuda" com o ID da etiqueta; estorno automático se a etiqueta não abrir | InVue OneKEY; C&A; nextbike | MVP: botão na página e liberação pelo painel com login | [link](https://invue.com/onekey-ecosystem) |
| Jornada do cliente | Página da etiqueta mostra outros tamanhos na loja, onde devolver a etiqueta e quantas vezes ela já foi reutilizada | Zara Store Mode; Walmart Store Map; EON/Passaporte Digital de Produto | MVP: tela estática com o ponto de devolução. Final: estoque em tempo real | [link](https://www.zara.com/nz/en/help-center/StoreMode) |

## 4. O que não aproveitar

1. Liberação por ímã externo: exige ponto fixo e é frágil, porque destacadores genéricos são vendidos na internet por US$ 13 a 125 (faixa de preço não verificada).
2. App nativo obrigatório e pareamento Bluetooth manual (Zliide, rapitag, Renner, Amazon Style): geram atrito. A rapitag entrou em insolvência em 2025 (detalhes em concorrentes-diretos.md). A Zliide Technologies faliu em 2025 e teve marca, patentes e software comprados pela Touchtech por valor simbólico (jul/2025); as duas lojas Amazon Style fecharam em nov/2023.
3. Etiqueta só RFID, sem retenção física (Zara): os chips foram achados e arrancados. É o argumento para manter a trava.
4. GPS, modem celular, painel solar ou dínamo em cada unidade (Mobike, OMNI): caros, grandes e inúteis dentro da loja.
5. Abertura automática ao chegar perto (geocerca da patente Amazon): liberaria sem intenção ou a etiqueta errada. O Tag&Go precisa de gesto explícito.
6. Verificação por selfie ou biometria facial (CLEAR, C&A Pay): pesada demais para compra de roupa e exige cuidado com a LGPD.

## 5. Três destaques que mais mudam o projeto

**1. Cadeado de bicicleta compartilhada e armários de encomenda como análogo da trava e da frota** (Bike Itaú/PBSC, nextbike, Lime, Amazon Hub Locker, DHL Packstation). A lógica é a do Tag&Go: fecha por ação mecânica, abre por comando autorizado e a transação só termina quando o dispositivo confirma o estado. Muda o projeto em três pontos:
- sensor de posição do pino, que o MVP não tem (hoje ele só manda o pulso);
- autorização como código de uso único levado pelo celular via BLE e validado na etiqueta, que dispensa Wi-Fi e funciona com rede ruim (a estação offline é a falha mais citada da Tembici, não verificado);
- frota com status e tensão da bateria a cada evento, bloqueando etiquetas com carga baixa, e caminhos de falha prontos (código curto, estorno automático após timeout).

**2. Cabides Mainetti/Braiform e etiquetas recirculadas Sensormatic como análogo da logística reversa.** Mais de 1 bilhão de cabides reusados por ano só na Braiform, 9 reusos por cabide em média, 2,5 bilhões de etiquetas recirculadas pela Sensormatic em 2 anos e taxas de reuso acima de 90% em muitos casos (Pact). Muda o projeto porque a reutilização deixa de ser tarefa da loja: urna sem triagem, retorno no caminhão de reposição, recondicionamento no CD (recarga, teste, recadastro) e crédito por devolução (este último é proposta do grupo; não achamos crédito publicado nos programas citados). Como a Riachuelo é verticalizada, a etiqueta pode ser associada à peça na fábrica ou no CD. Conta do grupo: para durar 100 ciclos, a perda precisa ficar abaixo de 1% por ciclo, o que exige rastreio individual (como a Brambles faz com paletes) e incentivo ao cliente.

**3. Etiqueta eletrônica de prateleira (e-paper) como análogo da indicação de estado e da bateria longa** (Vusion, SoluM, Pricer; hangtag ESway na L&T). Duram anos porque dormem e só gastam energia ao mudar de estado. O MVP faz o contrário: ESP32 com Wi-Fi ligado e power bank (20 a 68 mA em modem-sleep contra 10 µA em deep-sleep, pelo datasheet). Muda o projeto: rádio que acorda a etiqueta, energia gasta só no pulso do solenoide, autonomia especificada como "N liberações + D dias", LED com cores padronizadas (inclusive bateria fraca e localizar) e frota gerida pela nuvem com localização. O ESway mostra que uma etiqueta eletrônica por peça de roupa já funciona com cerca de 20 mil itens.

Atenção: há patentes vigentes nos EUA que cobrem de perto o conceito (Sensormatic US10121339 e US10121338, até 2035/2036, e US12101138, até 2040; Samsung BR US10586228, até 2034). É preciso ler as reivindicações e buscar equivalentes no INPI antes do projeto detalhado.

## 6. Parágrafo para o relatório

O estudo de aproveitamento técnico partiu de um benchmarking comparativo organizado em seis linhas de similaridade: dispositivos antifurto de varejo e suas patentes, soluções de liberação pelo celular após o pagamento, travas de sistemas de compartilhamento, etiquetas eletrônicas e rastreadores, ativos retornáveis e serviços de jornada do cliente na loja. Mais de sessenta referências foram analisadas segundo as funções do Tag&Go, registrando-se o princípio de solução, o desempenho disponível, o que pode ser aproveitado e o que não se aplica. Na retenção, constatou-se que as etiquetas comerciais prendem o pino por meio mecânico passivo e usam o elemento ativo apenas para soltar, o que confirma o princípio da fechadura do protótipo e fornece uma meta de arrancamento de 356 N. Na autorização, travas de bicicletas compartilhadas e armários de encomendas mostraram que a validação pode ocorrer na própria etiqueta, com um código de uso único emitido pelo servidor após o pagamento e transportado pelo celular via Bluetooth, dispensando Wi-Fi na etiqueta, e que a transação deve ser encerrada somente após a confirmação da liberação por um sensor de posição do pino. As etiquetas eletrônicas de prateleira indicaram que autonomias de anos decorrem de permanecer em repouso e despertar apenas por comando de rádio, o que orienta a substituição do power bank por uma célula interna e a adoção de uma linguagem padronizada de cores e sinais sonoros. Na reutilização, os programas de recirculação de etiquetas rígidas e de cabides demonstraram a viabilidade de um ciclo fechado entre loja, centro de distribuição e reposição; como a etiqueta eletrônica tem custo elevado, a perda por ciclo precisa ser inferior a um por cento para amortizá-la em cem usos, o que exige rastreamento individual e incentivo à devolução. Para o atendimento assistido, adotou-se o modelo de credencial digital do funcionário, com validade limitada e registro das liberações. Foram descartados a liberação por ímã externo, o aplicativo nativo obrigatório, a etiqueta sem retenção física e os módulos de localização por satélite. Identificaram-se ainda patentes vigentes nos Estados Unidos sobre etiquetas autodestacáveis por comando sem fio, cujos equivalentes no Brasil deverão ser verificados junto ao INPI antes do projeto detalhado.

## 7. Fontes

Antifurto de varejo
1. Hard Tags (páginas de produto). Sensormatic Solutions, 2026. https://www.sensormatic.com/loss-prevention-liability/merchandise-protection/hard-tags
2. US7148805B2 (patente de hard tag, prioridade 2003). Sensormatic. https://patents.google.com/patent/US7148805B2/en
3. Gen7 Hard Tag with pin, RF and RFID (10141983). Checkpoint Systems, 2026. https://www.checkpointsystems.ca/en/10141983
4. XT 2-Alarm Hard Tag (10102826). Checkpoint Systems, 2026. https://www.checkpointsystems.ca/en/10102826
5. Mini Alarming Lanyard Tag Series, User Guide Rev. E. Sensormatic, 2014. https://docs.johnsoncontrols.com/sensormatic/api/khub/documents/DdXjy5eexQnxgaVw3SpH4g/content
6. US7450013B2, System and method for authenticated detachment of product tags. Checkpoint Systems, 2008. https://patents.google.com/patent/US7450013B2/en
7. US20070205902A1, RF release mechanism for hard tag. Checkpoint Systems, 2007. https://patents.google.com/patent/US20070205902A1/en
8. US10121339B2, Self-detaching anti-theft device for retail environment (ver também US9978236B2 e US11263882B2). Sensormatic, 2018. https://patents.google.com/patent/US10121339B2/en
9. US10121338B2, Self-detaching anti-theft device (ver também US12101138B2 e US9460597B1). Sensormatic, 2018. https://patents.google.com/patent/US10121338B2
10. Sensormatic collaborates with Zliide to reimagine self-checkout (NRF 2023). Sensormatic e Zliide, 2023. https://www.sensormatic.com/resources/pr/2023/nrf-2023-zliide
11. US11417186B2, Device for automated removal of security tags. Kohl's, 2022. https://patents.google.com/patent/US11417186B2/en
12. Detection Systems (pedestais EAS). Sensormatic, 2026. https://www.sensormatic.com/loss-prevention-liability/eas/detection-systems
13. Zara finds shoplifters able to outsmart its new security system. FashionNetwork/Bloomberg, 2023. https://us.fashionnetwork.com/news/Zara-finds-shoplifters-able-to-outsmart-its-new-security-system,1555246.html

Liberação pelo celular
14. Transforming Retail: rapitag's Pilot Program Proves Successful. rapitag (EuroCIS), 2024. https://www.eurocis-tradefair.com/en/Visit/What_to_expect/Exhibitor_News/Transforming_Retail_rapitag%60s_Pilot_Program_Proves_Successful
15. US10586228B2, Method for secure mobile payment and RF tag with integrated anti-theft device. Samsung Eletrônica da Amazônia, 2020. https://patents.google.com/patent/US10586228B2
16. Born out of Covid, Paytag wants to change how we shop in-store. Ctech/Calcalist, 2026. https://www.calcalistech.com/ctechnews/article/5i583v2fg
17. MishiPay Scan & Go. MishiPay, 2023. https://mishipay.com/scan-go-solution/
18. Lojas Renner Raises Customer Approval with RFID. RFID Journal, 2023. https://www.rfidjournal.com/news/lojas-renner-raises-customer-approval-with-rfid/199247/
19. Riachuelo revela loja pop-up em SP que servirá de modelo para mais de 300 unidades. Mercado&Consumo, 2025. https://mercadoeconsumo.com.br/08/12/2025/noticias/riachuelo-revela-loja-pop-up-em-sp-que-servira-de-modelo-para-mais-de-300-unidades-da-rede/
20. Market4U reduz índice de furtos com algoritmo de IA. Convergência Digital, 2023. https://convergenciadigital.com.br/inovacao/market4u-reduz-ndice-de-furtos-com-algoritmo-de-inteligncia-artificial-ia/
21. CLEAR and InVue Unlock Secure Self-Service Retail. CLEAR e InVue, 2026. https://identity.clearme.com/post/invue-and-clear-partnership-announcement
21a. OneKEY Ecosystem (chave digital do funcionário, validade de até 24 h, desativação em tempo real, auditoria). InVue, 2026. https://invue.com/onekey-ecosystem
21b. Touchtech Acquires Rare Competitor Zliide. MarketScreener, 2025. https://www.marketscreener.com/quote/stock/TOUCHTECH-AB-149016198/news/Touchtech-Acquires-Rare-Competitor-Zliides-No-Staff-Transition-Involved-50503076/
21c. Amazon to close apparel stores in latest physical retail strategy shift. CNBC, 2023. https://www.cnbc.com/2023/11/02/amazon-to-close-apparel-stores-in-physical-retail-strategy-shift.html

Compartilhamento
22. Como usar a Bike Itaú. Tembici, 2026. https://bikeitau.com.br/como-usar/
23. Bikes & Smart Stations. Lyft Urban Solutions (PBSC), 2026. https://lyfturbansolutions.com/bikes-smart-stations
24. Share Bike Surrenders Its Secrets To A Teardown (ofo). Hackaday, 2018. https://hackaday.com/2018/07/27/share-bike-surrenders-its-secrets-to-a-teardown/
25. US10360745B2, Smart lock for shared-ride bicycle. Vbikes Technology, 2019. https://patents.google.com/patent/US10360745B2/en
26. Lime's new e-bike has a swappable battery. TechCrunch, 2022. https://techcrunch.com/2022/01/12/lime-new-e-bike-swappable-battery-works-with-scooters
27. OZ35 Cable Lock for Micromobility. OMNI, 2026. https://www.omnismartiot.com/Smart-Lock/OZ35-cable-lock-for-micromobility.html
28. FAQ. nextbike, 2026. https://www.nextbike.de/en/faq/
29. ChargeSPOT FAQ. INFORICH, 2026. https://eu.chargespot.global/en/faq
30. EP4060854A1, Power bank rental apparatus. Shenzhen Zhumang Technology, 2022. https://patents.google.com/patent/EP4060854A1/en
31. US11600125B1, Autonomous device authentication and compartment unlocking. Amazon, 2023. https://patents.google.com/patent/US11600125B1/en
32. EP3410410A1, Locker system access control. Deutsche Post DHL, 2021. https://patents.google.com/patent/EP3410410A1/en
33. Perguntas Frequentes. Grupo Clique (Clique Retire), 2026. https://www.cliqueretire.com.br/perguntas-frequentas-faq/

Etiquetas eletrônicas e rastreadores
34. Electronic Shelf Labels. VusionGroup, 2026. https://www.vusion.com/products/sesimagotag/electronic-shelf-labels/
35. L&T Fashion Warehouse Pilots the Digital Future of Fashion Retail (ESway). GK Software e Vusion, 2026. https://www.gk-software.com/us/corporate-news-and-press-releases/en-press-release-20260224-lut-reta-award
36. Newton Pro. SoluM, 2026. https://www.solum-group.com/esl-n-iot/product-lineup/professional-esl/newton-pro
37. Instant flash. Pricer, 2022. https://www.pricer.com/products/technology/instant-flash
38. Apple introduces new AirTag. Apple, 2026. https://www.apple.com/newsroom/2026/01/apple-introduces-new-airtag-with-expanded-range-and-improved-findability/
39. NTAG 424 DNA and NTAG 424 DNA TagTamper. NXP, 2026. https://www.nxp.com/products/rfid-nfc/nfc-hf/ntag-for-tags-and-labels/ntag-424-dna-424-dna-tagtamper-advanced-security-and-privacy-for-trusted-iot-applications:NTAG424DNA

Retornáveis
40. Hard Tag Recirculation Among Stevie Awards' Sustainability Initiatives. Sensormatic, 2024. https://www.sensormatic.com/resources/ar/2024/hard-tag-recirculation-among-stevie-awards-sustainability-initiatives-of-the-year
41. New Tag Recirculation Program Launched by Prosegur and Pact Group. Loss Prevention Media, 2024. https://losspreventionmedia.com/new-tag-recirculation-program-launched-by-prosegur-and-pact-group/
42. Research From Braiform Highlights Potential Damage of Clothes Hangers. Braiform, 2018. https://www.prnewswire.co.uk/news-releases/research-from-braiform-highlights-potential-damage-of-clothes-hangers-to-the-environment-690222131.html
43. Hangerloop. Mainetti, 2026. https://www.mainetti.com/hangerloop/
44. Brambles FY25 Result. Brambles (CHEP), 2025. https://www.brambles.com/Content/cms/news/2025/Brambles_FY25_Result_ASX___Media_Release.pdf
45. Garrafa universal: embalagem reutilizável para diversas marcas. Ellen MacArthur Foundation (Coca-Cola), 2020. https://www.ellenmacarthurfoundation.org/pt/exemplos-circulares/embalagem-desenhada-reutilizacao-diversas-marcas-garrafa-universal

Jornada do cliente
46. Store Mode In The App. Zara (Inditex), 2026. https://www.zara.com/nz/en/help-center/StoreMode
47. Walmart apps store maps help customers find time and products. Walmart, 2019. https://corporate.walmart.com/news/2019/11/27/walmart-apps-store-maps-help-customers-find-time-and-products-this-holiday-season
48. Scan and pack as you shop. IKEA, 2026. https://www.ikea.com/gb/en/customer-service/mobile-apps/scan-and-pack-as-you-shop-pubc3fed9a0/
49. Tá online, tá na Renner (Pague Digital). Lojas Renner, 2023. https://blog.lojasrenner.com.br/2023/10/ta-online-ta-na-renner/
50. C&A quer elevar experiência do cliente com loja conceito. Meio & Mensagem, 2025. https://www.meioemensagem.com.br/marketing/ca-experiencia-loja-conceito
51. Special In-Store Services for Members. Nike, 2026. https://www.nike.com/membership/in-store-services
52. Sephora Launches Beauty (Re)purposed. Sephora, 2023. https://newsroom.sephora.com/sephora-launches-sustainable-empties-collection-program-beauty-repurposed-to-help-reduce-packaging-waste-%EF%BF%BC/
53. Textile Apparel and the Digital Product Passport. Comissão Europeia, 2026. https://single-market-economy.ec.europa.eu/single-market/digital-product-passport/textile-apparel_en
