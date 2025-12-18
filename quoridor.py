"""Module de la classe Quoridor

Classes:
    * Quoridor - Classe pour encapsuler le jeu Quoridor.
    * interpréter_la_ligne_de_commande - Génère un interpréteur de commande.
"""

import argparse
from copy import deepcopy
import networkx as nx

from quoridor_error import QuoridorError

from graphe import construire_graphe


class Quoridor:
    """Classe pour encapsuler le jeu Quoridor.

    Vous ne devez pas créer d'autre attributs pour votre classe.

    Attributes:
        joueurs (List): Un itérable de deux dictionnaires joueurs
            dont le premier est toujours celui qui débute la partie.
        murs (Dict): Un dictionnaire contenant une clé 'horizontaux' associée à
            la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
            associée à la liste des positions [x, y] des murs verticaux.
        tour (int): Un entier positif représentant le tour du jeu (1 pour le premier tour).
    """

    def __init__(self, joueurs, murs=None, tour=1):
        """Constructeur de la classe Quoridor.

        Initialise une partie de Quoridor avec les joueurs, les murs et le tour spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        Cette méthode ne devrait pas être modifiée.

        Args:
            joueurs (List): un itérable de deux dictionnaires joueurs
                dont le premier est toujours celui qui débute la partie.
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions [x, y] des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions [x, y] des murs verticaux.
            tour (int, optionnel): 
            Un entier positif représentant le tour du jeu (1 pour le premier tour).
        """
        self.tour = tour
        self.joueurs = deepcopy(joueurs)
        self.murs = deepcopy(murs or {"horizontaux": [], "verticaux": []})

    def état_partie(self):
        """Produire l'état actuel du jeu.

        Cette méthode ne doit pas être modifiée.

        Returns:
            Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
                  Notez que les positions doivent être sous forme de liste [x, y] uniquement.
        """
        return deepcopy(
            {
                "tour": self.tour,
                "joueurs": self.joueurs,
                "murs": self.murs,
            }
        )

    def formater_entête(self):
        """Formater la représentation graphique de la légende.

        Returns:
            str: Chaîne de caractères représentant la légende.
        """
        jj = [f'{i+1}={joueur['nom']},' for i, joueur in enumerate(self.joueurs)]
        longueurmax = max(len(p) for p in jj)

        lignes = ['Légende:']
        for i, joueur in enumerate(self.joueurs):
            entete = jj[i]
            espaces = longueurmax - len(entete) + 1
            mursrestants = '|' * int(joueur.get("murs", 0))
            lignes.append(f"   {entete}{' ' * espaces}murs={mursrestants}")

        return '\n'.join(lignes) + '\n'

    def formater_le_damier(self):
        """Formater la représentation graphique du damier.

        Returns:
            str: Chaîne de caractères représentant le damier.
        """
        joueurs = self.joueurs
        murs = self.murs
        positions = {tuple(j["position"]): str(i+1) for i, j in enumerate(joueurs)}
        mh = {tuple(m) for m in murs.get("horizontaux", [])}
        mv = {tuple(m) for m in murs.get("verticaux", [])}

        damier = '   -----------------------------------\n'
        for y in range(9, 0, -1):
            # ligne des cases
            lignesc = f"{y} |"
            for x in range(1, 10):
                point = positions.get((x, y), '.')
                right_wall = ((x + 1, y) in mv) or ((x + 1, y - 1) in mv)
                lignesc += f" {point} |" if right_wall else f" {point}  "
            lignesc = lignesc[:-1] + '|\n'
            damier += lignesc

            if y == 1:
                break

            # ligne des murs horizontaux / séparateurs
            lignesm = "  |"
            for x in range(1, 10):
                left_h = (x - 1, y) in mh
                here_h = (x, y) in mh
                right_v = (x + 1, y - 1) in mv

                if left_h:
                    # when a horizontal wall starts to the left we only add a small spacer or a '|'
                    segment = "|" if right_v else " "
                else:
                    # otherwise either draw the horizontal wall or empty space
                    segment = "-------" if here_h else "   "
                    # if we didn't draw the horizontal wall, append a possible vertical separator
                    if not here_h:
                        segment += "|" if right_v else " "
                lignesm += segment

            lignesm = lignesm[:-1] + '|\n'
            damier += lignesm

        damier += "--|-----------------------------------\n"
        damier += "  | 1   2   3   4   5   6   7   8   9\n"
        return damier

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.

        Cette représentation est la même que celle du projet précédent.

        Returns:
            str: La chaîne de caractères de la représentation.
        """
        return f"{self.formater_entête()}{self.formater_le_damier()}"

    def déplacer_un_joueur(self, joueur, position):
        """Déplace un jeton.

        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        Args:
            joueur (str): le nom du joueur.
            position (List[int, int]): La liste [x, y] de la position du jeton (1<=x<=9 et 1<=y<=9).

        Raises:
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """
        x, y = position
        #verifier si position valide
        if x < 1 or x > 9 or y < 1 or y > 9:
            raise QuoridorError("La position est invalide (en dehors du damier).")

        if joueur == self.joueurs[0]['nom']:
            ind = 0
        else:
            ind = 1

        depart = self.joueurs[ind]['position']
        arrivee = position

        positions = [i['position'] for i in self.joueurs]
        graphe = construire_graphe(positions, self.murs['horizontaux'], self.murs['verticaux'])

        if not graphe.has_edge(tuple(depart), tuple(arrivee)):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")

        self.joueurs[ind]['position'] = [x, y]

    def placer_un_mur(self, joueur, position, orientation):
        """Placer un mur.

        Pour le joueur spécifié, placer un mur à la position spécifiée.

        Args:
            joueur (str): le nom du joueur.
            position (List[int, int]): la liste [x, y] de la position du mur.
            orientation (str): l'orientation du mur ('MH' ou 'MV').

        Raises:
            QuoridorError: Le joueur a déjà placé tous ses murs.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: Vous ne pouvez pas enfermer un joueur.
        """

        #code pour les erreurs:

        x = position[0]
        y = position[1]
        murs = self.murs
        murs_temp = deepcopy(self.murs)

        if joueur == self.joueurs[0]['nom']:
            ind = 0

        else:
            ind = 1

        if self.joueurs[ind]['murs'] == 0: #aucun murs restant
            raise QuoridorError('Le joueur a déjà placé tous ses murs.')

        #toutes les autres erreurs possible sauf enfermement d'un joueur
        if orientation == 'MH':
            if y <= 1 or y > 9 or x < 1 or x >=9:
                raise QuoridorError('La position est invalide (en dehors du damier).')

            if (
                [x+1, y-1] in murs['verticaux']
                or [x+1, y] in murs['horizontaux']
                or [x-1, y] in murs['horizontaux']
                or [x, y] in murs['horizontaux']
                ):
                raise QuoridorError('Un mur occupe déjà cette position.')

        if orientation == 'MV':
            if x <= 1 or x > 9 or y < 1 or y >= 9:
                raise QuoridorError('La position est invalide (en dehors du damier).')

            if (
                [x-1, y+1] in murs['horizontaux']
                or [x, y+1] in murs['verticaux']
                or [x, y-1] in murs['verticaux']
                or [x, y] in murs['verticaux']
                ):
                raise QuoridorError('Un mur occupe déjà cette position.')

        #enfermement d'un joueur

        if orientation == 'MH':
            murs_temp['horizontaux'].append(position)

        else:
            murs_temp['verticaux'].append(position)

        positions = [i['position'] for i in self.joueurs]
        graphe_potentiel = (
            construire_graphe(positions,
            murs_temp['horizontaux'], murs_temp['verticaux'])
            )

        if (
            nx.has_path(graphe_potentiel, tuple(self.joueurs[0]['position']), 'B1') is False
            or
            nx.has_path(graphe_potentiel, tuple(self.joueurs[1]['position']), 'B2') is False
        ):
            raise QuoridorError('Vous ne pouvez pas enfermer un joueur.')

        #placer le mur si valide:

        if orientation == 'MH':
            murs['horizontaux'].append(position)

        else:
            murs['verticaux'].append(position)

        self.joueurs[ind]['murs'] -= 1


    def appliquer_un_coup(self, joueur, coup, position):
        """Appliquer un coup

        Cette méthode permet d'appliquer un coup à l'état actuel du jeu.

        Si le coup appliqué provient du joueur 2, vous devez incrémenter le tour.

        Args:
            joueur (str): le nom du joueur.
            coup (str): Le type de coup
                'D' pour déplacer le jeton
                'MH' pour placer un mur horizontal
                'MV' pour placer un mur vertical
            position (List[int, int]): La liste [x, y] de la position du coup.

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: Le type de coup est invalide.
            QuoridorError: La partie est déjà terminée.

            --- Peuvent être levées par déplacer_un_joueur ou placer_un_mur ---
            QuoridorError: Le joueur a déjà placé tous ses murs.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: Vous ne pouvez pas enfermer un joueur.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        if (
            joueur != self.joueurs[0]['nom']
            and
            joueur != self.joueurs[1]['nom']
            ):
            raise QuoridorError("Le joueur n'existe pas.")

        if coup not in ['D', 'MH', 'MV']:
            raise QuoridorError('Le type de coup est invalide.')

        if self.partie_terminée():
            raise QuoridorError('La partie est déjà terminée.')

        if coup == 'D':
            self.déplacer_un_joueur(joueur, position)

        else:
            self.placer_un_mur(joueur, position, coup)

        if joueur == self.joueurs[1]['nom']:
            self.tour += 1

        return (coup, position)


    def sélectionner_un_coup(self, joueur):
        """Récupérer le coup

        Notez que seul 2 questions devrait être posée à l'utilisateur.

        Notez aussi que cette méthode ne devrait pas modifier l'état du jeu.

        En cas de coup invalide, cette méthode doit afficher le message d'erreur
         et redemander un coup jusqu'à ce qu'un coup valide soit entré.

        Args:
            joueur (str): le nom du joueur.

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        while True:
            try:

                état = self.état_partie()
                copie = Quoridor(joueurs=état['joueurs'], murs=état['murs'], tour=état['tour'])
                coup = input('Quel coup voulez-vous jouer? (D, MH, MV) : ')
                pos_str = input('Donnez la position du coup à jouer (x, y) : ')
                pos_list = pos_str.replace(',', ' ').split()
                pos = [int(pos_list[0]), int(pos_list[1])]

                copie.appliquer_un_coup(joueur, coup, pos)
                break

            except QuoridorError as err:
                print(err)
                continue

        return (coup, pos)

    def partie_terminée(self):
        """Déterminer si la partie est terminée.

        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        #joueur1 gagne
        partie = self.état_partie()
        if partie['joueurs'][0]['position'][1] == 9:
            return partie['joueurs'][0]['nom']

        #joueur2 gagne
        if partie['joueurs'][1]['position'][1] == 1:
            return partie['joueurs'][1]['nom']

        return False

    def jouer_un_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.

        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        Args:
            joueur (str): le nom du joueur.

        Raises:
            QuoridorError: Le joueur n'existe pas.
            QuoridorError: La partie est déjà terminée.

        Returns:
            tuple: Un tuple composé d'un type de coup et de la position.
               Le type de coup est une chaîne de caractères.
               La position est une liste de 2 entier [x, y].
        """
        #verif joueur existe
        if joueur != self.joueurs[0]['nom'] and joueur != self.joueurs[1]['noms']:
            raise QuoridorError("Le joueur n'existe pas.")
        #verif partie terminée
        if self.partie_terminée():
            raise QuoridorError("La partie est déjà terminée.")

        #determiner quel joueur joue
        ind = 0 if joueur == self.joueurs[0]['nom'] else 1

        #construire graphe
        graphe = (
            construire_graphe([self.joueurs[1]['position'], self.joueurs[0]['position']],
            self.murs['horizontaux'], self.murs['verticaux'])
            )

        #identifier la cible
        cible = 'B1' if ind == 0 else 'B2'

        # position de depart
        depart = tuple(self.joueurs[ind]['position'])

        #chemin le plus court
        chemin = nx.shortest_path(graphe, depart, cible)

        #appliquer le deplacement
        self.appliquer_un_coup(joueur, 'D', chemin[1])
        return ('D', chemin[1])


def interpréter_la_ligne_de_commande():
    """Génère un interpréteur de commande.

    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
                   Cette objet aura l'attribut «idul» représentant l'idul du joueur.
    """
    parser = argparse.ArgumentParser(prog="main.py", description="Quoridor")
    parser.add_argument("idul", help="IDUL du joueur")

    # Complétez le code ici
    # vous pourriez aussi avoir à ajouter des arguments dans ArgumentParser(...)

    return parser.parse_args()
