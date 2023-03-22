# Crossword Solver
Questo è uno script per ottenere le risposte a un cruciverba, utilizzando pyTesseract e Web Scraping

## Set Up
### Compilare da Te
Scarica la cartella ZIP o clona il repository con:
```
clone di git https://github.com/TonicStark/crosswords-solver.git
```

Quindi installa le dipendenze in un virtualenv, puoi crearne uno tramite `python -m venv <nome del virtualenv>`, con:
```python
pip install -r requisiti.txt
```

Quindi, è necessario installare quello che viene chiamato **Tesseract**, una libreria per il riconoscimento del testo, in particolare, **OCR**. Puoi cercarlo su Github e seguire le istruzioni sul loro Repo. Questo è il [link](https://github.com/tesseract-ocr/tesseract).
Quindi aggiungi la cartella di installazione al tuo **PERCORSO DI SISTEMA** altrimenti lo script **non funzionerà!**. [Qui](https://chlee.co/how-to-setup-environment-variables-for-windows-mac-and-linux/) c'è una guida.

Nel *virtualenv*, esegui il seguente comando:
```
pyinstaller --onefile --noconsole .\main.py
```
questo **compilerà** il file `main.py`, come un **singolo** *eseguibile*.
Quando finisci il processo di compilazione, dovresti avere un *repo* come questo:
```
.
└── crossword-solver/
    ├── build
    ├── dist/
    │   └── main.exe
    ├── README Translation
    ├── venv
    ├── .gitignore
    ├── main.py
    ├── main.spec
    ├── README.md
    └── requirements.txt
```
All'interno di `dist/` dovresti avere un **file**, `main.exe` che puoi **eseguire** come un singolo programma, senza dover *attivare* il *virtualenv* ogni volta.

## Scarica (solo Windows)
Altrimenti, puoi *scaricare* nella sezione **Release**, il file *compilato*.

# Avvia lo script
Ora che sai come eseguire il programma, puoi semplicemente farlo. **Buona soluzione!**