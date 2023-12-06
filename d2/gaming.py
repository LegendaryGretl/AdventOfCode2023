input = open("input.txt")

game_dict = {}

# arrange information into a dictionary where game number is the key
for line in input.read().split("\n"):
    #line = line.replace(" ", "") # get rid of whitespace
    game_str = line.split(":")[0][5:]
    try:
        match_list = line.split(":")[1]
        match_list = match_list.split(";")
        for i in range(len(match_list)):
            match_list[i] = match_list[i].strip().split(",")
            for j in range(len(match_list[i])):
                match_list[i][j] = match_list[i][j].strip().split(" ")
    except:
        # error handling
        break
    game_dict[game_str] = match_list

#print(game_dict)

# determine which games are possible give certain numbers of cubes
max_red = 12
max_green = 13
max_blue = 14

sum_possible = 0
for game_num in game_dict.keys():
    counter = 0
    for draw in game_dict[game_num]:
        for item in draw:
            if item[1] == "red":
                if int(item[0]) > max_red:
                    counter += 1
            elif item[1] == "green":
                if int(item[0]) > max_green:
                    counter += 1
            elif item[1] == "blue":
                if int(item[0]) > max_blue:
                    counter += 1
    if counter == 0:
        sum_possible += int(game_num)

print(sum_possible)

# find sum of powerset of minimum number of cubes for each game
sum_powers = 0
for game_num in game_dict.keys():
    max_red = 0
    max_green = 0
    max_blue = 0
    for draw in game_dict[game_num]:
        for item in draw:
            if item[1] == "red":
                if int(item[0]) > max_red:
                    max_red = int(item[0])
            elif item[1] == "green":
                if int(item[0]) > max_green:
                    max_green = int(item[0])
            elif item[1] == "blue":
                if int(item[0]) > max_blue:
                    max_blue = int(item[0])
    sum_powers += max_red * max_blue * max_green

print(sum_powers)