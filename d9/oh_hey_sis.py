def gen_difference_arr(input):
    out = []
    for i in range(len(input) - 1):
        out.append(input[i + 1] - input[i])
    return out

history_txt = open("input.txt")

histories = history_txt.read().strip().split("\n")

sum = 0
for h in histories:
    cur = h.split()
    cur = [int(k) for k in cur]
    ext = cur[-1]
    next = gen_difference_arr(cur)
    while not all(v == 0 for v in next):
        ext += next[-1]
        next = gen_difference_arr(next)
    sum += ext

print(sum)

sum = 0
for h in histories:
    cur = h.split()
    cur = [int(k) for k in cur]
    ext = cur[0]
    next = gen_difference_arr(cur)
    counter = 1
    while not all(v == 0 for v in next):
        if counter % 2 == 1:
            ext -= next[0]
        else:
            ext += next[0]
        counter += 1
        next = gen_difference_arr(next)
    sum += ext

print(sum)