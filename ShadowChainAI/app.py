import gradio as gr
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel

from environment import SecurityEnv

# Create FastAPI app
app = FastAPI()
env = SecurityEnv()

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

# -------- GRADIO UI --------
def run_env():
    result = subprocess.run(
        ["python", "inference.py"],
        capture_output=True,
        text=True
    )
    return result.stdout

demo = gr.Interface(
    fn=run_env,
    inputs=[],
    outputs="text",
    title="ShadowChain AI Environment",
    description="Runs insider threat simulation and exposes OpenEnv API."
)

# Mount Gradio inside FastAPI
app = gr.mount_gradio_app(app, demo, path="/")