import time
import os

class Unveil:
    def __init__(self, lines: list):
        self.lines = lines

    def run(self):
        # Parse the grid
        grid = [line.split() for line in self.lines[:-1]]

        # Find the starting position ('X')
        start_x, start_y = None, None
        for i, row in enumerate(grid):
            if 'X' in row:
                start_x, start_y = row.index('X'), i
                break
            
        def count_points(cell):
            if cell == "R":
                return 5
            elif cell == "O":
                return -1
            else:
                return 0
        
        def generate_spiral(length):
                spiral = ["NE"]
                spiral += ["SE"] * (length - 1)
                spiral += ["S"] * (length)
                spiral += ["SW"] * (length)
                spiral += ["NW"] * (length)
                spiral += ["N"] * (length)
                spiral += ["NE"] * (length)
                # print(spiral)
                return spiral
            
        # (x, y)
        direction_map = {
            "N": (0, -1),
            "NE": (1, -1),
            "NW": (-1, -1),
            "S": (0, 1),
            "SE": (1, 1),
            "SW": (-1, 1),
        }
        
        # ANSI color codes for spiral visualization
        COLORS = [
            "\033[91m",  # Red
            "\033[92m",  # Green
            "\033[93m",  # Yellow
            "\033[94m",  # Blue
            "\033[95m",  # Magenta
            "\033[96m",  # Cyan
            "\033[97m",  # White
        ]

        # Helper to check if a cell is within bounds
        def is_valid(y, x):
            return 0 <= y < len(grid) and 0 <= x < len(grid[0])

        # Perform the spiral traversal
        visited = {}  # Map (y,x) to spiral number
        path = []
        score = 0
        x, y = start_x, start_y
        visited[(y, x)] = 0  # Starting position is spiral 0
        path.append((y, x))

        def display_grid():
            os.system('clear')  # Clear the console
            for i, row in enumerate(grid):
                for j, cell in enumerate(row):
                    if (i, j) in visited:
                        spiral_num = visited[(i, j)]
                        color_code = COLORS[spiral_num % len(COLORS)]
                        print(f"{color_code}{cell}\033[0m", end=" ")  # Color based on spiral number
                    else:
                        print(cell, end=" ")
                print()
            print(f"\nCurrent Score: {score}")
            print(f"Path: {path}")
            time.sleep(0.3)

        # Spiral logic
        spiral_length = 1
        path_length = 0
        out_of_bounds = False
        current_spiral = 0

        while not out_of_bounds:
            directions = generate_spiral(spiral_length)
            for direction in directions:
                dx, dy = direction_map[direction]
                if is_valid(y + dy, x + dx):
                    y += dy
                    x += dx
                    visited[(y, x)] = current_spiral
                    path.append((y, x))
                    cell = grid[y][x]
                    score += count_points(cell)
                    
                    path_length += 1
                    # display_grid()
                else:
                    out_of_bounds = True
                    break
            spiral_length += 1
            current_spiral += 1

        return path_length * score

if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
    unveil = Unveil(lines)
    score = unveil.run()
    print(score)

