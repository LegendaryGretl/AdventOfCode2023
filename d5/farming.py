def input_in_map(map, input):
    dest = int(map[0])
    source = int(map[1])
    map_len = int(map[2])
    # input isn't in this map
    if (input < source) or (input > source + map_len - 1):
        return -1
    diff = input - source
    return dest + diff

def range_in_map(map, range):
    dest = int(map[0])
    source = int(map[1])
    map_len = int(map[2])
    r_start = int(range[0])
    r_end = int(range[1])
    missing_ranges = []
    # ranges don't overlap
    if ((r_start < source) and (r_end < source)) or ((r_start > (source + map_len - 1)) and (r_end > (source + map_len - 1))):
        return (), [range]
    if r_start < source:
        start = dest
        missing_ranges.append((r_start, source - 1))
    else:
        start = dest + r_start - source
    if (r_end > (source + map_len - 1)):
        end = (dest + map_len - 1)
        missing_ranges.append((source + map_len, r_end))
    else:
        end = dest + r_end - source
        
    return (start, end), missing_ranges

map_file = open("input.txt")

map_categories = map_file.read().split("\n\n")

seed_raw = map_categories[0].split(":")
seeds = seed_raw[1].strip()
seeds = seeds.split(" ")
seeds = [int(s) for s in seeds]
# part 1 solution 
input = seeds
new_input = [-1 for item in input]

for map_raw in map_categories[1:]:
    try:
        map_list = map_raw.split(":")[1]
        map_list = map_list.strip().split("\n")
        for map in map_list:
            map_condioned = map.split(" ")
            for i in range(len(input)):
                if new_input[i] < 0:
                    new_input[i] = input_in_map(map_condioned, int(input[i]))
        for i in range(len(input)):
            if new_input[i] < 0:
                new_input[i] = input[i]
    except:
        print("error at", map_raw)
        break
    input = new_input
    new_input = [-1 for item in input]

print("p1:", min(input))


#part 2 solution input
input = []
for i in range(int(len(seeds)/2)):
    input.append((seeds[2*i], seeds[2*i]+ seeds[2*i + 1] - 1))
new_input = [() for item in input]

for map_raw in map_categories[1:]:
    
    map_list = map_raw.split(":")[1]
    map_list = map_list.strip().split("\n")
    for map in map_list:
        map_condioned = map.split(" ")
        i = 0
        while i < len(input):
            if len(new_input[i]) < 1:
                new_input[i], missing_range = range_in_map(map_condioned, input[i])
                if len(new_input[i]) > 1:
                    for item in new_input[i]:
                        if item < 0:
                            print(new_input[i], input[i], map_condioned)
                            range_in_map(map_condioned, input[i])
                if (len(new_input[i]) > 1) and len(missing_range) > 0:
                    for item in missing_range:
                        input.append(item)
                        new_input.append(())
            i += 1
    for i in range(len(input)):
        if len(new_input[i]) < 1:
            new_input[i] = input[i]
    input = new_input
    new_input = [() for item in input]

mins = [range[0] for range in input]
print(min(mins)) 