import math

def steps_to_end_with_z(cur_loc, loc_dict, route):
    i = 0
    while cur_loc[-1] != "Z":
        p = i % len(route)
        if route[p] == "L":
            cur_loc = loc_dict[cur_loc][0]
        elif route[p] == "R":
            cur_loc = loc_dict[cur_loc][1]
        else:
            print("error:", route[p])
        i += 1
    return i


map_txt = open("input.txt")

map_lines = map_txt.read().strip().split("\n")
route = map_lines[0]

loc_dict = {}

for line in map_lines[2:]:
    if len(line) < 1:
        continue
    temp = line.replace(" ", "").split("=")
    lnr = temp[1].replace("(", "").replace(")", "").split(",")
    loc_dict[temp[0]] = lnr

cur_loc = "AAA"

i = 0
while cur_loc != "ZZZ":
    p = i % len(route)
    if route[p] == "L":
        cur_loc = loc_dict[cur_loc][0]
    elif route[p] == "R":
        cur_loc = loc_dict[cur_loc][1]
    else:
        print("error:", route[p])
    i += 1

ghost_loc = []
for key in loc_dict.keys():
    if key[-1] == "A":
        ghost_loc.append(key)

# i = 0
# ghost_end = False
# while not ghost_end:
#     p = i % len(route)
#     ghost_end = True
#     for k in range(len(ghost_loc)):
#         if route[p] == "L":
#             ghost_loc[k] = loc_dict[ghost_loc[k]][0]
#         elif route[p] == "R":
#             ghost_loc[k] = loc_dict[ghost_loc[k]][1]
#         else:
#             print("error:", route[p])
#         if ghost_loc[k][-1] != "Z":
#             ghost_end = False
#         else:
#             pass
#     i += 1

steps = []
for item in ghost_loc:
    steps.append(steps_to_end_with_z(item, loc_dict, route))

print(math.lcm(steps[0], steps[1], steps[2], steps[3], steps[4], steps[5]))
