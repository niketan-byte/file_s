from typing import Optional

from fastapi import FastAPI, HTTPException

from in_memory_file_system.file_system import InMemoryFileSystem

app = FastAPI()

# Initialize the in-memory file system
file_system = InMemoryFileSystem(load_state_file='file_system_state.json')


# Define API endpoints here...

@app.post("/mkdir/{directory_name}")
def create_directory(directory_name: str):
    if file_system.mkdir(directory_name):
        return {"message": f"Directory '{directory_name}' created successfully"}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to create directory '{directory_name}'")


@app.post("/cd")
async def change_directory(path: Optional[str] = None):
    if file_system.cd(path):
        return {"message": f"Current directory changed to '{file_system.current_directory}'"}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to change directory to '{path}'")


@app.get("/pwd")
def get_current_directory():
    return {"current_directory": file_system.current_directory}


@app.get("/ls")
def list_contents(path: str = None):
    contents = file_system.ls(path)
    return {"contents": contents}


@app.post("/grep/{file_name}/{pattern}")
def search_pattern_in_file(file_name: str, pattern: str):
    matching_lines = file_system.grep(file_name, pattern)
    return {"matching_lines": matching_lines}


@app.get("/cat/{file_name}")
def display_file_contents(file_name: str):
    contents = file_system.cat(file_name)
    if contents is not None:
        return {"contents": contents}
    else:
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")


@app.post("/touch/{file_name}")
def create_empty_file(file_name: str):
    if file_system.touch(file_name):
        return {"message": f"Empty file '{file_name}' created successfully"}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to create file '{file_name}'")


@app.post("/echo/{file_name}")
def write_text_to_file(file_name: str, text: str):
    if file_system.echo(text, file_name):
        return {"message": f"Text written to file '{file_name}'"}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to write text to file '{file_name}'")


@app.post("/mv/{source}/{destination}")
def move_file_or_directory(source: str, destination: str):
    if file_system.mv(source, destination):
        return {"message": f"Moved '{source}' to '{destination}'"}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to move '{source}' to '{destination}'")


@app.post("/cp/{source}/{destination}")
def copy_file_or_directory(source: str, destination: str):
    if file_system.cp(source, destination):
        return {"message": f"Copied '{source}' to '{destination}'"}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to copy '{source}' to '{destination}'")


@app.post("/rm/{path}")
def remove_file_or_directory(path: str):
    if file_system.rm(path):
        return {"message": f"Removed '{path}'"}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to remove '{path}'")
