// Dados compartilhados pelo desenho 2D (animacao.html) e pelo manual em 3D (simulacao-3d.html).
// Medidas em mm. Origem no canto interno da base: x = comprimento, y = altura, z = largura.
const D = {
  L: 206, W: 72, H: 50, wall: 2, floor: 1.6, lid: 2.4,          // caixa: 210 x 76 x 54 por fora
  qi: {x: 80, z: 19, l: 67, w: 34, h: 1},
  pb: {x: 40, z: 1, l: 150, w: 70, y: 1, h: 18},
  exp: {x: 46, z: 9.25, l: 73, w: 53.5, y: 21},
  esp: {x: 56, z: 21.5, l: 53, w: 29, y: 31.1},
  C: {x: 16, z: 52},                                           // eixo do pino e da embreagem
  A: {x: 16, z: 36}, R: 16,                                    // eixo do servo e raio do braço
  clutch: {r: 6.5, y0: 40.2, y1: 51.2}, shelf: {y0: 39.4, y1: 40.2}, mag: {r: 5, y0: 27.2, y1: 39.2},
  jaw: {hx: 70, hy: 59.4, x0: -2, x1: 66, z0: 38, z1: 70, th: 8, open: .56},
  pin: {len: 16},
  fab: {x0: 34, x1: 64, z0: 40},
  ridL: [46, 52, 58, 64], ridJ: [43, 49, 55, 61, 67],
  slot: {x0: 42, x1: 64, zs: [46, 54, 62], w: 3.6, dip: 5.6},       // variante C: rasgos da tampa e dedos da garra
  jawSw: {x: 27, z: 38, px: 34, pz: 50},
  qr: {cx: 150, cz: 36, s: 34},                                // adesivo do QR colado na tampa
  sem: {x: 186, z: 8.25, l: 13, w: 55.5, cx: 192.5, zs: [21, 36, 51]},
  baseSw: {x: 24, z: 2}
};

const MEDIDAS = [
  ['Caixa (por fora)', '210 × 76 × 54 mm. Com a garra fechada, 65 mm de altura', 'projeto'],
  ['Garra', '68 × 32 × 8 mm, abre cerca de 30°', 'projeto'],
  ['Power bank Basike 10.000 mAh', '150 × 70 × 15 mm no site da marca; 147,5 × 69 × 18 mm na Amazon. Usei 150 × 70 × 18', 'anúncio'],
  ['Receptor de indução USB-C', '67 × 34 × 1 mm, 5 V e 0,5 a 1 A, folga de 2 a 6 mm', 'anúncio'],
  ['Base de indução Lelong LE-520', 'Ø 100 × 8 mm', 'estimativa'],
  ['ESP32 DevKit 30 pinos', '53 × 29 mm, fileiras a 25,8 mm', 'anúncio'],
  ['Expansor de ESP32', '73 × 53,5 × 16 mm, 4 furos M3', 'anúncio'],
  ['Servo SG90', 'corpo 22,7 × 12,1 × 22,6 mm; abas com 32,4 mm; 30,7 mm até o topo do eixo; eixo a 5,8 mm da ponta', 'anúncio'],
  ['Adesivo do QR', '34 × 34 mm, impresso em papel adesivo', 'projeto'],
  ['Chave fim de curso', '25 × 13,7 × 5,8 mm, haste de 13 mm, curso de 2,5 mm', 'anúncio'],
  ['Semáforo de LED', '55,5 × 13 × 13 mm, LEDs de 8 mm a cada 15 mm', 'anúncio'],
  ['Ímã de neodímio', 'Ø 10 × 4 mm, cerca de 2,5 kg de força e 4.500 G na face (dado do N52)', 'anúncio'],
  ['Pino da etiqueta', 'haste de Ø 1,2 mm, cabeça de Ø 12 mm, 16 mm de comprimento', 'anúncio'],
  ['Esferas da embreagem', 'Ø 2,5 mm', 'patente'],
  ['Embreagem (copo de metal)', 'Ø 13 × 11 mm', 'estimativa'],
  ['Força para arrancar o pino', 'cerca de 36 kgf (alvo de projeto de uma patente)', 'patente'],
  ['Destacador de loja comum', '4.500 G', 'anúncio']
];

// O que comprar: [nome, quantidade, preço visto, link, para que serve]. Preços vistos entre 29/09 e 07/10/2026, sem frete.
const COMPRAS = {
  etq: ['Etiquetas rígidas de loja, com pino (pacote com 20)', '1 pacote', 'R$ 67,78', 'https://www.amazon.com.br/dp/B0GP6ZF16R', 'De dentro de uma delas saem a embreagem e o pino. As outras ficam para teste.'],
  ima: ['Ímãs de neodímio N50, 10 × 4 mm (kit com 10)', '1 kit', 'R$ 21,48', 'https://www.usinainfo.com.br/imas-de-neodimio-e-acessorios-magneticos/ima-de-neodimio-n50-super-forte-10mm-x-4mm-kit-com-10-unidades-5012.html', 'Três empilhados abrem a embreagem.'],
  esp: ['ESP32 com USB-C, 30 pinos', '1', 'R$ 56,81', 'https://www.usinainfo.com.br/esp32/esp32-wifi-e-bluetooth-com-usb-c-30-pinos-e-cp2102-9114.html', 'É o computador da caixa. Tem Wi-Fi.'],
  exp: ['Expansor para ESP32 de 30 pinos', '1', 'R$ 21,19', 'https://www.usinainfo.com.br/expansores-shields/expansor-para-esp32-devkit-v1-30-pinos-usb-c-e-micro-8795.html', 'Placa onde o ESP32 encaixa. Dá pinos fáceis para ligar os fios, sem solda.'],
  srv: ['Microservo SG90', '2 (um de reserva)', 'R$ 28,32', 'https://www.usinainfo.com.br/servo-motores/micro-servo-motor-9g-sg90-180-16kgfcm-de-posicao-2299.html', 'Motor pequeno que gira o braço dos ímãs.'],
  chv: ['Módulo chave fim de curso', '2', 'R$ 9,58', 'https://www.usinainfo.com.br/sensor-de-vibracao/modulo-chave-fim-curso-sensor-de-impacto-para-projetos-4618.html', 'Uma sente a garra fechar e a outra sente a base de carga.'],
  sem: ['Semáforo de LED', '1', 'R$ 7,78', 'https://www.usinainfo.com.br/outros-modulos-arduino/semaforo-led-33v5v-8mm-s3-5466.html', 'Os três LEDs: vermelho, amarelo e verde.'],
  jff: ['Jumpers fêmea-fêmea, 20 cm (40 un.)', '1', 'R$ 7,50', 'https://www.eletrogate.com/jumpers-femea-femea-40-unidades-de-20-cm', 'Os fios de encaixe. São usados 10.'],
  jmf: ['Jumpers macho-fêmea, 20 cm (40 un.)', '1', 'R$ 8,46', 'https://www.eletrogate.com/jumpers-macho-femea-40-unidades-de-20-cm', 'Três deles ligam o plugue do servo.'],
  pwb: ['Power bank Basike 10.000 mAh, com visor', '1', 'R$ 95,00', 'https://www.amazon.com.br/dp/B0DHVLRFGD', 'A bateria da caixa.'],
  qir: ['Receptor de indução com plugue USB-C', '1', 'R$ 67,93', 'https://www.magazineluiza.com.br/adaptador-sem-fio-wireless-qi-inducao-receptor-universal-tipo-c-brasil-home/p/gkj66889f8/in/usba/', 'Folha fina que recebe a carga sem fio e passa para o power bank.'],
  qib: ['Base de carregador sem fio Lelong LE-520', '1', 'R$ 28,69', 'https://www.magazineluiza.com.br/carregador-por-inducao-15w-sem-fio-usb-acompanha-cabo-usb-c-le520-lelong/p/ke9dh49dk3/te/accp/', 'Onde a caixa é posta para recarregar.'],
  prf: ['Kit de parafusos e porcas M2 a M5', '1', 'R$ 18,72', 'https://www.amazon.com.br/dp/B0GS5M3LC5', 'Parafusos da tela, do módulo e da tampa.'],
  pla: ['Filamento PLA 1,75 mm, 1 kg', '1', 'cerca de R$ 100', '', 'Plástico da impressora 3D. Qualquer marca e cor.'],
  cap: ['Capacitor eletrolítico de 1.000 µF, 16 V', '1 (opcional)', 'cerca de R$ 2', '', 'Só se o ESP32 reiniciar quando o servo mexe.']
};
const CASA = ['Fita dupla face de espuma', 'Cola instantânea em gel', 'Um pregador de roupa (para tirar a mola)', 'Parafuso M3 de 40 mm com porca (eixo da garra)', 'Tira de borracha: câmara de ar de bicicleta ou fita antiderrapante', 'Cabo USB-C que passe dados (o de carregar celular costuma servir)', 'Adesivo com o QR da caixa: uma folha de papel adesivo e uma impressora comum'];
const FERR = ['Serrinha ou arco de serra', 'Óculos de proteção', 'Chave Philips pequena', 'Paquímetro ou régua', 'Lixa fina', 'Estilete', 'Alicate de bico', 'Notebook com porta USB', 'Celular com câmera'];

// Ligações: [módulo, pino do módulo, destino no expansor, cor em código, nome da cor]
const LIG = [
  ['LEDs', 'GND', 'GND', '#222222', 'preto'], ['LEDs', 'R', 'GPIO 19', '#d32f2f', 'vermelho'], ['LEDs', 'Y', 'GPIO 21', '#f9a825', 'amarelo'], ['LEDs', 'G', 'GPIO 22', '#2e7d32', 'verde'],
  ['Chave da garra', 'VCC', '3V3', '#d32f2f', 'vermelho'], ['Chave da garra', 'GND', 'GND', '#222222', 'preto'], ['Chave da garra', 'OUT', 'GPIO 27', '#6a1b9a', 'roxo'],
  ['Chave da base', 'VCC', '3V3', '#d32f2f', 'vermelho'], ['Chave da base', 'GND', 'GND', '#222222', 'preto'], ['Chave da base', 'OUT', 'GPIO 33', '#00838f', 'azul-claro'],
  ['Servo', 'marrom', 'GND', '#6b3f1d', 'marrom'], ['Servo', 'vermelho', '5 V fixo', '#c62828', 'vermelho'], ['Servo', 'laranja', 'GPIO 13', '#f08a1c', 'laranja']
];
const W0 = .06, W1 = .98;
const fioP = n => W0 + (W1 - W0) * n / LIG.length;           // progresso em que o fio n entra
function textoFio(n) {
  const l = LIG[n], srv = l[0] == 'Servo';
  const de = srv ? 'Enfie a ponta com pino de um jumper macho-fêmea no furo do fio ' + l[1] + ' do plugue do servo.' :
    'Encaixe uma ponta de um jumper ' + l[4] + ' no pino ' + l[1] + ' ' + (l[0] == 'LEDs' ? 'do semáforo' : 'da ' + l[0].toLowerCase()) + '.';
  const para = l[2] == 'GND' ? 'num pino G (terra) do expansor' : l[2] == '3V3' ? 'num pino V (3,3 V) do expansor' : l[2] == '5 V fixo' ? 'no pino 5V do conector de força do expansor' : 'no pino S da porta ' + l[2].replace('GPIO ', '') + ' do expansor';
  return 'Fio ' + (n + 1) + ' de ' + LIG.length + '. ' + de + ' A outra ponta vai ' + para + '.';
}

// Etapas de construção e de funcionamento: [título, texto, [[rótulo, detalhe], ...], [[progresso, o que fazer agora], ...]]
const STEPS = [
 ['Tirar a embreagem da etiqueta', 'A embreagem é a trava que as lojas usam. Ela vem pronta dentro de cada etiqueta: é só abrir e tirar.',
  [['O que é', 'Um copinho de metal com três esferas dentro. O pino entra e não sai.'], ['Onde cortar', 'Em volta da base da cúpula, sem encostar no metal.'], ['Guardar', 'O pino de 16 mm que vem com a etiqueta.']],
  [[0, 'Pegue uma etiqueta do pacote. O pino vem separado: guarde, porque ele vai na garra.'], [.2, 'Segure a etiqueta firme na mesa e serre em volta da cúpula (a parte redonda e alta), bem rente à base. Vá devagar e pare quando sentir o metal.'], [.56, 'Tire a tampa da cúpula com a mão ou com o alicate.'], [.72, 'Lá dentro tem um copinho de metal: é a embreagem. Puxe para fora inteira, sem amassar.']]],
 ['Módulo da trava: embreagem', 'O módulo da trava é uma peça impressa que segura a embreagem em cima e o servo embaixo.',
  [['Encaixe', 'Furo com 0,2 mm de folga e um pingo de cola instantânea.'], ['Parede', '0,8 mm de plástico por baixo da embreagem. O ímã desliza encostado nela.'], ['Por que um módulo', 'Embreagem e servo na mesma peça: a distância entre eles não depende de fechar a tampa.']],
  [[0, 'Ponha o módulo da trava em pé na mesa. A prateleira com o anel fica em cima.'], [.3, 'Vire a embreagem: o lado do furo do pino fica para cima.'], [.48, 'Leve a embreagem até o anel da prateleira. Esse anel é o berço dela.'], [.62, 'Passe um pingo de cola por fora do copo e empurre até encostar na prateleira.']]],
 ['Módulo da trava: servo', 'O servo é o motor. Ele desce entre os dois apoios do módulo e fica preso pelas abas.',
  [['Medida', 'Corpo de 22,7 × 12,1 × 22,6 mm, abas com 32,4 mm.'], ['Parafusos', 'Os dois compridos que vêm no saquinho do servo.'], ['Posição', 'Eixo a 16 mm do centro da embreagem.']],
  [[0, 'Desça o servo entre os dois apoios, com o eixo branco para cima e do lado da embreagem. As abas dele apoiam em cima dos apoios.'], [.5, 'Parafuse a primeira aba. Aperte só até firmar.'], [.7, 'Parafuse a segunda aba.']]],
 ['Módulo da trava: braço e ímãs', 'O braço impresso leva os três ímãs até embaixo da embreagem.',
  [['Cola', 'Instantânea em gel. Lixe antes o ímã e o anel.'], ['Folga', '0,2 mm entre o topo dos ímãs e a parede de 0,8 mm.'], ['Parafuso do braço', 'Só na etapa de teste, depois de pôr o servo em 0°.']],
  [[0, 'Lixe de leve os três ímãs e o lado de dentro do anel do braço, para a cola pegar.'], [.15, 'Passe cola no anel e encaixe o primeiro ímã.'], [.3, 'Encoste o segundo ímã no primeiro. Eles se grudam sozinhos e batem forte: cuidado com o dedo.'], [.45, 'Encoste o terceiro. O topo da pilha fica rente com o topo do anel.'], [.62, 'Encaixe o braço no eixo do servo, apontando para longe da embreagem. Ainda sem parafuso.']]],
 ['Base: receptor e power bank', 'A base é a caixa impressa. Primeiro entram o receptor de carga sem fio e a bateria.',
  [['Base', '210 × 76 × 54 mm por fora. Paredes de 2 mm, fundo de 1,6 mm.'], ['Receptor', '67 × 34 × 1 mm. Fica longe dos ímãs.'], ['Testar antes', 'Se o power bank carrega e alimenta ao mesmo tempo, e se não desliga sozinho com pouco consumo.']],
  [[0, 'Ponha a base impressa na mesa, de boca para cima.'], [.2, 'Cole o receptor de indução no fundo com fita dupla face. O lado que encosta no carregador fica virado para baixo.'], [.45, 'Cole o power bank por cima, com a entrada USB-C virada para a ponta onde sobra espaço.'], [.75, 'Encaixe o plugue USB-C do receptor na entrada do power bank.']]],
 ['ESP32 no expansor', 'O ESP32 é o computador da caixa. Ele encaixa no expansor, que fica colado em cima do power bank.',
  [['Expansor', '73 × 53,5 mm. Cada porta tem três pinos: S (sinal), V (tensão) e G (terra).'], ['Jumper do expansor', 'Em 3,3 V. Em 5 V queima as entradas do ESP32.'], ['Energia', 'Cabo USB-C do power bank na entrada do ESP32.']],
  [[0, 'Cole um pedaço de fita dupla face em cima do power bank.'], [.2, 'Cole o expansor na fita.'], [.45, 'Encaixe o ESP32 nos dois soquetes pretos do expansor. Alinhe todos os pinos antes de empurrar. A porta USB-C fica virada para o lado da trava.'], [.66, 'Confira o jumper do expansor: tem que estar na posição 3V3.'], [.7, 'Ligue o cabo USB-C do power bank no ESP32. Uma luz acende na placa. Depois desligue o cabo para continuar.']]],
 ['Módulo da trava na caixa', 'O módulo pronto vai para a ponta livre da caixa.',
  [['Fixação', 'Dois parafusos M3 curtos.'], ['Chave da base', 'Colada no fundo, sobre o furo do pino-guia.'], ['Conferir', 'O braço gira de 0 a 90° sem bater em nada.']],
  [[0, 'Segure o módulo da trava pela base.'], [.25, 'Leve até a ponta livre da caixa, com a embreagem do lado da frente.'], [.55, 'Desça até encostar no fundo e prenda com dois parafusos M3 curtos.'], [.8, 'Cole uma chave fim de curso no fundo, ao lado, com a haste de metal para cima.']]],
 ['Tampa por dentro', 'Com a tampa virada na mesa, os LEDs e a chave da garra são presos pelo lado de dentro.',
  [['LEDs', 'Três furos de 8,6 mm, a cada 15 mm.'], ['Chave da garra', 'Fecha quando a garra abaixa. Um pino branco atravessa a tampa e encosta na garra.'], ['Sem tela', 'O QR é um adesivo colado por fora, no fim da montagem.']],
  [[0, 'Vire a tampa: o lado de dentro, que é liso, fica para cima.'], [.2, 'Encaixe os três LEDs do semáforo nos três furos e prenda com dois pingos de cola.'], [.5, 'Cole uma chave fim de curso ao lado do furo pequeno, com a haste sobre o pino branco. É ela que sente a garra fechar.']]],
 ['Garra', 'A garra é a parte que prende a roupa. Ela gira numa dobradiça e uma mola de pregador a mantém aberta.',
  [['Dentes', 'Cinco fileiras na garra e quatro na tampa, com tira de borracha colada.'], ['Pino', 'O de 16 mm, liso, solto numa bolsa da garra e com um funil na entrada. Fica fora da área do tecido.'], ['Dobradiça', 'Parafuso M3 de 40 mm como eixo, com a porca frouxa.'], ['Mola', 'De pregador de roupa. Abre a garra quando a embreagem solta.']],
  [[0, 'Desvire a tampa e apoie sobre os módulos.'], [.3, 'Corte tiras de borracha de 36 × 2 mm e cole em cima dos quatro dentes da tampa.'], [.45, 'Na garra: cole borracha nos cinco dentes, solte o pino na bolsa e feche com a tampinha. O pino fica pendurado.'], [.65, 'Tire a mola de um pregador de roupa e encaixe entre os dois apoios da dobradiça.'], [.8, 'Alinhe o furo da garra com os apoios e passe o parafuso M3 de 40 mm. Ponha a porca sem apertar: a garra tem que girar.']]],
 ['Fiação', 'Cada fio (jumper) liga um pino de um módulo a um pino do expansor. É um fio por vez, sem pressa.',
  [['LEDs', 'Vermelho 19, amarelo 21, verde 22, mais GND.'], ['Chaves', 'Garra 27, base 33. Cada uma com 3V3 e GND.'], ['Servo', 'Sinal no 13, força no pino 5V do conector de força.']],
  [[0, 'Ponha a tampa em pé atrás da caixa, aberta. Confira que nada está ligado na energia.']]],
 ['Programa e teste', 'O ESP32 recebe o programa pelo cabo USB e cada parte é testada sozinha.',
  [['Ordem', 'LEDs, servo e chaves. Só depois o Wi-Fi.'], ['Servo', 'Se o ESP32 reiniciar quando o servo mexe, falta o capacitor.'], ['Depois', 'Repetir tudo no power bank por 30 minutos.']],
  [[0, 'Tire o cabo do power bank do ESP32 e ligue o cabo do notebook.'], [.1, 'Carregue o programa de teste. Os LEDs acendem um por vez: vermelho, amarelo, verde.'], [.58, 'O servo vai até 90° e volta para 0°.'], [.78, 'Com o servo parado em 0°, ajuste o braço apontando para longe da embreagem e prenda com o parafusinho do saquinho do servo.'], [.92, 'Aperte cada chave com o dedo e veja o valor mudar no Monitor Serial.']]],
 ['Fechar a caixa', 'A tampa desce, é presa com quatro parafusos e recebe o adesivo do QR.',
  [['Parafusos', 'M3 direto no plástico, em furo de 2,5 mm.'], ['Fios', 'Dobrados para o lado do expansor, longe do braço do servo.'], ['QR', 'Adesivo de 34 × 34 mm com o endereço da caixa, por exemplo seusaas/c/01.']],
  [[0, 'Tire o cabo do notebook e religue o cabo do power bank no ESP32.'], [.08, 'Dobre os fios para o lado do expansor e abaixe a tampa devagar. Nenhum fio pode ficar perto do braço do servo.'], [.6, 'Prenda com quatro parafusos M3 nos cantos.'], [.86, 'Imprima o QR da caixa em papel adesivo e cole na tampa. Teste com a câmera do celular: tem que abrir o endereço.']]],
 ['Prender a roupa', 'A garra fica aberta pela mola. O funcionário põe a borda da roupa dentro e fecha a garra com a mão.',
  [['Sem furo', 'Os dentes com borracha apertam o tecido em zigue-zague.'], ['Trava', 'O pino da garra desce na embreagem, ao lado do tecido. Ela segura o pino em qualquer altura, então serve para tecido fino ou grosso.'], ['Onde prender', 'De preferência atrás de uma bainha. As etiquetas sem pino da Sensormatic pedem o mesmo.']],
  [[0, 'Garra aberta. A roupa entra pela frente até o batente.'], [.36, 'Apertar a garra para baixo.'], [.6, 'Travou. LED vermelho.']]],
 ['Cadastrar', 'O funcionário lê com o celular o QR colado na caixa. Como a caixa está livre, a página que abre é a de cadastro.',
  [['QR fixo', 'É sempre o mesmo endereço. O servidor decide a página pelo estado da caixa.'], ['Senha', 'O cadastro pede a senha do funcionário.'], ['Servidor', 'Ao salvar, a caixa passa de livre para à venda.']],
  [[0, 'O QR está colado na tampa.'], [.25, 'Ler o QR com o celular.'], [.62, 'Informar a roupa e o preço.'], [.8, 'Servidor: à venda.']]],
 ['Tentativa de furto', 'Alguém segura a caixa e puxa a roupa. Os dentes seguram o tecido e a garra não abre, porque o pino está travado.',
  [['Força', 'Estimativa de 12 a 80 N só com o atrito, mais o ganho do zigue-zague. Um pino que fura segura uns 350 N. Medir no teste.'], ['Reforço', 'Prender atrás de uma costura ou bainha, que não passa entre os dentes.'], ['Alerta', 'Se a chave da garra abrir sem ordem, o painel da loja avisa.']],
  [[0, 'A roupa está presa.'], [.15, 'Puxão na roupa.'], [.8, 'Continua presa.']]],
 ['Pagar', 'O cliente lê o mesmo QR. Como a caixa agora está à venda, a página que abre é a de compra.',
  [['Servidor', 'Estado à venda: abre a compra. Ao pagar, passa para paga.'], ['Pagamento', 'Simulado no protótipo.'], ['Sem aplicativo', 'É uma página comum, aberta pela câmera.']],
  [[0, 'O mesmo QR da tampa.'], [.2, 'Ler o QR com o celular.'], [.55, 'Página de compra.'], [.8, 'Pago.']]],
 ['Soltar', 'A caixa recebe a ordem e gira os ímãs para baixo da embreagem. O pino solta e a mola abre a garra.',
  [['Servo', 'Gira 90° e segura por 8 s.'], ['Garra', 'Abre sozinha, cerca de 30°.'], ['A testar', 'Se a mola atrapalha a soltura. Mola fraca é melhor.']],
  [[0, 'O ESP32 pergunta ao servidor se há ordem.'], [.12, 'O servo gira os ímãs para baixo da embreagem.'], [.4, 'A garra abre. LED verde.'], [.58, 'O cliente tira a roupa.'], [.88, 'O servo volta.']]],
 ['Recarregar', 'A caixa vazia é posta na base de indução. O painel da loja mostra a bateria de cada caixa.',
  [['Base', 'Berço impresso com pino-guia, que entra no furo do fundo e aperta a chave.'], ['LED', 'Amarelo enquanto a chave da base está apertada.'], ['Bateria no aplicativo', 'É uma estimativa: o ESP32 informa há quantas horas saiu da base e o servidor calcula a porcentagem. Medir de verdade exige trocar o power bank por outra bateria.']],
  [[0, 'Levantar a caixa.'], [.2, 'Base de indução no lugar.'], [.5, 'Descer a caixa na base.'], [.68, 'Carregando. LED amarelo.'], [.74, 'No painel da loja aparece o estado e a bateria estimada da caixa.']]]
];
const NA = 12;
LIG.forEach((l, n) => STEPS[9][3].push([fioP(n), textoFio(n)]));
const DUR = i => i < NA ? Math.max(9000, STEPS[i][3].length * 4200) : 10000;
const EST = ['livre', 'à venda', 'paga', 'liberada', 'na base'];

// Manual de cada etapa de construção: materiais (códigos de COMPRAS ou texto), ferramentas, como conferir e erros comuns.
const MAN = [
 {mats: ['etq'], ferr: ['Serrinha', 'Óculos de proteção', 'Alicate de bico'], ok: 'Enfie o pino na embreagem: ele entra e não sai. Encoste três ímãs empilhados no lado oposto ao furo: o pino solta.', erros: ['Serrar fundo demais e cortar o copo de metal.', 'Se o copo abrir e as esferas caírem, use outra etiqueta.']},
 {mats: ['Módulo da trava (impresso)', 'A embreagem da etapa anterior', 'Cola instantânea em gel'], ferr: [], ok: 'A embreagem não gira nem sobe quando você puxa com o dedo. O furo está limpo.', erros: ['Cola dentro do furo trava o mecanismo. Use pouca.', 'Embreagem de cabeça para baixo: o pino não entra.']},
 {mats: ['srv', 'Os dois parafusos compridos do saquinho do servo'], ferr: ['Chave Philips pequena'], ok: 'O servo não balança e o fio sai livre por baixo.', erros: ['Apertar demais racha o plástico impresso.', 'Servo virado ao contrário: o eixo tem que ficar do lado da embreagem.']},
 {mats: ['Braço do ímã (impresso)', 'ima', 'Cola instantânea em gel'], ferr: ['Lixa fina'], ok: 'Girando o braço com a mão, os ímãs passam por baixo da embreagem sem raspar.', erros: ['Deixar os ímãs perto de celular, cartão ou relógio.', 'Prender o dedo entre dois ímãs.']},
 {mats: ['Base (impressa)', 'qir', 'pwb', 'Fita dupla face'], ferr: [], ok: 'Com a base em cima do carregador de indução, o visor do power bank mostra que está carregando.', erros: ['Receptor de cabeça para baixo: não carrega.', 'Fundo da caixa com mais de 2 mm: a carga falha.']},
 {mats: ['exp', 'esp', 'Fita dupla face'], ferr: [], ok: 'A luz do ESP32 acende quando o cabo do power bank é ligado.', erros: ['Um pino do ESP32 fora do soquete entorta. Olhe de lado antes de empurrar.', 'Jumper do expansor em 5 V.']},
 {mats: ['Dois parafusos M3 curtos (do kit)', 'chv', 'Fita dupla face'], ferr: ['Chave Philips pequena'], ok: 'O braço gira de 0 a 90° sem bater na parede nem no power bank.', erros: ['Fio do servo preso embaixo do módulo.']},
 {mats: ['Tampa (impressa)', 'sem', 'chv', 'Cola instantânea em gel'], ferr: [], ok: 'Desvirando a tampa, os três LEDs aparecem nos furos e o pino branco da chave sobe e desce.', erros: ['Cola na ponta dos LEDs.', 'Chave colada torta: o pino branco não aperta a haste.']},
 {mats: ['Garra (impressa)', 'O pino guardado da etiqueta', 'Tampinha do pino (impressa)', 'Tira de borracha', 'Mola de um pregador de roupa', 'Parafuso M3 de 40 mm com porca', 'Cola instantânea em gel'], ferr: ['Estilete', 'Alicate de bico'], ok: 'A garra abre sozinha pela mola e fecha com um dedo. O pino aponta para o furo da embreagem.', erros: ['Porca apertada: a garra não gira.', 'Borracha grossa demais: a garra não fecha até o pino travar.']},
 {mats: ['jff', 'jmf'], ferr: [], ok: 'Cada fio está firme nas duas pontas, e nenhum pino V está ligado num pino G.', erros: ['Fio no pino vizinho. Conte os pinos duas vezes.', 'Plugue do servo com as cores trocadas.', 'Chave ligada no pino V de 5 V.']},
 {mats: ['Cabo USB-C de dados', 'O parafusinho do saquinho do servo'], ferr: ['Notebook', 'Chave Philips pequena'], ok: 'LEDs, servo e as duas chaves respondem.', erros: ['ESP32 reinicia quando o servo mexe: falta o capacitor.', 'Erro ao carregar: segure o botão BOOT da placa.'], aviso: 'O programa de teste ainda vai ser escrito. Ele entra junto com o programa final.'},
 {mats: ['Quatro parafusos M3 (do kit)', 'Adesivo com o QR da caixa'], ferr: ['Chave Philips pequena'], ok: 'A tampa assenta sem forçar, o braço do servo continua livre e o QR abre o endereço da caixa.', erros: ['Fio esmagado entre a tampa e a parede.']}
];

// Capítulos de preparação, antes de construir. view: o que o 3D mostra.
const PREP = [
 {tit: 'O que vamos construir e o que comprar', txt: 'Uma caixa que prende a roupa com uma garra, tem um QR colado para cadastrar e pagar, e solta sozinha depois do pagamento.', view: 'final', compras: true,
  passos: [[0, 'Este é o aparelho pronto. Gire com o mouse para ver de todos os lados.'], [.34, 'Tudo o que é comprado está na lista ao lado, com o link de cada loja. Os preços foram vistos entre 29/09 e 07/10/2026, sem frete.'], [.67, 'Compre primeiro as etiquetas e os ímãs. Com eles você faz o teste que decide o projeto: se três ímãs empilhados abrem a embreagem.']],
  ok: 'Você sabe o que cada peça faz e de onde ela vem.', erros: ['Comprar etiqueta do tipo superlock: o ímã pequeno não abre.', 'Comprar o ESP32 de 38 pinos: ele não encaixa no expansor de 30.']},
 {tit: 'Ferramentas e coisas de casa', txt: 'Nada aqui precisa de solda nem de ferramenta elétrica.', view: 'final', ferramentas: true,
  passos: [[0, 'Separe as ferramentas da lista ao lado.'], [.5, 'Separe também as coisas de casa: fita dupla face, cola em gel, um pregador de roupa, uma tira de borracha e um cabo USB-C que passe dados.']],
  ok: 'Tudo da lista está na mesa.', erros: ['Cabo USB que só carrega: o notebook não enxerga a placa.']},
 {tit: 'Imprimir as peças', txt: 'As peças de plástico são feitas na impressora 3D, que derrete um fio de plástico e desenha a peça camada por camada.', view: 'print',
  aviso: 'Os arquivos das peças para imprimir ainda vão ser gerados. Antes disso é preciso medir a embreagem de verdade com paquímetro.',
  cfg: [['Material', 'PLA de 1,75 mm. É o mais fácil de imprimir.'], ['Bico e camada', 'Bico de 0,4 mm, camada de 0,2 mm.'], ['Paredes', '3 voltas. Na garra e no módulo, 4.'], ['Temperatura', '200 a 210 °C no bico e 60 °C na mesa.'], ['Onde imprimir', 'Num laboratório da faculdade ou numa impressora de mesa de 220 × 220 mm.']],
  passos: [[0, 'Instale um fatiador gratuito, como o Cura ou o OrcaSlicer. É o programa que transforma o desenho da peça em instruções para a impressora.', -1],
   [.09, 'No fatiador, escolha PLA, camada de 0,2 mm e 3 paredes. Abra o arquivo da peça, confira a posição na mesa e clique em fatiar. Salve no cartão ou mande pela rede.', -1],
   [.94, 'Depois de imprimir: tire as rebarbas com estilete. Teste se o parafuso M3 entra nas colunas e se a embreagem entra no berço. Se ficar apertado, lixe.', -1]],
  ok: 'As peças saem sem empenar e os encaixes entram com a mão.', erros: ['Primeira camada não gruda: limpe a mesa com álcool e nivele.', 'Furo apertado: é normal sair 0,1 a 0,3 mm menor. Lixe ou alargue.', 'Imprimir tudo antes de medir a embreagem.']},
 {tit: 'Preparar o computador', txt: 'O programa do ESP32 é enviado pelo Arduino IDE, que é gratuito. Isso é feito uma vez só.', view: 'pc',
  links: [['Baixar o Arduino IDE', 'https://www.arduino.cc/en/software'], ['Driver CP210x, se a porta não aparecer', 'https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers']],
  codigo: 'https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json',
  passos: [[0, 'Instale o Arduino IDE 2.'], [.14, 'Abra Arquivo > Preferências. No campo "URLs adicionais para gerenciadores de placas", cole o endereço que está no quadro ao lado.'],
   [.28, 'Abra Ferramentas > Placa > Gerenciador de placas. Procure "esp32", da Espressif, e instale.'],
   [.42, 'Ligue o ESP32 no notebook com o cabo USB-C. Se nenhuma porta nova aparecer em Ferramentas > Porta, instale o driver CP210x.'],
   [.56, 'Em Ferramentas > Placa, escolha "DOIT ESP32 DEVKIT V1". Em Ferramentas > Porta, escolha a porta que apareceu.'],
   [.7, 'Em Sketch > Incluir biblioteca > Gerenciar bibliotecas, instale: ESP32Servo e ArduinoJson.'],
   [.84, 'Teste: abra Arquivo > Exemplos > 01.Basics > Blink e clique na seta Carregar. A luz azul da placa começa a piscar.']],
  ok: 'A luz azul do ESP32 pisca depois de carregar o Blink.', erros: ['"Failed to connect": segure o botão BOOT da placa enquanto carrega.', 'Porta não aparece: cabo que só carrega, ou falta o driver.']},
 {tit: 'Noções de elétrica em cinco minutos', txt: 'Para ligar os fios você só precisa saber três letras e duas regras.', view: 'fios',
  passos: [[0, 'Três tipos de pino. G é a terra, o lado negativo. V é a tensão, o lado positivo. S é o sinal, por onde passa a informação.'],
   [.15, 'O expansor repete G, V e S para cada porta do ESP32. O número impresso ao lado de cada trio é o número da porta.'],
   [.3, 'O jumper é um fio com um encaixe em cada ponta. Empurre o encaixe no pino, reto, até o fim. Ele fica firme sozinho.'],
   [.45, 'Regra 1: nunca ponha nem tire fio com o power bank ou o cabo USB ligado.'],
   [.6, 'Regra 2: o jumper amarelo do expansor escolhe a tensão dos pinos V. Deixe em 3V3. Em 5 V, as entradas do ESP32 queimam.'],
   [.75, 'Só o servo usa 5 V. Ele pega num conector separado do expansor, marcado 5V.'],
   [.88, 'A cor do fio não muda nada na eletricidade. Usamos vermelho para V e preto para G só para não confundir.']],
  ok: 'Você sabe achar G, V e S no expansor e sabe onde fica o jumper de 3V3.', erros: ['Ligar V direto em G: é curto-circuito e o power bank desliga.']}
];
const NP = PREP.length;

const FLOW = [
 {act: ['sen', 'led', 'e2s'], lab: {sen: 'garra = 1', led: 'vermelho', e2s: '{"caixa":"01","garra":1,"fora_da_base_s":40}'}},
 {act: ['c2s', 's2c', 'sdb', 's2e', 'span'], lab: {c2s: 'GET /c/01, depois POST cadastro', s2c: 'estado livre: página de cadastro', sdb: 'roupa, preço, estado = à venda', s2e: 'estado = à venda'}},
 {act: ['sen', 'e2s', 'span'], lab: {sen: 'garra = 1, segue presa', e2s: '{"caixa":"01","garra":1}', span: 'se garra = 0 sem ordem: alerta'}},
 {act: ['c2s', 's2c', 'sdb', 'span'], lab: {c2s: 'GET /c/01, depois POST pagar', s2c: 'estado à venda: página de compra', sdb: 'venda, estado = paga'}},
 {act: ['e2s', 's2e', 'srvo', 'led', 'sen', 'sdb'], lab: {e2s: 'tem ordem?', s2e: '{"ordem":"soltar"}', srvo: '90° por 8 s', led: 'verde', sen: 'garra = 0', sdb: 'estado = liberada'}},
 {act: ['sen', 'led', 'e2s', 'sdb', 'span'], lab: {sen: 'base = 1', led: 'amarelo', e2s: '{"caixa":"01","base":1}', sdb: 'estado = na base, zera a bateria estimada', span: 'bateria estimada de cada caixa'}}
];

const cl = x => Math.max(0, Math.min(1, x));
const seg = (p, a, b) => cl((p - a) / (b - a));
const ez = p => p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
const lerp = (a, b, t) => a + (b - a) * t;

// Estado do produto na etapa i, com progresso p de 0 a 1.
// jaw: 1 aberta, 0 fechada. cin: quanto o tecido entrou. mag: 0 repouso, 1 sob a embreagem.
function estado(i, p) {
  const o = {jaw: 1, cin: 0, cloth: 0, pull: 0, press: 0, led: 'off', scr: 'off', btn: 0, ph: 0, mode: 'cam', who: 'funcionário', est: '', mag: 0, lift: 0, base: 0, seat: 0, grip: 0};
  if (i == 10) { o.led = p > .1 && p < .25 ? 'red' : p >= .25 && p < .4 ? 'yellow' : p >= .4 && p < .55 ? 'green' : 'off';
    o.mag = ez(seg(p, .58, .66)) * (1 - ez(seg(p, .69, .77))); }
  if (i < NA) return o;
  const s = i - NA; o.est = 'livre';
  if (s == 0) { o.cloth = 1; o.cin = ez(seg(p, .02, .3)); o.press = p > .36 && p < .62 ? 1 : 0; o.jaw = 1 - ez(seg(p, .42, .6)); o.led = p > .6 ? 'red' : 'off'; }
  if (s >= 1 && s <= 3) { o.cloth = 1; o.cin = 1; o.jaw = 0; o.led = 'red'; }
  if (s == 1) { o.ph = ez(seg(p, .25, .4)); o.mode = p < .62 ? 'cam' : 'cad'; o.est = p < .75 ? 'livre' : 'à venda'; }
  if (s == 2) { o.est = 'à venda'; o.pull = ez(seg(p, .15, .3)) * (1 - seg(p, .8, .95)); o.grip = o.pull; }
  if (s == 3) { o.who = 'cliente'; o.ph = ez(seg(p, .2, .35)); o.mode = p < .55 ? 'cam' : p < .8 ? 'buy' : 'ok'; o.est = p < .85 ? 'à venda' : 'paga'; }
  if (s == 4) { o.cloth = 1; o.mag = ez(seg(p, .12, .38)) * (1 - ez(seg(p, .88, 1))); o.jaw = ez(seg(p, .4, .5)); o.cin = 1 - ez(seg(p, .58, .84));
    o.led = p < .4 ? 'red' : 'green'; o.est = p < .46 ? 'paga' : 'liberada'; }
  if (s == 5) { const up = ez(seg(p, .05, .22)), dn = ez(seg(p, .5, .68)); o.lift = up * 34 - dn * 26; o.base = ez(seg(p, .2, .45)); o.seat = p > .68 ? 1 : 0;
    o.led = o.seat ? 'yellow' : 'green'; o.est = !o.seat ? 'liberada' : p < .9 ? 'na base' : 'livre'; o.ph = ez(seg(p, .74, .86)); o.mode = 'pan'; o.who = 'painel da loja'; o.bat = Math.round(lerp(38, 46, seg(p, .74, 1))); }
  return o;
}
function magPos(m) { const a = lerp(0, Math.PI / 2, m); return {x: D.A.x + D.R * Math.cos(a), z: D.A.z + D.R * Math.sin(a), a}; }
// Quantos fios já estão no lugar na etapa de fiação.
function fiosProntos(i, p) { return i > 9 ? LIG.length : i < 9 ? 0 : LIG.filter((l, n) => p >= fioP(n)).length; }
// Índice do passo atual dentro de uma lista [[progresso, texto], ...].
function passoAtual(lista, p) { let k = 0; lista.forEach((e, n) => { if (p >= e[0] - 1e-6) k = n; }); return k; }
function agora(i, p) { const s = STEPS[i][3]; return s[passoAtual(s, p)][1]; }

// ---------- variantes do produto (usadas pelo manual em 3D) ----------
// Cada etapa tem um nome curto fixo. Uma variante é uma lista de etapas, com trocas onde ela é diferente.
const IDS = ['tag', 'clutch', 'servo', 'arm', 'base', 'esp', 'place', 'lid', 'jaw', 'wire', 'test', 'close', 'f_lock', 'f_reg', 'f_pull', 'f_pay', 'f_rel', 'f_chg'];
const ETAPA = {}; IDS.forEach((id, k) => ETAPA[id] = {tit: STEPS[k][0], txt: STEPS[k][1], cfg: STEPS[k][2], passos: STEPS[k][3], man: MAN[k] || {}});
const VAR = {
 emb: {nome: 'A. Embreagem de loja e ímãs', curto: 'A: embreagem e ímãs',
  resumo: 'A garra é travada por um pino que desce numa embreagem tirada de uma etiqueta de loja. O servo leva três ímãs para baixo dela e o pino solta.',
  ids: IDS.slice(), over: {}, sem: [], casa: [], custo: 'cerca de R$ 440', nImp: 7,
  pros: ['Trava pronta e forte: a patente fala em 36 kgf.', 'Segura o pino em qualquer altura, então serve para tecido fino ou grosso.', 'O servo não faz força contra a trava, só leva o ímã.'],
  contras: ['Depende de o ímã abrir a embreagem através de 0,8 mm de plástico.', 'O pino entra em arco. Não achei produto que faça assim.', 'Montagem de precisão: 0,2 mm de folga entre ímã e parede.'],
  teste: 'Encostar três ímãs empilhados numa embreagem e ver se o pino solta. Custa R$ 89 e leva uma hora.',
  print: [[.18, 'Base: de boca para cima, sem suporte, 20% de preenchimento. É a maior e ocupa quase toda a mesa.', 0], [.3, 'Tampa: com o lado de dentro apoiado na mesa. Os dentes, o batente e os apoios da dobradiça ficam para cima. Sem suporte.', 1],
   [.42, 'Garra: com o lado liso apoiado na mesa e os dentes para cima. 40% de preenchimento e 4 paredes, porque é a peça que faz força.', 2], [.54, 'Módulo da trava: em pé, como vai ficar na caixa. Ligue o suporte, por causa da prateleira. 40% de preenchimento.', 3],
   [.66, 'Braço do ímã: de cabeça para baixo, com o anel apoiado na mesa. 100% de preenchimento.', 4], [.76, 'Berço da base de carga: apoiado no lado maior, sem suporte.', 5], [.86, 'Tampinha do pino: é pequena, imprima duas.', 6]]},
 lin: {nome: 'B. Lingueta com mola e servo', curto: 'B: lingueta e mola',
  resumo: 'A garra tem um gancho que desce pela tampa. Uma lingueta com mola entra no gancho e faz o clique. O servo puxa a lingueta para trás e a garra abre.',
  ids: ['servo', 'bolt', 'horn', 'base', 'esp', 'place', 'lid', 'jaw', 'wire', 'test', 'close', 'f_lock', 'f_reg', 'f_pull', 'f_pay', 'f_rel', 'f_chg'],
  sem: ['etq', 'ima'], casa: ['Mola de caneta (para a lingueta)'], custo: 'cerca de R$ 350', nImp: 6,
  pros: ['Não compra etiqueta nem ímã.', 'Dá para ver a trava funcionando e corrigir reimprimindo uma peça pequena.', 'É o que o relatório descreve: mola, gatilho e microatuador.', 'Sem ímã perto da carga por indução.'],
  contras: ['Trava numa altura só. A espessura do tecido fica por conta da borracha dos dentes.', 'A trava é de plástico impresso: aguenta menos e gasta com o uso.', 'O atrito do plástico varia. Pode precisar de duas ou três impressões.'],
  teste: 'Imprimir só a lingueta, o gancho e o trilho, e soltar com o dedo dez vezes seguidas. Não precisa comprar nada.',
  print: [[.18, 'Base: de boca para cima, sem suporte, 20% de preenchimento. É a maior e ocupa quase toda a mesa.', 0], [.3, 'Tampa: com o lado de dentro apoiado na mesa. Os dentes, o batente e os apoios da dobradiça ficam para cima. Sem suporte.', 1],
   [.42, 'Garra: com o lado liso apoiado na mesa, os dentes e o gancho para cima. 40% de preenchimento e 4 paredes. O gancho é a parte que faz força.', 2], [.54, 'Módulo da trava: em pé, com o trilho da lingueta em cima. Ligue o suporte. 40% de preenchimento.', 3],
   [.66, 'Lingueta: deitada, 100% de preenchimento. Imprima duas, uma de reserva.', 4], [.78, 'Berço da base de carga: apoiado no lado maior, sem suporte.', 5]],
  over: {
   servo: {tit: 'Módulo da trava: servo', txt: 'O módulo da trava é uma peça impressa com dois apoios para o servo embaixo e um trilho para a lingueta em cima.',
    cfg: [['Medida do servo', 'Corpo de 22,7 × 12,1 × 22,6 mm, abas com 32,4 mm.'], ['Parafusos', 'Os dois compridos que vêm no saquinho do servo.'], ['Trilho', 'Canal de 6 × 6 mm para a lingueta, com 0,3 mm de folga.']],
    passos: [[0, 'Ponha o módulo da trava em pé na mesa. Embaixo ficam os dois apoios do servo e em cima o trilho da lingueta.'], [.35, 'Desça o servo entre os dois apoios, com o eixo branco para cima.'], [.72, 'Parafuse a primeira aba. Aperte só até firmar.'], [.86, 'Parafuse a segunda aba.']],
    man: {mats: ['Módulo da trava (impresso)', 'srv', 'Os dois parafusos compridos do saquinho do servo'], ferr: ['Chave Philips pequena'], ok: 'O servo não balança e o fio sai livre por baixo.', erros: ['Apertar demais racha o plástico impresso.', 'Servo virado: o eixo fica embaixo do meio do trilho.']}},
   bolt: {tit: 'Módulo da trava: lingueta e mola', txt: 'A lingueta é a peça que segura o gancho da garra. Uma mola de caneta a empurra para a frente.',
    cfg: [['Lingueta', '5,6 × 5,6 × 20 mm, com a ponta chanfrada em cima.'], ['Curso', '6 mm para trás solta o gancho.'], ['Mola', 'De caneta, cortada com cerca de 12 mm.']],
    passos: [[0, 'Lixe de leve a lingueta impressa, até ela correr solta no trilho.'], [.3, 'Ponha a mola no fundo do trilho.'], [.55, 'Empurre a lingueta para dentro do trilho, com a ponta chanfrada para cima e para a frente. O pino dela fica para baixo.'], [.8, 'Aperte e solte com o dedo: ela tem que voltar sozinha, todas as vezes.']],
    man: {mats: ['Lingueta (impressa)', 'Mola de caneta'], ferr: ['Lixa fina', 'Alicate de bico, para cortar a mola'], ok: 'A lingueta volta sozinha dez vezes seguidas, sem prender.', erros: ['Lingueta justa demais: lixe até correr solta.', 'Mola comprida demais: a lingueta não recolhe os 6 mm.']}},
   horn: {tit: 'Módulo da trava: braço do servo', txt: 'O braço do servo é a alavanca que puxa a lingueta para trás.',
    cfg: [['Braço', 'O de uma ponta só, que vem no saquinho do servo.'], ['Parafuso', 'Só na etapa de teste, depois de pôr o servo em 0°.'], ['Força', 'Com braço curto o servo puxa mais forte. Use o furo mais perto do eixo.']],
    passos: [[0, 'Pegue o braço de uma ponta só que vem no saquinho do servo.'], [.4, 'Encaixe no eixo, encostado no pino da lingueta. Ainda sem parafuso.']],
    man: {mats: ['Braço de uma ponta, do saquinho do servo'], ferr: [], ok: 'Girando o braço com a mão, a lingueta recolhe e volta.', erros: ['Braço do outro lado do pino: o servo empurra em vez de puxar.']}},
   jaw: {txt: 'A garra é a parte que prende a roupa. Ela gira numa dobradiça, uma mola de pregador a mantém aberta, e o gancho dela desce pelo rasgo da tampa.',
    cfg: [['Dentes', 'Cinco fileiras na garra e quatro na tampa, com tira de borracha de 2 a 3 mm.'], ['Gancho', 'Já vem impresso na garra. Tem uma janela onde a lingueta entra.'], ['Dobradiça', 'Parafuso M3 de 40 mm como eixo, com a porca frouxa.'], ['Mola', 'De pregador de roupa. Abre a garra quando a lingueta recolhe.']],
    passos: [[0, 'Desvire a tampa e apoie sobre os módulos.'], [.3, 'Corte tiras de borracha de 36 × 2 mm e cole em cima dos quatro dentes da tampa.'], [.45, 'Na garra: cole borracha nos cinco dentes. O gancho fica do lado da ponta e aponta para o rasgo da tampa.'], [.65, 'Tire a mola de um pregador de roupa e encaixe entre os dois apoios da dobradiça.'], [.8, 'Alinhe o furo da garra com os apoios e passe o parafuso M3 de 40 mm. Ponha a porca sem apertar: a garra tem que girar.']],
    man: {mats: ['Garra com gancho (impressa)', 'Tira de borracha', 'Mola de um pregador de roupa', 'Parafuso M3 de 40 mm com porca', 'Cola instantânea em gel'], ferr: ['Estilete', 'Alicate de bico'], ok: 'A garra abre sozinha pela mola e, ao fechar, o gancho entra no rasgo sem raspar.', erros: ['Porca apertada: a garra não gira.', 'Borracha grossa demais: o gancho não desce até a lingueta.']}},
   test: {passos: [[0, 'Tire o cabo do power bank do ESP32 e ligue o cabo do notebook.'], [.1, 'Carregue o programa de teste. Os LEDs acendem um por vez: vermelho, amarelo, verde.'], [.58, 'O servo vai até a posição de soltar e volta para 0°. A lingueta recolhe e volta junto.'], [.78, 'Com o servo parado em 0°, ajuste o braço encostado no pino da lingueta e prenda com o parafusinho do saquinho do servo.'], [.92, 'Aperte cada chave com o dedo e veja o valor mudar no Monitor Serial.']]},
   f_lock: {txt: 'A garra fica aberta pela mola. O funcionário põe a borda da roupa dentro e fecha a garra com a mão, até o clique.',
    cfg: [['Sem furo', 'Os dentes com borracha apertam o tecido em zigue-zague.'], ['Clique', 'O gancho empurra a lingueta, passa, e a mola a devolve para dentro da janela do gancho.'], ['Onde prender', 'De preferência atrás de uma bainha.']],
    passos: [[0, 'Garra aberta. A roupa entra pela frente até o batente.'], [.36, 'Apertar a garra para baixo.'], [.6, 'Clique: a lingueta entrou no gancho. LED vermelho.']]},
   f_pull: {txt: 'Alguém segura a caixa e puxa a roupa. Os dentes seguram o tecido e a garra não abre, porque o gancho está preso na lingueta.',
    cfg: [['Força', 'A lingueta de plástico aguenta menos que uma embreagem de metal. Precisa ser medida no teste.'], ['Reforço', 'Prender atrás de uma costura ou bainha, que não passa entre os dentes.'], ['Alerta', 'Se a chave da garra abrir sem ordem, o painel da loja avisa.']]},
   f_rel: {txt: 'A caixa recebe a ordem e o servo puxa a lingueta para trás. O gancho fica livre e a mola abre a garra.',
    cfg: [['Servo', 'Puxa 6 mm e segura por 1 a 2 s.'], ['Garra', 'Abre sozinha, cerca de 30°.'], ['A testar', 'Se o servo consegue puxar com a mola da garra empurrando o gancho contra a lingueta.']],
    passos: [[0, 'O ESP32 pergunta ao servidor se há ordem.'], [.12, 'O servo puxa a lingueta para trás.'], [.4, 'A garra abre. LED verde.'], [.58, 'O cliente tira a roupa.'], [.88, 'O servo solta e a lingueta volta.']]}
  }}
};
// Opções pesquisadas que não foram modeladas em 3D.
const OUTRAS = [
 ['Mini trava solenoide de 12 V', 'Pronta no Brasil por R$ 35 a 49, mas precisa de relé e de um elevador de tensão. Mais fios e risco de reiniciar o ESP32.'],
 ['Mini trava solenoide de 5 a 6 V', 'Ligaria direto no power bank com um relé, mas só achei importada.'],
 ['Catraca impressa com gatilho', 'Trava em várias alturas, mas o servo não consegue soltar o gatilho sob carga sem um segundo gatilho em alavanca.'],
 ['Eletroímã', 'Abre quando acaba a bateria e gasta energia o tempo todo.']
];
// Variante C: mesma trava da B (lingueta com mola), mas a garra tem dedos que empurram o tecido para dentro de rasgos na tampa.
VAR.gar = {nome: 'C. Garra com dedos e rasgos', curto: 'C: dedos e rasgos',
  resumo: 'A garra tem três dedos que empurram a borda da roupa para dentro de três rasgos na tampa. O tecido faz um zigue-zague dentro da caixa e fica preso pelo atrito das curvas. A garra trava com a mesma lingueta com mola da variante B.',
  ids: VAR.lin.ids.slice(), sem: ['etq', 'ima'], casa: ['Mola de caneta (para a lingueta)'], nImp: 6, herda: 'lin',
  pros: ['Segura muito mais que os dentes: o tecido dá três meias-voltas dentro da caixa, e cada curva multiplica o atrito.', 'Não fura a roupa.', 'Não compra etiqueta nem ímã.', 'Os dedos e os rasgos saem da impressora junto com a garra e a tampa.'],
  contras: ['Pode deixar o tecido marcado se a peça ficar presa muitos dias.', 'Tecido grosso (jeans, moletom) pode não caber no rasgo. A folga precisa de teste.', 'Precisa de uma bolsa sob a tampa, onde o tecido dobra, longe dos fios.', 'A trava continua sendo a lingueta de plástico da variante B.'],
  teste: 'Imprimir só um pedaço de tampa com os rasgos e a garra com os dedos. Prender um tecido fino e um grosso e puxar com uma balança de mala.',
  print: [[.18, 'Base: de boca para cima, sem suporte, 20% de preenchimento. É a maior e ocupa quase toda a mesa.', 0], [.3, 'Tampa: com o lado de dentro para cima, para a bolsa dos rasgos sair sem suporte. Bordas dos rasgos com chanfro de 0,5 mm, para não cortar o tecido.', 1],
   [.42, 'Garra: deitada, com os dedos e o gancho para cima. 40% de preenchimento e 4 paredes. Os dedos e o gancho fazem força.', 2], [.54, 'Módulo da trava: em pé, com o trilho da lingueta em cima. Ligue o suporte. 40% de preenchimento.', 3],
   [.66, 'Lingueta: deitada, 100% de preenchimento. Imprima duas, uma de reserva.', 4], [.78, 'Berço da base de carga: apoiado no lado maior, sem suporte.', 5]],
  over: {
   lid: {txt: 'Com a tampa virada na mesa, os LEDs e a chave da garra são presos pelo lado de dentro. Nesta variante a tampa já sai da impressora com os três rasgos e a bolsa onde o tecido dobra.',
    cfg: [['Rasgos', 'Três, de 22 × 3,6 mm, a cada 8 mm, com as bordas chanfradas.'], ['Bolsa', 'Caixa de 24 × 28 mm e 5,5 mm de fundo sob os rasgos. O tecido dobra ali dentro, longe dos fios.'], ['LEDs', 'Três furos de 8,6 mm, a cada 15 mm.'], ['Chave da garra', 'Fecha quando a garra abaixa.']],
    passos: [[0, 'Vire a tampa: o lado de dentro fica para cima. A bolsa dos rasgos aparece como uma caixinha.'], [.2, 'Encaixe os três LEDs do semáforo nos três furos e prenda com dois pingos de cola.'], [.5, 'Cole uma chave fim de curso ao lado do furo pequeno, com a haste sobre o pino branco.'], [.75, 'Passe o dedo dentro dos três rasgos: tem que estar liso. Lixe qualquer rebarba, porque ela rasga o tecido.']],
    man: {mats: ['Tampa com rasgos (impressa)', 'sem', 'chv', 'Cola instantânea em gel'], ferr: ['Lixa fina'], ok: 'Os LEDs aparecem nos furos, o pino branco da chave sobe e desce, e os rasgos estão lisos por dentro.', erros: ['Rebarba no rasgo: rasga o tecido.', 'Cola na ponta dos LEDs.']}},
   jaw: {txt: 'A garra desta variante tem três dedos no lugar dos dentes. Ao fechar, os dedos entram nos rasgos da tampa e levam o tecido junto. O gancho trava na lingueta, como na variante B.',
    cfg: [['Dedos', '22 × 2,4 × 8,6 mm. Entram cerca de 5,6 mm abaixo da face da tampa.'], ['Folga', 'Cerca de 0,6 mm de cada lado entre dedo e rasgo, para o tecido passar. Ajustar no teste.'], ['Gancho', 'O mesmo da variante B, com janela para a lingueta.'], ['Dobradiça', 'Parafuso M3 de 40 mm como eixo e mola de pregador.']],
    passos: [[0, 'Desvire a tampa e apoie sobre os módulos.'], [.3, 'Confira na garra que os três dedos estão retos. Feche a garra devagar, ainda sem eixo: cada dedo tem que entrar no seu rasgo sem raspar.'], [.45, 'Posicione a garra sobre os apoios da dobradiça, com o gancho apontando para o rasgo do gancho.'], [.65, 'Tire a mola de um pregador de roupa e encaixe entre os dois apoios da dobradiça.'], [.8, 'Passe o parafuso M3 de 40 mm e ponha a porca sem apertar: a garra tem que girar.']],
    man: {mats: ['Garra com dedos e gancho (impressa)', 'Mola de um pregador de roupa', 'Parafuso M3 de 40 mm com porca'], ferr: ['Lixa fina', 'Alicate de bico'], ok: 'A garra abre sozinha pela mola e, ao fechar, os três dedos entram nos rasgos e o gancho desce até a lingueta.', erros: ['Dedo torto: imprima a garra deitada, com os dedos para cima.', 'Folga pequena demais: tecido grosso não entra e a garra não trava.']}},
   f_lock: {txt: 'A garra fica aberta pela mola. O funcionário estende a borda da roupa sobre os rasgos e fecha a garra até o clique. Os dedos empurram o tecido para dentro da caixa.',
    cfg: [['Sem furo', 'O tecido é dobrado, não perfurado.'], ['Zigue-zague', 'O tecido desce e sobe em volta de cada dedo. Cada curva soma atrito.'], ['Clique', 'O gancho passa pela lingueta e a mola a devolve para a janela do gancho.']],
    passos: [[0, 'Garra aberta. A borda da roupa fica estendida sobre os três rasgos.'], [.36, 'Apertar a garra para baixo. Os dedos levam o tecido para dentro dos rasgos.'], [.6, 'Clique: a lingueta entrou no gancho. LED vermelho.']]},
   f_pull: {txt: 'Alguém segura a caixa e puxa a roupa. Para sair, o tecido teria de escorregar pelas curvas em volta dos três dedos, e o atrito cresce a cada curva.',
    cfg: [['Força', 'Pela equação do cabrestante, uma meia-volta com coeficiente de atrito de 0,5 multiplica a força por cerca de 4,8. Três meias-voltas dão cerca de 110 vezes. É estimativa: medir no ensaio.'], ['Limite', 'Quem segura de verdade passa a ser a lingueta e o gancho, que são de plástico.'], ['Alerta', 'Se a chave da garra abrir sem ordem, o painel da loja avisa.']]}
  }};
const varDe = v => VAR[v].herda ? [v, VAR[v].herda] : [v];   // variantes cujas peças e passos valem para v

// ---------- lista de compras (preços conferidos em 14/10/2026, frete para o CEP 05508-010) ----------
// uso por variante: o = obrigatório, r = reserva, x = opcional; ausente = não precisa
const LOJA = {
  'Usinainfo': {frete: 14.36, como: 'JT Express, 4 a 7 dias úteis. Calculado no carrinho com a lista completa'},
  'Amazon': {frete: 0, como: 'Entrega grátis mostrada na página. Itens importados chegam de 28/10 a 04/11'},
  'Magazine Luiza': {frete: 12.90, como: 'Só a base de indução paga frete. Estimativa da página para a região de Osasco'},
  '3D Fila': {frete: null, como: 'A cotar'},
  'Ímã de Neodímio': {frete: null, como: 'A cotar'}
};
const TODAS = {emb: 'o', lin: 'o', gar: 'o'};
const BUY = [
 {n: 'ESP32 DevKit V1 30 pinos, USB-C', q: 2, nota: '1 + 1 reserva', pix: 56.81, card: 59.80, loja: 'Usinainfo', f: 'Controlar', link: 'https://www.usinainfo.com.br/esp32/esp32-wifi-e-bluetooth-com-usb-c-30-pinos-e-cp2102-9114.html', uso: TODAS},
 {n: 'Expansor para ESP32 30 pinos', q: 1, pix: 21.19, card: 22.30, loja: 'Usinainfo', f: 'Controlar', link: 'https://www.usinainfo.com.br/expansores-shields/expansor-para-esp32-devkit-v1-30-pinos-usb-c-e-micro-8795.html', uso: TODAS},
 {n: 'Micro servo SG90', q: 3, nota: '1 + 2 reserva', pix: 14.16, card: 14.90, loja: 'Usinainfo', f: 'Liberar', link: 'https://www.usinainfo.com.br/servo-motores/micro-servo-motor-9g-sg90-180-16kgfcm-de-posicao-2299.html', uso: TODAS},
 {n: 'Micro servo MG90S, engrenagem metálica', q: 1, nota: 'se o SG90 não tiver força', pix: 34.87, card: 36.70, loja: 'Usinainfo', f: 'Liberar', link: 'https://www.usinainfo.com.br/servo-motores/micro-servo-9g-tower-pro-mg90s-180-22kgfcm-de-posicao-com-engrenagens-metalicas-3628.html', uso: {emb: 'r', lin: 'r', gar: 'r'}},
 {n: 'Módulo chave fim de curso', q: 3, nota: '2 + 1 reserva', pix: 4.79, card: 5.04, loja: 'Usinainfo', f: 'Controlar', link: 'https://www.usinainfo.com.br/sensor-de-vibracao/modulo-chave-fim-curso-sensor-de-impacto-para-projetos-4618.html', uso: TODAS},
 {n: 'Semáforo LED 8 mm', q: 2, nota: '1 + 1 reserva', pix: 7.78, card: 8.19, loja: 'Usinainfo', f: 'Indicar', link: 'https://www.usinainfo.com.br/outros-modulos-arduino/semaforo-led-33v5v-8mm-s3-5466.html', uso: TODAS},
 {n: 'Jumper fêmea-fêmea 20 cm, kit 20', q: 1, pix: 5.79, card: 6.09, loja: 'Usinainfo', f: 'Controlar', link: 'https://www.usinainfo.com.br/jumper/jumper-premium-para-protoboard-femea-femea-20cm-kit-c-20-pecas-2612.html', uso: TODAS},
 {n: 'Jumper macho-fêmea 20 cm, kit 20', q: 1, pix: 5.79, card: 6.09, loja: 'Usinainfo', f: 'Controlar', link: 'https://www.usinainfo.com.br/jumper/jumper-premium-para-protoboard-macho-femea-20cm-kit-c-20-pecas-2314.html', uso: TODAS},
 {n: 'Capacitor eletrolítico 1000 µF 16 V', q: 2, nota: '1 + 1 reserva', pix: 1.94, card: 2.04, loja: 'Usinainfo', f: 'Energia', link: 'https://www.usinainfo.com.br/capacitor-eletrolitico/capacitor-eletrolitico-1000uf-16v-3052.html', uso: TODAS},
 {n: 'Etiqueta rígida antifurto com pino, pacote 20 (dela sai a embreagem)', q: 1, nota: '20 embreagens e 20 pinos', pix: 64.84, card: 64.84, loja: 'Amazon', f: 'Reter', link: 'https://www.amazon.com.br/dp/B0GP6ZF16R', uso: {emb: 'o'}, aviso: 'Só 1 em estoque e vem do exterior: comprar logo'},
 {n: 'Ímã de neodímio N50 10 × 4 mm, kit 10', q: 1, nota: 'usa 3', pix: 21.48, card: 22.61, loja: 'Usinainfo', f: 'Liberar', link: 'https://www.usinainfo.com.br/imas-de-neodimio-e-acessorios-magneticos/ima-de-neodimio-n50-super-forte-10mm-x-4mm-kit-com-10-unidades-5012.html', uso: {emb: 'o'}},
 {n: 'Kit de molas de compressão e extensão, 200 peças', q: 1, nota: 'mola da lingueta', pix: 44.49, card: 46.83, loja: 'Usinainfo', f: 'Reter', link: 'https://www.usinainfo.com.br/robotica-educacional/kit-de-molas-para-robotica-200-pecas-mola-de-compressao-e-extensao-para-projetos-diy-5160.html', uso: {emb: 'r', lin: 'o', gar: 'o'}},
 {n: 'Power bank Basike 10.000 mAh com visor', q: 1, pix: 95.00, card: 95.00, loja: 'Amazon', f: 'Energia', link: 'https://www.amazon.com.br/dp/B0DHVLRFGD', uso: TODAS},
 {n: 'Receptor de carga sem fio Qi, USB-C', q: 1, pix: 67.93, card: 78.99, loja: 'Magazine Luiza', f: 'Energia', link: 'https://www.magazineluiza.com.br/adaptador-sem-fio-wireless-qi-inducao-receptor-universal-tipo-c-brasil-home/p/gkj66889f8/in/usba/', uso: TODAS},
 {n: 'Carregador por indução Lelong LE-520 (base)', q: 1, pix: 30.74, card: 30.74, loja: 'Magazine Luiza', f: 'Energia', link: 'https://www.magazineluiza.com.br/carregador-por-inducao-15w-sem-fio-usb-acompanha-cabo-usb-c-le520-lelong/p/ke9dh49dk3/te/accp/', uso: TODAS},
 {n: 'Kit de parafusos inox M2 a M5, 120 peças', q: 1, pix: 18.72, card: 18.72, loja: 'Amazon', f: 'Montar', link: 'https://www.amazon.com.br/dp/B0GS5M3LC5', uso: TODAS},
 {n: 'Filamento PLA preto 1,75 mm, 1 kg', q: 1, nota: 'dispensável se o laboratório tiver', pix: 89.90, card: 97.09, loja: '3D Fila', f: 'Montar', link: 'https://3dfila.com.br/produto/filamento-pla-preto/', uso: TODAS},
 {n: 'Etiqueta NFC NTAG215, kit 10', q: 1, nota: 'pagar encostando o celular', pix: 23.90, card: 23.90, loja: 'Amazon', f: 'Identificar', link: 'https://www.amazon.com.br/dp/B0CKTK9HSJ', uso: {emb: 'x', lin: 'x', gar: 'x'}},
 {n: 'Ímã de neodímio N42 20 × 10 mm', q: 1, nota: 'se os ímãs pequenos não abrirem', pix: 24.87, card: 24.87, loja: 'Ímã de Neodímio', f: 'Liberar', link: 'https://www.imadeneodimio.com/ima-de-neodimio-disco-20mm-x-10mm-n42', uso: {emb: 'x'}}
];
const CASA_ZERO = ['mola de pregador de roupa', 'fita dupla face', 'cola instantânea em gel', 'borracha (câmara de ar ou fita antiderrapante)', 'papel adesivo para o QR', 'mola de caneta, se não comprar o kit de molas'];
// total da variante: itens obrigatórios e reservas, mais o frete das lojas usadas
function totalVar(v, campo = 'pix') { let t = 0; const lojas = new Set();
  BUY.forEach(b => { const u = b.uso[v]; if (u == 'o' || u == 'r') { t += b.q * b[campo]; lojas.add(b.loja); } });
  let fr = 0; const cotar = []; lojas.forEach(l => { if (LOJA[l].frete == null) cotar.push(l); else fr += LOJA[l].frete; });
  return {itens: t, frete: fr, total: t + fr, cotar}; }
function etapaDe(v, id) { const b = ETAPA[id] || {}, h = VAR[v].herda, o = VAR[v].over[id] || (h && VAR[h].over[id]) || {}; return {tit: o.tit || b.tit, txt: o.txt || b.txt, cfg: o.cfg || b.cfg || [], passos: o.passos || b.passos, man: o.man || b.man || {}}; }
function estadoId(id, p) { return estado(IDS.indexOf(id), p); }
