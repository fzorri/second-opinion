
# https://api-docs.deepseek.com/quick_start/pricing

import os
import json
from openai import OpenAI
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

class DeepSeek_LLM(LLMBase):
    def __init__(self, config_data):
        super().__init__(config_data)
        self.conversation_history = self._new_conversation()
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.client = self.initialize_client()

    def initialize_client(self):
        return OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

    def send_message(self, text):
        text = self._resolve_refs(text)
        self.conversation_history["messages"].append({"role": "user", "content": text})

        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=self.conversation_history["messages"],
                max_tokens=1024, temperature=0.1, stream=False
            )

            usage = self._extract_usage(response)
            self.conversation_history["messages"].append({"role": "assistant", "content": response.choices[0].message.content})
            self._update_metadata(usage)
            Tools.save_conversation(self.conversation_history, self.model_folder, self.timestamp)
            return self.model_name, response.choices[0].message.content
        except Exception as e:
             error_message = "An unexpected error occurred:  \n" + str(e)
             return self.model_name, error_message

    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=self._normalize_conversation(json.load(ch))





