"""Risk engine module for Round 1 security simulation."""


def calculate_risk_score(context_features, behavior_features):
    """Combine context and behavior risk contributions into a single score."""
    risk_score = (
        context_features["time_risk"]
        + context_features["location_risk"]
        + behavior_features["failed_login_risk"]
        + behavior_features["file_access_risk"]
    )

    return min(risk_score, 1.0)
