DEFAULT_SYSTEM_PROMPT = """\
      Given a person who has made the following posts, how would you rate their likely interest in the given query, on a scale from 1 to 100? Only output a single number and nothing else. If there is no indication that the person is not interested in the query, output 0. If there are things that indicate the person is absolutly interested on the subject output 100. You can also output a single digit between 1 and 100 to indicate how likely the person is to be interested in the query given the posts. Please only output a single number and nothing else. DO NOT explain anything, Just output the number.
  """

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
INSTRUCTION = "Rate the person's interest on the topic of {query} given the following posts/n Posts: {content}"
