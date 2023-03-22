# Importing GUI LIbraries
import customtkinter
import tkinter
import easygui

# Importing OCR and Crossword Solver Libraries
from bs4 import BeautifulSoup
import pytesseract
import PIL.Image
import requests

# Creating the App object
app = customtkinter.CTk()
app.geometry("600x700")
app.title("Crossword Solver")

# Creating the Title
title = customtkinter.CTkLabel(app, text="Crossword Solver", font=("Berlin Sans FB", 30))
title.pack(pady=15)

# Saving the Path
filepath = tkinter.StringVar(value="Selected Path: None")

# Saving Clues' Answers
clues_answers = tkinter.StringVar(value="")

# Function to get the Path
def get_file() -> None:

    # Asking the Filepath using a GUI
    global filepath
    path = easygui.fileopenbox()

    # Checking if the Selected Path is valid
    splitted_path = path.split("\\")[-1].split(".")[1]
    if splitted_path in ["jpg", "png", "gif", "bmp", "tiff"]:
        filepath.set(f"Selected Path: {path}")

# Creating the Choosefile Button
choosefile_btn = customtkinter.CTkButton(app, text="Choose an Img File", font=("Berlin Sans FB", 15), command=get_file)
choosefile_btn.pack(pady=10)

# File Label
file_label = customtkinter.CTkLabel(app, textvariable=filepath, font=("Berlin Sans FB", 20))
file_label.pack(pady=10)

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

    # Using Pre Created Answers Text
    global clues_answers
    generic_text = ""
    
    # Creating a Text Using Numbers and Answers
    for key, value in answers.items():
        generic_text += f"{key}: {value}\n"

    # Setting the Text to the Extracted Answers
    clues_answers.set(generic_text)

# Action Button
action_btn = customtkinter.CTkButton(app, text="Solve Crossword", font=("Berlin Sans FB", 15), command=solve)
action_btn.pack(pady=10)

# Answers Label
answers_label = customtkinter.CTkLabel(app, textvariable=clues_answers, font=("Berlin Sans FB", 14))
answers_label.pack(pady=10)