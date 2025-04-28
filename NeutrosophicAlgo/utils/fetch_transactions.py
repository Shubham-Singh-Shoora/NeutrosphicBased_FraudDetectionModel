import os
import json
import pandas as pd
import time
import requests
from dotenv import load_dotenv

load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY") 
API_SLEEP_TIME = 0.25  # 🔥 Sleep 0.25 seconds between API calls (4 calls/sec max)

def fetch_wallet_transactions(wallet_address):
    base_url = "https://api.etherscan.io/api"
    start_block = 0
    end_block = 99999999
    sort = "asc"
    page = 1
    offset = 1000  
    all_transactions = []

    while True:
        params = {
            "module": "account",
            "action": "txlist",
            "address": wallet_address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": ETHERSCAN_API_KEY
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()

            if data["status"] != "1":
                print(f"[WARNING] {wallet_address}: {data.get('message', 'Unknown error')}")
                break  # If no more data or error, exit loop

            txs = data["result"]

            if not txs:
                break  # No more transactions

            all_transactions.extend(txs)

            if len(txs) < offset:
                break  # Fetched last page

            page += 1
            time.sleep(API_SLEEP_TIME)

        except Exception as e:
            print(f"[ERROR] Exception fetching {wallet_address} page {page}: {e}")
            time.sleep(5)  # Wait a bit longer and try again
            continue

    return all_transactions

def main():
    input_file = "NeutrosophicAlgo/data/input/wallets.csv"
    output_dir = "NeutrosophicAlgo/data/transactions/"
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_file)

    for idx, row in df.iterrows():
        wallet = row['wallet_address']
        print(f"[INFO] Fetching transactions for {wallet}")

        try:
            transactions = fetch_wallet_transactions(wallet)
            if transactions:
                with open(os.path.join(output_dir, f"{wallet}.json"), "w") as f:
                    json.dump(transactions, f, indent=2)
                print(f"[✅] Saved {len(transactions)} transactions for {wallet}")
            else:
                print(f"[⚠️] No transactions found for {wallet}")

        except Exception as e:
            with open("NeutrosophicAlgo/logs/process_log.txt", "a") as log_file:
                log_file.write(f"Failed to fetch for {wallet}: {str(e)}\n")
            print(f"[ERROR] Failed fetching {wallet}: {e}")

if __name__ == "__main__":
    main()
