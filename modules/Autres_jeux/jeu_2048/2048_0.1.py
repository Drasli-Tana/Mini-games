a = [
    [0,0,1,0], #[1, 1, 1, 0]
    [1,1,1,1], #[0, 0, 1, 0]
    [1,0,0,1], #[0, 0, 1, 1]
    [1,0,0,0]  #[0, 1, 1, 0]
    ]

def move(table):
    mvt = False
    for i in table:
        #Chaque ligne du tableau
        for j in range(len(i) - 2, -1, -1):
            #les cases 1 à 3 de la ligne (de 0 à 2)
            if i[j] != 0:
                #vérifie si la case spécifiée est vide
                #Sinon, traite la case
                k = j
                if i[k + 1] == 0:
                    mvt = True
                    while k < 3 and i[k + 1] == 0:
                        #Dans le cas ou la case à droite est vide,
                        #décaler la première et mettre l'emplacement
                        #précédent à vide
                        i[k + 1] = i[k]
                        i[k] = 0
                        k += 1
    return mvt

def compress(table):
    for i in table:
        for j in range(len(i) - 1, 0, -1):
            if i[j] != 0:
                if i[j] == i[j - 1]:
                    i[j] *= 2
                    i[j - 1] = 0

def proceed(table):
    move(table)
    compress(table)
    move(table)

def mveRight(table):
    proceed(table)

def mveLeft(table):
    for i in table:
        i = i.reverse()

    proceed(table)

def mveUp(table):
    a = len(table)
    for i in range(a):
        ligne = []
        for j in range(a - 1, -1, -1):
            ligne.append(table[j][i])
        table.append(ligne)

    for i in range(len(table) - 4):
        table.pop(0)

    proceed(table)

    for i in range(a - 1, -1, -1):
        ligne = []
        for j in range(a):
            ligne.append(table[j][i])
        table.append(ligne)

    for i in range(len(table) - 4):
        table.pop(0)

def mveDown(table):
    a = len(table)
    for i in range(a-1, -1,-1):
        ligne = []
        for j in range(a):
            ligne.append(table[j][i])
        table.append(ligne)

    for i in range(len(table) - 4):
        table.pop(0)

    proceed(table)

    for i in range(a):
        ligne = []
        for j in range(a - 1, -1, -1):
            ligne.append(table[j][i])
        table.append(ligne)

    for i in range(len(table) - 4):
        table.pop(0)

