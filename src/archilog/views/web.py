import datetime

from flask import Flask, redirect, render_template, request, url_for

from archilog.datadb import get_cagnotte, init_db
from archilog.domaine import (
    ajouter_depense,
    calculer_equilibre,
    creer_cagnotte,
    lister_cagnottes,
    lister_depenses,
    supprimer_cagnotte,
    supprimer_depenses,
)


app = Flask(__name__)
init_db()

@app.route("/")
def index():
    cagnottes = lister_cagnottes()
    return render_template("index.html", cagnottes=cagnottes)



@app.route("/creer", methods=["POST"])
def creer():
    try:
        creer_cagnotte(request.form["nom_creer"])
    except ValueError as e:
        return render_template(
            "erreur.html",
            message=str(e),
            retour_url=url_for("index"),
            retour_label="← Retour à l'accueil",
        )
    return redirect(url_for("index"))



@app.route("/supprimer", methods=["POST"])
def supprimer():
    try:
        supprimer_cagnotte(request.form["nom_supp"])
    except ValueError as e:
        return render_template(
            "erreur.html",
            message=str(e),
            retour_url=url_for("index"),
            retour_label="← Retour à l'accueil",
        )
    return redirect(url_for("index"))



@app.route("/cagnotte/<cid>")
def detail(cid):
    cagnotte = get_cagnotte(cid)
    depenses = lister_depenses(cid)
    bilan    = calculer_equilibre(cid)
    return render_template(
        "detail.html",
        cagnotte=cagnotte,
        depenses=depenses,
        bilan=bilan,
        today=datetime.date.today().isoformat(),
    )



@app.route("/cagnotte/<cid>/ajouter", methods=["POST"])
def ajouter(cid):
    try:
        ajouter_depense(
            cid,
            request.form["participant"],
            float(request.form["montant"]),
            datetime.date.fromisoformat(request.form["date"]),
        )
    except ValueError as e:
        return render_template(
            "erreur.html",
            message=str(e),
            retour_url=url_for("detail", cid=cid),
            retour_label="← Retour à la cagnotte",
        )
    return redirect(url_for("detail", cid=cid))




@app.route("/cagnotte/<cid>/supprimer-depense", methods=["POST"])
def supprimer_depense_vue(cid):
    try:
        supprimer_depenses(cid, request.form["participant"])
    except ValueError as e:
        return render_template(
            "erreur.html",
            message=str(e),
            retour_url=url_for("detail", cid=cid),
            retour_label="← Retour à la cagnotte",
        )
    return redirect(url_for("detail", cid=cid))
