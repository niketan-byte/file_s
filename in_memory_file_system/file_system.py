import os
import json
import atexit
from typing import Dict, List, Optional
from copy import deepcopy
from in_memory_file_system.utils import get_absolute_path, get_parent_and_name, get_directory


class InMemoryFileSystem:
    def __init__(self, load_state_file='file_system_state.json'):
        self.file_system: Dict[str, Dict] = {'/': {'type': 'directory', 'contents': {}}}
        self.current_directory = '/'
        self.load_state_file = load_state_file

        # Load the state if the file exists
        if os.path.exists(load_state_file):
            self.load_state(load_state_file)

        # Register the exit handler to save the state when the program exits
        atexit.register(self.save_state_on_exit)

    def mkdir(self, directory_name: str) -> bool:
        # Create a new directory
        # Handle errors if the directory already exists or if the path is invalid

        # Ensure the directory name is not empty
        if not directory_name:
            print("Error: Directory name cannot be empty.")
            return False

        # Get the full path of the new directory
        new_directory_path = get_absolute_path(self.current_directory, directory_name)

        # Check if the directory already exists
        if new_directory_path in self.file_system:
            print(f"Error: Directory '{directory_name}' already exists.")
            return False

        # Create the new directory
        parent_directory_path, new_directory_name = get_parent_and_name(new_directory_path)
        parent_directory = get_directory(self.file_system, parent_directory_path)

        if 'contents' not in parent_directory:
            parent_directory['contents'] = {}

        parent_directory['contents'][new_directory_name] = {'type': 'directory', 'contents': {}}
        return True

    def cd(self, path: str) -> bool:
        # Change the current directory
        # Support relative paths (.., ../), absolute paths (/), and handle errors

        # Handle special cases for root directory
        if path == '/' or path == '~':
            self.current_directory = '/'
            return True

        if path == '..':
            parent_directory_path, _ = get_parent_and_name(self.current_directory)
            if parent_directory_path:
                self.current_directory = parent_directory_path
            else:
                print("Error: Already at the root directory.")
            return True

        if path.startswith('/'):
            # Absolute path
            target_directory_path = path
            target_directory = get_directory(self.file_system, path)
        else:
            # Relative path
            target_directory_path = get_absolute_path(self.current_directory, path)
            target_directory = get_directory(self.file_system, target_directory_path)

        if target_directory:
            self.current_directory = target_directory_path
            return True
        else:
            print(f"Error: Invalid path '{path}'.")
            return False

    def ls(self, path: Optional[str] = None) -> List[str]:
        # List the contents of the current or specified directory
        # If path is None, list contents of the current directory

        if path is None:
            path = self.current_directory

        target_directory = get_directory(self.file_system, path)

        if not target_directory:
            print(f"Error: Invalid path '{path}'.")
            return []

        contents = target_directory.get('contents', {})
        return list(contents.keys())

    def grep(self, file_name: str, pattern: str) -> List[str]:
        # Search for a specified pattern in a file
        # Return a list of matching lines

        file_path = f"{self.current_directory}/{file_name}"
        target_file = get_directory(self.file_system, file_path)

        if not target_file or target_file.get('type') != 'file':
            print(f"Error: Invalid file path '{file_path}'.")
            return []

        contents = target_file.get('contents', '')
        lines = contents.split('\n')

        matching_lines = [line for line in lines if pattern in line]

        return matching_lines

    def cat(self, file_name: str) -> Optional[str]:
        # Display the contents of a file
        # Return None if the file does not exist

        file_path = f"{self.current_directory}/{file_name}"
        target_file = get_directory(self.file_system, file_path)

        if not target_file or target_file.get('type') != 'file':
            print(f"Error: Invalid file path '{file_path}'.")
            return None

        return target_file.get('contents', '')

    def touch(self, file_name: str) -> bool:
        # Create a new empty file
        # Handle errors if the file already exists or if the path is invalid

        # Ensure the file name is not empty
        if not file_name:
            print("Error: File name cannot be empty.")
            return False

        # Get the full path of the new file
        file_path = f"{self.current_directory}/{file_name}"

        # Check if the file already exists
        if get_directory(self.file_system, file_path):
            print(f"Error: File '{file_name}' already exists.")
            return False

        # Create the new file
        parent_directory_path, new_file_name = get_parent_and_name(file_path)
        parent_directory = get_directory(self.file_system, parent_directory_path)

        parent_directory['contents'][new_file_name] = {'type': 'file', 'contents': ''}
        return True

    def echo(self, text: str, file_name: str, delete_content: bool = False) -> bool:
        # Write text to a file
        # Create the file if it doesn't exist

        # Ensure the file name is not empty
        if not file_name:
            print("Error: File name cannot be empty.")
            return False

        # Get the full path of the file
        file_path = f"{self.current_directory}/{file_name}"

        # Create the file if it doesn't exist
        if not get_directory(self.file_system, file_path):
            parent_directory_path, new_file_name = get_parent_and_name(file_path)
            parent_directory = get_directory(self.file_system, parent_directory_path)

            parent_directory['contents'][new_file_name] = {'type': 'file', 'contents': ''}

        # Delete content if specified
        if delete_content:
            target_file = get_directory(self.file_system, file_path)
            target_file['contents'] = ''
        else:
            # Write text to the file
            target_file = get_directory(self.file_system, file_path)
            target_file['contents'] = text.replace("\\n", "\n")

        return True

    def mv(self, source: str, destination: str) -> bool:
        # Move a file or directory to another location
        # Handle errors if the source does not exist or if the destination is invalid

        # Get the full paths of the source and destination
        source_path = f"{self.current_directory}/{source}"
        destination_path = f"{self.current_directory}/{destination}"

        # Check if the source exists
        source_item = get_directory(self.file_system, source_path)
        if not source_item:
            print(f"Error: Source '{source}' does not exist.")
            return False

        # Check if the destination is a directory
        destination_directory = get_directory(self.file_system, destination_path)
        if not destination_directory or destination_directory.get('type') != 'directory':
            print(f"Error: Invalid destination directory '{destination}'.")
            return False

        # Move the source to the destination
        parent_directory_path, source_name = get_parent_and_name(source_path)
        destination_directory['contents'][source_name] = source_item
        del get_directory(self.file_system, parent_directory_path)['contents'][source_name]

        return True

    def cp(self, source: str, destination: str) -> bool:
        # Copy a file or directory to another location
        # Handle errors if the source does not exist or if the destination is invalid

        # Get the full paths of the source and destination
        source_path = f"{self.current_directory}/{source}"
        destination_path = f"{self.current_directory}/{destination}"

        # Check if the source exists
        source_item = get_directory(self.file_system, source_path)
        if not source_item:
            print(f"Error: Source '{source}' does not exist.")
            return False

        # Check if the destination is a directory
        destination_directory = get_directory(self.file_system, destination_path)
        if not destination_directory or destination_directory.get('type') != 'directory':
            print(f"Error: Invalid destination directory '{destination}'.")
            return False

        # Copy the source to the destination
        parent_directory_path, source_name = get_parent_and_name(source_path)
        destination_directory['contents'][source_name] = deepcopy(source_item)

        return True

    def rm(self, path: str) -> bool:
        # Remove a file or directory
        # Handle errors if the path does not exist or if it's the root directory

        # Check if the path is the root directory
        if path == '/':
            print("Error: Cannot remove the root directory.")
            return False

        # Get the full path of the item to be removed
        item_path = f"{self.current_directory}/{path}"

        # Check if the item exists
        item = get_directory(self.file_system, item_path)
        if not item:
            print(f"Error: Item '{path}' does not exist.")
            return False

        # Get the parent directory and the name of the item
        parent_directory_path, item_name = get_parent_and_name(item_path)

        # Remove the item from the parent directory
        del get_directory(self.file_system, parent_directory_path)['contents'][item_name]

        return True

    def save_state(self, file_path: str) -> bool:
        # Save the current state of the file system to a file

        try:
            with open(file_path, 'w') as file:
                json.dump(self.file_system, file, indent=2)
            print(f"State saved to {file_path}")
            return True
        except Exception as e:
            print(f"Error saving state: {str(e)}")
            return False

    def load_state(self, file_path: str) -> bool:
        # Load the state of the file system from a file

        try:
            with open(file_path, 'r') as file:
                self.file_system = json.load(file)
            print(f"State loaded from {file_path}")
            return True
        except Exception as e:
            print(f"Error loading state: {str(e)}")
            return False

    def save_state_on_exit(self):
        # Save the state of the file system when the program exits
        self.save_state('file_system_state.json')
