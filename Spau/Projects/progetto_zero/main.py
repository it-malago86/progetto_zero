import time
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# Configurazione DATABASE_URL (legge dal docker-compose.yml)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/contatti_db")

# Setup SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modello Database
class ContattoDB(Base):
    __tablename__ = "contatti"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)

# Schema Pydantic (per la validazione dei dati in entrata)
class ContattoSchema(BaseModel):
    nome: str
    email: str

# Funzione di inizializzazione con attesa (Retry logic)
def init_db():
    print("Tentativo di connessione al database...")
    for i in range(10):
        try:
            # Crea le tabelle se non esistono
            Base.metadata.create_all(bind=engine)
            print("Database collegato e tabelle create!")
            return
        except OperationalError:
            print(f"Database non pronto, riprovo tra 3 secondi... ({i+1}/10)")
            time.sleep(3)
    print("Errore: Impossibile connettersi al database.")

init_db()

# Inizializzazione FastAPI
app = FastAPI()

# Montaggio file statici (per index.html e CSS)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse('static/index.html')

@app.post("/aggiungi")
def aggiungi_contatto(contatto: ContattoSchema):
    db = SessionLocal()
    try:
        nuovo = ContattoDB(nome=contatto.nome, email=contatto.email)
        db.add(nuovo)
        db.commit()
        return {"status": "successo"}
    except Exception as e:
        print(f"Errore nel salvataggio: {e}")
        return {"status": "errore"}
    finally:
        db.close()

@app.get("/lista")
def scarica_lista():
    db = SessionLocal()
    contatti = db.query(ContattoDB).all()
    db.close()
    return contatti

