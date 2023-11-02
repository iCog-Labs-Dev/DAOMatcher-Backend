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
        self.chain = LLMChain(prompt=self.prompt, llm=self.model)

    def generate(self, query, content):
        content = self.clean_content(content)
        print(
            "\033[94;1m{:<12} {:10}\033[0m".format(
                "Token: ",
                len(self.prompt.format_prompt(query=query, content=content).text) / 4,
            )
        )
        try:
            response = self.chain.run({"query": query, "content": content})
            print("\033[92;1m" + response + "\033[0m\n")
            response = self.extract_response(response)
            # print(f"Prompt: {prompt.template}")  # For debugging only

            return response
        except IndexError:
            print("\033[91;1mThe model can't process this user.\033[0m\n")
            return ""

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
            if "Response:" in response:
                response = response.split("Response:")[1]
            elif "Final Thought:" in response:
                response = response.split("Final Thought:")[1]
            response = response.split("\n")[0].strip()
            response = "".join(char for char in response if char.isdigit())
            if not all(char.isdigit() for char in response):
                return ""

            if len(response) > 2 and response != "100":
                return ""

            return response
        except Exception as e:
            print(f"\033[91;1m{e}.\033[0m\n")
            return ""
