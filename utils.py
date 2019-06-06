import math
import random
def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def generateListEdges(circuit, points):
    edges = []
    for i in range(0, len(points) - 1):
        edges.append((circuit[i], circuit[i + 1], length(points[circuit[i]], points[circuit[i + 1]])))
    edges.append((circuit[0], circuit[len(circuit) - 1], length(points[circuit[0]], points[circuit[len(circuit) - 1]])))
    return edges

def sumaCoste(edges):
    return sum([i[2] for i in edges])

def verbose(coste,camino):
    result='%.2f' % coste + ' ' + str(0)+"\n"
    for i in camino: result += str(i) + ' '
    return result

def greedy (points):
    nodeCount=len(points)
    solution = range(0, nodeCount)
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount - 1):
        obj += length(points[solution[index]], points[solution[index + 1]])
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data+= ' '.join(map(str, solution))
    return output_data

def approx2opt(param,cost,points,ver=False):
    for k in range(0,len(param)-2):
        for i in range(k,len(param) - 2):
            new_cost = calculate_cost_movement(param,cost,points,k, i+2)
            if new_cost < cost:
                param[k:i + 3] = list(reversed(param[k:i + 3]))
                cost = new_cost
    if ver:
        return verbose(cost,param)
    return cost

def calculate_cost_movement(solution,cost,points,pos1,pos2):
    if pos1 == 0 and pos2 == len(solution)-1:
        return cost
    if pos2 == len(solution) - 1:
        pos2_next = 0
    else:
        pos2_next = pos2 + 1
    aux = cost - (length(points[solution[pos1 - 1]], points[solution[pos1]]) + length(points[solution[pos2]],
                                                                                           points[solution[pos2_next]]))
    return aux + (length(points[solution[pos1 - 1]], points[solution[pos2]]) + length(points[solution[pos1]],
                                                                                           points[solution[pos2_next]]))


def simulatedAnneling(solution,costX,points,alpha=0.95, temperature=10, inter=10000, stopIter=1000000, stopTemperature=0.00001):
    aux = solution.copy()
    stop=0
    best_solution = costX
    while(temperature>stopTemperature and stopIter>=stop ):
        for _ in range(inter):
            pos1 = random.randint(0, len(solution)-2)
            pos2 = random.randint(pos1+1, len(solution)-1)
            costY = calculate_cost_movement(aux,costX,points,pos1,pos2)
            delta = costY-costX
            if delta < 0:
                best_solution_ar=aux
                aux[pos1:pos2 + 1] = list(reversed(aux[pos1:pos2 + 1]))
                costX=costY
                best_solution=costY
                solution[pos1:pos2+1] = list(reversed(solution[pos1:pos2+1]))
            else:
                u = random.random()
                if u < math.exp(-delta/temperature):
                    aux[pos1:pos2+1] = list(reversed(aux[pos1:pos2+1]))
                    costX=costY
        temperature=alpha*temperature
        stop+=1
    return verbose(best_solution,best_solution_ar)

def max_array(max_ran):
    max_ran_copy=max_ran.copy()
    primero=0
    segundo=0
    max_ran_copy.sort(reverse=True)
    for i in range(len(max_ran_copy)):
        if max_ran_copy[0]==max_ran[i]:
            primero=i
        if max_ran_copy[1]==max_ran[i]:
            segundo=i
    return primero,segundo
def darwin(set):
    sum_generation=sum([i[1] for i in set])
    probability = [i[1] / sum_generation for i in set]
    father=0
    mother=0
    max_ran=[0 for _ in range(len(set))]
    for i in range(len(probability)):
        for k in range(round(probability[i]*100)):
            ran=random.randint(0,10000000)
            if ran>= max_ran[i]:
                max_ran[i]=ran
    father,mother=max_array(max_ran)
    return (set[father],set[mother])

def election_partial(partial1,partial2):
    if partial1 and partial2:return True
    for i in partial1:
        for j in partial2:
            if i == j: return True
    return False


def partial_crossing(father,mather,points):
    partial_father=[]
    partial_mather=[]
    pos1=0
    pos2=0
    while(election_partial(partial_father,partial_mather)):
        pos1 = random.randint(0, len(father) - 2)
        pos2 = random.randint(pos1 + 1, len(father) - 1)
        partial_father = father[pos1:pos2]
        partial_mather = mather[pos1:pos2]
    son = [-1 for _ in mather]
    son[pos1:pos2] = partial_father
    for i in range(len(mather)):
        if not pos1<=i<pos2:
            if  mather[i] in partial_father:
                son[i]=partial_mather[partial_father.index(mather[i])]
            else:
                son[i] = mather[i]
    return [son,sumaCoste(generateListEdges(son,points))]

def geneticAlgorithm (solution,points,number=4, generation=10, mutan=1):
    set = []
    for _ in range(number):
        individuo=random.sample(solution,k=len(solution))
        adptitud = sumaCoste(generateListEdges(individuo,points))
        set.append([individuo,adptitud])
    for _ in range(generation):
        father,mather = darwin(set)
        son = partial_crossing(father[0],mather[0],points)
        if mutan <= random.randint(1,100):
            son[1] = approx2opt(son[0],son[1],points)
        set[-1] = son
    set.sort(key=lambda comp: comp[1])
    return verbose(set[0][1],set[0][0])

def tabu_search(solution,cost,points,count=5,iter=100000):
    tabu_list = []
    for _ in range(iter):
        if not tabu_list:
            for i in tabu_list:
                i.decrease()
                if i == 0: tabu_list.remove(i)
        pos1 = random.randint(0, len(solution)-2)
        pos2 = random.randint(pos1+1, len(solution)-1)
        new_cost = calculate_cost_movement(solution,cost,points,pos1,pos2)
        potential_tabu=tabu(solution[pos1],solution[pos2],count)
        if potential_tabu not in tabu_list and new_cost < cost:
            tabu_list.append(potential_tabu)
            solution[pos1:pos2+1] = list(reversed(solution[pos1:pos2+1]))
            cost=new_cost
    return verbose(cost,solution)
class tabu:
    def __init__(self,m1,m2,count):
        self.moviment=[m1,m2]
        self.tabu_count = count

    def decrease(self):
        self.tabu_count-=1

    def __eq__(self, other):
        return self.moviment == other.moviment
