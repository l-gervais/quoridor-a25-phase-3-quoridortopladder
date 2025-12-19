import turtle
from quoridor import Quoridor

class QuoridorX(Quoridor):
    def __init__(self, joueurs, murs=None, tour=1):
        super().__init__(joueurs, murs, tour)

        self.screen = turtle.Screen()
        self.screen.title("QuoridorX")
        self.screen.setup(width=600, height=600)
        self.screen.tracer(0)

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

        self.afficher()

    def afficher(self):
        self.pen.clear()
        self.dessiner_grille()
        self.dessiner_murs()
        self.dessiner_pions()
        self.screen.update()

    # --- Coordonnées utilitaires ---
    def to_xy(self, x, y):
        """Convertit une case (1–9, 1–9) en coordonnées turtle."""
        taille = 40
        origine = -4 * taille
        return origine + (x - 1) * taille, origine + (y - 1) * taille

    # --- Damier ---
    def dessiner_grille(self):
        taille = 40
        self.pen.color("black")
        for i in range(10):
            # lignes horizontales
            self.pen.up()
            self.pen.goto(*self.to_xy(1, 1 + i))
            self.pen.down()
            self.pen.forward(9 * taille)

            # lignes verticales
            self.pen.up()
            self.pen.goto(*self.to_xy(1 + i, 1))
            self.pen.setheading(90)
            self.pen.down()
            self.pen.forward(9 * taille)
            self.pen.setheading(0)

    # --- Murs ---
    def dessiner_murs(self):
        taille = 40
        self.pen.color("brown")
        self.pen.width(10)

        # murs horizontaux
        for x, y in self.murs["horizontaux"]:
            x0, y0 = self.to_xy(x, y)
            self.pen.up()
            self.pen.goto(x0, y0 + taille/2)
            self.pen.down()
            self.pen.forward(2 * taille)

        # murs verticaux
        for x, y in self.murs["verticaux"]:
            x0, y0 = self.to_xy(x, y)
            self.pen.up()
            self.pen.goto(x0 - taille/2, y0)
            self.pen.setheading(90)
            self.pen.down()
            self.pen.forward(2 * taille)
            self.pen.setheading(0)

        self.pen.width(1)

    # --- Pions ---
    def dessiner_pions(self):
        couleurs = ["blue", "red"]
        for i, joueur in enumerate(self.joueurs):
            x, y = joueur["position"]
            x0, y0 = self.to_xy(x, y)
            self.pen.up()
            self.pen.goto(x0 + 20, y0 + 20)
            self.pen.dot(30, couleurs[i])