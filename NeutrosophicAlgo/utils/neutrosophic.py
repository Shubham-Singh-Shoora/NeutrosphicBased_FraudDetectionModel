# Neutrosophic scoring functions for fraud analysis
def compute_truth(total_value, small_tx_count):
    """
    Normalize total value (ETH) as a proxy for risk.
    Adjust for small transaction counts (address poisoning).
    """
    
    return max(0.0, 1.0 - (small_tx_count / (total_value + 1)))

def compute_indeterminacy(recent_tx_count):
    return 0.9 if recent_tx_count < 5 else 0.3 if recent_tx_count < 10 else 0.1


def compute_falsity(tx_count):
    return min(1.0, tx_count / 500)  # Scale falsity based on tx_count

def compute_neutrosophic_vector(total_value, recent_tx_count, tx_count, small_tx_count):
    """
    Compute the neutrosophic vector (T, I, F) for fraud analysis.
    """
    
    T = compute_truth(total_value, small_tx_count)
    I = compute_indeterminacy(recent_tx_count)
    F = compute_falsity(tx_count)
    return T, I, F