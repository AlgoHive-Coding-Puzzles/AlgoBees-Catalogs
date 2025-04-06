import os
import subprocess
import time

def validate_folder(folder_path):
    """Check if the specified folder exists."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return False
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a directory.")
        return False
    return True

def validate_number(number_str):
    """Validate that the input is a positive integer."""
    try:
        number = int(number_str)
        if number <= 0:
            print("Error: lines_count must be a positive integer.")
            return None
        return number
    except ValueError:
        print(f"Error: '{number_str}' is not a valid integer.")
        return None

def process_subfolder(subfolder_path, lines_count, unique_id):
    """Run the required Python scripts in the specified subfolder and return results."""
    # Run forge.py (preparation step) with timing
    forge_start_time = time.time()
    forge_result = subprocess.run(
        ["python3", "forge.py", str(lines_count), unique_id],
        cwd=subfolder_path,
        capture_output=True,
        text=True
    )
    forge_time = time.time() - forge_start_time
    
    if forge_result.returncode != 0:
        print(f"Error running forge.py in {os.path.basename(subfolder_path)}: {forge_result.stderr}")
        return None
    
    # Run decrypt.py
    decrypt_result = subprocess.run(
        ["python3", "decrypt.py"],
        cwd=subfolder_path,
        capture_output=True,
        text=True
    )
    if decrypt_result.returncode != 0:
        print(f"Error running decrypt.py in {os.path.basename(subfolder_path)}: {decrypt_result.stderr}")
        return None
    
    decrypt_output = decrypt_result.stdout.strip()
    
    # Run unveil.py
    unveil_result = subprocess.run(
        ["python3", "unveil.py"],
        cwd=subfolder_path,
        capture_output=True,
        text=True
    )
    if unveil_result.returncode != 0:
        print(f"Error running unveil.py in {os.path.basename(subfolder_path)}: {unveil_result.stderr}")
        return None
    
    unveil_output = unveil_result.stdout.strip()
    
    return {
        "decrypt": decrypt_output,
        "unveil": unveil_output,
        "forge_time": forge_time
    }

def main():
    # Get inputs from the user
    folder_path = input("Enter the folder path: ").strip()
    if not validate_folder(folder_path):
        return

    lines_count_str = input("Enter the lines count (positive integer): ").strip()
    lines_count = validate_number(lines_count_str)
    if lines_count is None:
        return

    unique_id = input("Enter the unique ID: ").strip()
    if not unique_id:
        print("Error: Unique ID cannot be empty.")
        return

    # Get immediate subfolders (1 level deep)
    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    
    if not subfolders:
        print(f"No subfolders found in '{folder_path}'.")
        return

    # Sort subfolders to ensure consistent ordering
    subfolders.sort()
    
    # Display header
    print("\n-----------------------")
    
    # Process each subfolder
    success_count = 0
    failure_count = 0
    
    for i, subfolder in enumerate(subfolders, 1):
        quest_name = os.path.basename(subfolder)
        print(f"Quest {i}:")
        
        # Track time for entire quest processing
        quest_start_time = time.time()
        
        results = process_subfolder(subfolder, lines_count, unique_id)
        
        quest_time = time.time() - quest_start_time
        
        if results:
            print(f"Decrypt: {results['decrypt']}")
            print(f"Unveil: {results['unveil']}")
            print(f"Forge time: {results['forge_time']:.2f} seconds")
            print(f"Total quest time: {quest_time:.2f} seconds")
            print()
            success_count += 1
        else:
            print(f"Failed to process quest {i}")
            print(f"Total quest time: {quest_time:.2f} seconds")
            print()
            failure_count += 1
    
    print("-----------------------")
    print(f"Processing complete: {success_count} successful, {failure_count} failed")

if __name__ == "__main__":
    main()