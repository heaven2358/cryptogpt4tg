# 🤖 CryptoGPT Telegram Bot


A context-aware Telegram bot that provides real-time cryptocurrency price information, purchase options, and conversational assistance. Powered by APRO AI Oracle on ATTPs protocol.

![CryptoGPT Architecture](https://github.com/heaven2358/cryptogpt4tg/raw/main/docs/architecture.png)

## 🌟 Vision

We believe the future of crypto trading won't happen on complex exchange dashboards—it will happen in chat conversations.

Wherever you are—Telegram, Discord, Twitter (X), Instagram, or even livestreams and podcasts—just say a sentence, and your AI crypto assistant will understand your intent, fetch verifiable on-chain data, recommend optimal trading paths, and eventually complete entire transactions.

We're not just building a bot, but an intelligent agent embedded in any conversational environment, connecting all Web3 scenarios and becoming the most natural gateway between users and the on-chain world.

## 🚀 Features

- 🧠 OpenAI GPT-4-powered natural language understanding
- 🔗 Verifiable crypto price queries via [APRO AI Oracle](https://apro.com)
  - Real-time median prices from multiple sources
  - Signed and timestamped for verification
- 💱 Smart fiat-to-crypto recommendations with optimal paths
  - MoonPay direct purchase options
  - 1inch/PancakeSwap swap routes
  - Binance direct fiat purchase (lowest friction)
- 💬 Multi-turn context memory per user
- 🌍 Multi-language support (Chinese 🇨🇳 / English 🇺🇸 auto-detect)
- 🛡️ Sensitive content detection (wallets, seed phrases, card numbers)
- 🧩 Dual-mode runtime: Telegram chat or console input
- 🔧 Daemonized background execution with signal-based control

## 🔮 Future Roadmap

- One-click in-chat transaction execution (no platform switching)
- Universal crypto agent across all social platforms
- Cross-chain support and portfolio tracking
- Web dashboard + on-chain identity
- Multi-signature guardrails for enhanced security

## 📦 Installation

```bash
git clone https://github.com/heaven2358/cryptogpt4tg.git
cd cryptogpt4tg
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Configuration
```bash
cp .env.example .env
```

### Edit .env and fill in:
```
BEARER_TOKEN=""
OPENAI_API_KEY=""
CONSUMER_KEY=""
CONSUMER_SECRET=""
TELEGRAM_BOT_TOKEN=""
```

## 🧪 Usage
### Show help
```bash
python main.py -h
```

### Run in Console Test Mode
```bash
python main.py -i
```

### Start Telegram Bot in Foreground
```bash
python main.py -t
```
### Start as Daemon (Telegram Mode)
```bash
python main.py -d -t
```

## 🧯 Daemon Control
### Restart daemon
```bash
kill -HUP {pid}
```

## 📄 Testing
```bash
python -m unittest discover tests
```

## 🔒 Security & Trust

- ✅ End-to-end encryption
- ✅ Oracle signature verification
- ✅ Zero-trust message routing
- ✅ Transaction proof receipts

## 🧠 Technical Stack

- APRO AI Oracle (verifiable data)
- ATTPs Protocol (data integrity, proof)
- Smart Routing Engine (fee optimization)
- Telegram Bot API (user interface)
- Fiat onramps (MoonPay, Binance)
- DEX Aggregators (1inch, PancakeSwap)

## 🚀 Try It Now

- Telegram: [@cryptobladegptbot](https://t.me/cryptobladegptbot)
- Web Demo: [https://cryptogpt-test.apro.com](https://cryptogpt-test.apro.com)

## 👥 Team

- Xie Min - Blockchain + ATTPs Protocol
- Jade - AI/NLP Engineering
- Leo - Telegram Bot & Integration

---

Built with ❤️ at YZI Labs x AGI House Hackathon