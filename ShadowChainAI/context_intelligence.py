"""Context intelligence module for Round 1 security simulation."""


def extract_context_features(state):
    """Extract time and location risk contributions from state."""
    login_time = state["login_time"]
    location = state["location"]

    time_risk = 0.0
    if login_time < 6 or login_time > 22:
        time_risk = 0.4
    elif login_time < 9 or login_time > 17:
        time_risk = 0.2

    location_risk = 0.0
    if location not in ["office", "home", "vpn"]:
        location_risk = 0.3

    return {
        "login_time": login_time,
        "location": location,
        "time_risk": time_risk,
        "location_risk": location_risk,
    }
