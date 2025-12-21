from api import appliquer_un_coup, créer_une_partie, récupérer_une_partie
from quoridor import Quoridor, interpréter_la_ligne_de_commande
from quoridorx import QuoridorX

JETONS = {
    "viall24": "7e011e28-4b76-45a8-badf-b0b0a6d65545",
}

if __name__ == "__main__":
    args = interpréter_la_ligne_de_commande()
    secret = JETONS[args.idul]

    id_partie, état = créer_une_partie(args.idul, secret)

    quoridor = (
        QuoridorX(état["joueurs"], état["murs"], état["tour"])
        if args.graphique
        else Quoridor(état["joueurs"], état["murs"], état["tour"])
    )

    while True:
        print(quoridor)
        if args.graphique:
            quoridor.afficher()

        if args.automatique:
            try:
                # 1. choisir le coup du joueur
                coup_joueur, position_joueur = quoridor.jouer_un_coup(
                    quoridor.état_partie()["joueurs"][0]["nom"]
                )

                # 2. appliquer le coup du joueur localement
                quoridor.appliquer_un_coup(
                    quoridor.état_partie()["joueurs"][0]["nom"],
                    coup_joueur,
                    position_joueur,
                )

                # 3. envoyer le coup au serveur
                coup_robot, position_robot = appliquer_un_coup(
                    id_partie,
                    coup_joueur,
                    position_joueur,
                    args.idul,
                    secret,
                )

                # 4. appliquer le coup du robot localement
                quoridor.appliquer_un_coup(
                    quoridor.état_partie()["joueurs"][1]["nom"],
                    coup_robot,
                    position_robot,
                )

            except StopIteration as erreur:
                print(quoridor)
                print(f"Le gagnant est {erreur}")
                break

            continue
        
        else:
            coup_joueur, position_joueur = quoridor.sélectionner_un_coup(
                quoridor.état_partie()["joueurs"][0]["nom"]
            )
            coup_joueur, position_joueur = quoridor.appliquer_un_coup(
                quoridor.état_partie()["joueurs"][0]["nom"],
                coup_joueur,
                position_joueur,
            )

        try:
            coup, position = appliquer_un_coup(
                id_partie,
                coup_joueur,
                position_joueur,
                args.idul,
                secret,
            )

            coup, position = quoridor.appliquer_un_coup(
                quoridor.état_partie()["joueurs"][1]["nom"],
                coup,
                position,
            )

        except StopIteration as erreur:
            id_partie, état, gagnant = récupérer_une_partie(
                id_partie,
                args.idul,
                secret,
            )
            quoridor = Quoridor(état["joueurs"], état["murs"], état["tour"])
            print(quoridor)
            print(f"Le gagnant est {erreur}")
            break