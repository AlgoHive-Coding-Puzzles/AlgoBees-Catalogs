class Decrypt:
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
            # Calculate new 'lights' from the previous one
            lights = {
                (x, y)
                for x in range(BOARD_SIZE)
                for y in range(BOARD_SIZE)
                if (x, y) in lights and 2 <= neighbours(x, y) <= 3
                or (x, y) not in lights and neighbours(x, y) == 3
            }

        return len(lights)

if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
    decrypt = Decrypt(lines)
    solution = decrypt.run()
    print(solution)

