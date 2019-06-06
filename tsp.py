import networkx as nx
from mip import gurobi_solution
from utils import *
import numpy as np

class tsp:

    def __init__(self,points):
        self.grafo = nx.Graph()
        edges = []
        for i in range(0, len(points) - 1):
            for j in range(i, len(points)):
                if i != j: edges.append((i, j, length(points[i], points[j])))
        self.grafo.add_weighted_edges_from(edges)
        self.points = points

    def approximation2(self,ver=False):
        # You might want to use the function "nx.minimum_spanning_tree(g)"
        # which returns a Minimum Spanning Tree of the graph
        gm = nx.minimum_spanning_tree(self.grafo)
        # You also might want to use the command "list(nx.dfs_preorder_nodes(graph, 0))"
        # which gives a list of vertices of the given graph in depth-first preorder.
        # print(nx.dfs_preorder_nodes(gm, 0))
        circuit = list(nx.dfs_preorder_nodes(gm, 0))
        edges = generateListEdges(circuit, self.points)
        if ver:
            return verbose(circuit, sumaCoste(edges))
        return [circuit, sumaCoste(edges)]

    def gurobi_method(self):
        solution = gurobi_solution(self.points)
        return verbose(solution[1],solution[0])

    def christofides(self,ver=False):

        # You might want to use the function "nx.minimum_spanning_tree(g)"
        # which returns a Minimum Spanning Tree of the graph g
        gm = nx.minimum_spanning_edges(self.grafo)
        listEdges = [(i[0], i[1], i[2]['weight']) for i in list(gm)]

        multiGraph = nx.MultiGraph()
        multiGraph.add_weighted_edges_from(listEdges)
        # nx.max_weight_matching(W, maxcardinality = True)
        # which computes a maximum-weighted matching of W.
        x = [n for n, i in nx.degree(multiGraph) if i % 2 != 0]
        edges = []
        for i in range(0, len(x) - 1):
            for j in range(i, len(x)):
                if i != j: edges.append((x[i], x[j], -length(self.points[x[i]], self.points[x[j]])))

        graph = nx.Graph()
        graph.add_weighted_edges_from(edges)
        m = list(nx.max_weight_matching(graph, maxcardinality=True))
        edges = []
        for i in m:
            edges.append((i[0], i[1], length(self.points[i[0]], self.points[i[1]])))
        multiGraph.add_weighted_edges_from(edges)
        # You also might want to use the command "list(nx.dfs_preorder_nodes(graph, 0))"
        # which gives a list of vertices of the given graph in depth-first preorder.
        circuit = [i[1] for i in list(nx.eulerian_circuit(multiGraph, source=0))]
        circuit.insert(0, 0)
        circuitHal = []
        for i in circuit:
            if i not in circuitHal:
                circuitHal.append(i)
        edges = generateListEdges(circuitHal, self.points)
        if ver:
            return verbose(circuit, sumaCoste(edges))
        return [circuitHal, sumaCoste(edges)]

    def optimize_model(self, model, cost,method='simulatedAnneling'):
        if method == '2-opt':
            return approx2opt(model,cost, self.points,True)
        elif method == 'simulatedAnneling':
            return simulatedAnneling(model,cost,self.points)
        elif method == 'tabu_search':
            return tabu_search(model,cost,self.points)
        elif method == 'geneticAlgorithm':
            return geneticAlgorithm(model,self.points)
        else:
            return simulatedAnneling(self.points)