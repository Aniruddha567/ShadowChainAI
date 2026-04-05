import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

from environment import SecurityEnv

# -------- INIT --------
env = SecurityEnv()
app = FastAPI()

# -------- API MODELS --------
class ActionRequest(BaseModel):
    action: str

# -------- API ENDPOINTS --------
@app.post("/reset")
def reset():
    state = env.reset()
    return {"state": state}

@app.post("/step")
def step(req: ActionRequest):
    state, reward, done, info = env.step(req.action)
    return {
        "state": state,
        "reward": reward,
        "done": done,
        "info": info
    }

# -------- GRADIO FUNCTION --------
def run_env():
    result = subprocess.run(
        ["python", "inference.py"],
        capture_output=True,
        text=True
    )
    return result.stdout

# -------- GRADIO UI --------
demo = gr.Interface(
    fn=run_env,
    inputs=[],
    outputs="text",
    title="ShadowChain AI Environment",
    description="Runs insider threat simulation and exposes OpenEnv API."
)

# -------- RUN BOTH --------
@app.get("/")
def root():
    return {"message": "ShadowChain AI API running"}

# Launch Gradio separately
if __name__ == "__main__":
    demo.launch()