class Hole():
    def __init__(self, start_pt=[0, 0]):
        self.location = start_pt
        self.holes = []
        self.endpoints = []
        self.area = 0
        self.perimeter = 0

    def digHole(self, direction, dist, color):
        if direction == "U":
            for i in range(1, dist + 1):
                self.holes.append((self.location[0], self.location[1] - i, color))
            self.location[1] -= dist
        elif direction == "D":
            for i in range(1, dist + 1):
                self.holes.append((self.location[0], self.location[1] + i, color))
            self.location[1] += dist
        elif direction == "L":
            for i in range(1, dist + 1):
                self.holes.append((self.location[0] - i, self.location[1], color))
            self.location[0] -= dist
        elif direction == "R":
            for i in range(1, dist + 1):
                self.holes.append((self.location[0] + i, self.location[1], color))
            self.location[0] += dist
        self.endpoints.append((self.location[0], self.location[1], color))
        self.perimeter += dist


    def digHexHole(self, hex_code):
        dist = int(hex_code[1:6], 16)
        direction = int(hex_code[6])
        if direction == 3:
            self.location[1] -= dist
        elif direction == 1:
            self.location[1] += dist
        elif direction == 2:
            self.location[0] -= dist
        elif direction == 0:
            self.location[0] += dist
        self.endpoints.append((self.location[0], self.location[1]))
        self.perimeter += dist


    def calcArea(self):
        self.area = self.shoelaceArea() + self.perimeter/2 + 1
        return self.area
        
    
    def shoelaceArea(self):
        A = 0
        for i in range(len(self.endpoints)):
            A += self.endpoints[i][0] * (self.endpoints[(i + 1) % len(self.endpoints)][1] - self.endpoints[i - 1][1])
        return 0.5 * A



trench_map_txt = open("input.txt")
trench_map_lines = trench_map_txt.read().strip().split("\n")
trench_map = [item.split() for item in trench_map_lines]

holes = Hole()
for item in trench_map:
    #holes.digHole(item[0], int(item[1]), item[2])
    holes.digHexHole(item[2].replace("(", "").replace(")", ""))

print(holes.calcArea())