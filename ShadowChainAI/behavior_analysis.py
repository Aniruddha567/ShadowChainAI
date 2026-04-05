"""Behavior analysis module for Round 1 security simulation."""


def extract_behavior_features(state):
    """Extract behavior risk contributions from user activity."""
    file_access = state["activity"]["file_access"]
    failed_logins = state["activity"]["failed_logins"]

    failed_login_risk = 0.0
    if failed_logins >= 3:
        failed_login_risk = 0.3
    elif failed_logins >= 1:
        failed_login_risk = 0.1

    file_access_risk = 0.0
    if file_access > 10:
        file_access_risk = 0.2

    return {
        "file_access": file_access,
        "failed_logins": failed_logins,
        "failed_login_risk": failed_login_risk,
        "file_access_risk": file_access_risk,
    }
