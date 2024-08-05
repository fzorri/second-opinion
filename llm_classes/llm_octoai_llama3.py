# https://octoai.cloud/text/chat?model=meta-llama-3-70b-instruct
# Warning: correct declaration can be found in 
#https://octo.ai/docs/text-gen-solution/python-sdk
#prerequisite: pip install octoai

import os
import json
from octoai.text_gen import ChatMessage
from octoai.client import OctoAI
from llm_classes.llm_base import LLMBase
from config import OctoAI_LLama3_70_CFG
from tools import Tools
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown

class OctoAI_LLama3_70_LLM(LLMBase):
    def __init__(self):
        config           = OctoAI_LLama3_70_CFG
        self.api_key     = config["API_KEY"]
        self.modelName   = config["MODEL_NAME"]
        self.model       = config["MODEL_ID"]
        self.modelFolder = config["MODEL_FOLDER"]
        self.conversation_history=[]
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        super().__init__()  # Call the base class constructor

    #this is going to return self.client= OctoAI initialized
    def initialize_client(self):
        return OctoAI(api_key=self.api_key)        

    def send_message(self, text):
        # Add the new user message to the conversation history
        self.conversation_history.append(ChatMessage(role="user", content=text))
        try:
            response = self.client.text_gen.create_chat_completion(
            max_tokens=2048,
            messages=self.conversation_history,
            model=self.model,
            presence_penalty=0, temperature=0.1, top_p=0.9 )

            # Add the assistant's response to the conversation history
            self.conversation_history.append(ChatMessage(role="assistant", content=response.choices[0].message.content))

            Tools.save_conversation(self.conversation_history,self.modelFolder,self.timestamp, Tools.chat_message_encoder)

            return self.modelName, response.choices[0].message.content

        except Exception as e:
            error_message = "An unexpected error occurred:  \n" + str(e)
            return self.modelName, error_message



    def load_conversation(self,conversation_file):
        """
        Load the conversation history from a JSON file.
        Args: file_path (str): The path to the file where the history is saved.
        Returns: list: The list of ChatMessage objects loaded from the file.
        """
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]

        with open(conversation_file, 'r') as file:
            history = json.load(file)

        # Update the history with the loaded data
        self.conversation_history = []
        for message in history:
            self.conversation_history.append(ChatMessage(role=message["role"], content=message["content"]))

    def print_conversation(self,file_path):
        os.system("cls")
        self.load_conversation(file_path)
        Tools.print_colored(f"Conversation history Start: {self.timestamp}","black", "green")
        print("\n")
        for entry in self.conversation_history:
            if entry.role == 'user':
                Tools.print_colored("Your question:","black", "green")
                print(entry.content)
            elif entry.role == 'assistant':
                Tools.print_colored(f"AI answer:", "blue", "white")
                if LLMBase.USE_MARKDOWN:
                    console =Console()
                    md = Markdown(entry.content) # '  \n' two spaces and \n means carriage return
                    console.print(md)
                else:
                    print(entry.content) # normal print where '\n' means carriage return  
        Tools.print_colored(f"\nConversation history ended: {self.timestamp}","black", "green")                              
        
