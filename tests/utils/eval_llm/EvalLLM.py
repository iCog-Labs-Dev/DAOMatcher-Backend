from tests.utils.eval_llm import model
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from tests.utils.eval_llm import SYSTEM_PROMPT, INSTRUCTION, ACTIONS, InterestLevels

from langchain_core.output_parsers import StrOutputParser


class EvalLLM:
    def __init__(self, temperature=0.1, max_tokens=512):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt = Prompt().get_prompt_template()

        self.chain = self.prompt | self.model | StrOutputParser()

    def evaluate_rag_output(self, topic, score, user_data):
        response = self.chain.invoke(
            {
                "topic": topic,
                "user_data": user_data,
                "score": score,
            }
        )
        print("\n" + response + "\n")

        response = self.extract_score(response)

        return response

    def extract_score(self, response):
        response = response.split("Overall: ")[1]
        return response


class Prompt:
    def get_prompt_template(self, query=INSTRUCTION, system_prompt=SYSTEM_PROMPT):
        template = system_prompt + query

        prompt = PromptTemplate(
            template=template,
            input_variables=(["topic", "user_data", "score"]),
        )
        prompt = prompt.partial(actions=str(ACTIONS), intervals=str(InterestLevels))
        return prompt
