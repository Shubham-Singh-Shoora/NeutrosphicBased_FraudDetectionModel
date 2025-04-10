# 🕵️‍♂️ Ethereum Wallet Fraud Score Engine

A modular, research-backed fraud detection engine using **SWARA + Neutrosophic Logic + WSM**, designed for analyzing Ethereum wallet transactions. Built for easy integration with backend APIs.

---

## 📦 Project Structure

```
fraud_detection_model/
│
├── data/
│   └── criteria_config.json       # Criteria definitions + neutrosophic scale
│
├── utils/
│   ├── swara.py                   # SWARA weight calculator
│   ├── neutrosophic.py            # Neutrosophic scoring for T/I/F
│
├── analysis/
│   └── wallet_analyzer.py        # Extracts indicators, computes fraud score
│
├── main.py                       # Example test run using local data
├── sample_wallet_transactions.json # Example input from backend (optional)
├── .gitignore
└── README.md
```

---

## 🚀 How It Works

1. **Backend provides** a list of Ethereum transactions for a given wallet.
2. **SWARA weights** are computed from the criteria config.
3. **T, I, F values** are derived based on wallet behavior.
4. **Fraud score** is computed using a simplified WSM approach.
5. **Result returned** to backend in structured JSON format:

```json
{
  "score": 0.72,
  "label": "⚠️ Suspicious",
  "details": {
    "total_value_eth": 100.25,
    "recent_tx_count": 12,
    ...
  }
}
```

---

## 🧪 Testing It Locally

1. Place example transactions in `sample_wallet_transactions.json`.
2. Run:
```bash
python main.py
```

---

## 🤝 Contributing

1. Clone the repo and create a branch:
```bash
git checkout -b feature/backend-connector
```
2. Make changes, commit and push:
```bash
git commit -m "Add backend integration logic"
git push origin feature/backend-connector
```
3. Open a pull request to `main`.

---

## 📜 License
MIT — use it freely, improve it openly!

---

Made with ❤️ for decentralized security!
