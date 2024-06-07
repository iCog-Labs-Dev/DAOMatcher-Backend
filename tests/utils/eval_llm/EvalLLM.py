from tests.utils.eval_llm import model
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from tests.utils.eval_llm import SYSTEM_PROMPT


class EvalLLM:
    def __init__(self, temperature=0.1, max_tokens=512):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt = PromptTemplate(
            template=SYSTEM_PROMPT,
            input_variables=("topic", "rag_output", "user_data"),
        )

        self.chain = LLMChain(prompt=self.prompt, llm=self.model)

    def evaluate_rag_output(self, topic, rag_output, user_data, score):
        prompt_data = {
            "topic": topic,
            "rag_output": rag_output,
            "user_data": user_data,
            "score": "{score}",
        }

        self.prompt.format_prompt(**prompt_data)
        response = self.chain.predict(
            topic=topic, rag_output=rag_output, user_data=user_data, score=score
        )

        # response = self.extract_score(response)

        return response

    def extract_score(self, response):
        response = response.split("Response: ")[1]
        return response
