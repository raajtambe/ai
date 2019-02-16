import sys
import copy
import math

class city:
    
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.distance=[]

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
		line +=1
		if(line > num_of_cities):
			break
		temp = new_city.split()
		new_city = city(float(temp[0]),float(temp[1]))
		cities.append(new_city)
	return cities

graph = load_cities("euc_100")


print(len(graph))