class Unveil:
    def __init__(self, lines: list):
        self.lines = lines

    def run(self):
        # Set up the board by tracking only active cells in a set
        active_cells = {
            (x, y)
            for y, line in enumerate(self.lines)
            for x, char in enumerate(line.strip())
            if char == '#'
        }
        
        # Determine the dimensions dynamically
        width = len(self.lines[0].strip())
        height = len(self.lines)
        
        # Cache for calculating next state
        neighbor_deltas = [
            (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        ]
        
        # Do 100 iterations
        for _ in range(100):
            # Track cells to check (active cells + their neighbors)
            cells_to_check = set()
            for x, y in active_cells:
                cells_to_check.add((x, y))
                for dx, dy in neighbor_deltas:
                    cells_to_check.add((x + dx, y + dy))
            
            # Calculate next state
            new_active = set()
            for x, y in cells_to_check:
                # Skip if outside bounds
                if not (0 <= x < width and 0 <= y < height):
                    continue
                
                # Count active neighbors
                neighbor_count = sum(
                    1 for dx, dy in neighbor_deltas
                    if (x + dx, y + dy) in active_cells
                )
                
                # Apply Game of Life rules
                if (x, y) in active_cells:
                    if 2 <= neighbor_count <= 3:
                        new_active.add((x, y))
                elif neighbor_count == 3:
                    new_active.add((x, y))
            
            active_cells = new_active
            
        # Count Bee-Hive forms
        return self.count_bee_hives(active_cells)

    def count_bee_hives(self, lights):
        # Define the relative positions of a horizontal Bee-Hive pattern
        """
        . # # .
        # . . #
        . # # .
        """
        horizontal_offsets = [
            (0, 0), (1, 0),  # Top row
            (-1, 1), (2, 1),  # Middle row (dots in the center)
            (0, 2), (1, 2)   # Bottom row
        ]

        # Define the relative positions of a vertical Bee-Hive pattern
        """
        . # .
        # . #
        # . #
        . # .
        """
        vertical_offsets = [
            (0, 0),          # Top row
            (-1, 1), (1, 1), # Second row
            (-1, 2), (1, 2), # Third row
            (0, 3)           # Bottom row
        ]

        count = 0
        for x, y in lights:
            # Check for horizontal Bee-Hive
            if all((x + dx, y + dy) in lights for dx, dy in horizontal_offsets) and \
               (x, y + 1) not in lights and (x + 1, y + 1) not in lights:  # Middle dots must be empty
                count += 1

            # Check for vertical Bee-Hive
            if all((x + dx, y + dy) in lights for dx, dy in vertical_offsets) and \
               (x, y + 1) not in lights and (x, y + 2) not in lights:  # Middle dots must be empty
                count += 1

        return count

if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
    unveil = Unveil(lines)
    solution = unveil.run()
    print(solution)

