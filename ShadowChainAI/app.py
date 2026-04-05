import gradio as gr
import subprocess


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
    description="Runs insider threat simulation and shows results."
)

demo.launch()