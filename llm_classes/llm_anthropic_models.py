

from llm_classes.llm_anthropic_base import Anthropic_Claude_Base
from config import Anthropic_Claude_Haiku_CFG
class Anthropic_Claude_Haiku_LLM(Anthropic_Claude_Base):
    def __init__(self):
        super().__init__(Anthropic_Claude_Haiku_CFG)
                      
from config import Anthropic_Claude_Opus_CFG
class Anthropic_Claude_Opus_LLM(Anthropic_Claude_Base):
    def __init__(self):
        super().__init__(Anthropic_Claude_Opus_CFG)

from config import Anthropic_Claude_Sonnet_CFG
class Anthropic_Claude_Sonnet_LLM(Anthropic_Claude_Base):
    def __init__(self):
        super().__init__(Anthropic_Claude_Sonnet_CFG)    


from config import Anthropic_Claude_Haiku_45_CFG
class Anthropic_Claude_Haiku_45_LLM(Anthropic_Claude_Base):
    def __init__(self):
        super().__init__(Anthropic_Claude_Haiku_45_CFG)
                      
from config import Anthropic_Claude_Opus_45_CFG
class Anthropic_Claude_Opus_45_LLM(Anthropic_Claude_Base):
    def __init__(self):
        super().__init__(Anthropic_Claude_Opus_45_CFG)

from config import Anthropic_Claude_Sonnet_45_CFG
class Anthropic_Claude_Sonnet_45_LLM(Anthropic_Claude_Base):
    def __init__(self):
        super().__init__(Anthropic_Claude_Sonnet_45_CFG)  