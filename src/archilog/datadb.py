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
    Column("cagnotte_id", Uuid, ForeignKey("cagnotte.id"), nullable=False),
)

def init_db():
    metadata.create_all(engine)

def creer(cagnotte):
    with engine.begin() as conn:
        conn.execute(cagnotte_table.insert().values(
            id=cagnotte.id,
            nom=cagnotte.nom,
        ))


def lister():
    with engine.begin() as conn:
        return conn.execute(cagnotte_table.select()).fetchall()

def supprimer(nom):
    with engine.begin() as conn:
        conn.execute(delete(cagnotte_table).where(nom == cagnotte_table.c.nom)
)