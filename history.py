#Class for deal with history recovery for LLM. Attempt 1
# 20240626 - History presented in reversed order since many times we need
# to recover the latest conversation(s)
import os
import re
import importlib
import shutil
from datetime import datetime
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
                formatted_time = f"{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"  # HH:MM:SS
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
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                messages = data["messages"] if isinstance(data, dict) else data
                if isinstance(messages, list) and messages:
                    combined_content = ""
                    attach_count = 0
                    for item in messages:
                        content = item.get('content', '')
                        if isinstance(content, list):
                            content = ' '.join(str(p) for p in content)
                        attach_count += len(re.findall(r'\[Ref: [^\]]+\]', str(content)))
                        content = str(content).replace('\r', '').replace('\n', '')
                        if len(combined_content) + len(content) + 1 <= self.CONTENT_LENGTH_LIMIT:
                            if combined_content:
                                combined_content += '|'
                            combined_content += content
                        else:
                            remaining_space = self.CONTENT_LENGTH_LIMIT - len(combined_content)
                            if remaining_space > 0:
                                combined_content += '|' + content[:remaining_space]
                            break
                    prefix = f"({attach_count} attachments) " if attach_count > 0 else ""
                    return prefix + combined_content
                else:
                    return "  Error: Data is empty."
        except json.JSONDecodeError:
            return "  Error: Invalid JSON format."
        except Exception as e:
            return f"  Error: {e}"

# WATCHOUT: There is no turning back!
    def delete_conversation(self, filepath):
        try:
            # Read JSON to find attachment references
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                messages = data["messages"] if isinstance(data, dict) else data
                # Delete referenced attachment files
                attach_dir = os.path.join(os.path.dirname(filepath), "attachments")
                for msg in messages:
                    content = msg.get('content', '')
                    for ref in re.findall(r'\[Ref: ([^\]]+)\]', str(content)):
                        ref_path = os.path.join(attach_dir, ref)
                        if os.path.exists(ref_path):
                            os.remove(ref_path)
                            print(f"Deleted attachment: {ref}")
                # Delete attachments folder if empty
                if os.path.exists(attach_dir) and not os.listdir(attach_dir):
                    os.rmdir(attach_dir)
            except:
                pass
            # Delete JSON file
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
        all_messages = []
        total_in = 0
        total_out = 0
        total_tokens = 0
        # Target attachment directory (from first file)
        first_dir = os.path.dirname(files[0])
        target_attach_dir = os.path.join(first_dir, "attachments")

        for file in files:
            print(f"merging {file} ...")
            with open(file, 'r') as f:
                data = json.load(f)
                messages = data["messages"] if isinstance(data, dict) else data
                all_messages.extend(messages)
                if isinstance(data, dict):
                    m = data.get("metadata", {})
                    total_in += m.get("total_input_tokens", 0)
                    total_out += m.get("total_output_tokens", 0)
                    total_tokens += m.get("total_tokens", 0)
            # Merge attachment files
            src_attach_dir = os.path.join(os.path.dirname(file), "attachments")
            if os.path.exists(src_attach_dir):
                os.makedirs(target_attach_dir, exist_ok=True)
                for att_file in os.listdir(src_attach_dir):
                    src = os.path.join(src_attach_dir, att_file)
                    dst = os.path.join(target_attach_dir, att_file)
                    if os.path.exists(dst):
                        # Handle filename conflict
                        base, ext = os.path.splitext(att_file)
                        dst = os.path.join(target_attach_dir, f"{base}_{datetime.now().strftime('%H%M%S')}{ext}")
                    shutil.copy2(src, dst)

        merged = {
            "messages": all_messages,
            "metadata": {
                "conversation_name": "",
                "last_updated": datetime.now().strftime("%Y%m%d-%H%M%S"),
                "total_input_tokens": total_in,
                "total_output_tokens": total_out,
                "total_tokens": total_tokens
            }
        }

        first_file = files[0]
        with open(first_file, 'w') as f:
            json.dump(merged, f, indent=4)

        for file in files[1:]:
            self.delete_conversation(file)
        print(f"Done! All files have been merged to {first_file}.")

    
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
                    choice = input("Options: (V)iew, (S)elect, (E)xport to Markdown or (D)elete conversation (0 to abort):")
                    #Assembly the complete folder to access the conversation
                    if choice == "Delete": #Need to type exactly 'Delete' to avoid mistakes.
                        self.delete_conversation(filepath)
                    elif choice.upper() == "V":
                        self.print_conversation(filepath)
                    elif choice.upper() == "E":
                        self.export_to_markdown(filepath)
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

        messages = data["messages"] if isinstance(data, dict) else data
        model_folder = os.path.dirname(file_path)

        for entry in messages:
            role = entry.get('role', '')
            content = entry.get('content', '')
            if isinstance(content, list):
                content = ' '.join(str(p) for p in content)
            # Resolve [Ref: ...] markers for display
            content = self._resolve_refs_for_display(content, model_folder)
            if role == 'user':
                Tools.print_colored("Your question:","black", "green")
                print(content)
            elif role in ('assistant', 'model'):
                Tools.print_colored(f"AI answer:", "blue", "white")
                if USE_MARKDOWN:
                    console =Console()
                    md = Markdown(content)
                    console.print(md)
                else:
                    print(content)

    def _resolve_refs_for_display(self, text, model_folder):
        def replace_ref(match):
            ref_name = match.group(1)
            attach_path = os.path.join(model_folder, "attachments", ref_name)
            if not os.path.exists(attach_path):
                return f"[Attachment missing: {ref_name}]"
            try:
                with open(attach_path, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
            except:
                return f"[Error reading: {ref_name}]"
        return re.sub(r'\[Ref: ([^\]]+)\]', replace_ref, text)

    def export_to_markdown(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            messages = data["messages"] if isinstance(data, dict) else data
            model_folder = os.path.dirname(file_path)

            markdown_content = []
            for entry in messages:
                role = entry.get('role', '')
                content = entry.get('content', '')
                if isinstance(content, list):
                    content = ' '.join(str(p) for p in content)
                # Resolve [Ref: ...] markers for export
                content = self._resolve_refs_for_display(content, model_folder)
                if role == 'user':
                    markdown_content.append(f"**User:**\n{content}\n")
                elif role in ('assistant', 'model'):
                    markdown_content.append(f"**Assistant:**\n{content}\n")

            markdown_output = "\n".join(markdown_content)
            output_filepath = os.path.splitext(file_path)[0] + '.md'

            with open(output_filepath, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_output)

            print(f"Successfully exported conversation to {output_filepath}")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


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
