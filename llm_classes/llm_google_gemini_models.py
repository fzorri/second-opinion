# https://colab.research.google.com/github/google/generative-ai-docs/blob/main/site/en/gemini-api/docs/get-started/python.ipynb
# Notice that this solution is somewhat clumsy, without getting all the real power
# that gemini llm provides (No candidates, no asychronic, etc.)
# This is a FIRST iteration.
# prerequisite: pip install -q -U google-generativeai


import google.generativeai as genai
from llm_classes.llm_base import LLMBase
from llm_classes.llm_google_base import Google_Gemini_Base
from config import Gemini_Flash_1_5_CFG

class Gemini_Flash_1_5_LLM(Google_Gemini_Base):

    def __init__(self):
        super().__init__(Gemini_Flash_1_5_CFG)

from config import Gemini_Pro_1_5_CFG

class Gemini_Pro_1_5_LLM(Google_Gemini_Base):

    def __init__(self):
        super().__init__(Gemini_Pro_1_5_CFG)    