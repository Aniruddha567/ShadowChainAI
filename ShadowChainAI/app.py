import gradio as gr
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel

from environment import SecurityEnv

# -------- INIT --------
env = SecurityEnv()
app = FastAPI()

# -------- MODELS --------
class ActionRequest(BaseModel):
    action: str

# -------- API --------
@app.post("/reset")
async def reset():
    state = env.reset()
    return {"state": state}

@app.post("/step")
async def step(req: ActionRequest):
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

# -------- MOUNT UI --------
app = gr.mount_gradio_app(app, demo, path="/")