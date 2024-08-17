class SandBrick():
    def __init__(self, in_str):
        input = in_str.split("~")
        self.S0 = [int(x) for x in input[0].split(",")]
        self.S1 = [int(x) for x in input[1].split(",")]

    def __eq__(self, b):
        if isinstance(b, SandBrick):
            return self.S1 == b.S1 and self.S0 == b.S0
        else:
            return False
        
    def __repr__(self):
        return f'{self.S0}~{self.S1}'
    
    def __key__(self):
        return (self.S0[0], self.S0[1], self.S1[2], self.S1[0], self.S1[1], self.S1[2])

    def __hash__(self):
        return hash(self.__key__())

    def Collision(self, B):
        for i in range(3):
            # check if B in within self's bounds
            #if not (B.S1[i] <= self.S1[i] and B.S0[i] >= self.S0[i]):
            if not (B.S0[i] <= self.S1[i] and self.S0[i] <= B.S1[i]):
                return False
        return True
    
    def Adjacent(self, B, above=True):
        if above and B.S0[2] <= self.S1[2]:
            return False
        for i in range(3):
            # check if B in within self's bounds + 1
            if not (B.S1[i] <= self.S1[i] + 1 and B.S0[i] >= self.S0[i] - 1):
                return False
        return True
        
    def WouldFall(self, B):
        # given block B, would self fall further downwards or be stopped?
        if B.S1[2] != self.S0[2] - 1:
            return True # won't be stopped by B, B isn't directly underneath
        for i in range(2):
            if not (B.S0[i] <= self.S1[i] and B.S1[i] >= self.S0[i]):
                return True # won't be stopped by B, B is far away
        return False # B is directly beneath self, and prevents a fall

    def Fall(self, new_height=None):
        if self.S0[2] > 1 and new_height == None:
            self.S0[2] -= 1
            self.S1[2] -= 1
        elif new_height != None:
            self.S1[2] -= self.S0[2]
            self.S0[2] = new_height
            self.S1[2] += new_height
            


    def UnFall(self):
        self.S0[2] += 1
        self.S1[2] += 1


class SandPile():
    def __init__(self, in_str):
        input = in_str.strip().split("\n")
        self.bricks = []
        for line in input:
            self.bricks.append(SandBrick(line))
        self.bricks.sort(key=lambda x: x.S0[2])
        self.disintegration_dict = {}

    def AllFall2(self):
        fallen = []
        while len(self.bricks) > 0:
            stopped = False
            A = self.bricks.pop(0)
            while A.S0[2] > 1 and not stopped:
                A.Fall()
                for B in fallen:
                    if A.Collision(B):
                        stopped = True
                        A.UnFall()
                        break
            fallen.append(A)
        self.bricks = fallen[:]


    def AllFall(self):
        for i in range(len(self.bricks)):
            A = self.bricks[i]
            stopped = False
            while A.S0[2] > 1 and not stopped:
                # if (i > 0) and A.S0[2] > self.bricks[i-1].S1[2]:
                #     A.Fall(self.bricks[i-1].S1[2])
                # else:
                #     A.Fall()
                A.Fall()
                for B in self.bricks[:i]:
                    if A.Collision(B):
                        stopped = True
                        A.UnFall()
                        break
            self.bricks[i] = A


    def SafeToDisintegrate(self):
        self.AllFall()
        safe = []
        all_supports = []
        for A in self.bricks:
            supports = []
            for B in [x for x in self.bricks if x.S1[2] < A.S0[2]]:
                if not A.WouldFall(B):
                    supports.append(B)
            if len(supports) > 1:
                for item in supports:
                    if item not in safe:
                        safe.append(item)
            for item in supports:
                if item not in all_supports:
                    all_supports.append(item)
        loafing = [x for x in self.bricks if x not in all_supports]
        safe += loafing
        return safe
    
    def SafeToDisintegrate2(self):
        self.AllFall()
        safe = self.bricks[:]
        for i in range(len(self.bricks)):
            A = self.bricks[i]
            supports = []
            for B in self.bricks[:i]:
                if not A.WouldFall(B):
                    supports.append(B)
                    if len(supports) > 1:
                        break
            if len(supports) == 1:
                if supports[0] in safe:
                    safe.remove(supports[0])
        return safe
    
    def GenerateDisintegrationList(self):
        self.AllFall()
        supported_by_dict = {}
        
        # for each block, generate list of blocks that support it
        for i in range(len(self.bricks)):
            A = self.bricks[i]
            supported_by = []
            for B in [c for c in self.bricks[:i] if c.S1[2] == A.S0[2] - 1]:
                if not A.WouldFall(B):
                    supported_by.append(B)
            supported_by_dict[A] = supported_by

        fallen = {}

        # for each block that would directly cause other blocks to fall, create a list of which blocks fall because of it
        for key in supported_by_dict.keys():
            if len(supported_by_dict[key]) == 1:
                support = supported_by_dict[key][0]
                if support not in fallen.keys():
                    fallen[support] = [key]
                else:
                    fallen[support].append(key)

        # for each block that causes another block to fall, find all blocks that fall afterwards because of its removal
        for key in fallen.keys():
            above = [c for c in self.bricks if c.S0[2] > key.S1[2]] # only look at the block above this key
            for block in above: 
                max_height = max(fallen[key], key=lambda x: x.S1[2])
                if block.S0[2] > max_height.S1[2] + 1:
                    pass
                if block in fallen[key]:
                    continue
                if all(elem in fallen[key] for elem in supported_by_dict[block]):
                    fallen[key].append(block)

        return supported_by_dict, fallen

        
    

input_txt = open("input.txt").read().strip()
pile = SandPile(input_txt)
# out = pile.SafeToDisintegrate2()
# print("Part 1:", len(out))
sup, top = pile.GenerateDisintegrationList()
totl = 0
for k in top.keys():
    totl += len(top[k])
print("Part 2:", totl)