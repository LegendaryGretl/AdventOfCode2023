def add_h_pos_to_dict(h, v, dict):
    list = [h, h]
    if v in dig_dict.keys():
        list = dict[v]
        if h < dict[v][0]:
            list[0] = h
        if h > dict[v][1]:
            list[1] = h
    return list

dig_plan_txt = open("easy_input.txt")
dig_plan = dig_plan_txt.read().strip().split("\n")
dig_plan = [item.split() for item in dig_plan]
# print(dig_plan)

horz = 0
vert = 0
dig_dict = {}
dig_coords = [(0, 0)]
perim = 0
for entry in dig_plan:
    entry[1] = int(entry[1])
    perim += entry[1]
    if entry[0] == "L":
        horz -= entry[1]
        dig_coords.append((horz, vert))
        dig_dict[vert] = add_h_pos_to_dict(horz, vert, dig_dict)
    elif entry[0] == "R":
        horz += entry[1]
        dig_coords.append((horz, vert))
        dig_dict[vert] = add_h_pos_to_dict(horz, vert, dig_dict)
    elif entry[0] == "U":
        v_end = vert - entry[1]
        dig_coords.append((horz, v_end))
        while vert > v_end:
            vert -= 1
            dig_dict[vert] = add_h_pos_to_dict(horz, vert, dig_dict)         
        vert = v_end
    elif entry[0] == "D":
        v_end = vert + entry[1]
        dig_coords.append((horz, v_end))
        while vert < v_end:
            vert += 1
            dig_dict[vert] = add_h_pos_to_dict(horz, vert, dig_dict)
        vert = v_end
         

sum = 0
for k in dig_dict.keys():
    # print(k, dig_dict[k])
    l = dig_dict[k]
    sum += l[1] - l[0] + 1
print(sum)

i = 0
area = 0
while i < len(dig_coords):
    x1, y1 = dig_coords[i]
    x2, y2 = dig_coords[(i + 1) % len(dig_coords)]
    area += x1*y2 - x2*y1
    i += 1
# x1, y1 = dig_coords[i]
# x2, y2 = dig_coords[0]
# area += x1*y2 - x2*y1

print(area/2)
print(area + perim/2 + 1)