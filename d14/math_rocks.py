import copy

def calc_force_north(coord, map):
    f_max = len(map)
    num_obs = 0
    for row in reversed(range(0, coord[0])):
        if map[row][coord[1]] == "O":
            num_obs += 1
        elif map[row][coord[1]] == "#":
            f_max = len(map) - row -1
            break
    return f_max - num_obs

def calc_no_roll(map):
    force = 0
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "O":
                force += len(map) - row
    return force

def blank_map(map):
    blank = copy.deepcopy(map)
    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == "O":
                blank[row][col] = "."
    return blank

def roll_north(map):
    new_map = blank_map(map)
    for col in range(len(map[0])):
        for row in range(len(map)):
            if map[row][col] == "O":
                r = row
                while r > 0 and new_map[r - 1][col]== ".":
                    r -= 1          
                if r ==0:
                    new_map[r][col] = "O"
                elif new_map[r ][col] == ".":
                    new_map[r][col] = "O"
    return new_map

rock_map_txt = open("input.txt")
rock_map = rock_map_txt.read().strip().split("\n")
backward_rock_map = rock_map[::-1]

sum = 0
for row in range(len(rock_map)):
    for col in range(len(rock_map[row])):
        if rock_map[row][col] == "O":
            sum += calc_force_north((row, col), rock_map)
print(sum)

rock_listy = [list(row) for row in rock_map]
blank = blank_map(rock_listy)
# print(rock_listy, "\n\n", blank)

# for item in roll_north(rock_listy):
#     print(item)
# print(roll_north(rock_listy))
    
cur_map = rock_listy
prev_map = blank_map(rock_listy)

prev_maps =[]

cycles = -1
while cur_map not in prev_maps:
    prev_map = copy.deepcopy(cur_map)
    # n
    cur_map = roll_north(prev_map)
    # e
    cur_map = roll_north([list(e) for e in zip(*cur_map[::-1])])
    # s
    cur_map = roll_north([list(e) for e in zip(*cur_map[::-1])])
    # w
    cur_map = roll_north([list(e) for e in zip(*cur_map[::-1])])
    # north again
    cur_map = [list(e) for e in zip(*cur_map[::-1])]
    # if cycles < 3:
    #     for item in cur_map:
    #         print(item)
    #     print("\n\n")
    # else:
    #     break
    cycles += 1
    if cycles % 1000 == 0:
        print(cycles)
    if cycles > 1000000000:
        break
    if cycles > 0:
        prev_maps.append(prev_map)

idx = prev_maps.index(cur_map)
cycle = prev_maps[idx+1:]
cycle.append(cur_map)
cycles += 1

print(len(cycle), (1000000000-cycles) % (len(cycle)), calc_no_roll(cycle[(1000000000-cycles) % (len(cycle)) - 1]))

# for i in range(len(cycle)):
#     print (i, calc_no_roll(cycle[i]))
# print(calc_no_roll(cur_map))
