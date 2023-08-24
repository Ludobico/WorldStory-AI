from langchain import ConversationChain
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.llms import LlamaCpp


def get_chain(stream_handler, tracing: bool = False) -> ConversationChain:
    """Create a ConversationChain for question/answering."""

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "Let's work this out in a step by step way to be sure we have the right answer."
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    manager = AsyncCallbackManager([])
    stream_manager = AsyncCallbackManager([stream_handler])
    if tracing:
        tracer = LangChainTracer()
        tracer.load_default_session()
        manager.add_handler(tracer)
        stream_manager.add_handler(tracer)

    streaming_llm = LlamaCpp(model_path="./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
                             callback_manager=stream_manager, verbose=True, streaming=True, max_tokens=25)

    memory = ConversationBufferMemory(return_messages=True)

    qa = ConversationChain(
        callback_manager=manager, memory=memory, llm=streaming_llm, verbose=True, prompt=prompt
    )

    return qa
