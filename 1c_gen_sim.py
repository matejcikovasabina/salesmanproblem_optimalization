import random
import matplotlib.pyplot as plt
import math

WIDTH = 200
NUM_CITIES = 20
NUM_INDIVIDUALS = 50
NUM_GENERATION = 500
NUM_LIMIT = 50
MUTATION_RATE = 0.1
MIN_TEMPERATURE = 0.001
TEMPERATURE_RATE = 0.995
TEMPERATURE_START = 1000  
TOURNAMENT_SIZE=3

#randomly selecting 2 different indices and reversing the cities inbetween
def mutate(path):
    new_path = path[:]
    i, j = sorted(random.sample(range(len(path)), 2))
    new_path[i:j] = reversed(new_path[i:j])
    return new_path

def change(first_parent, second_parent, size, mid):
    child = [None] * size #empty child path of the same size as parents
    child[:mid] = first_parent[:mid] #first half from first parent
    #filling remaining cities from second parent but skipping the cities already in the child
    pos = mid
    for city in second_parent:
        if city not in child:
            child[pos] = city
            pos += 1
    return child

# crossover between two parents by swapping their halves to produce two children
def crossover(p1, p2):
    size = len(p1)
    mid = size // 2
    return change(p1, p2, size, mid), change(p2, p1, size, mid)

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# calculates total path distance and its fitness (1 / distance)
def calculate_fitness(path, cities):
    total = 0
    for i in range(len(path)):
        city_a = cities[path[i]]
        city_b = cities[path[(i + 1) % len(path)]]
        total += distance(city_a, city_b)
    fitness = 1 / total
    return fitness, total

def roulette_wheel_selection(population, fitnesses):
    total = sum(fitnesses)
    r = random.random()
    counter = 0.0
    # iterating through all individuals and their corresponding fitness values
    for ind, f in zip(population, fitnesses):
        counter += f / total # adding individual s probability
        if r <= counter: #if random number falls into this range, the parent is this individual
            return ind
    return population[-1]

#generates path as a list of cities indices
def random_path():
    path = list(range(NUM_CITIES))
    random.shuffle(path)
    return path

def tournament_selection(population, fitnesses):
    idxs = random.sample(range(len(population)), TOURNAMENT_SIZE) #randomly selecting a small subset from population
    best_i = max(idxs, key=lambda i: fitnesses[i]) #finding the index of the individual with highest fitness
    return population[best_i]

def genetic_algorithm(cities, selection_type):
    history = [] #saving the best length of each generation
    individuals = [] #saving all paths in one generation
    #generating first generation
    for i in range(NUM_INDIVIDUALS):
        path = random_path() 
        individuals.append(path)

    population = [] #each element: (fitness, length)
    for p in individuals:
        fitness, length = calculate_fitness(p, cities) #using 1/length for maximazing fitness
        population.append((fitness, length))
    generation = 1
    no_improve_count = 0
    #runs until reaches total number of generation or generations with no improvement reached the allowed limit 
    while generation <= NUM_GENERATION and no_improve_count < NUM_LIMIT:
        sorted_pop = sorted(zip(population, individuals), key=lambda x: x[0], reverse=True) #sorting the population in discending order by fitness
        (best_fit, best_length), best_path = sorted_pop[0]
        (_, _), second_best_path = sorted_pop[1]
        new_population = [best_path, second_best_path] #two best paths moved to next generation
        history.append(best_length) #saving best length (distance) from one generation

        while len(new_population) < NUM_INDIVIDUALS:
            if selection_type == "tournament":
                # select parents using tournament selection
                p1 = tournament_selection(individuals, [f for f, _ in population])
                p2 = tournament_selection(individuals, [f for f, _ in population])
            elif selection_type == "roulette":
                # select parents using roulette wheel selection
                p1 = roulette_wheel_selection(individuals, [f for f, _ in population])
                p2 = roulette_wheel_selection(individuals, [f for f, _ in population])

            # crossover to produce children
            c1, c2 = crossover(p1, p2)
            new_population.extend([c1, c2])

        individuals = [] #new paths for next generation
        for p in new_population[:NUM_INDIVIDUALS]:
            #applying mutation on paths with probability = MUTATION_RATE
            if random.random() < MUTATION_RATE:
                mutated = mutate(p)   
                individuals.append(mutated)
            else:        
                individuals.append(p)

        population = []  
        #calculating fitness and length for new generation
        for p in individuals:
            fitness, length = calculate_fitness(p, cities) 
            population.append((fitness, length)) 

        # tracking whether the best fitness improved - reset or increase the no-improvement counter
        (current_best_fit, _), _ = max(zip(population, individuals), key=lambda x: x[0])
        if current_best_fit > best_fit:
            best_fit = current_best_fit
            no_improve_count = 0
        else:
            no_improve_count += 1
        generation += 1

    return best_path, history, best_length

def sim_algorithm(cities):
    history = [] #saving the best length (energy) in each generation
    history_t = []
    path = random_path() #generates the initial random path
    _, length = calculate_fitness(path, cities) #we re using length (distance) to minimize the "energy"
    history.append(length)
    temperature = TEMPERATURE_START
    #alogirthm runs until the temperature reaches limit
    while temperature > MIN_TEMPERATURE: 
        new_path = mutate(path) #new candidate
        _, new_length = calculate_fitness(new_path, cities)
        deltaE = new_length - length #deltaE - the change in energy
        #better solution accepting immideately
        if deltaE < 0:
            path = new_path
            length = new_length
        #worse solution accpting with probabilty
        else:
            #the worse the solution and the lower the temperature, the smaller chance of accepting
            probability = math.exp(-deltaE / temperature)
            if probability > random.random():
                path = new_path
                length = new_length
        history.append(length)
        history_t.append(temperature)
        #lowering the temperature to lower the probabilty
        temperature *= TEMPERATURE_RATE

    return path, history, history_t

#generating a list of cities with random coordinates, each city represented as touple (x,y)
def generated_cities():
    cities = []
    for i in range(NUM_CITIES):
        city = (random.randint(1, WIDTH), random.randint(1, WIDTH)) 
        cities.append(city)
    return cities

print("1 - genetic algorithm")
print("2 - simulated annealing")
algorithm = int(input())

if algorithm == 1:
    cities = generated_cities()
    print("1 - Tournament selection")
    print("2 - Roulette selection")
    print("3 - Both (compare tournament & roulette)")
    choice = int(input())
    if choice == 1 or choice == 2:
        if choice == 1:
            selection_type = "tournament"
            title_method = "Tournament selection"
        else:
            selection_type = "roulette"
            title_method = "Roulette selection"

        best_path, history, best_length = genetic_algorithm(cities, selection_type)

        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        order = best_path + [best_path[0]]
        x = [cities[i][0] for i in order]
        y = [cities[i][1] for i in order]
        plt.plot(x, y, marker="o")
        plt.title(f"{title_method} – Best path")

        plt.subplot(1, 2, 2)
        plt.plot(range(1, len(history) + 1), history, "bo-")
        plt.title(f"{title_method} – Path length over generations")

        plt.tight_layout()
        plt.show()

    elif choice == 3:
        best_path_t, history_t, _ = genetic_algorithm(cities, "tournament")
        best_path_r, history_r, _ = genetic_algorithm(cities, "roulette")

        plt.figure(figsize=(12, 10))

        # tournament – best path
        plt.subplot(2, 2, 1)
        order_t = best_path_t + [best_path_t[0]]
        x_t = [cities[i][0] for i in order_t]
        y_t = [cities[i][1] for i in order_t]
        plt.plot(x_t, y_t, marker="o")
        plt.title("Tournament selection – Best path")

        # tournament – path length
        plt.subplot(2, 2, 2)
        plt.plot(range(1, len(history_t) + 1), history_t, "bo-")
        plt.title("Tournament selection – Path length over generations")


        # roulette – best path
        plt.subplot(2, 2, 3)
        order_r = best_path_r + [best_path_r[0]]
        x_r = [cities[i][0] for i in order_r]
        y_r = [cities[i][1] for i in order_r]
        plt.plot(x_r, y_r, marker="o")
        plt.title("Roulette selection – Best path")

        # roulette – path length
        plt.subplot(2, 2, 4)
        plt.plot(range(1, len(history_r) + 1), history_r, "bo-")
        plt.title("Roulette selection – Path length over generations")

        plt.tight_layout()
        plt.show()


elif algorithm == 2:
    cities = generated_cities()
    best_path, history, history_t = sim_algorithm(cities)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(history, label="Length")
    axes[0].plot(history_t, label="Temperature")
    axes[0].set_title("length – simulated annealing")
    axes[0].legend()

    order = best_path + [best_path[0]]
    x = [cities[i][0] for i in order]
    y = [cities[i][1] for i in order]
    axes[1].plot(x, y, marker="o")
    axes[1].set_title("simulated annealing – best path")

    plt.tight_layout()
    plt.show()
