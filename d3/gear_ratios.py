# define helper functions
def is_adjacent(array, center, comp):
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            if array[center[0] + i][center[1] + j] == array[comp[0] + i][comp[1] + j]:
                return True
    return False

def adjacent_to_symbol(symb_idx_arr, row, col):
    # prevent going out of bounds
    if row < 1:
        start = 0
    else:
        start = row-1
    if row >= len(symb_idx_arr) -1:
        stop = row
    else:
        stop = row + 1
    
    for row in symb_idx_arr[start: stop + 1]:
        for c in [col - 1, col, col + 1]:
            # if c is smaller than the smaller idx or larger than the largest
            # skip and go onto the next
            # also skip if row is empty
            if (len(row) < 1) or (c < row[0]) or (c > row[-1]):
                continue
            if c in row:
                return True
    return False

def adjacent_num_locations(array, center):
    new_nums = []
    for i in [-1, 0, 1]:
        streak = False # use this var to make sure you aren't recording the same number twice
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                streak = False
                continue
            if ((center[0] + i) < 0) or ((center[0] + i) >= len(array)):
                streak = False
                continue
            if ((center[1] + j) < 0) or ((center[1] + j) >= len(array)):
                streak = False
                continue
            if (array[center[0] + i][center[1] + j]).isnumeric():
                if not streak:
                    new_nums.append([center[0] + i, center[1] + j])
                streak = True
            else:
                streak = False
    return new_nums

schematic = open("input.txt")

lines = schematic.read().split("\n")

spec_char_loc = []
potential_gears = []
for line in lines:
    line_char_loc = [pos for pos, char in enumerate(line) if (not (char.isnumeric() or char == ".")) ]
    line_gears = [pos for pos, char in enumerate(line) if char == "*" ]
    spec_char_loc.append(line_char_loc)
    potential_gears.append(line_gears)

row = 0
col = 0
sum = 0
while row < len(spec_char_loc):
    while col < len(lines[row]):
        new_num = 0
        if not lines[row][col].isnumeric():
            col += 1
            continue

        adj_to_symbol = False
        while True:
            new_num = new_num*10 + int(lines[row][col])
            if adjacent_to_symbol(spec_char_loc, row, col):
                adj_to_symbol = True
            col += 1
            if (col >= len(lines[row])) or (not lines[row][col].isnumeric()):
                break
        if adj_to_symbol == False:
            new_num = 0
        # if new_num > 0:
        #     print(row, col, new_num)
        sum += new_num
    # reset column number, increment row number
    row += 1
    col = 0

print(sum)

sum = 0
for row in range(len(potential_gears)):
    for gear in potential_gears[row]:
        new_num = 0
        adjacents = adjacent_num_locations(lines, (row, gear))
        if len(adjacents) != 2:
            continue
        new_num = 1
        for temp_r, temp_c in adjacents:
            temp_num = 0
            line = lines[temp_r]
            while (temp_c > 0) and (line[temp_c - 1].isnumeric()):
                temp_c -= 1
            while True:
                temp_num = temp_num*10 + int(lines[temp_r][temp_c])
                temp_c += 1
                if (temp_c >= len(lines[row])) or (not line[temp_c].isnumeric()):
                    break
            new_num *= temp_num
        sum += new_num
        print(row, gear, new_num)

print(sum)
            

