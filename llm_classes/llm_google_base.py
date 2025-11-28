# https://colab.research.google.com/github/google/generative-ai-docs/blob/main/site/en/gemini-api/docs/get-started/python.ipynb
# Notice that this solution is somewhat clumsy, without getting all the real power
# that gemini llm provides (No candidates, no asychronic, etc.)
# This is a FIRST iteration.
# prerequisite: pip install -q -U google-generativeai
# Models: https://ai.google.dev/gemini-api/docs/models

import os
import json
import google.generativeai as genai
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

class Google_LLM(LLMBase):
    def __init__(self,config_data):
        super().__init__(config_data)
        self.conversation_history=[]
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.initialize_client() # Google's client configuration is global


    def initialize_client(self):
        return genai.configure(api_key=self.api_key)

    def send_message(self, text):
        generation_config = { "temperature": 0, "top_p": 0.95, "top_k": 64, "max_output_tokens": 8192, "response_mime_type": "text/plain",}
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE",},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE", },
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE", },
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE", },]
        try:
            model = genai.GenerativeModel( model_name=self.model_id, safety_settings=safety_settings, generation_config=generation_config,)

            self.conversation_history.append({"role": "user", "parts": [text + "\n"]})
            chat_session = model.start_chat(history=self.conversation_history)
            response = chat_session.send_message(text)

            # Add LLM response to history
            self.conversation_history.append({"role": "model", "parts": [response.text]})

            Tools.save_conversation(self.conversation_history,self.model_folder,self.timestamp)
            return self.model_name, response.text
        except Exception as e:
            error_message = "An unexpected error occurred:  \n" + str(e)
            return self.model_name, error_message


    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=json.load(ch)


