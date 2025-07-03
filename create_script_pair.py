import os

def create_script_pair():
    folder_path = input("Enter the full folder path: ").strip()
    if not os.path.isdir(folder_path):
        print("❌ Invalid path.")
        return

    file_name = input("Enter the base name (without extension): ").strip()
    if not file_name:
        print("❌ Invalid file name.")
        return

    py_path = os.path.join(folder_path, f"{file_name}.py")
    bat_path = os.path.join(folder_path, f"{file_name}.bat")

    # Create .py file with a simple hello world as placeholder
    if not os.path.exists(py_path):
        with open(py_path, 'w') as py_file:
            py_file.write("# Your Python code starts here\nprint('Hello from', __file__)\n")
        print(f"✅ Created: {py_path}")
    else:
        print(f"⚠️ Python file already exists: {py_path}")

    # Create .bat file to run the python script
    if not os.path.exists(bat_path):
        with open(bat_path, 'w') as bat_file:
            bat_file.write(f"python \"{file_name}.py\"\npause\n")
        print(f"✅ Created: {bat_path}")
    else:
        print(f"⚠️ Batch file already exists: {bat_path}")

if __name__ == "__main__":
    create_script_pair()
