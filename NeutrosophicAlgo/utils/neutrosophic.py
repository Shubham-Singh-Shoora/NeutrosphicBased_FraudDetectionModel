# Neutrosophic scoring functions for fraud analysis
def compute_truth(total_value):
    # Normalize total value (ETH) as a proxy for risk
    return min(1.0, total_value / 1000)

def compute_indeterminacy(recent_tx_count):
    return 0.3 if recent_tx_count > 10 else 0.1

def compute_falsity(tx_count):
    return 0.1 if tx_count > 50 else 0.6

def compute_neutrosophic_vector(total_value, recent_tx_count, tx_count):
    T = compute_truth(total_value)
    I = compute_indeterminacy(recent_tx_count)
    F = compute_falsity(tx_count)
    return T, I, F
