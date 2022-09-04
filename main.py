try:
    import tkinter as tk #python3

except ImportError:
    import Tkinter as tk #python2
#Pas forcément utile, les distributions python 2 sont obsolètes

try:
    from PIL import Image, ImageTk
    displayImages = True

except ImportError:
    displayImages = False
# Voir code page intro

import sys
import inspect

c = inspect.getfile(lambda: None)[:-7]
# pour eviter des problèmes d'importation on ajoute le chemin des modules
sys.path.append(c+"/modules")
sys.path.append(c+"Autres_jeux")
# Inutile selon moi, après faut voir si t'as des problèmes


import modules.acte1 as act1 
# pour pas confondre avec la classe -> inutile, la classe commence par un A
# majuscule
# importation acte 1
import introduction as intro
# Importe la fenêtre d'intro


class Jeu():
    def __init__(self):
        """ Affichage de la page d'acceuil """
        # il faut affecter photo à self.photo sinon tkinter ne
        # garde pas une reférence


        self.root = tk.Tk()
        self.root.resizable(width=False, height=False)
        self.root.geometry('800x600')
        self.root.title("page d'acceuil")
        
        self.canvas_principal = tk.Canvas(
            self.root, width=750, height=550, bg='ivory')

        if displayImages:
            image = Image.open("Images/acceuil.jpg")
            image = image.resize((750,550))
            photo = self.photo = ImageTk.PhotoImage(image)
            self.canvas_principal.create_image(0,0, anchor = tk.NW, image=photo)

        else:
            self.canvas_principal.create_text(375, 275,
                text= "Impossible de charger les images")
        
        self.canvas_principal.pack()
        
        self.button_start = tk.Button(
            self.root, text="Start",
            command = lambda:[
                self.generate_menu(),
                self.canvas_principal.destroy(),
                self.button_start.destroy()],
            width=12, font = 20, bg = "gray", fg = "white")
        
        self.button_start.pack()

        # bloque la fenetre principale
        self.root.mainloop()

    def generate_menu(self):
        """ Affichage de la fenetre du menu """
        self.root.title("page menu")
        self.root.geometry('300x200')
        label_menu = tk.Label(self.root, text= "Menu", font = 25)
        label_menu.place(relx = 0.42, rely = 0.05)

        button_intro = tk.Button(
            self.root, text = "Lancer l'introduction",
            command = self.generate_intro)
        button_intro.place(relx = 0.3, rely = 0.2)

        button_acte1 = tk.Button(
            self.root, text = "Acte1",
            command = self.generate_acte1)
        
        button_acte1.place(relx = 0, rely = 0.4)
        
        """
        button_acte2 = tk.Button(self.root, text = "Acte2",
                                 command = self.generate_2048)
        button_acte2.place(relx = 0, rely = 0.6)    

        button_acte3 = tk.Button(self.root, text = "Acte3")
        button_acte3.place(relx = 0, rely = 0.8)
        """

    def generate_intro(self):
        self.introWin = intro.Introduction(self.root, self)


    def generate_acte1(self):
        self.acte1_choix = tk.Toplevel()
        self.acte1_choix.geometry('400x300')
        self.acte1_choix.title("Choix acte 1")
        self.acte1_choix.resizable(width=False, height=False)


        self.label_texte_choix0 = tk.Label(
            self.acte1_choix,
            text = "Il est temps de choisir ma destinée:", font = 12)
        
        self.label_texte_choix0.place(relx = 0.23, rely = 0.05)

        button_start = tk.Button(self.acte1_choix, text="Choix A, me venger",
                                 command = lambda:[
                                     self.acte1_choix.destroy(),
                                     creation_acte(0,"A")])
        button_start.place(relx = 0.38, rely = 0.3)

        self.label_texte_choix1 = tk.Label(self.acte1_choix, text = "Ou alors")
        self.label_texte_choix1.place(relx = 0.45, rely = 0.45)

        button_start = tk.Button(self.acte1_choix,
                                 text="choix B, partir enquêter",
                                 command = lambda:[
                                     self.acte1_choix.destroy(),
                                     creation_acte(0,"B")])
        button_start.place(relx = 0.35, rely = 0.6)

        self.acte1_choix.grab_set()

def creation_acte(acte, choix):
    # fonction qui instencie les actes
    acte_actuel = act1.Acte1(choix)

app = Jeu()

