import time
from grid import load_grid
from algorithms.greedy import greedy_search
from algorithms.astar import astar_search
from algorithms.genetic import genetic_search

def display_grid(grid, path):
    display = [row[:] for row in grid]
    for (x, y) in path:
        if display[y][x] not in ("S", "G"):
            display[y][x] = "*"
    for row in display:
        print(" ".join(row))

def tester_algo(grid, start, goal, nom, algo):
    debut = time.time()
    chemin = algo(grid, start, goal)
    temps = time.time() - debut
    if chemin:
        print(f"\n[{nom}]  Longueur : {len(chemin)-1} pas  |  Temps : {temps*1000:.2f} ms")
        display_grid(grid, chemin)
    else:
        print(f"\n[{nom}]  Aucun chemin trouvé  |  Temps : {temps*1000:.2f} ms")

print("Choisir une grille")
print("1 - grid1")
print("2 - grid2")
print("3 - grid3")
choix_grille = input("-> ")

grilles = {
    "1": "./grid_datasets/grid1.txt",
    "2": "./grid_datasets/grid2.txt",
    "3": "./grid_datasets/grid3.txt",
}

if choix_grille not in grilles:
    print("Choix invalide.")
else:
    fichier = grilles[choix_grille]
    grid, start, goal = load_grid(fichier)
    print(f"\nGrille {choix_grille} chargée ✓")

    print("\nChoisir un algorithme ")
    print("1 - Glouton")
    print("2 - A*")
    print("3 - Génétique")
    print("4 - Comparer les 3")
    choix_algo = input("→ ")

    algos = {
        "1": ("Glouton",   greedy_search),
        "2": ("A*",        astar_search),
        "3": ("Génétique", genetic_search),
    }

    print("=" * 50)

    if choix_algo in algos:
        nom, algo = algos[choix_algo]
        tester_algo(grid, start, goal, nom, algo)
    elif choix_algo == "4":
        for nom, algo in algos.values():
            tester_algo(grid, start, goal, nom, algo)
    else:
        print("Choix invalide.")
