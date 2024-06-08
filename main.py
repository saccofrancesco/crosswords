# Importing Libraries
from bs4 import BeautifulSoup
from bs4.element import Tag
import pytesseract
import PIL.Image
import requests
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

# Set Up the Configurations' Options
CONFIG: str = r"--psm 6 --oem 3"

# Dizy Site
SITE: str = "https://www.dizy.com"

# Query URL
QUERY: str = "https://www.dizy.com/it/cruciverba/?q="

# Transform and analyze the image to extract text
def img_to_text(image: bytes) -> str:
    """
    Extracts text from an image using Tesseract OCR.

    Parameters:
    image (bytes): The image from which text will be extracted.

    Returns:
    str: The extracted text.
    """
    return pytesseract.image_to_string(PIL.Image.open(image), config=CONFIG)

# Function for cleaning data and splitting the clues
def clean_and_split_clues(text: str) -> list:
    """
    Cleans and splits the text into individual clues.

    Parameters:
    text (str): The raw text containing the clues.

    Returns:
    list: A list of cleaned clues.
    """
    # Clean the data
    text: str = text.replace(
        "ORIZZONTALI", "").replace(
        "VERTICALI", "").replace(
        ":", "").replace(
        "-", "").replace(
        "_", "").replace(
        ".", "")
    not_filtered_list: list = text.split()

    # Split the clues
    cleared_clues: list = []
    current_clue: str = ""
    for word in not_filtered_list:
        if word.isdigit() and len(word) not in [3, 4]:
            if current_clue:
                cleared_clues.append(current_clue.strip())
                current_clue: str = ""
        else:
            current_clue += f"{word} "
    if current_clue:
        cleared_clues.append(current_clue.strip())

    return cleared_clues

# Function to get soup response from a page
def requestsoup_and_find(link: str, elem: str):
    """
    Sends a GET request to a URL and parses the HTML to find a specified element.

    Parameters:
    link (str): The URL to request.
    elem (str): The HTML element to find.

    Returns:
    BeautifulSoup element: The first found HTML element matching the specified tag.
    """
    source: str = requests.get(link).text
    soup: BeautifulSoup = BeautifulSoup(source, "html.parser")
    return soup.find(elem)

# Resolve only one clue
def get_clue_response(clue: str) -> str:
    """
    Gets the response for a single crossword clue by scraping a website.

    Parameters:
    clue (str): The crossword clue to solve.

    Returns:
    str: The answer to the clue, or None if not found.
    """
    url: str = QUERY + clue
    ul: Tag = requestsoup_and_find(url, "ul")
    if ul is not None:
        href: Tag = ul.find("a")
        if href is not None:
            link: str = SITE + href["href"]
            table: Tag = requestsoup_and_find(link, "table")
            if table is not None:
                answer: Tag = table.find("b")
                if answer is not None:
                    return answer.text
    else:
        return None

# Solve the clues scraping on the clues site, pairing the answers
def solve_clues(clues: list, bar=None) -> dict:
    """
    Solves a list of crossword clues by scraping answers from a website.

    Parameters:
    clues (list): A list of crossword clues to solve.
    bar (streamlit.progress, optional): A Streamlit progress bar object.

    Returns:
    dict: A dictionary mapping clues to their answers.
    """
    answers: dict = {}

    if bar is not None:
        increment: int = 0
        add: int = 100 // len(clues)

    for i, phrase in enumerate(clues):
        if bar is not None:
            increment += add
            bar.progress(increment, "Risolvendo le domande...")

        answer: str = get_clue_response(phrase)
        if answer is not None:
            answers[clues[i]] = answer

    if bar is not None:
        bar.progress(100, "Finito!")

    return answers

# Main program
if __name__ == "__main__":
    
    # Modifying App name and icon
    st.set_page_config(
        page_title='Crossword Solver',
        page_icon="favicon.ico",
        layout="centered")

    # Title of the Program
    st.title("Crossword Solver")

    # Creating multiple tabs for photo and inline answers
    phrase_tab, photo_tab = st.tabs(["Frase", "Foto"])

    # Managing the Photo tab
    with photo_tab:
        # Creating a Camera input to take photos
        image: UploadedFile = st.camera_input(".", label_visibility="hidden")

        # Displaying a success message if an image is uploaded
        if image is not None:
            st.success("Immagine caricata con successo!")

        # Button for starting the process
        photo_button: bool = st.button("Analizza e cerca")

        # Check if an image is being inserted
        if photo_button and image is not None:
            with st.spinner("Estraendo il testo..."):
                # Extract text from the image
                text: str = img_to_text(image)

                # Find the clues
                clues: list = clean_and_split_clues(text)

            # Creating a progress bar
            bar: bool = st.progress(0, "Risolvendo le domande...")

            # Finding the clue's answers
            answers: dict = solve_clues(clues, bar)

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
        phrase: str = st.text_input(".", placeholder="Inserisci una domanda",
                               max_chars=100, label_visibility="hidden")
        
        # Displaying an enter button
        phrase_button: bool = st.button("Cerca")

        # Searching the response
        if phrase_button and phrase != "":
            with st.spinner("Trovando la risposta..."):
                answer: str = get_clue_response(phrase)

            # None case
            if answer is None:
                # Display a warning box
                st.warning("Risposta non trovata...")
            else:
                # Display the response with markdown format
                st.markdown(f"**Risposta:** **{answer}**")
