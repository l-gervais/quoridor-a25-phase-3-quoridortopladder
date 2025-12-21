import turtle
from quoridor import Quoridor, QuoridorError


class QuoridorX(Quoridor):
    """Version graphique interactive de Quoridor (turtle)."""

    # ==========================================================
    # CONSTRUCTEUR
    # ==========================================================
    def __init__(self, joueurs, murs=None, tour=1):
        super().__init__(joueurs, murs, tour)

        # fenêtre
        self.screen = turtle.Screen()
        self.screen.title("QuoridorX")
        self.screen.setup(800, 800)
        self.screen.tracer(0)

        # stylo principal
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()

        # stylo messages
        self.msg = turtle.Turtle()
        self.msg.hideturtle()
        self.msg.penup()

        # paramètres graphiques
        self.case = 60
        self.orig_x = -240
        self.orig_y = -240

        # état interaction
        self.coup_prêt = False
        self.position_coup = None
        self.orientation_mur = "MH"
        self.message_erreur = ""

        # événements
        self.screen.onclick(self.clic)
        self.screen.onkey(lambda: self.set_orientation("MH"), "h")
        self.screen.onkey(lambda: self.set_orientation("MV"), "v")
        self.screen.listen()

        self.afficher()

    # ==========================================================
    # AFFICHAGE
    # ==========================================================
    def afficher(self):
        self.pen.clear()
        self.msg.clear()

        self.dessiner_damier()
        self.dessiner_murs()
        self.dessiner_joueurs()
        self.dessiner_legende()
        self.afficher_message()

        self.screen.update()

    def dessiner_damier(self):
        for i in range(10):
            self.pen.goto(self.orig_x + i * self.case, self.orig_y)
            self.pen.pendown()
            self.pen.goto(self.orig_x + i * self.case, self.orig_y + 9 * self.case)
            self.pen.penup()

            self.pen.goto(self.orig_x, self.orig_y + i * self.case)
            self.pen.pendown()
            self.pen.goto(self.orig_x + 9 * self.case, self.orig_y + i * self.case)
            self.pen.penup()

    def dessiner_joueurs(self):
        couleurs = ["blue", "red"]
        for i, j in enumerate(self.joueurs):
            x, y = j["position"]
            px, py = self.coord_case(x, y)
            self.pen.goto(px, py - 15)
            self.pen.color(couleurs[i])
            self.pen.write(str(i + 1), align="center",
                           font=("Arial", 24, "bold"))

    def dessiner_murs(self):
        self.pen.color("brown")
        self.pen.width(4)

        for x, y in self.murs["horizontaux"]:
            px, py = self.coord_case(x, y)
            py -= self.case / 2
            self.pen.goto(px - self.case / 2, py)
            self.pen.pendown()
            self.pen.goto(px + self.case * 1.5, py)
            self.pen.penup()

        for x, y in self.murs["verticaux"]:
            px, py = self.coord_case(x - 1, y)
            px += self.case / 2
            self.pen.goto(px, py - self.case / 2)
            self.pen.pendown()
            self.pen.goto(px, py + self.case * 1.5)
            self.pen.penup()
        self.pen.width(1)

    def dessiner_legende(self):
        self.pen.goto(-360, 260)
        self.pen.color("black")
        self.pen.write(
            f"1 = {self.joueurs[0]['nom']} (murs: {self.joueurs[0]['murs']})\n"
            f"2 = {self.joueurs[1]['nom']} (murs: {self.joueurs[1]['murs']})\n"
            f"Orientation mur : h / v (actuelle: {self.orientation_mur})",
            font=("Arial", 12, "normal")
        )

    def afficher_message(self):
        if self.message_erreur:
            self.msg.goto(-360, -300)
            self.msg.color("red")
            self.msg.write(self.message_erreur,
                           font=("Arial", 12, "bold"))

    # ==========================================================
    # INTERACTION UTILISATEUR
    # ==========================================================
    def set_orientation(self, o):
        self.orientation_mur = o
        self.message_erreur = ""
        self.afficher()

    def clic(self, x, y):
        case_x = round((x - self.orig_x) / self.case + 0.5)
        case_y = round((y - self.orig_y) / self.case + 0.5)

        if 1 <= case_x <= 9 and 1 <= case_y <= 9:
            self.position_coup = [case_x, case_y]
            self.coup_prêt = True

    # ==========================================================
    # MÉTHODE CLÉ : sélection du coup (graphique)
    # ==========================================================
    def sélectionner_un_coup(self, joueur):
        while True:
            self.coup_prêt = False
            self.message_erreur = ""
            self.afficher()

            while not self.coup_prêt:
                self.screen.update()

            # tester sur une COPIE
            état = self.état_partie()
            copie = Quoridor(
                joueurs=état["joueurs"],
                murs=état["murs"],
                tour=état["tour"]
            )

            try:
                copie.appliquer_un_coup(joueur, "D", self.position_coup)
                return "D", self.position_coup

            except QuoridorError:
                try:
                    copie.appliquer_un_coup(
                        joueur,
                        self.orientation_mur,
                        self.position_coup
                    )
                    return self.orientation_mur, self.position_coup

                except QuoridorError as err:
                    # erreur attrapée → affichée → on recommence
                    self.message_erreur = str(err)

    # ==========================================================
    # UTILITAIRE
    # ==========================================================
    def coord_case(self, x, y):
        px = self.orig_x + (x - 1) * self.case + self.case / 2
        py = self.orig_y + (y - 1) * self.case + self.case / 2
        return px, py
