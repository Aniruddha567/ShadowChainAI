import gradio as gr
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

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

# -------- GRADIO --------
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
    description="Runs insider threat simulation and exposes API."
)

# -------- MAIN --------
if __name__ == "__main__":
    import threading

    # Run FastAPI in background
    def run_api():
        uvicorn.run(app, host="0.0.0.0", port=7861)

    threading.Thread(target=run_api).start()

    # Run Gradio UI
    demo.launch(server_name="0.0.0.0", server_port=7860)