import math
import numpy as np
from scipy.optimize import minimize

class Graph:
    def __init__(self, vertices):
        self.V = len(vertices)
        self.vertices = vertices
        self.steiner_points = []
        self.graph = []
        self.neighboors = {}
        self.mst_edges = []
        self.total_length = 0

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])
    
    @staticmethod
    def distance(v1, v2):
        x1, y1 = v1
        x2, y2 = v2
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance
    
    @staticmethod
    def angle(A, B, C):
        x1, y1 = A
        x2, y2 = B
        x3, y3 = C

        vector_AB = (x2 - x1, y2 - y1)
        vector_BC = (x2 - x3, y2 - y3)

        dot_product = vector_AB[0] * vector_BC[0] + vector_AB[1] * vector_BC[1]
        magnitude_AB = math.sqrt(vector_AB[0]**2 + vector_AB[1]**2)
        magnitude_BC = math.sqrt(vector_BC[0]**2 + vector_BC[1]**2)

        angle_radians = math.acos(dot_product / (magnitude_AB * magnitude_BC))

        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

    def search(self, parent, i):
        # search for parent vertex in Kruskal algorithm
        if parent[i] == i:
            return i
        return self.search(parent, parent[i])
    
    def fill_neighboors(self, mst):
        # get list of neighbooring vertices for each vertex
        for u, v in mst: 
            if u in self.neighboors:    
                self.neighboors[u].append(v)
            else:
                self.neighboors[u] = [v]
            if v in self.neighboors:    
                self.neighboors[v].append(u)
            else:
                self.neighboors[v] = [u]

    def apply_union(self, parent, rank, x, y):
        # unite two sections of graph
        xroot = self.search(parent, x)
        yroot = self.search(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
 
    def mst(self):
        # kruskal algorithm for finding minimum spanning tree
        self.graph = []
        self.V = len(self.vertices)
        keys = list(self.vertices.keys())
        for key1 in keys[:-1]:
            for key2 in keys[key1 + 1:]:
                self.add_edge(key1, key2, Graph.distance(self.vertices[key1], self.vertices[key2]))
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.search(parent, u)
            y = self.search(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        self.total_length = sum([w for _, _, w in result])
        self.mst_edges = [(u,v) for u, v, _ in result]

    def min_angle_and_point(self, u, v):
        min_angle = 180
        point = 0
        if len(self.neighboors[v]) < 2:
            return min_angle, point
        neighboors = self.neighboors[v]
        for neighboor in neighboors:
            if neighboor == u or self.vertices[v] == self.vertices[neighboor]: continue
            angle = Graph.angle(self.vertices[u], self.vertices[v], self.vertices[neighboor])
            if angle < min_angle: 
                min_angle = angle
                point = neighboor
        return min_angle, point        

    def objective_function(self, candidate, vertices):
        return sum(Graph.distance(candidate, vertex) for vertex in vertices)
    
    def fermat_point(self, vertices, initial_guess):
        # constraints = ({'type': 'ineq', 'fun': lambda x: sum(x) - 1})
        # result = minimize(self.objective_function, initial_guess, args=(vertices,), constraints=constraints, method='COBYLA')

        result = minimize(self.objective_function, initial_guess, args=(vertices,), method='Nelder-Mead')

        return (result.x[0], result.x[1])
        
    def steiner(self):
        # find minimal steiner tree
        self.mst()
        self.fill_neighboors(self.mst_edges)
        for m, n in self.mst_edges:
            u, v = m, n 
            if u not in self.neighboors[v]: continue
            min_angle, point = self.min_angle_and_point(u, v)
            if min_angle >= 120: 
                u, v = n, m
                min_angle, point = self.min_angle_and_point(u, v)
            if min_angle < 120:    
                self.neighboors[v] = [x for x in self.neighboors[v] if x != u and x != point]
                self.neighboors[u] = [x for x in self.neighboors[u] if x != v]
                self.neighboors[point] = [x for x in self.neighboors[point] if x != v]
                steiner_point_index = len(self.vertices)
                self.vertices[steiner_point_index] = self.vertices[v]
                self.steiner_points.append(steiner_point_index)
                self.neighboors[steiner_point_index] = [u, v, point]
                self.neighboors[u].append(steiner_point_index)
                self.neighboors[v].append(steiner_point_index)
                self.neighboors[point].append(steiner_point_index)
        eps = 100
        while eps > 0.001:
            for key in self.steiner_points:
                initial_steiner_position = self.vertices[key]
                vertices = []
                neigboors = self.neighboors[key]
                for neighboor in neigboors:
                    coords = self.vertices[neighboor]
                    vertices.append([i for i in coords])
                vertices = np.array(vertices)    
                fermat_point = self.fermat_point(vertices, self.vertices[key])
                self.vertices[key] = fermat_point
                improvement = Graph.distance(initial_steiner_position, fermat_point)
                if improvement < eps:
                    eps = improvement
     
        self.mst()

def steiner_tree(vertices): 
    g = Graph(vertices)
    g.steiner()
    return g