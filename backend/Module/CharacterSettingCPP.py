from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


class CharacterSettingLangchain_LlamaCPP():
    def llm_connect(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        llm = LlamaCpp(model_path="../Models/WizardLM-13B-1.0.ggmlv3.q4_0.bin",
                       callback_manager=callback_manager, verbose=True, temperature=0.95, max_tokens=512, n_ctx=4096, streaming=True)
        return llm

    def prompt_setting(self):
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
        return prompt

    def llm_prompt_chain(self):
        llm = self.llm_connect()
        prompt = self.prompt_setting()
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        return llm_chain

    def run_llm_chain(self):
        text = "You are a talented writer creating a character for a story. Provide detailed information for the following aspects of your character:"
        llm_chain = self.llm_prompt_chain()
        response = llm_chain.run(text)
        return response
