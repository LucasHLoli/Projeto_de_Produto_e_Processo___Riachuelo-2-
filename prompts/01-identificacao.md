# PARTE 01 — IDENTIFICAÇÃO
## Como o celular sabe qual peça é?

---

## 0. Papel

Você é engenheiro de aplicação de RFID/NFC. Sua tarefa é especificar, comprar e testar os
**dois rádios passivos** que vão na etiqueta: um que o **celular do cliente** lê, e outro que
o **pórtico da saída** lê. Nenhum dos dois usa energia própria.

---

## 1. Contexto mínimo (autossuficiente)

O projeto elimina a fila do caixa: o cliente lê a etiqueta antifurto da peça com o celular,
paga no app e destrava a etiqueta numa estação de autoatendimento.

Para isso a etiqueta precisa se identificar em **duas situações diferentes**, que exigem
tecnologias diferentes:

| Situação | Distância | Quem lê | Tecnologia |
|---|---|---|---|
| Cliente encosta o celular | 1–3 cm | smartphone | **NFC 13,56 MHz** |
| Cliente passa pelo pórtico | 1–3 m | leitor fixo | **UHF RFID 915 MHz** |

São faixas de frequência e físicas diferentes. **Não existe um chip só que faça bem os dois
casos ao custo desejado** — por isso a etiqueta leva dois adesivos.

---

## 2. Você recebe

De `CONTRATOS.md`:
- formato do `item_id` (EPC-96, 24 hex);
- o payload NDEF: URL única `https://tagandgo.app/i/<item_id>`;
- requisito de alcance UHF: ≥ 1,0 m.

Da parte 03: o espaço disponível dentro da carcaça — **peça esse número antes de comprar
o inlay UHF**, porque inlays longos não cabem.

---

## 3. Você entrega

1. **Especificação de compra** dos dois componentes: chip, tamanho, quantidade, fornecedor, preço.
2. **Arquivo NDEF** gravado e testado.
3. **Relatório de compatibilidade**: leitura testada em pelo menos **6 celulares diferentes**
   (Android e iPhone, modelos antigos e novos).
4. **Curva de alcance UHF** medida: distância de leitura × orientação da etiqueta.
5. **Ensaio de degradação**: a leitura ainda funciona com a etiqueta encostada em tecido? em
   metal (arara)? com várias etiquetas juntas?
6. Especificação do **QR Code** de contingência.
7. Texto para `2-conteudo/3-proposta.tex`.

---

## 4. Restrições

- O NFC e o QR **codificam exatamente a mesma URL**. Sem exceção.
- A etiqueta é **pública e burra**: qualquer um pode ler, e ler não autoriza nada. Nunca
  grave preço, chave ou `tag_id` no NDEF.
- Componentes passivos apenas. Se sua solução precisar de bateria, está errada.
- Custo alvo somado dos dois rádios: **≤ R$ 5 por etiqueta**. `[COTAR]`

---

## 5. Método passo a passo

### 5.1 Escolha e compra

**NFC — leitura pelo celular**

| Requisito | Valor |
|---|---|
| Norma | NFC Forum Type 2, ISO 14443-A |
| Chip sugerido | NTAG213 (180 bytes de usuário — sobra para a URL) |
| Formato | adesivo circular Ø 25 mm |
| Quantidade | comprar **20** (vai perder alguns nos testes) |
| Preço esperado | R$ 1–3 cada `[COTAR]` |

**UHF — leitura pelo pórtico**

| Requisito | Valor |
|---|---|
| Norma | EPC Gen2 / ISO 18000-6C, faixa 902–928 MHz (**Brasil, ANATEL**) |
| Formato | inlay adesivo, **comprimento ≤ 70 mm** — confirmar com a parte 03 |
| Quantidade | comprar **20** |
| Preço esperado | R$ 0,50–2 cada `[COTAR]` |

> **Armadilha:** inlays UHF vendidos para o mercado europeu são sintonizados em 868 MHz e
> perdem alcance em 915 MHz. Confirme a faixa antes de comprar.

### 5.2 Gravação do NDEF

1. Grave um registro **URI** único: `https://tagandgo.app/i/<item_id>`.
2. Aplicativo de gravação: qualquer leitor NFC de Android com função de escrita.
3. **Não** trave (*lock*) as primeiras etiquetas — você vai querer regravar durante os testes.
   Trave só as da demonstração final.
4. Confira que a URL cabe: NTAG213 tem 180 bytes de usuário; a URL da §2 usa ~45.

### 5.3 Ensaio de compatibilidade

Teste em **no mínimo 6 celulares**, variando fabricante e idade. Para cada um, registre:

| Campo | O que anotar |
|---|---|
| Modelo e versão do sistema | ex. Android 13, iOS 17 |
| Tem NFC? | sim/não |
| Abriu a URL **sem app instalado**? | sim/não |
| Distância máxima de leitura | mm |
| Onde fica a antena NFC no aparelho | topo / centro / base |

> **Fato que muda o projeto:** iPhones a partir do XS leem NDEF em segundo plano, sem app.
> iPhones anteriores, e vários Android básicos, **não leem** ou exigem app aberto. Meça, não
> confie na especificação. Se a taxa de sucesso for baixa, o **QR vira o caminho principal e
> o NFC vira o diferencial** — e essa conclusão precisa aparecer no relatório.

### 5.4 Ensaio de alcance UHF

Precisa do leitor da parte 04. Se ele ainda não chegou, **faça os testes de NFC primeiro** e
deixe este para depois — não fique parado.

Meça a distância de leitura em quatro condições:

1. etiqueta no ar, de frente para a antena;
2. etiqueta girada 90°;
3. etiqueta encostada em tecido dobrado;
4. etiqueta encostada em arara metálica ← **é aqui que a leitura costuma cair para quase zero**.

E com **10 etiquetas juntas**, simulando uma sacola: quantas o leitor enxerga de uma vez?

### 5.5 QR de contingência

- Mesma URL do NDEF.
- Nível de correção de erro **M** ou **Q** (a etiqueta sofre atrito e sujeira).
- Lado mínimo 20 mm; teste leitura a 15 cm com celular de câmera fraca.
- Especifique **onde** ele fica impresso na carcaça (combine com a parte 03).

---

## 6. Perguntas que seu entregável precisa responder

1. Qual chip NFC e qual inlay UHF, com fornecedor e preço?
2. Em que fração dos celulares testados o NFC funcionou sem app?
3. Qual o alcance UHF real, na pior orientação e encostado em metal?
4. Quantas etiquetas o leitor enxerga simultaneamente?
5. NFC é o caminho principal ou o QR é? **Responda com base no ensaio, não na expectativa.**
6. Custo somado dos rádios por etiqueta.

---

## 7. Critérios de aceite

- [ ] Componentes comprados, não só escolhidos no catálogo.
- [ ] NDEF gravado e lido com sucesso em pelo menos 6 celulares distintos.
- [ ] Tabela de compatibilidade preenchida por modelo.
- [ ] Alcance UHF medido nas 4 condições, incluindo encostado em metal.
- [ ] Ensaio com 10 etiquetas simultâneas feito.
- [ ] QR especificado e testado.
- [ ] Comprimento do inlay confirmado como compatível com a carcaça da parte 03.
- [ ] Custo por etiqueta apurado e dentro de R$ 5.

---

## 8. O que NÃO fazer

- Não projete antena. Compre inlay pronto — projeto de antena UHF é trabalho de meses.
- Não use NFC para o pórtico. O alcance de 13,56 MHz é de centímetros; não existe truque.
- Não grave dado sensível no NDEF. A etiqueta é lida por qualquer estranho no provador.
- Não compre inlay de 868 MHz.
- Não escolha o inlay antes de saber o espaço interno da carcaça (parte 03).
- Não implemente o app — isso é da parte 02. Você entrega a URL funcionando, ela consome.
