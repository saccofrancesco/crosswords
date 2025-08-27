# -----------------------------
# IMPORTS
# -----------------------------
import streamlit as st
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import base64
from openai import OpenAI
from streamlit.runtime.uploaded_file_manager import UploadedFile

# -----------------------------
# OPENAI CLIENT USING SECRETS
# -----------------------------
client: OpenAI = OpenAI(api_key=st.secrets["openai"]["api_key"])

# -----------------------------
# CONFIG & URLS
# -----------------------------
SITE: str = "https://www.dizy.com"
QUERY: str = "https://www.dizy.com/it/cruciverba/?q="  # Base URL to search crossword clues

# -----------------------------
# IMAGE OCR WITH GPT
# -----------------------------
def encode_uploaded_image(uploaded_file: UploadedFile) -> str:
    """
    Encode a Streamlit UploadedFile (image) to Base64 string for OpenAI input.
    """
    img_bytes: bytes = uploaded_file.read()
    return base64.b64encode(img_bytes).decode("utf-8")

def img_to_text(uploaded_file: UploadedFile) -> str:
    """
    Extract text from an image using OpenAI's GPT image model.
    Returns all detected text as a single string.
    """
    base64_image: str = encode_uploaded_image(uploaded_file)
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract all the crossword clues from this image, return them as plain text separated by line breaks."
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}"
                    }
                ],
            }
        ],
    )
    return response.output_text

# -----------------------------
# CLEAN AND SPLIT CLUES
# -----------------------------
def clean_and_split_clues(text: str) -> list[str]:
    """
    Remove unwanted headings and symbols from OCR text, then split it into individual clues.
    """
    text = text.replace("ORIZZONTALI", "").replace("VERTICALI", "").replace(":", "")
    clues: list[str] = [line.strip() for line in text.split("\n") if line.strip()]
    return clues

# -----------------------------
# WEB SCRAPING FOR ANSWERS
# -----------------------------
def requestsoup_and_find(link: str, elem: str) -> Tag | None:
    """
    Fetch HTML content of a webpage and return the first occurrence of a given element.
    """
    source: str = requests.get(link).text
    soup: BeautifulSoup = BeautifulSoup(source, "html.parser")
    return soup.find(elem)

def get_clue_response(clue: str) -> str | None:
    """
    Search dizy.com for the clue and return the first matching answer if found.
    """
    url: str = QUERY + clue
    ul: Tag | None = requestsoup_and_find(url, "ul")
    if ul is not None:
        href: Tag | None = ul.find("a")
        if href is not None:
            link: str = SITE + href["href"]
            table: Tag | None = requestsoup_and_find(link, "table")
            if table is not None:
                answer: Tag | None = table.find("b")
                if answer is not None:
                    return answer.text
    return None

def solve_clues(clues: list[str], bar=None) -> dict[str, str]:
    """
    Solve multiple crossword clues and return a dictionary of {clue: answer}.
    Optionally update a Streamlit progress bar.
    """
    answers: dict[str, str] = {}
    increment: int = 0
    add: int = 100 // len(clues) if clues else 0

    for i, phrase in enumerate(clues):
        if bar is not None:
            increment += add
            bar.progress(increment, "Risolvendo le domande...")

        answer: str | None = get_clue_response(phrase)
        if answer:
            answers[phrase] = answer

    if bar is not None:
        bar.progress(100, "Finito!")

    return answers

# -----------------------------
# STREAMLIT APP
# -----------------------------
st.set_page_config(page_title="Crossword Solver", page_icon="icon.png", layout="centered")
st.title("Crosswords")

phrase_tab, photo_tab = st.tabs(["Frase", "Foto"])

# -----------------------------
# PHOTO TAB
# -----------------------------
with photo_tab:
    image: UploadedFile | None = st.camera_input(".", label_visibility="hidden")
    if image is not None:
        st.success("Immagine caricata con successo!")

    photo_button: bool = st.button("Analizza e cerca")
    if photo_button and image is not None:
        with st.spinner("Estraendo il testo..."):
            text: str = img_to_text(image)
            clues: list[str] = clean_and_split_clues(text)

        bar = st.progress(0, "Risolvendo le domande...")
        answers: dict[str, str] = solve_clues(clues, bar)

        clue_col, answ_col = st.columns(2, gap="small")
        clue_col.subheader("Domande")
        answ_col.subheader("Risposte")

        for clue, answer in answers.items():
            clue_col.markdown(f"**{clue}**")
            answ_col.markdown(f"**{answer}**")

# -----------------------------
# PHRASE TAB
# -----------------------------
with phrase_tab:
    phrase: str = st.text_input(
        ".", placeholder="Inserisci una domanda", max_chars=100, label_visibility="hidden"
    )
    phrase_button: bool = st.button("Cerca")
    if phrase_button and phrase:
        with st.spinner("Trovando la risposta..."):
            answer: str | None = get_clue_response(phrase)

        if answer is None:
            st.warning("Risposta non trovata...")
        else:
            st.markdown(f"**Risposta:** **{answer}**")
