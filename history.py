#Class for deal with history recovery for LLM. Attempt 1
# 20240626 - History presented in reversed order since many times we need
# to recover the latest conversation(s)
import os
import importlib
from tools import Tools
import json
import config

# Optionally let's add markdown support
from rich.console import Console
from rich.markdown import Markdown

USE_MARKDOWN = True
PAGE_SIZE  = 22
CONTENT_LENGTH_LIMIT = 120


class History:

    # Initializer / Instance attributes
    def __init__(self, folder):
        self.folder_path = folder
     
    # Method to list .json files
    """
    List the json files in a way we can see some of data in the terminal
    """
    def list_json_files(self, page_size=PAGE_SIZE):
        if not os.path.exists(self.folder_path):
            print(f"The folder {self.folder_path} does not exist.")
            return []

        ordered_json_files = [f for f in os.listdir(self.folder_path) if f.endswith('.json')]
        json_files = sorted(ordered_json_files, reverse=True)
        if not json_files:
            print("No .json files found in the folder.")
            return []
        
        formatted_files = []
        #file format is conversation_history_YYYYMMDD-HHMMSS.json
        #this loop stripes the date and time from the filename and shows it in a simplfied way
        for file in json_files:
            if file.startswith('conversation_history_'):
                date_time_part = file[len('conversation_history_'):-5]  # Remove prefix and '.json'
                date_part, time_part = date_time_part.split('-')
                formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]}"  # YYYY-MM-DD
                formatted_time = f"{time_part[:2]}:{time_part[2:4]}:{time_part[4:]}"  # HH:MM:SS
                formatted_files.append((file, f"{formatted_date} {formatted_time}"))

        if not formatted_files:
            print("No valid conversation history files found.")
            return []

        total_files = len(formatted_files)
        print (f"Found {total_files} conversation history files. Available conversations:")
        
        #let's paginate the conversation history so we can see them all
        current_page = 0
        while current_page * page_size < total_files:
            start = current_page * page_size
            end = min(start + page_size, total_files)
            
            for idx in range(start, end):
                file, formatted_date_time = formatted_files[idx]
                content = self.peek_inside_json(os.path.join(self.folder_path, file))
                print(f"{str(idx + 1).zfill(2)}. {formatted_date_time} -> {content}\n")

            if end < total_files:
                try:
                    print("Enter to see more, Ctrl-C to stop listing")
                    input()
                except KeyboardInterrupt: # Handle Ctrl+C (KeyboardInterrupt) to exit gracefully
                    print("\nEnding list result...")
                    break
            current_page += 1

        #return list of file names
        return [file for file, _ in formatted_files]

     # Method to peek inside a json file to see in advance what could be inside of it.

    CONTENT_LENGTH_LIMIT = 100  # Define a constant for content length limit

    def peek_inside_json(self, file_path):
        """
        Check a JSON file inside, showing the first 100 characters.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if isinstance(data, list) and data:  # Check if data is a non-empty list
                    combined_content = ""
                    for item in data:
                        if isinstance(item, dict) and 'content' in item:
                            content = item['content'].replace('\r', '').replace('\n', '')  # remove carriage returns and newlines
                            if len(combined_content) + len(content) + 1 <= self.CONTENT_LENGTH_LIMIT:
                                if combined_content:
                                    combined_content += '|'
                                combined_content += content
                            else:
                                remaining_space = self.CONTENT_LENGTH_LIMIT - len(combined_content)
                                if remaining_space > 0:
                                    combined_content += '|' + content[:remaining_space]
                                break
                    return combined_content
                else:
                    return "  Error: Data is not a list or is empty."
        except json.JSONDecodeError:
            return "  Error: Invalid JSON format."
        except Exception as e:
            return f"  Error: {e}"

# WATCHOUT: There is no turning back!
    def delete_conversation(self, filepath):
        # Placeholder method to delete conversations
        try:
            os.remove(filepath)
            print(f"File {filepath} has been deleted.")
        except FileNotFoundError:
            print(f"File {filepath} does not exist.")
        except PermissionError:
            print(f"You do not have permission to delete the file {filepath}.")
        except Exception as e:
            print(f"An error occurred: {e}")

    """
    Delete multiple conversations
    """
    def delete_conversations(self, files):
        # Placeholder method to delete conversations
        for file in files:
            self.delete_conversation(file)

   
    """
    Merge the conversations in one only conversations
    Warning: it deletes all the other files, keeping the latest
    """
    def merge_conversations(self, files):
        # Placeholder method to merge conversations
        merge=[]
        for file in files:
            print(f"merging {file} ..." )
            with open(file, 'r') as f:
                merge.extend(json.load(f))
        
        #get the first file in the files array
        first_file = files[0]
        #write the merged data to the first file
        with open(first_file, 'w') as f:
            json.dump(merge, f, indent=4)

        #delete the other files
        for file in files[1:]:
            self.delete_conversation(file)
        print (f"Done! All files have been merged to {first_file}.")

    
    """
    Allows to pick a conversation, and some conversation management (view it, delete it, merge it, etc.)
    """
    def select_file(self):
        json_files = self.list_json_files()
        if not json_files:
            return None

        while True:
            try:
                selection = input("Select file# or multiple file numbers separated by commas.(0 to abort)")
                if selection == '0':
                    return

                # Split the user input into a list of integers
                selected_indices = [int(num.strip()) for num in selection.split(',')]

                # Validate the selected indices
                valid_indices = [index for index in selected_indices if 1 <= index <= len(json_files)]
                # Check for invalid indices
                invalid_indices = [index for index in selected_indices if index not in valid_indices]

                if invalid_indices:
                    print("Invalid selection. Please try again.")
                    continue

                if len(valid_indices) == 1:
                    filepath= os.path.join(self.folder_path, json_files[valid_indices[0] - 1])
                    print (f"file to operate: {filepath}")
                    choice = input("Options: (V)iew, (S)elect or (Delete) conversation (0 to abort):")
                    #Assembly the complete folder to access the conversation
                    if choice == "Delete": #Need to type exactly 'Delete' to avoid mistakes.
                        self.delete_conversation(filepath)
                    elif choice.upper() == "V":
                        self.print_conversation(filepath)
                    elif choice.upper() == "S":
                        return filepath #return with a conversation to continue the dialog.
                    elif choice == "0":
                        return
                    else:
                        print("Invalid choice. Please try again.")
                        continue
                else:
                    #loop over all the files selected and put them in an array.
                    print ("Files to operate:")
                    files=[]
                    for index in valid_indices:
                        filepath= os.path.join(self.folder_path, json_files[index - 1])
                        files.append(filepath)
                        print (filepath)

                    choice = input("Options: (Merge) or (Delete) conversations (0 to abort):")
                    if choice == "Delete":
                        self.delete_conversations(files)
                    elif choice == "Merge":
                        self.merge_conversations(files)
                    elif choice == "0":
                        return
                    else:
                        print("Invalid choice. Please try again.")
                        continue
            except ValueError:
                print("Please enter valid numbers separated by commas.")

    """
    Print a simple conversation
    """
    def print_conversation(self,file_path):
        os.system("cls")
        with open(file_path, 'r') as file:
            data = json.load(file)

        for entry in data:
            if entry['role'] == 'user':
                Tools.print_colored("Your question:","black", "green")
                print(entry['content'])
            elif entry['role'] == 'assistant':
                Tools.print_colored(f"AI answer:", "blue", "white")
                if USE_MARKDOWN:
                    console =Console()
                    md = Markdown(entry['content']) # '  \n' two spaces and \n means carriage return
                    console.print(md)
                else:
                    print(entry['content']) # normal print where '\n' means carriage return


 # Example usage:
if __name__ == "__main__":
    history = History('models\deepseek-coder')
    selected_file = history.select_file()
    """
        if selected_file:
        print(f"You selected: {selected_file}")
        p =os.path.join(HISTORY_PATH,folder,selected_file)
        print (f"complete path: {p}")
        history.print_conversation(p)
    """
