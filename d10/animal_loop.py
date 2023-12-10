pipe_dict = {"|":("N", "S"), "-": ("E", "W"), "L": ("N", "E"), \
             "J": ("N", "W"), "7": ("S", "W"), "F": ("S", "E"), ".":()}

def move_in_pipes(start, pipe_map, entry_direction):
    pipe_type = pipe_map[start[0]][start[1]]
    if pipe_type == "S":
        directions = []
        if start[0] > 0:
            north = pipe_map[start[0] - 1][start[1]]
            if "S" in pipe_dict[north]:
                directions.append("N")
        if start[0] < len(pipe_map) -1:
            south = pipe_map[start[0] + 1][start[1]]
            if "N" in pipe_dict[south]:
                directions.append("S")
        if start[1] > 0:
            west = pipe_map[start[0]][start[1] - 1]
            if "E" in pipe_dict[west]:
                directions.append("W")
        if start[1] < len(pipe_map[0]) -1:
            east = pipe_map[start[0]][start[1] + 1]
            if "W" in pipe_dict[east]:
                directions.append("E")
        return directions
    elif pipe_type == ".":
        print("Error: pipe loop has been breached")
        return -1
    else:
        for item in pipe_dict[pipe_type]:
            if item != entry_direction:
                return traverse_pipe(start, item)
        print("Error: exit is not possible")
        return -1
    
def traverse_pipe(start, direction):
    if direction == "N":
        return (start[0] - 1, start[1]), "S"
    if direction == "S":
        return (start[0] + 1, start[1]), "N"
    if direction == "E":
        return (start[0], start[1] + 1), "W"
    if direction == "W":
        return (start[0], start[1] - 1), "E"
    
def count_crossings(start, direction, loop_path):
    loc = [start[0], start[1]]
    crossings = 0
    if direction == "N":
        while (loc[0] > 0):
            loc[0] -= 1
            if (loc[0], loc[1]) in loop_path:
                crossings += 1
                # idx = loop_path.index((loc[0], loc[1]))
                # try: 
                #     if (loc[0] - 1, loc[1]) == loop_path[idx - 1]:
                #         while (idx > 0) and ((loc[0] - 1, loc[1]) == loop_path[idx - 1]):
                #             idx -=1 
                #             loc[0] -= 1
                #     elif (loc[0] - 1, loc[1]) == loop_path[idx + 1]:
                #         while (idx < len(loop_path) - 1) and ((loc[0] - 1, loc[1]) == loop_path[idx + 1]):
                #             idx +=1 
                #             loc[0] -= 1
                # except:
                #     pass
    if direction == "S":
        while (loc[0] < len(pipe_map) - 1):
            loc[0] += 1
            if (loc[0], loc[1]) in loop_path:
                crossings += 1
    if direction == "W":
        while (loc[1] > 0):
            loc[1] -= 1
            if (loc[0], loc[1]) in loop_path:
                crossings += 1
    if direction == "E":
        while (loc[1] < len(pipe_map[0]) - 1):
            loc[1] += 1
            if (loc[0], loc[1]) in loop_path:
                crossings += 1
    return crossings

def count_crossings_diag(start, loop_path):
    loc = [start[0], start[1]]
    crossings = 0
    while (loc[0] > 0) and (loc[1] > 0):
        loc[0] -= 1
        loc[1] -= 1
        if (loc[0], loc[1]) in loop_path:
            crossings += 1
    if crossings % 2 == 0:
        return crossings
    crossings = 0
    loc = [start[0], start[1]]
    while (loc[0] < len(pipe_map) -1 ) and (loc[1] < len(pipe_map[0]) -1):
        loc[0] += 1
        loc[1] += 1
        if (loc[0], loc[1]) in loop_path:
            crossings += 1
    return crossings

    
pipes_txt = open("medium_input.txt")
pipe_map = pipes_txt.read().strip().split("\n")

# find S
for i in range(len(pipe_map)):
    if pipe_map[i].find("S") != -1:
        starting_pos = (i, pipe_map[i].find("S"))
        break

directions = move_in_pipes(starting_pos, pipe_map, None)
pipe_0, dir_0= traverse_pipe(starting_pos, directions[0])
path0 = []
path0.append(pipe_0)
pipe_1, dir_1= traverse_pipe(starting_pos, directions[1])
path1 = []
path1.append(pipe_1)
dist = 1
while (pipe_0[0] != pipe_1[0]) or (pipe_0[1] != pipe_1[1]):
    pipe_0, dir_0 = move_in_pipes(pipe_0, pipe_map, dir_0)
    pipe_1, dir_1 = move_in_pipes(pipe_1, pipe_map, dir_1)
    path0.append(pipe_0)
    path1.append(pipe_1)
    dist +=1 
print(dist)

path1.pop()
path1.reverse()
full_path = [starting_pos] + path0 + path1

enclosed = 0
for r in range(len(pipe_map)):
    for c in range(len(pipe_map[r])):
        if pipe_map[r][c] != ".":
            continue
        # jank = 0
        # if count_crossings((r, c), "N", full_path) % 2 == 0:
        #     jank += 1
        # if count_crossings((r, c), "S", full_path) % 2 == 0:
        #     jank += 1    
        # if count_crossings((r, c), "E", full_path) % 2 == 0:
        #     jank += 1
        # if count_crossings((r, c), "W", full_path) % 2 == 0:
        #     jank += 1
        # if jank < 3:
        #     enclosed += 1
        if count_crossings_diag((r, c), full_path) %2 == 0:
            continue
        enclosed += 1

print(enclosed)