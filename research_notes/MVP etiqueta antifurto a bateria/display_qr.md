# Displaying a QR code on a battery-powered ESP32 tag (Tag&Go MVP): e-paper vs OLED vs printed sticker

Research date: 2026-09-29. Demo date: 07/12/2026 (about 10 weeks away). Several retailer pages (MakerHero, Mercado Livre, Medium, Santander) returned HTTP 403 to the fetch tool, so some prices come from search snippets and are flagged as such.

## 1. E-paper modules: zero-power persistence, refresh, current, wiring, GxEPD2 class, pitfalls

### Takeaway
E-paper is the only screen option that meets the "QR has to stay on" requirement with zero power. The image stays after power is removed, and standby current is below 0.01 uA. For a new QR, a full refresh takes about 2-2.6 s at roughly 26 mW. The recommended part is the WeAct 1.54" 200x200 black/white module (SSD1681 controller). In GxEPD2 it uses `GxEPD2_BW<GxEPD2_154_D67, GxEPD2_154_D67::HEIGHT>`, with 8 wires on SPI at 3.3 V.

### Cited Findings
- Waveshare 1.54" e-Paper module specs: 200x200, black/white, SPI (Mode 0), 8-pin connector VCC/GND/DIN/CLK/CS/DC/RST/BUSY, supply 3.3 V/5 V, refresh time 2 s, refresh power 26.4 mW (typ.), standby current "< 0.01uA (almost none)", and the image is retained without power — [Waveshare wiki, 1.54inch e-Paper Module Manual](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_Manual)
- Waveshare precautions:
  - "After refreshing partially several times, you need to fully refresh EPD once. Otherwise, the display effect will be abnormal, which cannot be repaired!"
  - Do not leave the panel powered for long periods; put it in sleep mode or power it off when idle.
  - Recommended minimum refresh interval is 180 s.
  - The FPC ribbon is fragile.
  - Operating temperature is 0-50 °C.
  - [Waveshare wiki](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_Manual)
- The Waveshare product page lists the 1.54" module as having an "embedded controller" and supporting partial refresh. It keeps showing the last content for a long time after power-down. — [Waveshare product page](https://www.waveshare.com/1.54inch-e-paper-module.htm) (via search snippet)
- GxEPD2 driver constants for `GxEPD2_154_D67` (200x200):
  - `hasPartialUpdate = true`, `hasFastPartialUpdate = true`
  - `power_on_time = 100` ms, `power_off_time = 150` ms
  - `full_refresh_time = 2600` ms (measured 2509602 us), `partial_refresh_time = 500` ms (measured 457282 us)
  - [GxEPD2 source, src/epd/GxEPD2_154_D67.h](https://github.com/ZinggJM/GxEPD2)
- GxEPD2 README panel-to-class mapping: GDEH0154D67 (SSD1681) → `GxEPD2_154_D67`; GDEY0154D67 (SSD1681) → `GxEPD2_154_GDEY0154D67`; GDEY0213B74 (SSD1680) → `GxEPD2_213_B74`; GDEY029T94/GDEM029T94 (SSD1680) → `GxEPD2_290_T94` — [GxEPD2 README](https://github.com/ZinggJM/GxEPD2)
- GxEPD2 README on voltage:
  - "The display panels are for 3.3V supply and 3.3V data lines"; do not connect 5 V directly.
  - With 5 V MCUs, a 4k7/10k resistor divider is required, and a "series resistor only is not enough for reliable operation".
  - Newer Waveshare boards have level converters and regulators on board.
  - Use `init(115200, true, 2, false)` for Waveshare boards with the "clever" reset circuit.
  - [GxEPD2 README](https://github.com/ZinggJM/GxEPD2)
- WeAct's official ESP32 example (EpaperModuleTest_Arduino_ESP32.ino):
  - Pins: `CS_PIN 5`, `BUSY_PIN 4`, `RES_PIN 16`, `DC_PIN 17`, with SCK=18 and MOSI (labelled SDA)=23.
  - 1.54" constructor: `GxEPD2_BW<GxEPD2_154_D67, GxEPD2_154_D67::HEIGHT> display(GxEPD2_154_D67(CS_PIN, DC_PIN, RES_PIN, BUSY_PIN)); // GDEH0154D67 200x200, SSD1681`.
  - Init is `display.init(115200,true,50,false)`, and the sketch ends with `display.hibernate()`.
  - Note: the comment line in the same file says "RES(RST)=17, DC=16", which is the reverse of the `#define`s. Follow the `#define`s, or pick your own pins and keep the code in sync.
  - [WeAct example, ESP32](https://github.com/WeActStudio/WeActStudio.EpaperModule/blob/master/Example/EpaperModuleTest_Arduino_ESP32/EpaperModuleTest_Arduino_ESP32.ino)
- WeAct's ESP32-C3 example uses CS(SS)=7, SCK=4, MOSI=6, BUSY=3, RES=2, DC=1, with the same GxEPD2 constructors — [WeAct example, ESP32-C3](https://github.com/WeActStudio/WeActStudio.EpaperModule/blob/master/Example/EpaperModuleTest_Arduino_ESP32C3/EpaperModuleTest_Arduino_ESP32C3.ino)
- The same WeAct examples give the classes for the larger WeAct modules:
  - 2.13" B/W: `GxEPD2_213_BN` (DEPG0213BN 122x250, SSD1680)
  - 2.9" B/W: `GxEPD2_290_BS` (DEPG0290BS 128x296, SSD1680)
  - 1.54" 4-color: `GxEPD2_154c_GDEM0154F51H` (JD79660)
  - These differ from the Good Display part numbers in the GxEPD2 README, so use the WeAct example's class for WeAct modules. — [WeAct example](https://github.com/WeActStudio/WeActStudio.EpaperModule/blob/master/Example/EpaperModuleTest_Arduino_ESP32/EpaperModuleTest_Arduino_ESP32.ino)
- WeAct's Doc folder includes the SSD1680, SSD1681 and SSD1683 datasheets, plus the datasheet of the ME6231A33M3G (a 3.3 V LDO). The 1.54" B/W panel doc is part "YRD0150BBS810F0MP-M7". — [WeAct repo Doc folder](https://github.com/WeActStudio/WeActStudio.EpaperModule) (listed via GitHub API)
- A Brazilian retailer listing for a 1.54" 200x200 e-paper module gives 0.3 s partial and 2 s full refresh, 26.4 mW typical during update and <0.017 mW standby. The same listing also says "red and black", which is inconsistent, so confirm it is the B/W version. — [Eletrodex](https://www.eletrodex.net/display-e-paper-1-54-200x200)
- Several people have used WeAct 1.54" + GxEPD2_154_D67 on ESP32 variants: a Medium write-up with ESP32-H2 Super Mini, and a Digital Concepts page — [Medium/AndroidCrypto](https://medium.com/@androidcrypto/commissioning-of-a-1-54-inch-e-paper-display-from-weact-to-an-esp32-h2-super-mini-development-board-c340cdc9a507) (403 on fetch; seen via search snippet), [Digital Concepts](https://digitalconcepts.net.au/arduino/index.php?op=ePaperDisplay)

### Inferences
- Zero-power persistence: the "must stay on" requirement is met physically. The ESP32 draws the QR once, calls `display.hibernate()`, and can then deep-sleep or even be switched off. The QR stays visible until the next refresh.
- Refresh current: 26.4 mW at 3.3 V is about 8 mA for about 2.6 s per full refresh, so roughly 0.006 mAh per new QR. That is negligible next to the ESP32's Wi-Fi/BLE consumption.
- Wiring for ESP32 DevKit v1 + WeAct 1.54" (no soldering if the module has a header; female-female Dupont jumpers):

  | Module | ESP32 DevKit | ESP32-C3 (WeAct example) |
  |---|---|---|
  | VCC | 3V3 | 3V3 |
  | GND | GND | GND |
  | SDA/DIN (MOSI) | GPIO23 | GPIO6 |
  | SCL/CLK (SCK) | GPIO18 | GPIO4 |
  | CS | GPIO5 | GPIO7 |
  | DC | GPIO17 | GPIO1 |
  | RES/RST | GPIO16 | GPIO2 |
  | BUSY | GPIO4 | GPIO3 |

  - Power the module from 3V3, never 5 V, to stay inside the GxEPD2 3.3 V rule even if the board has an LDO.
- Pitfalls to brief the team on:
  1. **BUSY pin.** If BUSY is miswired or floating, GxEPD2 waits on it and the screen never updates or times out. Check BUSY first when "nothing happens".
  2. **Fragile ribbon.** Do not bend the FPC ribbon; glue the module into the 3D-printed case by its PCB, not by the glass.
  3. **Full refresh for every new QR, partial only for small text.**
     - Draw every new QR with a full refresh. Ghosting from repeated partial refreshes could leave faint old modules that confuse scanners.
     - Partial refresh (0.5 s) is fine for a small "PAGO / LIBERADO" status line, followed by a full refresh at the next session.
  4. **Refresh interval.** The 180 s minimum interval is a longevity recommendation. A demo refreshing every minute or so for one day is not a real risk.
  5. **Temperature.** 0-50 °C is fine for a demo room.
  6. **Colour choice.** Choose B/W, not 3-color (red/yellow). 3-color panels typically do not support partial refresh and refresh much more slowly. This is general knowledge, not verified in this session; the WeAct example uses different classes (`GxEPD2_3C`) for them.
- Size choice for QR use:
  - 1.54" 200x200 (active area about 27.6 mm square, about 0.14 mm pixels) comfortably fits a version 3-4 QR at 4-5 px per module, i.e. 18-20 mm wide, and still leaves room for a text line.
  - 2.13" 250x122 has only 122 px of height. It fits V3/V4 at 3 px per module (about 17-19 mm) with room beside it for status text.
  - 2.9" 296x128 gives about 20-22 mm QRs plus a wide text area, but is physically larger for a garment tag.

### Gaps
- Could not fetch WeAct's own spec sheet text: the README is only images. Exact WeAct refresh times/currents, whether the module ships with a pre-soldered 8-pin header and cable, and whether its on-board LDO makes it 5 V-supply tolerant are not confirmed. The ME6231A33 datasheet in the repo suggests an on-board 3.3 V regulator.
- No independent measurement of WeAct 1.54" refresh current found; the 26.4 mW figure is Waveshare's.

## 2. OLED 0.96" SSD1306 / 1.3" SH1106: scan reliability, current, burn-in, button-press use

### Takeaway
A QR on a 128x64 OLED can be scanned, but only with small codes. The 64-pixel height limits you to QR version 2-3 at 2 px per module, which gives a QR only about 10 mm wide on a 0.96" panel (about 13 mm on a 1.3"). That is below the commonly cited 2x2 cm minimum. The OLED also goes dark when off, drawing about 1.4-7 mA while lit, and it burns in with static images. Use it for status or for an on-button-press QR, not for an always-on QR.

### Cited Findings
- Eletrogate 0.96" OLED: 128x64, SSD1306, I2C, 3-5 V supply, 3.3 V and 5 V logic, 30x27 mm, pins GND/VCC/SCL/SDA, and a variant "com os pinos soldados" (pre-soldered pins) — [Eletrogate](https://www.eletrogate.com/display-oled-0-96-i2c-azul)
- Measured SSD1306 128x64 current scales linearly with lit pixels (R² > 0.999):
  - I(mA) = 0.054124 × fill% + 1.444 at contrast 0x7F
  - I(mA) = 0.047538 × fill% + 1.397 at contrast 0x01
  - Quiescent current is about 1.4 mA.
  - [Harris' Electronics, SSD1306 power consumption](https://hsel.co.uk/2018/12/04/ssd1306-power-consumption/)
- Other reports: "about 25 mA at full brightness and about 1.5 mA when off" per a module listing. Adafruit forum users measured 0.22-0.25 mA (down to 0.011 mA) in sleep mode, and about 1.1 uA after desoldering capacitors. The 25 mA figure conflicts with the hsel measurement (max about 6.9 mA at 100% fill). — [Adafruit forum](https://forums.adafruit.com/viewtopic.php?t=41332), [Electropeak listing](https://electropeak.com/0-96-inch-i2c-oled-display-module-ssd1306) (both via search summary; not fetched)
- An ESP8266 + 128x64 OLED QR project scales the QR 2x ("each QR code pixel shows up as four pixels on the OLED"). Its author notes that "codes seem to scan much better with lit background", i.e. dark modules on lit pixels. — [PhillipJacobsen/Generate-Display-QRcode-on-OLED](https://github.com/PhillipJacobsen/Generate-Display-QRcode-on-OLED)
- A search summary of SSD1306 QR tutorials says one implementation found scale 1 easier for phones than scale 2. This is anecdotal and contradicts the PhillipJacobsen 2x approach. — [Wokwi/Hackster SSD1306 QR examples](https://www.hackster.io/Hack-star-Arduino/arduino-simulator-qr-code-generation-on-arduino-ssd1306-786044) (search snippet)
- A simulated ESP32 + SSD1306 dynamic QR project exists on Wokwi and can be tried in the browser before buying hardware — [Wokwi "Dynamic QRcode ssd1306 and ESP32"](https://wokwi.com/projects/387371909460858881)
- General QR sizing guidance: the standard minimum is about 2x2 cm, which modern phones scan from about 25 cm (10 in) — [useqrkit](https://useqrkit.com/blog/qr-code-minimum-size) (search snippet)
- Burn-in:
  - Users report SSD1306 modules showing burned pixels within 2-4 months of constant static content — [esphome feature-requests #624](https://github.com/esphome/feature-requests/issues/624) (via search summary)
  - T50 (half brightness) is about 5,000-10,000 h at full contrast; lowering contrast extends it — [Zbotic](https://zbotic.in/oled-display-burn-in-how-to-prevent-pixel-degradation/) (secondary source, via search summary)

### Inferences
- **0.96" geometry.** From the 0.96" diagonal at 2:1, the active area is about 21.8 x 10.9 mm and the pixel pitch about 0.17 mm. With only 64 px of height:
  - V2 (25 modules) at 2x = 50 px, which leaves a quiet zone of about 3.5 modules.
  - V3 (29 modules) at 2x = 58 px, which leaves only about 1.5 modules of quiet zone vertically. That is marginal, since the spec wants 4, but phones usually tolerate less.
  - V4 (33 modules) at 2x = 66 px does not fit, so V4 only works at 1x (about 5.6 mm wide, unreliable).
  - The realistic maximum on the 0.96" is V3 at 2x, a QR about 10 mm wide. That means at most 53 bytes at ECC L or 42 at ECC M (see section 5). The phone must be held close (about 5-10 cm), where some phones struggle to focus.
- **1.3" SH1106.** Same 128x64 resolution, larger pixels: about 29.5 x 14.8 mm active area, about 0.23 mm pitch. V3 at 2x becomes about 13 mm wide, which is better but still under 2 cm.
- **Current.** A lit-background QR is about 70-85% of pixels on, i.e. about 5-6 mA at full contrast from the hsel formula. The SSD1306 keeps showing its RAM contents while the ESP32 deep-sleeps, as long as the OLED stays powered. Always-on OLED is therefore about 120-150 mAh/day for the OLED alone. That is OK for a one-day demo on a 1000 mAh cell, but it contradicts "low power" and risks burn-in over weeks.
- **Button-press pattern.** If the OLED is used, show the QR only on a button press (or on tag pickup), for 30-60 s, then send display-off (SSD1306 command 0xAE) and deep-sleep. This removes the burn-in and battery objections, but a shopper sees a blank tag until they press the button.
- **Wiring.** OLED wiring is simpler than e-paper: 4 wires, VCC→3V3, GND, SDA→GPIO21, SCL→GPIO22 on ESP32 DevKit (the default I2C pins). The typical I2C address is 0x3C.

### Gaps
- No controlled test found of phone-scan success rate versus QR version and scale on a 0.96" OLED. The claims are anecdotal and conflicting (1x vs 2x).
- SH1106 1.3" Brazilian retail price was not found.

## 3. Printed QR sticker vs screen: when is a sticker enough, and what does a dynamic QR add?

### Takeaway
A printed sticker with a static URL (`...?t=<tagID>`) is enough to open the payment page. It costs nothing, needs no power and scans best. A screen adds real value only if the tag generates a per-session nonce and checks it at unlock time, which is anti-replay, and shows status (PAGO/LIBERADO). Note that a static site such as GitHub Pages cannot check a nonce itself. The check has to happen on the ESP32 or on a backend.

### Cited Findings
- ESP32 `esp_random()` returns a 32-bit word from the hardware RNG. It gives true random numbers only when:
  - Wi-Fi or Bluetooth is enabled (the RF subsystem supplies entropy), or
  - `bootloader_random_enable()` has been called, or
  - it runs during the bootloader.
  - Otherwise the output "should be considered as pseudo-random only."
  - [Espressif ESP-IDF Random Number Generation docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/random.html)
- About 2x2 cm is the reliable minimum QR size for phones at about 25 cm; a printed sticker can easily be 2.5-3 cm — [useqrkit](https://useqrkit.com/blog/qr-code-minimum-size) (search snippet)

### Inferences
- **What a static sticker does and doesn't do.** A static sticker exposes a fixed URL. Anyone who photographs it can open that tag's payment page later. On its own that is harmless as long as paying releases only this tag, and only when the phone is physically next to it. Security therefore comes from how the unlock command is authorized, not from the QR.
- **Anti-replay design that works without a server (fits GitHub Pages):**
  1. At session start (button press or tag pickup), the ESP32 generates a nonce `n = esp_random()` with the radio on, stores it (e.g. in an `RTC_DATA_ATTR` variable so it survives deep sleep), and draws the QR `https://<user>.github.io/tg/?t=01&n=7F3A9C1B`.
  2. The payment page (static) simulates payment and then sends the unlock command to the tag, carrying the same `n`. It sends this over Web Bluetooth or Wi-Fi to the ESP32; the unlock channel is covered by other research notes.
  3. The ESP32 releases the tag only if `n` matches the current session nonce, then immediately generates a new nonce and redraws. A screenshot of an old QR is now useless. This is the demo-able "dynamic QR" story.
- **Status display.** The e-paper can show "PAGO - LIBERADO ✓" after unlock, and it persists with zero power. That is useful demo feedback that a sticker cannot give; a sticker needs an LED or buzzer instead.
- **Demo fallback.** Even if the team builds a screen, put a printed sticker with the static URL on the back of the tag (or on a card) as a fallback. That way the live demo on 07/12 does not depend on the display working.

### Gaps
- No source found on real retail anti-theft tags using dynamic QR; the anti-replay argument above is design reasoning, not a cited practice.

## 4. Libraries and on-device QR generation; example code

### Takeaway
Use GxEPD2 for e-paper and Adafruit_SSD1306 + Adafruit_GFX (or U8g2) for OLED. For QR generation use ricmoo's QRCode library, which has an MIT license, uses stack-only memory and supports versions 1-40 with ECC L/M/Q/H. On current ESP32 Arduino cores it has a header-name clash with the core's own `qrcode.h`. The known fix is to rename the library files.

### Cited Findings
- ricmoo QRCode API:
  - `QRCode qrcode; uint8_t qrcodeBytes[qrcode_getBufferSize(...)]; qrcode_initText(&qrcode, qrcodeBytes, 3, ECC_LOW, "HELLO WORLD");`, then read modules with `qrcode_getModule(&qrcode, x, y)`.
  - Size = 4 × version + 17 modules.
  - "stack-based (no heap necessary)", MIT license.
  - [ricmoo/QRCode](https://github.com/ricmoo/QRCode)
- Issue #35 "Doesn't work with latest esp32 boards in Arduino IDE" — [ricmoo/QRCode #35](https://github.com/ricmoo/QRCode/issues/35). The workaround comment:
  - Rename `qrcode.h`/`qrcode.c` to e.g. `qrcoderm.h`/`qrcoderm.c` and rename the library folder.
  - Change the include on line 33 of the `.c` file.
  - Use `#include <qrcoderm.h>`.
  - [issue comment 1179311130](https://github.com/ricmoo/QRCode/issues/35#issuecomment-1179311130)
- ePaper-writer (ESP32 + WeAct 2.13" + GxEPD2 + qrcode) confirms "the qrcode library has a naming conflict with a qrcode.h from the ESP32 core", links the same fix, and says to restart the Arduino IDE afterwards — [ftjuh/ePaper-writer](https://github.com/ftjuh/ePaper-writer)
- Other working examples:
  - [G6EJD/ESP32-e-paper-QRcode-generator](https://github.com/G6EJD/ESP32-e-paper-QRcode-generator): ESP32 + e-paper QR
  - [geprc/QRcode_EPD](https://github.com/geprc/QRcode_EPD): QR library for e-ink, tested on ESP32
  - [Arduino forum: Drawing qrcode with GxEPD2 on 1.54 eink](https://forum.arduino.cc/t/drawing-qrcode-with-gxepd2-on-1-54-eink-display/645392)
  - [Arduino++ blog: ePaper QR Code Display](https://arduinoplusplus.wordpress.com/2022/01/23/epaper-qr-code-display/)
  - [yoprogramo/ESP_QRcode](https://github.com/yoprogramo/ESP_QRcode): SSD1306/SH1106/TFT/E-INK, but marked obsolete in favour of the QRcodeDisplay project
- The WeAct example sketches use GxEPD2's page loop, `setPartialWindow()`, checks of `display.epd2.hasFastPartialUpdate`, and `display.hibernate()` — [WeAct example](https://github.com/WeActStudio/WeActStudio.EpaperModule/blob/master/Example/EpaperModuleTest_Arduino_ESP32/EpaperModuleTest_Arduino_ESP32.ino)

### Inferences

#### E-paper code pattern
This pattern was composed from the cited APIs and is not compiled/tested in this session. Libraries to install: GxEPD2 (+ Adafruit GFX, pulled in automatically) and QRCode by Richard Moore, renamed as above.

```cpp
#include <GxEPD2_BW.h>
#include <qrcoderm.h>            // ricmoo QRCode, renamed to avoid ESP32-core qrcode.h clash
#include <Fonts/FreeSans9pt7b.h>
#define CS_PIN 5
#define DC_PIN 17
#define RES_PIN 16
#define BUSY_PIN 4               // SCK=18, MOSI=23 (ESP32 VSPI defaults)
GxEPD2_BW<GxEPD2_154_D67, GxEPD2_154_D67::HEIGHT>
  display(GxEPD2_154_D67(CS_PIN, DC_PIN, RES_PIN, BUSY_PIN));

RTC_DATA_ATTR uint32_t nonce;    // survives deep sleep

void drawQR(const char* url, const char* status) {
  QRCode qr;
  uint8_t buf[qrcode_getBufferSize(4)];
  qrcode_initText(&qr, buf, 4, ECC_MEDIUM, url);   // V4 = 33x33, up to 62 bytes at ECC M
  const int s = 4;                                  // 33*4 = 132 px (~18 mm)
  const int ox = (200 - qr.size * s) / 2, oy = 16;
  display.setFullWindow();                          // full refresh for every new QR (no ghosting)
  display.firstPage();
  do {
    display.fillScreen(GxEPD_WHITE);
    for (uint8_t y = 0; y < qr.size; y++)
      for (uint8_t x = 0; x < qr.size; x++)
        if (qrcode_getModule(&qr, x, y))
          display.fillRect(ox + x * s, oy + y * s, s, s, GxEPD_BLACK);
    display.setFont(&FreeSans9pt7b);
    display.setTextColor(GxEPD_BLACK);
    display.setCursor(10, 190);
    display.print(status);                          // e.g. "Tag 01 - aponte a camera"
  } while (display.nextPage());
  display.hibernate();                              // panel draws ~0 A, image stays
}

void setup() {
  display.init(115200, true, 50, false);            // as in WeAct's example
  nonce = esp_random();                             // true random only with Wi-Fi/BLE on
  char url[64];
  snprintf(url, sizeof(url), "https://usuario.github.io/tg/?t=01&n=%08lX", (unsigned long)nonce);
  drawQR(url, "Tag 01 - aponte a camera");
}
void loop() {}
```

#### OLED code pattern
This uses the standard Adafruit_SSD1306 API, not re-verified in this session.

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <qrcoderm.h>
Adafruit_SSD1306 oled(128, 64, &Wire, -1);
void showQR(const char* url) {
  QRCode qr; uint8_t buf[qrcode_getBufferSize(3)];
  qrcode_initText(&qr, buf, 3, ECC_LOW, url);       // V3 = 29x29, max 53 bytes at ECC L
  const int s = 2, ox = (128 - qr.size*s)/2, oy = (64 - qr.size*s)/2;
  oled.fillScreen(SSD1306_WHITE);                   // lit background scans better
  for (uint8_t y = 0; y < qr.size; y++)
    for (uint8_t x = 0; x < qr.size; x++)
      if (qrcode_getModule(&qr, x, y))
        oled.fillRect(ox + x*s, oy + y*s, s, s, SSD1306_BLACK);
  oled.display();
}
// setup: Wire.begin(); oled.begin(SSD1306_SWITCHCAPVCC, 0x3C);
// after 60 s: oled.ssd1306_command(SSD1306_DISPLAYOFF);
```

- For SH1106 1.3", Adafruit_SSD1306 does not drive it correctly. Use U8g2 (`U8G2_SH1106_128X64_NONAME_F_HW_I2C`) or Adafruit_SH110X instead. This is general knowledge, not verified in this session.
- Beginners can prototype the whole OLED+QR flow in the Wokwi simulator linked in section 2 before the parts arrive.

### Gaps
- Did not verify whether a maintained, drop-in ESP32-safe fork of ricmoo QRCode exists in the Arduino Library Manager under a non-clashing header name. The rename workaround is the only cited fix.
- Did not verify the exact SH1106 library class names against current library docs.

## 5. URL length vs QR version vs screen resolution; recommended URL format

### Takeaway
Keep the URL at 53 bytes or less, which fits QR version 3 at ECC L (29x29) or version 4 at ECC M (33x33, up to 62 bytes). A GitHub Pages URL with a short repo name and one-letter parameters (`https://<user>.github.io/tg/?t=01&n=7F3A9C1B`) is about 40-50 characters. Byte mode applies, because `?`, `=` and `&` are not in the QR alphanumeric set.

### Cited Findings
- QR capacity from the ricmoo README, as byte mode (and alphanumeric mode) at ECC L / ECC M:

  | Version (modules) | Byte, ECC L | Byte, ECC M | Alphanumeric, ECC L | Alphanumeric, ECC M |
  |---|---|---|---|---|
  | V1 (21x21) | 17 | 14 | 25 | 20 |
  | V2 (25x25) | 32 | 26 | 47 | 38 |
  | V3 (29x29) | 53 | 42 | 77 | 61 |
  | V4 (33x33) | 78 | 62 | 114 | 90 |
  | V5 (37x37) | 106 | 84 | 154 | 122 |
  | V6 (41x41) | 134 | 106 | 195 | 154 |

  — [ricmoo/QRCode README](https://github.com/ricmoo/QRCode)
- Size = 4 × version + 17 modules — [ricmoo/QRCode](https://github.com/ricmoo/QRCode)

### Inferences
- URL length examples:
  - `https://usuario.github.io/tg/?t=01&n=7F3A9C1B` = 45 characters, which fits V3 at ECC L and V4 at ECC M.
  - With a longer username and repo name (e.g. `https://nomegrande.github.io/tagandgo/?t=01&n=7F3A9C1B`) it reaches about 55 characters, which pushes to V4 at ECC L.
- Keep the URL short:
  - short repo name
  - one-letter parameter names
  - 2-digit tag ID
  - 8 hex characters of nonce (32 bits)
  - include the trailing `/` before `?` to avoid a GitHub Pages redirect
- Fit per screen, with a 4-module quiet zone unless noted:

  | Screen | Fits |
  |---|---|
  | 1.54" 200x200 | V3 at 5 px per module (185 px incl. quiet zone), or V4 at 4 px per module (164 px). QR 18-20 mm. Best fit. |
  | 2.13" 250x122 | V3/V4 at 3 px per module. QR about 17-19 mm, with space for text at the side. |
  | 2.9" 296x128 | V3/V4 at 3 px per module. QR about 20-22 mm. |
  | 0.96" OLED 128x64 | V2 or V3 at 2 px per module only, with a reduced quiet zone for V3. QR about 10 mm. |
  | 1.3" OLED 128x64 | Same as the 0.96". QR about 13 mm. |

- Prefer ECC M on e-paper, where space allows V4, for tolerance to glare and scratches on the tag's window. On a 128x64 OLED, ECC L is forced if the URL exceeds 42 bytes.
- The qrcode library picks byte mode automatically for URLs containing `?`/`=`/`&`. An all-uppercase URL would not save space, because these characters fall outside the alphanumeric set regardless of case, and GitHub Pages paths are case-sensitive.

### Gaps
- The quiet-zone tolerance of phone scanners (iOS Camera, Google Lens) at under 4 modules was not measured or sourced.

## 6. Prices and purchase links in Brazil (September 2026)

### Takeaway
The 0.96" OLED costs about R$26-29 at Eletrogate. A 1.54" e-paper module costs R$150-230 at Brazilian retail, but only about €7-9 from the WeAct official store on AliExpress. There, Remessa Conforme orders of US$50 or less paid no federal import tax from 13 May 2026 (MP 1.357/2026), but ICMS of about 20% still applies. Shipping time before 07/12/2026 is the main risk.

### Cited Findings
- Eletrogate (Brazil), OLED 0.96" I2C 128x64 SSD1306:
  - White (H2-009): R$26.90, or R$25.56 by PIX.
  - Blue/Yellow (A11-001): R$28.90, or R$27.46 by PIX.
  - Blue "com os pinos soldados" (G33-001): out of stock at fetch time.
  - [Eletrogate](https://www.eletrogate.com/display-oled-0-96-i2c-azul), [Eletrogate branco](https://www.eletrogate.com/display-oled-128x64-0.96-i2c-branco), [Eletrogate azul/amarelo](https://www.eletrogate.com/display-oled-128x64-096-i2c-azulamarelo)
- Eletrodex, "Display e-Paper 1.54" 200x200": R$226.45 (R$215.13 with discount), 9 units in stock. Brand not stated, and the listing mentions "red and black", so verify the colour version. — [Eletrodex](https://www.eletrodex.net/display-e-paper-1-54-200x200)
- Amazon.com.br, 1.54" 200x200 SPI E-Ink module: R$153.89 — [Amazon.com.br](https://www.amazon.com.br/polegadas-Interface-compat%C3%ADvel-eletr%C3%B4nico-prateleira/dp/B072Q4WTWH) (search snippet; not fetched)
- Other Brazilian listings exist but returned 403, so no price was obtained:
  - Mercado Livre "Módulo E-paper 1.54 Display E-ink ... Mh-et Live" — [Mercado Livre](https://www.mercadolivre.com.br/modulo-epaper-154--display-eink-preto-tela-spi-mhet-live/up/MLBU2023809120)
  - MakerHero "Display e-Paper 1.54 200x200" — [MakerHero](https://www.makerhero.com/produto/display-e-paper-1-54-200x200/)
- WeAct Studio official AliExpress listing for the 1.54" B/W e-paper: about €7 per one search summary, and "US$8.99" per another. Not verified on the live page. — [AliExpress WeAct 1.54](https://www.aliexpress.com/item/1005006291142235.html); 2.13"/2.9" listing: [AliExpress WeAct 2.13/2.9](https://www.aliexpress.com/item/1005004644515880.html)
- LCSC lists the Waveshare 1.54" e-Paper from US$5.55 — [LCSC](https://www.lcsc.com/product-detail/E-ink-Display_Waveshare-1-54inch-e-Paper_C5374685.html) (search snippet)
- Import tax: MP nº 1.357/2026 zeroed the federal import tax on purchases of US$50 or less, effective 13 May 2026. State ICMS of 20% still applies on product plus shipping. For US$50.01-3,000 the rate is 30%, with a US$20 deduction for Remessa Conforme. — [CNN Brasil, 13/05/2026](https://www.cnnbrasil.com.br/economia/macroeconomia/dou-extra-traz-mp-que-isenta-tributacao-para-compras-internacionais-ate-us-50/); Receita Federal program page: [Remessa Conforme](https://www.gov.br/receitafederal/pt-br/assuntos/aduana-e-comercio-exterior/manuais/remessas-postal-e-expressa/programa-remessa-conforme-o-que-e-como-funciona)

### Inferences
- Budget impact (about R$600 total):
  - AliExpress WeAct 1.54" at about US$8-9 plus about 20% ICMS is roughly R$55-65 landed.
  - Buying locally costs R$150-230, i.e. 25-38% of the whole budget for one display.
  - A 0.96" OLED is about R$27. A printed sticker is about R$0-5.
- With the demo on 07/12/2026, an AliExpress order placed in early October is plausible but risky. Order at once, and in parallel either buy one local unit (Amazon.com.br / Eletrodex / Mercado Livre) or rely on the sticker fallback.

### Gaps
- MP 1.357/2026 is a Medida Provisória. MPs lapse unless Congress converts them within 60+60 days, and 13 May + 120 days falls around mid/late September 2026. Whether it was converted into law, and therefore whether the zero rate still applies on 29/09/2026, was NOT verified. Check the tax shown at AliExpress checkout.
- Current AliExpress BRL prices, delivery estimates to São Paulo, and Mercado Livre/MakerHero prices could not be fetched (403).
- No 1.3" SH1106 price from a Brazilian retailer was found.

## 7. Recommendation for a minimal, reliable, battery-powered MVP

### Takeaway
Build the tag with an ESP32 (DevKit or ESP32-C3) and a WeAct 1.54" B/W e-paper (SSD1681, `GxEPD2_154_D67`). Draw a per-session dynamic QR with a nonce, plus a status line. Keep a printed static-URL sticker as the demo fallback. Do not use an OLED as the always-on QR display.

### Cited Findings
- E-paper keeps the image with no power (standby < 0.01 uA) and refreshes in about 2-2.6 s at about 26 mW — [Waveshare wiki](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_Manual), [GxEPD2 GxEPD2_154_D67.h](https://github.com/ZinggJM/GxEPD2)
- A vendor example for ESP32 and ESP32-C3 with exact pins and constructor exists — [WeAct example](https://github.com/WeActStudio/WeActStudio.EpaperModule/blob/master/Example/EpaperModuleTest_Arduino_ESP32/EpaperModuleTest_Arduino_ESP32.ino)
- An OLED draws about 1.4-7 mA whenever lit and can burn in with static content — [hsel.co.uk](https://hsel.co.uk/2018/12/04/ssd1306-power-consumption/), [esphome #624](https://github.com/esphome/feature-requests/issues/624)
- A 128x64 OLED limits the QR to about V3 at 2x; see sections 2 and 5 — [ricmoo/QRCode](https://github.com/ricmoo/QRCode)

### Inferences
- **Ranking for this MVP:**
  1. **E-paper 1.54" (recommended).**
     - It literally satisfies "the QR stays on" at zero power.
     - Its 18-20 mm QR at V3/V4 scans like paper.
     - It supports the dynamic-nonce anti-replay story and shows PAGO/LIBERADO.
     - Wiring is 8 jumpers on 3.3 V SPI.
     - Main risks: price or delivery time, and the fragile ribbon.
  2. **Printed sticker (the fallback, and honestly sufficient for the core flow).**
     - Most reliable scan, no power, no code.
     - Loses the per-session nonce and on-tag status, so status would go to an LED or buzzer.
     - If time or money runs short, the MVP should ship with this plus nonce checking done in the unlock step (e.g. the tag's ID plus a code shown on the payment page).
  3. **OLED 0.96"/1.3" (only if e-paper is unobtainable).**
     - Cheapest screen (about R$27) and 4-wire I2C.
     - But the QR is only about 10-13 mm, it is dark unless powered, and it risks burn-in.
     - Use it only as QR-on-button-press (display off after about 60 s) or as a status display next to a printed QR.
- **Build tips for beginners:**
  - Prototype first in Wokwi (OLED) or with the WeAct example sketch (e-paper).
  - Rename the ricmoo QRCode files on day one to avoid the ESP32-core `qrcode.h` clash.
  - Power the e-paper from 3V3.
  - Use a full refresh for each new QR.
  - Call `display.hibernate()` after every draw.
  - Generate the nonce with Wi-Fi/BLE on (or after `bootloader_random_enable()`) so `esp_random()` is truly random.

### Gaps
- No hands-on measurement or source was found comparing phone-scan reliability between e-paper, OLED and paper under shop lighting. The ranking relies on geometry and the vendor data above.
