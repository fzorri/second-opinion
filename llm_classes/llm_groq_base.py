# generic class for Groq models.
# https://console.groq.com/docs/text-chat
# pip install groq

import os
import json
from groq import Groq
from llm_classes.llm_base import LLMBase
from datetime import datetime
from tools import Tools
from rich.console import Console
from rich.markdown import Markdown

class Groq_Base(LLMBase):
    def __init__(self,config):
        self.api_key     = config["API_KEY"]      #api_key
        self.modelName   = config["MODEL_NAME"]   #model_name
        self.model       = config["MODEL_ID"]     #model_id
        self.modelFolder = config["MODEL_FOLDER"] #model_folder
        self.conversation_history = []
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
        super().__init__()  # Call the base class constructor

    #this is going to return self.client= MistralClient initialized
    def initialize_client(self):
        return Groq(api_key=self.api_key)        

    def send_message(self, text):
        # Append the user's message to the conversation history
        self.conversation_history.append({"role": "user", "content": text})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history
        )
        
         # Append the model's response to the conversation history
        self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
        Tools.save_conversation(self.conversation_history,self.modelFolder,
                                self.timestamp)

        return self.modelName, response.choices[0].message.content
    
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
        


