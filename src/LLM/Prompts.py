DEFAULT_SYSTEM_PROMPT = """
  You are expert human topic interest inferer.
  You are given a summarized paragraphs of posts below in a triple back ticks.
  Follow the following step and rate the persons interest in the topic given below in the angular brackets on the scale of 100.
  Your output should only contain a single number.
  """
#The current working prompt
"Given a person who is described as follows, display a single number denoting how much the person would be interested in the given topic from 1-100. If there is no indication that the person is not interested in the query, output 0. If there are things that indicate the person is absolutly interested on the subject output 100. You can also output a single digit between 1 and 100 to indicate how likely the person is to be interested in the topic based on the given description. Please only output a single number and nothing else. DO NOT explain anything, Just output the number."

SUMMERIZE_SYSTEM_PROMPT = """
    Given the following paragraphs separated by **** in a triple backticks, summarize each paragraph using excalty 50 words.
    Your response should contain all the paragraphs separated by **** with no other additional infomation attached to it.
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
S_SYSTEM_PROMPOT = B_SYS + SUMMERIZE_SYSTEM_PROMPT + E_SYS

INSTRUCTION = """How much is the person interested in the following topic separated by angular brackets given the following posts in triple backticks.
topic: <{query}>
Description: ```{content}```
Response: <single number from 1-100>
"""
S_INSTRUCTION = """Shorten each of the following posts that are put into separate paragraph. Summerize each post without losing its context and topic into a single sentence. You should responde with a single long paragraph that has all summeries about the posts.
Posts: {content}"""
