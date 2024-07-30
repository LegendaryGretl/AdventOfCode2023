class MachinePart():
    def __init__(self, x, m, a, s):
        self.X =x
        self.M = m
        self.A = a
        self.S = s

    def __init__(self, input_str):
        input_str_clean = input_str.replace("{", "").replace("}", "")
        input_list = input_str_clean.split(",")
        for item in input_list:
            if item.split("=")[0] == 'x':
                self.X = int(item.split("=")[1])
            elif item.split("=")[0] == 'm':
                self.M = int(item.split("=")[1])
            elif item.split("=")[0] == 'a':
                self.A = int(item.split("=")[1])
            elif item.split("=")[0] == 's':
                self.S = int(item.split("=")[1])

    def getRating(self, category):
        if category == "x":
            return self.X
        if category == "m":
            return self.M
        if category == "a":
            return self.A
        if category == "s":
            return self.S
        return -1
    
    def sumTotal(self):
        return self.X + self.M + self.A + self.S


class MachinePartRange():
    def __init__(self, x=None, m=None, a=None, s=None):
        if (x == None):
            self.X = (1, 4000)
        else:
            self.X = (x[0], x[1])

        if (m == None):
            self.M = (1, 4000)
        else:
            self.M = (m[0], m[1])

        if (a == None):
            self.A = (1, 4000)
        else:
            self.A = (a[0], a[1])

        if (s == None):
            self.S = (1, 4000)
        else:
            self.S = (s[0], s[1])

    def __repr__(self):
        return f'X: {self.X}, M: {self.M}, A: {self.A}, S: {self.S}'

    def Copy(self):
        return MachinePartRange(self.X, self.M, self.A, self.S)

    def splitRangeGT(self, category, value):
        # [start, value], [value + 1, stop]
        lower = self.Copy()
        upper = self.Copy()
        if category == "x":
            lower.X = (self.X[0], value)
            upper.X = (value + 1, self.X[1])
        if category == "m":
            lower.M = (self.M[0], value)
            upper.M = (value + 1, self.M[1])
        if category == "a":
            lower.A = (self.A[0], value)
            upper.A = (value + 1, self.A[1])
        if category == "s":
            lower.S = (self.S[0], value)
            upper.S = (value + 1, self.S[1])
        return lower, upper
    
    def splitRangeLT(self, category, value):
        # [start, value - 1], [value, stop]
        lower = self.Copy()
        upper = self.Copy()
        if category == "x":
            lower.X = (self.X[0], value - 1)
            upper.X = (value, self.X[1])
        if category == "m":
            lower.M = (self.M[0], value - 1)
            upper.M = (value, self.M[1])
        if category == "a":
            lower.A = (self.A[0], value - 1)
            upper.A = (value, self.A[1])
        if category == "s":
            lower.S = (self.S[0], value - 1)
            upper.S = (value, self.S[1])
        return lower, upper

    def getNumberOfParts(self):
        x = self.X[1] - self.X[0] + 1
        m = self.M[1] - self.M[0] + 1
        a = self.A[1] - self.A[0] + 1 
        s = self.S[1] - self.S[0] + 1
        return x*m*a*s



class SortingRule():
    def __init__(self, rule_str):
        self.category = rule_str[0]
        self.comparator = rule_str[1]
        self.threshold = int(rule_str.split(":")[0][2:])
        self.outputWorkflow = rule_str.split(":")[1]
    
    def checkMachinePart(self, part):
        if self.comparator == ">":
            if part.getRating(self.category) > self.threshold:
                return self.outputWorkflow
        elif self.comparator == "<":
            if part.getRating(self.category) < self.threshold:
                return self.outputWorkflow
        return ""
    
    def checkMachinePartRange(self, part_range):
        # binned part ranges will go to the next part in the workflow, while next part ranges
        # still need to be assigned their next workflow
        if self.comparator == ">":
            next, binned = part_range.splitRangeGT(self.category, self.threshold)
        elif self.comparator == "<":
            binned, next = part_range.splitRangeLT(self.category, self.threshold)
        return (next, ""), (binned, self.outputWorkflow)


class SortingWorkflow():
    def __init__(self, workflow_str):
        self.name = workflow_str.split("{")[0]
        self.rules = []
        rules = workflow_str.split("{")[1].replace("}", "").split(",")
        for rule in rules[:-1]:
            self.rules.append(SortingRule(rule))
        self.default = rules[-1]

    def sortMachinePart(self, part):
        for rule in self.rules:
            dest = rule.checkMachinePart(part)
            if len(dest) > 0:
                return dest
        return self.default

    def sortMachinePartRange(self, part_range):
        current_range = part_range
        ranges_and_destinations = []
        for rule in self.rules:
            next, binned = rule.checkMachinePartRange(current_range)
            ranges_and_destinations.append(binned)
            current_range = next[0]
        ranges_and_destinations.append((current_range, self.default)) # apply default rule
        return ranges_and_destinations


class SortingSystem():
    def __init__(self, workflows):
        self.workflows = []
        for line in workflows.split("\n"):
            self.workflows.append(SortingWorkflow(line))

    def acceptMachinePart(self, part):
        wkflow = [x for x in self.workflows if x.name == "in"][0]
        for i in range(len(self.workflows)):
            next_wkflow = wkflow.sortMachinePart(part)
            if next_wkflow == "A":
                return True
            if next_wkflow == "R":
                return False
            wkflow = [x for x in self.workflows if x.name == next_wkflow][0]
        return False
    
    def binAllRanges(self):
        starting_range = MachinePartRange()
        starting_wkflow = [x for x in self.workflows if x.name == "in"][0]
        ranges_and_destinations = []
        accepted_ranges = []
        ranges_and_destinations.append((starting_range, starting_wkflow))
        while len(ranges_and_destinations) > 0:
            part_range, wkflow = ranges_and_destinations.pop(0)
            next_groups = wkflow.sortMachinePartRange(part_range)
            for item in next_groups:
                pr = item[0] # part range
                wk_name = item[1]
                if wk_name == "A":
                    accepted_ranges.append(pr.Copy())
                elif wk_name != "R":
                    wk = [x for x in self.workflows if x.name == wk_name][0]
                    ranges_and_destinations.append((pr.Copy(), wk))
        return accepted_ranges


input_str = open("input.txt").read().split("\n\n")
sorting_system = SortingSystem(input_str[0])
machine_parts = []
for part in input_str[1].split("\n"):
    machine_parts.append(MachinePart(part))

total = 0
for m_part in machine_parts:
    if sorting_system.acceptMachinePart(m_part):
        total += m_part.sumTotal()
print("Part 1:", total)

output = sorting_system.binAllRanges()
total = 0
for item in output:
    total += item.getNumberOfParts()
    print(item)

print("Part 2:", total)