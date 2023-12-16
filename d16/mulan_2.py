sp_vert = {"self":"|","N":["N"], "E":["N", "S"], "S":["S"], "W":["N", "S"]}
sp_horz = {"self":"-","N":["E", "W"], "E":["E"], "S":["E", "W"], "W":["W"]}
m_fw = {"self":"/","N":["E"], "E":["N"], "S":["W"], "W":["S"]}
m_bw = {"self":"\\","N":["W"], "E":["S"], "S":["E"], "W":["N"]}

mirrors = [sp_vert, sp_horz, m_fw, m_bw]

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
                    directions = m[dir]
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

mir_map_txt = open("input.txt")
mir_map = mir_map_txt.read().strip().split("\n")
energy_map = []
for i in range(len(mir_map)):
    mir_map[i] = [l for l in mir_map[i]]
    energy_map.append(["." for l in mir_map[i]])

beam_heads = [(0, 0)]
beam_dirs = ["E"]
for m in mirrors:
    if mir_map[0][0] == m["self"]:
        beam_dirs = m[beam_dirs[0]]
energy_map[0][0] = "#"
passed_by = []
while len(beam_heads) > 0:
    to_delete = []
    for i in range(len(beam_heads)):
        next_tile, next_dirs = beam_path_step(beam_heads[i], beam_dirs[i], mir_map, energy_map)
        if (beam_heads[i], beam_dirs[i]) in passed_by:
            to_delete.append(i)
            print(passed_by.index((beam_heads[i], beam_dirs[i])))
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
for item in energy_map:
    print("".join(item))               