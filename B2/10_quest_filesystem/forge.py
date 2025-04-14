# forge.py - Génère input.txt
import sys
import random

class Forge:
    def __init__(self, lines_count: int, unique_id: str = None):
        self.lines_count = lines_count
        self.unique_id = unique_id
        
    def generate_folder_name(self):
        """
        Return a name between 3 and 8 characters
        """
        length = random.randint(3, 8)
        return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length))
    
    def generate_file(self, max_size=30000):
        """
        Return a file with random extension, and as second part of the return, a random size
        """
        extensions = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=3))
        filename = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=6))
        size = random.randint(5000, max_size)  # Reduced maximum file size
        return f"{filename}.{extensions}", size
    
    def generate_structure(self):
        """
        Generate a random structure of folders and files (recursive)
        """
        MAX_DEPTH = 4  # Increased depth for more variety
        MAX_FILES = 3  # Reduced max files for better control of directory sizes
        MAX_FOLDERS_PER_FOLDER = 3
        
        def create_structure(depth=0):
            if depth > MAX_DEPTH:
                return {}
            
            structure = {}
            
            # Generate files - fewer files at deeper levels
            files = []
            num_files = random.randint(1, max(1, MAX_FILES - depth))
            for _ in range(num_files):
                # Smaller files at deeper levels to ensure some dirs are under 100k
                max_size = 30000 if depth > 1 else 40000
                file_name, size = self.generate_file(max_size)
                files.append((file_name, size))
            
            if files:
                structure["files"] = files
            
            # Generate subfolders - fewer folders at deeper levels
            num_folders = random.randint(0, max(1, MAX_FOLDERS_PER_FOLDER - depth))
            for _ in range(num_folders):
                if depth < MAX_DEPTH:
                    folder_name = self.generate_folder_name()
                    sub_structure = create_structure(depth + 1)
                    if sub_structure:
                        structure[folder_name] = sub_structure
            
            return structure

        # Start with a root folder
        root_folder = self.generate_folder_name()
        return {root_folder: create_structure()}
    
    def validate_structure(self, structure):
        """
        Check if the structure has at least one directory <= 100,000 bytes
        and the largest such directory is not 0
        """
        # Calculate directory sizes
        dir_sizes = {}
        
        def calculate_dir_sizes(node, path=''):
            dir_size = 0
            
            for name, content in node.items():
                if name == "files":
                    for _, size in content:
                        dir_size += size
                else:
                    subdir_path = f"{path}/{name}" if path else name
                    subdir_size = calculate_dir_sizes(content, subdir_path)
                    dir_size += subdir_size
            
            if path:  # Don't store size for the root
                dir_sizes[path] = dir_size
            return dir_size
        
        # Calculate sizes for all directories
        for root, contents in structure.items():
            calculate_dir_sizes(contents, root)
        
        # Check if we have directories <= 100,000 bytes
        valid_dirs = [size for size in dir_sizes.values() if size <= 100000]
        
        return len(valid_dirs) >= 3  # At least 3 valid directories

    def pretty_print(self, structure):
        """
        Pretty print the structure
        """
        def print_structure(structure, prefix=""):
            for key, value in structure.items():
                if key == "files":
                    # Print files at the current level
                    for file_name, size in value:
                        print(f"{prefix}- {file_name} ({size} bytes)")
                else:
                    # Print folder and recursively print its contents
                    print(f"{prefix}- {key}/")
                    print_structure(value, prefix + "  ")
        
        # Print the root folder
        for root, contents in structure.items():
            print(f"{root}/")
            print_structure(contents, "  ")
    
    def run(self) -> list:
        random.seed(self.unique_id)
        
        # Generate structure until we have one with valid directories
        attempts = 0
        max_attempts = 10
        valid_structure = False
        structure = None
        
        while not valid_structure and attempts < max_attempts:
            structure = self.generate_structure()
            valid_structure = self.validate_structure(structure)
            attempts += 1
        
        # Return the lines as a list
        lines = []
        def collect_lines(structure, prefix=""):
            for key, value in structure.items():
                if key == "files":
                    for file_name, size in value:
                        lines.append(f"{prefix}- {file_name} ({size} bytes)")
                else:
                    lines.append(f"{prefix}- {key}/")
                    collect_lines(value, prefix + "  ")
                    
        collect_lines(structure)
        return lines
        

if __name__ == '__main__':
    lines_count = int(sys.argv[1])
    unique_id = sys.argv[2]
    forge = Forge(lines_count, unique_id)
    lines = forge.run()
    with open('input.txt', 'w') as f:
        f.write('\n'.join(lines) + '\n')
