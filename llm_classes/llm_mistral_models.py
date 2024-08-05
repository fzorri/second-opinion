
from llm_classes.llm_mistral_base import Mistral_base
from config import Mistral_Codestral_CFG
class Mistral_Codestral_LLM(Mistral_base):
    def __init__(self):
        super().__init__(Mistral_Codestral_CFG)

from config import Mistral_Largest_CFG
class Mistral_Largest_LLM(Mistral_base):
    def __init__(self):
        super().__init__(Mistral_Largest_CFG)


