import textwrap
import together
import requests
from ..LLM.Prompts import *
from ..LLM.TogetherLLM import TogetherLLM
from langchain import PromptTemplate, LLMChain
import requests


# llm = HuggingFacePipeline(pipeline = pipe, model_kwargs = {'temperature':0})
def init_model():
    llm = TogetherLLM(
        model="togethercomputer/llama-2-70b-chat", temperature=0.1, max_tokens=512
    )
    together.Models.start("togethercomputer/llama-2-70b-chat")
    print("Model started successfully")
    return llm


def get_prompt(query, system_prompt=SYSTEM_PROMPT):
    template = B_INST + system_prompt + query + E_INST
    prompt = PromptTemplate(
        template=template,
        input_variables=["query", "content"]
        if system_prompt == SYSTEM_PROMPT
        else ["content"],
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


def generate(query, content, llm):
    s_prompt = get_prompt(S_INSTRUCTION, S_SYSTEM_PROMPOT)
    prompt = get_prompt(INSTRUCTION)
    # print(prompt)

    s_llm_chain = LLMChain(prompt=s_prompt, llm=llm)
    s_content: str = s_llm_chain.run(content)
    s_content = s_content.replace("\n", "")

    print("Short content: ", s_content)

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run({"query": query, "content": s_content})
    # print(f"Prompt: {prompt}") #For debugging only
    return response


def parse_text(text):
    wrapped_text = textwrap.fill(text, width=100)
    return wrapped_text


# These vaiables are only used for the following function, hence defined here
LOCAL_LLM_PORT = 5001
LOCAL_LLM_URL = f"http://localhost:{LOCAL_LLM_PORT}"
LLM_URL = None


def generate_search(query, content):
    headers = {"Content-Type": "application/json"}  # Specify JSON content type
    data = {"query": query, "content": content}

    Url = LLM_URL if LLM_URL else LOCAL_LLM_URL

    try:
        response = requests.post(Url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Assuming the server returns JSON data as well
        generated_text = response.json()
        print("POST request successful")
        print("Response:", generated_text)
        return generated_text

    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")
        return str(e)
