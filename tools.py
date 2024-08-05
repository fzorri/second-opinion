import os
import json
from mistralai.models.chat_completion import ChatMessage as MChatMessage
from octoai.text_gen import ChatMessage as OChatMessage
from pynput.keyboard import Key, Listener

class Tools:
    # print in the command line with a colored background and text
    # Example usage
    #print_colored("Hello, World!", "red", "white")
    #print_colored("This is a warning!", "yellow", "black")
    #print_colored("Success message", "green", "black")

    def print_colored(text, color, background):
        print(Tools.return_string_colored(text,color,background))

    def return_string_colored(text,color,background):
        color_codes = {'black': '30','red': '31','green': '32','yellow': '33','blue': '34','magenta': '35','cyan': '36', 'white': '37'    }
        background_codes = { 'black': '40','red': '41', 'green': '42', 'yellow': '43','blue': '44', 'magenta': '45', 'cyan': '46', 'white': '47' }
        color_code = color_codes.get(color.lower(), '37')  # Default to white if color not found
        background_code = background_codes.get(background.lower(), '40')  # Default to black if background not found
        return f"\033[{color_code};{background_code}m{text}\033[0m"

    # read multiples lines directly from command line.

    def getInput():
        lines = []
        try:
            while True:
                line = input()
                if line.upper()=="END":
                    print("\n(End) Processing...") #input is interruptible if we enter end
                    break
                lines.append(line)  # Strip newline from non-empty lines

        except KeyboardInterrupt : # Handle Ctrl+C (KeyboardInterrupt) to exit gracefully
            print("\nCtl-C detected. Processing...") #input is INTERRUPTIBLE with Control-Z
            raise KeyboardInterrupt

        except EOFError:
            print("\nCtl-Z detected. Processing...") #input is INTERRUPTIBLE with Control-Z but it does not work for Mac.
            raise KeyboardInterrupt

        answer=""
        for line in lines:
            answer = answer + line + "\n"
        return answer

    @staticmethod
    def chat_message_encoder(obj):
        """
        Custom JSON encoder for the ChatMessage object.
        """
        if isinstance(obj, (MChatMessage, OChatMessage)):
            return {
                "role": obj.role,
                "content": obj.content
            }
        return json.JSONEncoder().default(obj)

    @staticmethod
    def save_conversation(conversation_history,folder,timestamp,encoder = None):
        """
        Save the conversation history to a JSON file.
        """
        # Save the conversation history to a file in the specific folder completely.
        os.makedirs(folder, exist_ok=True)  # Create the directory if it doesn't exist
        filename = os.path.join(folder, f"conversation_history_{timestamp}.json")
        if encoder is None:
            with open(filename, "w") as file:
                json.dump(conversation_history, file, indent=4)         
        else:
            with open(filename, "w") as file:
                json.dump(conversation_history, file, indent=4,default=encoder)         

