import pandas as pd
from utils.neutrosophic import compute_neutrosophic_vector
from utils.swara import get_weighted_criteria

def extract_indicators(transactions):
    df = pd.DataFrame(transactions)
    df["value"] = df["value"].astype(float) / 1e18
    df["timeStamp"] = pd.to_datetime(pd.to_numeric(df["timeStamp"]), unit="s")

    total_value = df["value"].sum()
    tx_count = len(df)
    recent_tx_count = len(df[df["timeStamp"] > pd.Timestamp.now() - pd.Timedelta(days=30)])
    unique_counterparties = len(set(df["from"].tolist() + df["to"].tolist()))
    avg_tx_value = df["value"].mean()
    interactions_with_contracts = len(df[df["to"].str.startswith("0x") & df["input"] != "0x"])

    return {
        "total_value_eth": total_value,
        "recent_tx_count": recent_tx_count,
        "tx_count": tx_count,
        "unique_counterparties": unique_counterparties,
        "avg_tx_value": avg_tx_value,
        "interactions_with_contracts": interactions_with_contracts
    }

def compute_fraud_score(indicators, weights):
    # Extract T, I, F from core indicators (you can expand this logic if needed)
    T, I, F = compute_neutrosophic_vector(
        indicators["total_value_eth"],
        indicators["recent_tx_count"],
        indicators["tx_count"]
    )

    weight_dict = dict(weights)
    fraud_score = (
        weight_dict["total_value_eth"] * T +
        weight_dict["recent_tx_count"] * (1 - I) +
        weight_dict["tx_count"] * (1 - F)
    )

    fraud_score = max(0.0, min(1.0, fraud_score))
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
