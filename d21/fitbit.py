class GardenPath():
    def __init__(self, map, steps=64):
        self.Garden = map
        self.Steps = steps

    def gardenBFS(self, start=None):
        if start == None:
            start = self.findStart()
        valid_endpts = []
        frontier = []
        visited = []
        origin = (start[0], start[1], 0) # x, y, dist from start
        frontier.append(origin)
        while len(frontier) > 0:
            frontier.sort(key = lambda x : x[2])
            here = frontier.pop(0)
            if here[2] > self.Steps:
                return valid_endpts
            for n in self.getNeighbors(here):
                dist = here[2] + 1
                if dist % 2 == 0 and n not in valid_endpts:
                    valid_endpts.append(n)
                if n not in visited:
                    visited.append(n)
                    frontier.append((n[0], n[1], dist))
        return valid_endpts

    def getNeighbors(self, l):
        neighbors = []
        x = l[0]
        y = l[1]
        if x > 0:
            if self.Garden[x -1][y] != '#':
                neighbors.append((x - 1, y))
        if y > 0:
            if self.Garden[x][y - 1] != '#':
                neighbors.append((x, y - 1))
        if x < len(self.Garden) - 1:
            if self.Garden[x +1][y] != '#':
                neighbors.append((x + 1, y))
        if y < len(self.Garden[0]) - 1:
            if self.Garden[x][y + 1] != '#':
                neighbors.append((x, y + 1))
        return neighbors
    
    def findStart(self):
        for i in range(len(self.Garden)):
            for j in range(len(self.Garden[0])):
                if self.Garden[i][j] == 'S':
                    return (i, j)
        return (-1, -1)
        


input_str = open("easy_input.txt").read().strip().split("\n")
elf = GardenPath(input_str, 64)
path = elf.gardenBFS()
print(len(path))