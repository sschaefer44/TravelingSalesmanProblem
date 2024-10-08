import os
import random

def init_Pop(population_size, cityList):
    population = []
    for i in range(population_size):
        tour = list(range(len(cityList)))
        random.shuffle(tour)
        population.append(tour)
    return population

def calcDist(dists, tour):
    totDist = 0
    for i in range(len(tour)):
        totDist += dists[tour[i-1]][tour[i]]
    return totDist

def selection(population, size, distance):
    selected = []
    for i in range(len(population)):
        randindividuals = random.sample(population, size)
        selectedindividual = min(randindividuals, key=lambda x: calcDist(distance, x))
        selected.append(selectedindividual)
    return selected

def crossover(parent1, parent2):
    beg_Index = random.randint(0, len(parent1)-1)
    fin_Index = random.randint(beg_Index, len(parent1)-1)
    child = [-1] * len(parent1)
    for i in range(beg_Index, fin_Index + 1):
        child[i] = parent1[i]
    rem = [item for item in parent2 if item not in child]
    j = 0
    for i in range(len(parent2)):
        if child[i] == -1:
            child[i] = rem[j]
            j += 1
    return child

def mutation(ind):
    index1, index2 = random.sample(range(len(ind)), 2)
    ind[index1], ind[index2] = ind[index2], ind[index1]

def genetic_Algorithm(pop_size, num_of_gens, tour_size, mutation_rate, distances):
    num_cities = len(distances)
    population = init_Pop(pop_size, Cities)
    for generation in range(num_of_gens):
        parents = selection(population, tour_size, distances)
        offspring = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i+1]
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            if random.random() < mutation_rate:
                mutation(child1)
                mutation(child2)
            offspring.append(child1)
            offspring.append(child2)
        population = offspring
        best_individual = min(population, key=lambda x: calcDist(distances, x))
        print(f"Generation {generation+1}, Best Tour: {best_individual}, Distance: {calcDist(distances, best_individual)}")
    best_solution = min(population, key=lambda x: calcDist(distances, x))
    return best_solution, calcDist(distances, best_solution)

def main():
    global Cities
    Cities = []
    fileName = input("Welcome! Please enter a File Name: ")
    if (os.path.exists(fileName) == False):
       fileName = input("Error! You did not enter a valid file Name. Please enter a valid file name: ")
    with open(fileName, "r") as file:
        N = int(file.readline())
        Cities = []
        for x in range(N):
            Cities.append(file.readline().strip())
        rows, cols = (N, N)
        distArr = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(N):
            distances = file.readline().strip().split()
            for j in range(N):
                value = int(distances[j])
                distArr[i][j] = value
    
    population_size = 50
    num_generations = 100
    tournament_size = 5
    mutation_rate = 0.1

    best_solution, best_distance = genetic_Algorithm(population_size, num_generations, tournament_size, mutation_rate, distArr)
    print(f"Best Tour: {best_solution}, Distance: {best_distance}")

main()
