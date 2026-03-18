from grid import get_neighbors
from algorithms.greedy import heuristic
import heapq


def astar_search(grid, start, goal):
    # start = (x,y) et goal = (x,y)
    
    # liste des cases à explorer (file de priorité)
    open_list = []
    # chaque élément : (f = g + heuristique, g = coût depuis le départ, position)
    # heapq transforme la liste en “tas” pour garder l’élément avec la plus petite valeur en haut
    heapq.heappush(open_list, (heuristic(start, goal), 0, start))  

    # dictionnaire pour reconstruire le chemin
    # clé = case actuelle, valeur = case précédente
    came_from = {}

    # coût depuis le départ pour chaque case
    g_score = {start: 0}

    # tant que la liste ouverte n'est pas vide
    while open_list:

        # on récupère la case avec le plus petit f
        f_actuel, g_actuel, current = heapq.heappop(open_list)

        # si on atteint l'objectif, on reconstruit le chemin
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # pour chaque voisin accessible de la case actuelle
        for voisin in get_neighbors(grid, current[0], current[1]):

            # coût pour atteindre ce voisin en passant par la case actuelle
            tentative_g = g_actuel + 1

            # si ce chemin est meilleur que le précédent connu
            if tentative_g < g_score.get(voisin, float("inf")):

                # on enregistre la case actuelle comme "précédente" du voisin
                came_from[voisin] = current

                # on met à jour le meilleur coût pour ce voisin
                g_score[voisin] = tentative_g

                # f = g + heuristique
                f_voisin = tentative_g + heuristic(voisin, goal)

                # on ajoute le voisin à la liste prioritaire
                heapq.heappush(open_list, (f_voisin, tentative_g, voisin))

    # aucun chemin trouvé
    return None