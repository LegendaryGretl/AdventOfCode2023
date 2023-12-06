scratch_text = open("input.txt")

cards = {}
scratch_lines = scratch_text.read().split("\n")
for line in scratch_lines:
    try:
        card_num = line.split(":")[0]
        numbers = line.split(":")[1]
        card_num = card_num.replace(" ", "")
        card_num = card_num[4:]
        win = numbers.split("|")[0].strip()
        win = win.replace("  ", " ")
        reveal = numbers.split("|")[1].strip()
        reveal = reveal.replace("  ", " ")
        win = win.split(" ")
        for i in range(len(win)):
            win[i] = win[i].strip()
        reveal = reveal.split(" ")
        for i in range(len(reveal)):
            reveal[i] = reveal[i].strip()
        cards[card_num] = [win, reveal]
    except:
        print("error. input:", line)
        continue

sum = 0
num_wins_arr = []
for c in cards.keys():
    wins = cards[c][0]
    result = cards[c][1]
    num_wins = 0
    for num in wins:
        if num in result:
            num_wins += 1
    num_wins_arr.append(num_wins)
    if num_wins > 0:
        sum += pow(2, num_wins - 1)
    #print(num_wins, wins, result)
#print(sum)

num_wins_arr[-2] = 2

# initialize array
num_cards = [1 for item in cards.keys()]
for i in range(len(num_cards)):
    if num_wins_arr[i] > 0:
        if num_wins_arr[i] >= (len(num_cards) - i - 1):
            num_wins_arr[i] = len(num_cards) - i - 1
        for j in range(i+1, i + num_wins_arr[i] + 1):
            num_cards[j] += num_cards[i]

sum = 0
for item in num_cards:
    sum += item
print((sum))