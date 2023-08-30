DEFAULT_SYSTEM_PROMPT = """
  You are expert topic interest inferer. Your task is to provide an interest of a human on a given topic on the scale of 1-100. Your response output should contain only one number that coresponds to the interest of the person on the topic.
  If the user seems to be extremly likely to be interested in the topic output 100. If the user doesn't seem to be likely to be interested at all output 0.
  You should never provide any explantion to the output, your response should be only in numbers corresponding to the scores, nothing else.
  """
#The current working prompt
"Given a person who is described as follows, display a single number denoting how much the person would be interested in the given topic from 1-100. If there is no indication that the person is not interested in the query, output 0. If there are things that indicate the person is absolutly interested on the subject output 100. You can also output a single digit between 1 and 100 to indicate how likely the person is to be interested in the topic based on the given description. Please only output a single number and nothing else. DO NOT explain anything, Just output the number."

SUMMERIZE_SYSTEM_PROMPT = """
    Given the following paragraphs separated by '------------------' in a triple backticks, summarize each paragraph using at most 50 words.
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
S_SYSTEM_PROMPOT = B_SYS + SUMMERIZE_SYSTEM_PROMPT + E_SYS

INSTRUCTION = """For the following topic in '<>' and posts separated by '------------------'  in '``````' perform the following steps
step 1: summarize each post that is separated by '------------------' at most 50 words.
step 2: from the summarized posts above, identify sentences that are related to the given topic.
step 3: if you can find sentences related to the provided topics procced with step 3 other wise output 0 and end your analysis.
step 4: rate how much interested the user can be on the given topic on the scale of 1-100 based on the identified sentences and their correlation with the topic.
step 5: ouput a single number based on step 4.

topic: <{query}>
Description: ```{content}```

Strictly provide your output as follows. Don't include any explanation or any text.
Response: <single number from 1-100>
"""
S_INSTRUCTION = """
For the posts provided in triple backticks, summarize each post in using at most 50 words.
Each posts are separated using '------------------', so your output should also be separated by '------------------'
corresponding to each summarized posts.

Posts: ```{content}```

Use the following format for the output.
Response: <Summarized Post 1.------------------Summarized Post 2.------------------>

"""
