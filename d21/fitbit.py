import numpy as np
import math

class GardenPath():
    def __init__(self, map, steps=64):
        self.Garden = map
        self.Steps = steps


    def stepsInInfiniteGardenRedux(self, steps=None):
        # source: https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
        if steps != None:
            self.Steps = steps

        l = len(self.Garden)
        w = l // 2
        assert w == 65
        n = (steps - w) / l
        assert n == 202300

        visited = self.gardenBFSRecord()
        even_corners = len([item for item in visited if item[1] % 2 == 0 and item[1] > 65])
        odd_corners = len([item for item in visited if item[1] % 2 == 1 and item[1] > 65])
        even_full = len([item for item in visited if item[1] % 2 == 0])
        odd_full = len([item for item in visited if item[1] % 2 == 1])
        
        return ((n + 1) ** 2) * odd_full + (n ** 2) * even_full - ((n + 1) * odd_corners) + (n * even_corners)

    def stepsInInfiniteGarden(self, steps=None):
        # source: https://www.reddit.com/r/adventofcode/comments/18o4y0m/2023_day_21_part_2_algebraic_solution_using_only/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
        if steps != None:
            self.Steps = steps
        
        w = len(self.Garden)
        start = (int((w - 1)/2), int((w - 1)/2))
        N = int((self.Steps - start[0]) / w)
        uneven = N % 2 == 0
        E = len(self.gardenBFS(start, self.Steps, False))
        O = len(self.gardenBFS(start, self.Steps, True))

        Sa = int((3*w - 1) / 2) - 1 
        Sb = int((w - 1) / 2) 
        St = w - 1

        A = len(self.gardenBFS((0, 0), Sa, True))
        A += len(self.gardenBFS((0, w - 1), Sa, True))
        A += len(self.gardenBFS((w - 1, 0), Sa, True))
        A += len(self.gardenBFS((w - 1, w - 1), Sa, True))

        B = len(self.gardenBFS((0, 0), Sb, False))
        B += len(self.gardenBFS((0, w - 1), Sb, False))
        B += len(self.gardenBFS((w - 1, 0), Sb, False))
        B += len(self.gardenBFS((w - 1, w - 1), Sb, False))

        T = len(self.gardenBFS((0, start[0]), St, uneven))
        T += len(self.gardenBFS((start[0], 0), St, uneven))
        T += len(self.gardenBFS((w - 1, start[0]), St, uneven))
        T += len(self.gardenBFS((start[0], w - 1), St, uneven))

        # return ((N + 1) ** 2) * O + (N ** 2) * E + ((N + 1) **2) * A + N * B

        return ((N - 1) ** 2) * O + (N ** 2) * E + (N - 1) * A + N * B + T

    def gardenBFSRecord(self, limit = None):
        start = self.findStart()
        frontier = []
        visited = {}
        origin = (start[0], start[1], 0) # x, y, dist from start
        frontier.append(origin)
        # visited.append((start, 0))
        while len(frontier) > 0:
            frontier.sort(key = lambda x : x[2])
            here = frontier.pop(0)
            if limit != None and here[2] > limit:
                return visited
            if (here[0], here[1]) in visited:
                continue
            visited[(here[0], here[1])] = here[2]
            for n in self.getNeighbors(here):
                dist = here[2] + 1
                if n not in visited:
                    # visited.append((n, dist))
                    frontier.append((n[0], n[1], dist))
        return visited
    
    def gardenBFSRecord3(self, limit=None):
        start = self.findStart()
        frontier = []
        visited = {}
        odd = {}
        even = {}
        origin = (start[0], start[1], 0) # x, y, dist from start
        frontier.append(origin)
        # visited.append((start, 0))
        while len(frontier) > 0:
            frontier.sort(key = lambda x : x[2])
            here = frontier.pop(0)
            h = (here[0], here[1])

            if limit != None and here[2] > limit:
                return visited, odd, even

            # if here[2] % 2 == 0 and h not in even:
            #     even[h] = here[2]
            # elif here[2] % 2 == 1 and h not in odd:
            #     odd[h] = here[2]
   
            if h in visited:
                continue
            else:
                visited[h] = here[2]
                if here[2] % 2 == 0 and h not in even:
                    even[h] = here[2]
                elif here[2] % 2 == 1 and h not in odd:
                    odd[h] = here[2]

            for n in self.getNeighbors(here):
                dist = here[2] + 1
                if n not in visited:
                    # visited.append((n, dist))
                    frontier.append((n[0], n[1], dist))
        return visited, odd, even

    def gardenBFSRecord2(self, limit = None):
        start = self.findStart()
        frontier = []
        visited = []
        odd = {}
        even = {}
        origin = (start[0], start[1], 0) # x, y, dist from start
        frontier.append(origin)
        # visited.append((start, 0))
        while len(frontier) > 0:
            frontier.sort(key = lambda x : x[2])
            here = frontier.pop(0)

            if limit != None and here[2] > limit:
                return odd, even
            
            # check even/oddness of step number
            if here[2] % 2 == 0 and (here[0], here[1]) not in even:
                even[(here[0], here[1])] = here[2]
            elif here[2] % 2 == 1 and (here[0], here[1]) not in odd:
                odd[(here[0], here[1])] = here[2]

            if (here[0], here[1]) in visited:
                continue
            visited.append((here[0], here[1]))
            
            for n in self.getNeighbors(here):
                dist = here[2] + 1
                if n not in visited:
                    # visited.append((n, dist))
                    frontier.append((n[0], n[1], dist))
        return odd, even

    def gardenBFS(self, start=None, steps=None, uneven = None):
        if start == None:
            start = self.findStart()
        if steps == None:
            steps = self.Steps

        # start_status = (start[0] + start[1] + steps) % 2
        # if uneven:
        #     start_status = 1 - start_status
        if uneven != None:
            if uneven:
                start_status = 1
            else:
                start_status = 0
        else:
            start_status = steps % 2
        valid_endpts = []
        frontier = []
        visited = []
        origin = (start[0], start[1], 0) # x, y, dist from start
        frontier.append(origin)
        while len(frontier) > 0:
            frontier.sort(key = lambda x : x[2])
            here = frontier.pop(0)
            if here[2] > steps:
                return valid_endpts
            for n in self.getNeighbors(here):
                dist = here[2] + 1
                if dist % 2 == start_status and n not in valid_endpts:
                # if (dist) % 2 == start_status and n not in valid_endpts:
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
        


input_str = open("input.txt").read().strip().split("\n")
clean_input_str = input_str[:]
half = 65
full = 131
repeats = 21

b = half
# b = 5
assert clean_input_str[b][b] == 'S'

clean_input_str[b] = clean_input_str[b][:b] + '.' + clean_input_str[b][b + 1:]
triple_in = ""
for line in clean_input_str:
    for i in range(repeats):
        triple_in += line
    triple_in += '\n'
triple_in *= repeats
b = math.ceil(repeats/2)*full + half
# b = 2*11 + 5
triple_in = triple_in.strip().split('\n')
triple_in[b] = triple_in[b][:b] + 'S' + triple_in[b][b + 1:]

# for line in triple_in:
#     print(line)

# triple_in= triple_in[:9*b*b] + 'S' + triple_in[9*b*b + 1:]
# output = open("triple_input.txt", "w").write(triple_in)
# elf = GardenPath(input_str, 26501365)
elf = GardenPath(triple_in, 26501365)
# path = elf.gardenBFS(steps=64)
# print("Part 1:", len(path))
# visited = elf.gardenBFSRecord()
# print("Part 1:", len([v for v in visited if v[1] < 65 and v[1] % 2 == 0]))

# 617238327466724 -> too high, 617238274464002 -> still too high
# 617238381686528 -> wrong
# 612491040764126 -> wrong
# 612490971172814 -> wrong
# 614864614526528 -> wrong
# 614864684116928 -> wrong
# 614864614930614 -> wrong
# 172544738287914 -> wrong
# 614864627270946 -> wrong
# 614864614526013 - > wrong
# steps = elf.stepsInInfiniteGarden(26501365)
# steps = elf.stepsInInfiniteGardenRedux(26501365)
# steps = elf.stepsInInfiniteGarden(50)
# print("Part 2:", steps)

# t_arr = [6, 10, 50, 100]

# for t in t_arr:
#     test = elf.gardenBFS(steps=t)
#     print(len(test))

s = [half, full + half, 2*full + half]

# test = elf.gardenBFS(steps=half)
# visited, odd, even = elf.gardenBFSRecord3(half)
# print(len(test))
# print(len(visited), len(odd), len(even))


# p1 = len(elf.gardenBFS(steps=s[0]))
# p2 = len(elf.gardenBFS(steps=s[1]))
# p3 = len(elf.gardenBFS(steps=s[2]))
# visited = elf.gardenBFSRecord(s[2])
visited, odd, even = elf.gardenBFSRecord3(s[2])
test = len([k for k, v in even.items() if v <= half])
p1 = len([k for k, v in odd.items() if v <= s[0]])
p2 = len([k for k, v in even.items() if v <= s[1]])
p3 = len([k for k, v in odd.items() if v <= s[2]])

p1p = len([k for k, v in even.items() if v <= s[0]])
p2p = len([k for k, v in odd.items() if v <= s[1]])
p3p = len([k for k, v in even.items() if v <= s[2]])

# p1p = len([k for k, v in visited.items() if v <= s[0]])
# p2p = len([k for k, v in visited.items() if v <= s[1]])
# p3p = len([k for k, v in visited.items() if v <= s[2]])


# p1 = 3846 
# p2 = 34047 
# p3 = 94296

# cof = np.polyfit(s, [p1, p2, p3], 2)
points = [(0, p1), (1, p2), (2, p3)]
# cof = np.polyfit([0, 1, 2], [p1, p2, p3], 2)
cof = np.polyfit(*zip(*points), 2)
# x = 26501365
x = 202300
print(test)
print(p1, p2, p3)
print(p1p, p2p, p3p)
# print("Estimate part 2:", cof[0] * (x**2) + cof[1] * x + cof[2])
print(cof)
print("Part 2:", np.polyval(cof, x))

print(3802 + 15021 * x + 14909 * (x **2))