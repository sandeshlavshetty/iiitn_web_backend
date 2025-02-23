import os

def list_files(startpath, exclude=".venv"):
    for root, dirs, files in os.walk(startpath):
        if exclude in root:
            continue
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

list_files(".")  # Change "." to the desired path
