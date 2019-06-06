#!/usr/bin/python3.6
import time
from collections import namedtuple
import tsp
import AntSystem
from utils import greedy



Point = namedtuple("Point", ['x', 'y'])

def verbose(coste,camino):
    result=('%.2f' % coste + ' ' + str(0)+"\n")
    for i in camino: result += str(i) + ' '
    return result

def print_solution(NPproblem_tsp, solution,method):
    st = time.time()
    sa = NPproblem_tsp.optimize_model(solution[0],solution[1],method=method)
    ft = time.time() - st
    return sa
    #print("Tiempo emplado: " + str(ft))
    #print("Margen de mejora aproximado: " + str(((solution[1] - sa[1]) / solution[1] * 100)) + " %\n")

def solve_it(input_data, method="",oporation="",solo=False,default=True):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    if len(points) > 30000 and default:
            print("greedy")
            return greedy(points)

    NPproblem_tsp = tsp.tsp(points)
    if default:
        if len(points) > 200:
            approx = NPproblem_tsp.christofides()
            return print_solution(NPproblem_tsp,approx,"simulatedAnneling")
        else:
            approx = NPproblem_tsp.gurobi_method()
            return approx

    if method=='approximation2':
        approx = NPproblem_tsp.approximation2()
    elif method == 'christofides':
        approx= NPproblem_tsp.christofides()
    elif method== 'antSystem':
        Hormigas = AntSystem.AntSystem(points, 1, 2, 0.02, 10, nodeCount, nodeCount)
        algo=Hormigas.calcule_route()
        return verbose(algo[1],algo[0])
    elif method== 'gurobi':
        approx = NPproblem_tsp.gurobi_method()
        return approx
    else:
        approx = NPproblem_tsp.christofides()
    if solo:
        return verbose(approx[1],approx[0])
    else:
        return print_solution(NPproblem_tsp,approx,oporation)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        if len(sys.argv)>3:
            if sys.argv[2].strip()=='-m' :
                if len(sys.argv)>5:
                    if sys.argv[4].strip()=='-o' :
                        print(solve_it(input_data, sys.argv[3].strip(),sys.argv[5].strip(),default=False))
                    else:
                        print("ERROR operation not suported")
                else:
                    print(solve_it(input_data, sys.argv[3].strip(),solo=True,default=False))
            else:
                print("ERROR operation not suported")
        else:
            print(solve_it(input_data))


    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
