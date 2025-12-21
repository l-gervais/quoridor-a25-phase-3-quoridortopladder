import turtle
import networkx as nx
from quoridor import Quoridor, QuoridorError, construire_graphe

class QuoridorX(Quoridor):
    def __init__(self, joueurs, murs=None, tour=1):
        super().__init__(joueurs, murs, tour)

        # Initialisation turtle
        self.screen = turtle.Screen()
        self.screen.title("QuoridorX")
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

        self.taille_case = 30
        self.offset = -135  # pour centrer le damier
        self.orientation_mur = 'H'  # par défaut horizontal
        self.mode_action = 'D'      # par défaut déplacer pion

        # Lancer affichage initial
        self.afficher()

        # Liaison clic souris et touches pour orientation mur
        self.screen.onscreenclick(self.clic_plateau)
        self.screen.onkey(lambda: self.changer_orientation('H'), "MH")
        self.screen.onkey(lambda: self.changer_orientation('V'), "MV")
        self.screen.onkey(lambda: self.changer_mode('D'), "d")  # pour déplacer pion
        self.screen.onkey(lambda: self.changer_mode('M'), "m")  # pour poser mur
        self.screen.listen()

    # ------------------ AFFICHAGE ------------------ #
    def afficher(self):
        self.pen.clear()
        self.dessiner_damier()
        self.dessiner_murs()
        self.dessiner_pions()
        self.screen.update()

    def dessiner_damier(self):
        self.pen.up()
        self.pen.goto(self.offset, self.offset)
        self.pen.down()
        for _ in range(4):
            self.pen.forward(9 * self.taille_case)
            self.pen.left(90)

        # lignes internes
        for i in range(1, 9):
            # horizontales
            self.pen.up()
            self.pen.goto(self.offset, self.offset + i*self.taille_case)
            self.pen.down()
            self.pen.forward(9*self.taille_case)
            # verticales
            self.pen.up()
            self.pen.goto(self.offset + i*self.taille_case, self.offset)
            self.pen.down()
            self.pen.goto(self.offset + i*self.taille_case, self.offset + 9*self.taille_case)

    def dessiner_pions(self):
        couleurs = ["blue", "red"]
        for i, joueur in enumerate(self.joueurs):
            x, y = joueur["position"]
            self.pen.up()
            self.pen.goto(self.offset + (x-0.5)*self.taille_case, self.offset + (y-0.5)*self.taille_case)
            self.pen.dot(self.taille_case*0.6, couleurs[i])

    def dessiner_murs(self):
        self.pen.color("black")
        # murs horizontaux
        for x, y in self.murs['horizontaux']:
            self.pen.up()
            self.pen.goto(self.offset + (x-1)*self.taille_case, self.offset + (y-1)*self.taille_case + self.taille_case/2)
            self.pen.down()
            self.pen.forward(2*self.taille_case)
        # murs verticaux
        for x, y in self.murs['verticaux']:
            self.pen.up()
            self.pen.goto(self.offset + (x-1)*self.taille_case + self.taille_case/2, self.offset + (y-1)*self.taille_case)
            self.pen.down()
            self.pen.goto(self.offset + (x-1)*self.taille_case + self.taille_case/2, self.offset + (y+1)*self.taille_case)

    # ------------------ INTERACTION ------------------ #
    def changer_orientation(self, orientation):
        """Changer l'orientation du mur à placer"""
        self.orientation_mur = orientation
        print(f"Orientation du mur: {orientation}")

    def changer_mode(self, mode):
        """Changer le mode d'action: 'D' pour déplacer, 'M' pour mur"""
        if mode in ['D', 'M']:
            self.mode_action = mode
            print(f"Mode d'action: {'Déplacer pion' if mode=='D' else 'Poser mur'}")

    def clic_plateau(self, x, y):
        """Gestion du clic du joueur"""
        joueur = self.joueurs[0]['nom'] 

        # Conversion du clic en coordonnées de case (1 à 9)
        case_x = int((x - self.offset) // self.taille_case) + 1
        case_y = int((y - self.offset) // self.taille_case) + 1

        # S’assurer que la case est dans le plateau
        case_x = max(1, min(9, case_x))
        case_y = max(1, min(9, case_y))

        try:
            if self.mode_action == 'D':  # déplacement du pion
                self.appliquer_un_coup(joueur, 'D', [case_x, case_y])

            elif self.mode_action == 'M':  # poser un mur
                # Déterminer la position du mur selon l’orientation
                if self.orientation_mur.upper() == 'H':
                    mur_x = max(1, min(8, case_x))  # colonnes 1 à 8 pour murs
                    mur_y = max(2, min(9, case_y))
                    coup_mur = 'MH'
                else:  # vertical
                    mur_x = max(2, min(9, case_x))
                    mur_y = max(1, min(8, case_y))
                    coup_mur = 'MV'

                self.appliquer_un_coup(joueur, coup_mur, [mur_x, mur_y])

            self.afficher()

            # Jouer le tour du bot après le joueur
            self.jouer_tour_bot()

        except QuoridorError as e:
            print(f"Erreur: {e}")

    # BOT #
    def jouer_tour_bot(self):
        if self.partie_terminée():
            print("Partie terminée !")
            return

        bot = self.joueurs[1]['nom']
        try:
            coup, position = self.jouer_un_coup(bot)
            self.appliquer_un_coup(bot, coup, position)
            self.afficher()
        except QuoridorError as err:
            print(f"Erreur bot: {err}")

    #IA#
    def jouer_un_coup(self, joueur):
        ind = 0 if joueur == self.joueurs[0]['nom'] else 1
        positions = [i['position'] for i in self.joueurs]
        graphe = construire_graphe(
            positions,
            self.murs['horizontaux'],
            self.murs['verticaux']
        )
        cible = 'B1' if ind == 0 else 'B2'
        source = tuple(self.joueurs[ind]['position'])
        chemin = nx.shortest_path(graphe, source=source, target=cible)
        prochaine = chemin[1]

        # Vérifier si on peut poser un mur pour bloquer l'adversaire
        adv = self.joueurs[1-ind]['position']
        dist_adv = len(nx.shortest_path(graphe, tuple(adv), 'B1' if ind==1 else 'B2'))
        dist_self = len(chemin)
        if self.joueurs[ind]['murs'] > 0 and dist_adv == 2 and dist_self > 2:
            x, y = adv
            if ind == 0:
                return 'H', [x, y]  # horizontal
            else:
                return 'V', [x, y]  # vertical
        else:
            return 'D', [prochaine[0], prochaine[1]]