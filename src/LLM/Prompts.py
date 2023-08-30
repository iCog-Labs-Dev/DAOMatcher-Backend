DEFAULT_SYSTEM_PROMPT = """
  You are expert topic interest inferer. Your task is to provide an interest of a human on a given topic on the scale of 1-100. Your response output should contain only one number that coresponds to the interest of the person on the topic.
  If the user seems to be extremly likely to be interested in the topic output 100. If the user doesn't seem to be likely to be interested at all output 0.
  You should never provide any explantion to the output, your response should be only in numbers corresponding to the scores, nothing else.
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
step 1: analyze whether the given description is related to the topic or not
step 2: if the description is related, predict the description relation to the topic on the scale of 1-100
step 3: if the description is not related, predict the description relation to the topic as 0
step 4: ouput a single number based on your analysis

topic: <{query}>
Description: ```{content}```

Strictly follow the following output format. Don't include any response that is not included in here.
Response: <single number from 1-100>
"""
S_INSTRUCTION = """Shorten each of the following posts that are put into separate paragraph. Summerize each post without losing its context and topic into a single sentence. You should responde with a single long paragraph that has all summeries about the posts.
Posts: {content}"""
