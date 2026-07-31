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
from search_engine import notify_deletion

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
                file_path = os.path.join(self.folder_path, file)
                metadata = self.get_conversation_metadata(file_path)
                content = self.peek_inside_json(file_path)

                # Check if conversation has a name
                conv_name = None
                if metadata:
                    conv_name = metadata.get("conversation_name", "")
                    if conv_name:
                        conv_name = conv_name.strip()

                if conv_name:
                    # Named conversation — show name prominently with green color
                    tokens = metadata.get("total_tokens", -1) if metadata else -1
                    tokens_str = self.format_token_count(tokens)
                    line = f"★ {conv_name} | {tokens_str}"
                    colored_line = Tools.return_string_colored(line, "green", "black")
                    print(f"{str(idx + 1).zfill(2)}. {colored_line}")
                    print(f"    {formatted_date_time} -> {content}\n")
                else:
                    # Unnamed conversation — original format
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

    def get_conversation_metadata(self, file_path):
        """Extract metadata from a conversation file. Returns dict or None."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data.get("metadata", None)
                return None
        except:
            return None

    @staticmethod
    def format_token_count(tokens):
        """Format token count for display."""
        if tokens is None or tokens == -1:
            return "(no calculation yet)"
        elif tokens == 0:
            return "0 tokens"
        else:
            return f"{tokens:,} tokens"

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
            notify_deletion(filepath)
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
    Set or change the conversation_name attribute in metadata.
    If metadata is missing (old list format), creates it with tokens = -1.
    """
    def set_conversation_name(self, filepath, name):
        try:
            name = name.strip()
            if not name:
                print("Name cannot be empty.")
                return False
            if len(name) > config.MAX_CONVERSATION_NAME_LENGTH:
                print(f"Name too long. Maximum {config.MAX_CONVERSATION_NAME_LENGTH} characters.")
                return False

            with open(filepath, 'r') as f:
                data = json.load(f)

            # Convert to dict format if needed (old list format)
            if isinstance(data, list):
                data = {
                    "messages": data,
                    "metadata": {
                        "conversation_name": name,
                        "last_updated": datetime.now().strftime("%Y%m%d-%H%M%S"),
                        "total_input_tokens": -1,
                        "total_output_tokens": -1,
                        "total_tokens": -1
                    }
                }
            else:
                # Dict format — just update the name
                if "metadata" not in data:
                    data["metadata"] = {}
                data["metadata"]["conversation_name"] = name

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"✓ Conversation named: {name}")
            return True
        except Exception as e:
            print(f"Error naming conversation: {e}")
            return False

   
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
                    choice = input("Options: (V)iew, (S)elect, (E)xport, (N)ame or (D)elete conversation (0 to abort):")
                    #Assembly the complete folder to access the conversation
                    if choice == "Delete": #Need to type exactly 'Delete' to avoid mistakes.
                        self.delete_conversation(filepath)
                    elif choice.upper() == "V":
                        self.print_conversation(filepath)
                    elif choice.upper() == "E":
                        self.export_to_markdown(filepath)
                    elif choice.upper() == "S":
                        return filepath #return with a conversation to continue the dialog.
                    elif choice.upper() == "N":
                        name = input("Enter conversation name: ")
                        self.set_conversation_name(filepath, name)
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

        def replace_path(match):
            file_path = match.group(1)
            if not os.path.exists(file_path):
                return f"[Path not found: {file_path}]"
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
            except:
                return f"[Error reading: {file_path}]"

        text = re.sub(r'\[Ref: ([^\]]+)\]', replace_ref, text)
        text = re.sub(r'\[Path: ([^\]]+)\]', replace_path, text)
        return text

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

    # ============================================================
    # ORPHANED CONVERSATIONS
    # ============================================================

    @staticmethod
    def list_orphaned_folders():
        """
        Compare models/ directory with active model_folder in models.yaml.
        Return list of (folder_name, folder_path, conversation_count) for orphaned folders.
        """
        active_folders = set()
        for provider_data in config.MODELS_CONFIGURATION.get("providers", {}).values():
            for model in provider_data.get("models", []):
                folder = model.get("model_folder", "")
                if folder:
                    active_folders.add(os.path.normpath(folder))

        models_base = "models"
        orphaned = []
        if os.path.exists(models_base):
            for folder_name in os.listdir(models_base):
                folder_path = os.path.join(models_base, folder_name)
                if os.path.isdir(folder_path):
                    norm_path = os.path.normpath(folder_path)
                    if norm_path not in active_folders:
                        count = len([f for f in os.listdir(folder_path)
                                    if f.endswith('.json') and f.startswith('conversation_history_')])
                        if count > 0:
                            orphaned.append((folder_name, folder_path, count))

        return sorted(orphaned, key=lambda x: x[0])

    def select_orphaned_file(self):
        """
        Browse orphaned conversations with restricted actions: View/Export/Delete only.
        Supports multiple selection for delete (e.g., 1,3,5-8).
        """
        json_files = self.list_json_files()
        if not json_files:
            return None

        while True:
            try:
                selection = input("Select file# (comma-separated, ranges like 1-5, 0 to abort): ")
                if selection == '0':
                    return None

                # Parse selection: supports "1,3,5-8" format
                selected_indices = []
                for part in selection.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-', 1)
                        selected_indices.extend(range(int(start), int(end) + 1))
                    else:
                        selected_indices.append(int(part))

                valid_indices = [index for index in selected_indices if 1 <= index <= len(json_files)]
                invalid_indices = [index for index in selected_indices if index not in valid_indices]

                if invalid_indices:
                    print(f"Invalid selections: {invalid_indices}. Please try again.")
                    continue

                if len(valid_indices) == 1:
                    # Single selection — full options
                    filepath = os.path.join(self.folder_path, json_files[valid_indices[0] - 1])
                    choice = input("Options: (V)iew, (E)xport, (N)ame, (D)elete conversation (0 to abort): ")

                    if choice.upper() == "V":
                        self.print_conversation_readonly(filepath)
                    elif choice.upper() == "E":
                        self.export_to_markdown(filepath)
                    elif choice.upper() == "N":
                        name = input("Enter conversation name: ")
                        self.set_conversation_name(filepath, name)
                    elif choice.upper() == "D":
                        confirm = input(f"Delete {os.path.basename(filepath)}? (yes/no): ")
                        if confirm.lower() == "yes":
                            self.delete_conversation(filepath)
                            json_files = self.list_json_files()
                            if not json_files:
                                print("No more conversations in this folder.")
                                return None
                    elif choice == "0":
                        return None
                    else:
                        print("Invalid choice.")
                else:
                    # Multiple selection — delete only
                    files = []
                    for index in valid_indices:
                        filepath = os.path.join(self.folder_path, json_files[index - 1])
                        files.append(filepath)

                    print(f"\n{len(files)} conversations selected:")
                    for f in files:
                        print(f"  - {os.path.basename(f)}")

                    choice = input("\n(D)elete all selected (0 to abort): ")

                    if choice.upper() == "D":
                        confirm = input(f"Delete {len(files)} conversations? (yes/no): ")
                        if confirm.lower() == "yes":
                            for f in files:
                                self.delete_conversation(f)
                            print(f"Deleted {len(files)} conversations.")
                            json_files = self.list_json_files()
                            if not json_files:
                                print("No more conversations in this folder.")
                                return None
                    elif choice == "0":
                        return None
                    else:
                        print("Invalid choice.")

            except ValueError:
                print("Invalid input. Use numbers like: 1,3,5-8")

    def print_conversation_readonly(self, file_path):
        """
        Print conversation with [DEPRECATED] header. Read-only, no actions.
        """
        os.system("cls" if os.name == "nt" else "clear")

        fname = os.path.basename(file_path)
        timestamp = fname[len('conversation_history_'):-5]

        with open(file_path, 'r') as ch:
            data = json.load(ch)

        messages = data["messages"] if isinstance(data, dict) else data
        model_folder = os.path.dirname(file_path)

        Tools.print_colored("=" * 60, "black", "red")
        Tools.print_colored("  [DEPRECATED MODEL]  This conversation is read-only", "white", "red")
        Tools.print_colored("=" * 60, "black", "red")
        Tools.print_colored(f"Conversation from: {timestamp}", "black", "green")
        print("\n")

        for entry in messages:
            role = entry.get('role', '')
            content = entry.get('content', '')

            if role == 'user' and '[File:' in str(content):
                file_match = re.search(r'\[File: ([^\]]+)\]', str(content))
                if file_match:
                    Tools.print_colored(f"  Attached: {file_match.group(1)}", "gray", "black")

            if '[Ref:' in str(content) or '[Path:' in str(content):
                content = self._resolve_refs_for_display(content, model_folder)

            if role == 'user':
                Tools.print_colored("Your question:", "black", "green")
                print(content)
            elif role in ('assistant', 'model'):
                Tools.print_colored("Answer:", "blue", "white")
                if USE_MARKDOWN:
                    console = Console()
                    md = Markdown(content)
                    console.print(md)
                else:
                    print(content)

        Tools.print_colored(f"\nConversation ended: {timestamp}", "black", "green")

    @staticmethod
    def delete_orphaned_model(folder_path):
        """
        Delete an entire orphaned model folder and all its contents.
        Requires typing the folder name for confirmation.
        """
        folder_name = os.path.basename(folder_path)
        file_count = len([f for f in os.listdir(folder_path) if f.endswith('.json')])

        print(f"\nThis will DELETE {file_count} conversations from '{folder_name}'.")
        print(f"Path: {folder_path}")
        confirm = input("Type the folder name to confirm (or 0 to abort): ")

        if confirm == folder_name:
            # Notify search index for each conversation file before deletion
            for f in os.listdir(folder_path):
                if f.endswith('.json') and f.startswith('conversation_history_'):
                    notify_deletion(os.path.join(folder_path, f))
            shutil.rmtree(folder_path)
            print(f"Deleted: {folder_path}")
        elif confirm == "0":
            print("Aborted.")
        else:
            print("Folder name didn't match. Aborted.")


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
