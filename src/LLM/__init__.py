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
    "Search for explicit mentions of the topic in the posts",
    "Search for indication of interest in the topic from the posts",
    "Search for similar topics to the given topic in the posts",
    "Pick a number from the interest levels matching the user's interest in the topic of question",
]

InterestLevels = [
    "very unlikely(10-20)",
    "unlikely(20-30)",
    "maybe unlikely(30-40)",
    "neutral(40-50)",
    "maybe likely(50-60)",
    "likely(60-70)",
    "very likely(70-80)",
    "Extremely likely(80-100)",
]

DEFAULT_SYSTEM_PROMPT = """
You are expert topic interest inferer. Your task is to provide an interest of a human on a given topic on the scale of 1-100. Your response output should contain only one number that coresponds to the interest of the person on the topic. If the user seems to be extremly likely to be interested in the topic output 100. If the user doesn't seem to be likely to be interested at all output 0. If the user's interest is between the two, output a flexible number between 0 and 100 corresponding to the user's interest in the given topic as preciely as possible.
human: {query}
Posts: {content}
"""
INSTRUCTION = """Given the topic and the Posts above.

Use the following format:
Question: The topic the human asked you

Thought: you should always think about what to do
Action: the action to take, should be one of {actions}
Action Input: the input to the action
Observation: verbal description of what you learned after perorming the above action
(... this pattern 'Thought/Action/Action Input/Observation' can be repeated N times as needed)

Final Thought: you now know what the final respond should be.
Response: only single number from 1-100 using {InterestLevels} as a guide.
"""

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

SYSTEM_PROMPT = DEFAULT_SYSTEM_PROMPT

palm.configure(api_key=API_KEY)

# Selecting the first and only text generation model available in palm
model = GooglePalm(temperature=0.0, google_api_key=API_KEY)
