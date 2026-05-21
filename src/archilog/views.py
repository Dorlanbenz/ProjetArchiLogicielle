import click

from archilog import *
from archilog.domaine import *

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
            type=click.Choice(["1", "2", "3", "4"])
        )
        if choix == "1":  
            menu_creer_cagnotte()
        elif choix == "2": 
            menu_lister_cagnottes()
        elif choix == "3": 
            menu_supprimer_cagnotte()
        elif choix == "4": 
            click.echo("Au revoir !"); 
            break


def menu_creer_cagnotte():
    while True:
        nom = click.prompt("Nom de la cagnotte à créer")
        try:
            creer_cagnotte(nom)
            click.echo(f"Cagnotte '{nom}' créée")
        except ValueError as e:
            click.echo(f"Erreur : {e}")
            continue
        choix = click.prompt("1 : Créer une autre\n2 : Retour\nVotre choix", type=click.Choice(["1", "2"]))
        if choix == "2": 
            break


def menu_supprimer_cagnotte():
    while True:
        liste = lister_cagnottes()

        if not liste:
            click.echo("Aucune cagnotte à supprimer")
            return
        for ind, c in enumerate(liste, start=1):
            click.echo(f" {ind} --> '{c.nom}'")
        nom = click.prompt("Nom de la cagnotte à supprimer")
        if not any(c.nom == nom for c in liste):
            click.echo(f"'{nom}' introuvable, réessayez")
            continue

        supprimer_cagnotte(nom)

        click.echo(f"Cagnotte '{nom}' supprimée")
        choix = click.prompt("1 : Supprimer une autre\n2 : Retour\nVotre choix", type=click.Choice(["1", "2"]))

        if choix == "2": 
            break


def menu_lister_cagnottes():
    while True:
        liste = lister_cagnottes()
        if not liste:
            click.echo("Aucune cagnotte n'est présente")
            return
        for ind, c in enumerate(liste, start=1):
            click.echo(f" {ind} --> '{c.nom}'")
        choix = click.prompt("1 : Accéder à une cagnotte\n2 : Retour\nVotre choix", type=click.Choice(["1", "2"]))
        if choix == "2": 
            break
        numero = int(click.prompt("Numéro de la cagnotte", type=click.Choice([str(i) for i in range(1, len(liste)+1)])))
        menu_cagnotte(liste[numero - 1])


def menu_cagnotte(cagnotte):
    while True:
        choix = click.prompt(
            f"\nCagnotte '{cagnotte.nom}'\n"
            "1 : Ajouter une dépense\n"
            "2 : Supprimer une dépense\n"
            "3 : Lister les dépenses\n"
            "4 : Retour\nVotre choix",
            type=click.Choice(["1", "2", "3", "4"])
        )
        if choix == "1":   
            menu_ajouter_depense(cagnotte)
        elif choix == "2": 
            menu_supprimer_depense(cagnotte)
        elif choix == "3": 
            menu_lister_depenses(cagnotte)
        elif choix == "4": 
            break


def menu_ajouter_depense(cagnotte):
    while True:
        participant = click.prompt("Nom du participant")
        montant = click.prompt("Montant", type=float)
        date_str = click.prompt("Date (YYYY-MM-DD)")
        date = datetime.date.fromisoformat(date_str)

        try:
            ajouter_depense(cagnotte.id, participant, montant, date)
            click.echo(f"Dépense de '{participant}' ({montant}€) ajoutée")
        except ValueError as e:
            click.echo(f"Erreur : {e}")
        choix = click.prompt("1 : Ajouter une autre\n2 : Retour\nVotre choix", type=click.Choice(["1", "2"]))
        if choix == "2": 
            break


def menu_supprimer_depense(cagnotte):
    while True:
        depenses = lister_depenses(cagnotte.id)
        if not depenses:
            click.echo("Aucune dépense dans cette cagnotte")
            return
        for ind, d in enumerate(depenses, start=1):
            click.echo(f" {ind} → {d.participant} : {d.montant}€ ({d.date})")
        participant = click.prompt("Nom du participant à supprimer")
        try:
            supprimer_depenses(cagnotte.id, participant)
            click.echo(f"Dépense de '{participant}' supprimée")
        except ValueError as e:
            click.echo(f"Erreur : {e}")
            continue
        choix = click.prompt("1 : Supprimer une autre\n2 : Retour\nVotre choix", type=click.Choice(["1", "2"]))
        if choix == "2": 
            break


def menu_lister_depenses(cagnotte):
    depenses = lister_depenses(cagnotte.id)
    if not depenses:
        click.echo("Aucune dépense dans cette cagnotte")
        return
    click.echo(f"\nDépenses de '{cagnotte.nom}' :")
    for ind, d in enumerate(depenses, start=1):
        click.echo(f" {ind} → {d.participant} : {d.montant}€ ({d.date})")
    # bilan
    transactions = calculer_equilibre(cagnotte.id)
    if not transactions:
        click.echo("\nTout le monde est quitte !")
    else:
        click.echo("\n── Qui doit à qui ? ──")
        for t in transactions:
            click.echo(f" {t['de']} doit {t['montant']}€ à {t['vers']}")

    click.prompt("\n1 : Retour", type=click.Choice(["1"]))







