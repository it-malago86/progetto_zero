# File Organizer (Python)

Semplice tool per organizzare file (per tipo o per data).

Prerequisiti
- Linux con Python 3.8+ installato (consigliato 3.11).
- Docker (opzionale, consigliato per esecuzione riproducibile).

Struttura del progetto
- organizer.py       -> logica principale (CLI)
- gui_organizer.py   -> interfaccia grafica opzionale (tkinter)
- config.json        -> regole personalizzate esempio
- requirements.txt   -> dipendenze (opzionali)
- Dockerfile         -> immagine per esecuzione container
- .gitignore, .dockerignore

Uso - sviluppo locale (consigliato)
1. Crea e attiva virtualenv:
   python3 -m venv .venv
   source .venv/bin/activate
2. Installa dipendenze (se presenti):
   pip install -r requirements.txt
3. Esegui in dry-run (non sposta file):
   python organizer.py /percorso/sorgente -t /percorso/target --dry-run
4. Per eseguire l'effettivo spostamento rimuovi --dry-run:
   python organizer.py /percorso/sorgente -t /percorso/target

Uso - Docker (CLI)
1. Build:
   docker build -t file-organizer:latest .
2. Esegui (mappa cartelle host nel container):
   docker run --rm -v "/percorso/host/sorgente:/data" -v "/percorso/host/target:/out" file-organizer:latest /data -t /out --dry-run
3. Eseguire come utente host (evitare file root-owned):
   docker run --rm -u $(id -u):$(id -g) -v "$(pwd)/test_data:/data" -v "$(pwd)/out:/out" file-organizer:latest /data -t /out

Nota GUI
- GUI con tkinter funziona meglio in locale (venv).
- In Docker la GUI richiede X11 forwarding o VNC (più complesso). Per ora usa la GUI localmente.

Contribuire
- Crea branch feature/..., aggiungi test in tests/ e apri PR.
