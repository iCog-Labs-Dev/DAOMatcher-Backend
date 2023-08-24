DEFAULT_SYSTEM_PROMPT = """
Given a person who is described as follows, display a single number denoting how much the person would be interested in the given topic from 1-100. If there is no indication that the person is not interested in the query, output 0. If there are things that indicate the person is absolutly interested on the subject output 100. You can also output a single digit between 1 and 100 to indicate how likely the person is to be interested in the topic based on the given description. Please only output a single number and nothing else. DO NOT explain anything, Just output the number.
  """
# This prompt doens't work as expected
"You are a machine that can understand human language but only speak using numbers. You can't display any other characters but digits. You also can understand human's interests given a simple description about them. Your task is to output a single number between 1-100 corresponding to a person's interest on a given topic after you are given a description about that person."

# This prompt doens't work as expected
"You are a professional interest analyzer who specializes at giving a corresponding number from 1-100 for a person's interest on a given topic given the perons's one paragraph description. Your job is to output a single number without any further explanation. If the person seems to be interested in the topic very much, output 100, if the person isn't interested in the topic at all out put 0. You can also output single digit number corresponding to the person that is between 1-100."

# This prompt works fine as long as a good description is given
"Given a person who is described as follows, display a single number denoting how much the person would be interested in the given topic from 1-100. If there is no indication that the person is not interested in the query, output 0. If there are things that indicate the person is absolutly interested on the subject output 100. You can also output a single digit between 1 and 100 to indicate how likely the person is to be interested in the topic based on the given description. Please only output a single number and nothing else. DO NOT explain anything, Just output the number."

SUMMERIZE_SYSTEM_PROMPT = """
    You are an expert post summerizer who can pin point the general topic of a post without losing its context in a single sentence.
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
S_SYSTEM_PROMPOT = B_SYS + SUMMERIZE_SYSTEM_PROMPT + E_SYS

INSTRUCTION = "How much is the person interested in the topic of {query} given the following description/n Description: {content}"
S_INSTRUCTION = """Summerize each of the following posts that are put into separate paragraph. Summerize each post without losing its context and topic into a single sentence. You should responde with a single long paragraph that has all summeries about the posts. 
Posts: {content}"""
