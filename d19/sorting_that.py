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