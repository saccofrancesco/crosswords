# Crossword-Solver
This is a script for getting the Answers to a Crossword Puzzle, using pyTesseract and Web Scraping

## Set Up
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

## How It Works
To run the program, you simply have to run the `main.py` file. You can run it as it is and, by default, it will use one of the six test images in the `/img` folder, specifically the `/img/text1.jpg` image. If you want to use a different image, you can modify the source code here:

![code](img/code.png)

or, you can run the program with one flag, one command-line argument. Specifically, this command, `python main.py <path to your image>`. This will take the image you selected and use it for the analysis.

# Start the Script
Now that you know how to run the program, you can simply do it. **Happy Solving!**