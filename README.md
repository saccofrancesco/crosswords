<div align="center">
  <img src="icon.png" alt="Crosswords App" width="350">
  <h1>🧩 Crosswords: Crossword Puzzle Answer Finder</h1>
</div>

<div align="center">
  <a href="https://www.buymeacoffee.com/YOUR_USERNAME">
    <img src="https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=☕&slug=saccofrancesco&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" />
  </a>
</div>

<h4 align="center">A fast and intuitive crossword solver powered by <a href="https://platform.openai.com/docs/overview" target="_blank">OpenAI</a> and web scraping — built with <a href="https://streamlit.io" target="_blank">Streamlit</a>.</h4>

<p align="center">
  <img src="https://img.shields.io/github/contributors/saccofrancesco/crosswords?style=for-the-badge" alt="Contributors">
  <img src="https://img.shields.io/github/forks/saccofrancesco/crosswords?style=for-the-badge" alt="Forks">
  <img src="https://img.shields.io/github/stars/saccofrancesco/crosswords?style=for-the-badge" alt="Stars">
</p>

<p align="center">
  <a href="#tldr">TL;DR</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

---

## 📌 TL;DR
**Crosswords** helps you solve puzzles by recognizing text with ChatGPT OCR and scraping answer databases.  
It runs locally or online via Streamlit — fast, lightweight, and cross-platform.

👉 Try it online: [crosswords.streamlit.app](https://crosswords.streamlit.app)

---

## 🔑 Key Features

- **AI-Powered Clue Recognition** – Uses ChatGPT’s image model to read and structure crossword clues from screenshots or scans
- **Efficient Solver** – Web scraping + AI clue parsing finds answers fast
- **Real-Time Generation** – Instant suggestions from your clues
- **Simple UI** – Clean Streamlit interface
- **Cross-Platform** – Runs on Windows, macOS, and Linux

---

## ⚡ Quickstart

You’ll need [Git](https://git-scm.com/), [Python](https://www.python.org/downloads/), and [pip](https://pip.pypa.io/en/stable/).

```bash
# Clone this repository
git clone https://github.com/saccofrancesco/crosswords.git
cd crosswords

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
```

This will start a **local server** (for your device) and a **network server** (accessible across devices on your network).

---

## 🖼️ How It Works: Clue Recognition with ChatGPT Vision

1. Upload or paste a screenshot/photo of your crossword puzzle.
2. ChatGPT’s image model automatically **detects and extracts the clues** (e.g., “12 Across: Capital of Norway (4)”).
3. The app structures them into JSON format for easy processing:

```json
[
  { "number": "12", "direction": "Across", "clue": "Capital of Norway", "length": 4 },
  { "number": "7", "direction": "Down", "clue": "Opposite of cold", "length": 3 }
]
```

1. The solver uses these parsed clues to query answer databases and return suggestions.

No more messy OCR post-processing — just **clean, structured clues straight from the puzzle image**.

---

## 🧠 Credits & Acknowledgements

Crosswords uses these great tools:

* [Python](https://www.python.org/)
* [ChatGPT](https://platform.openai.com/docs/overview)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Streamlit](https://streamlit.io/)

---

## 📎 You Might Also Like...

Explore more by the same author:

* [SupremeBot](https://github.com/saccofrancesco/supreme-bot): A Supreme shopping bot built with [NiceGUI](https://nicegui.io).
* [Lock](https://github.com/saccofrancesco/lock): A secure local password manager built with [CustomTkinter](https://customtkinter.tomschimansky.com/).

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) — feel free to use it in your own projects!

---

> GitHub [@saccofrancesco](https://github.com/saccofrancesco)