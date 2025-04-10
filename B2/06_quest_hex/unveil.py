class Unveil:
    def __init__(self, lines: list):
        self.lines = lines
        
    def determine_bee_vision_color(self, hex_color: str) -> int:
        # Remove '#' if present
        if hex_color.startswith('#'):
            hex_color = hex_color[1:]
        
        # Parse the hex color to get the RGB components
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        bee_uv = max(0, int(b * 0.2 + g * 0.1 - r * 0.3))
        bee_green = int(g * 0.8)
        bee_blue = int(b * 0.7 + g * 0.3)
        
        return bee_uv, bee_green, bee_blue
       
    def run(self):
        vote_count = {
            'uv': 0,
            'green': 0,
            'blue': 0,
        }
        for i in range(len(self.lines)):
            # Remove leading and trailing whitespace
            self.lines[i] = self.lines[i].strip()
            # Add the color to the vote count
            uv, green, blue = self.determine_bee_vision_color(self.lines[i])
            vote_count['uv'] += uv
            vote_count['green'] += green
            vote_count['blue'] += blue
        
        print(vote_count)
        new_hexa = self.build_new_hexa(vote_count['uv'], vote_count['green'], vote_count['blue'])
        
        print(new_hexa)
        print(f"New hex color: {new_hexa}")
        return self.convert_hexa_to_int(new_hexa) * 2     
        
    def build_new_hexa(self, u, g, b):
        """Build a new hex color from UGB values, if the values are too high, we do a modulo 256"""
        u = u % 256
        g = g % 256
        b = b % 256
        print(f"U: {u}, G: {g}, B: {b}")
        return f'#{u:02X}{g:02X}{b:02X}'
    
    def convert_hexa_to_int(self, hexa):
        """Convert a hex color to an int"""
        hexa = hexa.lstrip('#')
        return int(hexa, 16)
            
if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
    unveil = Unveil(lines)
    solution = unveil.run()
    print(solution)

