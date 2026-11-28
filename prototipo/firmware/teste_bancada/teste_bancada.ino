// Tag&Go – teste de bancada (sem Wi-Fi). Confere ligações, LEDs, chave e servo
// antes de juntar com o firmware do servidor (prototipo/software/plano-desenvolvimento.md).
//
// Placa: "ESP32 Dev Module". Biblioteca: ESP32Servo (Gerenciador de Bibliotecas).
// Monitor Serial a 115200. Comandos: t = travar, l = liberar, s = estado.
//
// Ligações (tabela completa em prototipo/LIGACOES.md):
//   Servo        sinal GPIO 13 (laranja S), 5 V (vermelho V), GND (marrom G)
//   Chave        OUT -> GPIO 27 (S), GND -> G.  VCC NÃO LIGA (usa pull-up interno: o pino nunca recebe 5 V)
//   Semáforo     R -> 26, Y -> 33, G -> 25, GND -> G
//   Capacitor    1000 uF: + no V e − no G da coluna do GPIO 12 (segura o pico do servo)
//   Alimentação  power bank -> USB-C do EXPANSOR (não do ESP32). Jumper do expansor em 5 V.

#include <ESP32Servo.h>

// ----- escolha a versão -----
#define VERSAO_A 1          // 1 = garra com dentes (lingueta), 0 = etiqueta de loja + ímãs

const int PINO_SERVO = 13;
const int PINO_CHAVE = 27;
const int LED_R = 26, LED_Y = 33, LED_G = 25;

#if VERSAO_A
const int ANG_TRAVA = 40;   // lingueta dentro do gancho
const int ANG_SOLTA = 90;   // lingueta recuada 4,6 mm
#else
const int ANG_TRAVA = 0;    // ímãs longe da embreagem (repouso)
const int ANG_SOLTA = 120;  // ímãs embaixo da embreagem
#endif

// Medir no Monitor Serial e ajustar: com pull-up, a chave apertada costuma dar LOW.
const int NIVEL_APERTADA = LOW;

Servo servo;
bool travada = false;

void leds(bool r, bool y, bool g) {
  digitalWrite(LED_R, r); digitalWrite(LED_Y, y); digitalWrite(LED_G, g);
}

void moverServo(int ang) {
  servo.attach(PINO_SERVO, 500, 2400);
  servo.write(ang);
  delay(600);
  servo.detach();            // sem sinal o servo não esquenta; a lingueta fica parada pelo atrito das engrenagens
}

bool garraFechada() {
  int a = digitalRead(PINO_CHAVE);
  delay(50);
  return a == digitalRead(PINO_CHAVE) && a == NIVEL_APERTADA;
}

void travar()  { moverServo(ANG_TRAVA); travada = true;  leds(1, 0, 0); Serial.println("TRAVADA"); }
void liberar() { moverServo(ANG_SOLTA); travada = false; leds(0, 0, 1); Serial.println("LIBERADA"); }

void setup() {
  Serial.begin(115200);
  pinMode(LED_R, OUTPUT); pinMode(LED_Y, OUTPUT); pinMode(LED_G, OUTPUT);
  pinMode(PINO_CHAVE, INPUT_PULLUP);
  // teste dos LEDs
  leds(1, 0, 0); delay(400); leds(0, 1, 0); delay(400); leds(0, 0, 1); delay(400);
  moverServo(ANG_SOLTA);     // começa destravada
  leds(0, 1, 0);
  Serial.println("Pronto. t = travar, l = liberar, s = estado");
}

bool fechadaAntes = false;

void loop() {
  bool fechada = garraFechada();
#if VERSAO_A
  // A: a garra fechou -> trava sozinha. Abriu depois de liberar -> volta ao amarelo.
  if (fechada && !fechadaAntes && !travada) travar();
  if (!fechada && fechadaAntes && !travada) leds(0, 1, 0);
#endif
  if (fechada != fechadaAntes) { Serial.print("chave: "); Serial.println(fechada ? "apertada" : "solta"); }
  fechadaAntes = fechada;

  if (Serial.available()) {
    char c = Serial.read();
    if (c == 't') travar();
    if (c == 'l') liberar();
    if (c == 's') { Serial.print(travada ? "travada" : "livre"); Serial.print(", chave "); Serial.println(fechada ? "apertada" : "solta"); }
  }
  delay(20);
}
