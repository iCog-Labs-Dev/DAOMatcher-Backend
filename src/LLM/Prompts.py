import textwrap
from langchain import PromptTemplate

class Prompt:
  
  DEFAULT_SYSTEM_PROMPT = """
  You are expert topic interest inferer. Your task is to provide an interest of a human on a given topic on the scale of 1-100. Your response output should contain only one number that coresponds to the interest of the person on the topic.
  If the user seems to be extremly likely to be interested in the topic output 100. If the user doesn't seem to be likely to be interested at all output 0.
  You should never provide any explantion to the output, your response should be only in numbers corresponding to the scores, nothing else.
  """
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
  
  B_INST, E_INST = "[INST]", "[/INST]"
  B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
  
  SYSTEM_PROMPT = B_SYS + DEFAULT_SYSTEM_PROMPT + E_SYS
  
  def get_prompt_template(self, query=INSTRUCTION, system_prompt=SYSTEM_PROMPT):
    template = self.B_INST + system_prompt + query + self.E_INST
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["query", "content"]
        if system_prompt == self.SYSTEM_PROMPT
        else ["content"],
    )
    return prompt
  
  ## Helper function to format the response
  def cut_off_text(text, prompt):
      cutoff_phrase = prompt
      index = text.find(cutoff_phrase)
      if index != -1:
          return text[:index]
      else:
          return text
        
  def remove_substring(string, substring):
    return string.replace(substring, "")
  
  def parse_text(text):
    wrapped_text = textwrap.fill(text, width=100)
    return wrapped_text