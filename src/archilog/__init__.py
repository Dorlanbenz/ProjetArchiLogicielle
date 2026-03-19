import click
import uuid
import sqlite3

from dataclasses import dataclass
from archilog.datadb import *


@dataclass
class Cagnotte:
    id: uuid.UUID
    nom: str


@click.group()
def cli():
    init_db()



@cli.command()
@click.option("-n", "--name", prompt="Nom de la cagnotte à créer", help="Nom de la cagnotte : ")
def creercagnotte(name: str):
    cagnotte = Cagnotte(id=uuid.uuid4(), nom=name)
    creer(cagnotte)
    click.echo(f"cagnotte '{cagnotte.nom}' créée")


@cli.command()
def listercagnottes():
    liste = lister()
    if not liste:
        click.echo("Aucune cagnotte n'est présente")
    click.echo("Les différentes Cagnottes : ")
    ind = 1
    for item in liste:
        click.echo(f" {ind} : '{item.nom}'")
        ind += 1


@cli.command()
@click.option("-n", "--name", prompt="Nom de la cagnotte à supprimer", help="Nom de la cagnotte à supprimer : ")
def supprimercagnotte(name: str):
    supprimer(name)
    click.echo(f"cagnotte '{name}' supprimée")