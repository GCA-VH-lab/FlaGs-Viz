import os

def generate_file_structure(directory):
    file_structure = ""
    for root, dirs, files in os.walk(directory):
        current_level = root.replace(directory, "").count(os.sep)
        indent = "    " * current_level
        file_structure += f"{indent}|- {os.path.basename(root)}/\n"
        sub_indent = "    " * (current_level + 1)
        for file in files:
            file_structure += f"{sub_indent}{file}\n"
    return file_structure.strip()

current_directory = os.getcwd()
repo_file_structure = generate_file_structure(current_directory)
print(repo_file_structure)
