import together
import requests
from ..LLM.Prompts import *
from ..LLM.TogetherLLM import TogetherLLM
from langchain import LLMChain
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from ..LLM.LLMMethods import *
from ..LLM.Prompts import *


class LLM:
    
    LOCAL_LLM_PORT = 5001
    LOCAL_LLM_URL = f"http://localhost:{LOCAL_LLM_PORT}"
    LLM_URL = None
    
    def __init__(self, temperature=0.1, max_tokens=512):
        llm = TogetherLLM(
            model="togethercomputer/llama-2-70b-chat", temperature=temperature, max_tokens=max_tokens
        )
        llm.start()
        
        self.model = llm
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def generate(self, query, content):
        prompt = Prompt().get_prompt_template()

        llm_chain = LLMChain(prompt=prompt, llm=self.model)
        
        response = llm_chain.run({"query": query, "content": content})
        response = response.split("Response:")[1]
        print(f"Prompt: {prompt.template}")  # For debugging only
        
        return response