import textwrap
from src.LLM import INSTRUCTION, SYSTEM_PROMPT, B_INST, E_INST, ACTIONS, InterestLevels
from langchain import PromptTemplate


class Prompt:
    def get_prompt_template(self, query=INSTRUCTION, system_prompt=SYSTEM_PROMPT):
        template = system_prompt + query

        prompt = PromptTemplate(
            template=template,
            input_variables=["query", "content", "actions", "InterestLevels"]
            if system_prompt == SYSTEM_PROMPT
            else ["content"],
        )
        prompt = prompt.partial(
            actions=str(ACTIONS), InterestLevels=str(InterestLevels)
        )
        return prompt

    ## Helper function to format the response
    def cut_off_text(text, prompt):
        cutoff_phrase = prompt
        index = text.find(cutoff_phrase)
        if index != -1:
            return text[:index]
        else:
            return text

    def remove_substring(string, substring):
        return string.replace(substring, "")

    def parse_text(text):
        wrapped_text = textwrap.fill(text, width=100)
        return wrapped_text
