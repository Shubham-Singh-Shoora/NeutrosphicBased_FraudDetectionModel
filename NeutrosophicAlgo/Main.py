import json
from analysis.wallet_analyzer import extract_indicators, compute_fraud_score
from utils.swara import get_weighted_criteria

# Simulated backend input (replace with actual backend request body)
with open("sample_wallet_transactions.json", "r") as f:
    tx_data = json.load(f)

print("[INFO] Transactions received from backend:", len(tx_data))

indicators = extract_indicators(tx_data)
weights = get_weighted_criteria()
result = compute_fraud_score(indicators, weights)

print("\n[RESULT] Fraud Analysis Result:")
print(json.dumps(result, indent=2))
