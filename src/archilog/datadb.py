import uuid
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Date, ForeignKey, Uuid, delete, insert, update



engine = create_engine("sqlite:///data.db", echo=False)
metadata = MetaData()

cagnotte_table = Table(

    "cagnotte", metadata,
    Column("id", Uuid, primary_key=True, default=uuid.uuid4),
    Column("nom", String, nullable=False, unique=True),
    
)

depense_table = Table(

    "depense", metadata,
    Column("id", Uuid, primary_key=True, default=uuid.uuid4),
    Column("participant", String, nullable=False),
    Column("montant", Float, nullable=False),
    Column("date", Date, nullable=False),
    Column("cagnotte_id", Uuid, ForeignKey("cagnotte.id", ondelete="CASCADE"), nullable=False),

)

def init_db():
    metadata.create_all(engine)

def creer(cagnotte):
    with engine.begin() as conn:
        conn.execute(cagnotte_table.insert().values(
            id=cagnotte.id,
            nom=cagnotte.nom
        ))


def lister():
    with engine.begin() as conn:
        return conn.execute(cagnotte_table.select()).fetchall()


def supprimer(nom):
    with engine.begin() as conn:
        conn.execute(delete(cagnotte_table).where(cagnotte_table.c.nom == nom)
)


def ajout_depense(depense):
    with engine.begin() as conn:
        conn.execute(depense_table.insert().values(
            id=depense.id,
            participant=depense.participant,
            montant=depense.montant,
            date=depense.date,
            cagnotte_id=uuid.UUID(str(depense.cagnotte_id))
        
        ))


def supprimer_depense(cagnotte_id, participant):
    with engine.begin() as conn:
        conn.execute(delete(depense_table).where(
            depense_table.c.cagnotte_id == uuid.UUID(str(cagnotte_id)),
            depense_table.c.participant == participant
    ))


def get_depense(cagnotte_id):
    with engine.begin() as conn:
        stmt = depense_table.select().where(depense_table.c.cagnotte_id == uuid.UUID(str(cagnotte_id)))

        return conn.execute(stmt).fetchall()


def participant_existe(cagnotte_id, participant):
    with engine.begin() as conn:

        row = conn.execute(depense_table.select().where(
            depense_table.c.cagnotte_id == uuid.UUID(str(cagnotte_id)),
            depense_table.c.participant == participant
        )).fetchone()

        return row is not None


def get_cagnotte(cagnotte_id):
    with engine.begin() as conn:

        row = conn.execute(cagnotte_table.select().where(
            cagnotte_table.c.id == uuid.UUID(str(cagnotte_id))
        )).fetchone()

        return row