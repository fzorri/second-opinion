from llm_classes.llm_fireworks_base import Fireworks_Base
from config import Fireworks_Llama3_8b_Instruct_CFG

class Fireworks_Llama3_8b_Instruct_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Llama3_8b_Instruct_CFG)


from config import Fireworks_Mistral_8x22_CFG

class Fireworks_Mistral_8x22_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Mistral_8x22_CFG)


from config import Fireworks_Qwen2_Chat_CFG

class Fireworks_Qwen2_Chat_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Qwen2_Chat_CFG)   


from config import Fireworks_Qwen2_Instruct_CFG

class Fireworks_Qwen2_Instruct_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Qwen2_Instruct_CFG)


from config import Fireworks_StarCoder2_16b_CFG

class Fireworks_StarCoder2_16b_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_StarCoder2_16b_CFG)

from config import Fireworks_Yi_Large_CFG
class Fireworks_Yi_Large_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Yi_Large_CFG)

from config import Fireworks_Llama3_1_70b_CFG

class Fireworks_Llama3_1_70b_LLM(Fireworks_Base):
    def __init__(self):
        super().__init__(Fireworks_Llama3_1_70b_CFG)

