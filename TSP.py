import sys
import copy
import math

class city:
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.dist_to_city=[]

    def init_dist_to_cities(self,LIST):
        self.dist_to_city=LIST

    def distance(self,CITY):
        d= math.sqrt((self.x - CITY.x)**2 + (self.y - CITY.y)**2)
        return d
    


def load_cities(filename):
    ifile=open(filename)
    cities= []
    type = ifile.readline()
    num_of_cities = int(ifile.readline())
    line = 0
    for new_city in ifile:
        temp = new_city.split()
        new_city = city(float(temp[0]),float(temp[1]))
        cities.append(new_city)
        line +=1
        if(line >= num_of_cities):
            break
    i=0
    for dist in ifile:
        temp = dist.split()
        dist_to_cities = []
        for weight in temp:
            dist_to_cities.append(float(weight))
        cities[i].init_dist_to_cities(dist_to_cities)
        i+=1
    return cities

def simulatedAnnealing(PATHS):
    for path in PATHS:
        best =  [] + path
        C = [] + path
        T = 10**10
        for i in range(0,200): # TODO proper termination criteria later
            N = get_random_neighbor(C)
            delta_E = fitness(N) - fitness(C)
            prob = P(C,N,delta_E)
            if(spin_wheel(prob)):
                C = N
                if(fitness(C) > fitness(best)):
                    best = C
                T = decrease_temp(T,i)
            

graph = load_cities("TestCases/euc_100")

