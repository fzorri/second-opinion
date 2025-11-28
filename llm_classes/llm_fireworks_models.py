from llm_classes.llm_fireworks_base import Fireworks_Base

from config import Fireworks_Mistral_8x22_CFG
class Fireworks_Mistral_8x22_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Mistral_8x22_CFG)
        
      
from config import Fireworks_Qwen3_CFG
class Fireworks_Qwen3_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Qwen3_CFG)      


from config import Fireworks_KimiK2T_CFG
class Fireworks_KimiK2T_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_KimiK2T_CFG)      

'''
from config import Fireworks_Qwen3_235b_CFG

class Fireworks_Qwen3_235b_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Qwen3_235b_CFG)      

from config import Fireworks_StarCoder2_16b_CFG

class Fireworks_StarCoder2_16b_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_StarCoder2_16b_CFG)

20251028: Removido
from config import Fireworks_Yi_Large_CFG
class Fireworks_Yi_Large_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Yi_Large_CFG)

20251028 : Deprecated
from config import Fireworks_DeepSeekR1_CFG
class Fireworks_DeepSeekR1_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_DeepSeekR1_CFG)        

        class Fireworks_Llama3_1_70b_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Llama3_1_70b_CFG)

from config import Fireworks_Llama3_1_405b_CFG

class Fireworks_Llama3_1_405b_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Llama3_1_405b_CFG)


'''
