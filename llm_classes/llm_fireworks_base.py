# Mistral 8x22 from fireworks.ai
# https://readme.fireworks.ai/docs/querying-text-models
# pip install --upgrade fireworks-ai

#Testing OpenAI compatibility https://readme.fireworks.ai/docs/querying-text-models#using-the-web-console

import os
import json
from fireworks.client import Fireworks
from fireworks.client.error import InvalidRequestError
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

class Fireworks_LLM(LLMBase):
    def __init__(self,config_data):
        super().__init__(config_data)
        self.conversation_history = self._new_conversation()
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.client = self.initialize_client()

    def initialize_client(self):
        return Fireworks(api_key=self.api_key)        

    def send_message(self, text):
        text = self._resolve_refs(text)
        self.conversation_history["messages"].append({"role": "user", "content": text})

        try:
            response = self.client.chat.completions.create( model=self.model_id, messages=self.conversation_history["messages"])

            usage = self._extract_usage(response)
            self.conversation_history["messages"].append({"role": "assistant", "content": response.choices[0].message.content})
            self._update_metadata(usage)
            Tools.save_conversation(self.conversation_history,self.model_folder,self.timestamp)

            return self.model_name, response.choices[0].message.content
        except InvalidRequestError as e:
            error_message = "An error happened processing the request:  \n" + str(e)
            return self.model_name, error_message
        except Exception as e:
             error_message = "An unexpected error occurred:  \n" + str(e)
             return self.model_name, error_message
    
    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=self._normalize_conversation(json.load(ch))

