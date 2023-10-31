import os
import together
from dotenv import load_dotenv
import google.generativeai as palm
from langchain.llms import GooglePalm

TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]
together.api_key = TOGETHER_API_KEY
API_KEY = os.environ.get("PALM_API_KEY")

LOCAL_LLM_PORT = os.environ.get("LLM_PORT")
LOCAL_LLM_URL = f"http://127.0.0.1:{LOCAL_LLM_PORT}"
LLM_URL = None

ACTIONS = [
    "Find the user's top interests from the posts",
    "Search the topic in question in the User's top interests",
    "Analyze the user's top interests to find a number corresponding to the user's interest in the topic in question",
    "Decide which level of interest the user has from the Interest level list",
    "Pick a number from the interest level matching the user's interest in the topic in question",
]

InterestLevels = [
    "very unlikely(10-20)",
    "unlikely(20-30)",
    "maybe unlikely(30-40)",
    "neutral(40-50)",
    "maybe likely(50-60)",
    "likely(60-70)",
    "very likely(70-80)",
    "Extremely likely(70-100)",
]

DEFAULT_SYSTEM_PROMPT = """
You are expert topic interest inferer. Your task is to provide an interest of a human on a given topic on the scale of 1-100. Your response output should contain only one number that coresponds to the interest of the person on the topic. If the user seems to be extremly likely to be interested in the topic output 100. If the user doesn't seem to be likely to be interested at all output 0. If the user's interest is between the two, output a flexible number between 0 and 100 corresponding to the user's interest in the given topic as preciely as possible. You should always respond with "Response:" in the end what ever value you decide on.

Posts: {content}"""
INSTRUCTION = """Given the topic below and the Posts above. you should respond with the following format strictly and always include the "Response:" No matter what.

Use the following format:
Question: the interest level of the user in the topic asked by the human

Thought: you should always think about what to do
Action: the action to take, should be one of {actions}
Action Input: the input to the action
Observation: what you learned after perorming the above action
(repeat the above set of formats 'Thought/Action/Action Input/Oversvation' N times if you aren't sure what to respond)

Thought: you now know how to respond.
Response: single number from 1-100 using the {InterestLevels} as guide

human: {query}
AI:
"""

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

palm.configure(api_key=API_KEY)

# Selecting the first and only text generation model available in palm
model = GooglePalm(temperature=0.0, google_api_key=API_KEY)
