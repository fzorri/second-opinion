# another_llm.py
# prerequisite: pip install openai
# 20250501: the parameter max_completion_tokens have changed to max tokens without warning

import os
import json
from openai import OpenAI
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown


class OpenAI_LLM(LLMBase):
    # Define a default token limit
    def __init__(self, config_data):
        super().__init__(config_data)
        self.temperature= self.config.get("temperature", Tools.DEFAULT_TEMPERATURE)
        self.conversation_history = []
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.client = self.initialize_client()

    #this is going to return self.client= MistralClient initialized
    def initialize_client(self):
        return OpenAI(api_key=self.api_key)        

    def send_message(self, text):
        # Append the user's message to the conversation history
        # max_tokens=self.max_tokens, 
        self.conversation_history.append({"role": "user", "content": text})
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=self.conversation_history,
                max_tokens =self.max_tokens,
                temperature=self.temperature, 
                stream=False )

            # Append the model's response to the conversation history
            self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})

            Tools.save_conversation(self.conversation_history,self.model_folder,
                                    self.timestamp)
            return self.model_name, response.choices[0].message.content

        except Exception as e:
            error_message = "An unexpected error occurred:  \n" + str(e)
            return self.model_name, error_message

    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=json.load(ch)

