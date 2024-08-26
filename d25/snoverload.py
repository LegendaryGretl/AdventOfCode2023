class Graph():
    def __init__(self, input_str):
        self.G = {}

        for line in input_str.strip().split("\n"):
            lhs, rhs = line.split(": ")
            rhs = rhs.split(" ")
            for v in rhs:
                edge = (lhs, v)
                if lhs in self.G.keys():
                    self.G[lhs].append(edge)
                else:
                    self.G[lhs] = [edge]

                if v in self.G.keys():
                    self.G[v].append(edge)
                else:
                     self.G[v]= [edge]
               
    def getNeighbors(self, vertex):
        # returns list of neighbors in form (vertex, edge)
        edges = self.G[vertex]
        neighbors = []
        for e in edges:
            for item in e:
                if item != vertex:
                    neighbors.append((item, e))
        return neighbors
    
    def getNeighborsExculdingCuts(self, vertex, cuts):
        # returns list of neighbors in form (vertex, edge)
        edges = self.G[vertex]
        neighbors = []
        for e in edges:
            if e in cuts:
                continue
            for item in e:
                if item != vertex:
                    neighbors.append((item, e))
        return neighbors

    def BFS(self, start, end):
        # frontier keeps current node, list of edges
        frontier = [(start, [])]
        visited = [start]
        while len(frontier) > 0:
            frontier.sort(key=lambda x:len(x[1])) # min edge path length
            cur_v, edge_path = frontier.pop(0)
            if cur_v == end:
                return edge_path
            for n, e in self.getNeighbors(cur_v):
                if n not in visited:
                    frontier.append((n, edge_path + [e]))
                    visited.append(n)
        return []

    def BFStoAll(self, start):
        # frontier keeps current node, list of edges
        frontier = [(start, [])]
        visited = [start] 
        edges = []
        while len(frontier) > 0:
            # frontier.sort(key=lambda x:len(x[1])) # min edge path length
            temp = min(frontier, key=lambda x: len(x[1]))
            cur_v, edge_path = temp
            frontier.remove(temp)
            # cur_v, edge_path = frontier.pop(0)
            if len(visited) == len(list(self.G.keys())):
                return edges
            for n, e in self.getNeighbors(cur_v):
                if n not in visited:
                    frontier.append((n, edge_path + [e]))
                    visited.append(n)
                    if e not in edges:
                        edges += edge_path
        return []
    
    def BFSExcludingCuts(self, start, end, cuts):
        # frontier keeps current node, list of edges
        frontier = [[start]]
        visited = [start]
        while len(frontier) > 0:
            frontier.sort(key=lambda x:len(x))
            cur_path = frontier.pop(0)
            cur_v = cur_path[-1]
            if cur_v == end:
                return cur_path
            for n, e in self.getNeighborsExculdingCuts(cur_v, cuts):
                if n not in visited:
                    frontier.append(cur_path + [n])
                    visited.append(n)
        return []

    def findHotPaths(self):
        edge_counter = {}
        V = list(self.G.keys())
        for i in range(len(V)):
            v = V[i]
            edges = self.BFStoAll(v)
            for e in edges:
                if not e in edge_counter.keys():
                    edge_counter[e] = 1
                else:
                    edge_counter[e] += 1
        edge_counter = dict(sorted(edge_counter.items(), key=lambda item: item[1]))
        return list(edge_counter.keys())[-3:]
    
    def findGroups(self):
        cuts = self.findHotPaths()
        v = list(self.G.keys())[0]
        reached = 1
        unreached = 0
        for dest in list(self.G.keys())[1:]:
            path = self.BFSExcludingCuts(v, dest, cuts)
            if len(path) > 0:
                reached += 1
            else:
                unreached += 1
        return reached * unreached
    
input_str = open("input.txt").read().strip()
biggySmalls = Graph(input_str)
print(biggySmalls.findGroups())
    
        