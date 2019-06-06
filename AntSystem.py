import numpy as np
import math as m
from utils import length
import random


def calculate_array2D_cost(points,ants,cities):
    cost = np.empty((ants,cities))
    for row in range(ants):
        for column in range(cities):
            if row != column:
                cost[row][column] = length(points[row],points[column])
            else:
                cost[row][column] = -1
    return cost

class AntSystem:

    def transition_probabilities(self,r,s,sum_cost):
        return (m.pow(self.pheromones[r][s],self.alpha)*m.pow(self.heuristics[r][s],self.beta))/sum_cost

    def update_pheromones(self,delta):
        self.pheromones=(self.decrease*self.pheromones)+delta

    def __init__(self, points, alpha, beta, decrease,initial_pheromones, ants, cities):
        self.alpha = alpha
        self.beta = beta
        self.ants = ants
        self.decrease = decrease
        self.cities = cities
        self.pheromones = initial_pheromones+np.zeros((self.ants,self.cities))
        self.cost = calculate_array2D_cost(points,self.ants,self.cities)
        self.heuristics = 1/self.cost

    def calcule_route(self,stop=2):
        solution = []
        cost_repeated = 0
        while cost_repeated <= stop:
            ants_solution = []
            delta = np.zeros((self.ants, self.cities))
            for ant in range(self.ants):
                iteration_solution = [ant]
                #ciclos
                for _ in range(self.cities):
                    sum_cost = sum([m.pow(self.pheromones[ant][city],self.alpha)*m.pow(self.heuristics[ant][city],self.beta)
                                    for city in range(self.cities) if city != ant and city not in iteration_solution])
                    probabilities = [(self.transition_probabilities(ant,city,sum_cost),city)
                                    for city in range(self.cities) if city != ant and city not in iteration_solution]
                    u = random.random()
                    length = len(iteration_solution)
                    for p in probabilities:
                        if p[0] > u:
                            iteration_solution.append(p[1])
                            break
                    if probabilities and len(iteration_solution) == length:
                        iteration_solution.append(probabilities[0][1])

                cost_ant = 0
                for edge in range(len(iteration_solution) - 1):
                    cost_ant += self.cost[iteration_solution[edge]][iteration_solution[edge+1]]
                cost_ant += self.cost[iteration_solution[-1]][iteration_solution[0]]
                ants_solution.append((iteration_solution,cost_ant))
                cost_heuristics=1/cost_ant

                matrix_aux = np.zeros((self.ants,self.cities))
                for edge in range(len(iteration_solution) - 1):
                    matrix_aux[iteration_solution[edge]][iteration_solution[edge + 1]]+=cost_heuristics
                matrix_aux[iteration_solution[-1]][iteration_solution[0]]+=cost_heuristics

                delta = delta +  matrix_aux
            self.update_pheromones(delta)
            ants_solution.sort(key=lambda comp: comp[1])
            if not solution:
                solution = ants_solution[0]
            else:
                if solution[0][1] > ants_solution[0][1]:
                    solution = ants_solution[0]
                else:
                    cost_repeated+=1
        return solution


    def print(self):
        print("Feromanas\n" + str(self.pheromones))
        print("Coste\n" + str(self.cost))
        print("Heuristics\n" + str(self.heuristics))
