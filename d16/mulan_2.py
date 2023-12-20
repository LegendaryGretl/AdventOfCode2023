import copy
import functools

class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
    #   if not isinstance(args, collections.Hashible):
    #      # uncacheable. a list, for instance.
    #      # better to not cache than blow up.
    #      return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)

sp_vert = {"self":"|","N":("N"), "E":("N", "S"), "S":("S"), "W":("N", "S")}
sp_horz = {"self":"-","N":("E", "W"), "E":("E"), "S":("E", "W"), "W":("W")}
m_fw = {"self":"/","N":("E"), "E":("N"), "S":("W"), "W":("S")}
m_bw = {"self":"\\","N":("W"), "E":("S"), "S":("E"), "W":("N")}

mirrors = [sp_vert, sp_horz, m_fw, m_bw]

passed_by = []

def move_beam(place, dir, map):
    coord = [place[0], place[1]]
    if dir == "N":
        if coord[0] > 0:
            coord[0] -= 1
    elif dir == "S":
        if coord[0] < len(map) -1:
            coord[0] += 1
    elif dir == "E":
        if coord[1] < len(map[0]) -1:
            coord[1] += 1
    elif dir == "W":
        if coord[1] > 0:
            coord[1] -= 1
    return tuple(coord)

def beam_path_step(start, dir, map, energy):
    next = move_beam(start, dir, map)
    directions = []
    if next != start:
        energy[next[0]][next[1]] = "#"
        if map[next[0]][next[1]] != ".":
            for m in mirrors:
                if map[next[0]][next[1]] == m["self"]:
                    # if map[next[0]][next[1]] == "\\":
                    #     print(dir, m[dir])
                    directions = [item for item in m[dir]]
                    break
        else:
            directions.append(dir)
    return next, directions

def calc_energy(energy_map):
    sum = 0
    for row in range(len(energy_map)):
        for col in range(len(energy_map[row])):
            if energy_map[row][col] == "#":
                sum += 1
    return sum

@memoized
def energy_from_path_start(s_row, s_col, dir, tile_loop=False, prev_encountered = False, first=False):
    global passed_by
    global mir_map
    global energy_map 
    start = (s_row, s_col)
    energy_val = 0
    if first:
        directions = find_relection_direction(start, mir_map, dir)
        next = (s_row, s_col)
    else:
        # check to see if you're repeating the same direction and location as a previous calculation
        if tile_loop:
            return 0
        else:
            passed_by.append((start, dir))
        if not prev_encountered:
            energy_val = 1
        else:
            energy_val = 0 
        if len(dir) == 0:
        # check if there are any directions left
            return energy_val
        # move beam to next step, find possible paths in the next tile
        next = move_beam(start, dir, mir_map)
        directions = []
        if next != start:
            # energy_map[next[0]][next[1]] = "#"
            if mir_map[next[0]][next[1]] != ".":
                for m in mirrors:
                    if mir_map[next[0]][next[1]] == m["self"]:
                        directions = [item for item in m[dir]]
                        break
            else:
                directions.append(dir)

    # print(start, energy_val, next, [item[0] for item in passed_by])
    if len(directions) == 0:
        return energy_val + energy_from_path_start(next[0], next[1], "", (next, "") in passed_by, next in [item[0] for item in passed_by])
    if len(directions) == 1:
        return energy_val + energy_from_path_start(next[0], next[1], directions[0], (next, directions[0]) in passed_by, next in [item[0] for item in passed_by])
    if len(directions) == 2:
        return energy_val + energy_from_path_start(next[0], next[1], directions[0], (next, directions[0]) in passed_by, next in [item[0] for item in passed_by]) + \
            energy_from_path_start(next[0], next[1], directions[1], (next, directions[1]) in passed_by, next in [item[0] for item in passed_by])
    
def find_relection_direction(start, mir_map, dir):
    for m in mirrors:
        if mir_map[start[0]][start[1]] == m["self"]:
            beam_dirs = [item for item in m[dir]]
            return beam_dirs
    return dir
    
mir_map_txt = open("easy_input.txt")
mir_map = mir_map_txt.read().strip().split("\n")
energy_map = []
for i in range(len(mir_map)):
    mir_map[i] = [l for l in mir_map[i]]
    energy_map.append(["." for l in mir_map[i]])

beam_heads = [(0, 0)]
beam_dirs = ["E"]
for m in mirrors:
    if mir_map[0][0] == m["self"]:
        beam_dirs = [item for item in m[beam_dirs[0]]]
energy_map[0][0] = "#"
passed_by = []
while len(beam_heads) > 0:
    to_delete = []
    for i in range(len(beam_heads)):
        next_tile, next_dirs = beam_path_step(beam_heads[i], beam_dirs[i], mir_map, energy_map)
        if (beam_heads[i], beam_dirs[i]) in passed_by:
            to_delete.append(i)
            # print(passed_by.index((beam_heads[i], beam_dirs[i])))
        elif len(next_dirs) > 0:
            # elif next_tile != beam_heads[i]:
            passed_by.append((beam_heads[i], beam_dirs[i]))
            beam_heads[i] = next_tile
            beam_dirs[i] = next_dirs[0]
            if len(next_dirs) > 1:
                beam_heads.append(next_tile)
                beam_dirs.append(next_dirs[1])
        else:
            to_delete.append(i)
    for idx in reversed(to_delete):
        del beam_heads[idx]
        del beam_dirs[idx]

print(calc_energy(energy_map))
# print(energy_map)
# i = 0
# for item in energy_map:
#     print("".join(item))          
#     print("".join(mir_map[i]))
#     i+=1     

energy_map = []
for i in range(len(mir_map)):
    mir_map[i] = [l for l in mir_map[i]]
    energy_map.append(["." for l in mir_map[i]])

passed_by = []
# print(energy_from_path_start(0, 0, "E"))
beam_heads = []
beam_dirs = []
beam_heads += [(i, 0) for i in range(len(mir_map))]
beam_dirs += ["E" for i in range(len(mir_map))]

beam_heads += [(len(mir_map[0]) - 1, i) for i in range(len(mir_map[0]))]
beam_dirs += ["N" for i in range(len(mir_map))]

beam_heads += [(i, len(mir_map) - 1) for i in range(len(mir_map))]
beam_dirs += ["W" for i in range(len(mir_map))]

beam_heads += [(0, i) for i in range(len(mir_map[0]))]
beam_dirs += ["S" for i in range(len(mir_map))]

# print(energy_from_path_start(0, 3, "S", False, False, True))
# for item in energy_map:
#     print("".join(item))

max_eng = -1
max_start = (-1, -1)
for i in range(len(beam_heads)):
    passed_by = []
    eng = energy_from_path_start(beam_heads[i][0], beam_heads[i][1], beam_dirs[i], False, False, True)
    if eng > max_eng:
        max_eng = eng
        max_start = (beam_heads[i][0], beam_heads[i][1])

print(max_eng, max_start)