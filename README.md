<div align="center">
  <img src="icon.png" alt="Crosswords App" width="350">
  <h1>Crosswords: Crossword Puzzle Answer Finder</h1>
</div>

<h4 align="center">An app to help you solve crossword puzzles using pyTesseract and Web Scraping built using https://streamlit.io.</h4>

<p align="center">
  <img src="https://img.shields.io/github/contributors/saccofrancesco/crosswords?style=for-the-badge" alt="Contributors">
  <img src="https://img.shields.io/github/forks/saccofrancesco/crosswords?style=for-the-badge" alt="Forks">
  <img src="https://img.shields.io/github/stars/saccofrancesco/crosswords?style=for-the-badge" alt="Stars">
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features of Crosswords

* **Efficient Crossword Solver** – Find answers to crossword puzzles with ease using OCR (Tesseract) and web scraping.
* **Real-Time Answer Generation** – Quickly generates answers based on the clues provided.
* **Simple Interface** – Intuitive UI for seamless interaction and fast crossword solving.
* **Cross-Platform Compatibility** – Works on Windows, macOS, and Linux.

## How To Use Crosswords

### Online
You can simply visit the crosswords app clicking [here](https://crosswords.streamlit.app)!

### Set it up on your machine

Follow these steps to clone and run the Crosswords app on your machine. You'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed, along with [pip](https://pip.pypa.io/en/stable/).

1. Clone this repository:

```bash
$ git clone https://github.com/saccofrancesco/crosswords.git
```

2. Navigate into the repository:

```bash
$ cd crosswords
```

3. Install dependencies:

```bash
$ pip install -r requirements.txt
```

4. Install Tesseract:

Tesseract is required for text recognition (OCR). You can find the installation instructions on the [Tesseract GitHub page](https://github.com/tesseract-ocr/tesseract). After installation, be sure to add the installation folder to your **SYSTEM PATH**.

5. Run the app:

```bash
$ streamlit run .\main.py
```

This will start a **local server** and a **network server**, allowing you to access the app from different devices.

## Credits & Acknowledgements

Crosswords uses the following open-source libraries:

* [Python](https://www.python.org/)
* [pyTesseract](https://github.com/madmaze/pytesseract)
* [Streamlit](https://streamlit.io/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## You Might Also Like...

Explore more projects by the same author:

* [supreme-bot](https://github.com/saccofrancesco/supreme-bot): A bot for buying Supreme items built with [NiceGUI](https://nicegui.io).
* [lock](https://github.com/saccofrancesco/lock): A secure password manager built using [CustomTkinter](https://customtkinter.tomschimansky.com/).

## License

This project is licensed under the Attribution-NonCommercial-ShareAlike 4.0 International License.

---

> GitHub [@saccofrancesco](https://github.com/saccofrancesco)