DEFAULT_SYSTEM_PROMPT = """
  You are expert topic interest inferer. Your task is to provide an interest of a human on a given topic on the scale of 1-100. Your response output should contain only one number that coresponds to the interest of the person on the topic.
  If the user seems to be extremly likely to be interested in the topic output 100. If the user doesn't seem to be likely to be interested at all output 0.
  """
#The current working prompt
"Given a person who is described as follows, display a single number denoting how much the person would be interested in the given topic from 1-100. If there is no indication that the person is not interested in the query, output 0. If there are things that indicate the person is absolutly interested on the subject output 100. You can also output a single digit between 1 and 100 to indicate how likely the person is to be interested in the topic based on the given description. Please only output a single number and nothing else. DO NOT explain anything, Just output the number."

SUMMERIZE_SYSTEM_PROMPT = """
    Given the following paragraphs separated by '------------------' in a triple backticks, summarize each paragraph using excalty 50 words.
    Your response should contain all the paragraphs separated by '------------------' with no other additional infomation attached to it.
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
S_SYSTEM_PROMPOT = B_SYS + SUMMERIZE_SYSTEM_PROMPT + E_SYS

INSTRUCTION = """For the following topic in '<>' and description in '``````' perform the following steps
step 1: analyze whether the user could be interested in the topic or not
step 2: if the user is interested, predict the user's interest on the scale of 1-100
step 3: if the user is not interested, predict the user's interest as 0
step 4: ouput a single number based on your analysis

you should use only number format as your output.
topic: <{query}>
Description: ```{content}```
Response: <single number from 1-100>
"""
S_INSTRUCTION = """Shorten each of the following posts that are put into separate paragraph. Summerize each post without losing its context and topic into a single sentence. You should responde with a single long paragraph that has all summeries about the posts.
Posts: {content}"""
