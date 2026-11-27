# Phone-to-tag communication for the Tag&Go MVP (iPhone + Android, no app, ESP32 on battery)

Research date: 2026-09-29. Scope: how the shopper's phone tells the ESP32 tag to unlock after a simulated payment. Battery sizing, the release mechanism and the 3D-printed enclosure are outside this scope.

## Option A: Wi-Fi + MQTT (static HTTPS page -> MQTT over WSS -> broker -> ESP32)

### Takeaway
This is the only option that works on both iPhone Safari and Android Chrome with no app installed. The page is a static HTTPS page (GitHub Pages) that loads mqtt.js and publishes over `wss://` to a free broker, and the ESP32 subscribes to the same broker over plain TCP 1883 (public broker) or TLS 8883 (private free-tier broker). Several free brokers expose the required secure-WebSocket port. None of them guarantees uptime, so the demo should configure two of them.

### Cited Findings
**Free public brokers (no account needed)**
- HiveMQ public broker: host `broker.hivemq.com`; TCP 1883, TLS TCP 8883, WebSocket 8000, TLS WebSocket 8884. — [HiveMQ MQTT Dashboard / public broker](https://www.mqtt-dashboard.com/)
- HiveMQ says the public broker "must not be used in Production, Dev, Staging or UAT environments". It adds that HiveMQ "does not commit to an uptime percentage" and may update the instances "which may lead to message loss". HiveMQ may disconnect or ban clients at any time and makes no guarantees on bandwidth or latency. Anyone can access the broker, so no sensitive data should be sent. — [mqtt-dashboard.com](https://www.mqtt-dashboard.com/)
- HiveMQ markets the public broker for "quick connection tests and MQTT experiments". It is "public and shared, so it is not intended for private or production data". — [HiveMQ public broker page](https://www.hivemq.com/mqtt/public-mqtt-broker/)
- EMQX public broker: host `broker.emqx.io`; TCP 1883, WebSocket 8083, TLS 8883, secure WebSocket 8084 with path `/mqtt`, i.e. `wss://broker.emqx.io:8084/mqtt`. EMQX describes it as a "global, geo-distributed EMQX cluster" for prototyping and learning, not production. All messages are visible to other users. — [EMQX public broker page](https://www.emqx.com/en/mqtt/public-mqtt5-broker); [EMQX blog: MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket); [EMQX MQTT.js tutorial](https://www.emqx.com/en/blog/mqtt-js-tutorial)
- There are user reports of the EMQX public WSS 8084 endpoint failing to connect at times ("wss in 8084 port stop to work with mqttx"). — [emqx/MQTTX issue #1733](https://github.com/emqx/MQTTX/issues/1733); [MQTTX discussion #1847](https://github.com/emqx/MQTTX/discussions/1847)
- test.mosquitto.org ports: 1883/1884 plain MQTT; 8883/8885 TLS with a self-signed CA; 8886 TLS with Let's Encrypt; 8080 WebSockets; 8081 secure WebSockets with a Let's Encrypt certificate; 8090/8091 other WS variants. The operator warns it "will often be running unreleased or experimental code and may not be as stable as you might hope" and "may also be slow—the broker often runs under valgrind or perf". It also says "please do not abuse or rely upon it for anything of importance" and "anybody could be listening". — [test.mosquitto.org](https://test.mosquitto.org/)

**Free private brokers (account needed)**
- HiveMQ Cloud Serverless (free): "100 connections", "10 GB/Month", "No credit card required", MQTT over WebSockets supported, TLS encryption and RBAC. It is "A basic MQTT broker for learning and experimenting" with "No uptime SLA" and community support only. — [HiveMQ pricing](https://www.hivemq.com/pricing/)
- EMQX Cloud has a free offer of "1M session min/month". Detailed quotas were not visible on the page fetched. — [EMQX public broker page](https://www.emqx.com/en/mqtt/public-mqtt5-broker)
- Adafruit IO free plan: 10 feeds, 5 dashboards, 30 days of storage, 30 data points per minute. Going over 30 per minute temporarily blocks the account. Adafruit IO+ costs US$10/month or US$99/year. — [Adafruit Learning System: IO Plus](https://learn.adafruit.com/welcome-to-adafruit-io/io-plus); [Adafruit IO data policies](https://learn.adafruit.com/adafruit-io/data-policies)

**Browser side (mqtt.js)**
- In browsers, MQTT.js supports only MQTT over WebSockets. The README says "you must use ws:// or wss:// protocols". The bundle is available from unpkg at `https://unpkg.com/mqtt/dist/mqtt.min.js`. Example: `mqtt.connect('wss://test.mosquitto.org', {clientId, username, password, reconnectPeriod: 1000})`. v5 was "Completely rewritten in Typescript". — [MQTT.js GitHub](https://github.com/mqttjs/MQTT.js)
- An HTTPS page cannot open a `ws://` connection. Browsers throw "SecurityError: Failed to construct 'WebSocket': An insecure WebSocket connection may not be initiated from a page loaded over HTTPS". Only `wss://` works from a GitHub Pages page. — [Medium write-up of the error](https://hungchienhsiang.medium.com/securityerror-failed-to-construct-websocket-an-insecure-websocket-connection-may-not-be-f2d1d5289a33); [Mozilla bug 917829](https://bugzilla.mozilla.org/show_bug.cgi?id=917829)
- MDN's mixed-content page lists fetch/XHR as blockable. Private-IP hosts are not upgraded but blocked. MDN treats only loopback (`localhost`, `127.0.0.1`) as a secure origin, not LAN IPs such as 192.168.x.x. — [MDN Mixed content](https://developer.mozilla.org/en-US/docs/Web/Security/Mixed_content)

**ESP32 side**
- Random Nerd Tutorials' ESP32 MQTT tutorial uses PubSubClient: `client.setServer(mqtt_server, 1883)`, `client.setCallback(callback)`, `client.subscribe(...)` inside a `reconnect()` loop that retries every 5 s. The authors say PubSubClient "is not fully compatible with the ESP32" but was "working very reliably during our tests". They mention AsyncMqttClient as a non-blocking alternative, because PubSubClient's reconnect loop blocks when the broker is down. — [Random Nerd Tutorials: ESP32 MQTT publish/subscribe](https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/)
- For TLS to HiveMQ Cloud on port 8883, the usual pattern is `WiFiClientSecure` plus a root CA certificate in PROGMEM, used with PubSubClient and broker username/password. Working examples can be run in the Wokwi simulator. — [Wokwi: HiveMQ Cloud with ESP32](https://wokwi.com/projects/381829353297474561); [Wokwi: HiveMQ Cloud with ESP32 working](https://wokwi.com/projects/393711893949907969); [HiveMQ forum: ESP32 with root certificate](https://community.hivemq.com/t/connecting-esp32-to-cloud-hivemq-using-root-certificate/1770)

### Inferences
- **Simplest reliable combination:** the page publishes to `wss://broker.hivemq.com:8884/mqtt` or `wss://broker.emqx.io:8084/mqtt`, and the ESP32 subscribes to the same broker on TCP 1883 with no TLS. The ESP32 needs no certificates, which removes the most common beginner failure (TLS/CA errors). This works because both endpoints of a public broker are the same broker. Test it on day 1.
- **More "credible" variant:** HiveMQ Cloud Serverless (free, private, username/password, TLS). The cost is a CA certificate in the firmware and broker credentials in the public page's JavaScript. Credentials in client-side JS are visible to anyone, so this raises the bar only slightly. Use it if the team has time after the public-broker version works.
- Configure two brokers (HiveMQ primary, EMQX secondary), selectable by a URL parameter on the page (e.g. `?b=2`) and by a fallback list on the ESP32. No public broker gives an uptime guarantee.
- mqtt.js from a CDN: pin a major version (e.g. `https://unpkg.com/mqtt@5/dist/mqtt.min.js`) so a future release does not break the demo. Better still, copy the file into the GitHub Pages repo so the demo does not depend on unpkg.
- PubSubClient is the easiest library for novices and has the most tutorials. Its default maximum packet size is small (commonly 256 bytes; verify in the library). Keep payloads short or call `client.setBufferSize()`. ESP-IDF MQTT and AsyncMqttClient are more robust but harder for beginners.
- Test on the real hotspot whether the shopper's phone on a restrictive network (classroom Wi-Fi) can reach non-443 ports (8884/8084). If it cannot, the shopper's phone should use mobile data.

### Gaps
- No source found giving measured end-to-end latency (page publish to ESP32 callback) for HiveMQ or EMQX public brokers. HiveMQ explicitly gives no latency guarantee. Maker reports usually describe it as near-instant (sub-second), but this is unverified; the team should measure it (e.g. timestamp in payload, 20 trials).
- Could not confirm whether HiveMQ Cloud Serverless or EMQX Serverless offer WSS on port 443 (useful behind firewalls). The HiveMQ pricing page did not state the WSS port.
- The EMQX Cloud free-tier fetch showed only "1M session min/month". Connection and traffic caps were not visible.
- The mqtt.js README fetch reported v5.0.0 as the "latest". That is the v5 changelog headline; the actual latest 5.x minor version in 2026 was not confirmed.

## Option B: Web Bluetooth (phone talks BLE directly to the tag)

### Takeaway
It does not satisfy the iPhone requirement. As of August 2026, Safari on iOS does not support Web Bluetooth, and the only workaround is installing a Safari extension or a special browser, which breaks the "no app installation" rule. It works on Chrome for Android, Samsung Internet and desktop Chrome/Edge.

### Cited Findings
- caniuse (data updated August 2026): Safari on iOS/iPadOS has no native support. A third-party Safari web extension, iOSWebBLE, polyfills `navigator.bluetooth` by bridging to CoreBluetooth, but the user must install it. Chrome for Android is supported (v154 listed). Samsung Internet is supported from 6.2. Firefox has no support in any version, and Mozilla's standards position is "Harmful". Chrome desktop has supported it since 56 and Edge since 79. Global support is about 78%. — [caniuse: Web Bluetooth](https://caniuse.com/web-bluetooth)

### Inferences
- With Web Bluetooth, iPhone shoppers (a large share of Riachuelo's customers would be expected to use iPhones) could not unlock without installing something. That is not acceptable for the MVP brief. Web Bluetooth could be an optional Android-only offline path, but it adds a second code path for little demo value.
- BLE would save energy on the tag compared with Wi-Fi, which is the main argument for a real product. A real product would likely use a native app or App Clip rather than the browser.

### Gaps
- The WebKit team's formal position statement was not fetched in this session. caniuse only summarizes it as "Safari opposes".

## Option C: other routes (ESP32 as its own access point / captive portal, HTTP backends, Web NFC)

### Takeaway
An ESP32 SoftAP + captive portal works without internet and has been shown to work on iPhone, but the UX is poor for a shopper. The phone must leave its Wi-Fi/4G context, iOS popups are inconsistent, and there is a small client limit. It is a good offline fallback for the demo but a weak primary path. HTTP backends (Firebase RTDB, Adafruit IO) work but add accounts, keys and rate limits without being simpler than MQTT. Web NFC is Android-Chrome only.

### Cited Findings
**SoftAP + captive portal**
- A captive portal runs the ESP32 in AP mode (usually 192.168.4.1). A DNS server answers every domain lookup with the ESP32's IP, so the phone's connectivity check (e.g. `captive.apple.com`) lands on the ESP32 page. — [Harald Kreuzer: ESP32 provisioning captive portal](https://www.haraldkreuzer.net/en/news/esp32-wifi-provisioning-soft-ap-and-captive-portal); [iotespresso: captive portal](https://iotespresso.com/create-captive-portal-using-esp32/)
- Some iPhones disconnect from a Wi-Fi network with "no Internet connection" when they cannot reach expected internet resources, which is a problem for offline captive portals. — [espboards.dev: ESP32 captive portal issues](https://www.espboards.dev/troubleshooting/issues/wifi/esp32-captive-portal-issues/); [Apple Developer Forums thread 71629](https://developer.apple.com/forums/thread/71629)
- CDFER/Captive-Portal-ESP32, described as an example "that actually works": the popup appears on iPhone X (iOS 16.2) and iPhone 5c (iOS 10.3.3) and on Samsung Android 9/12 devices, with no popup on macOS after Big Sur. Some phones need cellular data turned off (OnePlus 6 gets stuck on IP assignment with cellular on). There is a "Maximum of 4 clients connected at the same time". It needs AsyncTCP, ESPAsyncWebServer and DNSServer. — [CDFER/Captive-Portal-ESP32](https://github.com/CDFER/Captive-Portal-ESP32)
- Since Chrome 142 (shipped 28 Oct 2025), a public HTTPS site that sends requests to a private IP (192.168.x.x, 10.x, 172.16.x), localhost or a `.local` name triggers a Local Network Access permission prompt, per site and per user. — [Chrome for Developers: Local Network Access prompt](https://developer.chrome.com/blog/local-network-access); [Steele O'Brien: Chrome LNA](https://steeleobrienconsulting.com/blog/chrome-local-network-access/)

**HTTP backends instead of MQTT**
- Firebase Realtime Database on the free Spark plan allows at most 100 simultaneous connections, and this limit cannot be raised. The common ESP32 library is Mobizt's Firebase ESP Client, and Random Nerd Tutorials has an ESP32 + RTDB tutorial. — [Firebase RTDB limits](https://firebase.google.com/docs/database/usage/limits); [Random Nerd Tutorials: ESP32 Firebase RTDB](https://randomnerdtutorials.com/esp32-firebase-realtime-database/); [Arduino docs: Firebase ESP32 Client](https://docs.arduino.cc/libraries/firebase-esp32-client/)
- Adafruit IO free: 30 data points/min; exceeding it temporarily blocks the account. — [Adafruit IO data policies](https://learn.adafruit.com/adafruit-io/data-policies)

**Web NFC**
- caniuse (August 2026): Web NFC works only in Chrome for Android (v154) and Baidu Browser. It does not work in Safari iOS, Samsung Internet, Firefox or desktop Chrome. Safari opposes it and Firefox marks it "Harmful". — [caniuse: Web NFC](https://caniuse.com/webnfc)

### Inferences
- **The GitHub Pages page cannot talk directly to the ESP32 on the LAN.** The page is HTTPS and the ESP32 serves plain HTTP on a private IP, so mixed-content blocking applies, and Chrome's Local Network Access prompt also appears. That rules out the idea of "the page on github.io calls http://192.168.x.x/unlock". Any local path must be a page served by the ESP32 itself over http.
- The SoftAP flow for a shopper is: scan a Wi-Fi-join QR, join the tag's network (losing internet), wait for the captive sheet, pay, unlock, then rejoin the normal network. That is many steps and fragile on iOS, so it should not be the primary path. As a **presenter-only offline fallback** it is valuable: the presenter's phone joins "TagGo-Demo-XXXX" and opens `http://192.168.4.1`. This works without internet or a broker.
- Firebase RTDB is a reasonable alternative to MQTT (it has a JS SDK for the page and a library for the ESP32). But it needs a Google project, security rules and an API key, and the ESP32 library is heavier than PubSubClient. For a one-command demo, MQTT is simpler.
- Web NFC would exclude iPhones. An NFC sticker that simply opens the same URL (NDEF URL record) works on both platforms without Web NFC, so the tag could carry the QR and an optional NFC sticker pointing to the same page.

### Gaps
- Google Apps Script as a free polling backend was not researched (no sources fetched). Its quotas and latency are unknown here.
- Supabase Realtime free-tier limits were not researched in this session.
- iOS scanning of `WIFI:` QR codes from the Camera app is widely used but was not confirmed with a source in this session.

## Security that is simple but credible for the demo (tag ID + nonce, single use)

### Takeaway
Use a random, unguessable topic per tag plus a one-time nonce that the tag generates and rotates after every unlock. This blocks accidental triggering, stale or replayed messages and casual pranks on the public broker. It is not real security, because anyone subscribed to the public broker can see the messages. Present it honestly as the protocol a production payment backend would sign.

### Cited Findings
- Public brokers (HiveMQ, EMQX, Mosquitto) are readable by anyone: "anybody could be listening", and messages are visible to other users. — [test.mosquitto.org](https://test.mosquitto.org/); [EMQX blog: MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket); [mqtt-dashboard.com](https://www.mqtt-dashboard.com/)
- The reference smart-locker project (MicaellaSalili/smartlocker) uses per-locker topics `smartlocker/locker/{LOCKER_ID}/unlock` / `lock` / `status`, with plain-text `UNLOCK`/`LOCK` commands and JSON status. It has no authentication, nonce or token. — [smartlocker ESP32 code](https://github.com/MicaellaSalili/smartlocker/blob/main/ESP32_SmartLocker_Code.ino)
- HiveMQ Cloud free offers per-user credentials (RBAC) and TLS, which lets the team keep strangers off the broker. — [HiveMQ pricing](https://www.hivemq.com/pricing/)

### Inferences
- **Proposed protocol (works with a printed, static QR):**
  1. The QR contains only the page URL and tag ID, e.g. `https://<user>.github.io/taggo/?t=K7Q9-3FXA`. The tag ID is 8+ random characters, so the topic is hard to guess.
  2. At boot and after every unlock, the ESP32 generates a random nonce (`esp_random()`). It publishes the nonce **retained** to `taggo/K7Q9-3FXA/state` as `{"s":"locked","n":"a91f3c"}`.
  3. On load, the page subscribes to `.../state` and receives the current nonce immediately, because the message is retained. It shows "Etiqueta conectada" (tag connected) and the price.
  4. After the simulated payment, the page publishes to `taggo/K7Q9-3FXA/cmd`: `{"c":"unlock","n":"a91f3c","ts":...}`.
  5. The ESP32 accepts the command only if `n` equals its current nonce. It then turns the LED green, enables the release (servo, or a button that is only armed now) and publishes `{"s":"unlocked"}` (with ack). It invalidates the nonce and generates a new one after re-locking.
  6. The page shows "Liberado" (released) only after receiving the ack. With no ack within ~5 s, it retries once and then shows an error. This avoids a false "paid and released" state.
- **Variant with a dynamic QR:** if the tag has a small display (OLED/e-paper), the QR itself can include the nonce (`?t=...&n=...`). This is closer to the "nonce in the QR" idea in the brief but adds hardware and power draw. The retained-state approach above gets the same one-time property with a printed QR.
- **Honest framing for the demo:** say that in production the unlock token would be signed by the payment backend (e.g. an HMAC with a secret the tag and the server share, never exposed in the browser), and that the MVP demonstrates the flow and one-time token logic, not the cryptography. Optionally use HiveMQ Cloud credentials so outsiders cannot publish.
- Keep the physical "unlock" as a local action gated by state (LED green plus the button becoming active), so a stray message cannot drive a motor unexpectedly.

### Gaps
- No source found for a ready-made ESP32 + static-page MQTT project that already implements nonce/one-time tokens. The design above is original and should be tested.

## Simulated payment UX on the web page

### Takeaway
A self-made "Pagamento simulado" screen (fake card or Pix confirmation, with an explicit "modo demonstração" label) is the simplest and most honest option and has no external dependency. Stripe Payment Links in test mode can be used with no code and redirect back to the page, but this adds an account, a redirect and an external dependency, and can be bypassed without server-side verification.

### Cited Findings
- Stripe Payment Links can be set to "Don't show a confirmation page" and redirect to a custom URL. Stripe replaces the literal `{CHECKOUT_SESSION_ID}` in that URL with the session ID. This works in test mode as well as live mode. Stripe recommends retrieving the session on a server to verify payment status before confirming. — [Stripe: After a payment link payment](https://docs.stripe.com/payment-links/post-payment); [Stripe: Customize checkout for Payment Links](https://docs.stripe.com/payment-links/customize)

### Inferences
- Recommended page flow (mobile-first, a single HTML file):
  1. Product card with name, price and "Etiqueta conectada ✓" (shown after the retained state arrives).
  2. "Pagar" button leading to a choice of Pix or Cartão. The Pix path shows a fake Pix QR plus a "Simular confirmação do Pix" button. The Cartão path uses a pre-filled test card `4242 4242 4242 4242` and "Confirmar".
  3. 1.5 s spinner "Processando…", then publish the unlock and wait for the ack, then a green "Pagamento aprovado · Etiqueta liberada".
  4. Persistent banner: "Demonstração — nenhum pagamento real é processado".
- Stripe test mode is "trivial" only if a team member already has a Stripe account. Without a backend, the redirect page cannot verify payment, so it is just as simulated as a fake screen. It adds an external dependency and a context switch during the live demo.
- Mercado Pago sandbox was not researched. It typically needs test users and a backend, so it is not recommended for this MVP.

### Gaps
- Mercado Pago sandbox requirements (test users, whether it needs a backend) were not verified in this session.
- Whether Stripe account creation in Brazil for test mode needs a CNPJ/CPF was not verified.

## Hosting the page (GitHub Pages and alternatives)

### Takeaway
GitHub Pages is free for public repositories and serves a static `index.html`. That is all this architecture needs, since all logic is client-side JS plus the broker. Allow up to 10 minutes for changes to publish.

### Cited Findings
- Steps: create the repository, then go to Settings > Pages. Choose the publishing source branch/folder (e.g. `main` / root or `/docs`), put an `index.html` at the top of that source, and the site builds automatically via GitHub Actions. — [GitHub Docs: Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- On GitHub Free, the repository must be public. Pages sites are public even if the repo is private (on paid plans). Changes can take up to 10 minutes to publish. Pages does not support server-side languages (PHP, Ruby, Python). — [GitHub Docs: Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

### Inferences
- The URL will be `https://<user>.github.io/<repo>/`. `github.io` sites are served over HTTPS, which is why `wss://` is mandatory. HTTPS behaviour is covered on GitHub's "Securing your GitHub Pages site with HTTPS" page, which was not fetched in this session.
- The public repo must not contain anything secret. With a public broker there is nothing secret. With HiveMQ Cloud, the broker credentials will be visible in the JS anyway (see the security section).
- Netlify (drag-and-drop deploy) and Cloudflare Pages are equivalent free static-HTTPS alternatives, and either is a backup if GitHub Pages has an outage. Not verified in this session.
- Generate the QR codes from the final URL with any free QR generator. Print them at ≥2 cm with a quiet zone so they scan quickly under classroom lighting.

### Gaps
- Current GitHub Pages bandwidth/size soft limits and HTTPS-enforcement details were not captured from the page fetched.
- Netlify/Cloudflare Pages free-tier terms were not researched.

## Wi-Fi at USP/Poli and ESP32 radio limitations

### Takeaway
Use a phone hotspot, not eduroam. ESP32 (classic, S3, C3) is 2.4 GHz only. ESP32 technically supports WPA2-Enterprise (PEAP), but it needs personal USP credentials in the firmware and has known connection problems. On iPhone, turn on "Maximize Compatibility" so the hotspot uses 2.4 GHz.

### Cited Findings
- ESP32-C3 supports 2.4 GHz Wi-Fi 4 only. ESP32-C5 is Espressif's dual-band 2.4 + 5 GHz Wi-Fi 6 part. — [Espressif ESP32-C5 product page](https://www.espressif.com/en/products/socs/esp32-c5); [OpenELAB: C3 vs C6 vs C5](https://openelab.io/blogs/learn/difference-between-esp32-c3-esp32-c6-and-esp32-c5)
- iPhone hotspots can default to 5 GHz, which the ESP32 cannot join. The fix is the "Maximize Compatibility" toggle on the Personal Hotspot settings page. — [SensorPush support: iPhone Personal Hotspot](https://support.sensorpush.com/hc/en-us/articles/4404419632023-Why-can-t-I-connect-to-the-Personal-Hotspot-on-my-iPhone); [Arduino Forum: ESP32 + iPhone 13 hotspot](https://forum.arduino.cc/t/esp32-wifi-connectivity-issue-with-iphone13-hotspot/1127501); [Apple Developer Forums 686586](https://developer.apple.com/forums/thread/686586)
- ESP32 supports WPA2-Enterprise. The official arduino-esp32 example `WiFiClientEnterprise.ino` connects to eduroam-style PEAP with `WiFi.begin(ssid, WPA2_AUTH_PEAP, identity, username, password)`. ESP8266 does not support PEAP/TTLS-MSCHAPv2. — [arduino-esp32 WiFiClientEnterprise example](https://github.com/espressif/arduino-esp32/blob/master/libraries/WiFi/examples/WiFiClientEnterprise/WiFiClientEnterprise.ino); [Elektor: ESP32 on WPA2 Enterprise](https://www.elektormagazine.com/labs/how-connect-esp32-to-wpawpa2-enterprise-network)
- There are open reports of ESP32 enterprise connections failing. — [arduino-esp32 issue #5027](https://github.com/espressif/arduino-esp32/issues/5027); [ESP32 forum: ESP32 and eduroam](https://esp32.com/viewtopic.php?t=4727)

### Inferences
- Recommended: the presenter's phone hotspot with a simple WPA2-Personal SSID/password hard-coded in the firmware (e.g. `TagGo-Demo`). Prefer an Android phone as the hotspot if available, since it lets you force 2.4 GHz explicitly. If using an iPhone, enable "Maximize Compatibility" and keep the Personal Hotspot screen open during the demo. iPhones may stop advertising the hotspot when no device is connected and settings are closed; this is a commonly reported behaviour not verified by a source here.
- Keep a second hotspot phone configured as a backup SSID in the firmware (`WiFiMulti` with two networks).
- Avoid eduroam: it needs a real person's USP credentials in the firmware (a privacy and credential-exposure problem), has known PEAP failures, and classroom networks may isolate clients or block ports. Also, the shopper's phone does not need to be on the same network as the tag: it only needs internet (4G or any Wi-Fi) to reach the broker.
- Hardware choice for novices: a classic ESP32 DevKit (the most tutorials) or an ESP32-C3 SuperMini (cheaper, lower power). Either is fine because both are 2.4 GHz. The C5 is unnecessary.

### Gaps
- USP/Poli-specific network policies (client isolation, blocked ports, guest networks) were not researched.
- Battery life of the ESP32 with Wi-Fi + MQTT always connected was not in scope. Another researcher should cover it; Wi-Fi is known to be the dominant power draw.

## Existing maker projects/tutorials to reuse ("scan QR -> web -> MQTT -> ESP32 unlock")

### Takeaway
No single public repo matches the full Tag&Go flow (static HTTPS page + WSS + nonce + ESP32), but the pieces exist and can be combined: the smart-locker ESP32 MQTT unlock code, Random Nerd's PubSubClient template, the EMQX mqtt.js tutorial for the page, and Wokwi HiveMQ examples for testing without hardware.

### Cited Findings
- **MicaellaSalili/smartlocker:** ESP32 + PubSubClient on `test.mosquitto.org:1883`. Per-locker topics `smartlocker/locker/{ID}/unlock|lock|status`, relay on GPIO 26 driving a 12 V solenoid. The flow is: user scans QR, UNLOCK command, then LOCK after verification. No auth. — [smartlocker code](https://github.com/MicaellaSalili/smartlocker/blob/main/ESP32_SmartLocker_Code.ino)
- **fdisotto/esp32-mqtt-example:** controls an ESP32 from a web panel via MQTT. — [GitHub](https://github.com/fdisotto/esp32-mqtt-example)
- **Levantosina/ESP32-MQTT-Servo-Control:** servo via MQTT, tested in the Wokwi simulator. — [GitHub](https://github.com/Levantosina/ESP32-MQTT-Servo-Control)
- **SunFounder ESP32 Starter Kit, Video 30:** servo control with MQTT. — [SunFounder docs](https://docs.sunfounder.com/projects/esp32-starter-kit/en/latest/arduino_video_course/video_30_servo_mqtt.html)
- **Innovate Yourself: "Smart Door Unlock System using ESP32 and MQTT"** (tutorial plus YouTube, with an acknowledgement variant). — [innovationyourself.com](https://www.innovationyourself.com/smart-door-unlock-system/); [YouTube with acknowledgement](https://www.youtube.com/watch?v=5GPObHmhOZk)
- **vogler/SmartLock:** 3D-printed smart lock on ESP32 powered by 2 AA cells, N20 geared motor with a TB6612FNG driver. Relevant for the battery plus 3D-print angle. — [GitHub](https://github.com/vogler/SmartLock)
- **SLMS / SE42_SmartLocker:** locker booking and payment with QR/OTP, ESP32 solenoids over MQTT. — [minhtran324/SE42_SmartLocker](https://github.com/minhtran324/SE42_SmartLocker)
- **EMQX MQTT-Client-Examples:** official example clients in many languages, including JS and ESP32. — [GitHub](https://github.com/emqx/MQTT-Client-Examples)
- **Wokwi HiveMQ Cloud + ESP32 projects:** run the firmware in the browser simulator before the hardware arrives. — [Wokwi project](https://wokwi.com/projects/381829353297474561)

### Inferences
- Suggested reuse: take Random Nerd's PubSubClient skeleton (Wi-Fi + reconnect + callback), borrow the per-ID topic structure from smartlocker, and use the EMQX mqtt.js tutorial for the browser client. Add the nonce/ack logic from the security section.
- Prototype everything in Wokwi first (ESP32 + LED + servo + public broker). The firmware logic can then be shown working before the 3D print and wiring are finished, and it serves as a backup video.

### Gaps
- Could not verify the quality or maintenance status of each repo (commit dates, licences). Check licences before copying code into the report.

## Recommendation: one end-to-end architecture, steps, failure modes and demo fallback

### Takeaway
**Recommended:** a static page on GitHub Pages (HTTPS) using mqtt.js over `wss://` to a free public broker (HiveMQ primary, EMQX backup), and an ESP32 on the presenter's 2.4 GHz phone hotspot using PubSubClient on TCP 1883. Add a per-tag random topic, a retained one-time nonce, an ack back to the page, and a local offline fallback (ESP32 SoftAP page plus a hidden physical override). It is the only option that works on both iPhone and Android with no install, has the fewest parts for novices, is free, and fits the ~R$600 budget with room to spare.

### Cited Findings
- Only WSS works from an HTTPS page, and mqtt.js in the browser supports only ws/wss. — [MQTT.js GitHub](https://github.com/mqttjs/MQTT.js); [Medium: insecure WebSocket error](https://hungchienhsiang.medium.com/securityerror-failed-to-construct-websocket-an-insecure-websocket-connection-may-not-be-f2d1d5289a33)
- HiveMQ public broker WSS 8884 and EMQX public broker WSS 8084 `/mqtt` are available without an account. Neither guarantees uptime. — [mqtt-dashboard.com](https://www.mqtt-dashboard.com/); [EMQX blog](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- Web Bluetooth and Web NFC are unavailable on iOS Safari. — [caniuse Web Bluetooth](https://caniuse.com/web-bluetooth); [caniuse Web NFC](https://caniuse.com/webnfc)
- ESP32/C3 are 2.4 GHz only, and the iPhone hotspot needs "Maximize Compatibility". — [OpenELAB](https://openelab.io/blogs/learn/difference-between-esp32-c3-esp32-c6-and-esp32-c5); [SensorPush](https://support.sensorpush.com/hc/en-us/articles/4404419632023-Why-can-t-I-connect-to-the-Personal-Hotspot-on-my-iPhone)
- The ESP32 captive portal works on tested iPhones and Androids offline, but with caveats (max 4 clients, cellular interference on some phones). — [CDFER/Captive-Portal-ESP32](https://github.com/CDFER/Captive-Portal-ESP32)

### Inferences
**Architecture (text diagram)**
```
[Printed QR on tag] --scan--> https://<user>.github.io/taggo/?t=<TAGID>
   Phone (Safari/Chrome, 4G or any Wi-Fi)
     mqtt.js  --wss://broker.hivemq.com:8884/mqtt-->  [Public broker]  <--tcp 1883--  ESP32 (on presenter hotspot, 2.4 GHz)
     subscribe taggo/<TAGID>/state (retained nonce)                                   publish state/nonce, ack
     publish   taggo/<TAGID>/cmd {"c":"unlock","n":<nonce>}                          subscribe cmd -> LED green -> release
```

**Why this and not the others:** it is the only path meeting "iPhone + Android + no install". The ESP32 side is about 80 lines of well-documented Arduino code with no TLS. The page is a single HTML file. All services are free with no credit card. Unlike the captive portal, the shopper never has to change Wi-Fi.

**Step list for the team**
1. Buy an ESP32 DevKit (or ESP32-C3), an LED (or RGB LED/WS2812), a button, an SG90 micro-servo (if the release is motorized) and a battery (power bank or LiPo + charger module; see the battery research).
2. In Wokwi, build ESP32 + LED + button + servo. Flash a PubSubClient sketch connected to `broker.hivemq.com:1883` and verify it with the web client at mqtt-dashboard.com or MQTTX.
3. Write `index.html`: include mqtt.js pinned to v5 and saved in the repo; parse `?t=`; connect to `wss://broker.hivemq.com:8884/mqtt`; subscribe to state; build the fake payment UI; publish the unlock with the nonce; wait for the ack.
4. Create a public GitHub repo, enable Pages (main/root) and wait up to 10 min. Test on one iPhone and one Android, on both 4G and Wi-Fi.
5. Add the nonce logic and the retained state on the ESP32. Rotate the nonce after re-lock. Add a `WiFiMulti` list of two hotspots and a fallback broker list (HiveMQ, then EMQX).
6. Generate the QR with the tag ID and print it on the tag. Label a second QR "Plano B (offline)" pointing to the ESP32 SoftAP (see below).
7. Rehearse at least 20 end-to-end runs in the classroom or a similar place a few days before 07/12/2026. Record a video of a successful run as the final fallback.

**Failure modes and mitigations**
- Public broker down or slow: page and firmware fall back to the second broker (EMQX `wss://broker.emqx.io:8084/mqtt` / `broker.emqx.io:1883`). Optionally use HiveMQ Cloud free as a private third option.
- ESP32 cannot join the hotspot (5 GHz, typo, iPhone hotspot sleeping): use an Android hotspot or iPhone "Maximize Compatibility" with the screen open, and a second SSID in `WiFiMulti`. Show Wi-Fi/broker status on the LED (e.g. blinking blue = connecting, solid red = locked and online).
- Shopper's phone on a Wi-Fi that blocks port 8884: use 4G. The presenter should do the demo on 4G by default.
- Message lost while the ESP32 is reconnecting: the page waits for the ack and retries. Retained state shows the page whether the tag is online ("Etiqueta offline" warning).
- Someone else on the public broker sends junk to the topic: the random tag ID and one-time nonce make it ignored.
- Battery flat mid-demo: have a charged spare battery or power bank and keep the tag's USB cable at hand.

**Offline fallback for the live demo (defense in depth)**
- Plan B: the ESP32 also runs a SoftAP (`TagGo-Offline`, WPA2 password) serving a copy of the payment page at `http://192.168.4.1`. It is triggered by long-pressing the button, or it is always on in AP+STA mode. The presenter's phone joins it and runs the same flow locally with no internet or broker.
- Plan C: a hidden physical override (e.g. a 5-second press of a combination, or a serial command from a laptop) that runs the green-LED + release sequence. Use it only to show the mechanism if all networking fails, and say so openly.
- Plan D: a pre-recorded video of a successful full run.

### Gaps
- End-to-end latency and success rate over a phone hotspot were not measured by any source; the team must measure them during rehearsal.
- Power consumption of AP+STA mode (for Plan B) versus STA only was not researched.
- Whether iOS Safari keeps the WSS connection alive while the Camera→Safari handoff happens, or when the screen locks mid-payment, was not verified. Mitigation: the page reconnects on `visibilitychange`.
