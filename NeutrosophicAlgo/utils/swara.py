import json

def load_criteria(path="data/criteria_config.json"):
    with open(path, "r") as f:
        return json.load(f)

def swara_weights(linguistic_scores, neutrosophic_scale):
    """
    Given a list of linguistic scores (ordered by importance),
    compute SWARA-based weights using the truth-membership value.
    """
    k = [1.0]
    for score in linguistic_scores[1:]:
        t_value = neutrosophic_scale[score][0]
        k_j = t_value + 1e-9
        k.append(k_j)

    q = [1.0]
    for j in range(1, len(k)):
        q.append(q[j-1] / k[j])

    total = sum(q)
    weights = [q_j / total for q_j in q]
    return weights

def get_weighted_criteria():
    config = load_criteria()
    criteria = config["criteria"]
    scale = config["neutrosophic_scale"]

    # Sort by importance (assumes they're already ordered in the JSON)
    linguistic_scores = [c["importance"] for c in criteria]
    weights = swara_weights(linguistic_scores, scale)

    return [(c["name"], w) for c, w in zip(criteria, weights)]

if __name__ == "__main__":
    print("[SWARA] Weights:")
    for name, weight in get_weighted_criteria():
        print(f"  {name}: {weight:.4f}")
