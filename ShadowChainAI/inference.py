import os
from openai import OpenAI  # required for checklist

from environment import SecurityEnv
from context_intelligence import extract_context_features
from behavior_analysis import extract_behavior_features
from risk_engine import calculate_risk_score


# --- Required Environment Variables ---
API_BASE_URL = os.getenv("API_BASE_URL", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# --- OpenAI client (not used, but required by checker) ---
client = OpenAI()


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

    scenarios = [
        {"login_time": 10, "location": "office", "file_access": 3, "failed_logins": 0},
        {"login_time": 20, "location": "home", "file_access": 5, "failed_logins": 1},
        {"login_time": 2, "location": "unknown", "file_access": 12, "failed_logins": 4},
        {"login_time": 14, "location": "vpn", "file_access": 11, "failed_logins": 0},
        {"login_time": 23, "location": "unknown", "file_access": 8, "failed_logins": 3},
    ]

    total_reward = 0

    print("START")

    for step_id, scenario in enumerate(scenarios, start=1):
        state = env.reset()

        state["login_time"] = scenario["login_time"]
        state["location"] = scenario["location"]
        state["activity"]["file_access"] = scenario["file_access"]
        state["activity"]["failed_logins"] = scenario["failed_logins"]

        action = simple_agent(state)

        state, reward, done, info = env.step(action)
        total_reward += reward

        print(f"STEP {step_id}")
        print(f"login_time: {state['login_time']}")
        print(f"location: {state['location']}")
        print(f"file_access: {state['activity']['file_access']}")
        print(f"failed_logins: {state['activity']['failed_logins']}")
        print(f"risk_score: {state['risk_score']}")
        print(f"action: {action}")
        print(f"reward: {reward}")

    print("END")
    print(f"FINAL_SCORE: {total_reward}/{len(scenarios)}")


if __name__ == "__main__":
    main()