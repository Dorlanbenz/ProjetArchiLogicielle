import click
import uuid


from dataclasses import dataclass
from archilog.datadb import *



@dataclass
class Cagnotte:
    id: uuid.UUID
    nom: str


@click.group()
def cli():
    init_db()


def creercagnotte():
    name = click.prompt('Nom de la cagnotte à créer')
    cagnotte = Cagnotte(id=uuid.uuid4(), nom=name)
    creer(cagnotte)
    click.echo(f"cagnotte '{cagnotte.nom}' créée")
    choix = click.prompt(
        "1 : Créer une autre cagnotte\n"
        "2 : Retour au menu\n"
        "Votre choix",
        type=click.Choice(["1", "2"])
    )
    if choix == "1":
        _creer_cagnotte()


def supprimercagnotte():
    while True:
        liste = lister()
        if not liste:
            click.echo("Aucune cagnotte à supprimer")
            return

        while True:
            name = click.prompt('Nom de la cagnotte à supprimer')
            noms = [item.nom for item in liste]
            if name not in noms:
                click.echo(f"Aucune cagnotte '{name}' trouvée, réessayez")
            else:
                break

        supprimer(name)
        click.echo(f"Cagnotte '{name}' supprimée")
        choix = click.prompt(
            "1 : Supprimer une autre cagnotte\n"
            "2 : Retour au menu\n"
            "Votre choix",
            type=click.Choice(["1", "2"])
        )
        if choix == "2":
            break  # retour au menu



def listercagnottes():
    liste = lister()
    if not liste:
        click.echo("Aucune cagnotte n'est présente")
        choix = click.prompt("Que voulez-vous faire? : ",
                type=click.Choice(["créer une cagnotte", "supprimer une cagnotte" ,"quitter"]))

        if choix == "créer une cagnotte":
            _creer_cagnotte()
        elif choix == "supprimer une cagnotte":
            _supprimer_cagnotte()
        return

    click.echo("Les différentes Cagnottes : ")
    ind = 1
    for item in liste:
        click.echo(f" {ind} --> '{item.nom}'")
        ind += 1
    click.prompt(
        "1 : Retour au menu\n"
        "Votre choix",
        type=click.Choice(["1"])
    )


@click.command()
def _creer_cagnotte():
    creercagnotte()


@click.command()
def _supprimer_cagnotte():
    supprimercagnotte()


@cli.command()
def _lister_cagnottes():
    listercagnottes()

import archilog.views

