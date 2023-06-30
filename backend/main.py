from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from Module.CharacterSettingCT import CharacterSettingLangchain_CTransformers
import uvicorn
from fastapi_async_langchain.responses import StreamingResponse

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


async def generate_stream_data():
    for data in CSL.llm_connect():
        yield data


@app.get('/test')
async def chaintest():
    return StreamingResponse(CSL.llm_connect(), media_type='text/event-stream')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
