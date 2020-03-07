import random
import copy
import sys

class path:
    # static distance table
    distances = [[0,2,11,3,18,14,20,12,5],[2,0,13,10,5,3,8,20,17],[11,13,0,5,19,21,2,5,8],[3,10,5,0,6,4,12,15,1],[18,5,19,6,0,12,6,9,7],[14,3,21,4,12,0,19,7,4],[20,8,2,12,6,19,0,21,13],[12,20,5,15,9,7,21,0,6],[5,17,8,1,7,4,13,6,0]]
    
    # takes array of nodes in path in order
    def __init__(self, list):
        self.node_order = list
    
    # for printing a path in order of cities traversed
    def __str__(self):
        string = ""
        for x in range(0,len(self.node_order)-1):
            string += str(self.node_order[x]) + " -> "
        string += str(self.node_order[len(self.node_order)-1])
        return string
    
    # for calculating path cost
    def path_cost(self):
        path_length = 0
        for x in range(0, len(self.node_order) - 1):
            path_length += self.distances[self.node_order[x+1]-1][self.node_order[x]-1]
        return path_length
    
    # fitness function returns multiplicative inverse of path sum
    def fitness(self):
        return 1.0 / self.path_cost()
    
    # generates a random path using Fisher-Yates algorithm
    @staticmethod
    def generatePath():
        new_path_list = [1,2,3,4,5,6,7,8,9]
        new_index = 0;
        for x in range(0, len(new_path_list)):
            # pick a random index in the path
            new_index = random.randint(0,8)
            # swap the x'th node with the node at the new index
            new_path_list[x], new_path_list[new_index] = \
                new_path_list[new_index], new_path_list[x]
        new_path_list.append(new_path_list[0])
        new_path = path(new_path_list)
        return new_path

# randomly selects a parent based on fitness (takes sorted pop and cumulative fitness) 
def random_selection(population, total_fit):
    prob = random.random() # generate a prob in [0.0,1.0)
    cum_prob = 0.0 # set a cumulative probability    
    ind = 0 # set index of which element to search
    while ind < len(population) and cum_prob < prob : #seek until cumulative probability reached
        cur_fit_prob = population[ind].fitness() / total_fit
        cum_prob += cur_fit_prob
        ind += 1
    return population[ind - 1] # return chosen parent

# produce child based on parent 1 and parent 2
def reproduce(p1, p2):
    # chop off last node of each parent (as it is duplicate data)
    del p1.node_order[-1]
    del p2.node_order[-1]
    # initially set child to p2
    child = copy.deepcopy(p2)
    # stochastically pick a segment from parent 1 (up to the entire array)
    ind1 = random.randint(0,len(p1.node_order)-1)
    ind2 = random.randint(0,len(p1.node_order)-1)
    # if they are out of order, swap them
    if ind1 > ind2:
        ind1, ind2 = ind2, ind1
    # delete the selected elements from p2
    for x in range(ind1,ind2+1): 
        toDelete = p1.node_order[x] # set number to delete in child
        child.node_order.remove(toDelete) # delete that element from child
    # insert whole segment from p1 into child
    for x in range(ind1,ind2+1):
        child.node_order.insert(x,p1.node_order[x])
    # copy back last node from first node
    child.node_order.append(child.node_order[0])
    return child

# mildly mutate a state by randomly swapping two cities in state
def mutate(child):
    index1 = random.randint(1,7)
    index2 = random.randint(1,7)
    while index2 == index1:
        index2 = random.randint(1,7)
    # swap cities in route
    child.node_order[index1], child.node_order[index2] = \
        child.node_order[index2], child.node_order[index1]

# calculate total fitness (for assigning probability to each path in pop)
def total_pop_fitness(population):
    total_fitness = 0
    for iterator in population:
        total_fitness += iterator.fitness()
    return total_fitness    

# primary function returns solution
def genetic_algorithm(population, num_trials):
    # REPEAT
    for i in range(0, num_trials):
        # reset new population
        new_population = []
        # sort population by fitness (most fit at lowest index)
        population = sorted(population, key = path.fitness, reverse = True)
        # generate new population from children of stochastically selected parents
        for j in population:
            dad = random_selection(population, total_pop_fitness(population))
            mom = random_selection(population, total_pop_fitness(population))
            child = reproduce(copy.deepcopy(dad), copy.deepcopy(mom)) # generate first child
            # mutate child with small probability
            prob = random.random()
            if prob < .1 :
                mutate(child)
            # add child to new_pop
            new_population.append(child) 
        # overwrite our original population with offspring
        population = new_population
    # sort according to fitness function
    population = sorted(population, key = path.fitness, reverse = True)      
    # return best path
    return population[0]
    
def main():
    init_pop_size = 20 # default pop size (if not provided from system)
    num_trials = 1000  # default number of trials (if not provided from system)
    if len(sys.argv) < 2: # no output file provided
        output_file = open('TSOut.txt','a')
    else : # if output file specified
        output_file = open(sys.argv[1], 'a')
    if len(sys.argv) > 2: # grab initial pop size from command line
        init_pop_size = int(sys.argv[2])
    if len(sys.argv) > 3: # grab number of trials from command line
        num_trials = int(sys.argv[3])
        
    # generate initial population
    initPopulation = []    
    for _ in range(0,init_pop_size):
        initPopulation.append(path.generatePath())   
    # find solution using genetic algorithm
    best_solution = genetic_algorithm(initPopulation, num_trials)
    # print data to output file
    print(best_solution, file = output_file)
    print("Solution has path cost: " + str(best_solution.path_cost()), file = output_file)
    print(str(best_solution.path_cost())) # print answer to std out
main()