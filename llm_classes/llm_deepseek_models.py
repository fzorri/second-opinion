from llm_classes.llm_deepseek_base import DeepSeekLLMBase
from config import DeepSeek_Chat_CFG

class DeepSeek_Chat_LLM(DeepSeekLLMBase):
    def __init__(self):
        super().__init__(DeepSeek_Chat_CFG)

from config import DeepSeek_Code_CFG

class DeepSeek_Code_LLM(DeepSeekLLMBase):
    def __init__(self):
        super().__init__(DeepSeek_Code_CFG)