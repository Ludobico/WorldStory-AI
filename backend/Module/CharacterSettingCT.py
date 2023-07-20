from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from ctransformers.langchain import CTransformers
from langchain.llms import LlamaCpp
from sse_starlette.sse import EventSourceResponse


class CharacterSettingLangchain_CTransformers:
    def llm_connect(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = LlamaCpp(model_path='./Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin',
                       callback_manager=callback_manager, verbose=True, temperature=0.95, max_tokens=512, n_ctx=4096, streaming=True)

        template = """
{instruct}

Character Name:
Gender:
Age:
Personality:
Background:
Dialogue Style:
Appearance:

Ensure your responses are consistent with the world and setting of your story. Be creative and feel free to include any relevant details that will help the model generate a rich and unique character description. Provide as much information as possible to make the character come to life within the story you have in mind.
create a character for a story set in various settings such as historical, futuristic, fantasy,modern or science fiction.
Let's think step by step.

Provide a JSON-formatted response with information about a person. Include the following fields: Character Name, Gender, Age, Personality, Background, Dialogue Style and Appearance. Do not create any keys except for the 7 keys above

writer : 

"""
        prompt = PromptTemplate(
            template=template, input_variables=["instruct"])
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        text = "You are a talented writer creating a character for a story. Provide detailed information for the following aspects of your character:"
        return llm_chain, text


if __name__ == "__main__":
    CSL = CharacterSettingLangchain_CTransformers()
    CSL.llm_connect()
