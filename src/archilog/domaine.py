import click
import uuid
import datetime

from dataclasses import dataclass
from archilog.datadb import *

@dataclass
class Cagnotte:
    id: uuid.UUID
    nom: str


@dataclass
class Depense:
    id: uuid.UUID
    participant: str
    montant: float
    date: datetime.date
    cagnotte_id: uuid.UUID


@click.group()
def cli():
    init_db()


def creer_cagnotte(nom):
    if any(c.nom == nom for c in lister()):
        raise ValueError(f"La cagnotte '{nom}' existe déjà")
    c = Cagnotte(id=uuid.uuid4(), nom=nom)
    creer(c)
    return c

def supprimer_cagnotte(nom):
    supprimer(nom)


def lister_cagnottes():
    return lister()


def ajouter_depense(cagnotte_id, participant, montant, date):
    if participant_existe(cagnotte_id, participant):
        raise ValueError(f"'{participant}' a déjà une dépense")
    dep = Depense(id=uuid.uuid4(), participant=participant, montant=montant, date=date, cagnotte_id=cagnotte_id)
    ajout_depense(dep)
    return dep


def supprimer_depenses(cagnotte_id, participant):
    if not participant_existe(cagnotte_id, participant):
        raise ValueError(f"Aucune dépense pour '{participant}'")
    supprimer_depense(cagnotte_id, participant)


def lister_depenses(cagnotte_id):
    return get_depense(cagnotte_id)


def calculer_equilibre(cagnotte_id):
    depenses = lister_depenses(cagnotte_id)
    if not depenses:
        return []

    total = sum(d.montant for d in depenses)
    moyenne = total / len(depenses)

    soldes = []
    for d in depenses:
        soldes.append({'nom': d.participant, 'montant': round(d.montant - moyenne, 2)})

    debiteurs  = sorted([s for s in soldes if s['montant'] < 0],  key=lambda x: x['montant'])
    crediteurs = sorted([s for s in soldes if s['montant'] > 0],  key=lambda x: x['montant'], reverse=True)

    resultats = []
    i, j = 0, 0
    while i < len(debiteurs) and j < len(crediteurs):
        a_payer    = abs(debiteurs[i]['montant'])
        a_recevoir = crediteurs[j]['montant']
        transfert  = round(min(a_payer, a_recevoir), 2)

        resultats.append({
            'de':      debiteurs[i]['nom'],
            'vers':    crediteurs[j]['nom'],
            'montant': transfert
        })

        debiteurs[i]['montant']  += transfert
        crediteurs[j]['montant'] -= transfert

        if abs(debiteurs[i]['montant'])  < 0.01: i += 1
        if abs(crediteurs[j]['montant']) < 0.01: j += 1

    return resultats