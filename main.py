# Importing Libraries
from bs4 import BeautifulSoup
import pytesseract
import PIL.Image
import requests
import streamlit as st
import math

# Set Up the Configurations' Options
CONFIG = r"--psm 6 --oem 3"

# Dizy Site
SITE = "https://www.dizy.com"

# Query URL
QUERY = "https://www.dizy.com/it/cruciverba/?q="

# Transform and analyze the image to extract text
def img_to_text(image: bytes) -> str:

    return pytesseract.image_to_string(PIL.Image.open(image), config=CONFIG)

# Function for cleaning data and splitting the clues
def clean_and_split_clues(text: str) -> list:

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

    return cleared_clues

# Solve the clues scraping on the clues site, pairing the answers
def solve_clues(clues: list, bar) -> dict:

    # Creating the Answers Dictionary
    answers = {}

    # Var for the progress bar
    increment = 0
    add = 100 // math.ceil(len(clues))

    # Parsing the Answers
    for i, phrase in enumerate(clues):
        increment += add
        bar.progress(increment, "Resolving Clues...")
        url = QUERY + phrase
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        if ul := soup.find("ul"):
            href = ul.find("a")
            link = SITE + href["href"]
            source = requests.get(link).text
            soup = BeautifulSoup(source, "html.parser")
            table = soup.find("table")
            answer = table.find("b").text
            answers[clues[i]] = answer

    # Concluding progress bar "progress"
    bar.progress(100, "Finished!")
    return answers

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

    # Check if an image is being inserted
    if image is not None:

        with st.spinner("Extracting text..."):
            # Extract text from the image
            text = img_to_text(image)

            # Find the clues
            clues = clean_and_split_clues(text)

        # Creating a progress bar
        bar = st.progress(0, "Resolving Clues...")

        # Finding the clue's answers
        answers = solve_clues(clues, bar)