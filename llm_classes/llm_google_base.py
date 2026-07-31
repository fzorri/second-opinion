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
        self.conversation_history=self._new_conversation()
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.initialize_client()

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
            # Build tools list for web search
            tools = []
            if self.web_search:
                tools.append({"google_search": {}})
            
            model = genai.GenerativeModel(
                model_name=self.model_id,
                safety_settings=safety_settings,
                generation_config=generation_config,
                tools=tools if tools else None
            )

            # Handle multimodal content (list of blocks) - skip _resolve_refs
            if isinstance(text, list):
                parts = []
                for block in text:
                    if block["type"] == "text":
                        # Resolve refs in text blocks only
                        resolved = self._resolve_refs(block["text"])
                        parts.append(resolved)
                    elif block["type"] == "image":
                        # Gemini wants raw bytes, not base64 string
                        import base64
                        parts.append({
                            "mime_type": block["mime_type"],
                            "data": base64.b64decode(block["data"])
                        })
                self.conversation_history["messages"].append({"role": "user", "parts": parts})
            else:
                text = self._resolve_refs(text)
                self.conversation_history["messages"].append({"role": "user", "parts": [text + "\n"]})
            
            chat_session = model.start_chat(history=self.conversation_history["messages"])
            response = chat_session.send_message(text)

            usage = self._extract_usage(response)
            self.conversation_history["messages"].append({"role": "model", "parts": [response.text]})
            self._update_metadata(usage)
            Tools.save_conversation(self.conversation_history,self.model_folder,self.timestamp)
            return self.model_name, response.text
        except Exception as e:
            error_message = "An unexpected error occurred:  \n" + str(e)
            return self.model_name, error_message

    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=self._normalize_conversation(json.load(ch))


