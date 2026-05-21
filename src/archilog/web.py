import click
import datetime
from flask import *
from archilog.datadb import init_db, get_cagnotte
from archilog.domaine import *

app = Flask(__name__)
init_db()


@app.route("/")
def index():
    cagnottes = lister_cagnottes()
    return f"""
    <h1>Cagnottes</h1>
    <form method="POST" action="/creer">
        <input name="nom_creer" placeholder="Créer cagnotte" required>
        <button>Créer</button>
    </form>
    <br>
    <form method="POST" action="/supprimer">
        <input name="nom_supp" placeholder="Supprimer cagnotte" required>
        <button>supprimer</button>
    </form>
    <ul>
        {''.join(f'<li><a href="/cagnotte/{c.id}">{c.nom}</a></li>' for c in cagnottes)}
    </ul>
    """


@app.route("/creer", methods=["POST"])
def creer():
    try:
        creer_cagnotte(request.form["nom_creer"])
    except ValueError as e:
        return f"{e} <a href='/'> Retour </a>"
    return redirect(url_for("index"))

@app.route("/supprimer", methods=["POST"])
def supprimer():
    try:
        supprimer_cagnotte(request.form["nom_supp"])
    except ValueError as e:
        return f"{e} <a href='/'> Retour </a>"
    return redirect(url_for("index"))


@app.route("/cagnotte/<cid>")
def detail(cid):
    cagnotte  = get_cagnotte(cid)
    depenses  = lister_depenses(cid)
    bilan     = calculer_equilibre(cid)

    lignes = ''.join(f"""
        <tr>
            <td>{d.participant}</td><td>{d.montant}€</td><td>{d.date}</td>
            <td>
                <form method="POST" action="/cagnotte/{cid}/supprimer-depense">
                    <input type="hidden" name="participant" value="{d.participant}">
                    <button>Supprimer</button>
                </form>
            </td>
        </tr>
    """ for d in depenses)

    bilan_html = ''.join(f"<li>{t['de']} doit {t['montant']}€ à {t['vers']}</li>" for t in bilan) or "<li>Tout le monde est quitte !</li>"

    return f"""
    <h1>{cagnotte.nom}</h1>
    <a href="/"> Retour </a>

    <h2>Ajouter une dépense</h2>
    <form method="POST" action="/cagnotte/{cid}/ajouter">
        <input name="participant" placeholder="Participant" required>
        <input name="montant" type="number" placeholder="Montant" required>
        <input name="date" type="date" required>
        <button>Ajouter</button>
    </form>

    <h2>Dépenses</h2>
    <table border="1">
        <tr><th>Participant</th><th>Montant</th><th>Date</th><th></th></tr>
        {lignes or "<tr><td colspan='4'>Aucune dépense</td></tr>"}
    </table>

    <h2>Bilan</h2>
    <ul>{bilan_html}</ul>
    """


@app.route("/cagnotte/<cid>/ajouter", methods=["POST"])
def ajouter(cid):
    try:
        ajouter_depense(
            cid,
            request.form["participant"],
            float(request.form["montant"]),
            datetime.date.fromisoformat(request.form["date"])
        )
    except ValueError as e:
        return f"{e} <a href='/cagnotte/{cid}'>Retour</a>"
    return redirect(url_for("detail", cid=cid))


@app.route("/cagnotte/<cid>/supprimer-depense", methods=["POST"])
def supprimer_depenses(cid):
    try:
        supprimer_depense(cid, request.form["participant"])
    except ValueError as e:
        return f"{e} <a href='/cagnotte/{cid}'>Retour</a>"
    return redirect(url_for("detail", cid=cid))