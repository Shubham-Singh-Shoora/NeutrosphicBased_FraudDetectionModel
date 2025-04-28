import pandas as pd
from utils.neutrosophic import compute_neutrosophic_vector
from utils.swara import get_weighted_criteria
from datetime import datetime, timedelta

def extract_indicators(transactions):
    """
    Extract fraud indicators from transaction data.
    :param transactions: List of transaction dictionaries.
    :return: Dictionary of indicators.
    """
    if not transactions:
        raise ValueError("No transactions provided.")

    # Convert transactions to a DataFrame
    df = pd.DataFrame(transactions)


    # Ensure 'value' exists and is numeric
    if "value" not in df.columns:
        raise KeyError("'value' field is missing in transaction data.")
    try:
        df["value"] = df["value"].astype(float) / 1e18  # Convert from Wei to ETH
    except ValueError as e:
        raise ValueError(f"Error converting 'value' to float: {e}")

    # Ensure 'timeStamp' exists and is a datetime object
    if "timeStamp" not in df.columns:
        raise KeyError("'timeStamp' field is missing in transaction data.")
    try:
        df["timeStamp"] = pd.to_datetime(pd.to_numeric(df["timeStamp"]), unit="s")
    except Exception as e:
        raise ValueError(f"Error converting 'timeStamp' to datetime: {e}")

    # Calculate indicators
    total_value = float(df["value"].sum())  # Convert to standard float
    tx_count = int(len(df))  # Convert to standard int
    recent_tx_count = int(len(df[df["timeStamp"] > pd.Timestamp.now() - pd.Timedelta(days=30)]))  # Convert to int
    unique_counterparties = int(len(set(df["from"].tolist() + df["to"].tolist())))  # Convert to int
    avg_tx_value = float(df["value"].mean()) if not df["value"].empty else 0.0  # Convert to float
    interactions_with_contracts = int(len(df[df["to"].str.startswith("0x") & df["input"] != "0x"]))  # Convert to int
    small_tx_count = int(len(df[df["value"] < 0.001]))  # Calculate small transaction count

    indicators = {
        "total_value": total_value,
        "recent_tx_count": recent_tx_count,
        "tx_count": tx_count,
        "unique_counterparties": unique_counterparties,
        "avg_tx_value": avg_tx_value,
        "interactions_with_contracts": interactions_with_contracts,
        "small_tx_count": small_tx_count  # Add small_tx_count to indicators
    }


    return indicators

def compute_fraud_score(indicators, weights):
    """
    Compute the fraud score based on indicators and SWARA weights.
    :param indicators: Dictionary of fraud indicators.
    :param weights: List of SWARA weights.
    :return: Dictionary containing the fraud score and risk label.
    """

    # Extract T, I, F from core indicators
    T, I, F = compute_neutrosophic_vector(
        indicators["total_value"],
        indicators["recent_tx_count"],
        indicators["tx_count"],
        indicators["small_tx_count"]  # Pass small_tx_count here
    )


    weight_dict = dict(weights)
    fraud_score = (
        weight_dict["total_value"] * (1-T) +
        weight_dict["recent_tx_count"] *  (I * 2) +
        weight_dict["tx_count"] *  (F * 2)
    )
    
    
    fraud_score = max(0.0, min(1.0, fraud_score))  # Clamp to [0, 1]
    if fraud_score > 0.7:
        label = "🚨 High Risk"
    elif fraud_score > 0.4:
        label = "⚠️ Suspicious"
    else:
        label = "✅ Safe"

    return {
        "score": round(fraud_score, 4),
        "label": label,
        "details": indicators
    }