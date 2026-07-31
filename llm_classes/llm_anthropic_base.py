# 
# https://docs.anthropic.com/en/api/client-sdks#python
# prerequisit: pip install anthropic
# anthropic_llm.py

import os
import json
import anthropic
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

class Anthropic_LLM(LLMBase):
    def __init__(self, config_data):
        super().__init__(config_data)
        self.conversation_history = self._new_conversation()
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.client = self.initialize_client()

    def initialize_client(self):
        return anthropic.Anthropic(api_key=self.api_key)

    def send_message(self, text):
        # Handle multimodal content (list of blocks) - skip _resolve_refs
        # NOTE: Anthropic retains images across turns (unlike other providers).
        # For now, we re-send images in history for consistency.
        # A future optimization could strip images from history for Anthropic
        # to save tokens, since Claude already has them in context.
        if isinstance(text, list):
            content = []
            for block in text:
                if block["type"] == "text":
                    # Resolve refs in text blocks only
                    resolved = self._resolve_refs(block["text"])
                    content.append({"type": "text", "text": resolved})
                elif block["type"] == "image":
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": block["mime_type"],
                            "data": block["data"],
                        }
                    })
            self.conversation_history["messages"].append({"role": "user", "content": content})
        else:
            text = self._resolve_refs(text)
            self.conversation_history["messages"].append({"role": "user", "content": text})

        try:
            response = self.client.messages.create( model=self.model_id,max_tokens=2048,
                                               temperature=0, 
                                               messages=self.conversation_history["messages"] )

            usage = self._extract_usage(response)
            self.conversation_history["messages"].append({"role": "assistant", "content": response.content[0].text})
            self._update_metadata(usage)
            Tools.save_conversation(self.conversation_history,self.model_folder,self.timestamp)
            return self.model_name , response.content[0].text
        
        except anthropic.BadRequestError as e:
            error_message = "An error happened processing the request:  \n" + str(e)
            return self.model_name, error_message
        except Exception as e:
             error_message = "An unexpected error occurred:  \n" +  str(e)
             return self.model_name, error_message

    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=self._normalize_conversation(json.load(ch))

        