class Unveil:
    def __init__(self, lines: list):
        self.lines = lines

    def run(self):
        BOARD_SIZE = 125
        
        # Set up the board
        lights = {
            (x, y)
            for y, line in enumerate(self.lines)
            for x, char in enumerate(line.strip())
            if char == '#'
        }

        # This returns the number of neighbours that are turned on.
        def neighbours(x, y):
            return sum(
                (_x, _y) in lights
                for _x in (x - 1, x, x + 1)
                for _y in (y - 1, y, y + 1)
                if (_x, _y) != (x, y)
            )

        # Do 100 iterations
        for _ in range(100):
            lights = {
                (x, y)
                for x in range(BOARD_SIZE)
                for y in range(BOARD_SIZE)
                if (x, y) in lights and 2 <= neighbours(x, y) <= 3
                or (x, y) not in lights and neighbours(x, y) == 3
            }

        # Count Bee-Hive forms
        return self.count_bee_hives(lights)

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
                # print(f"Horizontal Bee-Hive found at ({y + 1}, {x + 1})")
                count += 1

            # Check for vertical Bee-Hive
            if all((x + dx, y + dy) in lights for dx, dy in vertical_offsets) and \
               (x, y + 1) not in lights and (x, y + 2) not in lights:  # Middle dots must be empty
                # print(f"Vertical Bee-Hive found at ({y + 1}, {x + 1})")
                count += 1

        return count

if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
    unveil = Unveil(lines)
    solution = unveil.run()
    print(solution)

