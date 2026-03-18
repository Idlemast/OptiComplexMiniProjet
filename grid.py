
def load_grid(file):
    grid=[]
    start=None
    goal=None

    with open(file) as f:
        for y,line in enumerate(f):
            row=line.strip().split()
            for x,val in enumerate(row):
                if val=="S":
                    start=(x,y)
                if val=="G":
                    goal=(x,y)
            grid.append(row)

    return grid,start,goal


def get_neighbors(grid, x, y):
    # nombre de lignes de la grid
    nb_lignes = len(grid)

    # nombre de colonnes de la grid
    nb_col = len(grid[0])

    # liste qui contiendra les voisins accessibles
    voisins = []
    
    # déplacements possibles : haut, bas, gauche, droite
    for dep_x, dep_y in [(0,-1), (0,1), (-1,0), (1,0)]:
        
        # position de la case voisine
        new_x = x + dep_x
        new_y = y + dep_y
        
        # vérifier que la case reste dans la grid
        if 0 <= new_x < nb_col and 0 <= new_y < nb_lignes:
            
            # vérifier que ce n'est pas un mur
            if grid[new_y][new_x] != "X":
                
                # ajouter la case voisine accessible
                voisins.append((new_x, new_y))
                
    # renvoyer toutes les cases voisines accessibles
    return voisins