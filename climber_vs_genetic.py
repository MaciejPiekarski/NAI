import random, math

def climber(f):
	x0 = random.randint(0,1000)
	print('x0: %s' % (x0))
	breaker = 0
	while breaker < 1000:
		breaker += 1
		max = x0
		neighbours = [max - 1, max + 1]
		for x in neighbours:
			print('f(%s) = %s > f(%s) = %s' % (x, f(x), max, f(max)))
			if f(x) > f(max):
				max = x
		if max == x0:
			break
		x0 = max
	return max

def create_speciman(chromosome, fit):
	return {'chromosome': chromosome, 'fit': fit}

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
	for x in range(0, pop_size):
		population.append(create_speciman(random.randint(0,255), 0))
	# wyliczyc fitness dla populacji
	calculate_fitness(fitness, population)
	best = population[0]
	print (population)
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

f = lambda x: math.sin((math.pi*x)/128)
#f = lambda x: sum(x**2)

x = genetic(f, 10, 10)
#print (climber(f))
print (x)