# llm_base.py

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
        self.client = None # Client will be initialized by subclass

    def initialize_client(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def send_message(self, text):
        raise NotImplementedError("Subclasses should implement this method.")

    def get_response(self, text):
        return self.send_message(text)

    
    def load_conversation(self, conversation_history):
        raise NotImplementedError("Subclasses should implement this method.")
    
    
