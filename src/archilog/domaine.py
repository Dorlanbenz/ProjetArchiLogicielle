import click
import uuid


from dataclasses import dataclass
from archilog.datadb import *
from archilog.views import *

@dataclass
class Cagnotte:
    id: uuid.UUID
    nom: str


@dataclass
class Depense:
    id: uuid.UUID
    participant: str
    montant: float
    date: str
    cagnotte_id: uuid.UUID


@click.group()
def cli():
    init_db()


def creer_cagnotte():
    while True :
        liste = lister()

        click.echo("Les différentes Cagnottes présentes : ")
        ind = 1
        for item in liste:
            click.echo(f" {ind} --> '{item.nom}'")
            ind += 1

        while True :

            name = click.prompt('Nom de la cagnotte à créer')
            noms = [item.nom for item in liste]

            if name in noms :
                click.echo(f"Le nom de la cagnotte '{name}' est déjà présent, réessayez")
            else:
                break

        cagnotte = Cagnotte(id=uuid.uuid4(), nom=name)
        creer(cagnotte)

        click.echo(f"cagnotte '{cagnotte.nom}' créée")
        choix = click.prompt(
            "1 : Créer une autre cagnotte\n"
            "2 : Retour au menu\n"
            "Votre choix",
            type=click.Choice(["1", "2"])
        )

        if choix == "2":
            break


def supprimer_cagnotte():
    while True:
        liste = lister()

        click.echo("Les différentes Cagnottes présentes : ")
        ind = 1
        for item in liste:
            click.echo(f" {ind} --> '{item.nom}'")
            ind += 1

        if not liste:
            click.echo("Aucune cagnotte à supprimer")
            return

        while True:
            name = click.prompt('Saisir le nom de la cagnotte à supprimer')
            noms = [item.nom for item in liste]
            if name not in noms:
                click.echo(f"Aucune cagnotte '{name}' trouvée, réessayez")
            else:
                break

        supprimer(name)

        click.echo(f"Cagnotte '{name}' supprimée")
        choix = click.prompt(
            "1 : Supprimer une autre cagnotte ?\n"
            "2 : Retour au menu\n"
            "Votre choix",
            type=click.Choice(["1", "2"])
        )
        if choix == "2":
            break  


def lister_cagnottes():
    while True:
        liste = lister()
        if not liste:
            click.echo("Aucune cagnotte n'est présente")
            return

        click.echo("Les différentes Cagnottes : ")
        ind = 1
        for item in liste:
            click.echo(f" {ind} --> '{item.nom}'")
            ind += 1
        choix = click.prompt(
            "1 : Accéder à une cagnotte\n"
            "2 : Retour au menu\n"
            "Votre choix",
            type=click.Choice(["1", "2"])
        )

        if choix == "1":
            numero = click.prompt(
                "Entrez le numéro de la cagnotte à accéder",
                type=click.Choice([str(i) for i in range(1, len(liste) + 1)])
            )

            numero = int(numero)
            cagnotte = liste[numero - 1]
            return cagnotte

        elif choix == "2" :
            break



       
def ajouter_depense(cagnotte):
    pass

def supprimer_depense(cagnotte):
    pass

def lister_depenses(cagnotte):
    pass

