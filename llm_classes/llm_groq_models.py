from llm_classes.llm_groq_base import Groq_Base
from config import Groq_Llama3_CFG

class Groq_Llama3_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Llama3_CFG)

from config import Groq_MixtralAL8x7b_CFG

class Groq_MixtralAL8x7b_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Llama3_CFG)
                    
#Groq_Gemma2_9b
from config import Groq_Gemma2_9b_CFG

class Groq_Gemma2_9b_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Gemma2_9b_CFG)
