# Crossword-Solver
This is a script for getting the Answers to a Crossword Puzzle, using pyTesseract and Web Scraping

## Set Up
### Build by Yourself
Download the ZIP Folder, or Clone the Repository with:
```
git clone https://github.com/TonicStark/crosswords-solver.git
```

Then install the dependencies in a virtualenv, you can create one via `python -m venv <name of the virtualenv>`, with:
```python
pip install -r requirements.txt
```

Then, you need to install what is called **Tesseract**, a library for text recognition, specifically, **OCR**. You can search it on Github and follow the instructions over their Repo. This is the [link](https://github.com/tesseract-ocr/tesseract).
Then add the Installation Folder to Your **SYSTEM PATH** else, the script **won't work!**. [Here](https://chlee.co/how-to-setup-environment-variables-for-windows-mac-and-linux/) there is a guide.

In the *virtualenv*, run the following command:
```
pyinstaller --onefile --noconsole .\main.py
```
this will **build** the `main.py` file, as a **single** *executable*.
When you finish the build process, you should a *repo* like this:
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
Inside the `dist/` you should have a **file**, `main.exe` which you can **execute** as a single program, without having to *activate* the *virtualenv* each time.

## Download (Windows only)
Else, you can *download* in the **Release** section, the *builded* file.

# Start the Script
Now that you know how to run the program, you can simply do it. **Happy Solving!**