# Simplest 3D-printable electronic pin lock for the Tag&Go MVP (battery, ESP32, beginner team)

Research date: 2026-09-29. Demo date: 07/12/2026. Scope: the mechanism that holds a pin through the garment and releases it when the ESP32 commands it. It covers the actuator, the pin, the latch geometry, forces and printing, lock-state sensing, and fitting the mechanism in the box. Phone communication, the display and battery sizing are covered in the sibling notes.

Access notes:
- Several pages returned HTTP 403 to the fetch tool: Printables, MakerHero, i9 Automação and the handsontec SG90 PDF. Facts from those pages come from search-engine snippets and are labeled "(search snippet)".
- Every engineering calculation (forces, stresses, travel) is my own arithmetic from the cited specs. These are listed under Inferences.

---

## 1. Servo latch (SG90 / MG90S): torque, force at the arm, current, jitter, detaching, holding without power, existing designs

### Takeaway
A micro servo has more than enough force to open a small spring latch: roughly 12–18 N at a 10 mm arm for the SG90 and about 18–22 N for the MG90S. It draws a lot of current only for the second or so while it moves. Once the PWM signal stops, a hobby servo keeps its position through gearbox friction. The main rule is to keep the servo out of the load path. The pull on the pin should go into printed walls, not into the servo gears or horn. Then the latch holds with no power, and the servo only has to move to open.

### Cited Findings
**SG90 specs**
- TowerPro SG90 stall torque: 1.8 kgf·cm (about 11 N·cm) at 4.8 V and 2.4 kgf·cm (about 15 N·cm) at 6 V. Operating voltage 4.8–6 V. — [Components101 SG90](https://components101.com/motors/servo-motor-basics-pinout-datasheet) (search snippet); also [Zbotic SG90 guide](https://zbotic.in/sg90-servo-motor-pinout-torque-specs-arduino-projects/) (search snippet)
- Stall current varies by source: "less than 600 mA", "500–700 mA", and "up to 360 mA". Generic SG90 clones are often weaker than the original TowerPro. — search snippets from [ProtoSupplies SG90](https://protosupplies.com/product/servo-motor-micro-sg90/) and [Components101](https://components101.com/motors/servo-motor-basics-pinout-datasheet). The sources conflict, so assume up to about 0.7 A peak.
- A generic SG90 sold in Brazil (Usinainfo) is listed with lower torque: 1.2 kgf·cm at 4.8 V and 1.6 kgf·cm at 6 V. Other listed specs:
  - voltage range 3.0–6.0 V
  - current 100 mA with no load, 750 mA loaded
  - size 32 × 12.6 × 30 mm, weight 10 g
  - price R$ 14.16 (Pix) or R$ 14.90 (card), sold with 3 horns and screws

  — [Usinainfo SG90](https://usinainfo.com.br/servo-motores/micro-servo-motor-9g-sg90-180-2299.html)
- Idle current: search summaries of SG90 guides give about 10–20 mA at idle and 100–250 mA while moving. This was not verified on the pages themselves. — search results incl. [ProtoSupplies](https://protosupplies.com/product/servo-motor-micro-sg90/), [Zaitronics SG90 guide](https://zaitronics.com.au/blogs/guides/sg90-servo-arduino-guide)

**MG90S specs**
- MG90S (TowerPro, metal gears):
  - stall torque 1.8 kgf·cm at 4.8 V and 2.2 kgf·cm at 6 V
  - speed 0.10 s/60° at 4.8 V and 0.08 s/60° at 6 V
  - voltage 4.2–6 V
  - size 23 × 12.2 × 29 mm, weight 13.4 g
  - out of stock at Eletrogate on the day checked

  — [Eletrogate MG90S](https://www.eletrogate.com/micro-servo-towerpro-mg90s-metalico-t-rex); torque confirmed by [Components101 MG90S](https://components101.com/motors/mg90s-metal-gear-servo-motor) (search snippet)
- MG90S prices in Brazil: R$ 25.27 at WJ Componentes (R$ 23.29 with Pix), and R$ 99.90 for a 5-pack (Fam Aeromodelismo). — [WJ Componentes](https://www.wjcomponentes.com.br/servo-90g) (search snippet); [Fam Aeromodelismo](https://www.famaeromodelismo.com.br/MLB-4879162786-micro-servo-90g-metal-mg90s-_JM) (search snippet)

**Jitter, detaching and holding without power**
- While the servo receives PWM pulses, its drive circuit keeps comparing the target and actual positions and makes small corrections. This draws current even when the servo is "not moving". Putting the control pin into a high-Z state (detach) stops this. — [ripred/tomservo (GitHub)](https://github.com/ripred/tomservo) (search snippet + page)
- "Most hobby servos will happily hold position because of gearbox friction even when no valid PWM signal is present." No measured current numbers are given. — [ripred/tomservo](https://github.com/ripred/tomservo)
- On an ESP32, jitter is usually a power and ground problem. The ESP32 5 V pin cannot power a servo reliably. Recommended fixes:
  - a separate 5 V supply, with the ground shared with the ESP32
  - a 100–470 µF capacitor across the servo supply, placed near the servo
  - short wires

  — search results incl. [PrintBusters FAQ](https://printbusters.io/faq/why-does-my-servo-jitter-or-not-move-properly-on-esp32), [ST_Anything issue #159](https://github.com/DanielOgorchock/ST_Anything/issues/159)
- Arduino forum advice on locking a 3D-printed box:
  - Use a small servo to push or pull the locking pin through a linkage (for example, a piece of paper clip).
  - A stationary SG90 draws only a few mA.
  - Slider-crank linkages are "very" reliable.
  - A servo without a spring needs power to both lock and unlock.
  - Battery projects should disable the motor when idle.

  — [Arduino Forum: best way to lock and unlock a lid box (3D printed)](https://forum.arduino.cc/t/design-question-best-way-to-lock-and-unlock-a-lid-box-3d-printed/657878)

**Existing designs to adapt**
- Printables "Servo Latch – Geocache Box Servo Latch" (by Plexi):
  - designed for an MG90 servo; the SG90 should also work
  - the latch lever pivots on a 3 mm × 38 mm screw in a see-saw action with a small spring
  - a cam mounts on the servo's splined shaft (20 splines, 5 mm)

  — [Printables 134411](https://www.printables.com/model/134411-servo-latch-geocache-box-servo-latch) (search snippet; page returned 403)
- Printables "Servo operated lock" (Tonitwn): a treasure-chest servo lock with BBC micro:bit code. — [Printables 24182](https://www.printables.com/model/24182-servo-operated-lock) (search snippet)
- MyMiniFactory "3D Printable Servo-Lock" (John Larsson): 12 STL parts, printed and tested on an Ender-3. — [MyMiniFactory 365536](https://www.myminifactory.com/object/3d-print-servo-lock-365536) (search snippet)
- Other servo lockboxes:
  - Instructables "The Lock Box" (Arduino, servo as the locking element, IR remote) — [Instructables](https://www.instructables.com/The-Lock-Box/)
  - "SmartVault" (Arduino Nano + servo) — [Instructables](https://www.instructables.com/SmartVault-Arduino-Controlled-3D-Printed-Lockbox/)
  - Hackster rack-and-pinion smart lock — [Hackster](https://www.hackster.io/balli2000in/diy-smart-lock-arduino-rack-pinion-keypad-868103)
  - (all search snippets)
- Cautionary case: an ESP32 IoT lock box (rubenwardy, 2023).
  - The first servo design (pin + paper-clip pushrod + two-part slot) suffered from alignment and friction problems.
  - The second servo design (E-shaped gripper) caused "360° rotations" and broke the lock.
  - The author switched to a commercial solenoid lock powered from a separate MicroUSB port.

  — [rubenwardy blog: 3D-printed IoT lock box using ESP32](https://blog.rubenwardy.com/2023/03/16/lockbox/)

### Inferences
**Force at the arm (F = T / r; 1 kgf·cm = 0.0981 N·m)**

| Servo, voltage | Torque | Force at r = 10 mm | Force at r = 15 mm |
|---|---|---|---|
| TowerPro SG90, 4.8 V | 1.8 kgf·cm | ≈ 17.7 N | ≈ 11.8 N |
| Generic SG90, 4.8 V | 1.2 kgf·cm | ≈ 11.8 N | ≈ 7.8 N |
| MG90S, 4.8 V | 1.8 kgf·cm | ≈ 17.7 N | – |
| MG90S, 6 V | 2.2 kgf·cm | ≈ 21.6 N | – |

These are stall values. Plan on using no more than about half of them.

**Servo arm geometry**
- At r = 10 mm, a 30° rotation moves the arm tip about 5.2 mm (s = r·θ). That is plenty of stroke for a latch that needs 3–4 mm.

**Energy per unlock**
- One unlock costs about 0.3–0.5 A for about 1.5 s, roughly 0.2 mAh. This is negligible for the battery.
- What matters for the battery is (a) the peak current (0.5–0.7 A stall) and (b) the idle current if the servo stays powered (about 10–20 mA per the snippet).
- Detaching the PWM signal removes the "hold" current. Only switching the servo's supply (MOSFET, or a pack switch) brings idle current to zero.

**Load path is the key design rule**
- The pin's pull force should go into printed walls, not into the servo shaft or gears.
- With the recommended spring slider (Q4), the servo never carries the pull load and is detached at rest. Gearbox friction then only has to keep the horn parked out of the way.

**Why rubenwardy's servo designs failed**
- They put the servo in a linkage (paper-clip pushrod) or in a gripper under load.
- A design where the horn directly pushes a tab, with no pushrod, avoids that failure mode.
- The "360° rotation" failure suggests a faulty or continuous-rotation servo. Buy "180°" (positional) servos, since stores also sell 360° versions (see [Saravati](https://www.saravati.com.br/micro-servo-motor-mg90s-2-2kg-cm-engrenagens-de-metal-360.html)).

**SG90 or MG90S**
- The MG90S costs about R$ 10 more and has metal gears. Metal gears resist stripping if someone forces the latch, and give more consistent torque than generic SG90 clones.
- For a demo, buy both an SG90 and an MG90S, or two of either, as spares.

### Gaps
- Neither the TowerPro SG90 datasheet (handsontec PDF, DNS error) nor the MG90S datasheet PDF was opened. Torque figures are from retailer and aggregator pages. Stall current figures conflict (360–750 mA).
- I found no measured idle current for an SG90 that is powered but receives no PWM. The "~10 mA" figure is from a search summary. The team should measure it with a multimeter.
- I could not open the Printables pages (403), so I could not check the geocache latch's geometry, print settings or license.

---

## 2. Solenoid alternatives (5 V push-pull JF-0530B; 12 V "mini fechadura"/LY-03-style lock) compared with a servo for beginners

### Takeaway
Solenoids are fail-secure and have a spring return, but they draw 0.3–2 A while energized. They also need a MOSFET, a flyback diode, a pull-down resistor and, for the 12 V locks, a boost converter. That adds electronics that beginners can get wrong, and battery sag can reset the ESP32. Use the 5 V JF-0530B only as a drop-in replacement actuator for the same printed slider. Keep the 12 V mini lock as a last-resort, off-the-shelf fallback. The servo is simpler for this team.

### Cited Findings
**JF-0530B push-pull solenoid**
- Generic spec: 12 V version, 300 mA, 5 N force, 10 mm stroke, body 30 × 15 × 13 mm, pull-push type; 6, 12 and 24 V versions exist. Keep it on for no more than about 2 s because it heats up. — [Amazon DEVMO JF-0530B](https://www.amazon.com/DEVMO-JF-0530B-Pull-Push-Type-Solenoid-Electromagnet/dp/B07TNPD2SK); [ICStation](https://www.icstation.com/0530b-dc12v-300ma-5n10mm-pull-push-type-solenoid-electromagnet-p-7404.html) (search snippets)
- Current figures conflict: another retailer lists a 12 V JF-0530B at "1A". — [Bot'n Roll](https://www.botnroll.com/en/solenoides/4622-solenoid-jf-0530b-12v-1a-5n-10mm-range.html) (search snippet)
- The 5 V JF-0530B in Brazil (Fermarc):
  - 5 V DC, 2 A
  - 5 N pull, 10 mm stroke
  - body 30 × 16 × 15 mm; movable rod 6 mm × 58 mm
  - spring return: the plunger retracts when energized and the spring returns it when power is off
  - R$ 37.90 (R$ 36.76 with Pix)

  — [Fermarc Mini Solenoide 5V JF-0530B](https://www.fermarc.com/mini-solenoide-5v-jf-0530b)

**12 V mini locks**
- Brazilian retailers describe the 12 V "mini trava/fechadura solenoide" as follows:
  - stainless steel, about 600 mA at 12 V
  - maximum activation time 10 s (a longer pulse can overheat the coil)
  - for Arduino/ESP32
  - R$ 49.90 at Montimport, R$ 55 at Mekanus

  — [MakerHero](https://www.makerhero.com/produto/mini-trava-eletrica-solenoide-12v/) (search snippet; page 403); [Montimport](https://www.montimport.com/mini-fechadura-solenoide-eletrnica-12v-arduino-node-rasp/p/MLB47120027); [Loja Mekanus](https://www.lojamekanus.com.br/MLB-1268997833-mini-fechadura-eletrica-solenoide-12v-arduino-automaco-_JM) (search snippets)
- Usinainfo's range of 12 V locks, all 12 V DC and normally closed (fail-secure), with current around 1 A:
  - FEC-91 27 mm: R$ 34.58–46.17
  - XG07E 73 mm: R$ 33.16
  - SARY 50 mm: R$ 45.89
  - MK-202 73 mm: R$ 62.60
  - JF-0520B 12 V mini lock: R$ 50.18, "1A"
  - some models have a built-in open/close detection switch

  — [Usinainfo mini fechadura list](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide-563)

**Adafruit lock-style solenoid (reference for this lock type)**
- 12 V version:
  - 650 mA at 12 V, 500 mA at 9 V
  - designed for 1–10 s activation
  - no power used at rest (fail-secure); energizing retracts the slug
  - slanted slug (self-latching like a door latch)
  - 41.85 × 53.57 × 27.59 mm, 147.71 g
  - needs a power transistor and a diode; "don't try to power it with a 9V battery"

  — [Adafruit 1512](https://www.adafruit.com/product/1512)
- A smaller Adafruit version is 12 V at 350 mA. — [Adafruit 5065](https://www.adafruit.com/product/5065) (search snippet)

**Driver circuit**
- The IRLZ44N MOSFET is specified for 4 V gate drive, which is above the ESP32's 3.3 V. At about 3 V gate drive it still conducts well enough for loads under 10 A.
- A flyback diode across the inductive load is mandatory.
- Use a 100–220 Ω gate resistor, plus a 10 kΩ gate-to-source pull-down. Without the pull-down, the floating GPIO during ESP32 boot can partly turn the MOSFET on.

  — [ComponentIndex IRLZ44N guide](https://componentindex.net/components/mosfet-irlz44n/); [ElectricalFlux IRLZ44N](https://electricalflux.com/mcu-general/irlz44n-arduino-logic-level-compatibility-wiring) (search snippets)
- A solenoid lock locks whenever the lid shuts and needs power to unlock. Forum users preferred servos or gearmotors for battery projects. — [Arduino Forum](https://forum.arduino.cc/t/design-question-best-way-to-lock-and-unlock-a-lid-box-3d-printed/657878)

### Inferences
**Servo vs solenoid for this team**

| Criterion | SG90/MG90S servo | JF-0530B 5 V | 12 V mini lock (LY-03 style) |
|---|---|---|---|
| Extra electronics | none (3 wires; add a capacitor) | MOSFET + diode + resistors | MOSFET + diode + 12 V boost |
| Peak current | ≈ 0.5–0.7 A | ≈ 2 A at 5 V | ≈ 0.6–1 A at 12 V (≈ 2–3 A from a 1S Li-ion via boost) |
| Holds without power | yes, if the design has a spring | yes (spring return) | yes (fail-secure) |
| Force for opening | ≈ 12–18 N at 10 mm | 5 N (falls with stroke) | built-in |
| Size | 23–32 × 12 × 29 mm | 30 × 16 × 15 mm body + rod | 27–73 mm class; Adafruit 1512 = 42 × 54 × 28 mm |
| Price (BRL) | 14–25 | ≈ 37 | ≈ 33–63 |

**Why the solenoids draw so much from a battery**
- 2 A at 5 V is 10 W. A 12 V lock at 0.6–1 A is 7–12 W.
- From a 3.7 V cell through a boost converter, that is roughly 2–3 A input. That is at or above the limit of the small boost modules beginners buy.
- 4×AA alkaline cells sag at 2 A. Either way the ESP32 can brown out unless the solenoid has its own supply and a large capacitor (≥ 1000 µF).

**Force limitation of the JF-0530B**
- Its 5 N rating means it can only pull back a very light latch spring (about 1–2 N). It cannot release a pin that someone is pulling on, because pulling adds friction to the latch.

**How to use a solenoid if needed**
- The best use is as a drop-in actuator for the same spring slider described in Q4: the solenoid pulls the slider back.
- The 12 V mini lock's slanted steel bolt is itself a ready-made self-latching bolt. However, it is designed for a door strike, not a pin groove. Using it means redesigning the pin as a strike plate or a flat tongue with a window, and the lock is bulky for a 90 × 70 × 30 mm box.

### Gaps
- There is no manufacturer datasheet for the JF-0530B force-vs-stroke curve. The "5 N" is probably the maximum at the end of the stroke. The team should measure it with a luggage scale before relying on it.
- I found no reliable spec sheet for the "LY-03" model name. The notes use the generic Brazilian "mini fechadura solenoide 12V" listings instead.

---

## 3. The pin: commercial EAS pin vs nail vs grooved bolt vs rod with notch, and how the latch engages it without wear

### Takeaway
Commercial EAS pins are cheap, but their shank is only about 1.2 mm with shallow grooves. They are designed for a steel ball clutch and are too small for a printed latch to grip reliably. For the MVP, use a steel (or brass) pin of about Ø3–4 mm with one clear groove. The groove's shoulder must face the pin head and be square, so pulling cannot cam the latch open. The groove can be made by spinning a nail or rod in a hand drill against a file or hacksaw blade. Do not rely on screw threads as the "groove": V-threads push the latch sideways, and a thick printed slot only touches the thread crests.

### Cited Findings
**Commercial EAS pins**
- Real EAS hard tags must hold the pin when "up to an eighty pound pull force is applied to the tack" (80 lbf ≈ 356 N).
- The industry-standard grooved pin has a minimum diameter of 1.2 mm, because thinner grooved pins "would break at the notches". The patent's ball clutch uses three 1.5 mm steel balls to grip pins of 0.76–0.90 mm.

  — [US9053623B2, Security tag for delicate articles](https://patents.google.com/patent/US9053623B2/en)
- EAS flat steel pin (Easwise): head Ø12 mm, shank length 16 or 19 mm, smooth or grooved, 1.8 g each. — [Easwise EAS flat steel pin](https://www.easwise.com/eas-flat-steel-pin.html)
- 16 mm grooved and dome-head pins are common. The grooves "allow the lock to firmly grip the pin". — [INEO Products](https://www.ineoproducts.com/products/dome-head-16mm-grooved-pin) (US$ 75 / 1000); [BigJeffAudio 16 mm grooved flathead pins](https://bigjeffaudio.com/products/1000pcs-16mm-grooved-flathead-security-tag-pins-compatible-with-eas-systems) (search snippet)
- Brazilian prices:
  - replacement pins for rigid EAS tags: about R$ 150 per 1000 at i9 Automação Comercial ("preguinho" of 1.5 cm)
  - 1000 RF mini-tags with pins at WebContinental / Casas Bahia

  — [i9 Automação Comercial](https://www.i9automacaocomercial.com.br/pino-para-etiqueta-rigida-antifurto-eas-md03-1000-un/) (search snippet; page 403); [WebContinental](https://www.webcontinental.com.br/etiqueta-rigida-rf-mini-tag-c-pino-antifurto-para-roupa---branca-1-000-unidades-003166000069/p) (search snippet)

**Why steel pins, and PLA vs PETG**
- Plastic "tag fix" pins (nylon fasteners) are a different product: they are not locking pins. — [Dokassa](https://dokassa.com.br/pino-plastico-tag-fix-pin-antifurto-40mm-com-5-000-unidades-paulimaq-9743) (search snippet)
- FDM parts are weakest across the layers. PLA strength along Z is about 20–35 MPa, against about 55–60 MPa within a layer. Delamination is the most common failure mode. — [3DPrintMetric PLA vs PETG](https://3dprintmetric.com/blog/pla-vs-petg-strength-comparison/) (search snippet); [PMC10880662](https://pmc.ncbi.nlm.nih.gov/articles/PMC10880662/) (search snippet: PLA 59.9 MPa vs PETG 54.9 MPa; PETG bonds better between layers)

### Inferences
**Pin options compared**

| Pin | Verdict | Why |
|---|---|---|
| Commercial EAS pin (Ø ≈ 1.2 mm grooved, 16–19 mm, head Ø12) | Not with a printed latch | Grooves are too shallow and the shank too thin: a plastic edge would indent or slip. It needs a steel clutch (balls or spring-steel jaws). Buy a few only to show the "real" pin, or for a v2. |
| M3/M4 screw, latch engaging the threads | Not recommended | A V-thread flank turns the pull into a sideways force that can push a spring latch open. A thick printed slot touches only the crests. The pin can also be unscrewed by turning its head. |
| Printed pin (PETG, printed lying flat) | Early bench tests only | Theoretical tension at a Ø2.5 mm groove is about 4.9 mm² × 55 MPa ≈ 270 N if printed flat, and much less if printed upright (Z = 20–35 MPa). It cannot pierce fabric, and the groove wears. |
| Steel nail or rod, Ø3–4 mm, with one groove (recommended) | Yes | Steel never fails first. The groove is made with hand tools. It pierces knit fabric or goes through a seam or buttonhole. |
| Clevis pin with an E-clip groove, or pins turned by a machine shop | Best, if easy to get | Precise, square groove; a head is already present. |

**Recommended groove geometry**

| Parameter | Ø4 mm pin (preferred) | Ø3 mm pin (alternative) |
|---|---|---|
| Groove core diameter | Ø2.5 mm (0.75 mm deep) | Ø2.0 mm (0.5 mm deep) |
| Groove width | ≥ latch tip thickness + 0.5 mm (e.g. 3.5–4 mm for a 3 mm tip) | same rule |
| Lower shoulder (toward the tip) | square: it takes the pull | square |
| Upper side (toward the head) | may be tapered | may be tapered |
| Tip | pointed or rounded, to push the latch back on insertion | same |

**Making the groove with hand tools**
- Chuck the nail by the head end in a hand drill and let it spin.
- Hold a flat file or a hacksaw blade square against it until the groove reaches the target diameter.
- Check the diameter with calipers.
- Brass or aluminum rod files much faster than steel, and is still far stronger than the plastic latch.

**Fabric thickness**
- One groove gives a fixed gap between the head and the latch. Put a 2–3 mm EVA or rubber washer under the pin head, or a foam pad on the box face. It takes up fabric thickness from about 0.5 mm (t-shirt) up to about 2 mm (jeans or a fold), much like the multiple grooves on EAS pins.

**Wear**
- The latch bears on the groove shoulder over about half a ring:
  - Ø4/Ø2.5 pin: about (π/4)(4² − 2.5²)/2 ≈ 3.8 mm², so about 13 MPa at 50 N.
  - Ø3/Ø2.0 pin: about 2.0 mm², so about 25 MPa at 50 N.
- The Ø4 pin gives PETG a comfortable margin at demo loads. At the 356 N commercial rating, the stress (about 93 MPa) would crush any printed latch, so the MVP does not attempt that.
- To add a wear surface, glue a thin steel shim (for example, a slice of a flat washer) to the underside of the latch tip. Better: print spare latch sliders (they are small and quick to print).

### Gaps
- I found no published shank diameter or groove depth for the Brazilian "preguinho" EAS pins. The patent's 1.2 mm is described as the US industry norm.
- Brazilian availability and prices for clevis pins with E-clip grooves (Ø3–4 mm), and for plain steel or brass rod, were not searched.
- Ring-shank nails ("prego anelado") could work as ready-made ratchet pins. Their ring depth is unverified and probably too small (well under 0.5 mm) for plastic, so this idea is untested.

---

## 4. Spring-loaded keyhole/slider latch vs direct servo arm; springs; how to print it

### Takeaway
A spring-loaded sliding bolt is more robust than a servo arm entering the groove directly. The bolt works like a door-latch "lingueta" with a chamfered top edge. The pin pushes it aside on insertion, and it snaps into the groove with an audible click. The pull load goes into the box wall, not the servo. It stays locked with zero power. The servo's horn simply pushes a tab to open it for about 1.5 s, then parks clear. Use a metal spring (a ballpoint-pen spring), not a printed PLA spring. The direct-arm design has fewer parts and is the fallback.

### Cited Findings
- PLA makes a very poor spring material. PETG is the recommended printed-spring material, but plastic always creeps under constant load. Commenters note that mass-produced metal springs are available "for pennies" and are clearly better for reliable use. — [Hackaday, "The Challenges of 3D Printing Reliable Springs" (27 Apr 2026)](https://hackaday.com/2026/04/27/the-challenges-of-3d-printing-reliable-springs/)
- If a printed spring stays compressed for a long time, it slowly loses its rebound because of creep. PLA creep is noticeable even well below its glass-transition temperature. — search summaries of [Siraya Tech spring guide](https://siraya.tech/blogs/news/how-to-design-perfect-3d-printed-springs-tips-materials) and [FilamentSpecs creep](https://filamentspecs.com/creep-resistance-3d-printed-parts/)
- In a flexural test, PETG orthoses did not break, while PLA ones failed at 336 N before aging and 215 N after aging. — [PMC11359674](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11359674/) (search snippet)
- The geocache servo latch on Printables uses a pivoting lever with "a small spring" and a servo-driven cam. This confirms that a spring latch opened by a servo is an established hobby pattern. — [Printables 134411](https://www.printables.com/model/134411-servo-latch-geocache-box-servo-latch) (search snippet)
- Forum users recommend spring-loaded latches, and consider slider or slider-crank mechanisms reliable. — [Arduino Forum](https://forum.arduino.cc/t/design-question-best-way-to-lock-and-unlock-a-lid-box-3d-printed/657878)

### Inferences
**Spring slider vs direct servo arm**

| | Spring slider + servo opens | Direct servo arm in the groove |
|---|---|---|
| Locking | Automatic when the pin is pushed in (click); no command, no app step | The ESP32 must command "lock" after insertion (button, app or pin sensor) |
| Holds with power off | Yes, by the spring and geometry | Yes, by gearbox friction only; a bump or vibration can in principle back-drive it |
| Pull load path | Pin → slider → box top wall | Pin → arm tip → printed "roof" above the arm (without the roof, it bends the servo shaft) |
| Parts | Slider, spring, channel | Custom arm and roof |
| Alignment sensitivity | Low (the spring takes up play) | High: the arm tip must match the groove height within about ±0.5 mm; spline play of 1–2° gives about 0.2–0.35 mm at 10 mm radius |
| Beginner risk | Slider sticking (fix with 0.3 mm clearance, light sanding, dry PTFE or graphite) | Arm hits the pin if the pin is not fully inserted |

**Springs**
- Ballpoint-pen compression spring (about Ø5–6 mm): free, consistent, good for about 1–3 N of preload. Seat it on a printed peg or in a Ø6.5 mm pocket.
- Rubber band: works for a week, but creeps and perishes. Keep it only as an emergency spare.
- Printed PLA flexure: avoid. A PETG flexure is possible, but it creeps if it stays loaded for weeks.

**Force budget**
- Spring force of about 2–3 N plus friction is about 3–5 N. A generic SG90 gives about 12 N at a 10 mm arm, a margin of 2–4×.
- If a person is pulling on the pin while the latch opens, friction adds about μ × F_pull. With μ assumed to be 0.3 for plastic on steel (not sourced), a 30 N pull adds about 9 N. The latch may not open until the person stops pulling.
- The demo script should say "release, then pull".

**Printing the slider**
- Print it flat, so the pull bends it within its layers (strong direction).
- Use PETG, 100% infill (a small part), and 0.2 mm layers.
- Print the chamfer as a 45° slope on the top face. Place it so no support is needed, for example by printing the slider upside down or with the chamfer as a bottom 45° slope.

### Gaps
- I did not find a measured spring rate for a typical pen spring. The team should check it with a kitchen or luggage scale.
- I found no published test of how long a printed PETG slider lasts against a steel groove. Wear life is estimated, not sourced.

---

## 5. Forces, materials, wall thickness, infill, orientation, tolerances, wear surfaces

### Takeaway
Design the MVP to hold at least 50 N (about 5 kgf) without damage. That covers an enthusiastic tug in a demo. Commercial tags are rated for about 356 N (80 lbf), and a printed latch cannot match that without steel parts. Use:
- PETG for the slider and the pin guides; PLA is fine for the rest of the box.
- 3 mm walls around the pin, and the slider printed flat.
- 0.3 mm total sliding clearance.
- Pin holes drilled to size with a drill bit.

### Cited Findings
- Target of commercial EAS tags: hold the pin at up to 80 lbf (≈ 356 N). — [US9053623B2](https://patents.google.com/patent/US9053623B2/en)
- Sliding-fit clearance for FDM: 0.2–0.4 mm total (0.1–0.2 mm per side); 0.3 mm is a reliable starting point when both parts come from the same printer. — [Snapmaker tolerances](https://www.snapmaker.com/blog/3d-printing-tolerances/), [Sovol clearances](https://www.sovol3d.com/blogs/news/fdm-3d-printing-tolerances-clearances-how-to-design-parts-that-fit), [3DPut](https://3dput.com/complete-guide-to-3d-printing-tolerances-and-fit-getting-perfect-clearance-for-moving-parts/) (search summaries)
- AON3D rule of thumb: use one extrusion width (about 0.4 mm for a 0.4 mm nozzle) for a sliding fit and two widths for a free-running fit. — [AON3D engineering fits](https://www.aon3d.com/applications/engineering-fits-how-to-design-for-3d-printed-assemblies/) (search summary)
- A well-calibrated FDM printer holds about ±0.2 mm in XY and ±0.1–0.2 mm in Z. Printed holes typically come out 0.1–0.3 mm undersized. — search summaries of [Snapmaker](https://www.snapmaker.com/blog/3d-printing-tolerances/) and [X3D Studios](https://x3dstudios.com/blog/3d-printing-tolerances-guide)
- Strength (search summaries):
  - PLA: about 55–60 MPa within a layer and 20–35 MPa across layers (Z). — [3DPrintMetric](https://3dprintmetric.com/blog/pla-vs-petg-strength-comparison/)
  - PETG: a little lower in XY (54.9 vs 59.9 MPa), with better bonding between layers. — [PMC10880662](https://pmc.ncbi.nlm.nih.gov/articles/PMC10880662/)
  - PETG resists creep and aging better. — [PMC11359674](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11359674/)

### Inferences
**Demo pull force**
- I found no source for how hard people tug a tag in a demo. 50 N (about 5 kg) is a reasonable "firm tug" target, and 100 N (about 10 kg) is a stress case.
- The design numbers below survive 100 N with margin, except for wear on a Ø3 pin.

**Load path and wall thickness (recommended values)**
- Top wall around the pin: at least 3 mm (about 7–8 perimeters with a 0.4 mm nozzle, or 4 perimeters plus solid infill).
- Bosses and screw posts: at least 2.5 mm of wall.
- Side walls: 2 mm.
- Blade tip: 3 mm thick.
- At 50–100 N, a 3 mm top wall around a Ø4.4 mm hole sees small stresses. The failure mode is creep or indentation of the slider tip, not fracture.

**Orientation**
- Box shells: print open side up.
- Slider: print flat.
- Pin-guide plate: print flat.
- Never print a load-bearing hook or tab so that the pull separates its layers.

**Tolerances (recommended values)**
- Slider channel: 0.3 mm larger than the slider in width and in thickness.
- Pin holes: model Ø4.4 mm for a Ø4.0 mm pin, then open to size with a Ø4.5 mm drill bit by hand.
- Horn-to-tab gap at park: 1.5 mm.
- Print a 20 mm "tolerance test" coupon with slots of 0.2, 0.3 and 0.4 mm first, and pick the one that slides freely on the team's printer.

**Infill**
- Box: 20–30%.
- Slider, pin guide and any part near the pin: 100%, or 5 perimeters, which is effectively solid for small parts.

**Wear surfaces**
- The steel pin runs in printed holes. For longer life, press an M4 flat washer into a pocket in the top wall so the pin passes through steel. Its 4.3 mm hole is a good guide for a Ø4 pin.
- The groove shoulder bears on the slider. A glued steel shim under the tip is optional; keep spare sliders instead.

### Gaps
- I found no source for typical human tug forces on retail tags other than the 80 lbf design requirement.
- I did not find compressive or bearing strength values for PETG. The 13–25 MPa bearing estimates in Q3 are compared only against tensile values, which is conservative for bearing.

---

## 6. Confirming lock state (optional)

### Takeaway
A single microswitch that the pin tip presses at the bottom of its pocket confirms that the pin is present. Because the spring latch always snaps in when the pin is fully inserted, "pin present" is effectively "locked". A second switch or a reed switch on the slider is optional. Some off-the-shelf 12 V locks include a detection switch.

### Cited Findings
- Some commercial 12 V electronic locks include built-in open/close detection (for example MK-202, SARY 50 mm, XG07E). — [Usinainfo](https://www.usinainfo.com.br/mini-fechadura-eletrica-solenoide-563)
- The closest open-source analog (smart-security-tag, ESP32 + servo) detects tampering with a wire loop that sounds a buzzer when cut. — noted in the sibling research notes, citing [GitHub kishoreSpandiyan/smart-security-tag](https://github.com/kishoreSpandiyan/smart-security-tag)

### Inferences
**Pin-present switch**
- Mount a mini lever microswitch below the pin guide plate, so the pin tip closes it on the last 1 mm of travel.
- Wire it between an ESP32 GPIO (with `INPUT_PULLUP`) and GND.
- Firmware logic:
  - pin present → report "locked"
  - "unlock" command → move the servo; the switch should open within a few seconds as the shopper pulls the pin
  - pin absent → report "released" and return the servo to park

**Cheaper sensing without a switch**
- The steel pin can bridge two small screws or springs wired to a GPIO and GND. This is less reliable because of contact and oxidation.

**Demo value**
- The switch lets the ESP32 and the phone show "Travado / Liberado" and trigger an alarm if the pin disappears while the tag is still unpaid. That is a good story for the Riachuelo audience.

### Gaps
- I did not search Brazilian prices for mini lever microswitches or reed switches. They are typically a few reais (unverified).

---

## 7. Overall box: size, component fit, battery access, closure

### Takeaway
A box of about 90 × 70 × 30 mm is plausible if:
- the servo lies flat (12–13 mm tall);
- the latch and pin zone sits in one corner, about 30 × 25 mm;
- the ESP32 DevKit and the battery pack sit side by side.

Screw the lid with 4 M3 screws into printed bosses or heat-set inserts, and give the battery its own access. Measure the real parts before modelling, because the size of the battery pack decides everything.

### Cited Findings
- Component sizes:
  - SG90: 32 × 12.6 × 30 mm (with mounting tabs). — [Usinainfo](https://usinainfo.com.br/servo-motores/micro-servo-motor-9g-sg90-180-2299.html)
  - MG90S: 23 × 12.2 × 29 mm. — [Eletrogate](https://www.eletrogate.com/micro-servo-towerpro-mg90s-metalico-t-rex)
  - JF-0530B body: 30 × 16 × 15 mm plus the rod. — [Fermarc](https://www.fermarc.com/mini-solenoide-5v-jf-0530b)
  - Adafruit 12 V lock solenoid: 41.85 × 53.57 × 27.59 mm, 148 g, too bulky for a small tag. — [Adafruit 1512](https://www.adafruit.com/product/1512)
- rubenwardy's lock box: his first case was too small for the electronics. He also warns against putting the lock on a supply that could be reached by reprogramming. — [rubenwardy](https://blog.rubenwardy.com/2023/03/16/lockbox/)

### Inferences
**Layout (top view, 90 × 70 mm, inner height about 25 mm)**
- One end: the pin and latch zone (about 30 × 25 mm), with the servo lying flat beside it (32 × 13 mm footprint including tabs).
- Middle: the ESP32 DevKit (about 50 × 28 mm, not sourced; measure it).
- Other long side: the battery pack. A 4×AA flat holder is typically about 62 × 58 × 15 mm, which fills most of the box. A 2×AA or an 18650 holder is slimmer. The final choice is in the power notes.
- Display: on the lid.

If the parts do not fit, grow the box to about 100 × 70 × 35 mm rather than cramming the latch.

**Closure**
- A two-part shell with 4 M3 screws into printed Ø6 mm bosses, with 2.5 mm pilot holes for self-tapping, or M3 heat-set inserts.
- The lid screws double as the "security" layer: the shopper cannot open the box without a screwdriver.
- For battery access, either use the same screws (simplest) or a separate sliding battery door on the bottom.
- Emergency release: if the ESP32 dies in the demo, opening the 4 screws gives access to the slider, which can be pushed back with a finger. Rehearse this.

**Placement of the pin hole**
- Put it at least 8 mm from any wall, so the latch channel and spring fit.
- Keep the pin axis perpendicular to the top face.

### Gaps
- I did not source the dimensions of the ESP32 DevKit, the AA or 18650 holders, or the display. The sibling notes on the board, battery and display cover these. The figures above are approximate and must be measured.

---

## 8. Recommendation: one mechanism + fallback (sketch, parts, dimensions, print settings, assembly)

### Takeaway
**Recommended:** a spring-loaded sliding latch bolt ("lingueta com mola") engaging a grooved Ø4 mm steel pin, opened by a micro servo (MG90S preferred, SG90 acceptable) whose horn pushes a tab on the slider.
- It locks itself when the pin is pushed in, holds with zero power, and keeps the servo out of the load path.
- It costs under R$ 50 in parts, excluding the ESP32, battery and display.

**Fallback A (same hardware, fewer parts):** a custom servo arm that swings into the groove under a printed "roof". The ESP32 commands the lock.

**Fallback B (if the servo misbehaves):** keep the spring slider and pull it back with a 5 V JF-0530B solenoid through a MOSFET with a flyback diode, on a supply that can give 2 A pulses.

### Cited Findings
- Servo force, detach behavior and prices — see Q1 ([Usinainfo SG90](https://usinainfo.com.br/servo-motores/micro-servo-motor-9g-sg90-180-2299.html), [Eletrogate MG90S](https://www.eletrogate.com/micro-servo-towerpro-mg90s-metalico-t-rex), [WJ Componentes MG90S](https://www.wjcomponentes.com.br/servo-90g), [tomservo](https://github.com/ripred/tomservo)).
- Solenoid specs, prices and driver needs — see Q2 ([Fermarc JF-0530B 5V](https://www.fermarc.com/mini-solenoide-5v-jf-0530b), [ComponentIndex IRLZ44N](https://componentindex.net/components/mosfet-irlz44n/)).
- Metal springs rather than printed ones — [Hackaday 2026](https://hackaday.com/2026/04/27/the-challenges-of-3d-printing-reliable-springs/).
- 0.2–0.4 mm sliding clearance — [Snapmaker](https://www.snapmaker.com/blog/3d-printing-tolerances/), [AON3D](https://www.aon3d.com/applications/engineering-fits-how-to-design-for-3d-printed-assemblies/).
- Pull rating of real tags (80 lbf) — [US9053623B2](https://patents.google.com/patent/US9053623B2/en).

### Inferences
**Mechanism sketch (all dimensions are starting values; the pin axis is vertical and the slider moves horizontally along X just under the top wall)**

```
        pin head (Ø10–12) + EVA washer 2–3 mm
        ───────────┬───────────  garment
   ════════════════╪═══════════════  top wall (3 mm, hole Ø4.4, optional M4 washer insert)
    [spring]→[====SLIDER====>]│      slider 3 mm thick, tip has U-notch R1.35 + 45° top chamfer
          ↑tab    ← servo horn pushes tab to open
   ─────────────── ┼ ───────────────  pin guide plate (3 mm, hole Ø4.4), 0.5–1 mm below slider
                   ┴  pin tip → presses microswitch (optional)
```

**Pin**
- Ø4 mm steel nail or rod (brass or aluminum is easier to file), 22–25 mm long below the head, with a pointed or rounded tip.
- Groove: core Ø2.5 mm, width 4 mm.
- The lower (square) shoulder sits about 9–10 mm below the head's underside. That is the EVA washer (2–3) + fabric (about 1) + top wall (3) + slider (3) + 0.3 mm. Tune it on the real part.
- Make 3–4 pins; one is used in each demo run.

**Slider (PETG, 100% infill, printed flat)**
- 30 × 8 × 3 mm.
- Front tip: U-notch of radius 1.35 mm (fits the Ø2.5 core with 0.1 mm clearance per side), and a 45° chamfer about 1.5 mm on the top front edge.
- Rear: spring peg Ø3 × 6 mm, and a vertical tab 3 × 3 × 6 mm for the servo horn.
- Travel: 4 mm. It needs about 3 mm to clear the Ø4 pin: 0.75 mm engagement plus margin.
- Print 3 spares.

**Channel**
- 8.3 × 3.3 mm cross-section, formed between the top wall and a printed rail or the pin-guide plate.
- A hard stop defines the forward "locked" position. Without it, the spring would push the notch against the pin core and drag.

**Spring**
- A ballpoint-pen compression spring, preloaded 3–5 mm, giving about 1–3 N (measure it).

**Servo**
- MG90S (or SG90) lying flat, with the single-arm horn at about r = 10 mm.
- Park position: the horn is 1.5 mm clear of the tab with the slider forward.
- Open position: park + 40°. The tip moves about 7 mm: 1.5 mm gap + 4 mm slider travel + margin.
- Screw the servo to printed ears; do not rely on glue alone.

**Electronics for the latch**
- Servo signal to an ESP32 GPIO (for example GPIO 13).
- Servo V+ from the 4×AA pack (4.8–6 V, which is in the servo's rated range) or from a 5 V rail. Not from the ESP32's 3.3 V pin.
- Common GND.
- A 470 µF capacitor across the servo supply.
- Optional: a logic-level MOSFET to switch servo power off when idle.
- Optional: a pin-present microswitch to a GPIO with `INPUT_PULLUP`.

**Firmware outline (ESP32Servo library)**
1. On "unlock": `attach(pin)`, then `write(OPEN)`.
2. Wait about 1500 ms; the shopper pulls the pin.
3. `write(PARK)`, wait about 400 ms, then `detach()`.
4. Report the state from the microswitch.
5. Never leave the servo pushing against the tab. Always return to park, so the spring can re-lock on the next insertion.

**Print settings**
- Material: PETG for the slider, the pin-guide plate, and the top wall if printed as a separate lid; PLA is acceptable for the rest.
- Layers and walls: 0.2 mm layers, 4–5 perimeters.
- Infill: 20–30% for the box, 100% for the latch parts.
- Clearances: 0.3 mm for sliding fits.
- Holes: drill to final size by hand.
- Before the real parts, print a 0.2/0.3/0.4 mm clearance test.

**Parts list and budget for the mechanism only (Sept 2026 prices from the pages cited above)**

| Part | Price | Source |
|---|---|---|
| MG90S servo | ≈ R$ 25 | WJ Componentes |
| SG90 servo (spare) | ≈ R$ 15 | Usinainfo |
| Nail/rod Ø4 mm, EVA sheet, M3 screws, M4 washer | a few reais (not sourced) | hardware store |
| Pen spring | free | a ballpoint pen |
| Capacitor 470 µF, microswitch | a few reais (not sourced) | – |
| PETG/PLA filament | < 100 g | – |
| Total | ≈ R$ 50 | – |

Optional fallback B: JF-0530B 5 V (R$ 37.90) + logic-level MOSFET + diode.

**Assembly and test tips**
1. Print the slider and the channel first as a 40 × 40 mm "test block" with the pin hole. Hand-test insertion and pull 20 times before designing the rest of the box.
2. Deburr the slider tip and channel with a craft knife. Rub graphite pencil into the channel; do not use oil on PLA or PETG.
3. Test pulls with a luggage scale: 30 N, then 50 N, then 100 N. Check that the slider tip is not indented. If it is, move to the Ø4 pin, a thicker tip, or a steel shim.
4. Run 100 lock and unlock cycles on the bench with the real battery. This catches brownouts and a horn slipping on its spline; use the horn screw.
5. Demo script: "pay → click → tag opens → pull". Tell presenters not to pull while the servo is moving.
6. Bring 2 assembled spare tags, spare sliders and pins, a screwdriver for the emergency release, and fresh batteries.

**Fallback A (direct servo arm)**
- Replace the slider and spring with a printed arm (PETG, 3 mm thick tip) on the servo spline, swinging in the groove plane.
- Add a printed roof 0.3 mm above the arm's tip path, so the pull load goes into the roof, not the servo shaft.
- Lock = arm in the groove; unlock = arm swung 60–90° away.
- It needs a "lock" command: triggered by the microswitch when the pin is inserted, or by a button.
- It holds unpowered only through gearbox friction ([tomservo](https://github.com/ripred/tomservo)).
- It is simpler to print but less forgiving of groove-height errors.

**Fallback B (solenoid)**
- Same slider, but pulled back by a JF-0530B through a small printed link.
- Use a very light spring: the solenoid gives only 5 N and less over long stroke.
- It needs a MOSFET, a flyback diode, a 10 kΩ pull-down, and a supply or capacitor that can deliver about 2 A pulses without resetting the ESP32.
- Pulse it for 1 s at most; the product warns about heating.

### Gaps
- None of these geometries has been built and tested. All dimensions are first-iteration values from the arithmetic above, and must be tuned on the team's printer with the real pin and fabric.
- I found no existing Printables/Thingiverse model of a garment pin lock (the sibling note "projetos_parecidos" reached the same conclusion). The latch must be modelled by the team. The Printables geocache servo latch and the MyMiniFactory Servo-Lock are the closest references for servo-plus-spring latch geometry.
