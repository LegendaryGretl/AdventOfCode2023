import collections
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

def correct_arrangement(condition, grouping):
    if condition.count("#") != sum(grouping):
        return False
    marker = 0
    for item in grouping:
        if marker > len(condition) - 1:
            return False
        marker = condition[marker:].find("#"*int(item))
        if marker < -1:
            return False
        marker += int(item)
    if condition[marker:].find("#") != -1:
        return False
    return True

@memoized
def recurse_arrange(sequence, patt):
    if len(sequence) == 0:
        if len(patt) == 0:
            return 1
        else:
            return 0
    if len(patt) == 0:
        if sequence.find("#") != -1:
            return 0
        else:
            return 1
    pattern = [int(item) for item in patt.split(",")]
    if sequence[0] == ".":
        return recurse_arrange(sequence[1:], patt)
    if sequence[0] == "#":
        if len(sequence) < pattern[0]:
            return 0
        if sequence[:pattern[0]].find(".") == -1:
            if (len(sequence) > pattern[0]) and (sequence[pattern[0]] != "#"):
                patt = ",".join(str(x) for x in pattern[1:])
                return recurse_arrange(sequence[pattern[0] + 1:], patt)
            elif len(sequence) == pattern[0]:
                patt = ",".join(str(x) for x in pattern[1:])
                return recurse_arrange(sequence[pattern[0]:], patt)
            else:
                return 0
        else:
            return 0
    if sequence[0] == "?":
        return recurse_arrange("."+sequence[1:], patt) + recurse_arrange("#"+sequence[1:], patt)
    

springs_txt = open("input.txt")
springs_list = springs_txt.read().strip().split("\n")
springs_list = [item.split() for item in springs_list]
# for i in range(len(springs_list)):
#     springs_list[i][1] = [int(item) for item in springs_list[i][1].split(",")]

# print(springs_list)

# print(recurse_arrange("#.#.###", [1,1,3])

# print(recurse_arrange(".??..??...?##.", [1,1,3]))

# print(recurse_arrange("?#?#?#?#?#?#?#?", [1,3,1,6]))

# print(recurse_arrange("????.#...#...", [4,1,1]))

# print(recurse_arrange("????.######..#####.", [1,6,5]))

# print(recurse_arrange("?###????????", [3, 2, 1]))

tot_sum = 0
for item in springs_list:
    tot_sum += recurse_arrange(item[0], item[1])
print(tot_sum)

print(recurse_arrange(".??..??...?##.?"*5, "1,1,3,1,1,3,1,1,3,1,1,3,1,1,3"))

tot_sum = 0
for item in springs_list:
    # print((item[0]+"?") * 4 + item[0], item[1]*5)
    tot_sum += recurse_arrange((item[0]+"?") * 4 + item[0], (item[1]+",")*4+item[1])
print(tot_sum)