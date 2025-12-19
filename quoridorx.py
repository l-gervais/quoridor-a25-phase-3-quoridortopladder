import turtle
from quoridor import Quoridor

class QuoridorX(Quoridor):
    def __init__(self, joueurs, murs=None, tour=1):
        super().__init__(joueurs, murs, tour)

        self.screen = turtle.Screen()
        self.screen.title("QuoridorX")

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

        self.afficher()

    def afficher(self):
        self.pen.clear()
        self.dessiner_damier()
        self.dessiner_pions()
        self.screen.update()

    def dessiner_damier(self):
        taille = 30
        self.pen.up()
        self.pen.goto(-135, -135)
        self.pen.down()

        for _ in range(4):
            self.pen.forward(270)
            self.pen.left(90)

    def dessiner_pions(self):
        couleurs = ["blue", "red"]
        for i, joueur in enumerate(self.joueurs):
            x, y = joueur["position"]
            self.pen.up()
            self.pen.goto(-135 + (x-0.5)*30, -135 + (y-0.5)*30)
            self.pen.dot(20, couleurs[i])