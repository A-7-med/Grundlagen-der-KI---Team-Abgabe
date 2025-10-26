import random


# Grundstruktur des Genetischen Algorithmus
def genetic_algorithm_basic(
    fitness_fn,           # Bewertungsfunktion
    gene_pool,            # mögliche Werte für Gene (z. B. [0,1] oder Farben)
    state_length,         # Länge eines Individuums
    pop_size=50,          # Größe der Population
    generations=500,      # Anzahl der Generationen
    p_crossover=0.7,      # Wahrscheinlichkeit für Crossover
    p_mutation=0.01       # Wahrscheinlichkeit für Mutation
):
    """
    Einfache Implementierung des Genetischen Algorithmus.
    Er verwendet Selektion, Crossover und Mutation, um bessere Lösungen zu finden.
    """

    # Startpopulation erzeugen (zufällige Individuen)
    population = [
        [random.choice(gene_pool) for _ in range(state_length)]
        for _ in range(pop_size)
    ]

    # Hilfsfunktionen

    # Fitness-basiertes Auswählen von zwei Eltern (Roulette Wheel)
    def select_parents(population):
        fitness_values = [fitness_fn(ind) for ind in population]
        total = sum(fitness_values)
        if total == 0:
            # Wenn alle gleich schlecht sind, wähle zufällig
            return random.sample(population, 2)
        probs = [f / total for f in fitness_values]
        parents = random.choices(population, weights=probs, k=2)
        return parents

    # Einfache Ein-Punkt-Crossover-Funktion
    def crossover(parent1, parent2):
        if random.random() > p_crossover:
            return parent1[:], parent2[:]
        point = random.randint(1, state_length - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    # Mutation: zufällige Veränderung eines Gens
    def mutate(individual):
        for i in range(state_length):
            if random.random() < p_mutation:
                individual[i] = random.choice(gene_pool)
        return individual

    # Wiederhole über mehrere Generationen
    for gen in range(generations):
        new_population = []

        # Erzeuge Nachkommen bis zur Populationsgröße
        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < pop_size:
                new_population.append(mutate(child2))

        # Neue Generation ersetzt alte
        population = new_population

        # Optional: den besten Fitnesswert pro Generation ausgeben
        if gen % 50 == 0 or gen == generations - 1:
            best = max(population, key=fitness_fn)
            print(f"Generation {gen:3d} | Beste Fitness: {fitness_fn(best):.4f}")

    #Beste gefundene Lösung zurückgeben
    best_solution = max(population, key=fitness_fn)
    return best_solution
