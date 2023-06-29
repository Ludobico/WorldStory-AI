from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from Module.CharacterSettingCT import CharacterSettingLangchain_CTransformers
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()
CSL = CharacterSettingLangchain_CTransformers()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def test():
    return {'message': "hello world"}


@app.get('/test')
async def chaintest():
    model_path = os.path.join(
        '.', 'Models', 'WizardLM-13B-1.0.ggmlv3.q4_0.bin')
    return StreamingResponse(CSL.llm_connect(), media_type='text/event-stream')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
