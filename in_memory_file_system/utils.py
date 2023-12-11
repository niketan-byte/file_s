from typing import Dict, Tuple, Optional


def get_absolute_path(current_directory: str, path: str) -> str:
    # Convert a relative path to an absolute path
    # Handle cases like /, .., ../, etc.

    if path.startswith('/'):
        # Absolute path
        return path
    else:
        # Relative path
        current_parts = [part for part in current_directory.split('/') if part]
        path_parts = [part for part in path.split('/') if part]

        if path_parts and path_parts[0] == '..':
            # Handle relative paths with ..
            current_parts.pop()

        current_parts.extend(path_parts)
        return '/' + '/'.join(current_parts)


def get_parent_and_name(path: str) -> Tuple[str, str]:
    # Get the parent directory path and the name of the item
    parts = path.split('/')
    parent_directory_path = '/'.join(parts[:-1])
    item_name = parts[-1]
    return parent_directory_path, item_name


def get_directory(file_system: Dict[str, Dict], path: str) -> Optional[Dict]:
    # Get the directory or file at the specified path
    current = file_system

    for part in path.split('/'):
        if not part:
            continue

        current = current.get('contents', {}).get(part)

        if not current:
            return None

    return current
