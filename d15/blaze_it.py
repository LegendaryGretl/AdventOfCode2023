def hash_it_out(string, hash=0):
    for l in string:
        hash += ord(l)
        hash *= 17
        hash  = hash % 256
    return hash


init_seq_txt = open("input.txt")
init_seq = init_seq_txt.read().strip().split(",")

sum = 0
for item in init_seq:
    sum += hash_it_out(item)
print(sum)

boxes = {}
for cmd in init_seq:
    if cmd.find("-") != -1:
        label = cmd.split("-")
        box = hash_it_out(label[0])
        if box in boxes.keys():
            ls = [item[0] for item in boxes[box]]
            if  len(ls) > 0 and label[0] in ls:
                idx = ls.index(label[0])
                del boxes[box][idx]
    if cmd.find("=") != -1:
        label = cmd.split("=")
        box = hash_it_out(label[0])
        if box in boxes.keys():
            ls = [item[0] for item in boxes[box]]
            if len(ls) > 0 and label[0] in ls:
                idx = ls.index(label[0])
                boxes[box][idx] = label
            else:
                boxes[box].append(label)
        else:
            boxes[box] = [label]

sum = 0
for b in boxes.keys():
    temp = 0
    if len(boxes[b]) > 0:
        for i in range(len(boxes[b])):
            temp = 1
            temp*= b + 1
            temp *= i + 1
            print(boxes[b])
            temp *= int(boxes[b][i][1])
            sum += temp
        
print(sum)