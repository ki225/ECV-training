import os
import shutil

def get_all_json_files(directory):
    json_file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.json'):
                json_file_list.append(os.path.join(root, file))
    return json_file_list

def create_cve_folder_and_move_files(file_list):
    cve_folder = os.path.join(script_dir, "cve")
    
    # Create the "cve" folder if it doesn't exist
    if not os.path.exists(cve_folder):
        os.makedirs(cve_folder)
    
    # Move files to the "cve" folder
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        destination = os.path.join(cve_folder, file_name)
        shutil.move(file_path, destination)

# if __name__ == "__main__":
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Get all files in the current directory and its subdirectories
all_files = get_all_json_files(script_dir)
print(f"Total files found: {len(all_files)}")

# Move all files to the "cve" folder
create_cve_folder_and_move_files(all_files)

# Get the list of JSON files in the new "cve" folder
cve_folder = os.path.join(script_dir, "cve")
json_files = [f for f in os.listdir(cve_folder) if f.endswith('.json')]
print(f"\nJSON files in 'cve' folder: {len(json_files)}")