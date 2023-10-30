import os
import together

TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]
together.api_key = TOGETHER_API_KEY

LOCAL_LLM_PORT = os.environ.get("LLM_PORT")
LOCAL_LLM_URL = f"http://127.0.0.1:{LOCAL_LLM_PORT}"
LLM_URL = None

DEFAULT_SYSTEM_PROMPT = """
  You are expert topic interest inferer. Your task is to provide an interest of a human on a given topic on the scale of 1-100. Your response output should contain only one number that coresponds to the interest of the person on the topic.
  If the user seems to be extremly likely to be interested in the topic output 100. If the user doesn't seem to be likely to be interested at all output 0.
  You should never provide any explantion to the output, your response should be only in numbers corresponding to the scores, nothing else.

  topic: <{query}>
  Posts: ```{content}```
  """
INSTRUCTION = """For the above topic in '<>' and posts separated by '------------------'  in '``````' perform the following steps
  step 1: summarize each post that is separated by '------------------' at most 50 words.
  step 2: from the summarized posts above, identify sentences that are related to the given topic.
  step 3: if you can find sentences related to the provided topics procced with step 3 other wise output 0 and end your analysis.
  step 4: rate how much interested the user can be on the given topic on the scale of 1-100 based on the identified sentences and their correlation with the topic.
  step 5: ouput a single number that is precise and detailed with a variety of ranges that is between 1-100 based on step 4.

  Use the following format for your output. Don't ouput any text after the "Response:"
  Thought: <How do you find the user's interest given the posts>
  Action Input: <Method to find the user's interest>
  Action: <Find the user's top interests given the posts>
  Observation: <All of the user's top interests in one sentence>
  Thought: <Is {query} found in the User's interest>
  Action Input: <User's top interests>
  Action: <Search for {query} in the User's top interests>
  Observation: <Is the user interested in {query}>
  Thought: <How much can a user be interested in {query} if the user currenly given the current interests.>
  Action Input: <User's top interest, Interested or not>
  Action: <Analyze the user's top interests and Interested or not to find a number corresponding to the user interest in {query}>
  Obervation: <Found estimation number for the user's interest on {query} and why he might be interested>

  Response: <single number from 1-100>
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
