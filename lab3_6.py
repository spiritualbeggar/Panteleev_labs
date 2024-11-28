import random

# Генерация случайного графа
def generate_random_graph(num_items, max_weight, max_value):
    weights = [random.randint(1, max_weight) for _ in range(num_items)]  # Случайные веса
    values = [random.randint(1, max_value) for _ in range(num_items)]  # Случайные ценности
    weight_limit = random.randint(sum(weights) // 2, sum(weights))  # Ограничение на общий вес
    return weights, values, weight_limit

# Генерация случайной хромосомы
def generate_chromosome(item_count, weights, weight_limit):
    while True:
        chromosome = [random.randint(0, 1) for _ in range(item_count)]
        if sum(chromosome[i] * weights[i] for i in range(item_count)) <= weight_limit:
            return chromosome

# Восстановление решения из хромосомы
def decode_chromosome(chromosome, weights, values, weight_limit):
    total_weight = sum(chromosome[i] * weights[i] for i in range(len(chromosome)))
    total_value = sum(chromosome[i] * values[i] for i in range(len(chromosome)))
    return total_weight, total_value

# Оценочная функция
def fitness(chromosome, weights, values, weight_limit):
    total_weight, total_value = decode_chromosome(chromosome, weights, values, weight_limit)
    if total_weight > weight_limit:
        penalty = total_weight - weight_limit
        return total_value - penalty * 10  # Штраф
    return total_value

# Генерация начальной популяции
def generate_population(pop_size, item_count, weights, weight_limit):
    return [generate_chromosome(item_count, weights, weight_limit) for _ in range(pop_size)]

# Селекция (метод рулетки)
def select(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness <= 0:
        return random.choice(population)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fit in zip(population, fitnesses):
        current += fit
        if current > pick:
            return individual

# Эффективное скрещивание
def crossover(parent1, parent2):
    size = len(parent1)
    point1 = random.randint(1, size - 2)
    point2 = random.randint(point1, size - 1)
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

# Оператор мутации
def mutate(chromosome, mutation_rate):
    return [gene if random.random() > mutation_rate else 1 - gene for gene in chromosome]

# Генетический алгоритм
def genetic_algorithm(weights, values, weight_limit, pop_size=100, generations=100, mutation_rate=0.01):
    item_count = len(weights)
    population = generate_population(pop_size, item_count, weights, weight_limit)

    for _ in range(generations):
        fitnesses = [fitness(ind, weights, values, weight_limit) for ind in population]
        new_population = []
        
        for _ in range(pop_size // 2):
            parent1 = select(population, fitnesses)
            parent2 = select(population, fitnesses)
            offspring1, offspring2 = crossover(parent1, parent2)
            offspring1 = mutate(offspring1, mutation_rate)
            offspring2 = mutate(offspring2, mutation_rate)
            new_population.extend([offspring1, offspring2])
        
        population = new_population

    # Вычисление лучшего решения
    fitnesses = [fitness(ind, weights, values, weight_limit) for ind in population]
    best_index = fitnesses.index(max(fitnesses))
    best_individual = population[best_index]

    return population, fitnesses, best_individual, max(fitnesses)

# Пример использования
num_items = 10  # Количество предметов
max_weight = 50  # Максимальный вес предмета
max_value = 100  # Максимальная ценность предмета

# Генерация случайного графа (весов, ценностей и лимита)
weights, values, weight_limit = generate_random_graph(num_items, max_weight, max_value)

population, fitnesses, best_solution, best_value = genetic_algorithm(weights, values, weight_limit)

# Вывод всех решений
print("Решения последнего поколения:")
for i, (individual, fit) in enumerate(zip(population, fitnesses)):
    print(f"{i + 1}: Хромосома: {individual}, Оценка: {fit}")

# Вывод лучшего решения
print("\nЛучшее решение:")
print(f"Хромосома: {best_solution}, Максимальная полезность: {best_value}")
