# Importing libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import base64
from openai import OpenAI
from streamlit.runtime.uploaded_file_manager import UploadedFile
import json

# Creating and Configuring the OpenAI Client
client: OpenAI = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Crosswords' solutions site
SITE: str = "https://www.dizy.com"
QUERY: str = (
    "https://www.dizy.com/it/cruciverba/?q="  # Base URL to search crossword clues
)


# Transform the image from bytes to base64 encoding format to pass to ChatGPT image model
def encode_uploaded_image(uploaded_file: UploadedFile) -> str:
    """
    Encode a Streamlit UploadedFile (image) to Base64 string for OpenAI input.
    """
    img_bytes: bytes = uploaded_file.read()
    return base64.b64encode(img_bytes).decode("utf-8")


# Instructions prompt
prompt: str = """You are given an image of a crossword puzzle solution. 
Extract the clues and return them strictly in the following Python dictionary format, and nothing else:

{
    "Orizzontali": {
        "1": "...",
        "2": "...",
        "3": "...",
        ...
    },
    "Verticali": {
        "1": "...",
        "2": "...",
        "3": "...",
        ...
    }
}

Rules:
- Do not add explanations, comments, or extra text.
- Do not wrap the response in code fences.
- Use the exact key names "Orizzontali" and "Verticali".
- Only output the dictionary.
"""


def img_to_text(uploaded_file: UploadedFile) -> dict[str, dict[str, str]]:
    """
    Extract text from an image using OpenAI's GPT image model.
    Returns all detected text as formatted JSON like string.
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
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )
    return json.loads(response.output_text)


# Merged function to soup and find immediatley the given element
def requestsoup_and_find(link: str, elem: str) -> Tag | None:
    """
    Fetch HTML content of a webpage and return the first occurrence of a given element.
    """
    source: str = requests.get(link).text
    soup: BeautifulSoup = BeautifulSoup(source, "html.parser")
    return soup.find(elem)


# Web Scraping the dizy site to find teh response to a given clue
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


# Iterative function to loop all the finded clues given by the response of ChatGPT image model
def solve_clues(clues: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """
    Solve crossword clues given in the JSON-like format:
    {
        "Orizzontali": { "1": "clue text", "2": "clue text", ... },
        "Verticali":   { "1": "clue text", "2": "clue text", ... }
    }

    Returns the same structure but with answers filled in:
    {
        "Orizzontali": { "1": "ANSWER", "2": "ANSWER", ... },
        "Verticali":   { "1": "ANSWER", "2": "ANSWER", ... }
    }
    """
    solved: dict[str, dict[str, str]] = {"Orizzontali": {}, "Verticali": {}}

    for section, section_clues in clues.items():
        for num, clue_text in section_clues.items():
            answer: str | None = get_clue_response(clue_text)
            if answer:
                solved[section][num] = answer

    return solved


# Setup of the final Streamlit App
st.set_page_config(
    page_title="Crossword Solver", page_icon="icon.png", layout="centered"
)
st.title("Crosswords")

phrase_tab, photo_tab = st.tabs(["Frase", "Foto"])

# Tab layout description for the photo feature
with photo_tab:
    image: UploadedFile | None = st.camera_input(".", label_visibility="hidden")
    if image is not None:
        st.success("Immagine caricata con successo!")

    photo_button: bool = st.button("Analizza e cerca")
    if photo_button and image is not None:
        with st.spinner("Estraendo il testo..."):
            text: dict[str, dict[str, str]] = img_to_text(image)  # returns dict format

        with st.spinner("Risolvendo le domande..."):
            answers: dict[str, dict[str, str]] = solve_clues(text)

        # Create 2 columns
        horizontal_col, vertical_col = st.columns(2)

        # Show Orizzontali first
        if "Orizzontali" in answers:
            horizontal_col.markdown("### Orizzontali")
            for num, ans in answers["Orizzontali"].items():
                horizontal_col.markdown(f"**{num}.** **{ans}**")

        # Then Verticali
        if "Verticali" in answers:
            vertical_col.markdown("### Verticali")
            for num, ans in answers["Verticali"].items():
                vertical_col.markdown(f"**{num}.** **{ans}**")

# Tab layout description for the much simplier single phrase query
with phrase_tab:
    phrase: str = st.text_input(
        ".",
        placeholder="Inserisci una domanda",
        max_chars=100,
        label_visibility="hidden",
    )
    phrase_button: bool = st.button("Cerca")
    if phrase_button and phrase:
        with st.spinner("Trovando la risposta..."):
            answer: str | None = get_clue_response(phrase)

        if answer is None:
            st.warning("Risposta non trovata...")
        else:
            st.markdown(f"**Risposta:** **{answer}**")
