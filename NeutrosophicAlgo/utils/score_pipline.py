# utils/scoring_pipeline.py
import os
import json
import pandas as pd
from analysis.wallet_analyser import extract_indicators, compute_fraud_score
from utils.swara import get_weighted_criteria

def main():
    transaction_dir = "NeutrosophicAlgo/data/transactions/"
    score_output_file = "NeutrosophicAlgo/data/scores/fraud_scores.csv"

    wallet_scores = []

    weights = get_weighted_criteria()

    for filename in os.listdir(transaction_dir):
        if filename.endswith(".json"):
            wallet_address = filename.replace(".json", "")
            print(f"[INFO] Scoring wallet {wallet_address}")

            try:
                with open(os.path.join(transaction_dir, filename), "r") as f:
                    transactions = json.load(f)

                indicators = extract_indicators(transactions)
                result = compute_fraud_score(indicators, weights)

                wallet_scores.append({
                    "wallet_address": wallet_address,
                    "fraud_score": result["score"],
                    "risk_label": result["label"]
                })

            except Exception as e:
                with open("NeutrosophicAlgo/logs/process_log.txt", "a") as log_file:
                    log_file.write(f"Failed to score {wallet_address}: {str(e)}\n")
                print(f"[ERROR] Failed scoring {wallet_address}: {e}")

    df = pd.DataFrame(wallet_scores)
    df.to_csv(score_output_file, index=False)
    print(f"\n✅ Fraud scores saved to {score_output_file}")

if __name__ == "__main__":
    main()
