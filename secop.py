import os
import importlib
import sys
from halo import Halo
from rich.console import Console
from rich.markdown import Markdown
sys.path.append(os.path.dirname(__file__))
from history import History
from tools import Tools
import json
from config import MODELS_CONFIGURATION

MODEL_COLUMN_WIDTH = 38
MODEL_PATH = 'llm_classes'
AUTOCHECK_TEST="Round the pi number to the 4th decimal place.Answer in the following format 'Pi rounded is ...'"
AUTOCHECK_ANSWER="3.141"
HISTORY_PATH = 'models'
VERSION = '1.7.5'
REASONING_COLOR = 'gray'  # Color for reasoning text (subtle gray)

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
    
    loaded_llms = []
    for provider_name, provider_data in MODELS_CONFIGURATION.get("providers", {}).items():
        provider_class_name = provider_data.get("class")
        module_name = provider_data.get("module")
        if provider_class_name and module_name:
            try:
                module = importlib.import_module(module_name)
                llm_class = getattr(module, provider_class_name)
                
                for model_config in provider_data.get("models", []):
                    model_config["API_KEY"] = provider_data.get("API_KEY")
                    if model_config.get("enabled", True):
                        llm_instance = llm_class(model_config)
                        loaded_llms.append(llm_instance)
                    else:
                        print(f"Skipping disabled model: {model_config.get('model_name')} because {model_config.get('enabled_reason', '(no reason)')}")
            except Exception as e:
                print(f"Error loading provider {provider_name}: {e}")
                
    if not loaded_llms:
        print("No enabled models found for autocheck.")
        return

    for i, llm in enumerate(loaded_llms, start=1):
        try:
            model_name = llm.model_name.ljust(MODEL_COLUMN_WIDTH)
            content = AUTOCHECK_TEST
            mname, response = llm.get_response(content)
            pi_found = response.find(AUTOCHECK_ANSWER)
            
            if pi_found > -1: # Use -1 instead of 0 to check if substring is found anywhere
                result = Tools.return_string_colored("OK!!", "white", "green")
                print(f"{str(i).zfill(2)}: {model_name} : ", result)
            else:
                result = Tools.return_string_colored("FAIL", "white", "red")
                print(f"{str(i).zfill(2)}: {model_name} : ", result)
                print(f"Response: {response}")
        except KeyboardInterrupt:
            print("\nAutocheck process interrupted. Exiting...")
            return ""
        except Exception as e:
            model_name = llm.model_name.ljust(MODEL_COLUMN_WIDTH)
            result = Tools.return_string_colored("ERROR", "white", "red")
            print(f"{str(i).zfill(2)}: {model_name} : ", result)
            print(f"Error details: {e}")
                
def main2():
    check_proxy()
    print("***************************************************")
    print("* Second Opinion: A simple chatbot for AI models  *")
    print(f"* Version {VERSION}                                   *")
    if Tools.USE_MARKDOWN:
        print("* Markdown support: ON                            *")
    else:
        print("* Markdown support: OFF                          *")
    print("***************************************************")
    print()

    while True: 
        all_models_info = []
        # This first loop just gathers model configurations and class info without instantiating them.
        for provider_name, provider_data in MODELS_CONFIGURATION.get("providers", {}).items():
            provider_class_name = provider_data.get("class")
            module_name = provider_data.get("module")
            if not (provider_class_name and module_name):
                continue
            
            try:
                module = importlib.import_module(module_name)
                llm_class = getattr(module, provider_class_name)
                
                for model_config in provider_data.get("models", []):
                    model_config["API_KEY"] = provider_data.get("API_KEY")
                    
                    model_info = {
                        "is_enabled": model_config.get("enabled", True),
                        "llm_class": llm_class,
                        "model_config": model_config
                    }
                    
                    display_name = model_config.get('model_name', 'Unknown Model').ljust(MODEL_COLUMN_WIDTH)

                    if model_info["is_enabled"]:
                        max_tokens_info = ""
                        if model_config.get("max_tokens") is not None:
                            max_tokens_info = Tools.return_string_colored(str(model_config.get("max_tokens")), "white", "blue")
                            max_tokens_info = f" ({max_tokens_info} tokens)"
                        display_name += max_tokens_info
                    else:
                        reason = model_config.get('enabled_reason', '(no reason)')
                        display_name += f" {Tools.return_string_colored('DISABLED','white','red')} ({reason})"

                    model_info["display_name"] = display_name
                    all_models_info.append(model_info)

            except Exception as e:
                print(f"Error loading model configurations for provider {provider_name}: {e}")

        if not all_models_info:
            print("No models configured. Please check models.yaml and your .env file.")
            return

        for i, model_info in enumerate(all_models_info, start=1):
            print(f"{str(i).zfill(2)}: {model_info['display_name']}")
        
        print ("\nCOMMANDS\nA: Autocheck: test if all models are working properly")    
        try:
            while True:
                try:
                    choice = input("Select A, Model# or 0 to abort:")
                    if choice.upper() == "A":
                        autocheck()
                        continue
                    choice_num = int(choice)
                    if choice_num == 0:
                        return ""
                    if 1 <= choice_num <= len(all_models_info):
                        break
                    else:
                        print("Invalid choice")
                        continue
                except ValueError as e:
                        print(f"Invalid choice: {e.args[0]}")
                        continue
            
            selected_model_info = all_models_info[choice_num - 1]
            if not selected_model_info["is_enabled"]:
                print("The selected model is disabled. Please choose another one.\n")
                continue
            
            # LAZY LOADING: Instantiate the LLM class only AFTER the user has made a valid choice.
            spinner = Halo(text='Initializing model...', spinner='dots')
            with spinner:
                llm_class = selected_model_info['llm_class']
                model_config = selected_model_info['model_config']
                selected_llm = llm_class(model_config)
            
            print("\n")
            toPrint =f"Chat with {selected_llm.model_name} - Type 'end' or '*' in a new line to finalize, Ctl-C to return to the menu"
            Tools.print_colored(toPrint ,"black", "green")

        except KeyboardInterrupt:
            print("\nChoice selection aborted... interrupted. Exiting...")
            return ""
 
        while True:
            choice=input("Press ? to see previous conversations, or Enter for new conversation")
            if choice=="?":
                history = History(selected_llm.model_folder)
                conversation_file = history.select_file()
                if conversation_file is None:
                    continue
                selected_llm.load_conversation(conversation_file)
                Tools.print_conversation(conversation_file, selected_llm.model_name)
                break
            else:
                selected_llm.conversation_history = []
                break
            
        while True:
            try:
                Tools.print_colored( selected_llm.model_name+" - Enter your question, type 'end' in a separate line to end input, Ctl-C to return to the menu","black", "green")
                content = Tools.getInput()
                spinner = Halo(text=f'Waiting for {selected_llm.model_name}...', spinner='dots')
                with spinner:
                    model_name, response = selected_llm.get_response(content)
        
                Tools.print_colored(f"{model_name} answer:", "blue", "white")
                
                if Tools.USE_MARKDOWN:
                    console =Console()
                    md = Markdown(response)
                    console.print(md)
                else:
                    print(response)
            except KeyboardInterrupt:
                print("\nReturning to the menu...\n\n")
                break

if __name__ == "__main__":
    main2()


