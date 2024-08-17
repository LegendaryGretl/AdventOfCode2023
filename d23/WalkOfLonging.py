import time


class HikingMap():
    def __init__(self, input_str):
        self.Map = input_str.strip().split("\n")
        self.start = (0, 1)
        self.end = (len(self.Map) - 1, len(self.Map[0]) - 2)
        self.cross = self.findCrossRoads()
        self.crossMap = self.findCrossroadPaths()


    def getNextSteps(self, coords, slippery=False):
        if slippery:
            return self.getNextSteps_internal(coords[0], coords[1])
        else:
            return self.getNextSteps_internal_noslip(coords[0], coords[1])


    def getNextSteps_internal(self, row, col):
        tile = self.Map[row][col]
        valid_steps = []

        if tile == "#":
            return []
        elif tile == "^":
            return [(row-1, col)]
        elif tile == ">":
            return [(row, col + 1)]
        elif tile == "v":
            return [(row + 1, col)]
        elif tile == "<":
            return [(row, col - 1)]
        
        if row - 1 >= 0 and self.Map[row -1][col] != "#":
            valid_steps.append((row - 1, col))
        if row + 1 < len(self.Map) and self.Map[row +1][col] != "#":
            valid_steps.append((row + 1, col))
        if col - 1 >= 0 and self.Map[row][col - 1] != "#":
            valid_steps.append((row, col - 1))
        if col + 1 < len(self.Map[0]) and self.Map[row][col + 1] != "#":
            valid_steps.append((row, col + 1))

        return valid_steps
    

    def getNextSteps_internal_noslip(self, row, col):
        tile = self.Map[row][col]
        valid_steps = []

        if tile == "#":
            return []
        
        if row - 1 >= 0 and self.Map[row -1][col] != "#":
            valid_steps.append((row - 1, col))
        if row + 1 < len(self.Map) and self.Map[row +1][col] != "#":
            valid_steps.append((row + 1, col))
        if col - 1 >= 0 and self.Map[row][col - 1] != "#":
            valid_steps.append((row, col - 1))
        if col + 1 < len(self.Map[0]) and self.Map[row][col + 1] != "#":
            valid_steps.append((row, col + 1))

        return valid_steps


    def findCrossRoads(self):
        cross = []
        for row in range(len(self.Map)):
            for col in range(len(self.Map[0])):
                if len(self.getNextSteps((row, col), False)) > 2:
                    cross.append((row, col))
        cross.append(self.start)
        cross.append(self.end)
        return cross
    

    def DFS(self):
        paths = []
        longest_path = []
        paths.append([self.start])
        while len(paths) > 0:
            cur_path = paths.pop()
            last_step = cur_path[-1]
            for step in self.getNextSteps(last_step):
                if step == self.end:
                    if len(cur_path) + 1 > len(longest_path):
                        longest_path = cur_path + [step]
                elif step not in cur_path:
                    paths.append(cur_path + [step])
        return longest_path
    

    def DFSBetweenCrossroads(self):
        paths = []
        longest_path_len = -1
        paths.append(([self.start], 0)) # array of [path], dist
        while len(paths) > 0:
            cur_path, dist = paths.pop()
            last_step = cur_path[-1]
            for cross, delta in self.crossMap[last_step]:
                if cross == self.end:
                    if dist + delta > longest_path_len:
                        longest_path_len = dist + delta
                elif cross not in cur_path:
                    paths.append((cur_path + [cross], dist + delta))
        return longest_path_len
    

    def findCrossroadPaths(self):
        crossMap = {} # cross: [(endpt, dist), ..., (endpt, dist)]
        for c in self.cross:
            crossMap[c]  = self.crossroadBFS(c)
        return crossMap
                

    def crossroadBFS(self, cross):
        paths = []
        endpoints = [] # endpoint, distance
        for item in self.getNextSteps(cross):
            paths.append([cross, item])
        while len(paths) > 0:
            curr_path = paths.pop(0)
            here = curr_path[-1]
            next = self.getNextSteps(here)
            if here == self.end or len(next) > 2: # end or adjacent crossroad
                endpoints.append((here, len(curr_path) - 1))
            else:
                for step in next:
                    if step not in curr_path:
                        paths.append(curr_path + [step])
        return endpoints

    


input_str = open("input.txt").read()
forest = HikingMap(input_str)
# t0 = time.time()
# path = forest.DFS()
# t1 = time.time()
# print("Part 1:", len(path) - 1, 1000*(t1 - t0))
t0 = time.time()
travail = forest.DFSBetweenCrossroads()
t1 = time.time()
print("Part 2:", travail, 1000*(t1 - t0))
# for row in range(len(forest.Map)):
#     for col in range(len(forest.Map[0])):
#         if (row, col) in path:
#             print("O", end="")
#         else:
#             print(forest.Map[row][col], end="")
#     print("")