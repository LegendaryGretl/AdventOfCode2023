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

rock_map_txt = open("input.txt")
rock_map = rock_map_txt.read().strip().split("\n")
backward_rock_map = rock_map[::-1]

sum = 0
for row in range(len(rock_map)):
    for col in range(len(rock_map[row])):
        if rock_map[row][col] == "O":
            sum += calc_force_north((row, col), rock_map)
print(sum)