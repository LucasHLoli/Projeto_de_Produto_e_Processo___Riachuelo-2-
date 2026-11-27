# Microcontroller board and battery/power setup for the Tag&Go MVP (beginner-safe, no soldering)

Research date: 2026-09-29. Demo date: 07/12/2026 (about 10 weeks away). Prices are in BRL as found on Brazilian retailer pages or search snippets in Sept 2026; anything not backed by a source is labeled as an estimate.

---

## 1. Board choice: which board minimizes wiring and soldering?

### Takeaway
For total beginners who need a reliable live demo, the best choice is a plain **ESP32 DevKit (ESP32-WROOM-32, 30 or 38 pins) sold with the headers already soldered** (about R$55–80 at Eletrogate). It takes 4.5–12 V on VIN through its own regulator, so it can run straight from a 4×AA pack. It needs no soldering, and it has the most tutorials. The Seeed XIAO ESP32-C3 has a much lower sleep current (44 µA) and a built-in LiPo charger, but its battery connects to solder pads on the back and its headers come unsoldered. That makes it the best board for a later, smaller "v2", not for this MVP. The all-in-one boards (M5StickC Plus2, LilyGO T5) avoid display wiring, but each has a blocker for this project: a tiny battery, an unclear 5 V output on battery, a slow e-paper refresh, or unknown price and availability in Brazil.

### Cited Findings
**ESP32 DevKit (WROOM-32)**
- Eletrogate "Módulo WiFi ESP32 38 pinos – USB Tipo C": ESP32-WROOM-32D, CP2102 USB-serial, USB-C, 5 V input / 3.3 V logic (**5 V intolerant GPIOs**), "80 mA typical, 500 mA max", 2.54 mm pitch, **headers soldered**, integrated antenna. It was out of stock when checked; related modules cost R$54,90–79,90. Wi-Fi is 802.11 b/g/n **2.4 GHz only**. — [Eletrogate ESP32 38 pinos USB-C](https://www.eletrogate.com/modulo-wifi-esp32-38-pinos-usb-tipo-c)
- Eletrogate "Módulo WiFi ESP32 DevKitC S1" costs R$59,90 (R$56,90 via Pix), per the search snippet. — [Eletrogate DevKitC S1](https://www.eletrogate.com/modulo-wifi-esp32-devkitc-s1)
- Eletrogate also lists a 30-pin version. — [Eletrogate ESP32 30 pinos](https://www.eletrogate.com/modulo-wifi-esp32-bluetooth-30-pinos)
- Board-level deep-sleep current on DevKit-style boards is about **5–10 mA**, even though the chip alone draws about 15 µA. The AMS1117-3.3 regulator draws about 5 mA quiescent and the CP2102 USB-serial chip 2–5 mA. One measurement on a DevKit V1 found about 9 mA; another found 11.38 mA, falling to 8.15 mA with the regulator removed. — [Hubble: ESP32 deep sleep current, datasheet vs measured](https://hubble.com/community/guides/esp32-deep-sleep-current-what-the-datasheet-says-vs-what-you-ll-actually-measure/); [kohacraft blog, DevKitC deep sleep](https://en.kohacraft.com/archives/esp32-devkitcs-deepsleep-is-consuming-quite-a-bit-of-current-so-i-investigated-the-cause.html); [lucidar.me DevKitC V4](https://lucidar.me/en/esp32/power-consumption-of-esp32-devkitc-v4/)

**Seeed XIAO ESP32-C3**
- Official wiki figures: deep sleep **44 µA**; Wi-Fi active 75 mA; Wi-Fi modem-sleep 25 mA; Wi-Fi light-sleep 4 mA; BLE modem-sleep 27 mA. The LiPo charger is built in (fast charge 380 mA, trickle 40 mA). The battery connects to **BAT+/BAT− pads on the back, which need soldering** ("be careful not to short-circuit… and burn the battery"). The 3V3 pin gives up to 700 mA. **The 5V pin carries USB power only**; it can accept an external 5 V only through a protection diode. **Ships without soldered headers.** — [Seeed wiki XIAO ESP32C3](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)
- A "Pre-Soldered" SKU exists on the Seeed store. — [Seeed XIAO ESP32C3 Pre-Soldered](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Pre-Soldered-p-6331.html)
- RoboCore (Brazil) lists it at R$59,90, out of stock when searched. Its listing states a charging current of 350 mA/100 mA and deep sleep ">44 µA". — [RoboCore XIAO ESP32C3](https://www.robocore.net/seeed-studio/seeed-studio-xiao-esp32c3)
- It is also sold on Mercado Livre and Amazon.com.br; prices could not be retrieved (the page returned 403). — [Mercado Livre listing](https://produto.mercadolivre.com.br/MLB-3331396234-seeed-studio-xiao-esp32c3-risc-v-wifi-ble-mesh-iot-_JM); [Amazon.com.br](https://www.amazon.com.br/Seeed-Studio-XIAO-ESP32C3-Microcontroller/dp/B0B94JZ2YF)
- The XIAO ESP32-C3 battery pad is not wired to any ADC pin, so reading battery voltage needs an external resistor divider (more soldering). — [Seeed forum thread](https://forum.seeedstudio.com/t/xiao-expansion-board-base-for-battery/294978); [Seeed wiki](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)

**Seeed Expansion Base for XIAO (a "no-solder" add-on worth knowing about)**
- Built in:
  - 0.96" SSD1306 OLED (I2C)
  - User button (pin 1, INPUT_PULLUP), reset button, passive buzzer (A3)
  - PCF8563 RTC and microSD slot
  - **"5V servo connector"** (examples use pin 5)
  - **JST 2.0 mm LiPo connector with onboard charging (460 mA max)**
  - Grove ports (I2C, UART, A0/D0)

  Seeed's official compatibility list names XIAO SAMD21, RP2040 and nRF52840; ESP32-C3/S3 appear only in the code examples. The FAQ says "the 5V is directly sourced from the USB", so **it is unclear whether the servo header gets any power when running on battery**. — [Seeed wiki Expansion Base](https://wiki.seeedstudio.com/Seeeduino-XIAO-Expansion-Board/)
- Price: about US$16.40 (DigiKey). No Brazilian price was found. — [search result citing DigiKey / Seeed](https://www.seeedstudio.com/Seeeduino-XIAO-Expansion-board-p-4746.html)

**ESP32-C3 SuperMini**
- About 90% of its roughly 600 µA deep-sleep current comes from the red power LED. The fix is to desolder the LED or its resistor, or cut the trace. — [Random Nerd Tutorials, ESP32-C3 Super Mini](https://randomnerdtutorials.com/getting-started-esp32-c3-super-mini/)
- "SuperMini" is not an official Espressif design, and regulator quality varies between sellers. — [esp32.co.uk SuperMini pinout](https://esp32.co.uk/esp32-c3-supermini-pinout-safe-gpios/); [Mischianti SuperMini](https://mischianti.org/esp32-c3-super-mini-high-resolution-pinout-datasheet-and-specs/)

**LilyGO T5 2.13" e-paper (all-in-one)**
- 2.13" SSD1680 e-paper, 212×104 as listed. **Full refresh takes about 8 s.** The panel is bistable and keeps the image without power. It uses a CP2102 USB-UART and has "ultra-low power deep sleep" (no figure published). The wiki does not document the battery connector, charger or free GPIO. — [LilyGO wiki T5 2.13](https://wiki.lilygo.cc/products/t5-series/t5-epaper-2.13inch/)
- The product page (per search summary) mentions a battery connector, a charge/discharge protection chip and a toggle switch. — [LilyGO T5-2.13 product page](https://lilygo.cc/en-us/products/t5-2-13inch-e-paper)

**M5StickC Plus2 (all-in-one, enclosed)**
- ESP32-PICO-V3-02; 1.14" 135×240 TFT (ST7789v2); three buttons; red LED on G19; **internal 200 mAh battery**. The HOLD pin (GPIO4) must be set high after wake to keep power on. The Grove port provides GND, 5V, G32 and G33. The docs say 5 V is output when USB is connected, but **do not state whether 5 V is output on battery**, and give no standby current. — [M5Stack docs StickC-Plus2](https://docs.m5stack.com/en/core/M5StickC%20PLUS2)
- Brazilian listing for the older M5StickC Plus kit: R$325. Plus2 is sold on Mercado Livre, Space Hack and Electromaster, but no price was captured. — [Germinare listing](https://www.germinaretecnologia.com.br/MLB-2196241627-kit-de-desenvolvimento-m5stack-m5stickc-plus-com-pulseira-_JM); [Space Hack](https://spacehack.lojaintegrada.com.br/stickc-plus-2)
- M5Stack store marks the M5StickC PLUS2 as "[EOL]" (end of life). — [M5Stack store](https://shop.m5stack.com/products/m5stickc-plus2-esp32-mini-iot-development-kit)

**RoboCore "ESP32 com Display OLED e Suporte para Bateria 18650"**
- OLED SSD1306 and 18650 holder with USB charging. **Headers NOT soldered** (two strips are included). There is no battery-voltage feedback, 11 GPIO are available, and no battery is included. — [RoboCore ESP32 OLED 18650](https://www.robocore.net/wifi/esp32-oled-bateria-18650)

### Inferences
- **Ranking for this MVP (fewest failure modes for beginners):**

  | Board | Headers | Battery path | Soldering needed? | Verdict |
  |---|---|---|---|---|
  | **ESP32 DevKit (WROOM-32) 30/38-pin, USB-C** | Soldered | 4.5–12 V into VIN (AMS1117) | **No** | **Recommended** |
  | XIAO ESP32-C3 | Loose (pre-soldered SKU exists) | LiPo on solder pads | Yes (battery pads, and headers unless pre-soldered SKU) | Best "v2 / compact" choice |
  | XIAO ESP32-C3 + Expansion Base | Plug-in | JST LiPo | No | Tempting (OLED, button, servo header built in), but servo power on battery is unverified and Brazilian stock is unknown |
  | ESP32-C3 SuperMini | Usually loose | Needs external circuit | Yes | Avoid |
  | M5StickC Plus2 | N/A (enclosed) | 200 mAh internal | No | Fastest demo, but battery too small for 4 h (see §4), EOL, expensive, servo 5 V on battery unverified |
  | LilyGO T5 2.13 | Unclear | JST + charger | Probably (servo header) | Good e-paper story, but 8 s full refresh and unknown BR price |
  | RoboCore ESP32 + OLED + 18650 | Loose | 18650 | Yes | Avoid |

- The DevKit's weak point is its 5–11 mA deep-sleep draw. That does not matter for a 4-hour demo, and a physical on/off switch handles overnight storage (see §4).
- The DevKit is wide: the 30-pin version leaves almost no free holes on one side of a standard 830-point breadboard. Two practical fixes: two breadboards side by side, or **female-female Dupont jumpers straight from the board's pins to each module**, with no breadboard at all. This is common practice; no source was fetched for it.
- Buy **two identical boards** (one spare, preloaded with the same firmware). At about R$60 each this is cheap insurance for the live demo.

### Gaps
- No live price or stock was confirmed for the Seeed Expansion Base, the LilyGO T5 or the M5StickC Plus2 in Brazil.
- It is unverified whether the Seeed Expansion Base powers its servo header from the LiPo. The FAQ implies USB-only 5 V. If the team goes that route, test it on the bench.
- Some DevKit clones have a Schottky diode between USB 5 V and VIN and others may not; this could not be verified per listing. Hence the safety rule in §8: switch the battery OFF whenever USB is plugged in.

---

## 2. Battery options: AA NiMH vs LiPo+TP4056+MT3608 vs 18650 shield vs power bank

### Takeaway
**4×AA NiMH rechargeable cells in a closed holder with a built-in switch** are the safest and simplest choice. They give 4.8 V nominal and about 5.6 V fresh off the charger, which suits both the DevKit's VIN and the SG90 servo, so no charger or boost module goes inside the device. A single LiPo with a TP4056 charger and an MT3608 boost is smaller, but it adds three failure points: fire risk from a punctured or shorted cell, a boost trimpot that must be set with a multimeter, and solder pads. A USB power bank works only as a **backup**, because many banks shut off at low current.

### Cited Findings
- **AMS1117 (the DevKit regulator)** has about 1.1 V typical dropout (1.3 V max), so VIN must stay above about 4.5 V for a stable 3.3 V. 4×NiMH (4.8 V nominal) works but "close to the minimum threshold". An AP2112-type regulator (250 mV dropout) would allow down to about 3.55 V. — [Arduino forum: ESP32 using 4 AA batteries](https://forum.arduino.cc/t/esp32-using-4-aa-batteries/1219432); [Adafruit forum: powering ESP32 via VIN](https://forums.adafruit.com/viewtopic.php?t=208238)
- 4×AA holders with an on/off switch are widely sold in Brazil:
  - Fermarc: closed case with ON/OFF switch, red/black leads, 65×70×20 mm. — [Fermarc](https://www.fermarc.com/produto/suporte-para-4-pilhas-aa-com-chave-ligadesliga)
  - Armazém da Elétrica: 63.5×68.5×19.6 mm, wire leads. — [Armazém da Elétrica](https://www.armazemdaeletrica.com.br/none-58796943)
  - PowerVolt: holder with switch plus 4 cells for R$30,55 (cell type not stated; probably alkaline). — [PowerVolt](https://www.powervolt.com.br/produtos/suporte-para-4-pilhas-aa-com-chave-liga-desliga-4-pilhas/)
  - Eletrogate: plain 4×AA holder. — [Eletrogate suporte 4 pilhas AA](https://www.eletrogate.com/suporte-para-4-pilhas-aa)
- **TP4056 module with protection, USB-C (Eletrogate): R$4,90 (R$4,66 Pix).** Input 3.35–6 V, charge current up to **1 A** ("ajustável conforme necessário", i.e. by changing a resistor), 4.2 V ±1 % cutoff, red/green LEDs, B+/B− terminals. The page does not say whether these are solder pads or screw terminals. — [Eletrogate TP4056 USB-C com proteção](https://www.eletrogate.com/modulo-carregador-de-baterias-de-litio-tp4056-com-protecao-usb-c)
- **MT3608 step-up (Eletrogate): R$5,90 (R$5,60 Pix).** Input 2–24 V, **output adjustable 2.5–28 V**, 91 % efficiency, 37×17×6 mm. — [Eletrogate MT3608](https://www.eletrogate.com/regulador-de-tensao-ajustavel-mt3608-auto-boost-step-up); [MakerHero MT3608](https://www.makerhero.com/produto/regulador-de-tensao-mt3608-step-up/)
- **LiPo/Li-ion safety (Adafruit):**
  - Use a charger "clearly specified to be compatible… and has appropriate charging protection (voltage, current, temperature)".
  - "Do NOT strike, crush, puncture, disassemble" the battery; do not short-circuit it; do not install it in reverse polarity.
  - "Do NOT directly solder the battery or battery terminals."
  - Stop using a cell that "gives off an odor, generates heat, becomes discolored or deformed".
  - Tape the terminals before disposal.

  — [Adafruit Li-Ion & LiPoly batteries guide](https://learn.adafruit.com/li-ion-and-lipoly-batteries/conclusion)
- The XIAO BAT input is for a 3.7 V lithium cell only, "not intended for 5 V, 9 V or 12 V battery sources". — [esp32.co.uk XIAO ESP32-C3 battery](https://esp32.co.uk/seeed-xiao-esp32-c3-pinout-battery-power-esphome/)
- **Power bank auto-shutoff:** power banks have electronics that cut power when the load is too low. With an MCU, and especially in deep sleep, they "shut off after a few seconds/minutes". Workarounds are periodic dummy-load pulses through an NPN transistor, or buying a "dumb" bank without auto-off. — [aeq-web: Arduino with power bank](https://www.aeq-web.com/arduino-nodemcu-esp-powerbank-dummyload-automatic-shutdown-problem/); [GitHub ESP32_KeepPowerbankAlive](https://github.com/Staubgeborener/ESP32_KeepPowerbankAlive); [Arduino forum: ESP32 sleep with battery bank](https://forum.arduino.cc/t/esp32-sleep-mode-with-battery-bank/673542)

### Inferences
- **Option (a) 4×AA NiMH (recommended).**
  - Voltage: freshly charged NiMH sits around 1.4 V per cell (about 5.6 V per pack), holds about 1.2 V for most of the discharge, and ends around 1.0–1.1 V (4.0–4.4 V per pack). This is common NiMH behavior; no source was fetched. The pack fits VIN for most of its capacity, and the SG90 works best in its 4.8–6 V range.
  - End of discharge: the 3.3 V rail starts to sag and the ESP32 may become unstable. Rule for the demo: **start with freshly charged cells and carry a second charged set of 4.** Swapping takes 30 seconds, needs no tools, and carries no risk.
  - Charging: a commercial NiMH charger, outside the device. No charging electronics sit inside the 3D-printed box, so there is nothing to catch fire.
  - Do **not** use 3×AA:
    - 3×NiMH gives 3.6 V nominal, too low for VIN through the AMS1117.
    - Fresh 3×NiMH gives about 4.2 V, above the ESP32's 3.6 V maximum if wired to 3V3.
    - 3×alkaline gives 4.5 V, also far too high for 3V3.
  - 4×alkaline gives about 6.0–6.4 V fresh. VIN tolerates it, but the SG90 sits at or just above its 6 V nominal. Acceptable as an emergency fallback, but NiMH is preferred.
  - Size: the pack is about 65×70×20 mm. It is bulky for a "tag", but acceptable for an MVP. The team can print a separate battery "pod" or make the tag body thicker.
- **Option (b) 1S LiPo + TP4056 (protected) + MT3608 → 5 V.** Smallest and rechargeable over USB-C, but:
  1. **Set the MT3608 to 5.0 V with a multimeter *before* connecting the ESP32/servo.** It can output up to 28 V, and a mis-set trimpot destroys the board instantly.
  2. The TP4056's default 1 A charge current is too high for cells under about 1000 mAh (keep charging at 1C or less). Choose a cell of **1000 mAh or more with a built-in protection PCB and JST plug**, or change the programming resistor, which means soldering.
  3. The modules have solder pads, so soldering is needed.
  4. LiPo puncture risk inside a 3D-printed case (screws, snap-fits).
  5. Servo current peaks through the boost can still brown out the board.

  Choose this only for a later, smaller prototype, and only with a teammate who can solder.
- **Option (c) 18650 holder with charger/"battery shield".**
  - The cells can deliver very high short-circuit current.
  - Counterfeit or unbranded 18650s are common on marketplaces.
  - The RoboCore all-in-one board ships with unsoldered headers.

  No safety or simplicity advantage over (a). Not recommended. The "battery shield" claims are general knowledge, not sourced here.
- **Option (d) USB power bank.**
  - Good as a **demo-day backup**: plug it into the DevKit's USB-C with the AA pack switched OFF.
  - With Wi-Fi always on (about 100 mA or more), most banks probably stay on. In deep sleep (5–11 mA on a DevKit) many will shut off.
  - If used, pick a bank marketed with a "low-current / always-on / wearable mode", or test it for 30 minutes on the bench.

### Gaps
- No Brazilian price was retrieved for 4×AA NiMH cells or a NiMH charger. Estimate (unsourced): about R$80–150 for 4 low-self-discharge cells of 1900–2000 mAh plus a basic charger. The team may already own some.
- No source was found giving the exact minimum load current at which typical power banks shut off; it varies by model.
- No verified internal resistance was found for NiMH AA cells or holder springs, so the voltage sag under servo peaks was not quantified; measure it on the bench.

---

## 3. Servo power: SG90 peaks, brownout, capacitor, separate rail, common ground

### Takeaway
Design for **up to about 1 A servo peaks** (sources disagree: 250 mA to 1.3 A at stall). Never power the servo from the ESP32's 3V3 pin. Take servo power **straight from the battery or 5 V rail, in parallel with the board's VIN**, put a **470–1000 µF electrolytic capacitor across the servo supply**, and tie all grounds together. Do not disable the ESP32 brownout detector.

### Cited Findings
- **SG90 current, conflicting figures:**
  - About 250 mA stall. — [Industrial Monitor Direct SG90 power guide](https://industrialmonitordirect.com/blogs/knowledgebase/powering-sg90-servo-from-arduino-direct-5v-rail-design-guide)
  - "can reach 650–750 mA under mechanical stall" (search summary across SG90 guides). — [ESPBoards SG90](https://www.espboards.dev/sensors/sg90/); [ComponentIndex SG90](https://componentindex.net/components/sg90/)
  - A Miuzei SG90 spec sheet was cited in search results as "stall current 1300 ± 40 mA at 4.8 V" with stall torque 2.0 kg·cm. **I could not open the PDF to verify.** — [Miuzei SG90 spec PDF](https://images-na.ssl-images-amazon.com/images/I/61jUf7Q-0uL.pdf); [Kpower SG90 guide](https://www.kpower.com/insight_driver/7294.html)
- Servo start-up spikes pull the rail below the ESP32 minimum and trigger a **brownout reset**. The fix is 470–1000 µF across the servo 5 V rail plus a dedicated 5 V supply with GND tied to ESP32 GND. Even one SG90 "will exceed the ESP32 devboard's onboard regulator limit". — [Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/powering-sg90-servo-from-arduino-direct-5v-rail-design-guide); [Circuit Digest SG90 + ESP32](https://circuitdigest.com/microcontroller-projects/interfacing-sg90-servo-motor-with-esp32)
- ESP32 brownout (ESPBoards):
  - Causes: Wi-Fi start-up draws "up to 300–500 mA"; weak USB ports (100–300 mA); thin or long cables; loose connections.
  - Fix: "470 µF–1000 µF low-ESR electrolytic capacitor between VCC and GND (as close to the ESP32 as possible)" plus 0.1 µF ceramic; give motors their own supply with a common GND; use short, thick cables.
  - Disabling the brownout detector is a safety feature to keep, not a fix.

  — [ESPBoards: ESP32 brownout reset](https://www.espboards.dev/troubleshooting/issues/power/esp32-brownout-reset/)
- The Eletrogate blog notes that SG90-class servos "não possuem proteção contra sobrecorrente". — [Eletrogate blog: controle de corrente em servomotores](https://blog.eletrogate.com/controle-de-corrente-em-servomotores/)

### Inferences
- With the 4×AA architecture, the battery **is** the separate servo rail. The servo red wire goes to battery + (after the switch), not to any regulator output. The DevKit's AMS1117 feeds only the ESP32 and the 3.3 V modules, and the servo peak never passes through it.
- Place the **1000 µF / 16 V** electrolytic right at the servo power junction. **Observe polarity**: the stripe marks the negative leg and goes to GND; reversed electrolytics can burst. Optionally add a second 470 µF near VIN/GND of the board.
- Firmware mitigations (they cost nothing):
  - `attach()` the servo, move it, wait about 500 ms, then `detach()`. This stops holding current and jitter.
  - Do not start a servo move at the same moment as a Wi-Fi connection or HTTP request; sequence them.
  - Mechanically, keep the latch light so the servo never stalls against its end stop. Stall is the worst-case current and heats the servo.
- An alternative actuator (a small solenoid) typically draws more current than an SG90 and needs a MOSFET or driver plus a flyback diode. That adds parts and risk, so the SG90 is the simpler choice for beginners. This is general knowledge, not sourced here.

### Gaps
- No verified, primary SG90 datasheet figure for stall current was retrieved (the PDF was unreadable). Measure it with a multimeter in series (current range) on the bench using the Arduino Uno setup in §6.
- No measured data was found on how far a 4×AA NiMH holder sags under a 0.5–1 A pulse.

---

## 4. Power budget and autonomy estimates

### Takeaway
With the recommended DevKit + 4×AA NiMH of about 2000 mAh (assume about 1600 mAh usable), a **4-hour demo with ~50 unlock cycles uses about 360–600 mAh, roughly a quarter to a third of the pack**. The servo's share is negligible (under 10 mAh). **Standby in deep sleep on a DevKit lasts only about 6–7 days**, because the board's regulator and USB chip draw 5–11 mA. On a XIAO ESP32-C3 (44 µA) the same standby would last months. For the demo, use the holder's physical switch overnight and keep Wi-Fi connected during the demo, which is the most reliable firmware.

### Cited Findings
- **Classic ESP32 (WROOM-32) current per mode:**
  - Wi-Fi TX 180–240 mA; RX 95–100 mA
  - Modem sleep: 30–68 mA at 240 MHz, 27–44 mA at 160 MHz, 20–31 mA at 80 MHz
  - Light sleep: about 0.8 mA
  - Deep sleep: 6–10 µA (timer), 50–100 µA (ext0 wake), 10 µA (ext1); hibernation about 5 µA

  — [Last Minute Engineers: ESP32 sleep modes](https://lastminuteengineers.com/esp32-sleep-modes-power-consumption/)
- **ESP32-C3 (Espressif, 3.3 V, 25 °C):**
  - TX peak 335 mA (802.11b 1 Mbit/s @ 21 dBm) and 276–285 mA (g/n)
  - RX 84–87 mA
  - Modem sleep 15–20 mA
  - Light sleep 130 µA; deep sleep 5 µA; power-off 1 µA

  — [Espressif ESP32-C3 book, ch. 12.2.4](https://espressif.github.io/esp32-c3-book-en/chapter_12/12.2/12.2.4.html); [ESP32-C3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- XIAO ESP32-C3 at board level: deep sleep 44 µA, Wi-Fi active 75 mA, modem sleep 25 mA, light sleep 4 mA. — [Seeed wiki](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/); [Seeed power-consumption test PDF](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/Seeed_Studio_XIAO_ESP32C3_Power_Consumption_Tests.pdf)
- DevKit at board level in deep sleep: about 5–11 mA (AMS1117 plus CP2102). — [Hubble](https://hubble.com/community/guides/esp32-deep-sleep-current-what-the-datasheet-says-vs-what-you-ll-actually-measure/); [kohacraft](https://en.kohacraft.com/archives/esp32-devkitcs-deepsleep-is-consuming-quite-a-bit-of-current-so-i-investigated-the-cause.html)
- ESP32-C3 SuperMini deep sleep: about 600 µA, 90 % of it from the power LED. — [Random Nerd Tutorials](https://randomnerdtutorials.com/getting-started-esp32-c3-super-mini/)
- Wi-Fi start-up bursts: "up to 300–500 mA". — [ESPBoards brownout](https://www.espboards.dev/troubleshooting/issues/power/esp32-brownout-reset/)
- E-paper is bistable, so it draws no power to hold an image (a QR code stays visible with the board off or asleep). Full refresh takes about 8 s on the LilyGO 2.13". — [LilyGO wiki T5 2.13](https://wiki.lilygo.cc/products/t5-series/t5-epaper-2.13inch/)
- The 1.54" 200×200 SPI e-paper supports partial refresh and has "consumo ultra-baixo". — [Saravati MH-ET LIVE 1.54](https://www.saravati.com.br/modulo-e-paper-1-54-display-e-ink-preto-tela-spi-mh-et-live.html); [Waveshare 1.54" module](https://www.waveshare.com/1.54inch-e-paper-module.htm)
- M5StickC Plus2 battery: 200 mAh. — [M5Stack docs](https://docs.m5stack.com/en/core/M5StickC%20PLUS2)

### Inferences
These are calculations; the component currents come from the findings above, and **OLED and servo idle currents are estimates**.

**Scenario 1: demo day, 4 h, about 50 unlock cycles, DevKit + 4×AA NiMH (about 1600 mAh usable)**

| Load | Assumption | Average current |
|---|---|---|
| ESP32 connected to Wi-Fi, default modem sleep, occasional HTTP/MQTT | 30–68 mA modem sleep plus RX/TX bursts | 60–100 mA |
| DevKit overhead (AMS1117, CP2102, power LED) | from the deep-sleep measurements | about 10 mA |
| Display: OLED 0.96" on continuously (estimate) / e-paper between refreshes | OLED about 10–20 mA (unsourced estimate); e-paper about 0 | 0–20 mA |
| Servo idle, detached (estimate) | a few mA (unsourced) | ≤10 mA |
| LED on (with resistor) | typical indicator LED | 5–10 mA |
| **Total** | | **about 90–150 mA** |

- Energy for 4 h: 90–150 mA × 4 h = **360–600 mAh**, about 23–38 % of the pack.
- Continuous runtime to empty is roughly 1600 / 150 ≈ **11 h** (worst case) to 1600 / 90 ≈ **18 h**.
- Servo: 50 cycles × 2 moves (open and relock) × about 0.5 s × about 0.5 A (a generous average) ≈ 25 A·s ≈ **7 mAh**, under 1 % of the pack.
- Conclusion: **one charged 4×AA set easily covers the demo; a spare set covers any mistake.**
- The same scenario on a XIAO ESP32-C3 with a 1000 mAh LiPo: about 75 mA active plus display and LED ≈ 90–110 mA → 360–440 mAh in 4 h. That fits, with less margin.
- M5StickC Plus2: 200 mAh at about 100 mA ≈ **2 h**, so it **cannot** run a 4 h demo on its internal battery. It would have to run from a USB power bank.

**Scenario 2: standby for days (deep sleep, button wake, QR kept on e-paper)**
- DevKit: about 5–11 mA → 1600 mAh / 10 mA ≈ 160 h ≈ **6–7 days**. The servo's idle draw (if it stays on the battery rail), and the ext0-wake RTC peripherals, shorten this further.
- Practical choice for the MVP: **flip the holder's switch OFF** between sessions. The e-paper keeps showing the QR even with power off, which is a nice "product" talking point.
- XIAO ESP32-C3: 44 µA → 1000 mAh / 0.044 mA ≈ 22,700 h theoretical. In practice LiPo self-discharge and the external modules' sleep current dominate, so expect **months**. This is the number to quote for the *product* concept, flagged as a v2 board choice.
- Cost of one button wake (Wi-Fi connect about 1–3 s at about 150 mA average, plus e-paper refresh): about 0.1–0.2 mAh. Even hundreds of wakes are negligible. The 1–3 s connect time is typical, not sourced.

**Strategy recommendation**
- For the **demo**: keep Wi-Fi connected (no deep sleep) so that unlocks feel instant, and check battery voltage the morning before.
- For the **product narrative**: demonstrate the deep-sleep plus button-wake flow once. Pressing the button wakes the device, connects Wi-Fi, fetches or refreshes the QR, then sleeps again; the e-paper keeps the image. Show it as a separate firmware mode.

### Gaps
- No sourced figure for SSD1306 0.96" OLED current (it depends on how many pixels are lit) or for e-paper refresh current; both are estimated above.
- No sourced figure for SG90 idle current with and without the PWM signal.
- Real DevKit clone deep-sleep draw varies by regulator, USB chip and LED; measure the team's own board with a multimeter.

---

## 5. Wiring without soldering; minimal tools

### Takeaway
A **soldering iron is not needed** if the team buys: a DevKit with soldered headers; display, LED and button modules listed "com pinos soldados"; a 4×AA holder with wire leads; a breadboard (830 points) or a mini breadboard used as the power "hub"; and an assortment of male-male, male-female and female-female Dupont jumpers. Tools: a small screwdriver and, strongly recommended, a cheap multimeter.

### Cited Findings
- The Eletrogate ESP32 38-pin USB-C module ships with **soldered headers** at 2.54 mm pitch. — [Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-38-pinos-usb-tipo-c)
- Boards that ship **without** soldered headers: XIAO ESP32-C3 (wiki); RoboCore ESP32 + OLED + 18650 ("2 barras de pinos não soldadas"). — [Seeed wiki](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/); [RoboCore](https://www.robocore.net/wifi/esp32-oled-bateria-18650)
- XIAO battery connection requires soldering to the BAT pads. — [Seeed wiki](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)
- The Seeed Expansion Base is marketed as "No Soldering Needed", with a JST battery plug and a servo header. — [Amazon listing title](https://www.amazon.com/Seeeduino-Expansion-Prototyping-peripherals-Soldering/dp/B08P4GPR6M); [Seeed wiki](https://wiki.seeedstudio.com/Seeeduino-XIAO-Expansion-Board/)
- Eletrogate prices: protoboard 830 points R$11,90; jumpers sold in male-male 10/20 cm and other variants. — [search summary of Eletrogate catalog](https://www.eletrogate.com/categorias)
- Loose connections are a listed brownout cause. — [ESPBoards brownout](https://www.espboards.dev/troubleshooting/issues/power/esp32-brownout-reset/)

### Inferences
- **Suggested physical layout (no solder):**
  1. Plug the DevKit into one breadboard, or into two breadboards side by side because it is wide, or leave it free and use female-female jumpers.
  2. Use the **breadboard power rails** (or a separate 170-point mini breadboard) as the **"battery bus"**: battery red to the + rail, battery black to the − rail. Then plug in the servo's red and brown wires (via male-male jumpers), the capacitor legs, and jumpers to the board's VIN and GND.
  3. Connect the display, LED and button with female-female or male-female jumpers.
  4. For the final 3D-printed tag, replace the breadboard with the same jumpers plus a small piece of breadboard glued inside, or with **Wago 221 lever connectors** for the battery + and GND junctions. Wago accepts the stranded holder leads directly; stripping wire is the only "tool" step.
- **Holder leads:** thin stranded wire does not hold well in breadboards. Buy a holder with tinned ends or a JST/"P4" plug. Or twist each lead onto a male jumper and cover the joint with heat-shrink or electrical tape. A Wago connector is cleaner.
- **Minimal tools list:**
  - small Phillips screwdriver (holder cover, servo horn)
  - multimeter, about R$40–70 (estimate): checks battery voltage, confirms polarity, and measures servo current
  - flush cutter / wire stripper (optional)
  - electrical tape or heat-shrink
  - a USB-C data cable (**not** a charge-only cable; this is a common beginner trap)
  - hot glue or double-sided foam tape to fix parts inside the 3D-printed case
- **Is a soldering iron truly needed?** No, for the recommended setup. It becomes necessary only for: the XIAO battery pads; boards or modules with loose headers (SuperMini, RoboCore 18650 board, some OLED/e-paper listings); TP4056 or MT3608 pads; or permanent wiring. If any listing says "pinos não soldados" / "barra de pinos avulsa", pick a different listing or ask a lab (the Poli labs or the course's makerspace, if available) to solder it.
- Glue or tape every connector inside the tag. Dupont jumpers fall out when the tag is handled on stage, and this is the #1 live-demo failure.

### Gaps
- Whether particular OLED and e-paper listings in Brazil ship with soldered pins must be checked per listing. The display is covered by the separate display research note (`display_qr.md`).
- No sourced Brazilian prices were found for Wago 221 connectors, jumper kits or multimeters.

---

## 6. Role of the team's Arduino Uno

### Takeaway
Use the Uno as a **bench tester**: sweep the SG90 with the built-in `Servo` library to validate the 3D-printed latch mechanics and measure servo current before the ESP32 is involved. Do **not** try Uno + ESP-01 or Uno + HC-05 as the product brain. It adds a second MCU, voltage-level and AT-command problems, and (for HC-05) no iPhone support, all to solve problems the ESP32 already solves on one chip.

### Cited Findings
- Servo peaks can crash or reset a board powered through its onboard regulator; power the servo from a dedicated supply with a common GND. — [Industrial Monitor Direct SG90 guide](https://industrialmonitordirect.com/blogs/knowledgebase/powering-sg90-servo-from-arduino-direct-5v-rail-design-guide)
- The ESP32 already integrates Wi-Fi (2.4 GHz) and Bluetooth, at about R$55–80. — [Eletrogate ESP32 38 pinos](https://www.eletrogate.com/modulo-wifi-esp32-38-pinos-usb-tipo-c)

### Inferences
- **Bench test recipe:**
  1. Servo signal to Uno D9.
  2. Servo power from the 4×AA pack (red to +, brown to −).
  3. **Uno GND tied to pack −.**
  4. 1000 µF across the pack.
  5. Run the "Sweep" example.

  Put a multimeter in series with the servo red wire (10 A or mA range) to read the real current while the latch opens and closes. This settles the 250 mA vs 1.3 A question for the team's actual mechanism.
- **Uno + ESP-01:** the ESP-01 needs 3.3 V with Wi-Fi peaks of several hundred mA and 3.3 V logic. That means an extra regulator, a level shifter on RX, and AT firmware or a second program. **Uno + HC-05:** Bluetooth Classic SPP, which iPhones do not support for generic serial apps (known platform limitation, not sourced here). Both double the wiring and the debugging surface. Brief verdict: no.

### Gaps
- No source was fetched on Uno 3.3 V pin current limits or on HC-05/iOS compatibility; these are stated from general knowledge, and the report writer should keep them brief or soften them.

---

## 7. Brazil purchase links and prices (Sept 2026) and import taxes

### Takeaway
Everything needed for the recommended build is sold by Brazilian retailers (Eletrogate, RoboCore, Fermarc, MakerHero and others) for well under R$600. **Buy critical parts in Brazil now.** AliExpress is cheaper, but shipping is too slow for a demo about 10 weeks away. Import tax on purchases under US$50 was zeroed by MP 1.357/2026 in May 2026, but ICMS of 17–20 % still applies, and the MP's permanent status must be re-checked.

### Cited Findings
| Item | Where | Price found | Source |
|---|---|---|---|
| ESP32 DevKitC S1 (WROOM, soldered) | Eletrogate | R$59,90 (R$56,90 Pix) | [Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-devkitc-s1) |
| ESP32 38-pin USB-C (WROOM-32D, soldered) | Eletrogate | out of stock; related R$54,90–79,90 | [Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-38-pinos-usb-tipo-c) |
| ESP32 30-pin | Eletrogate | price not captured | [Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-bluetooth-30-pinos) |
| Seeed XIAO ESP32-C3 | RoboCore | R$59,90 (out of stock when searched) | [RoboCore](https://www.robocore.net/seeed-studio/seeed-studio-xiao-esp32c3) |
| Micro servo SG90 9g | Eletrogate | R$14,90 | [Eletrogate](https://www.eletrogate.com/micro-servo-9g-sg90-towerpro) |
| Micro servo SG90 | RoboCore / Curto Circuito | not captured | [RoboCore](https://www.robocore.net/servo-motor/micro-servo-9g-sg90-towerpro); [Curto Circuito](https://curtocircuito.com.br/servo-motor-9g-sg90.html) |
| Protoboard 830 points | Eletrogate | R$11,90 | [Eletrogate categories (search summary)](https://www.eletrogate.com/categorias) |
| 4×AA holder with switch + 4 cells | PowerVolt | R$30,55 | [PowerVolt](https://www.powervolt.com.br/produtos/suporte-para-4-pilhas-aa-com-chave-liga-desliga-4-pilhas/) |
| 4×AA holder with switch | Fermarc / Armazém da Elétrica | not captured | [Fermarc](https://www.fermarc.com/produto/suporte-para-4-pilhas-aa-com-chave-ligadesliga); [Armazém da Elétrica](https://www.armazemdaeletrica.com.br/none-58796943) |
| TP4056 USB-C with protection (only if LiPo route) | Eletrogate | R$4,90 (R$4,66 Pix) | [Eletrogate](https://www.eletrogate.com/modulo-carregador-de-baterias-de-litio-tp4056-com-protecao-usb-c) |
| MT3608 step-up (only if LiPo route) | Eletrogate | R$5,90 (R$5,60 Pix) | [Eletrogate](https://www.eletrogate.com/regulador-de-tensao-ajustavel-mt3608-auto-boost-step-up) |
| M5StickC Plus (older kit) | Mercado Livre / Germinare | R$325 | [Germinare](https://www.germinaretecnologia.com.br/MLB-2196241627-kit-de-desenvolvimento-m5stack-m5stickc-plus-com-pulseira-_JM) |
| Seeed Expansion Base for XIAO | DigiKey (USD) | about US$16.40; no BR price | [Seeed store](https://www.seeedstudio.com/Seeeduino-XIAO-Expansion-board-p-4746.html) |
| e-paper 1.54" SPI (MH-ET LIVE) | Saravati / Mercado Livre / Eletrodex | not captured | [Saravati](https://www.saravati.com.br/modulo-e-paper-1-54-display-e-ink-preto-tela-spi-mh-et-live.html); [Eletrodex](https://www.eletrodex.net/display-e-paper-1-54-200x200) |

- **Import tax (AliExpress etc.):** MP 1.357/2026, published 12 May 2026, **zeroed the federal import tax for purchases up to US$50 under Remessa Conforme**. It "already is in force, but needs to be analyzed by the National Congress within 120 days". Purchases from US$50 to US$3,000 stay at 60 % with a US$30 deduction. — [Agência Senado](https://www12.senado.leg.br/noticias/materias/2026/05/13/medida-provisoria-zera-taxa-das-blusinhas-para-importacoes-de-ate-us-50)
- ICMS still applies to these imports at 17 % to 20 % depending on the state, collected at checkout on Remessa Conforme platforms. — [Contmatic blog: Imposto de Importação 2026](https://simplifique.contmatic.com.br/blogs/imposto-de-importacao-2026-aliquotas-como-calcular); [Santander blog](https://www.santander.com.br/blog/taxacao-produtos-importados)

### Inferences
- **Estimated bill for the recommended build.** Items marked * are unsourced estimates.

  | Item | Estimate |
  |---|---|
  | 2× ESP32 DevKit (one spare) | about R$120–160 |
  | 2× SG90 | about R$30 |
  | 4×AA holder with switch | about R$15–30 |
  | 8× NiMH AA plus charger* | about R$120–200 |
  | 1000 µF/16 V capacitors (×3)* | about R$5 |
  | Protoboard 830 plus mini 170* | about R$20 |
  | Jumper kit (M-M/M-F/F-F)* | about R$20–30 |
  | RGB LED module + push-button module* | about R$10 |
  | Multimeter* | about R$50 |
  | **Total** | **about R$390–535**, before the display |

  The display is costed in the separate display note. Choosing the OLED instead of the e-paper keeps the total under R$600. If the team already owns NiMH cells or a multimeter, there is ample margin.
- **AliExpress:** buy only non-critical spares there. Delivery is typically several weeks and often uncertain; this is general knowledge, not measured for 2026. MP 1.357/2026's 120-day window from 12 May ended around September 2026, so **check whether Congress converted it into law or let it lapse** before counting on 0 % import tax.

### Gaps
- Live prices were not captured for: the NiMH cells and charger, the 1000 µF capacitor, jumper kits, the RGB LED module, the push-button module, the multimeter, the M5StickC Plus2, the LilyGO T5, Usinainfo, FilipeFlop/MakerHero, Baú da Eletrônica, or Mercado Livre (the Mercado Livre pages returned 403).
- The status of MP 1.357/2026 after its 120-day deadline (September 2026) was not verified.
- Current AliExpress delivery times to São Paulo were not verified.

---

## 8. Recommendation: one board + power setup, with pin-to-pin wiring

### Takeaway
**Recommended MVP stack:** an ESP32 DevKit (WROOM-32, USB-C, headers soldered), powered by **4×AA NiMH in a closed holder with an ON/OFF switch**. The battery feeds the board's **VIN (or "5V") pin** and the **SG90 red wire in parallel**, with a **1000 µF capacitor** across the servo supply. All grounds are common. Display, LED and button run on 3.3 V logic. There is **no LiPo, no charger module, no boost converter and no soldering.** A USB power bank into the DevKit's USB-C is the demo backup, used with the AA pack switched OFF.

### Cited Findings
- DevKit: 5 V input to the onboard regulator, 3.3 V logic, GPIOs not 5 V tolerant, headers soldered. — [Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-38-pinos-usb-tipo-c)
- VIN must stay above about 4.5 V because of AMS1117 dropout. — [Arduino forum](https://forum.arduino.cc/t/esp32-using-4-aa-batteries/1219432)
- Servo: separate supply plus 470–1000 µF plus common GND. — [Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/powering-sg90-servo-from-arduino-direct-5v-rail-design-guide); [ESPBoards](https://www.espboards.dev/troubleshooting/issues/power/esp32-brownout-reset/)
- Deep-sleep options on ESP32: ext0 wake 50–100 µA (chip level). — [Last Minute Engineers](https://lastminuteengineers.com/esp32-sleep-modes-power-consumption/)
- Wi-Fi is 2.4 GHz only. — [Eletrogate](https://www.eletrogate.com/modulo-wifi-esp32-38-pinos-usb-tipo-c)

### Inferences
**Wiring table:** ESP32 DevKit V1 / DevKitC with WROOM-32. GPIO numbers are the same on the 30- and 38-pin versions.

| Component / wire | Goes to | Notes |
|---|---|---|
| Battery holder **red (+)** (switch built into holder) | **+ rail** of breadboard ("battery bus") | 4×AA **NiMH** only (4.8 V nominal, about 5.6 V fresh) |
| Battery holder **black (−)** | **− rail** (GND bus) | |
| + rail | DevKit **VIN** (DOIT 30-pin label) / **5V** (DevKitC label) | **Never** to 3V3 |
| − rail | DevKit **GND** | Common ground for everything |
| Capacitor **1000 µF / 16 V**, + leg | + rail, next to the servo red wire | **Stripe = negative**; wrong polarity can burst it |
| Capacitor − leg (stripe) | − rail | |
| Servo **red** (+) | + rail | Straight from the battery, not from the board |
| Servo **brown/black** (GND) | − rail | |
| Servo **orange/yellow** (signal) | **GPIO 13** | ESP32Servo library; attach → move → detach |
| **OLED 0.96" I2C** VCC / GND / SDA / SCL | **3V3** / GND / **GPIO 21** / **GPIO 22** | Default ESP32 I2C pins |
| *or* **e-paper 1.54" SPI** VCC / GND / DIN / CLK / CS / DC / RST / BUSY | **3V3** / GND / **GPIO 23** / **GPIO 18** / **GPIO 5** / **GPIO 17** / **GPIO 16** / **GPIO 4** | Common GxEPD2 ESP32 mapping (VSPI); verify against the chosen library example |
| **RGB LED** (common-cathode) R / G / B / − | **GPIO 25** / **GPIO 26** / **GPIO 27** (optional) / GND | 220–330 Ω in series with each color, or buy a module with built-in resistors; a bicolor LED uses R and G only |
| **Push button** leg 1 / leg 2 | **GPIO 33** / GND | `INPUT_PULLUP`. GPIO 33 is an RTC pin, so it can wake from deep sleep (ext0, level LOW); enable the RTC pull-up in sleep |
| USB-C of DevKit | laptop (programming) or power bank (backup) | **Switch the AA pack OFF when USB is connected** |

**Pins to avoid on the classic ESP32** (standard Espressif guidance, not re-fetched here):
- GPIO 6–11: SPI flash.
- GPIO 34–39: input-only, with no internal pull-ups, so no good for the button.
- Strapping pins GPIO 0, 2 and 12: GPIO 12 held high at boot can break boot.
- GPIO 5 as e-paper CS is standard and idles high, so it is fine.

**Safety and reliability rules for the team (one page for the bench):**
1. Only NiMH rechargeable AAs; charge them in a commercial charger outside the device. Never mix old and new cells.
2. Nothing above 3.3 V goes to any GPIO or to the 3V3 pin. The battery goes only to VIN/5V and the servo.
3. Wire with the power switch **OFF**, and check polarity with the multimeter before switching ON.
4. Capacitor stripe to GND.
5. The servo must never stall against the latch end-stop. Tune the angles on the bench with the Uno first.
6. Glue or tape every jumper inside the 3D-printed tag.
7. Demo kit: spare charged 4×AA set, spare flashed ESP32, spare SG90, power bank + USB-C cable, and a phone hotspot configured for **2.4 GHz**. The ESP32 cannot join 5 GHz-only networks.

**Plan B / v2 (smaller tag, after the MVP):** XIAO ESP32-C3 Pre-Soldered with a 1000 mAh protected LiPo. This needs one soldering job on the BAT pads, done by someone experienced. It gives 44 µA deep sleep, so standby lasts months. The servo is fed from a 5 V boost set with a multimeter, or directly from the LiPo at reduced torque; the latter was not verified. Alternatively, use the Seeed Expansion Base (no solder: OLED, button and servo header are built in) once the team has bench-tested that its servo header is powered on battery.

### Gaps
- The GxEPD2 pin mapping and the "avoid these pins" list are from general ESP32 and GxEPD2 conventions; no source was fetched for them in this session. Cross-check against the display research note and the library's README.
- Deep-sleep wake with the RTC pull-up on GPIO 33 (ext0) was not tested here; there is example code in the ESP32 Arduino core (`DeepSleep/ExternalWakeUp`).
- It is unverified whether the specific DevKit clone bought has a diode between USB 5 V and VIN, so the rule "switch the battery OFF when USB is connected" stays as a precaution.
