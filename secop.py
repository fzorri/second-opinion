import os
from history import History
import importlib
from tools import Tools
import json
import config

# Optionally let's add markdown support
from rich.console import Console
from rich.markdown import Markdown

USE_MARKDOWN = True
MODEL_COLUMN_WIDTH = 38
MODEL_PATH = 'llm_classes'
AUTOCHECK_TEST="Round the pi number to the 4th decimal place.Answer in the following format 'Pi rounded is ...'"
AUTOCHECK_ANSWER="3.141"
HISTORY_PATH = 'models'
VERSION = '1.7.5'

#Get the list of classes dynamically
def load_classes_from_folder(folder_path, include_classes=None):
    if include_classes is None:
        include_classes = []
    classes = {}
    for file_name in os.listdir(folder_path):
        if not file_name.endswith('.py'): #exclude non .py files
            continue
        if file_name.startswith('__'): #exclude __init__.py (if there is one)
            continue
        module_name = file_name[:-3]  # remove the .py extension
        module = importlib.import_module(folder_path  + '.' + module_name)
        for attr_name in dir(module):
            if not any(
                attr_name.endswith(include[1:]) if include.startswith('*') else attr_name == include
                for include in include_classes
            ):
                continue  # skip the class if it ends with any of the excluded patterns or is exactly the excluded  name
            attr = getattr(module, attr_name)
            if isinstance(attr, type):  # check if the attribute is a class
                classes[attr_name] = attr
    return classes

#set proxy if is needed
def check_proxy():
     proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']
     for var in proxy_vars:
         if os.getenv(var):
             # Set the HTTP and HTTPS proxy environment variables
            os.environ['HTTP_PROXY'] = 'http://proxysis:8080'
            os.environ['HTTPS_PROXY'] = 'http://proxysis:8080'
            return True
     return False

"""
autocheck. Checks if the models are ready to be used
In order to check it the LLM has to answer a very simple question and we only check the answer partially
If the answer is incorrect or there is an error, a FAIL is shown. Otherwise OK is shown
V2: disabled options (ENABLED=false) are ignored 
"""

def autocheck():
    print("Autocheck. Checking models...(WARNING: some models could take a while if there is an error)")
    #Load classes dinamically, In short, load classes with _LLM suffix
    classes = load_classes_from_folder(MODEL_PATH, ['*_LLM'] )

    #Iterate over every model
    models_name=[]
    for i,c in enumerate(classes, start=1):
        try:
            name = c[:-4] + "_CFG" #get rid of the _LLM suffix and add the _CFG suffix, to obtain the configuration class dictionary name
            cfg = getattr(config,name,None) # look for the configuration class in the config.py file. 
            if cfg:
                model_name = cfg.get("MODEL_NAME") #list model name for every class. This trick avoid instancing the classes only to see the description.
                enabled = cfg.get("ENABLED")       #check if enabled in order to test it. By default all models are enabled unless explicitly disabled
                enabled = (enabled is None) or bool(enabled) #some type juggling here...
                enabled_reason = str(cfg.get("ENABLED_REASON")) or "(no reason)"

                #Select and instantiate class model
                if enabled:
                    selected_model = list(classes.values())[i - 1]
                    llm = selected_model()
                    content =AUTOCHECK_TEST
                    mname,response = llm.get_response(content)
                    pi_found=response.find(AUTOCHECK_ANSWER)
                    model_name=model_name.ljust(MODEL_COLUMN_WIDTH) #justify name to the right in order to get a nice table
                    if pi_found>0:
                        result=Tools.return_string_colored(f"OK!!", "white", "green")
                        print(f"{str(i).zfill(2)}: {model_name} : ", result)
                    else:
                        result=Tools.return_string_colored(f"FAIL", "white", "red")
                        print(f"{str(i).zfill(2)}: {model_name} : ", result)
                        print(response)
                else:
                    print("Skipping", model_name, "because", enabled_reason)
            else:
                print(f"No configuration found with the name {cfg},{name}")
        except KeyboardInterrupt: # Handle Ctrl+C (KeyboardInterrupt) to exit gracefully
            print("\nAutocheck process interrupted. Exiting...")
            return ""                
def main2():
    check_proxy()
    # Reads multiple lines from command line, returns entire text in context string.
    print("***************************************************")
    print("* Second Opinion: A simple chatbot for AI models  *")
    print(f"* Version {VERSION}                                   *")
    if USE_MARKDOWN:
        print("* Markdown support: ON                            *")
    else:
        print("* Markdown support: OFF                          *")
    print("***************************************************")
    print()

    #Load classes dinamically, In short, load classes with _LLM suffix
    classes = load_classes_from_folder(MODEL_PATH, ['*_LLM'] )

    #Enumerate the classes and list them in the console with their number, so we can select a class easily
    # VERY IMPORTANT: Every class configuration has the same suffix style, but ending in _CFG.
    while True: 
        models_name=[]
        models_folder=[]
        history=[]
        for i,c in enumerate(classes, start=1):
            name = c[:-4] + "_CFG" #get rid of the _LLM suffix and add the _CFG suffix, to obtain the configuration class dictionary name
            cfg = getattr(config,name,None) # look for the configuration class in the config.py file. 
            if cfg:
                model_name = cfg.get("MODEL_NAME") #list model name for every class. This trick avoid instancing the classes only to see the description.
                folder = cfg.get("MODEL_FOLDER")
                enabled = cfg.get("ENABLED") # Check if the model is enabled, absence means enabled
                enabled = (enabled is None) or bool(enabled) #some type juggling here...
                enabled_reason=str(cfg.get("ENABLED_REASON"))
                if enabled_reason is None:
                    enabled_reason = "(no reason)"
                #compose the model name and find out if it is enabled.
                if not enabled:
                    model_name = model_name.ljust(MODEL_COLUMN_WIDTH) + " " + Tools.return_string_colored("DISABLED","white","red") + " (" + enabled_reason + ")"
                models_name.append(model_name)
                models_folder.append(folder)
                print(f"{str(i).zfill(2)}: {model_name}") #format the number with 2 digits.
            else:
                print(f"No configuration found with the name {cfg}")
        print ("\nCOMMANDS\nA: Autocheck: test if all models are working properly")    
        try:
            #Allow to choose the model
            while True:
                try:
                    choice = input("Select A, Model# or 0 to abort:")
                    #check if autocheck is required
                    if choice.upper() == "A":
                        autocheck()
                        continue
                    choice_num = int(choice)
                    if choice_num == 0:
                        return ""
                    if 1 <= choice_num <= len(classes):
                        break
                    else:
                        print("Invalid choice")
                        continue
                except ValueError as e: #check if invalid value is added
                        print(f"Invalid choice: {e.args[0]}")
                        continue
            
            #Pick the appropriate class and instantiate it
            selected_model = list(classes.values())[choice_num - 1]
            selected_folder = models_folder[choice_num-1] #get the folder where the conversation is stored.
            
            print("\n")
            Tools.print_colored("Starting conversation with " + models_name[choice_num-1] ,"black", "green")
        except KeyboardInterrupt: # Handle Ctrl+C (KeyboardInterrupt) to exit gracefully
            print("\nChoice selection aborted... interrupted. Exiting...")
            return ""

#Test if everything works as expected.  
        while True:
            choice=input("Press ? to see previous conversations, or Enter for new conversation")
            if choice=="?":
                history = History(selected_folder)
                conversation = history.select_file()
                if conversation is None:
                    continue
                #history.print_conversation(conversation)
                llm = selected_model()
                llm.print_conversation(conversation)
                break
            else:
                llm = selected_model()
                break
            
        #Start the conversation        
        while True:
            try:
                Tools.print_colored("Enter your question, Ctrl-Enter+Enter to end input, Ctl-C to return to the menu","black", "green")
                content = Tools.getInput()
                model_name, response = llm.get_response(content)
                Tools.print_colored(f"{model_name} answer:", "blue", "white")
                if USE_MARKDOWN:
                    console =Console()
                    md = Markdown(response) # '  \n' two spaces and \n means carriage return
                    console.print(md)
                else:
                    print(response) # normal print where '\n' means carriage return
            except KeyboardInterrupt: # Handle Ctrl+C (KeyboardInterrupt) to exit gracefully
                print("\nReturning to the menu...\n\n")
                break
"""
Retrieves conversation history for a LLM model
Beta
"""

def conversation_history(models_name):
    return
"""
This part should do the following:
- Bassed on the model selected, go to models folder, retrieves the list 
of conversations and make a simple way of displaying them and selecting one.
- Once selected, history and date is retrieved and returned to the main program.
This will be used to initialize the proper LLM with conversation /date.
Additional conversation will be saved in the same conversation file.
"""     


if __name__ == "__main__":
    main2()


# Nuevas mejoras (spanish/english):
# TODO - Make sure good error control when running out of credits. 
# TODO - upload to Github
# TODO - Summarize video of the development
# TODO - Add more classes for Google for example
# TODO - Add more classes for Hugging Face and Endpoints 
# TODO - unit tests right now. Urgently.
