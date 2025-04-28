import os
import json
import pandas as pd
from dotenv import load_dotenv
from utils.fetcher import fetch_transactions_for_wallet

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(BASE_DIR, "data", "input")

    # Ask user for the wallet address
    wallet_address = input("Enter wallet address to extract 'to' fields: ").strip()

    if not wallet_address:
        raise ValueError("⚠️ Wallet address is required!")

    # Fetch transactions
    transactions = fetch_transactions_for_wallet(wallet_address, ETHERSCAN_API_KEY)

    if not transactions:
        raise ValueError(f"⚠️ No transactions found for {wallet_address}!")

    # Extract unique "to" addresses
    to_addresses = {tx.get('to') for tx in transactions if tx.get('to')}
    to_addresses = list(to_addresses)

    print(f"\n[INFO] Extracted {len(to_addresses)} unique 'to' addresses.")

    # Auto-generate output filename
    prefix = wallet_address[:6] + "..." + wallet_address[-4:]
    output_name = f"wallets_{prefix}.csv"
    output_path = os.path.join(INPUT_DIR, output_name)

    # Save to CSV
    os.makedirs(INPUT_DIR, exist_ok=True)
    df = pd.DataFrame(to_addresses, columns=["wallet_address"])
    df.to_csv(output_path, index=False)

    print(f"\n[✅] Wallets saved to: {output_path}")
