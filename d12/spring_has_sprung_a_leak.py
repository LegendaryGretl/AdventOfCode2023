def correct_arrangement(condition, grouping):
    if condition.count("#") != sum(grouping):
        return False
    marker = 0
    for item in grouping:
        if marker > len(condition) - 1:
            return False
        marker = condition[marker:].find("#"*int(item))
        if marker < -1:
            return False
        marker += int(item)
    if condition[marker:].find("#") != -1:
        return False
    return True

def recurse_arrange(sequence, pattern, sum=0):
    if len(sequence) == 0:
        if len(pattern) == 0:
            return 1
        else:
            return 0
    if len(pattern) == 0:
        if sequence.find("#") != -1:
            return 0
        else:
            return 1
    if sequence[0] == ".":
        return sum + recurse_arrange(sequence[1:], pattern, sum)
    if sequence[0] == "#":
        if len(sequence) < pattern[0]:
            return sum
        if sequence[:pattern[0]].find(".") == -1:
            if (len(sequence) > pattern[0]) and (sequence[pattern[0]] != "#"):
                return recurse_arrange(sequence[pattern[0] + 1:], pattern[1:], sum)
            elif len(sequence) == pattern[0]:
                return recurse_arrange(sequence[pattern[0]:], pattern[1:], sum)
            else:
                return sum
        else:
            return sum + 0
    if sequence[0] == "?":
        return sum + recurse_arrange("."+sequence[1:], pattern, 0) + recurse_arrange("#"+sequence[1:], pattern, 0)
    

springs_txt = open("input.txt")
springs_list = springs_txt.read().strip().split("\n")
springs_list = [item.split() for item in springs_list]
for i in range(len(springs_list)):
    springs_list[i][1] = [int(item) for item in springs_list[i][1].split(",")]

print(springs_list)

# print(recurse_arrange("#.#.###", [1,1,3], 0))

# print(recurse_arrange(".??..??...?##.", [1,1,3], 0))

# print(recurse_arrange("?#?#?#?#?#?#?#?", [1,3,1,6], 0))

# print(recurse_arrange("????.#...#...", [4,1,1], 0))

# print(recurse_arrange("????.######..#####.", [1,6,5], 0))

# print(recurse_arrange("?###????????", [3, 2, 1], 0))

tot_sum = 0
for item in springs_list:
    #print(item[0], item[1], recurse_arrange(item[0], item[1], 0))
    tot_sum += recurse_arrange(item[0], item[1])
print(tot_sum)