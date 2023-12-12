import copy

galaxies_txt = open("input.txt")

compressed_space = galaxies_txt.read().strip().split("\n")

non_empty_row_nums = set()
non_empty_col_nums = set()
all_rows = set()
all_cols = set()

for row in range(len(compressed_space)):
    for col in range(len(compressed_space[row])):
        if compressed_space[row][col] == "#":
            non_empty_row_nums.add(row)
            non_empty_col_nums.add(col)
        all_rows.add(row)
        all_cols.add(col)
            

expanded_space = copy.deepcopy(compressed_space)

row_offset = 0
for row in range(len(compressed_space)):
    col_offset = 0
    for col in range(len(compressed_space[row])):
        if col not in non_empty_col_nums:
           expanded_space[row+ row_offset] = expanded_space[row+ row_offset][:col + col_offset] + "." + expanded_space[row+ row_offset][col + col_offset:] 
           col_offset += 1
    if row not in non_empty_row_nums:
        expanded_space.insert(row + row_offset, expanded_space[row+ row_offset])
        row_offset += 1

list_o_gals = []
for row in range(len(expanded_space)):
    for col in range(len(expanded_space[row])):
        if expanded_space[row][col] == "#":
            list_o_gals.append((row, col))

sum = 0
for i in range(len(list_o_gals)):
    base_gal = list_o_gals[i]
    for gal in list_o_gals[i+1:]:
        sum += abs(base_gal[0] - gal[0]) + abs(base_gal[1] - gal[1])

# for item in expanded_space:
#     print(item)

print(sum)

# part 2

empty_rows = all_rows.difference(non_empty_row_nums)
empty_cols = all_cols.difference(non_empty_col_nums)

list_o_gals = []
for row in range(len(compressed_space)):
    for col in range(len(compressed_space[row])):
        if compressed_space[row][col] == "#":
            list_o_gals.append((row, col))

sum = 0
for i in range(len(list_o_gals)):
    base_gal = list_o_gals[i]
    for gal in list_o_gals[i+1:]:
        sum += abs(base_gal[0] - gal[0]) + abs(base_gal[1] - gal[1])
        if base_gal[0] < gal[0]:
            s_row = base_gal[0]
            e_row = gal[0]
        else:
            e_row = base_gal[0]
            s_row = gal[0]
        if base_gal[1] < gal[1]:
            s_col = base_gal[1]
            e_col = gal[1]
        else:
            e_col = base_gal[1]
            s_col = gal[1]
        for row in range(s_row, e_row):
            if row in empty_rows:
                sum += 1000000 -1 
        for col in range(s_col, e_col):
            if col in empty_cols:
                sum += 1000000 -1
                
print(sum)