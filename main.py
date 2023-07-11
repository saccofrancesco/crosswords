# Importing Libraries
from bs4 import BeautifulSoup
import pytesseract
import PIL.Image
import requests
import streamlit as st

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

    # Clean the data
    text = text.replace(
        "ORIZZONTALI",
        "").replace(
        "VERTICALI",
        "").replace(
            ":",
            "").replace(
                "-",
                "").replace(
                    "_",
                    "").replace(
                        ".",
        "")
    not_filtered_list = text.split()

    # Split the clues
    cleared_clues = []
    current_clue = ""
    for word in not_filtered_list:
        if word.isdigit() and len(word) not in [3, 4]:
            if current_clue:
                cleared_clues.append(current_clue.strip())
                current_clue = ""
        else:
            current_clue += f"{word} "
    if current_clue:
        cleared_clues.append(current_clue.strip())

    return cleared_clues

# Function to get soup response from a page


def requestsoup_and_find(link: str, elem: str):
    source = requests.get(link).text
    soup = BeautifulSoup(source, "html.parser")

    return soup.find(elem)

# Resolve only one clue


def get_clue_response(clue: str) -> str:

    url = QUERY + clue
    ul = requestsoup_and_find(url, "ul")
    if ul is not None:
        href = ul.find("a")
        if href is not None:
            link = SITE + href["href"]
            table = requestsoup_and_find(link, "table")
            if table is not None:
                answer = table.find("b")
                if answer is not None:
                    return answer.text

    return None

# Solve the clues scraping on the clues site, pairing the answers


def solve_clues(clues: list, bar=None) -> dict:
    answers = {}

    if bar is not None:
        increment = 0
        add = 100 // len(clues)

    for i, phrase in enumerate(clues):
        if bar is not None:
            increment += add
            bar.progress(increment, "Risolvendo le domande...")

        answer = get_clue_response(phrase)
        if answer is not None:
            answers[clues[i]] = answer

    if bar is not None:
        bar.progress(100, "Finito!")

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

    # Creating multiple tabs for photo and inline answers
    photo_tab, phrase_tab = st.tabs(["Foto", "Frase"])

    # Managing the Photo tab
    with photo_tab:

        # Creating a Camera input to take photos
        image = st.camera_input(".", label_visibility="hidden")

        # Check if an image is being inserted
        if image is not None:

            with st.spinner("Estraendo il testo..."):
                # Extract text from the image
                text = img_to_text(image)

                # Find the clues
                clues = clean_and_split_clues(text)

            # Creating a progress bar
            bar = st.progress(0, "Risolvendo le domande...")

            # Finding the clue's answers
            answers = solve_clues(clues, bar)

            # Creating 2 Columns
            clue_col, answ_col = st.columns(2, gap="small")
            clue_col.subheader("Domande")
            answ_col.subheader("Risposte")

            # Looping through the result and displaying the answers
            for clue, answer in answers.items():
                clue_col.markdown(f"**{clue}**")
                answ_col.markdown(f"**{answer}**")

    # Managing the Phrase tab
    with phrase_tab:

        # Displaying the input field
        st.text_input(".", placeholder="Inserisci una domanda",
                      max_chars=100, label_visibility="hidden")
