import tkinter as Tk

try:
    from PIL import ImageTk, Image
    displayImages = True
    # Le module étant à installer,
    # il est nécessaire de vérfier
    # que c'est bien le cas

except:
    displayImages = False


class Introduction(Tk.Toplevel):
    # stockera le texte pour l'intro
    tableau_texte_intro = {
        "reveil": "Driiing ! Vous vous réveillez comme chaque matin pour une " +
                  "nouvelle journée.",

        "voiture": "Vous prenez votre voiture et direction vers votre lieu de" +
                   " travail.",

        "travail": " Il est 8h et vous commencez enfin à travailler. Même"     +
                   " chose que d’habitude, trier des dossiers et faire de"     +
                   " nouveaux rapports. \nRien de plus ordinaire en fait."     +
                   " Alors que vous êtes perdu dans vos pensées, le chef "     +
                   "vous appelle.",

        "patron": "Vous arrivez au bureau un peu tendu et nerveux, et"         +
                  "commencez à vous demander si vous allez enfin recevoir\n"   +
                  "votre promotion tant attendue. ",

        "reunion": "Contre toute attente, le patron est en colère et commence" +
                   " à vous crier dessus. Vous ne comprenez pas ce qui se\n"   +
                   "passe et essayez de le calmer. Mais la discussion "        +
                   "s'envenime et vous vous faites virer. ",

        "vire": "Ne comprenant pas encore la situation, vous vous dirigez "    +
                "lentement vers votre bureau et commencez à ranger\nvos "      +
                "affaires. En lisant le document de renvoi, le motif vous "    +
                "interpelle: «coupure budgétaire». Quelle blague! L’entreprise"+
                " est\nen pleine croissance et elle manquerait d’argent?..."   +
                "Vous n’y croyez pas une seule seconde, mais vous n'avez pas " +
                "le choix.\nC’est donc avec regret que vous rentrez chez vous.",

        "one_week_later": "Une semaine plus tard...",

        "canape": "Ça fait une semaine déjà et vous n'en êtes toujours pas "   +
                  "remis. Vous avez passé ces derniers jours allongé sur le\n" +
                  "canapé à manger et dormir. Vous pensez que votre vie n’a "  +
                  "plus aucun sens.",

        "expulsion": "Alors que vous vous lamentez sur votre sort, vous "      +
                     "recevez un préavis d’expulsion vous informant qu’il\nne" +
                     " vous reste que quelques jours pour payer le loyer.\n"   +
                     "Que faire?"
    }
    # Permet d'accéder directement à une clé des deux dictionnaires
    clefs = ["reveil", "voiture", "travail", "patron", "reunion", "vire",
             "one_week_later", "canape", "expulsion"]

    def __init__(self, master, mainWin):
    # chargement des images pour l'intro, si 
        # exécuté en version graphique et module
        # installé
        self.intro_state = 0
        self.mainWin = mainWin
        
        super().__init__(master)
        # Crée la fenêtre graphique.
        # Équivalent à self = Tk.Toplevel(master)

        self.title("Fenêtre d'introduction")
        self.geometry('900x700')
        self.resizable(width=False, height=False)


        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)

        self.label_intro = Tk.Label(self, text = "Introduction")
        self.label_intro.grid(column = 0, row = 0)

        self.canvas_principal_intro = Tk.Canvas(
            self, width=700, height=500, bg='ivory')
        self.canvas_principal_intro.grid(column = 0, row = 1)


        if displayImages:
            self.loadImages()
        
            self.img_intro = self.canvas_principal_intro.create_image(
                0, 0, anchor = Tk.NW, image= self.tableau_image_intro["reveil"]
                )
        
        else:
            self.canvas_principal_intro.create_text(
                350, 250, text = "Impossible de charger les images",
                font = ("Consolas", "20"))

        self.label_texte_intro = Tk.Label(self, text = "")
        self.label_texte_intro.grid(column = 0, row = 2)

        self.button_suivant = Tk.Button(
            self, text = "Suivant",
            command = self.changement_texte_intro)

        self.button_suivant.grid(column = 1, row = 1, padx = 5, pady = 5)

        self.grab_set()

    def loadImages(self):
        """
         chargement des images pour l'intro, si 
         exécuté en version graphique et en ayant
         le module requis installé
        """
        imagesNames = Introduction.tableau_texte_intro.keys()
        # Comme le code a été relativement bien fait,
        # les clefs du texte et des images sont
        # identiques. On peut donc parcourir chacune
        # de ces clefs et associer l'image et le
        # texte.
        self.tableau_image_intro = {}
        
        for i in imagesNames:
            # Oui, c'est une boucle "for"
            img = Image.open("Images/" + i + ".jpg")
            img = img.resize((700, 500))
            
            img = ImageTk.PhotoImage(img)
            
            self.tableau_image_intro[i] = img

    def updateScreen(self, state):
        """
        Cette fonction met à jour le canvas.
        Si un problème est survenu dans l'import
        du module "PIL", Le texte affiché est:
        "Impossible de charger les images"
        """
        self.label_texte_intro.config(
            text =self.tableau_texte_intro[Introduction.clefs[state]])

        if displayImages:
            self.canvas_principal_intro.itemconfigure(
                self.img_intro,
                image=self.tableau_image_intro[Introduction.clefs[state]])


    def changement_texte_intro(self):
        """
            methode qui permet de changer le texte et les images lors de
            l'appuie du bouton suivant dans la fenetre introduction
        """
        if self.intro_state == 9:
            self.mainWin.generate_acte1()
            self.destroy()
        
        else:
            # évite les 7 autres "elif" en cascade
            self.updateScreen(self.intro_state)
            self.intro_state += 1
