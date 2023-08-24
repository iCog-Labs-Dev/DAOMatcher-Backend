DEFAULT_SYSTEM_PROMPT = """\
      Given a person who is described as follows, display the how much the person would be interested in the given topic from 1-100. If there is no indication that the person is not interested in the query, output 0. If there are things that indicate the person is absolutly interested on the subject output 100. You can also output a single digit between 1 and 100 to indicate how likely the person is to be interested in the topic based on the given description. Please only output a single number and nothing else. DO NOT explain anything, Just output the number.
  """

SUMMERIZE_SYSTEM_PROMPT = """
    You are an expert post summerizer who can pin point the general topic of a post without losing its context in a single sentence. You can create a summary about a person that comes from the posts.
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
S_SYSTEM_PROMPOT = B_SYS + SUMMERIZE_SYSTEM_PROMPT + E_SYS

INSTRUCTION = "Rate the person's interest on the topic of {query} given the following posts/n Posts: {content}"
S_INSTRUCTION = """Summerize each of the following posts that are put in separate paragraphs into the same paragraph where there is a single sentence for each posts.
{content}"""
