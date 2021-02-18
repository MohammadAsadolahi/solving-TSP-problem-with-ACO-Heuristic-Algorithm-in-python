#   soving Travelling salesman(TSP) using ant colony
#   by mohammad asadolahi
#   mohmad.asa1994@gmail.com
import math
import random
import matplotlib.pyplot as plt

class Draw:
    def DrawSolutionPlot(self, cities, path: list, gen=""):
        if gen != "":
            plt.title(f'Best Path untill Generation:{gen}')
        x = []
        y = []
        for point in cities:
            x.append(point['x'])
            y.append(point['y'])
        plt.plot(x, y, 'co')
        for route in range(1, len(path)):
            source = path[route - 1]
            destination = path[route]
            plt.arrow(x[source], y[source], x[destination] - x[source], y[destination] - y[source], color='r',
                      length_includes_head=True)
        plt.xlim(0, max(x) * 1.1)
        plt.ylim(0, max(y) * 1.1)
        plt.show()

class ACO:
    def __init__(self, cities, cityCount, antCount, evaporationRate):
        self.cities = cities
        self.cityCount = cityCount
        self.costMatrix = []
        self.antCount = antCount
        self.PheromoneMatrix = []
        self.initialDistances()
        self.evaporationRate = evaporationRate
        self.draw = Draw()

    def applyEvaporatio(self):#every generation we reduce all cells in pheromone matrix to simulate evaporation of pheromone
        for row in range(self.cityCount):
            for col in range(self.cityCount):
                if (self.PheromoneMatrix[row][col] - self.evaporationRate) < 0.000001:
                    self.PheromoneMatrix[row][col] = 0.000001
                else:
                    self.PheromoneMatrix[row][col] -= self.evaporationRate

    def solve(self, generations):
        step = 0
        if generations > 10:
            step = int(generations / 10)
        bestRoute = list(range(self.cityCount))
        random.shuffle(bestRoute)
        self.draw.DrawSolutionPlot(self.cities, bestRoute,f"random solution with cost: {self.getRouteCost(bestRoute)}")
        for generation in range(generations):
            for ant in range(self.antCount):
                route = []
                allowedList = list(range(self.cityCount))
                currentCity = random.randint(0, cityCount - 1)
                allowedList.remove(currentCity)
                route.append(currentCity)
                for cityNum in range(self.cityCount - 1):
                    nextCity = self.getNextCity(currentCity, allowedList,generation)
                    route.append(nextCity)
                    allowedList.remove(nextCity)
                    currentCity = nextCity
                if self.getRouteCost(route) < self.getRouteCost(bestRoute):
                    bestRoute = route[::]
                self.updatePheromone(route,generation+1)
            self.applyEvaporatio()
            if (generation % step) == 0:
                self.draw.DrawSolutionPlot(self.cities, bestRoute,
                                           f"{generation} with cost: {self.getRouteCost(bestRoute)}")
            print(f"generation:{generation}  best route is: {bestRoute}  with cost of: {self.getRouteCost(bestRoute)}")
        self.draw.DrawSolutionPlot(self.cities, bestRoute, f"{generations} with cost: {self.getRouteCost(bestRoute)}")
        self.draw.DrawSolutionPlot(self.cities, bestRoute, f"{generations} with cost: {self.getRouteCost(bestRoute)}")
        print("-------------------------------------------------------")
        for line in self.PheromoneMatrix:
            print(line)

    def getNextCity(self, currentCity, allowedList, generation):#we give this function a list of reamainedc cities and it choose one for next destination of ant by selection chance of every city
        probabilities = []
        sum = 0
        for city in allowedList:
            sum += self.PheromoneMatrix[currentCity][city]/self.costMatrix[currentCity][city]#we sum all phromones, if we divide it by cost of path then the chace of shorter pathes will increase
        for city in allowedList:
            probabilities.append(((self.PheromoneMatrix[currentCity][city]/self.costMatrix[currentCity][city]) / sum)) #we divide phromone in path of every city we can go and devide it to sum of all phromones to get the real chance of choosing the city, more phromone of a path leads to more chance to be selected by ant to go
        return random.choices(allowedList, weights=probabilities, k=1)[0]#  we choose one city in list of allowed cities by its chance

    def updatePheromone(self, route: list,generation):
        pheromoneChange = math.sqrt(1/self.getRouteCost(route)) #divideng 1 by route cost will give greater number for shorter distances, so shorter path get greater phromone in cities sequences
        for case in range(1, len(route)):
            source = route[case - 1]
            destination = route[case]
            self.PheromoneMatrix[source][destination] += pheromoneChange
            self.PheromoneMatrix[destination][source] += pheromoneChange # we update i,j in pheromone matrix just like j,i so the phromone for city1,city2 is equal to phromone of city2,city1

    def getRouteCost(self, route: list): #return cost of a route. for route like: "a,b,c" we sum "a->b" and "b->c" distances and returns it
        totalRouteCost = 0
        for case in range(1, len(route)):
            source = route[case - 1]
            destination = route[case]
            totalRouteCost += self.costMatrix[source][destination]
        return totalRouteCost

    def initialDistances(self): # initial n*n distance matrix and put Euclidean distances in it and n*n pheromone matrix gets initialized with 0.1 in every cell
        for i in range(cityCount):
            row = []
            pheromone = []
            for j in range(cityCount):
                row.append(self.getDistance(self.cities[i], self.cities[j]))
                pheromone.append(0.1)
            self.costMatrix.append(row)
            self.PheromoneMatrix.append(pheromone)#phromone matrix will be initialized to 0.1

    def getDistance(self, city1: dict, city2: dict): # return Euclidean distance between two cities
        return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


# main commands
# read cities names and disctances from "Cities List.txt" file in project directory
cities = []
cityCount = 0
with open('./Cities List.txt') as f:
    for line in f.readlines():
        city = line.split(' ')
        cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
        cityCount += 1

# cities, cityCount, antCount, evaporationRate)
aco = ACO(cities, cityCount, 15, 0.0008)
aco.solve(160) #run aco for 400 iteration
