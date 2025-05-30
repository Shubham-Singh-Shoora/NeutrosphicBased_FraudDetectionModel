import os
import json
import pandas as pd
from dotenv import load_dotenv
from analysis.wallet_analyser import extract_indicators, compute_fraud_score
from utils.swara import get_weighted_criteria
from utils.fetcher import fetch_transactions_for_wallet
from utils.neutrosophic import compute_neutrosophic_vector  # Import the function

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

    if not ETHERSCAN_API_KEY:
        raise ValueError("⚠️ Etherscan API Key not found! Please set it in .env file.")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
    OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

    # Show available input files
    print("\nAvailable Wallet CSVs:")
    input_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".csv")]
    for idx, file in enumerate(input_files, 1):
        print(f"{idx}. {file}")

    if not input_files:
        raise ValueError("⚠️ No input CSVs found in data/input/")

    # Ask user to select one
    choice = input("\nEnter the number of the input CSV to process: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(input_files):
        raise ValueError("⚠️ Invalid selection!")

    selected_input = input_files[int(choice) - 1]
    input_path = os.path.join(INPUT_DIR, selected_input)

    # Prepare output path
    output_name = selected_input.replace("wallets", "fraud_scores")
    output_path = os.path.join(OUTPUT_DIR, output_name)

    # Step 1: Read wallets
    wallets_df = pd.read_csv(input_path)
    wallets_list = wallets_df["wallet_address"].dropna().unique().tolist()

   

    results = []
    weights = get_weighted_criteria()
   

    for idx, wallet_address in enumerate(wallets_list, 1):
        print(f"[{idx}/{len(wallets_list)}] Processing wallet: {wallet_address}")

        try:
            transactions = fetch_transactions_for_wallet(wallet_address, ETHERSCAN_API_KEY)

            if not transactions:
                print(f"[⚠️] No transactions found for {wallet_address}. Skipping...")
                continue

            

            # Extract indicators
            indicators = extract_indicators(transactions)

           
            

            # Calculate small transaction count
            small_tx_count = sum(1 for tx in transactions if float(tx["value"]) < 0.001)

            # Compute neutrosophic vector
            T, I, F = compute_neutrosophic_vector(
                indicators["total_value"],
                indicators["recent_tx_count"],
                indicators["tx_count"],
                small_tx_count  # Pass the small_tx_count here
            )

            # Add T, I, F to indicators for fraud score calculation
            indicators["T"] = T
            indicators["I"] = I
            indicators["F"] = F

            

            # Compute fraud score
            fraud_result = compute_fraud_score(indicators, weights)

            results.append({
                "wallet_address": wallet_address,
                "fraud_score": fraud_result["score"],
                "risk_label": fraud_result["label"]
            })

        except Exception as e:
            print(f"[❌] Error processing {wallet_address}: {str(e)}")
            continue

    # Save all results
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)

    print(f"\n[✅] Fraud scores saved to: {output_path}")