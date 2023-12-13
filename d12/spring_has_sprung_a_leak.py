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
            return sum + 1
        else:
            return sum + 0
    if len(pattern) == 0:
        if sequence.find("#") != -1:
            return sum + 0
        else:
            return sum + 1
    if sequence[0] == ".":
        return recurse_arrange(sequence[1:], pattern, sum)
    if sequence[0] == "#":
        if len(sequence) < pattern[0]:
            return sum
        if sequence[:pattern[0]].find(".") == -1:
            if (len(sequence) == pattern[0] )or (sequence[pattern[0]] != "#"):
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
    springs_list[i][1] = (int(springs_list[i][1].split(",")[0]), int(springs_list[i][1].split(",")[1]))

print(recurse_arrange("#.#.###", [1,1,3], 0))

print(recurse_arrange(".??..??...?##.", [1,1,3], 0))