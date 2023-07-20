from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from Module.CharacterSettingCT import CharacterSettingLangchain_CTransformers
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


async def generate_stream_data():
    for data in CSL.llm_connect():
        yield data


@app.get('/test')
# async def chaintest():
#     return StreamingResponse(generate_stream_data(), media_type='text/event-stream')
async def test1():
    test_var = CSL.llm_connect()
    print(test_var['llm'])
    print(test_var['prompt'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
