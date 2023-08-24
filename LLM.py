import os
import together
import textwrap
from dotenv import load_env
from pyngrok import ngrok
from flask import Flask, request
from pydantic import Extra
from langchain.llms.base import LLM
from langchain import PromptTemplate, LLMChain
from langchain.utils import get_from_dict_or_env
from typing import Any, Dict


load_env()

# set your API key
together.api_key = os.environ["TOGETHER_API_KEY"]


class TogetherLLM(LLM):
    """Together large language models."""

    model: str = "togethercomputer/llama-2-70b-chat"
    """model endpoint to use"""

    together_api_key: str = os.environ["TOGETHER_API_KEY"]
    """Together API key"""

    temperature: float = 0.7
    """What sampling temperature to use."""

    max_tokens: int = 512
    """The maximum number of tokens to generate in the completion."""

    class Config:
        extra = Extra.forbid

    @staticmethod
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(values, "together_api_key", "TOGETHER_API_KEY")
        values["together_api_key"] = api_key
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(
            prompt,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        text = output["output"]["choices"][0]["text"]
        return text


# llm = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature':0})
def init_model():
    llm = TogetherLLM(
        model="togethercomputer/llama-2-70b-chat", temperature=0.1, max_tokens=512
    )
    together.Models.start("togethercomputer/llama-2-70b-chat")
    print("Model started successfully")
    return llm


DEFAULT_SYSTEM_PROMPT = """\
    You are an expert person interest rator who specialized in rating a person's interest given a list of posts made by the person. Your task is to rate the persons interest out of 100 and display only the number. The person you are working with hates reasoning and will fire you if you give any further explanation.
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS


def get_prompt(query):
    template = B_INST + SYSTEM_PROMPT + query + E_INST
    prompt = PromptTemplate(template=template, input_variables=["query", "content"])
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


def generate(query, content, llm):
    prompt = get_prompt(
        "Rate the person's interest on the topic of {query} given the following posts/n Posts: {content}"
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run({"query": query, "content": content})
    print(f"Prompt: {prompt}")
    return response


def parse_text(text):
    wrapped_text = textwrap.fill(text, width=100)
    return wrapped_text


port_no = 5000

app = Flask(__name__)
ngrok.set_auth_token("2TeUpGO7kAzr6rQYvURgNGIO0qG_25bMqYYu3vAcyUf72tc9i")
public_url = ngrok.connect(port_no).public_url
llm = init_model()


@app.route("/", methods=["GET", "POST"])
def semantic_search_query():
    if request.method == "GET":
        return "Send post request"
    elif request.method == "POST":
        print(request)
        query = request.json["query"]
        content = request.json["content"]
        prompt = generate(query, content, llm)
        print(prompt)
        return prompt


print(f"Public url for the API... {public_url}")

app.run(port=port_no)
together.Models.stop("togethercomputer/llama-2-70b-chat")
