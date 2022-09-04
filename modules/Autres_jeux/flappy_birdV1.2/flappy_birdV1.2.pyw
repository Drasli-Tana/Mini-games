#voici flappy bird 1.2 il fête l'arrivé de l'easter egg



from tkinter import *
from PIL import Image, ImageTk
from random import randrange



class FlappyEntite:
    """ c'est la classe de Flappy """
    def __init__(self,master):
        self.posX = 155
        self.posY = 175
        self.vitesse = -2
        self.ou = False
        self.compImage = 0
        self.bird1 = Image.open("image/bird1.png")
        self.bird2 = Image.open("image/bird2.png")
        self.bird1Tkinter = ImageTk.PhotoImage(self.bird1,master=master)
        self.bird2Tkinter = ImageTk.PhotoImage(self.bird2,master=master)
        self.photo = ("bird1",self.bird1Tkinter)
    def ressortImage(self):
        return self.photo
    def affectationPos(self,pos):
        self.posX = pos[0]
        self.posY = pos[1]
    def ressortPos(self):
        return (self.posX,self.posY)
    def move(self,gravite=0.35):
        if self.compImage == 20:
            self.photo = ("bird1",self.bird1Tkinter)
        self.compImage += 1
        self.posY += self.vitesse
        self.vitesse += gravite
        if self.vitesse >= 10:
            self.vitesse = 10
        if self.posY < 10:
            self.posY = 10
    def saut(self,event="",vit=-7.5):
        self.photo = ("bird2",self.bird2Tkinter)
        self.compImage = 0
        self.vitesse = vit
    def ressortOu(self):
        return self.ou
    def affectationOu(self,newOu):
        self.ou = newOu

class TuillauxEntites:
    """ c'est une classe tuillaux """
    def __init__(self,master):
        self.posX = []
        self.posTroup = []
        self.ou = []
        self.fqCreateTuillaux = randrange(130,200)
        self.imageTuillaux1 = Image.open("image/Tuillaux1.png")
        self.imageTuillaux2 = Image.open("image/Tuillaux2.png")
        self.photoTuillaux1 = ImageTk.PhotoImage(self.imageTuillaux1,master=master)
        self.photoTuillaux2 = ImageTk.PhotoImage(self.imageTuillaux2,master=master)
    def avancerTuillaux(self,cb,i=0,create=1):
        a = len(self.posX)
        if i < a:
            self.posX[i] -=cb
            if self.posX[i] <= -45:
                self.posX.__delitem__(i)
                self.posTroup.__delitem__(i)
                self.avancerTuillaux(cb,i,create)
            else:
                self.avancerTuillaux(cb,i+1,create)
        else:
            if create == 1:
                self.fqCreateTuillaux -= cb
                if self.fqCreateTuillaux <= 0:
                    self.creerTuillaux()
                    self.fqCreateTuillaux = randrange(130,200)
            else:
                self.fqCreateTuillaux = randrange(130,200)
    def creerTuillaux(self):
        self.posX.append(500)
        self.posTroup.append(randrange(0,350))
    def ressortTuillaux(self):
        return (self.posX,self.posTroup)
    def miseDansOu(self,quoi):
        self.ou = quoi
    def accesAOu(self):
        return self.ou

class EcritoEntite:
    """ c'est la classe des ecritos """
    def __init__(self):
        self.score = 0
        self.highScore = 0
        self.ou = []
    def ressetScore(self):
        self.score = 0
    def ajouterAuScore1(self):
        self.score += 1
        if self.score > self.highScore:
            self.highScore = self.score
    def ressortScore(self):
        return self.score
    def ressortHighScore(self):
        return self.highScore
    def accesAOu(self):
        return self.ou

class FlappyTk(Tk):
    """ c'est la classe principale """
    def __init__(self):
        """ initialisation de la classe """
        Tk.__init__(self)
        self.title("Flappy Bird 1.2")
        self.resizable(False,False)
        self.can = Canvas(self,width=500,height=500)
        self.can.pack()
        self.image = Image.open("image/fond_ecran1.png")
        self.photo = ImageTk.PhotoImage(self.image,master=self)
        self.arrierePlan = self.can.create_image(501,501,image = self.photo,anchor = "se")#self.can.create_rectangle(0,0,500,300,fill = "#aaf"),self.can.create_rectangle(0,300,500,500,fill = "#5a5"))
        self.flappy = FlappyEntite(self)
        self.tuillaux = TuillauxEntites(self)
        self.ecrito = EcritoEntite()
        self.timer = 0
        self.vt = 0.5

        self.enPartie = 0
        self.start("start")
        self.bind("<space>",self.start)

        self.bind("<e>",self.easterEgg)
        self.jeuEnCours()
    def start(self,event=""):
        self.bind("<space>",self.flappy.saut)
        self.vt = 1
        if self.enPartie != -1:
            self.tuillaux.avancerTuillaux(500,0,0)
            self.tuillaux.creerTuillaux()
            self.tuillaux.avancerTuillaux(100,0,0)
        a = self.flappy.ressortPos()
        self.ecrito.ressetScore()
        self.flappy.affectationPos((a[0],175))
        self.flappy.saut()
        if event == "start":
            self.enPartie = -1
        else:
            self.enPartie = 1

    def testTouchTuillaux(self,i=0):
        """ test si flappy touche un des tuillaux """
        a = self.flappy.ressortPos()
        b = self.tuillaux.ressortTuillaux()
        if i < len(b[0]):
            if a[0] > b[0][i]-9 and a[0] < b[0][i]+65:
                if not b[1][i]+6 <= a[1] <= b[1][i]+143:
                    self.enPartie = 0
                    self.bind("<space>",self.start)
                    if a[0] > b[0][i]-9+self.vt:
                        if a[1] <= b[1][i]+6:
                            self.flappy.affectationPos((a[0],b[1][i]+6))
                        elif b[1][i]+143 <= a[1]:
                            self.flappy.affectationPos((a[0],b[1][i]+143))
                elif a[0] >= b[0][i]+65-self.vt and a[0] <= b[0][i]+65:
                    self.ecrito.ajouterAuScore1()
                    self.vt +=0.025
            else:
                self.testTouchTuillaux(i+1)
    def effacerTuillaux(self,i=0):
        """ efface les tuillaux """
        a = len(self.tuillaux.accesAOu())
        if i < a:
            self.can.delete(self.tuillaux.accesAOu()[i])
            self.tuillaux.accesAOu().__delitem__(i)
            self.effacerTuillaux(i)
    def afficherTuillaux(self,i=0):
        """ affiche les tuillaux """
        a = self.tuillaux.ressortTuillaux()
        if i < len(a[0]):
            self.tuillaux.accesAOu().append(self.can.create_image(a[0][i]+60,a[1][i],anchor="se",image=self.tuillaux.photoTuillaux1))
            self.tuillaux.accesAOu().append(self.can.create_image(a[0][i]+60,a[1][i]+150,anchor="ne",image=self.tuillaux.photoTuillaux2))
            self.afficherTuillaux(i+1)
    def afficherFlappy(self):
        """ affiche Flappy """
        self.can.delete(self.flappy.ressortOu())
        a = self.flappy.ressortPos()
        self.flappy.affectationOu(self.can.create_image(a[0],a[1],image = self.flappy.ressortImage()[1]))
        if a[1] >= 500:
            self.enPartie = 0
            self.bind("<space>",self.start)
            self.flappy.affectationPos((a[0],494))
            self.afficherFlappy()
    def effacerEcrito(self,i=0):
        """ efface ecrito """
        a = self.ecrito.accesAOu()
        if i < len(a):
            self.can.delete(a[i])
            a.__delitem__(i)
            self.effacerEcrito(i)
    def afficherEcrito(self):
        """ affiche écrito """
        if self.enPartie != 1:
            self.timer += 1
            if self.timer >= 100:
                self.timer = 0
        else:
            self.timer = 0
        a = self.ecrito.accesAOu()
        a.append(self.can.create_text(475,50,text = str(self.ecrito.ressortScore())+"/" + str(self.ecrito.ressortHighScore()),fill="#f00",font=("helvelita",50),anchor="e"))
        if self.enPartie == -1 and self.timer <= 50:
            a.append(self.can.create_text(250,200,text = "PRESS START",fill="#f00",font=("helvelita",30)))
        elif self.enPartie == 0 and self.timer <= 50:
            a.append(self.can.create_text(250,200,text = "GAME OVER",fill="#f00",font=("helvelita",40)))
            a.append(self.can.create_text(250,250,text = "PRESS START",fill="#f00",font=("helvelita",30)))
    def jeuEnCours(self):
        """ affichage du jeu """
        #part 1 : on modifie le jeu
        if self.enPartie == 1:
            self.flappy.move()
            self.tuillaux.avancerTuillaux(self.vt)
            self.testTouchTuillaux()
        #part 2 : on affiche l'état actuel du jeu
        self.effacerTuillaux()
        self.afficherTuillaux()
        self.afficherFlappy()
        self.effacerEcrito()
        self.afficherEcrito()
        #part 3 : on recomence cette procédure.
        self.after(5,self.jeuEnCours)

    def easterEgg(self,e=""):
        fen = EasterEggTk()


class RaquetteEntite:
    """ceci est la classe des rackettes """
    def __init__(self,posX,posY=200,tailleX=10,tailleY=100,vitesse = 10):
        self.posX = posX
        self.posY = posY
        self.tailleX = tailleX
        self.tailleY = tailleY
        self.vitesse = vitesse
        self.ou = False
    def ressortPos(self):
        return (self.posX,self.posY,self.tailleX,self.tailleY)
    def ressortOu(self):
        return self.ou
    def affectationOu(self,ou):
        self.ou = ou
    def monter(self,vitesse):
        self.posY -= vitesse
        if self.posY <= 20:
            self.posY = 20
    def descendre(self,vitesse):
        self.posY += vitesse
        if self.posY >= 480-self.tailleY:
            self.posY = 480-self.tailleY
class BalleEntite:
    """ ceci esl la classe de ma balle """
    def __init__(self,posX = 300,posY = 250):
        self.posX = posX
        self.posY = posY
        self.direction = (3,0)
        self.ou = False
    def ressortPos(self):
        return (self.posX,self.posY)
    def affectationOu(self,ou):
        self.ou = ou
    def ressortOu(self):
        return self.ou
    def ressortDirection(self):
        return self.direction
    def affectationDirection(self,direction):
        self.direction = direction
    def move(self,raquette1,raquette2):
        a = raquette1.ressortPos()
        b = raquette2.ressortPos()
        self.posX += self.direction[0]
        self.posY += self.direction[1]
        if a[0] <= self.posX <= a[0]+a[2]:
            if a[1]<= self.posY <=a[1]+a[3]:
                self.direction = (-self.direction[0],self.direction[1]+(self.posY-a[1]-50)/20)
        elif b[0] <= self.posX <= b[0]+b[2]:
            if b[1]<= self.posY <=b[1]+b[3]:
                self.direction = (-self.direction[0],self.direction[1]+(self.posY-b[1]-50)/20)
        if self.posY <= 20 or self.posY >= 480:
            self.direction = (self.direction[0],-self.direction[1])
        if self.posX <= 20 or self.posX >= 580:
            self.direction = (0,0)
class EasterEggTk(Tk):
    """ ceci est la classe de l'easterEgg """
    def __init__(self):
        """ ceci est l'initialisation de la classe """
        Tk.__init__(self)
        self.title("pong 1.0")
        self.can = Canvas(self,width=600,heigh=500)
        self.can.pack()
        self.image = Image.open("image/EasterEggFont1.png")
        self.photo = ImageTk.PhotoImage(self.image,master=self)
        self.can.create_image(601,501,anchor="se",image=self.photo)
        self.raquette1 = RaquetteEntite(40)
        self.raquette2 = RaquetteEntite(550)
        self.balle = BalleEntite()

        self.continuerMonter2 = 0
        self.continuerDescendre2 = 0
        self.bind("<KeyPress - Right>",self.monterRaquette2)
        self.bind("<KeyRelease - Right>",self.arreterMonter2)
        self.bind("<KeyPress - Left>",self.descendreRaquette2)
        self.bind("<KeyRelease - Left>",self.arreterDescendre2)
        self.game()
    def monterRaquette2(self,e=""):
        self.continuerMonter2 = 1
    def descendreRaquette2(self,e=""):
        self.continuerDescendre2 = 1
    def arreterMonter2(self,e=""):
        self.continuerMonter2 = 0
    def arreterDescendre2(self,e=""):
        self.continuerDescendre2 = 0

    def bouggerRaquettes(self):
        """ sert a faire bougger les raquetes """
        if self.continuerMonter2 == 1:
            self.raquette2.monter(self.raquette2.vitesse)
        elif self.continuerDescendre2 == 1:
            self.raquette2.descendre(self.raquette2.vitesse)
        a = self.balle.ressortPos()
        if a[1] <= self.raquette1.posY+50:
            self.raquette1.monter(self.raquette1.posY+50-a[1])
        else:
            self.raquette1.descendre(-(self.raquette1.posY+50-a[1]))
    def afficherRaquettes(self):
        """ sert a afficher les raquettes """
        a = self.raquette1.ressortOu()
        b = self.raquette1.ressortPos()
        c = self.raquette2.ressortOu()
        d = self.raquette2.ressortPos()
        self.can.delete(a)
        self.can.delete(c)
        self.raquette1.affectationOu(self.can.create_rectangle(b[0],b[1],b[0]+b[2],b[1]+b[3],fill="#FFF"))
        self.raquette2.affectationOu(self.can.create_rectangle(d[0],d[1],d[0]+d[2],d[1]+d[3],fill="#FFF"))
    def bouggerBalle(self):
        """ sert a faire bougger la balle """
        self.balle.move(self.raquette1,self.raquette2)
    def afficherBalle(self):
        a = self.balle.ressortPos()
        b = self.balle.ressortOu()
        self.can.delete(b)
        self.balle.affectationOu(self.can.create_oval(a[0]+10,a[1]+10,a[0]-10,a[1]-10,fill="#FFFF00"))
    def game(self):
        """ ceci est le jeu """
        self.bouggerRaquettes()
        self.bouggerBalle()
        self.afficherRaquettes()
        self.afficherBalle()
        self.after(10,self.game)



root = FlappyTk()
root.mainloop()





