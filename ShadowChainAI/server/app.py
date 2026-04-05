from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from environment import SecurityEnv

app = FastAPI()
env = SecurityEnv()


class ActionRequest(BaseModel):
    action: str


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


@app.get("/")
def root():
    return {"message": "ShadowChain AI Running"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()