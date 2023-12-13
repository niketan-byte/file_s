import os
import json
import atexit
from typing import Dict, List, Optional
from copy import deepcopy
from in_memory_file_system.utils import get_absolute_path, get_parent_and_name, get_directory


class InMemoryFileSystem:
    def __init__(self, load_state_file='file_system_state.json'):
        """
        Initialize the InMemoryFileSystem.

        :param load_state_file: The file path from which to load the initial state.
        """
        self.file_system: Dict[str, Dict] = {'/': {'type': 'directory', 'contents': {}}}
        self.current_directory = '/'
        self.load_state_file = load_state_file

        # Load the state if the file exists
        if os.path.exists(load_state_file):
            self.load_state(load_state_file)

        # Register the exit handler to save the state when the program exits
        atexit.register(self.save_state_on_exit)

    def mkdir(self, directory_name: str) -> bool:
        """
        Create a new directory.

        :param directory_name: The name of the new directory.
        :return: True if the directory is created successfully, False otherwise.
        """
        try:
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

        except Exception as e:
            print(f"Error creating directory: {str(e)}")
            return False

    def cd(self, path: str) -> bool:
        """
        Change the current directory.

        :param path: The path to the target directory.
        :return: True if the directory is changed successfully, False otherwise.
        """
        try:
            if path == '/' or path == '~':
                # Special cases for root directory
                self.current_directory = '/'
                return True

            if path == '..':
                # Navigate to the parent directory
                parent_directory_path = get_parent_and_name(self.current_directory)[0]
                if parent_directory_path:
                    self.current_directory = parent_directory_path
                    return True
                else:
                    print("Error: Already at the root directory.")
                    return False

            if path.startswith('/'):
                # Absolute path
                target_directory_path = path
            else:
                # Relative path
                target_directory_path = get_absolute_path(self.current_directory, path)

            # Handle case where target_directory_path is root directory
            if target_directory_path == '/':
                self.current_directory = '/'
                return True

            target_directory = get_directory(self.file_system, target_directory_path)

            if target_directory:
                self.current_directory = target_directory_path
                return True
            else:
                print(f"Error: Invalid path '{path}'.")
                return False

        except Exception as e:
            print(f"Error changing directory: {str(e)}")
            return False

    def ls(self, path: Optional[str] = None) -> List[str]:
        """
        List the contents of the current or specified directory.

        :param path: The path to the target directory. If None, list contents of the current directory.
        :return: A list of directory contents.
        """
        try:
            if path is None:
                path = self.current_directory

            target_directory = get_directory(self.file_system, path)

            if not target_directory:
                print(f"Error: Invalid path '{path}'.")
                return []

            contents = target_directory.get('contents', {})
            return list(contents.keys())

        except Exception as e:
            print(f"Error listing contents: {str(e)}")
            return []

    def grep(self, file_name: str, pattern: str) -> List[str]:
        """
        Search for a specified pattern in a file.

        :param file_name: The name of the file.
        :param pattern: The pattern to search for.
        :return: A list of matching lines.
        """
        try:
            file_path = f"{self.current_directory}/{file_name}"
            target_file = get_directory(self.file_system, file_path)

            if not target_file or target_file.get('type') != 'file':
                print(f"Error: Invalid file path '{file_path}'.")
                return []

            contents = target_file.get('contents', '')
            lines = contents.split('\n')

            matching_lines = [line for line in lines if pattern in line]

            return matching_lines

        except Exception as e:
            print(f"Error searching pattern in file: {str(e)}")
            return []

    def cat(self, file_name: str) -> Optional[str]:
        """
        Display the contents of a file.

        :param file_name: The name of the file.
        :return: The contents of the file, or None if the file does not exist.
        """
        try:
            file_path = f"{self.current_directory}/{file_name}"
            target_file = get_directory(self.file_system, file_path)

            if not target_file or target_file.get('type') != 'file':
                print(f"Error: Invalid file path '{file_path}'.")
                return None

            return target_file.get('contents', '')

        except Exception as e:
            print(f"Error displaying file contents: {str(e)}")
            return None

    def touch(self, file_name: str) -> bool:
        """
        Create a new empty file.

        :param file_name: The name of the file.
        :return: True if the file is created successfully, False otherwise.
        """
        try:
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

        except Exception as e:
            print(f"Error creating empty file: {str(e)}")
            return False

    def echo(self, text: str, file_name: str, delete_content: bool = False) -> bool:
        """
        Write text to a file.

        :param text: The text to write.
        :param file_name: The name of the file.
        :param delete_content: If True, delete existing content in the file.
        :return: True if the text is written to the file successfully, False otherwise.
        """
        try:
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

        except Exception as e:
            print(f"Error writing text to file: {str(e)}")
            return False

    def mv(self, source: str, destination: str) -> bool:
        """
        Move a file or directory to another location.

        :param source: The path of the source file or directory.
        :param destination: The destination path.
        :return: True if the move operation is successful, False otherwise.
        """
        try:
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

            if '..' in destination:
                # Handle moving to a parent directory using '..'
                parent_directory_path, _ = get_parent_and_name(self.current_directory)
                if parent_directory_path:
                    destination_directory = get_directory(self.file_system, parent_directory_path)
                else:
                    print("Error: Cannot move to parent directory from root.")
                    return False

            if not destination_directory or destination_directory.get('type') != 'directory':
                print(f"Error: Invalid destination directory '{destination}'.")
                return False

            # Move the source to the destination
            destination_directory['contents'][source] = source_item
            del get_directory(self.file_system, self.current_directory)['contents'][source]

            return True

        except Exception as e:
            print(f"Error moving file or directory: {str(e)}")
            return False

    def cp(self, source: str, destination: str) -> bool:
        """
        Copy a file or directory to another location.

        :param source: The path of the source file or directory.
        :param destination: The destination path.
        :return: True if the copy operation is successful, False otherwise.
        """
        try:
            # Get the full paths of the source and destination
            source_path = f"{self.current_directory}/{source}"
            destination_path = f"{self.current_directory}/{destination}"

            # Check if the source exists
            source_item = get_directory(self.file_system, source_path)
            if not source_item:
                print(f"Error: Source '{source}' does not exist.")
                return False

            # Check if the destination is a directory
            destination_directory_path, destination_name = get_parent_and_name(destination_path)

            if destination_name == '..':
                # If the destination ends with '..', move up one directory level
                destination_directory_path, _ = get_parent_and_name(destination_directory_path)

            destination_directory = get_directory(self.file_system, destination_directory_path)

            if not destination_directory or destination_directory.get('type') != 'directory':
                print(f"Error: Invalid destination directory '{destination}'.")
                return False

            # Copy the source to the destination
            destination_directory['contents'][destination_name] = deepcopy(source_item)

            return True

        except Exception as e:
            print(f"Error copying file or directory: {str(e)}")
            return False

    def rm(self, path: str) -> bool:
        """
        Remove a file or directory.

        :param path: The path of the file or directory to be removed.
        :return: True if the removal is successful, False otherwise.
        """
        try:
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

        except Exception as e:
            print(f"Error removing file or directory: {str(e)}")
            return False

    def save_state(self, file_path: str) -> bool:
        """
        Save the current state of the file system to a file.

        :param file_path: The path of the file to save the state.
        :return: True if the state is saved successfully, False otherwise.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.file_system, file, indent=2)
            print(f"State saved to {file_path}")
            return True
        except Exception as e:
            print(f"Error saving state: {str(e)}")
            return False

    def load_state(self, file_path: str) -> bool:
        """
        Load the state of the file system from a file.

        :param file_path: The path of the file from which to load the state.
        :return: True if the state is loaded successfully, False otherwise.
        """
        try:
            with open(file_path, 'r') as file:
                self.file_system = json.load(file)
            print(f"State loaded from {file_path}")
            return True
        except Exception as e:
            print(f"Error loading state: {str(e)}")
            return False

    def save_state_on_exit(self):
        """
        Save the state of the file system when the program exits.
        """
        self.save_state(self.load_state_file)
