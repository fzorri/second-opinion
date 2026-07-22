# llm_base.py
import os
import re
from datetime import datetime
from config import MAX_FILE_SIZE_EMBED


class LLMBase:
    USE_MARKDOWN = True

    def __init__(self, config_data):
        self.config = config_data
        self.model_name = self.config.get("model_name")
        self.model_id = self.config.get("model_id")
        self.model_folder = self.config.get("model_folder")
        self.api_key = self.config.get("API_KEY")
        self.max_tokens = self.config.get("max_tokens")
        self.enabled = self.config.get("enabled", True)
        self.enabled_reason = self.config.get("enabled_reason", "")
        self.show_reasoning = self.config.get("show_reasoning", True)

        # Thinking/reasoning configuration (Nvidia-specific)
        self.enable_thinking = self.config.get("enable_thinking", False)
        self.reasoning_effort = self.config.get("reasoning_effort", "high")
        self.thinking_param = self.config.get("thinking_param", "thinking")

        self.client = None # Client will be initialized by subclass

    def _init_metadata(self, conversation_name=""):
        return {
            "conversation_name": conversation_name,
            "last_updated": datetime.now().strftime("%Y%m%d-%H%M%S"),
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tokens": 0
        }

    def _new_conversation(self):
        return {
            "messages": [],
            "metadata": self._init_metadata()
        }

    def _normalize_conversation(self, data):
        if isinstance(data, list):
            return {
                "messages": data,
                "metadata": self._init_metadata()
            }
        return data

    def _extract_usage(self, response):
        usage = {}
        resp_usage = getattr(response, 'usage', None) or getattr(response, 'usage_metadata', None)
        if resp_usage:
            usage['input_tokens'] = (
                getattr(resp_usage, 'prompt_tokens', None) or
                getattr(resp_usage, 'input_tokens', None) or
                getattr(resp_usage, 'prompt_token_count', None) or 0
            )
            usage['output_tokens'] = (
                getattr(resp_usage, 'completion_tokens', None) or
                getattr(resp_usage, 'output_tokens', None) or
                getattr(resp_usage, 'candidates_token_count', None) or 0
            )
            usage['total_tokens'] = (
                getattr(resp_usage, 'total_tokens', None) or
                getattr(resp_usage, 'total_token_count', None) or
                (usage['input_tokens'] + usage['output_tokens'])
            )
        return usage if usage else None

    def _update_metadata(self, usage=None):
        self.conversation_history["metadata"]["last_updated"] = datetime.now().strftime("%Y%m%d-%H%M%S")
        if usage:
            self.conversation_history["metadata"]["total_input_tokens"] += usage.get("input_tokens", 0)
            self.conversation_history["metadata"]["total_output_tokens"] += usage.get("output_tokens", 0)
            self.conversation_history["metadata"]["total_tokens"] += usage.get("total_tokens", 0)

    def _resolve_files(self, text):
        max_embed = self.config.get("max_file_size_embed") or MAX_FILE_SIZE_EMBED

        def replace_at(match):
            path = match.group(1).strip('"').strip("'")
            path = os.path.expanduser(path)
            if not os.path.exists(path):
                return f"[File not found: {path}]"
            try:
                size = os.path.getsize(path)
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                lines = content.count('\n') + 1
                name = os.path.basename(path)

                if size <= max_embed:
                    print(f"[Embedded: {name} - {lines} lines, {size} chars]")
                    return f"[File: {name} - {lines} lines, {size} chars]\n{content}\n[/File]"
                else:
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    safe_name = re.sub(r'[^\w\-]', '_', os.path.splitext(name)[0])
                    ref_name = f"{safe_name}_{timestamp}.txt"
                    attach_dir = os.path.join(self.model_folder, "attachments")
                    os.makedirs(attach_dir, exist_ok=True)
                    with open(os.path.join(attach_dir, ref_name), 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"[Attached: {name} - {lines} lines, {size} chars]")
                    return f"[File: {name} - {lines} lines, {size} chars]\n[Ref: {ref_name}]\n[/File]"
            except Exception as e:
                return f"[Error reading {path}: {e}]"

        return re.sub(r'@("([^"]+)"|\'([^\']+)\'|(\S+))', replace_at, text)

    def _resolve_refs(self, text):
        def replace_ref(match):
            ref_name = match.group(1)
            attach_path = os.path.join(self.model_folder, "attachments", ref_name)
            if not os.path.exists(attach_path):
                return f"[Attachment missing: {ref_name}]"
            try:
                with open(attach_path, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
            except Exception as e:
                return f"[Error reading attachment {ref_name}: {e}]"
        return re.sub(r'\[Ref: ([^\]]+)\]', replace_ref, text)

    def initialize_client(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def send_message(self, text):
        raise NotImplementedError("Subclasses should implement this method.")

    def get_response(self, text):
        text = self._resolve_files(text)
        return self.send_message(text)

    def load_conversation(self, conversation_history):
        raise NotImplementedError("Subclasses should implement this method.")
