def compare_hands(first, second):
    # returns true if first is stronger than second, false otherwise
    f_repeats = [first.count(i) for i in first if i > 0]
    try:
        f_kind = max(f_repeats) + first.count(-1)
    except:
        f_kind = first.count(-1)
    s_repeats = [second.count(i) for i in second if i > 0]
    try:
        s_kind = max(s_repeats) + second.count(-1)
    except:
        s_kind = second.count(-1)
    if f_kind > s_kind:
        return True
    if f_kind < s_kind:
        return False
    if f_kind == 3:
        f_full = False
        s_full = False
        if min(f_repeats) == 2:
            f_full = True
        if min(s_repeats) == 2:
            s_full = True

        if (f_full and s_full) or (not f_full and not s_full):
            pass
        elif f_full:
            return True
        elif s_full: 
            return False
    elif f_kind == 2:
        f_tp = False
        s_tp = False
        if f_repeats.count(2) == 4:
            f_tp = True
        if s_repeats.count(2) == 4:
            s_tp = True

        if (f_tp and s_tp) or (not f_tp and not s_tp):
            pass
        elif f_tp:
            return True
        elif s_tp: 
            return False
    
    for i in range(len(first)):
        if first[i] > second[i]:
            return True
        if first[i] < second[i]:
            return False
    return True # but they're actually equal

def insertion_sort_but_for_hands(list):
    # https://www.geeksforgeeks.org/insertion-sort/
    for i in range(len(list)):
        key = list[i]

        j= i -1
        while j >= 0 and compare_hands(list[j][0], key[0]):
            list[j + 1] = list[j]
            j -= 1
        list[j + 1] = key
    return list


games_txt = open("input.txt")

games = games_txt.read().split("\n")
for i in range(len(games)):
    games[i] = games[i].strip().split()
    hand_list = []
    for card in games[i][0]:
        if card == "A":
            hand_list.append(14)
        elif card == "K":
            hand_list.append(13)
        elif card == "Q":
            hand_list.append(12)
        elif card == "J":
            hand_list.append(-1)
        elif card == "T":
            hand_list.append(10)
        else:
            hand_list.append(int(card))
    games[i][0] = hand_list
    games[i][1] = int(games[i][1])

#print(games)
sorted_games = insertion_sort_but_for_hands(games)
# print(sorted_games)
sum = 0
for i in range(len(sorted_games)):
    print(i, sorted_games[i][0], sorted_games[i][1], sorted_games[i][1] * (i + 1))
    sum += sorted_games[i][1] * (i + 1)

print(sum)