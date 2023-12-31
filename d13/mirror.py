import math

def find_horz_mirroring(col):
    for h in range(1, len(col)):
        h_b = True
        if h <= math.floor(len(col) / 2):
            # print(h, ":", col[h:2*h], (col[:h])[::-1])
            if col[h:2*h] != (col[:h])[::-1]:
                h_b = False
                continue
        else:
            # print(h, ":", (col[h:])[::-1], col[h - len(col[h:]):h])
            if (col[h:])[::-1] != col[h - len(col[h:]):h]:
                h_b = False           
                continue
        if h_b:
            return h
    return -1

def find_smudge(a, b):
    diffs = 0
    idx = -1
    for i in range(len(a)):
        if a[i] != b[i]:
            idx = i
            diffs += 1
    if diffs == 1:
        return idx
    else:
        return -1
    
print(find_smudge("##.", "###"))

map_txt = open("input.txt")
map_list = map_txt.read().strip().split("\n\n")
map_list = [m.split("\n") for m in map_list]

# part 1
sum_h = 0
sum_v = 0
inc = 0
for map in map_list:
    h_p = []
    v_p = []
    col = "".join(l for l in [item[0] for item in map])
    row = map[0]
    
    # print("horz: ")
    for h in range(1, len(col)):
        h_b = True
        for i in range(len(map[0])):
            try:
                col = "".join(l for l in [item[i] for item in map])
            except:
                print(map, i)
            if h <= math.floor(len(col) / 2):
                # print(h, ":", col[h:2*h], (col[:h])[::-1])
                if col[h:2*h] != (col[:h])[::-1]:
                    h_b = False
                    break
            else:
                # print(h, ":", (col[h:])[::-1], col[h - len(col[h:]):h])
                if (col[h:])[::-1] != col[h - len(col[h:]):h]:
                    h_b = False
                    break
        if h_b:
            h_p.append(h)
            break

    # print("vert:")
    for v in range(1, len(row)):
        v_b = True
        for i in range(len(map)):
            row = map[i]
            if v <= math.floor(len(row) / 2):
                # print(v, ":", row[v:2*v], (row[:v])[::-1])
                if row[v:2*v] != (row[:v])[::-1]:
                    v_b = False
                    break
            else:
                # print(v, ":", (row[v:])[::-1], row[v - len(row[v:]):v])
                if (row[v:])[::-1] != row[v - len(row[v:]):v]:
                    v_b = False
                    break
        if v_b:
            v_p.append(v)
            break
    if len(h_p) > 0:
        sum_h += max(h_p)
    if len(v_p) > 0:
        sum_v += max(v_p)
    if len(h_p) + len(v_p) == 0:
        print(inc, ":", h_p, v_p)
        print(map)
    inc += 1

# print(sum_v + 100*sum_h)


# part 2
sum_h = 0
sum_v = 0
inc = 0
for map in map_list:
    h_p = []
    v_p = []
    col = "".join(l for l in [item[0] for item in map])
    row = map[0]
    
    # print("horz: ")
    for h in range(1, len(col)):
        h_b = True
        inc = 0
        for i in range(len(map[0])):
            try:
                col = "".join(l for l in [item[i] for item in map])
            except:
                print(map, i)
            if h <= math.floor(len(col) / 2):
                # print(h, ":", col[h:2*h], (col[:h])[::-1])
                if col[h:2*h] != (col[:h])[::-1]:
                    if inc >= 1 or (find_smudge(col[h:2*h], (col[:h])[::-1]) == -1):
                        h_b = False
                        break
                    else:
                        inc += 1
            else:
                # print(h, ":", (col[h:])[::-1], col[h - len(col[h:]):h])
                if (col[h:])[::-1] != col[h - len(col[h:]):h]:
                    if inc >= 1 or (find_smudge((col[h:])[::-1], col[h - len(col[h:]):h]) == -1):
                        h_b = False
                        break
                    else:
                        inc += 1
        if h_b and inc > 0:
            h_p.append(h)
            break

    # print("vert:")
    for v in range(1, len(row)):
        v_b = True
        inc = 0
        for i in range(len(map)):
            row = map[i]
            if v <= math.floor(len(row) / 2):
                # print(v, ":", row[v:2*v], (row[:v])[::-1])
                if row[v:2*v] != (row[:v])[::-1]:
                    if inc >= 1 or (find_smudge(row[v:2*v], (row[:v])[::-1]) == -1):
                        v_b = False
                        break
                    else:
                        inc += 1
            else:
                # print(v, ":", (row[v:])[::-1], row[v - len(row[v:]):v])
                if (row[v:])[::-1] != row[v - len(row[v:]):v]:
                    if inc >= 1 or (find_smudge((row[v:])[::-1], row[v - len(row[v:]):v]) == -1):
                        v_b = False
                        break
                    else:
                        inc += 1
        if v_b and inc > 0:
            v_p.append(v)
            break
    if len(h_p) > 0:
        sum_h += max(h_p)
    if len(v_p) > 0:
        sum_v += max(v_p)
    if len(h_p) + len(v_p) == 0:
        print(inc, ":", h_p, v_p)
        print(map)
    inc += 1

print(sum_v + 100*sum_h)
