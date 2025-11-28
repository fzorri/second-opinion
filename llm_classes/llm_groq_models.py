from llm_classes.llm_groq_base import Groq_Base
#from config import Groq_Llama3_CFG

from config import Groq_Llama33_70b_CFG
class Groq_Llama33_70b_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Llama33_70b_CFG)

from config import Groq_Kimi_K2_CFG
class Groq_Kimi_K2_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Kimi_K2_CFG)

from config import Groq_Qwen3_32b_CFG
class Groq_Qwen3_32b_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Qwen3_32b_CFG)

'''Deprecado 20251028
class Groq_Llama3_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Llama3_CFG)

Deprecado 20251228
from config import Groq_MixtralAL8x7b_CFG

class Groq_MixtralAL8x7b_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Llama3_CFG)
        
#Groq_Gemma2_9b . Deprecado 20251028
from config import Groq_Gemma2_9b_CFG

class Groq_Gemma2_9b_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_Gemma2_9b_CFG)

# Groq_DeepSeek_R1_Llama_70b_CFG        
Deprecated 20251028
from config import Groq_DeepSeek_R1_Llama_70b_CFG     
class Groq_DeepSeek_R1_Llama_70b_LLM(Groq_Base):
    def __init__(self):
        super().__init__(Groq_DeepSeek_R1_Llama_70b_CFG)
'''                
