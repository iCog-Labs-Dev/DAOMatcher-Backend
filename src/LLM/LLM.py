import re
from src.LLM.TogetherLLM import TogetherLLM
from src.LLM.Prompt import *
from langchain import LLMChain
from src.LLM import model


class LLM:
    def __init__(self, temperature=0.1, max_tokens=512):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt = Prompt().get_prompt_template()
        self.chain = LLMChain(prompt=self.prompt, llm=self.model, verbose=True)

    def generate(self, query, content):
        content = self.clean_content(content)
        response = self.chain.run({"query": query, "content": content})
        print("\033[94m" + response + "\033[0m")
        response = response.split("Response:")[1]
        response = response.split("\n")[0].strip()
        response = "".join(char for char in response if char.isdigit())
        if not all(char.isdigit() for char in response):
            return "0"
        # print(f"Prompt: {prompt.template}")  # For debugging only

        return response

    def clean_content(self, input_string):
        # Define a regular expression pattern to match alphanumeric and special characters
        pattern = re.compile("[\w\s!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~]+")

        # Use the pattern to filter out unwanted characters
        filtered_string = "".join(pattern.findall(input_string))
        filtered_string = filtered_string.replace("\n\n", "")
        filtered_string = filtered_string.replace("\n", "")

        return filtered_string
