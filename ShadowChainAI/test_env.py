from environment import SecurityEnv


def run_scenario(env, title, setup_fn, action):
    state = env.reset()
    setup_fn(state)
    state, reward, done, info = env.step(action)
    print(f"=== {title} ===")
    print(f"state: {state}")
    print(f"risk_score: {state['risk_score']}")
    print(f"action: {action}")
    print(f"reward: {reward}\n")


def main():
    env = SecurityEnv()

    run_scenario(
        env,
        "Scenario 1: Normal Login",
        lambda s: None,
        "allow",
    )

    run_scenario(
        env,
        "Scenario 2: Suspicious Activity",
        lambda s: (
            s.update({"login_time": 2, "location": "unknown"}),
            s["activity"].update({"failed_logins": 5, "file_access": 15}),
        ),
        "block",
    )

    run_scenario(
        env,
        "Scenario 3: Wrong Decision Case",
        lambda s: (
            s.update({"login_time": 3, "location": "unknown"}),
            s["activity"].update({"failed_logins": 4}),
        ),
        "allow",
    )


if __name__ == "__main__":
    main()
