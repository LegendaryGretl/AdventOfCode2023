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

springs_txt = open("input.txt")
springs_list = springs_txt.read().strip().split("\n")
springs_list = [item.split() for item in springs_list]
for i in range(len(springs_list)):
    springs_list[i][1] = (int(springs_list[i][1].split(",")[0]), int(springs_list[i][1].split(",")[1]))
