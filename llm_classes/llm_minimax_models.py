from llm_classes.llm_minimax_base import MinimaxLLMBase
from config import Minimax_Text01_CFG

class Minimax_Text01_LLM(MinimaxLLMBase):
    def __init__(self):
        super().__init__(Minimax_Text01_CFG)

from config import Abab_Chat_CFG

class Abab_Chat_LLM(MinimaxLLMBase):
    def __init__(self):
        super().__init__(Abab_Chat_CFG)