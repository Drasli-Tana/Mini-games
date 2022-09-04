import tkinter as Tk
import random as Ra
import tkinter.messagebox as Tm

class Grid2048 (Tk.Tk, Tk.Toplevel):
    couleurs = {
        "2": "9bcafa",
        "4": "8c167e",
        "8": "911616",
        "16": "158731",
        "32": "fff700",
        "64": "0062ff",
        "128": "ff0066",
        "256": "4000ff",
        "512": "0000ff",
        "1024": "9b05ff",
        "2048": "530f80"}
    
    def __init__(self, master=None, title = "2048"):
        if master is None:
            super().__init__()
        else:
            Tk.Toplevel.__init__(self, master)

        self.title(title)
        self.objectif = 2048
        
        self.resizable(False, False)
        self.menu = Tk.Menu(self)
        self.config(menu = self.menu)
        #On crée une barre de menus, et on l'assigne à la fenêtre
        
        self.fileMenu = Tk.Menu(self.menu, tearoff = False)
        self.fileMenu.add_command(label = "Reset", command =lambda: self.__reset())
        #On crée la catégorie "Fichier", et on y ajoute un boutton
        #permettant de réinitialiser la grille
        
        self.menu.add_cascade(menu = self.fileMenu, label = "Fichier")
        #On ajoute la catégorie "Fichier" à la barre de menus
        
        self.createCan()
        
        self.__reset()
                        
        self.bind("<Left>", self.left)
        self.bind("<Right>", self.right)
        
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

    def createCan(self):
        """
        Crée un canvas tkinter où seront affichées les tuiles
        """
        self.can = Tk.Canvas(self, width = 402, height = 402, bg = 'ivory')
        self.can.grid(row = 0, column = 0)

        for i in [101, 202, 303]:
            self.addLine(i, 0, i, 404)
            self.addLine(0, i, 404, i)
            
    def addLine(self, startX, startY, endX, endY):
        self.can.create_line(startX, startY, endX, endY)
        
    def couleurAssoc(self, valeur):
        color = "#"
        try: color += Grid2048.couleurs[valeur]
        except IndexError: color+= "000000"
        finally: return color
    
    def completeGrid(self):
        for i in range(len(self.table)):
            #on parcourt chaque ligne
            for j in range(len(self.table[i])):
                if self.table[i][j] != 0:
                    if self.table[i][j] != self.lastGrid[i][j]:
                    #Si la case inspectée est remplie, 
                    #on la colore en correspondance avec sa valeur
                        self.can.create_rectangle(
                            j * 101, i * 101, (j + 1) * 101, (i + 1) * 101 ,
                            fill = self.couleurAssoc(str(self.table[i][j])))
                        
                        self.can.create_text(j * 101 + 51, i * 101 + 51,
                                             text =self.table[i][j],
                                             fill= "black", font = (
                                                 "Consolas", "24"))
                    
                        if self.table[i][j] == self.objectif:
                            #Affiche un message dès que 2048 est atteint
                            Tm.showinfo("2048", "Vous avez gagné")
                            self.ended = True
                        
                else:
                    #Sinon, elle est blanche
                    self.can.create_rectangle(
                        j * 101, i * 101, (j + 1) * 101, (i + 1) * 101 ,
                        fill = "white")
        
        
        #On vérifie si un mouvement est encore possible
        if self.newCell(): Tm.showerror("2048", "Plus de mouvements possibles")
        
        #On sauvegarde l'état de la grille avant le prochain mouvement
        #Ceci est utilisé à des fins d'optimisation
        self.lastGrid = [i.copy() for i in self.table]
        
    
    def setObjective(self, objectif):
        self.objectif = objectif
        
        
    def isEnded(self):
        """
        Est utilisé pour déterminer si le joueur a atteint 2048,
        c'est à dire si la partie est terminée et que le joueur
        a gagné
        """
        return self.ended
    
    def __reset(self):
        self.ended = False
        
        self.table = [[0 for i in range(4)] for j in range(4)]
        self.lastGrid = [i.copy() for i in self.table]

        if Ra.random() > 0.9:
            newCell = 4
        else:
            newCell = 2
        self.table[Ra.randint(0,3)][Ra.randint(0,3)] = newCell
        
        self.completeGrid()
    
    
    def move(self):
        mvt = False
        for i in self.table:
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

    def compress(self, modify = True):
        movable = False
        for i in self.table:
            for j in range(len(i) - 1, 0, -1):
                if i[j] != 0:
                    if i[j] == i[j - 1]:
                        movable = True
                        if modify:
                            i[j] *= 2
                            i[j - 1] = 0
                            
        return movable

    def proceed(self):
        a = self.move()
        b = self.compress()
        c = self.move()
        
        return (a or b or c)
    
    def newCell(self, hasMoved = None):
        empty = []
        for i in range(len(self.table)):
                for j in range(len(self.table[i])):
                    if self.table[i][j] == 0:
                        empty.append((i, j))
        
        Ra.shuffle(empty)
        
        
        if hasMoved:
            self.table[empty[0][0]][empty[0][1]] = Ra.randint(1, 2) * 2
            self.completeGrid()
        
        elif hasMoved is None:
            if empty == []:
                a = not self.compress(False)
                self.mveDown()
                b =  not self.compress(False)
                self.mveUp()

                return (a and b)
        
        else:
            self.completeGrid()
    
    
    """
    Toutes les fonctions utilisées lors de l'appui sur une touche
    Les noms sont explicites
    """
    def right(self, event):
        a = self.proceed()
        
        self.newCell(a)  
        
    def left(self, event):
        self.mveLeft()
        a = self.proceed()
        self.mveLeft()
        
        self.newCell(a)
    
    def up(self, event):
        self.mveUp()
        a = self.proceed()
        self.mveDown()
        
        self.newCell(a)
    
    def down(self, event):
        self.mveDown()
        a = self.proceed()
        self.mveUp()
        
        self.newCell(a)
        
    """
    Modifie (fait "pivoter") le tableau afin d'avoir le même
    traitement pour la compression
    
    Note: les fonctions mvtUp et mvtDown sont opposées
    Pour revenir à l'état précédent l'appel d'une de ces méthodes,
    Il suffit d'appeler l'autre
    """
    def mveLeft(self):
        for i in self.table:
            i = i.reverse()
    
    def mveUp(self):
        a = len(self.table)
        for i in range(a):
            ligne = []
            for j in range(a - 1, -1, -1):
                ligne.append(self.table[j][i])
            self.table.append(ligne)
    
        for i in range(len(self.table) - 4):
            self.table.pop(0)
    
    def mveDown(self):
        a = len(self.table)
        for i in range(a - 1, -1, -1):
            ligne = []
            for j in range(a):
                ligne.append(self.table[j][i])
            self.table.append(ligne)
    
        for i in range(len(self.table) - 4):
            self.table.pop(0)

if __name__ == "__main__":
    Grid2048().mainloop()
