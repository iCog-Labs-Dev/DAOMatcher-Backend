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
        print(
            f"Token: {len(self.prompt.format_prompt(query=query, content=content).text) / 4}"
        )
        response = self.chain.run({"query": query, "content": content})
        print("\033[94m" + response + "\033[0m")
        response = self.extract_response(response)
        # print(f"Prompt: {prompt.template}")  # For debugging only

        return response

    def clean_content(self, input_string):
        # Define a regular expression pattern to match alphanumeric and special characters
        pattern = re.compile("[\w\s!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~]+")

        # Use the pattern to filter out unwanted characters
        filtered_string = "".join(pattern.findall(input_string))
        filtered_string = filtered_string.replace("\n\n", "")
        filtered_string = filtered_string.replace("  ", " ")
        filtered_string = filtered_string.replace("\n", "")
        filtered_string = filtered_string.replace("------------------", "")

        return filtered_string

    def extract_response(self, response):
        try:
            print("\033[94m" + response + "\033[0m")
            if "Response:" in response:
                response = response.split("Response:")[1]
            elif "Observation:" in response:
                response = response.split("Observation:")[1]
            response = response.split("\n")[0].strip()
            response = "".join(char for char in response if char.isdigit())

            if not all(char.isdigit() for char in response):
                return ""
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
            return ""
