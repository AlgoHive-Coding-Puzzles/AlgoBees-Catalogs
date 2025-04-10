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
    
    def generate_file(self):
        """
        Return a file with random extension, and as second part of the return, a random size
        """
        extensions = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=3))
        filename = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz", k=6))
        size = random.randint(10000, 75000)  # Size between 10k and 75k bytes
        return f"{filename}.{extensions}", size
    
    def generate_structure(self):
        """
        Generate a random structure of folders and files (recursive)
        src/
        - folder1/
        - - file1.txt (123 bytes)
        - - file2.txt (456 bytes)
        - - folderSome/
        - - - file3.txt (789 bytes)
        - folder2/
        - - file4.txt (123 bytes)
        - - folder4/
        - - - folder5/
        - - - - file5.txt (123 bytes)
        - - - file 6.txt (456 bytes)
        """
        MAX_DEPTH = 3
        MAX_FILES = 5
        MAX_FOLDERS_PER_FOLDER = 3
        
        def create_structure(depth=0):
            if depth > MAX_DEPTH:
                return {}
            
            structure = {}
            
            # Generate files
            files = []
            for _ in range(random.randint(2, MAX_FILES)):
                file_name, size = self.generate_file()
                files.append((file_name, size))
            
            if files:
                structure["files"] = files
            
            # Generate subfolders
            for _ in range(random.randint(1, MAX_FOLDERS_PER_FOLDER)):
                if depth < MAX_DEPTH:  # Ensure we don't go too deep
                    folder_name = self.generate_folder_name()
                    sub_structure = create_structure(depth + 1)
                    if sub_structure:  # Only add non-empty subfolders
                        structure[folder_name] = sub_structure
            
            return structure

        # Start with a root folder
        root_folder = self.generate_folder_name()
        return {root_folder: create_structure()}

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
        structure = self.generate_structure()
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
