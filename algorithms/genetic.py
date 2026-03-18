import random
from grid import get_neighbors
from algorithms.greedy import heuristic

# Paramètres globaux
POP = 60 # Nombre de chemins dans la population
GENS = 200 # Nombre de générations maximum

# Génère un chemin aléatoire depuis start
def rand_path(grid, start, goal):
    p = [start]  # Le chemin commence à start
    seen = {start}  # Cases déjà visitées (évite les boucles)
    for _ in range(len(grid) * len(grid[0])):
        # Récupère les voisins accessibles
        voisins = []
        for n in get_neighbors(grid, p[-1][0], p[-1][1]):
            if n not in seen:
                voisins.append(n)
        if not voisins:
            break # Chemin bloqué
        n = random.choice(voisins) # Choisit un voisin au hasard
        p.append(n)
        seen.add(n)
        if n == goal:
            break # Objectif atteint
    return p

# Évalue la qualité d'un chemin
# Plus le score est bas, mieux c'est
def fitness(p, goal):
    longueur = len(p)
    if p[-1] == goal:
        penalite = 0 # Chemin complet, pas de pénalité
    else:
        penalite = heuristic(p[-1], goal) * 3 # Pénalité si goal non atteint
    return longueur + penalite


# Croise deux chemins
def crossover(a, b):
    # Cherche les cases communes entre les deux chemins (sauf le départ)
    commun = []
    for case in a:
        if case in b and case != a[0]:
            commun.append(case)
    if not commun:
        return a[:] # Pas de point de rencontre : retourne a intact
    pt = random.choice(commun) # Choisit un point de rencontre au hasard
    # Début de a + fin de b à partir du point de rencontre
    debut = a[:a.index(pt)]
    fin = b[b.index(pt):]
    return debut + fin

# Mute un chemin : repart aléatoirement depuis un point de bascule
def mutate(p, grid, goal):
    if len(p) < 3:
        return p # Trop court pour muter
    i = random.randint(1, len(p) - 2) # Point de bascule aléatoire
    tail = [p[0]]
    seen = {p[0]}
    # Reconstruit le début jusqu'au point de bascule
    for n in p[1:i]:
        tail.append(n)
        seen.add(n)
    # Repart aléatoirement depuis le point de bascule
    for _ in range(len(grid) * len(grid[0])):
        voisins = []
        for n in get_neighbors(grid, tail[-1][0], tail[-1][1]):
            if n not in seen:
                voisins.append(n)
        if not voisins:
            break # Bloqué
        n = random.choice(voisins)
        tail.append(n)
        seen.add(n)
        if n == goal:
            break # Goal atteint après mutation
    return tail

# Algorithme génétique principal
def genetic_search(grid, start, goal, pop=POP, gens=GENS):
    # Crée la population initiale : pop chemins aléatoires
    pop_list = []
    for _ in range(pop):
        pop_list.append(rand_path(grid, start, goal))
    best = None  # Meilleur chemin trouvé
    for generation in range(gens):
        # Trie la population : les meilleurs chemins en premier
        pop_list.sort(key=lambda p: fitness(p, goal))
        # Cherche si un chemin de cette génération atteint le goal
        for p in pop_list:
            if p[-1] == goal:
                if best is None or len(p) < len(best):
                    best = p[:] # Nouveau meilleur chemin
        # Arrêt anticipé après 30 générations si un chemin est trouvé
        if best and generation > 30:
            break
        # Sélection élitiste
        # Garde le top 20% (les plus performants)
        nb_elite = pop // 5
        elite = pop_list[:nb_elite]
        pop_list = elite[:]

        # Reproduction
        # Remplit la population avec des enfants jusqu'à atteindre pop
        nb_parents = pop // 2
        while len(pop_list) < pop:
            # Choisit 2 parents parmi le top 50%
            parents = random.choices(pop_list[:nb_parents], k=2)
            enfant = crossover(parents[0], parents[1])
            # 30% de chance de muter l'enfant
            if random.random() < 0.3:
                enfant = mutate(enfant, grid, goal)
            pop_list.append(enfant)
    return best  # Retourne le meilleur chemin (ou None si aucun trouvé)