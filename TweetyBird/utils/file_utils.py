import json
import os


def open_json_file(filepath):
    if not os.path.exists(filepath):
        os.write(filepath, str.encode('{}'))

    with open(filepath, 'r') as file:
        contents = {}
        try:
            contents = json.load(file)
        except json.JSONDecodeError:  # This can happen if the file contents are empty
            pass
        return contents


def save_json_file(filepath, contents):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filepath, 'w') as file:
                file.write(json.dumps(contents))
            return result
        return wrapper
    return decorator
