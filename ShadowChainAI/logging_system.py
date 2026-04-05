"""Basic logging module for Round 1 security simulation."""

import copy


class BasicLogger:
    """In-memory logger for scenario, action, and rewards."""

    def __init__(self):
        self.records = []

    def log_episode(self, state, risk_score, action, reward):
        self.records.append(
            {
                "state": copy.deepcopy(state),
                "risk_score": risk_score,
                "action": action,
                "reward": reward,
            }
        )

    def get_logs(self):
        return self.records