"""
ShadowChainAI - OpenEnv Security Environment
Minimal environment for cybersecurity threat simulation.
"""

import copy

from context_intelligence import extract_context_features
from behavior_analysis import extract_behavior_features
from risk_engine import calculate_risk_score


class SecurityEnv:
    """OpenEnv-style environment for security operations."""

    VALID_ACTIONS = ["allow", "block", "quarantine", "monitor"]

    def __init__(self):
        self.state = {}
        self.done = False
        self.history = []

    def reset(self):
        """Reset environment to initial state."""
        self.done = False
        self.state = {
            "login_time": 9,           # hour of day (0-23)
            "location": "office",      # office | home | vpn | unknown
            "activity": {
                "file_access": 3,      # number of files accessed
                "failed_logins": 0,    # number of failed login attempts
            },
            "risk_score": 0.0,
        }
        return self.state

    def step(self, action):
        """
        Process an action and return (state, reward, done, info).

        Args:
            action: one of 'allow', 'block', 'quarantine', 'monitor'

        Returns:
            tuple: (state, reward, done, info)
        """

        if self.done:
            return self.state, 0.0, True, {}

        if action not in self.VALID_ACTIONS:
            return self.state, -1.0, False, {"error": "invalid_action"}

        # --- Risk Score Calculation ---
        context_features = extract_context_features(self.state)
        behavior_features = extract_behavior_features(self.state)

        risk_score = calculate_risk_score(context_features, behavior_features)
        self.state["risk_score"] = round(risk_score, 2)

        # --- Reward Calculation ---
        if risk_score >= 0.6:
            if action in ["block", "quarantine"]:
                reward = 1.0
            elif action == "monitor":
                reward = 0.3
            else:
                reward = -1.0

        elif risk_score >= 0.3:
            if action == "monitor":
                reward = 1.0
            elif action in ["block", "quarantine"]:
                reward = 0.5
            else:
                reward = -0.5

        else:
            if action == "allow":
                reward = 1.0
            elif action == "monitor":
                reward = 0.5
            else:
                reward = -0.5

        # Episode ends after one decision
        self.done = True

        # --- Logging ---
        self.history.append({
            "state": copy.deepcopy(self.state),
            "action": action,
            "reward": reward,
        })

        return self.state, reward, self.done, {}


# --- Quick Test ---
if __name__ == "__main__":
    env = SecurityEnv()

    # Scenario 1: Normal office login
    state = env.reset()
    print("=== Scenario 1: Normal Office Login ===")
    print(f"State: {state}")
    state, reward, done, _ = env.step("allow")
    print(f"Action: allow | Risk: {state['risk_score']} | Reward: {reward}\n")

    # Scenario 2: Suspicious activity
    state = env.reset()
    state["login_time"] = 2
    state["location"] = "unknown"
    state["activity"]["failed_logins"] = 5
    state["activity"]["file_access"] = 15
    print("=== Scenario 2: Suspicious Activity ===")
    print(f"State: {state}")
    state, reward, done, _ = env.step("block")
    print(f"Action: block | Risk: {state['risk_score']} | Reward: {reward}\n")

    # Scenario 3: Wrong decision
    state = env.reset()
    state["login_time"] = 3
    state["location"] = "unknown"
    state["activity"]["failed_logins"] = 4
    print("=== Scenario 3: Bad Decision ===")
    print(f"State: {state}")
    state, reward, done, _ = env.step("allow")
    print(f"Action: allow | Risk: {state['risk_score']} | Reward: {reward}")