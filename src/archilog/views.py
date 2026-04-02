import click
from archilog import *


@cli.command()
def menu():
    while True:
        choix = click.prompt(
            "\nMenu principal\n"
            "1 : Créer une cagnotte\n"
            "2 : Lister les cagnottes\n"
            "3 : Supprimer une cagnotte\n"
            "4 : Quitter\n"
            "Votre choix",
            type=click.Choice(["1", "2", "3","4"])
        )

        if choix == "1":
            creercagnotte()
        elif choix == "2":
            listercagnottes()
        elif choix == "3":
            supprimercagnotte()
        elif choix == "4":
            click.echo("Au revoir !")
            break