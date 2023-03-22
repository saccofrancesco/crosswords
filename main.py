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

# Method for Cleaning the Extracted Data
def clean_image_data(text: str) -> str:

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

    # Returning the New Cleaned Text
    return new_text

# Method for Storing the Extracted Answers' Clues
def get_clues(filePath: str) -> list:

    # Clues List
    words_clues = []

    # Storing Temporary Words' Clues
    with open(filePath, "r") as f:
        for line in f:
            cleaned_line = line.replace(" \n", "")
            words_clues.append(cleaned_line)

    # Returning the Created Clues' List
    return words_clues

# Method for Getting the Answer Using the Extracted Clues
def get_answers(cluesList: list) -> dict:

    # Answer Dictionary
    answers = {}

    # Getting all the Answer's URL's from Different Sites
    for i in track(range(len(cluesList)),
                   description="[yellow]Parsing Answers...[/yellow]\n"):
        splitted = cluesList[i].split(" ")
        phrase = " ".join(splitted[1:])
        url = QUERY + phrase
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        if ul := soup.find("ul"):
            href = ul.find("a")
            link = SITE + href["href"]
            source = requests.get(link).text
            soup = BeautifulSoup(source, "html.parser")
            answer = soup.find("b").text
            answers[cluesList[i]] = answer

    # Returning the Answers in a Dictionary Data Structure
    return answers

# Method for Displaying the Answers
def show_answers(answers: dict) -> None:

    # Creating the Table
    table = Table()

    # Creating the Columns
    table.add_column("Number", style="cyan")
    table.add_column("Clue", style="magenta")
    table.add_column("Answer", style="green")

    # Adding the Rows
    for key, value in answers.items():
        splitted = key.split(" ")
        n = splitted[0]
        clue = "".join(f'{word} ' for word in splitted[1:])
        table.add_row(n, clue, value)

    # Printing the Table
    CONSOLE.print(table)
    print("\n")


# Defined Main Instance of the Program
if __name__ == "__main__":

    # Running the Initialization
    INIT = init()

    # Running the Image's Analisy
    text = extract_text(INIT["config"], INIT["path"])

    # Cleaning the Text
    text = clean_image_data(text)

    # Writing to a File the Detected Text
    with open("temp.txt", "w") as f:
        f.write(text)

    # Getting the Clues
    CLUES = get_clues("temp.txt")

    # Getting the Answers
    ANSWERS = get_answers(CLUES)

    # Deleting Temporary Files
    os.remove("temp.txt")

    # Showing the Answers
    show_answers(ANSWERS)
