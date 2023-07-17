# Crossword Solver
[Crossword Solver](https://crosswordsolver.streamlit.app/) è un'app per ottenere le risposte a un cruciverba, utilizzando pyTesseract e Web Scraping

## Set Up
### Localmente
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

Quando hai finito, puoi già utilizzare l'app semplicemente *attivando* il tuo virtualenv ed eseguendo:
```
streamlit run .\main.py
```
Questo avvierà un **server locale** sul tuo *computer* e un altro sulla **rete** (Wi-Fi se sei connesso) in modo che tu possa *accedere* da diversi dispositivi.

### Online
Per usare questa app online, visita semplicemente [crossword-solver](https://studymate.streamlit.app/)!

# Avvia lo script
Ora che sai come eseguire il programma, puoi semplicemente farlo. **Buona soluzione!**