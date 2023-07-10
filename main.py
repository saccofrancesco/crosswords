# Importing Libraries
from bs4 import BeautifulSoup
import pytesseract
import PIL.Image
import requests
import streamlit as st

def solve() -> str:

    # Using Global defined Filepath
    global filepath

    # Dizy Site
    SITE = "https://www.dizy.com"

    # Query URL
    QUERY = "https://www.dizy.com/it/cruciverba/?q="

    # Set Up the Configurations' Options
    CONFIG = r"--psm 6 --oem 3"

    # Converting the Image to Text
    text = pytesseract.image_to_string(PIL.Image.open(filepath.get().split(" ")[2]), config=CONFIG)

    # String Manipulation for Clenaing the Data
    text = text.replace("ORIZZONTALI", "")
    text = text.replace("VERTICALI", "")
    text = text.replace(":", "")
    text = text.replace("-", "")
    text = text.replace("_", "")
    text = text.replace(".", "")
    not_filtered_list = text.split()
    new_text = ""
    for i in range(len(not_filtered_list)):
        if not_filtered_list[i] not in ["", "__", "_", "\n"]:
            if not_filtered_list[i].isdigit() and i != 0 and len(
                    not_filtered_list[i]) not in [3, 4]:
                new_text += "\n"
            new_text += f"{not_filtered_list[i]} "

    # Saving the Uncleared List
    uncleared_clues = new_text.split("\n")

    # Creating the Cleared List
    cleared_clues = []

    # Deleting Numbers
    for i in range(len(uncleared_clues)):
        splitted = uncleared_clues[i].split(" ")
        phrase = " ".join(splitted[1:])
        cleared_clues.append(phrase)

    # Creating the Answers Dictionary
    answers = {}

    # Parsing the Answers
    for i, phrase in enumerate(cleared_clues):
        url = QUERY + phrase
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        if ul := soup.find("ul"):
            href = ul.find("a")
            link = SITE + href["href"]
            source = requests.get(link).text
            soup = BeautifulSoup(source, "html.parser")
            answer = soup.find("b").text
            answers[cleared_clues[i]] = answer

# Main program
if __name__ == "__main__":

    # Modifiyng App name and icon
    st.set_page_config(
        page_title='Crossword Solver',
        page_icon="favicon.ico",
        layout="centered")

    # Title of the Program
    st.title("Crossword Solver")

    # Creating a Camera input to take photos
    image = st.camera_input(".", label_visibility="hidden")