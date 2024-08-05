# another_llm.py
# prerequisite: pip install openai

from llm_classes.llm_openai_chatgpt_base import OpenAI_ChatGPT_Base
from config import OpenAI_35_TURBO_CFG, OpenAI_4TURBO_CFG, OpenAI_4OMNI_CFG, OpenAI_4O_MINI_CFG
class OpenAI_35_TURBO_LLM(OpenAI_ChatGPT_Base):
    def __init__(self):
        super().__init__(OpenAI_35_TURBO_CFG)

 
#from config import OpenAI_4TURBO_CFG
class OpenAI_4TURBO_LLM(OpenAI_ChatGPT_Base):
    def __init__(self):
        super().__init__(OpenAI_4TURBO_CFG)


#from config import OpenAI_4OMNI_CFG
class OpenAI_4OMNI_LLM(OpenAI_ChatGPT_Base):
    def __init__(self):
        super().__init__(OpenAI_4OMNI_CFG)

class OpenAI_4O_MINI_LLM(OpenAI_ChatGPT_Base):
    def __init__(self):
        super().__init__(OpenAI_4O_MINI_CFG)
