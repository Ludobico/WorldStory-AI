from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import os
from Module.CharacterSettingCT import CharacterSettingLangchain_CTransformers
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()
CSL = CharacterSettingLangchain_CTransformers()


@app.get('/')
async def test():
    return {'message': "hello world"}


@app.get('/test')
async def chaintest():
    model_path = os.path.join(
        '.', 'Models', 'WizardLM-13B-1.0.ggmlv3.q4_0.bin')
    return StreamingResponse(CSL.llm_connect(model_dir=model_path), media_type='text/event-stream')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
