import requests

def fetch_transactions_for_wallet(wallet_address, api_key):
    """Fetch all normal transactions for a given wallet using Etherscan API."""
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch transactions: {response.text}")
    
    result = response.json()
    if result["status"] != "1":
        raise Exception(f"Etherscan API Error: {result.get('message', 'Unknown error')}")
    
    return result["result"]
