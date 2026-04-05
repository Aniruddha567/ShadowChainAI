import subprocess

def run_env():
    result = subprocess.run(["python", "inference.py"], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    print(run_env())