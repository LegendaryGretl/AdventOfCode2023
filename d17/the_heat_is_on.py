from queue import PriorityQueue
from copy import deepcopy as dcpy
# from dataclasses import dataclass, field
# from typing import Any

# @dataclass(order=True)
# class PrioritizedItem:
#     # shameless take from https://docs.python.org/3/library/queue.html
#     priority: int
#     item: Any=field(compare=False)

heat_map_txt = open("input.txt")
heat_map = heat_map_txt.read().strip().split("\n")
heat_map = [[int(l) for l in item] for item in heat_map]

compass_directions = ["N", "E", "S", "W"]

def move_cart(place, dir, map=heat_map):
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

def is_move_possible(place, dir, map=heat_map):
    coord = [place[0], place[1]]
    if dir == "N":
        if coord[0] <= 0:
            return False
    elif dir == "S":
        if coord[0] >= len(map) -1:
            return False
    elif dir == "E":
        if coord[1] >= len(map[0]) -1:
            return False
    elif dir == "W":
        if coord[1] <= 0:
            return False
    return True

class Block():
    # def __init__(self, coord, dir, straight_line_steps, map=heat_map):
    #     self.coord = coord
    #     self.entry_dir = dir
    #     self.map = map
    #     self.line_steps = straight_line_steps

    def __init__(self, info_tuple, map=heat_map):
        self.coord = info_tuple[0]
        self.entry_dir = info_tuple[1]
        self.map = map
        self.line_steps = info_tuple[2]

    def __lt__(self, other):
        return self.cost() < other.cost()
    
    def __le__(self, other):
        return self.cost() <= other.cost()
    
    def __gt__(self, other):
        return self.cost() > other.cost()
    
    def __ge__(self, other):
        return self.cost() >= other.cost()
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.coord == other.coord and self.entry_dir == other.entry_dir and self.line_steps == other.line_steps
    
    def __str__(self):
        return f"Coord:{self.coord} entry dir:{self.entry_dir} line steps: {self.line_steps}>"

    def get_coord(self):
        return self.coord

    def neighbors(self):
        n= []
        if self.line_steps > 2:
            return n
        
        if self.line_steps < 2 and is_move_possible(self.coord, self.entry_dir):
            n.append(Block((move_cart(self.coord, self.entry_dir, self.map), self.entry_dir, self.line_steps + 1)))
        
        idx = compass_directions.index(self.entry_dir)
        if is_move_possible(self.coord, compass_directions[idx - 1]):
            n.append(Block((move_cart(self.coord, compass_directions[idx - 1], self.map), compass_directions[idx - 1], 0)))
        
        if (idx < len(compass_directions) - 1) and is_move_possible(self.coord, compass_directions[idx + 1]) :
            n.append(Block((move_cart(self.coord, compass_directions[idx + 1], self.map), compass_directions[idx + 1], 0)))
        else:
            if is_move_possible(self.coord, compass_directions[0]):
                n.append(Block((move_cart(self.coord, compass_directions[0], self.map), compass_directions[0], 0)))
        
        return n
    
    def ultra_neighbors(self):
        n= []
        if self.line_steps > 9:
            return n
        
        if self.line_steps < 9 and is_move_possible(self.coord, self.entry_dir):
            n.append(Block((move_cart(self.coord, self.entry_dir, self.map), self.entry_dir, self.line_steps + 1)))
        
        idx = compass_directions.index(self.entry_dir)
        if self.line_steps >= 3 or self.line_steps < 0:
            if is_move_possible(self.coord, compass_directions[idx - 1]):
                n.append(Block((move_cart(self.coord, compass_directions[idx - 1], self.map), compass_directions[idx - 1], 0)))
            
            if (idx < len(compass_directions) - 1) and is_move_possible(self.coord, compass_directions[idx + 1]) :
                n.append(Block((move_cart(self.coord, compass_directions[idx + 1], self.map), compass_directions[idx + 1], 0)))
            else:
                if is_move_possible(self.coord, compass_directions[0]):
                    n.append(Block((move_cart(self.coord, compass_directions[0], self.map), compass_directions[0], 0)))
        
        return n
    
    def is_goal(self):
        if (self.coord[0] == len(self.map) - 1) and (self.coord[1] == len(self.map[0]) - 1):
            return True
        return False
    
    def is_ultra_goal(self):
        if (self.coord[0] == len(self.map) - 1) and (self.coord[1] == len(self.map[0]) - 1) and (self.line_steps >= 3):
            return True
        return False
    
    def cost(self):
        return self.map[self.coord[0]][self.coord[1]]
    
    def heuristic(self):
        ''' Manhattan distance '''
        return (len(self.map) - 1 - self.coord[0]) + (len(self.map[0]) - 1 - self.coord[1])

    def dict_key(self):
        return (self.coord, self.entry_dir, self.line_steps)


test = Block(((0, 1), "E", 4))
test.ultra_neighbors()
for n in test.ultra_neighbors():
    print(n)

frontier = PriorityQueue()
# start = Block(((0, 0), "E", -1))
start = ((0, 0), "E", -1)
frontier.put((0, start))
came_from = {}
cost_so_far = {}
came_from[start] = None
cost_so_far[start] = 0

while not frontier.empty():
    curr = Block(frontier.get()[1])
    if curr.is_ultra_goal():
        break

    for next in curr.ultra_neighbors():
        new_cost = cost_so_far[curr.dict_key()] + next.cost()
        if next.dict_key() not in cost_so_far.keys() or new_cost < cost_so_far[next.dict_key()]:
            cost_so_far[next.dict_key()] = new_cost
            priority = new_cost + next.heuristic()
            frontier.put((priority, next.dict_key()))
            came_from[next.dict_key()] = curr.dict_key()

# end_tile = (0, 0)
# for key in cost_so_far.keys():
#     if key[0] == (len(heat_map) -1 , len(heat_map[0]) -1):
#         end_tile = key
#         break

# print(cost_so_far[end_tile])
if not curr.is_ultra_goal():
    print("Failure")
print(cost_so_far[curr.dict_key()])



curr = curr.dict_key()
while curr != None and came_from[curr] != None:
    c = curr[0]
    heat_map[c[0]][c[1]] = "+"
    # print(curr)
    curr = came_from[curr]



for item in heat_map:
    print("".join([str(i) for i in item]))
