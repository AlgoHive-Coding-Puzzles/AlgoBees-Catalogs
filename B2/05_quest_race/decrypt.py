class Decrypt:
    def __init__(self, lines: list):
        self.lines = lines
        
    def run(self):
        racers = []
        for line in self.lines:
            parts = line.split()
            name = parts[0]
            speed = int(parts[3].replace("km/s", ""))
            fly_time = int(parts[5].replace("secondes", ""))
            recharge_time = int(parts[-2].replace("secondes", ""))
            racers.append((name, speed, fly_time, recharge_time))
                    
        time_limit = 7832
        distances = {}
        for name, speed, fly_time, recharge_time in racers:
            cycle_time = fly_time + recharge_time
            full_cycles = time_limit // cycle_time
            remaining_time = time_limit % cycle_time
            distance = full_cycles * speed * fly_time + min(remaining_time, fly_time) * speed
            distances[name] = distances.get(name, 0) + distance
        
        # Return the maximum distance
        return max(distances.values())
    
if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
    decrypt = Decrypt(lines)
    solution = decrypt.run()
    print(solution)
    
    