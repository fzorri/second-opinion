# invoking mistral directly
# pip install mistralai

import os
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from mistralai.exceptions import MistralAPIException
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

#20240531 - Exceptional case of changing endpoint:
#few days ago Codestral appeared. When I tried to integrate it failed.
# The issue is that it needs different endpoints in order to work.
# So mistral as exception uses an endpoint

class Mistral_base(LLMBase):
    def __init__(self, config):
        self.api_key     = config["API_KEY"]      #api_key
        self.modelName   = config["MODEL_NAME"]   #model_name 
        self.model       = config["MODEL_ID"]     #model_id
        self.modelFolder = config["MODEL_FOLDER"] #model_folder 
        self.endpoint    = config["MODEL_ENDPOINT"] #model_endpoint
        self.conversation_history=[]
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")


        super().__init__()  # Call the base class constructor        

    #this is going to return self.client= MistralClient initialized
    def initialize_client(self):
        #Special case for Codestral
        if self.endpoint != "":
            return MistralClient(api_key=self.api_key, endpoint=self.endpoint)
        else:
            return MistralClient(api_key=self.api_key)

    def send_message(self, text):
        # Add the new user message to the conversation history
        self.conversation_history.append(ChatMessage(role="user", content=text))
        try:
            response = self.client.chat(model=self.model,
                                    messages=self.conversation_history)

        # Add the assistant's response to the conversation history
            self.conversation_history.append(ChatMessage(role="assistant", content=response.choices[0].message.content))
            Tools.save_conversation(self.conversation_history,self.modelFolder,self.timestamp, Tools.chat_message_encoder)
            return self.modelName, response.choices[0].message.content
        except MistralAPIException as e:
            error_message = "An error happened processing the request:  \n" + str(e)
            return self.modelName, error_message
        except Exception as e:
             error_message = "An unexpected error occurred:  \n" + str(e)
             return self.modelName, error_message

    """
    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=json.load(ch)
    """

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
        

