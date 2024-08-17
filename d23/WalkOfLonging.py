class HikingMap():
    def __init__(self, input_str):
        self.Map = input_str.strip().split("\n")
        self.start = (0, 1)
        self.end = (len(self.Map) - 1, len(self.Map[0]) - 2)

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
    

input_str = open("input.txt").read()
forest = HikingMap(input_str)
path = forest.DFS()
print("Part 1:", len(path) - 1)
# for row in range(len(forest.Map)):
#     for col in range(len(forest.Map[0])):
#         if (row, col) in path:
#             print("O", end="")
#         else:
#             print(forest.Map[row][col], end="")
#     print("")