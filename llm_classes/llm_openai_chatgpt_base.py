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
    def __init__(self, config_data):
        super().__init__(config_data)
        self.temperature= self.config.get("temperature", Tools.DEFAULT_TEMPERATURE)
        self.conversation_history = self._new_conversation()
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.client = self.initialize_client()

    def initialize_client(self):
        return OpenAI(api_key=self.api_key)        

    def send_message(self, text):
        # Handle multimodal content (list of blocks) - skip _resolve_refs
        if isinstance(text, list):
            content = []
            for block in text:
                if block["type"] == "text":
                    # Resolve refs in text blocks only
                    resolved = self._resolve_refs(block["text"])
                    content.append({"type": "text", "text": resolved})
                elif block["type"] == "image":
                    content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{block['mime_type']};base64,{block['data']}",
                            "detail": "auto"
                        }
                    })
            self.conversation_history["messages"].append({"role": "user", "content": content})
        else:
            text = self._resolve_refs(text)
            self.conversation_history["messages"].append({"role": "user", "content": text})
        
        try:
            # Build API parameters
            api_params = {
                "model": self.model_id,
                "messages": self.conversation_history["messages"],
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": False
            }
            
            # Enable web search if configured
            if self.web_search:
                api_params["tools"] = [{"type": "web_search_preview"}]
            
            response = self.client.chat.completions.create(**api_params)

            usage = self._extract_usage(response)
            self.conversation_history["messages"].append({"role": "assistant", "content": response.choices[0].message.content})
            self._update_metadata(usage)
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
            self.conversation_history=self._normalize_conversation(json.load(ch))

