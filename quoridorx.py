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
        self.dessiner_murs()
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

    def dessiner_murs(self):
        taille = 30
        self.pen.color("black")
        self.pen.fillcolor("gray")
        self.pen.up()

        # murs horizontaux
        for x, y in self.murs.get('horizontaux', []):
            # position centrale du mur
            cx = -135 + (x + 0.5) * taille
            cy = -135 + (y - 0.5) * taille
            self.pen.goto(cx - taille, cy - 5)
            self.pen.down()
            self.pen.begin_fill()
            for _ in range(2):
                self.pen.forward(taille*2)
                self.pen.left(90)
                self.pen.forward(10)
                self.pen.left(90)
            self.pen.end_fill()
            self.pen.up()

        # murs verticaux
        for x, y in self.murs.get('verticaux', []):
            cx = -135 + (x - 0.5) * taille
            cy = -135 + (y + 0.5) * taille
            self.pen.goto(cx - 5, cy - taille)
            self.pen.down()
            self.pen.begin_fill()
            for _ in range(2):
                self.pen.forward(10)
                self.pen.left(90)
                self.pen.forward(taille*2)
                self.pen.left(90)
            self.pen.end_fill()
            self.pen.up()