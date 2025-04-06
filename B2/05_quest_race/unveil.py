class Unveil:
    def __init__(self, lines: list):
        self.lines = lines
        
    def run(self):
        racers = []
        for line in self.lines:
            parts = line.split()
            name = parts[0]
            speed = int(parts[3].replace("km/s", ""))
            fly_time = int(parts[5].replace("seconds", ""))
            recharge_time = int(parts[-2].replace("seconds", ""))
            racers.append((name, speed, fly_time, recharge_time))
        
        time_limit = 1059
        points = {name: 0 for name, _, _, _ in racers}
        distances = {name: 0 for name, _, _, _ in racers}

        for t in range(1, time_limit + 1):
            for name, speed, fly_time, recharge_time in racers:
                cycle_time = fly_time + recharge_time
                if (t % cycle_time) <= fly_time and (t % cycle_time) != 0:
                    distances[name] += speed
            
            max_distance = max(distances.values())
            for name in distances:
                if distances[name] == max_distance:
                    points[name] += 1
        
        return max(points.values())
    
if __name__ == '__main__':
    with open('input.txt') as f:
        lines = f.readlines()
    unveil = Unveil(lines)
    solution = unveil.run()
    print(solution)
    
    