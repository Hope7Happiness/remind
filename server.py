from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

from sound_backend import run as play_sound
from speech_backend import run as speak_text

app = FastAPI()

@app.get('/g/{data}')
async def pure_remind(data: str):
    play_sound()
    speak_text(data)

class Task(BaseModel):
    name: str

@app.post("/post")
async def post_based_remind(item: Task):
    raise NotImplementedError
    # return f'Task {item.name} has finished'

def run_server():
    uvicorn.run(app, host='0.0.0.0', port=54225, workers=1)

def kill_server():
    os.system('lsof -t -i:54225 | xargs kill -9')

if __name__ == '__main__':
    run_server()