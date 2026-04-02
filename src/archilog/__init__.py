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
    liste = lister()
    if not liste:
        click.echo("Aucune cagnotte à supprimer")
        return

    name = click.prompt('Nom de la cagnotte à supprimer')
    supprimer(name)
    click.echo(f"cagnotte '{name}' supprimée")
    choix = click.prompt(
        "1 : supprimer une autre cagnotte\n"
        "2 : Retour au menu\n"
        "Votre choix",
        type=click.Choice(["1", "2"])
    )
    if choix == "1":
        _supprimer_cagnotte()



def listercagnottes():
    liste = lister()
    if not liste:
        click.echo("Aucune cagnotte n'est présente")
        choix = click.prompt("Que voulez-vous faire? : ",
                type=click.Choice(["créer une cagnotte", "supprimer une cagnotte" ,"quitter"]))

        if choix == "créer une cagnotte":
            creercagnotte()
        elif choix == "supprimer une cagnotte":
            supprimercagnotte()
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

