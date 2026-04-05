from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

from environment import SecurityEnv

app = FastAPI()
env = SecurityEnv()

# -------- MODEL --------
class ActionRequest(BaseModel):
    action: str

# -------- RESET --------
@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}

# -------- STEP --------
@app.post("/step")
def step(req: ActionRequest):
    state, reward, done, info = env.step(req.action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

# -------- ROOT (OPTIONAL) --------
@app.get("/")
def root():
    return {"message": "ShadowChain AI Environment Running"}

# -------- OPTIONAL DEBUG --------
@app.get("/run")
def run_env():
    result = subprocess.run(
        ["python", "inference.py"],
        capture_output=True,
        text=True
    )
    return {"output": result.stdout}