import os
import json
from mistralai.models.chat_completion import ChatMessage as MChatMessage
from octoai.text_gen import ChatMessage as OChatMessage

# Imports for the modern, editable multi-line input
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

# Optionally let's add markdown support
from rich.console import Console
from rich.markdown import Markdown


class Tools:
    DEFAULT_ANSWER_TOKENS = 4096
    DEFAULT_TEMPERATURE   = 0.1
    USE_MARKDOWN = True

    @staticmethod
    def print_colored(text, color, background):
        print(Tools.return_string_colored(text,color,background))

    @staticmethod
    def return_string_colored(text,color,background):
        color_codes = {'black': '30','red': '31','green': '32','yellow': '33','blue': '34','magenta': '35','cyan': '36', 'white': '37'    }
        background_codes = { 'black': '40','red': '41', 'green': '42', 'yellow': '43','blue': '44', 'magenta': '45', 'cyan': '46', 'white': '47' }
        color_code = color_codes.get(color.lower(), '37')
        background_code = background_codes.get(background.lower(), '40')
        return f"\033[{color_code};{background_code}m{text}\033[0m"

    @staticmethod
    def getInput():
        """
        Reads multiple lines from the console using prompt_toolkit, allowing full editing.
        This version uses the correct key bindings based on official documentation.
        
        - Pressing Ctrl+J (the code for Ctrl+Enter on most terminals) will submit.
        - Pressing Ctrl+D is a universal fallback for submission.
        - Pressing the normal Enter key will add a new line.
        - Pressing Ctrl+C will abort the input.
        """
        bindings = KeyBindings()

        # Define a single handler function for submitting the input.
        def _submit_handler(event):
            """Exits the prompt, returning the buffer's content."""
            event.app.exit(result=event.app.current_buffer.text)

        # Bind the correct keys to the submit handler.
        # We use Keys.ControlJ because this is the key code most terminals
        # send for Ctrl+Enter.
        bindings.add(Keys.ControlJ)(_submit_handler)

        # We keep Keys.ControlD as a reliable, universal fallback.
        bindings.add(Keys.ControlD)(_submit_handler)
        
        #
        # --- IMPORTANT ---
        # We DO NOT bind Keys.ControlM (Enter). By not binding it, we allow
        # prompt_toolkit's default behavior for multi-line input, which is to
        # insert a newline. This is what allows you to type multiple lines.
        #
        
        try:
            # Updated toolbar to reflect the working keys.
            toolbar_text = 'Press [Ctrl+Enter] (or Ctrl+J) or [Ctrl+D] to submit | [Ctrl+C] to abort'

            text_block = prompt(
                '> ',
                multiline=True,
                key_bindings=bindings,
                bottom_toolbar=toolbar_text,
                prompt_continuation='  ' 
            )
            print("\n(End) Processing...")
            return text_block

        except KeyboardInterrupt:
            print("\nCtl-C detected. Returning to the menu...")
            raise KeyboardInterrupt
        except EOFError:
            print("\nInput ended. Processing...")
            return ""

    @staticmethod
    def chat_message_encoder(obj):
        if isinstance(obj, (MChatMessage, OChatMessage)):
            return {
                "role": obj.role,
                "content": obj.content
            }
        return json.JSONEncoder().default(obj)

    @staticmethod
    def save_conversation(conversation_history,folder,timestamp,encoder = None):
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"conversation_history_{timestamp}.json")
        if encoder is None:
            with open(filename, "w") as file:
                json.dump(conversation_history, file, indent=4)         
        else:
            with open(filename, "w") as file:
                json.dump(conversation_history, file, indent=4,default=encoder)
    
    @staticmethod
    def print_conversation(conversation_file, llm_model_name):
        os.system("cls" if os.name == "nt" else "clear")
        
        fname= os.path.basename(conversation_file)
        timestamp = fname[len('conversation_history_'):-5]

        with open(conversation_file, 'r') as ch:
            conversation_history = json.load(ch)

        Tools.print_colored(f"Conversation history Start: {timestamp} with {llm_model_name}","black", "green")
        print("\n")
        for entry in conversation_history:
            role = entry['role']
            content = entry['content']
            
            if role == 'user':
                Tools.print_colored("Your question:","black", "green")
                print(content)
            elif role == 'assistant' or role == 'model': # Google uses 'model' role
                Tools.print_colored(f"{llm_model_name} answer:", "blue", "white")
                if Tools.USE_MARKDOWN:
                    console = Console()
                    md = Markdown(content)
                    console.print(md)
                else:
                    print(content)
        Tools.print_colored(f"\nConversation history ended: {timestamp}","black", "green")