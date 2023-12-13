from typing import Optional

from fastapi import FastAPI, HTTPException

from in_memory_file_system.file_system import InMemoryFileSystem

app = FastAPI()

# Initialize the in-memory file system
file_system = InMemoryFileSystem(load_state_file='file_system_state.json')


@app.post("/mkdir/{directory_name}")
def create_directory(directory_name: str):
    """
    Create a directory.

    :param directory_name: The name of the directory.
    :return: A message indicating the success or failure of the operation.
    """
    try:
        if file_system.mkdir(directory_name):
            return {"message": f"Directory '{directory_name}' created successfully"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to create directory '{directory_name}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/cd")
async def change_directory(path: Optional[str] = None):
    """
    Change the current directory.

    :param path: The path to change to.
    :return: A message indicating the success or failure of the operation.
    """
    try:
        if file_system.cd(path):
            return {"message": f"Current directory changed to '{file_system.current_directory}'"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to change directory to '{path}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/pwd")
def get_current_directory():
    """
    Get the current directory.

    :return: The current directory.
    """
    try:
        return {"current_directory": file_system.current_directory}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/ls")
def list_contents(path: str = None):
    """
    List the contents of a directory.

    :param path: The path of the directory. If None, list the contents of the current directory.
    :return: The list of contents.
    """
    try:
        contents = file_system.ls(path)
        return {"contents": contents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/grep/{file_name}/{pattern}")
def search_pattern_in_file(file_name: str, pattern: str):
    """
    Search for a pattern in a file.

    :param file_name: The name of the file.
    :param pattern: The pattern to search for.
    :return: The list of matching lines.
    """
    try:
        matching_lines = file_system.grep(file_name, pattern)
        return {"matching_lines": matching_lines}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/cat/{file_name}")
def display_file_contents(file_name: str):
    """
    Display the contents of a file.

    :param file_name: The name of the file.
    :return: The contents of the file.
    """
    try:
        contents = file_system.cat(file_name)
        if contents is not None:
            return {"contents": contents}
        else:
            raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/touch/{file_name}")
def create_empty_file(file_name: str):
    """
    Create an empty file.

    :param file_name: The name of the file.
    :return: A message indicating the success or failure of the operation.
    """
    try:
        if file_system.touch(file_name):
            return {"message": f"Empty file '{file_name}' created successfully"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to create file '{file_name}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/echo/{file_name}")
def write_text_to_file(file_name: str, text: str):
    """
    Write text to a file.

    :param file_name: The name of the file.
    :param text: The text to write.
    :return: A message indicating the success or failure of the operation.
    """
    try:
        if file_system.echo(text, file_name):
            return {"message": f"Text written to file '{file_name}'"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to write text to file '{file_name}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/mv/{source}/{destination}")
def move_file_or_directory(source: str, destination: str):
    """
    Move a file or directory to another location.

    :param source: The source path.
    :param destination: The destination path.
    :return: A message indicating the success or failure of the operation.
    """
    try:
        if file_system.mv(source, destination):
            return {"message": f"Moved '{source}' to '{destination}'"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to move '{source}' to '{destination}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/cp/{source}/{destination}")
def copy_file_or_directory(source: str, destination: str):
    """
    Copy a file or directory to another location.

    :param source: The source path.
    :param destination: The destination path.
    :return: A message indicating the success or failure of the operation.
    """
    try:
        if file_system.cp(source, destination):
            return {"message": f"Copied '{source}' to '{destination}'"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to copy '{source}' to '{destination}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/rm/{path}")
def remove_file_or_directory(path: str):
    """
    Remove a file or directory.

    :param path: The path to the file or directory.
    :return: A message indicating the success or failure of the operation.
    """
    try:
        if file_system.rm(path):
            return {"message": f"Removed '{path}'"}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to remove '{path}'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
