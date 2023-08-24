import textwrap
import together
from LLM import TogetherLLM
from langchain import PromptTemplate, LLMChain


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
