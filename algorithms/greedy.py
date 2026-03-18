from grid import get_neighbors
def heuristic(a,b):
    # a = (x,y) et b = (x,y) 
    #L’heuristique se calcule ici avec la distance de Manhattan entre la position
    #actuelle a  et le point d’arrivée b, en se déplaçant uniquement de haut en bas et de gauche à droite,
    #comme une tour aux échecs.
    # abs(xa - xb) + abs(ya - yb)
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def greedy_search(grid, start, goal):
    # start = (x,y) et goal = (x,y)
    # le chemin commence au point de départ
    path = [start] # [(x,y)]

    # position actuelle : on commence au départ
    current = start
    
    # on fait un ensemble des cases déjà visitées
    deja_visite = set() #initialise
    deja_visite.add(current) #on ajoute l'actuel qui est le départ 

    def distance_heuristique(voisin):
        return heuristic(voisin, goal)
    # on continue tant que l'actuel n'est pas égal à l'objectif (tant que l'objectif n'est pas atteint )
    while current != goal:

        # on récupère les cases voisines accessibles
        voisins = get_neighbors(grid, current[0], current[1]) #current[0] = x et current[1]= y 

        # on garde seulement les voisins qu'on n'a pas encore visités
        voisins_non_visites = [v for v in voisins if v not in deja_visite] # v = (x, y)

        # si aucun voisin disponible, on est bloqué
        if not voisins_non_visites:
            return None

        # on choisit le voisin qui semble le plus proche de l'objectif
        # grâce à la fonction heuristic
        meilleur_voisin = min(voisins_non_visites, key=distance_heuristique)

        # on marque cette case comme visitée
        deja_visite.add(meilleur_voisin)

        # on ajoute cette case au chemin
        path.append(meilleur_voisin)

        # on se déplace vers cette nouvelle position
        current = meilleur_voisin

    # on renvoie le chemin trouvé entre start et goal
    return path