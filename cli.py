from in_memory_file_system.file_system import InMemoryFileSystem
import argparse

# Initialize the file system
file_system = InMemoryFileSystem(load_state_file='file_system_state.json')


def process_command(command_str):
    """
    Process a command string and execute the corresponding file system operation.

    :param command_str: The command string.
    """
    try:
        # Split the command string into a list of arguments
        command_parts = command_str.split()

        # Define command-line arguments
        parser = argparse.ArgumentParser(description='In-Memory File System CLI')
        parser.add_argument('command', choices=['mkdir', 'cd', 'ls', 'grep', 'cat', 'touch', 'echo', 'mv', 'cp', 'rm', 'pwd'],
                            help='The file system command')
        parser.add_argument('arguments', nargs='*', help='Command arguments')

        # Parse the command string
        args = parser.parse_args(command_parts)

        # Execute the corresponding function based on the provided command
        if args.command == 'mkdir':
            if args.arguments:
                directory_name = args.arguments[0]
                file_system.mkdir(directory_name)
            else:
                print("Error: Missing directory name.")
        elif args.command == 'cd':
            path = args.arguments[0] if args.arguments else None
            file_system.cd(path)
            print(f"Current directory changed to '{file_system.current_directory}'")
        elif args.command == 'ls':
            path = args.arguments[0] if args.arguments else None
            contents = file_system.ls(path)
            if contents:
                print("Contents:")
                for item in contents:
                    print(f"  {item}")
            else:
                print("Directory is empty.")
        elif args.command == 'grep':
            if len(args.arguments) >= 2:
                file_name = args.arguments[0]
                pattern = args.arguments[1]
                matching_lines = file_system.grep(file_name, pattern)
                if matching_lines:
                    print("Matching lines:")
                    for line in matching_lines:
                        print(f"  {line}")
                else:
                    print("No matching lines found.")
            else:
                print("Error: Missing file name or pattern.")
        elif args.command == 'cat':
            if args.arguments:
                file_name = args.arguments[0]
                contents = file_system.cat(file_name)
                if contents is not None:
                    print(f"Contents of '{file_name}':")
                    print(contents)
                else:
                    print(f"Error: File '{file_name}' not found.")
            else:
                print("Error: Missing file name.")
        elif args.command == 'touch':
            if args.arguments:
                file_name = args.arguments[0]
                file_system.touch(file_name)
                print(f"Empty file '{file_name}' created successfully")
            else:
                print("Error: Missing file name.")
        elif args.command == 'echo':
            if len(args.arguments) >= 2:
                file_name = args.arguments[0]
                text = args.arguments[1]
                file_system.echo(text, file_name)
                print(f"Text written to file '{file_name}'")
            else:
                print("Error: Missing file name or text.")
        elif args.command == 'mv':
            if len(args.arguments) >= 2:
                source = args.arguments[0]
                destination = args.arguments[1]
                file_system.mv(source, destination)
                print(f"Moved '{source}' to '{destination}'")
            else:
                print("Error: Missing source or destination.")
        elif args.command == 'cp':
            if len(args.arguments) >= 2:
                source = args.arguments[0]
                destination = args.arguments[1]
                file_system.cp(source, destination)
                print(f"Copied '{source}' to '{destination}'")
            else:
                print("Error: Missing source or destination.")
        elif args.command == 'rm':
            if args.arguments:
                path = args.arguments[0]
                file_system.rm(path)
                print(f"Removed '{path}'")
            else:
                print("Error: Missing file or directory path.")
        elif args.command == 'pwd':
            print(f"Current directory: '{file_system.current_directory}'")
        else:
            print(f"Error: Unknown command '{args.command}'")

        # Save the state after each command
        file_system.save_state('file_system_state.json')

    except Exception as e:
        print(f"Error: {str(e)}")


# Run commands interactively
while True:
    command_input = input("Enter a command: ")
    if command_input.lower() == 'exit':
        break
    process_command(command_input)
