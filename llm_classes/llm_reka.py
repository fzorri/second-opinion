# prerequisite: pip install reka-api

import os
import json
from reka.client import Reka
from llm_classes.llm_base import LLMBase
from config import Reka_CFG
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

class Reka_LLM(LLMBase):
    def __init__(self):
        config= Reka_CFG
        self.api_key     = config["API_KEY"]
        self.modelName   = config["MODEL_NAME"]
        self.model       = config["MODEL_ID"] #at the moment, it does not have a model
        self.modelFolder = config["MODEL_FOLDER"]
        self.conversation_history=[]
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        super().__init__()  # Call the base class constructor

    #this is going to return self.client= MistralClient initialized
    def initialize_client(self):
        #reka.API_KEY = self.api_key
        #return reka
        return Reka(api_key=self.api_key)

    def send_message(self, text):
        #try:
        #20240521: Fix. The append has to be done AFTER the chat method. If we add before the chat method,
        # the method will fire an error due misaligned human vs. model intercalation.
        # Pass the conversation history to reka.chat() 

        # Append the user's message to the conversation history
        self.conversation_history.append({"role": "user", "content": text})

        response = self.client.chat.create(messages=self.conversation_history,
                                           model=self.model)

        # Append the model's response to the conversation history
        #self.conversation_history.append({"role": "assistant", "content": response["text"]})
        self.conversation_history.append({"role": "assistant", "content": response.responses[0].message.content})

        Tools.save_conversation(self.conversation_history, self.modelFolder, self.timestamp)

        return self.modelName, response.responses[0].message.content
        #except Exception as e:
        #    error_message = "An error happened processing the request:  \n" + str(e)
        #    return self.modelName, error_message
            

            
    
    def load_conversation(self, conversation_file):
        fname= os.path.basename(conversation_file)
        self.timestamp = fname[len('conversation_history_'):-5]
        with open(conversation_file, 'r') as ch:
            self.conversation_history=json.load(ch)

    def print_conversation(self,file_path):
        os.system("cls")
        self.load_conversation(file_path)
        Tools.print_colored(f"Conversation history Start: {self.timestamp}","black", "green")
        print("\n")
        for entry in self.conversation_history:
            if entry['role'] == 'user':
                Tools.print_colored("Your question:","black", "green")
                print(entry['content'])
            elif entry['role'] == 'assistant':
                Tools.print_colored(f"AI answer:", "blue", "white")
                if LLMBase.USE_MARKDOWN:
                    console =Console()
                    md = Markdown(entry['content']) # '  \n' two spaces and \n means carriage return
                    console.print(md)
                else:
                    print(entry['content']) # normal print where '\n' means carriage return  
        Tools.print_colored(f"\nConversation history ended: {self.timestamp}","black", "green")                              
