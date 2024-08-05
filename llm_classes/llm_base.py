# llm_base.py

class LLMBase:
    USE_MARKDOWN = True
    
    def __init__(self):
        self.client = self.initialize_client()

    def initialize_client(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def send_message(self, text):
        raise NotImplementedError("Subclasses should implement this method.")

    def get_response(self, text):
        return self.send_message(text)

    
    def load_conversation(self, conversation_history):
        raise NotImplementedError("Subclasses should implement this method.")
    
    
