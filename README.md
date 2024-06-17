# Crosswords
[Crosswords](https://crosswords.streamlit.app/) is an app for getting the Answers to a Crossword Puzzle, using pyTesseract and Web Scraping

## Set Up
### Locally
Download the ZIP Folder, or Clone the Repository with:
```
git clone https://github.com/saccofrancesco/crosswords.git
```

Then install the dependencies in a virtualenv, you can create one via `python -m venv <name of the virtualenv>`, with:
```python
pip install -r requirements.txt
```

Then, you need to install what is called **Tesseract**, a library for text recognition, specifically, **OCR**. You can search it on Github and follow the instructions over their Repo. This is the [link](https://github.com/tesseract-ocr/tesseract).
Then add the Installation Folder to Your **SYSTEM PATH** else, the script **won't work!**. [Here](https://chlee.co/how-to-setup-environment-variables-for-windows-mac-and-linux/) there is a guide.

When you are done with this, you can already use the app by simply *activating* your virtualenv and running:
```
streamlit run .\main.py
```
This will start a **local server** on your *computer*, and another one on the *network* (Wi-Fi if you're connected) so that you can *access* from different devices.

## Online
o use this app online, simply visit [crosswords](https://crosswords.streamlit.app/)!

# Start the Script
Now that you know how to run the program, you can simply do it. **Happy Solving!**