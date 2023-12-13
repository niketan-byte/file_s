# In-Memory File System Documentation

## Overview
This project implements an in-memory file system using Python and FastAPI. The system provides a set of HTTP endpoints to interact with the file system, enabling operations such as creating directories, changing directories, listing contents, searching for patterns in files, and more.

## Problem Statement
The goal is to create a simple in-memory file system that allows users to perform file and directory operations through HTTP requests. This includes creating and navigating directories, reading and writing files, and moving or copying files and directories.

## Intuition
The project leverages the FastAPI framework to expose HTTP endpoints, making it easy to interact with the file system through RESTful API calls. The in-memory file system is represented as a hierarchical tree structure stored in a Python dictionary. Each node in the tree represents a directory or a file, with associated metadata.


## Installation

### Git Installation

1. **Clone the Repository:**
    ```bash
     git clone https://github.com/niketan-byte/file_system.git
     cd file_system_inito

    ```

2. **Setup Virtual Environment:**
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows, use: env\\Scripts\\activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Application:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

5. **Access the Application:**
    Open a web browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) to access the API documentation.

6. **Exit the Application:**
    To gracefully stop the application, press `Ctrl + C`. The state will be saved automatically.

### Docker Installation

1. **Build Docker Image:**
    ```bash
     docker build -t file_system .
    ```

2. **Run Docker Container:**
    ```bash
     docker run -p 8081:8081 -it -v $(pwd)/data/state:/app/state file_system
    ```

3. **Access the Application:**
    Open a web browser and go to [http://0.0.0.0:8081/docs#/](http://0.0.0.0:8081/docs#/) to access the API documentation.


## Project Structure

The project is organized into three main files:

**file_system.py:** Defines the InMemoryFileSystem class, which encapsulates the in-memory file system logic. It includes methods for performing file and directory operations, as well as saving and loading the file system state.

**cli.py:** Provides a command-line interface (CLI) for users to interact with the file system. Users can enter commands to perform various operations, and the system responds accordingly.

**main.py:** Implements FastAPI routes to expose the functionality of the in-memory file system over HTTP. Each route corresponds to a specific operation, and the API documentation is generated automatically.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
