from src.LLM.TogetherLLM import TogetherLLM
from src.LLM.Prompt import *
from langchain import LLMChain


class LLM:
    def __init__(self, temperature=0.1, max_tokens=512):
        self.model = TogetherLLM()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt = Prompt().get_prompt_template()
        self.chain = LLMChain(prompt=self.prompt, llm=self.model, verbose=True)

    def generate(self, query, content):
        response = self.chain.run({"query": query, "content": content})
        print("\033[94m" + response + "\033[0m")
        response = response.split("Response:")[1]
        response = response.split("\n")[0].strip()
        response = "".join(char for char in response if char.isdigit())
        if not all(char.isdigit() for char in response):
            return "0"
        # print(f"Prompt: {prompt.template}")  # For debugging only

        return response
