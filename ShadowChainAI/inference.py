from environment import SecurityEnv
from logging_system import BasicLogger
from context_intelligence import extract_context_features
from behavior_analysis import extract_behavior_features
from risk_engine import calculate_risk_score


def simple_agent(state):
    context = extract_context_features(state)
    behavior = extract_behavior_features(state)
    risk = calculate_risk_score(context, behavior)

    if risk >= 0.6:
        return "block"
    elif risk >= 0.3:
        return "monitor"
    else:
        return "allow"
def main():
    env = SecurityEnv()
    logger = BasicLogger()

    scenarios = [
        {"login_time": 10, "location": "office", "file_access": 3, "failed_logins": 0},
        {"login_time": 20, "location": "home", "file_access": 5, "failed_logins": 1},
        {"login_time": 2, "location": "unknown", "file_access": 12, "failed_logins": 4},
        {"login_time": 14, "location": "vpn", "file_access": 11, "failed_logins": 0},
        {"login_time": 23, "location": "unknown", "file_access": 8, "failed_logins": 3},
    ]

    for episode, scenario in enumerate(scenarios, start=1):
        state = env.reset()

        # Apply scenario
        state["login_time"] = scenario["login_time"]
        state["location"] = scenario["location"]
        state["activity"]["file_access"] = scenario["file_access"]
        state["activity"]["failed_logins"] = scenario["failed_logins"]

        # Agent decides (IMPORTANT)
        action = simple_agent(state)

        # Environment evaluates
        state, reward, done, info = env.step(action)

        # Logging
        logger.log_episode(state, state["risk_score"], action, reward)
        print(f"=== Episode {episode} ===")
        print(f"state: {state}")
        print(f"risk_score: {state['risk_score']}")
        print(f"chosen action: {action}")
        print(f"reward: {reward}\n")


if __name__ == "__main__":
    main()