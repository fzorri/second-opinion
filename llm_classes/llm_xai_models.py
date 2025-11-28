from llm_classes.llm_xai_base import Xai_Base

from config import Xai_Grok4_CFG

class Xai_Grok4_LLM(Xai_Base):
    def __init__(self):
        super().__init__(Xai_Grok4_CFG)

from config import Xai_Grok4_Fast_CFG

class Xai_Grok4_Fast_LLM(Xai_Base):
    def __init__(self):
        super().__init__(Xai_Grok4_Fast_CFG)



# Xai_Grok_41_fast_non_reasoning_CFG

from config import Xai_Grok_41_fast_non_reasoning_CFG
class Xai_Grok_41_fast_non_reasoning_LLM(Xai_Base):
    def __init__(self):
        super().__init__(Xai_Grok_41_fast_non_reasoning_CFG)

from config import Xai_Grok_41_fast_reasoning_CFG
class Xai_Grok_41_fast_reasoning_LLM(Xai_Base):
    def __init__(self):
        super().__init__(Xai_Grok_41_fast_reasoning_CFG)

'''
from config import Xai_Grok2_CFG

class Xai_Grok2_LLM(Xai_Base):
    def __init__(self):
        super().__init__(Xai_Grok2_CFG)


from config import Xai_GrokBeta_CFG

class Xai_GrokBeta_LLM(Xai_Base):
    def __init__(self):
        super().__init__(Xai_GrokBeta_CFG)
'''
        