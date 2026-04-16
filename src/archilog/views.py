import click

from archilog import *
from archilog.domaine import *

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@cli.command()
def menu():
    while True:
        choix = click.prompt(
            "\nMenu principal\n"
            "1 : Créer une cagnotte\n"
            "2 : Accéder aux cagnottes\n"
            "3 : Supprimer une cagnotte\n"
            "4 : Quitter\n"
            "Votre choix",
            type=click.Choice(["1", "2", "3","4"])
        )

        if choix == "1":
            creer_cagnotte()
        elif choix == "2":
            liste_cagnotte_view()
        elif choix == "3":
            supprimer_cagnotte()
        elif choix == "4":
            click.echo("Au revoir !")
            break




def menu_cagnotte(cagnotte):
    while True:
        choix = click.prompt(
            f"\nCagnotte '{cagnotte.nom}'\n"
            "1 : Ajouter une dépense\n"
            "2 : Supprimer une dépense\n"
            "3 : Lister les dépenses\n"
            "4 : Retour à la liste des cagnottes\n"
            "Votre choix",
            type=click.Choice(["1", "2", "3", "4"])
        )

        if choix == "1":
            ajouter_depense(cagnotte)
        elif choix == "2":
            supprimer_depense(cagnotte)
        elif choix == "3":
            lister_depenses(cagnotte)
        elif choix == "4":
            break

def liste_cagnotte_view():
    cagnotte = lister_cagnottes()  
    if cagnotte:                   
        menu_cagnotte(cagnotte)


