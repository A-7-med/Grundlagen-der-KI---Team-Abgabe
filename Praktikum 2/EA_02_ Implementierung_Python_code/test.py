from ga_basic import genetic_algorithm_basic  # deine GA-Implementierung importieren


# 1) 8-Queens-Problem


def queens_fitness(ind):
    """Weniger Konflikte = bessere Fitness (maximieren)."""
    n = len(ind)
    conflicts = 0
    for c1 in range(n):
        for c2 in range(c1 + 1, n):
            same_row = ind[c1] == ind[c2]
            same_diag = abs(ind[c1] - ind[c2]) == abs(c1 - c2)
            if same_row or same_diag:
                conflicts += 1
    return 1.0 / (1 + conflicts)

def solve_queens(n=8):
    # Gene: erlaubte Zeilenpositionen (1..n)
    gene_pool = list(range(1, n + 1))
    best = genetic_algorithm_basic(
        fitness_fn=queens_fitness,
        gene_pool=gene_pool,
        state_length=n,
        pop_size=60,
        generations=600,
        p_crossover=0.75,
        p_mutation=1.0/n  # Daumenregel: ~1/m
    )
    return best


# 2) Landkarten-Färbeproblem

NEIGHBORS = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D', 'E'],
    'D': ['B', 'C', 'E', 'F'],
    'E': ['C', 'D', 'F'],
    'F': ['D', 'E']
}

REGIONS = list(NEIGHBORS.keys())
COLORS = ['rot', 'grün', 'blau', 'gelb', 'orange']  # Start mit 5 Farben

def map_conflicts(coloring):
    """Zählt, wie viele Nachbarn die gleiche Farbe haben."""
    color_of = {REGIONS[i]: coloring[i] for i in range(len(REGIONS))}
    conflicts = 0
    for r in REGIONS:
        for n in NEIGHBORS[r]:
            if r < n and color_of[r] == color_of[n]:  # vermeidet Doppelzählung
                conflicts += 1
    return conflicts

def map_fitness(ind):
    """Gute Lösungen haben wenige Konflikte und benutzen wenig Farben."""
    conflicts = map_conflicts(ind)
    used_colors = len(set(ind))
    return 1.0 / (1 + conflicts + 0.1 * used_colors)

def solve_map_coloring():
    best = genetic_algorithm_basic(
        fitness_fn=map_fitness,
        gene_pool=COLORS,
        state_length=len(REGIONS),
        pop_size=80,
        generations=800,
        p_crossover=0.75,
        p_mutation=0.05
    )
    return best


# Ausführen

if __name__ == "__main__":
    # 8-Queens
    best_queens = solve_queens(n=8)
    print(" 8-Queens – beste gefundene Lösung:", best_queens)
    print("Konflikte:", int((1 / queens_fitness(best_queens)) - 1))

    # Landkarten-Färben
    best_map = solve_map_coloring()
    print("\n Landkarten-Färben – beste gefundene Lösung:")
    for i, r in enumerate(REGIONS):
        print(f"{r}: {best_map[i]}")
    print("Konflikte:", map_conflicts(best_map))
    print("Verwendete Farben:", len(set(best_map)))
