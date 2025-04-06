# forge.py - Génère input.txt
import sys
import random

class Forge:
    def __init__(self, lines_count: int, unique_id: str = None):
        self.lines_count = lines_count
        self.unique_id = unique_id
    
    def run(self) -> list:
        random.seed(self.unique_id)

        NAMES = [
            "Beeyoncé",
            "Beekachu",
            "Beethoven",
            "Beeware",
            "Beebop",
            "Beelieve",
        ]
        
        lines = []
        for i in range(len(NAMES)):
            lines.append(self.generate_spec(
                name=NAMES[i],
                speed=random.randint(5, 40),
                duration=random.randint(1, 25),
                recharge=random.randint(25, 150)
            ))
        return lines
    
    def generate_spec(self, name, speed, duration, recharge):
        return f"{name} vole a {speed}km/s pendant {duration} secondes, puis doit s'arrêter pour {recharge} secondes."
    
if __name__ == '__main__':
    lines_count = int(sys.argv[1])
    unique_id = sys.argv[2]
    forge = Forge(lines_count, unique_id)
    lines = forge.run()
    with open('input.txt', 'w') as f:
        f.write('\n'.join(lines) + '\n')
