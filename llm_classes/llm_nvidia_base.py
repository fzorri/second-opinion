# Nvidia NIM API (OpenAI-compatible format)
# https://build.nvidia.com/nim-setup
# pip install openai

import os
import json
from openai import OpenAI
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

class Nvidia_LLM(LLMBase):
    def __init__(self, config_data):
        super().__init__(config_data)
        self.temperature = self.config.get("temperature", Tools.DEFAULT_TEMPERATURE)
        self.conversation_history = self._new_conversation()
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.client = self.initialize_client()

    def initialize_client(self):
        return OpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=self.api_key
        )

    def send_message(self, text):
        text = self._resolve_refs(text)
        self.conversation_history["messages"].append({"role": "user", "content": text})
        try:
            extra_body = {}
            if self.enable_thinking:
                extra_body["chat_template_kwargs"] = {
                    self.thinking_param: True,
                    "reasoning_effort": self.reasoning_effort
                }

            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=self.conversation_history["messages"],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                extra_body=extra_body if extra_body else None,
                stream=False
            )

            reasoning = getattr(response.choices[0].message, "reasoning", None) or \
                        getattr(response.choices[0].message, "reasoning_content", None)

            content = response.choices[0].message.content

            if reasoning and self.show_reasoning:
                reasoning_colored = Tools.format_reasoning(reasoning)
                full_response = f"**Reasoning:**\n{reasoning_colored}\n\n**Answer:**\n{content}"
            else:
                full_response = content

            usage = self._extract_usage(response)
            self.conversation_history["messages"].append({"role": "assistant", "content": full_response})
            self._update_metadata(usage)
            Tools.save_conversation(self.conversation_history, self.model_folder, self.timestamp)

            return self.model_name, full_response

        except Exception as e:
            error_message = "An unexpected error occurred:  \n" + str(e)
            return self.model_name, error_message

    def load_conversation(self, conversation_file):
        fname = os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history = self._normalize_conversation(json.load(ch))
