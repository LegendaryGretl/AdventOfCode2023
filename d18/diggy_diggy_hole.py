trench_map_txt = open("input.txt")
trench_map = trench_map_txt.read().strip().split("\n")
trench_map = [item.split() for item in trench_map]


dig = [[0, 0]]

i = 0
pos = 0
for row in trench_map:
    row[1] = int(row[1])
    if row[0] == "L":
        pos -= row[1]
        if pos < dig[i][0]:
            dig[i][0] = pos
    elif row[0] == "R":
        pos += row[1]
        if pos > dig[i][1]:
            dig[i][1] = pos
    elif row[0] == "U":
        i -= row[1]
        while i < 0:
            dig.insert(0, [pos, pos])
            i += 1
        for k in range(i, i+row[1]):
            if pos < dig[k][0]:
                dig[k][0] = pos
            if pos > dig[k][1]:
                dig[k][1] = pos
    elif row[0] == "D":
        i += row[1]
        while i > len(dig) - 1:
            dig.append([pos, pos])
        for k in range(i - row[1], i):
            if pos < dig[k][0]:
                dig[k][0] = pos
            if pos > dig[k][1]:
                dig[k][1] = pos

sum = 0
for item in dig:
    sum += item[1] - item[0] + 1

print(sum)
print(dig)