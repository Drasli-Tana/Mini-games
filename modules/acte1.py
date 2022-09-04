import tkinter as tk
import threading
import time

try:
    from PIL import Image, ImageTk
    displayImages = True
except:
    displayImages = False

import modules.Autres_jeux.jeu_2048.latest as jeu1 # importation 2048

import inspect
c_1 = inspect.getfile(lambda: None)[:-16] + "Images/"


class Intervallometre(threading.Thread):

    def __init__(self, duree, fonction, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.duree = duree
        self.fonction = fonction
        self.args = args
        self.kwargs = kwargs
        self.encore = True  # pour permettre l'arret a la demande

    def run(self):
        while self.encore:
            self.timer = threading.Timer(self.duree, self.fonction, self.args, self.kwargs)
            self.timer.setDaemon(True)
            self.timer.start()
            self.timer.join()

    def stop(self):
        self.encore = False  # pour empecher un nouveau lancement de Timer et terminer le thread
        if self.timer.isAlive():
            self.timer.cancel()  # pour terminer une eventuelle attente en cours de Timer

duree = 2

class Acte1:
    def __init__(self, choix):
        if choix == "A":
            self.actu = False
            # variable qui sera utilisé dans changement_acte1A pour la scène
            self.acte1A_etat = 0
            self.etat = self.generate_acte1_A()
            

        elif choix == "B":
            self.actu = False
            self.etat = self.generate_acte1_B()


    def generate_acte1_A(self):
        # dictionnaire qui stockera le texte pour acte 1: A
        self.dict_texte_acte1A = {                     
            "entreprise": "Il fait nuit, c’est enfin le moment parfait pour"  +
                          " frapper un grand coup. Je ne peut rien faire \n"  +
                          "au patron mais demain il aura une grande surprise" +
                          " lorsqu’il découvrira que j’ai saboté leur système"+
                          " informatique.",

            "parking": "Pour être sûr de ne pas me faire remarquer je vais"   +
                       " passer par le parking souterrain. \n Mais attention" +
                       ", je dois faire vite. Si je me souviens bien dans 20" +
                       " minutes le gardien passera par là. ",

            "porte_code": "Voici le premier obstacle : une porte nécessitant" +
                          " un code. Celui-ci a été changé mais grâce à mon " +
                          "badge\nje pourrai avoir des indications ainsi que" +
                          " 8 tentatives pour le craquer.",

            "escalier": "Je peux maintenant emprunter les escaliers pour "    +
                        "monter à l’étage où se situe le bureau du patron.",

            "plan1": "Tiens voici un plan de l’étage. Actuellement je suis au"+
                     "niveau du point bleu et je dois me diriger vers \n le " +
                     "point violet en évitant les caméras en rouges.",

            "plan2": "Je dois vite mémoriser le chemin car il me reste plus " +
                     "beaucoup de temps.",

            "porte_normal1": "Je suis enfin devant la porte du bureau du "    +
                             "patron. Je n’ai pas la clé mais pas de problème"+
                             " je vais crocheter la serrure.",

            "porte_normal2": "Vite appuie le plus vite possible.",
            
            "camera" : "GAME OVER! \nLa caméra vous a repéré",
            
            "bureau": "Super, j’ai réussi à m’introduire dans le bureau du "  +
                      "patron. Je vais récupérer son badge ainsi \n que le "  +
                      "mot de passe puis direction la salle des serveurs.",

            "serveur": "Voici la salle des serveurs. Je vais enfin pouvoir me"+
                       " venger mais avant ça on me demande un mot de passe.",

            "arrestation": "Oh non! La police débarque (en Normandie?!)! ",
            
            "erreur": "Hahaha ! Je voudrais bien voir sa surprise quand il " +
                      "découvrira que tous les serveurs ont crash. ",

            "erreur2": "Bon il est temps de rentrer chez moi avant que "      +
                       "quelqu’un me remarque.",

            "erreur3": "Le lendemain...",

            
            "agent1": "Alors que je rentre dans la voiture de police, un type"+
                      " louche apparait",

            "agent2": "Agent: Je te propose une solution, travaille pour moi" +
                      " et je te ferai sortir de prison",
                      
            
            "tribunal1": "Je ne sais pas comment mais ils m’ont retrouvé, on" +
                         "dirait bien que c’est fini pour moi...",

            "tribunal2": "Le juge m'a finalement donnée une paine de 20 ans..."}
        
        self.imagesNames = self.dict_texte_acte1A.keys()
        # Stocke les clefs du dictionnaire

        if displayImages:
            # chargement image serrure pour le cliqueur
            self.gifSerrure = []
            for i in range(1, 13):
                img = Image.open(c_1 + "serrure_gif/serrure" + str(i) + ".png")
                img = img.resize((600, 450))
                
                self.gifSerrure.append(ImageTk.PhotoImage(img))
            
            # Chargement des plans 
            self.plans = {}
            for i in range(6):
                planIndice = "plan" + str(i)
                img = Image.open(c_1 + "plans/" + planIndice + ".jpg")
                img = img.resize((600,450))
                
                self.plans[planIndice] = ImageTk.PhotoImage(img)
            
            # Chargement de toutes les autres images
            self.images = {}
            for i in self.imagesNames:
                if not ("2" in i or
                        "3" in i):
                    
                    i = i.replace('1', '')
                    img = Image.open(
                        c_1 + i + ".jpg").resize((600, 450))
                    self.images[i] = ImageTk.PhotoImage(img)
            
            self.images["kill"] = ImageTk.PhotoImage(
                Image.open(c_1 + "kill.jpg").resize((200, 300)))
            
            self.images["porte_normale"] = ImageTk.PhotoImage(
                Image.open(c_1 + "porte_normal.jpg").resize((400, 500)))
            
            self.images["arrestation2"] = ImageTk.PhotoImage(
                Image.open(c_1 + "arrestation2.jpg").resize((600, 450)))

        
        self.acte1A = tk.Toplevel()
        self.acte1A.geometry('1100x800')
        self.acte1A.configure(bg = "gray")
        self.acte1A.title("Une vengeance (presque) parfaite")
        self.acte1A.resizable(width=False, height=False)

        self.canvas_acte1A = tk.Canvas(self.acte1A, width=1000,
                                       height=720, bg='ivory')
        self.canvas_acte1A.place(relx = 0.04, rely = 0.04)
        
        
        self.label_texte_acte1A_0 = tk.Label(
            self.acte1A, text = "Tout est perdu, il ne me reste plus qu’à " +
                                "me venger du nouveau patron", font = 30)
        self.label_texte_acte1A_0.place(relx = 0.05, rely = 0.05)
        
        self.updateCanvas("kill")
        
        self.createNextButton()        
        
        self.acte1A.grab_set()

        # actualisation de la fenetre
        if not self.actu:
            self.acte1A.mainloop()
            self.actu = True
    
    def updateCanvas(self, imageName):
        self.img_acte1A_0 = self.canvas_acte1A.create_image(
            100,100, anchor = tk.NW, image = self.images[imageName])

    def changement_acte1A(self, *args):
        """
            methode qui permet de changer le texte et les images lors de
            l'appuie du bouton suivant dans la fenetre acte1 A
        """
        # fenetre game over
        if self.acte1A_etat == -1:
            # ne fait plus rien car fin du jeu
            pass

        elif self.acte1A_etat == 0:
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["entreprise"])
            self.label_texte_acte1A_0.place(relx = 0.05, rely = 0.75)
            
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["entreprise"])
            self.acte1A_etat = 1

        elif self.acte1A_etat == 1:
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["parking"])
            
            self.label_texte_acte1A_0.place(relx = 0.05, rely = 0.75)
            
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["parking"])
            self.acte1A_etat = 2

        elif self.acte1A_etat == 2:
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["porte_code"])
           
            self.label_texte_acte1A_0.place(relx = 0.05, rely = 0.75)
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["porte_code"])
            self.acte1A_etat = 3

        elif self.acte1A_etat == 3:
            # lance un mini jeu: le juste prix
            self.juste_prix_tentatives = 8
            self.generate_juste_prix()

        elif self.acte1A_etat == 4:
            self.label_texte_acte1A_0.config(text = "Bien joué")
            self.acte1A_etat = 5

        elif self.acte1A_etat == 5:
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["escalier"])
            
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["escalier"])
            self.acte1A_etat = 6

        elif self.acte1A_etat == 6:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.plans["plan0"])
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["plan1"])
            self.acte1A_etat = 7

        elif self.acte1A_etat == 7:
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["plan2"])
            self.acte1A_etat = 8

        elif self.acte1A_etat == 8:
            self.label_texte_acte1A_0.config(text = "")
            # lance un mini jeu, trouver le chemin
            self.deleteNextButton()
            
            self.button_acte1A_monter = tk.Button(
                self.acte1A, text = "Monter", font = 26,
                command = self.changement_acte1A)
            self.button_acte1A_monter.place(relx = 0.8, rely = 0.8)
            self.acte1A_etat = 9

        elif self.acte1A_etat == 9:
            self.canvas_acte1A.itemconfigure(
                self.img_acte1A_0, image = self.plans["plan1"])
            
            self.button_acte1A_monter.destroy()
            self.button_acte1A_monter = tk.Button(
                self.acte1A, text = "Monter", font = 26,
                command = self.generate_chemin_game_over)
            self.button_acte1A_monter.place(relx = 0.8, rely = 0.8)

            self.button_acte1A_droite = tk.Button(
                self.acte1A, text = "Droite", font = 26,
                command = self.changement_acte1A)
            self.button_acte1A_droite.place(relx = 0.88, rely = 0.83)
            self.acte1A_etat = 10

        elif self.acte1A_etat == 10:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.plans["plan2"])
            self.button_acte1A_monter.destroy()
            self.button_acte1A_droite.destroy()
            self.button_acte1A_descendre = tk.Button(
                self.acte1A, text = "Descendre", font = 26,
                command = self.changement_acte1A)
            
            self.button_acte1A_descendre.place(relx = 0.8, rely = 0.9)

            self.button_acte1A_droite = tk.Button(
                self.acte1A, text = "Droite", font = 26,
                command = self.generate_chemin_game_over)
            self.button_acte1A_droite.place(relx = 0.88, rely = 0.83)
            self.acte1A_etat = 11

        elif self.acte1A_etat == 11:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.plans["plan3"])
            self.button_acte1A_descendre.destroy()
            self.button_acte1A_droite.destroy()
            self.button_acte1A_descendre = tk.Button(
                self.acte1A, text = "Descendre", font = 26,
                command = self.generate_chemin_game_over)
            
            self.button_acte1A_descendre.place(relx = 0.8, rely = 0.9)

            self.button_acte1A_droite = tk.Button(
                self.acte1A, text = "Droite", font = 26,
                command = self.changement_acte1A)
            
            self.button_acte1A_droite.place(relx = 0.88, rely = 0.83)
            self.acte1A_etat = 12

        elif self.acte1A_etat == 12:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.plans["plan4"])
            self.button_acte1A_descendre.destroy()
            self.button_acte1A_droite.destroy()
            self.button_acte1A_monter = tk.Button(
                self.acte1A, text = "Monter", font = 26,
                command = self.changement_acte1A)
            
            self.button_acte1A_monter.place(relx = 0.8, rely = 0.8)

            self.button_acte1A_droite = tk.Button(
                self.acte1A, text = "Droite", font = 26,
                command = self.generate_chemin_game_over)
            self.button_acte1A_droite.place(relx = 0.88, rely = 0.83)
            self.acte1A_etat = 13

        elif self.acte1A_etat == 13:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.plans["plan5"])
            self.button_acte1A_monter.destroy()
            self.button_acte1A_droite.destroy()
            self.button_acte1A_monter = tk.Button(
                self.acte1A, text = "Monter", font = 26,
                command = self.generate_chemin_game_over)
            self.button_acte1A_monter.place(relx = 0.8, rely = 0.8)

            self.button_acte1A_droite = tk.Button(
                self.acte1A, text = "Droite", font = 26,
                command = self.changement_acte1A)
            self.button_acte1A_droite.place(relx = 0.88, rely = 0.83)
            self.acte1A_etat = 14

        elif self.acte1A_etat == 14:
            self.button_acte1A_monter.destroy()
            self.button_acte1A_droite.destroy()
            self.label_texte_acte1A_0.config(text = "Bien joué!")
            
            self.createNextButton()
            
            self.acte1A_etat = 15

        elif self.acte1A_etat == 15:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["porte_normale"])
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["porte_normal1"])
            self.acte1A_etat = 16

        elif self.acte1A_etat == 16:
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["porte_normal2"])
            self.acte1A_clic = 0
            self.acte1A_etat = 17


        elif self.acte1A_etat == 17:
            self.funcClicId = self.acte1A.bind(
                "<KeyRelease-space>", self.clicker_augmente_clic)
            
            self.button_acte1A_suivant.destroy()
            # mini jeu clicker pour la serrure
            
            # Cette étape est juste la mise en place
            self.canvas_acte1A.itemconfigure(
                self.img_acte1A_0, image = self.gifSerrure[0])
            self.button_acte1A_craquer = tk.Button(
                self.acte1A, text = "craquer la serrure", font = 26,
                command = lambda:[self.clicker_augmente_clic(),
                                  self.changement_acte1A()])
           
            self.button_acte1A_craquer.place(relx = 0.5, rely = 0.8)
            
            self.label_texte_acte1A_0.config(
                text = "Clics: " + str(self.acte1A_clic))
            
            self.acte1A_etat += 1

        elif self.acte1A_etat == 18:            
            try:
                if self.acte1A_clic % 7 == 0:
                    if self.acte1A_clic > 8:
                        raise ValueError()
                    self.acte1A_clic_etat = self.gifSerrure[self.acte1A_clic // 7]
                
                    self.canvas_acte1A.itemconfigure(
                        self.img_acte1A_0, image = self.acte1A_clic_etat)
            
            except:
                self.button_acte1A_craquer.destroy()
                self.acte1A.unbind("<KeyRelease-space>", self.funcClicId)
                del self.funcClicId
                
                self.acte1A_etat += 1
                self.changement_acte1A()
                
                
        elif self.acte1A_etat == 19:
            self.acte1A_etat += 1
            
            self.createNextButton()

        elif self.acte1A_etat == 20:
            self.label_texte_acte1A_0.config(
                text = "Bien joué, la porte est ouverte")
            self.acte1A_etat = 31
        
        
        elif self.acte1A_etat == 31:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["bureau"])
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["bureau"])
            self.acte1A_etat = 32

        elif self.acte1A_etat == 32:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["serveur"])
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["serveur"])
            self.acte1A_etat = 33

        elif self.acte1A_etat == 33:
            # trouver mot de passe
            self.button_acte1A_suivant.destroy()
            self.mot_de_passe = 8192
            self.label_texte_acte1A_0.config(text = "indice c'est une puissance de 2")
            self.etiquette = tk.Label(self.acte1A, text='Mot de passe :')
            self.etiquette.place(relx = 0.22, rely = 0.85)

            self.entree = tk.Entry(self.acte1A, width=50)
            self.entree.place(relx = 0.3, rely = 0.85)
            self.entree.focus_force()

            self.button_teste_code = tk.Button(self.acte1A, text='Tester le code',
                                    command = lambda :[self.tester_code("autre")])
            self.button_teste_code.place(relx = 0.65, rely = 0.75)

            self.button_effacer_code = tk.Button(self.acte1A, text='effacer le code',
                                    command = self.effacer_code)
            self.button_effacer_code.place(relx = 0.65, rely = 0.85)

        elif self.acte1A_etat == 34:
            self.button_teste_code.destroy()
            self.button_effacer_code.destroy()
            self.etiquette.destroy()
            self.entree.destroy()
            self.label_texte_acte1A_0.config(
                text = "Bien jouer, tu t'es infiltré dans le serveur")
            
            self.createNextButton()
            
            self.acte1A_etat = 35

        elif self.acte1A_etat == 35:
            self.label_texte_acte1A_0.config(
                text = "Maintenant il est temps de"+
                       " le faire planter")
            self.compte_a_rebour = Intervallometre(duree, self.tester_fin_jeu)
            self.acte1A_etat = 36

        elif self.acte1A_etat == 36:
            # lancement jeu 2048, score minimum 512 ou 1024, 256 maintenant
            self.button_acte1A_suivant.destroy()
            self.generate_2048(256)

        elif self.acte1A_etat == 37:
            self.label_texte_acte1A_0.config(text = "OVERFLOW Error")
            self.acte1A_etat = 38

        elif self.acte1A_etat == 38:
            self.canvas_acte1A.itemconfigure(
                self.img_acte1A_0, image = self.images["erreur"])
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["erreur"])
            self.acte1A_etat = 39

        elif self.acte1A_etat == 39:
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["erreur2"])
            self.acte1A_etat = 40

        elif self.acte1A_etat == 40:
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["erreur3"])
            self.acte1A_etat = 41

        elif self.acte1A_etat == 41:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["arrestation"])
            self.label_texte_acte1A_0.config(
                text = self.dict_texte_acte1A["arrestation"])
            self.acte1A_etat = 42

        elif self.acte1A_etat == 42:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["arrestation2"])
            self.acte1A_etat = 43

        elif self.acte1A_etat == 43:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["tribunal"])
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["tribunal1"])
            self.acte1A_etat = 44

        elif self.acte1A_etat == 44:
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["tribunal2"])
            self.acte1A_etat = 45

        elif self.acte1A_etat == 45:
            self.canvas_acte1A.itemconfigure(self.img_acte1A_0,
                                             image = self.images["agent"])
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["agent1"])
            self.acte1A_etat = 46

        elif self.acte1A_etat == 46:
            self.label_texte_acte1A_0.config(text = self.dict_texte_acte1A["agent2"])
            self.button_acte1A_suivant.destroy()
            self.corrupt = tk.messagebox.askyesno("Accord", "Accepter l'offre?")

            self.acte1A_etat = 47


        elif self.acte1A_etat == 47:
            # histoie à finir
            pass
        
    
    def createNextButton(self):
        self.button_acte1A_suivant = tk.Button(
            self.acte1A, text = "Suivant", font = 26,
            command = self.changement_acte1A)
        
        self.button_acte1A_suivant.place(relx = 0.8, rely = 0.8)
        
        self.next = self.acte1A.bind("<space>", self.changement_acte1A)
    
    def deleteNextButton(self):
        self.button_acte1A_suivant.destroy()
        
        self.acte1A.unbind("<space>", self.next)
        
    def generate_chemin_game_over(self):
        self.label_texte_acte1A_0.config(
            text = self.dict_texte_acte1A["camera"])
        self.label_texte_acte1A_0.place(relx= 0.35, rely = 0.75)
        
        self.canvas_acte1A.itemconfigure(
            self.img_acte1A_0, image = self.images["camera"])

        # destruction des boutons
        try:
            self.button_acte1A_suivant.destroy()
        except:
            pass

        try:
            self.button_acte1A_monter.destroy()
        except:
            pass

        try:
            self.button_acte1A_droite.destroy()
        except:
            pass

        try:
            self.button_acte1A_descendre.destroy()
        except:
            pass

        try:
            self.button_acte1A_craquer.destroy()
        except:
            pass


    def clicker_augmente_clic(self, *args):
        self.acte1A_clic += 1
        
        self.label_texte_acte1A_0.config(
            text = "Clics :" + str(self.acte1A_clic))
        
        self.changement_acte1A()
        
    
    def generate_2048(self, maxvalue):
        self.jeu_2048 = jeu1.Grid2048(self.acte1A)
        self.jeu_2048.setObjective(maxvalue)
        self.start_thread()

    def jeu_2048_fini(self):
        return self.jeu_2048.isEnded()

    def tester_fin_jeu(self):
        self.etat_2048 = self.jeu_2048_fini()
        print("le jeu 2048 est fini: ", self.etat_2048)
        if self.etat_2048:
            self.jeu_2048.destroy()
            print("error overflow")
            self.stop_thread()
            self.acte1A_etat = 37
            
            self.createNextButton()


    def stop_thread(self):
        self.compte_a_rebour.stop()

    def start_thread(self):
        self.compte_a_rebour.start()
        
        
    def generate_juste_prix(self):
        self.juste_prix_reponse = 42
        self.juste_prix = tk.Toplevel()
        self.juste_prix.geometry('400x300')
        self.acte1A.resizable(width=False, height=False)
        self.juste_prix.title("Trouve le bon code")

        self.juste_prix_texte = tk.Label(self.juste_prix, text = "Il te reste:  "+
                                        str(self.juste_prix_tentatives)+" tentatives")
        self.juste_prix_texte.place(relx=0.1, rely = 0.05)

        self.etiquette = tk.Label(self.juste_prix, text='Mot de passe :')
        self.etiquette.place(relx = 0.05, rely = 0.2)

        self.entree = tk.Entry(self.juste_prix, width=50)
        self.entree.place(relx = 0.4, rely = 0.2)
        self.entree.focus_force()

        self.button_teste_code = tk.Button(self.juste_prix, text='Tester le code',
                                    command = self.tester_code)
        self.button_teste_code.place(relx = 0.25, rely = 0.7)

        self.button_effacer_code = tk.Button(self.juste_prix, text='effacer le code',
                                    command = self.effacer_code)
        self.button_effacer_code.place(relx = 0.25, rely = 0.85)

        self.juste_prix_saisie = self.entree.get()
        
        self.juste_prix.grab_set()

    def tester_code(self, jeu = "juste_prix", *args):
        # en test pour l'instant
        # il faut pouvoir géré les erreurs et exceptions
        if jeu == "juste_prix":
            code = self.juste_prix_reponse
            try:
                reponse = int(self.entree.get())
                

                if code != reponse:
                    self.juste_prix_tentatives -= 1
                    if self.juste_prix_tentatives == 0:
                        self.acte1A_etat = -1 # Game over
                        self.juste_prix.destroy()
                    
                    else:
                        self.juste_prix_texte.config(text = "Il te reste:  "+
                                            str(self.juste_prix_tentatives)+" tentatives")
                else:
                    self.acte1A_etat = 4
                    self.juste_prix.destroy()
            except ValueError:
                pass

        else:
            code = self.mot_de_passe
            try:
                reponse = int(self.entree.get())
            except:
                reponse = None
            
            if code == reponse:
                self.acte1A_etat = 34
                self.changement_acte1A()

    def effacer_code(self, *args):
        self.entree.delete(0, tk.END)


    def generate_acte1_B(self):
        self.acte1B = tk.Toplevel()
        self.acte1B.geometry('800x600')
        self.acte1B.title("Espion en herbe")
        self.acte1B.resizable(width=False, height=False)



        self.acte1B.grab_set()
