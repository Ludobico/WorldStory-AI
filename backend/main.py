from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain

import tracemalloc

# Load env variables from .env file
load_dotenv()

app = FastAPI()

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

tracemalloc.start()


@app.get('/')
async def hello_world():
    return {'message': "hello world"}


@app.get('/qs')
async def qs(question: str):
    template = """Question: {question}

    Answer: Let's work this out in a step by step way to be sure we have the right answer."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
                   callback_manager=callback_manager, verbose=True, streaming=True)
    llm_chain = LLMChain(prompt=prompt, llm=llm,)

    question = "What NFL team won the Super Bowl in the year Justin Bierber was born?"


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000)
