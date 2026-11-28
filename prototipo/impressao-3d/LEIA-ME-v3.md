# Protótipo v3 (compacto): o que cortar, imprimir e montar

Esta é a versão a usar. Gerada por `tagandgo_v3.py`, que simula todas as peças que se mexem e confere que nada bate.
O mecanismo é o mesmo da v2 (mesmas peças impressas); muda a caixa.

## Caixa

- MDF 3 mm. Interna 224 × 86 × 68,5 mm. Externa 230 × 92 × 71,5 mm (+ 9 mm de tampa na versão A, + 3 mm na B).
- **Embaixo:** receptor Qi no fundo, power bank deitado por cima.
  - USB do power bank virado para o vão vazio de 40 mm na ponta esquerda (ali fica o plugue do cabo).
  - Micro-USB virado para a parede da frente, onde sobra uma faixa de 14 mm para o rabicho do receptor Qi.
- **Prateleira:** chapa de MDF de 224 × 86 mm, apoiada nos 4 pés impressos (C4, 17 mm de altura), colados no fundo fora do power bank. O furo da prateleira deixa o cabo USB subir.
- **Em cima da prateleira:** mecanismo (servo e trilho) no meio, ESP32 com expansor na ponta direita.
- **Em cima da tampa:** semáforo preso por 2 pinos impressos (C6); os fios descem pelo rasgo.
- **Chave fim de curso:** na A, colada no suporte da peça A1, embaixo do gancho (a garra fechada aperta a alavanca 1 mm). Na B, em cima da tampa, no suporte B6, com a ponteira B7 encaixada na alavanca; a cabeça do pino aperta a alavanca 1,2 mm. Nas duas, o ESP32 fica sabendo que a roupa foi presa.
- **Tampa:** presa por 2 pinos impressos (C5) que entram nos cantos (C3). Sem parafusos.
- **Base Qi HyperX:** ela tem 2 áreas de carga e um ressalto no meio. A caixa fica **atravessada sobre uma das áreas**, com o ressalto para fora. O receptor Qi fica embaixo do centro do power bank e precisa cair em cima da bobina daquela área. Se a caixa ficar ao comprido sobre a base, apoia no ressalto e não carrega.
- Ligações pino a pino: `prototipo/LIGACOES.md`.
- **Montagem:** o fundo e a prateleira ficam dentro das paredes, e as paredes curtas ficam entre as longas.

## Arquivos

| | Versão A (garra com dentes) | Versão B (etiqueta de loja + ímãs) |
|---|---|---|
| MDF | `mdf/caixa_v3_A.svg`: 3 tampas (colar na ordem 3, 2, 1 de baixo para cima), prateleira, fundo, 4 paredes | `mdf/caixa_v3_B.svg`: 1 tampa, prateleira, fundo, 4 paredes |
| PLA (`stl_v3/`) | A1 base do servo, trilho e suporte da chave · A2a + A2b lingueta (colar) · A3 braço · A4 garra · A5 dobradiça · A7 eixo da garra | B5 teste da embreagem (primeiro) · B1 base do servo · B2 braço dos ímãs · B3 cápsula · B4 anel · B6 suporte da chave · B7 ponteira da alavanca |
| Comuns | C1 calços do servo · C3 cantos da tampa · C4 pés da prateleira · C5 pinos da tampa · C6 pinos do semáforo | igual |

Ender (Cura): PLA, bico 0,4, camada 0,2, 20 %, 3 paredes, sem suporte.

## Funcionamento

- **A:**
  1. A garra fecha e os 4 dentes empurram o pano para dentro dos furos.
  2. A garra aperta o pino da chave e o ESP32 recebe o sinal.
  3. O servo vai a 40° e a biela empurra a lingueta para dentro do entalhe do gancho: travado.
  4. Depois do pagamento, o servo vai a 90° e a lingueta recua 4,6 mm. O cliente levanta a garra.
- **B:**
  1. O pino da etiqueta trava na embreagem dentro da cápsula.
  2. Depois do pagamento, o servo gira 120° e leva 2 ímãs 15 × 5 até 0,2 mm embaixo do fundo da cápsula, e o pino solta.

## Medir antes de imprimir

1. **Servo:** altura do topo do braço plástico acima da base da orelha (máximo 17 mm; se for menos, usar calços).
2. **Chave fim de curso:** altura da alavanca.
3. **Receptor Qi:** tamanho da folha e comprimento do rabicho.
4. **Versão B:** tamanho da embreagem (imprimir o B5 primeiro).
5. **Cabo USB:** do power bank ao ESP32 (USB-A para USB-C). Dá cerca de 25 cm, passando pelo furo da prateleira.

## Só o que foi comprado

| Comprado | Onde entra |
|---|---|
| ESP32 DevKit (2) | 1 no expansor; 1 de reserva |
| Expansor ESP32 | na prateleira; recebe todos os fios |
| SG90 (3) e MG90S (1) | 1 SG90 no berço; os outros de reserva (o MG90S encaixa no mesmo berço) |
| Chave fim de curso (3) | 1 no suporte da A1 (versão A); 2 de reserva |
| Semáforo LED (2) | 1 em cima da tampa; 1 de reserva |
| Jumpers fêmea-fêmea | semáforo (4), chave (2), capacitor (2) |
| Jumpers macho-fêmea | reserva (não precisa) |
| Capacitor 1000 µF (2) | 1 no V/G do GPIO 12; 1 de reserva |
| Power bank ELG | embaixo da prateleira |
| Receptor Qi | embaixo do power bank, sobre a bobina da base |
| Base Qi HyperX | embaixo da caixa |

Fora da compra, só consumíveis: cola branca, cola quente, PLA e MDF do laboratório e o cabo de celular para ligar o power bank no expansor.
A versão B precisa de compra extra: etiquetas de loja e ímãs 15 × 5 N50.
