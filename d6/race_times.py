races_txt = open("input.txt")

race_data = races_txt.read().split("\n")
time = race_data[0].split(":")[1]
dist = race_data[1].split(":")[1]

time_list = time.strip().split()
time_list = [int(s.strip()) for s in time_list]
dist_list = dist.strip().split()
dist_list = [int(s.strip()) for s in dist_list]

total = 1
for i in range(len(time_list)):
    t = time_list[i]
    d = dist_list[i]
    p = 0
    num_wins = 0
    while p <= t:
        if p*(t - p) > d:
            num_wins += 1
        p += 1
    total *= num_wins

# print(total)

total_time = 51926890
total_dist = 222203111261225

p = 0
p_lower = 0
while p <= total_time:
    if p*(total_time - p) > total_dist:
        p_lower = p
        break
    p += 1

p = total_time
p_upper = 0
while p > 0:
    if p*(total_time - p) > total_dist:
        p_upper = p
        break
    p -= 1

print(p_upper - p_lower + 1)