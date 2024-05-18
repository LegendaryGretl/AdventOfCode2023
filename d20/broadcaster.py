import math

class Flip_Flop():
    def __init__(self, name):
        self.name = name
        self.state = "OFF"
        self.out = "L"

    def __repr__(self):
        return "%"+self.name+": "+self.out
    
    def output(self, input):
        if input == "H":
            return "Z"
        elif self.state == "ON":
            self.state = "OFF"
            self.out  = "L"
        else:
            self.state = "ON"
            self.out = "H"
        return self.out

class Conjunction():
    def __init__(self, name):
        self.name = name
        #self.ins = inputs
        self.out = "L"

    def __repr__(self):
        return "&"+self.name+": "+self.out

    def output(self, inputs):
        for item in inputs:
            if item == "L":
                self.out = "H"
                return self.out
        self.out = "L"
        return self.out
    
class Broadcaster():
    def __init__(self, name):
        self.name = name
        self.out = "L"
        
    def __repr__(self):
        return self.name+": "+self.out

    def output(self, input):
        self.out = input
        return self.out
    
class Module():
    def __init__(self, type, name):
        self.name = name
        self.type = type
        if type == "%":
            self.fn = Flip_Flop(name)
        elif type == "&":
            self.fn = Conjunction(name)
        elif type == "broadcaster":
            self.fn = Broadcaster(name)
        self.outputs = []
        self.inputs = []
        
    def __repr__(self):
        return self.fn.__repr__()
        rep = self.type + self.name + "("
        for item in self.inputs:
            rep += str(item.name)
        rep += ") -> " + self.fn.output + " ("
        for item in self.outputs:
            rep += str(item.name)
        rep += ")"
        return rep
        return self.type+self.name+"("+self.inputs+")"+"->"+self.fn.output+"("+self.outputs+")"

    def addOutput(self, mod):
        self.outputs.append(mod)
    
    def addInput(self, mod):
        self.inputs.append(mod)

    def output(self, input="L"):
        if self.type == "%":
            return self.fn.output(input)
        elif self.type == "&":
            return self.fn.output([a.fn.out for a in self.inputs])
        elif self.type == "broadcaster":
            return self.fn.output(input)

class Network():
    def __init__(self, input_lines):
        self.modules = []
        self.H = 0
        self.L = 0
        self.bPress = 0
        self.finalConjInputs = {}
        self.rxL = False
        # populate list of modules with type and name
        for line in input_lines:
            mod = line.split(" -> ")[0].strip()
            if mod == "broadcaster":
                self.modules.append(Module(mod, mod))
            else:
                self.modules.append(Module(mod[0], mod[1:]))

        # find all output modules
        for line in input_lines:
            outs = line.split(" -> ")[1].strip().split(", ")
            for o in outs:
                if o not in [a.name for a in self.modules]:
                    self.modules.append(Module("!", o))

        for line in input_lines:
            mod_name = line.split(" -> ")[0].strip()
            outs = line.split(" -> ")[1].strip()
            out_names = outs.split(", ")
            if mod_name == "broadcaster":
                m = [a for a in self.modules if a.name == mod_name][0]
                o = [a for a in self.modules if a.name in out_names]
            else:
                m = [a for a in self.modules if a.name == mod_name[1:]][0]
                o = [a for a in self.modules if a.name in out_names]

            for out in o:
                m.addOutput(out)
                out.addInput(m)
        self.stack = [("broadcaster", "L")]
        
    def pushButton(self):
        self.stack = [("broadcaster", "L")]
        self.L +=1 
        self.bPress += 1

    def processStep(self, input):
        mod = [a for a in self.modules if a.name == input[0]][0]
        out = mod.output(input[1])
        if out == "Z":
            return []
        # elif out == "H":
        #     self.H += 1
        # elif out == "L":
        #     self.L += 1
        # else:
        #     print("ERROR: unrecognized output")
        add_to_stack = []
        for output in mod.outputs:
            if out == "H":
                if output.name == "zp":
                    if mod.name not in self.finalConjInputs.keys():
                        self.finalConjInputs[mod.name] = self.bPress
                self.H += 1
            elif out == "L":
                if output.name == "rx":
                    self.rxL = True
                self.L += 1
            else:
                print("ERROR: unrecognized output")
            if output.type != "!":
                add_to_stack.append((output.name, out))
            else:
                if out == "L":
                    self.rxL = True
        return add_to_stack
    
    def processStack(self):
        while len(self.stack) > 0:
            step = self.stack.pop(0)
            # if step[1] == "H":
            #     self.H += 1
            # elif step[1] == "L":
            #     self.L += 1
            # else:
            #     print("ERROR: unrecognized output")
            next_steps = self.processStep(step)
            self.stack += next_steps


input_str = open("input.txt").read().split("\n")
networ = Network(input_str)
# for i in range(1000):
#     networ.pushButton()
#     networ.processStack()
# print(networ.L, networ.H, networ.H * networ.L)
# while networ.rxL == False:
#     networ.pushButton()
#     networ.processStack()
while len(networ.finalConjInputs.keys()) < 4:
    networ.pushButton()
    networ.processStack()
print(networ.bPress)
presses = 1
for item in networ.finalConjInputs.values():
    presses = math.lcm(presses, item)
print(presses)
