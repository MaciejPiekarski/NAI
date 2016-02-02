import random

def create_population():
    population = list()
    for x in range(0,100):
        population.append(random.randint(1,100))
    return population

#Algorytm wspinaczkowy
def climber(f):
    x0 = random.randint(0,len(f)-1)
    print('Indeks elemntu wylosowanego z listy: %s' % x0)
    breaker = 0
    while breaker < len(f)-1:
        breaker += 1
        max = f[x0]
        neighbours = [f[x0-1], f[x0+1]]
        print('Sasiad lewy: %s, Najwiekszy element: %s, Sasiad prawy %s' % (neighbours[0], max, neighbours[-1]))
        for x in neighbours:
            if x > max:
                max = x
        if max == f[x0]:
            break
        x0 = f.index(max)
    return max

#Algorytm ewolucyjny
def create_speciman(chromosome, fit):
    return {'chromosome': chromosome, 'fit': fit}

#selekcja: metoda rankingowa
def select_parents(population):
    # ile procent populacji wybrać (30-60%)
    percent = float(random.randint(3,6))/10
    parents_count = int(len(population)*percent)
    # posortowana lista rodzicow po kondycji
    sorted_population = sorted(population, key=lambda k: k['fit'])
    return sorted_population[:parents_count], sorted_population[parents_count:]

def cross(parents):
	kids = list()
	if len(parents) % 2 == 1:
		# jeżeli liczba rodziców jest nieparzysta najsilniejszy trafia do potomstwa
		kids.append(parents.pop(0))
	while parents:
		first = parents.pop(random.randint(0,len(parents)-1))
		second = parents.pop(random.randint(0,len(parents)-1))
		# podzielone po 4 bity
		bits = random.randint(1,7)
		x = 2**bits-1
		father_genes = [first['chromosome'] >> bits, first['chromosome'] % x]
		mother_genes = [second['chromosome'] >> bits, second['chromosome'] % x]
		first['chromosome'] = (mother_genes[0] << bits) | (father_genes[1])
		second['chromosome'] = (father_genes[0] << bits) | (mother_genes[1])
		kids.append(first)
		kids.append(second)
	return kids

def mutate(population):
	mutated = list()
	for speciman in population:
		if random.randint(0,99) < 2:
			res = speciman
			chromosomeToMutate = '{0:08b}'.format(res['chromosome'])
			chromosomeToMutate = list(chromosomeToMutate)
			index = random.randint(0,len(chromosomeToMutate)-1)
			mutatedChromosome = int(chromosomeToMutate[index]) ^ 1
			chromosomeToMutate[index] = str(mutatedChromosome)
			chromosomeToMutate = "".join(chromosomeToMutate)
			res['chromosome'] = int(chromosomeToMutate, 2)
		else:
			res = speciman
		mutated.append(res)
	return mutated

def calculate_fitness(fitness, population):
	for speciman in population:
		speciman['fit'] = fitness(speciman['chromosome'])

def genetic(fitness, pop_size, gen_count):
	# tworzenie popoulacji jako listy
	population = list()
	for x in range(0, len(pop_size)-1):
		population.append(create_speciman(pop_size[x], 0))
	# wyliczyc fitness dla populacji
	calculate_fitness(fitness, population)
	best = population[0]
	for pop in population:
		print (pop)
	# dla kazdej generacji:
	for generation in range(0, gen_count):
		parents, rest = select_parents(population)
		kids = cross(parents)
		kids = mutate(kids)
		calculate_fitness(fitness, kids)
		population = kids + rest
		chromosomes = []
		for spec in population:
			chromosomes.append(spec['chromosome'])
			if spec['fit'] > best['fit']:
				best = spec
		print (chromosomes)
	return('BEST SPECIMAN: %s' % (best))

def Rosenbrock(population):
    rossum = []
    for x in range(0, len(population)-1):
        rossum.append((1-population[x])**2 + 100*(population[x+1]-population[x]**2)**2)
    return rossum.index(max(rossum))

pop = create_population()
f = lambda x: x**2

print (pop)
print (climber(pop))
print (genetic(f,pop,10))
print (pop[Rosenbrock(pop)])