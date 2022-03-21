# Importing Libraries
import pytesseract
import PIL.Image
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track
import os
import sys

# Console Object
console = Console()

# Dizy Site
site = "https://www.dizy.com"

# Query URL
query = "https://www.dizy.com/it/cruciverba/?q="

# Defining the Initialization Method
def init() -> tuple:

    # Set Up the Configurations' Options
    CONFIG = r"--psm 6 --oem 3"

    # Defining the Image Path Manually or Via Command Line Arguments
    try:
        path = sys.argv[1]
    except IndexError:
        path = "img/text1.jpg"

    # Returning the Configurations and the Image Path
    return CONFIG, path

# Extracting Text form the Processed Image
def extractText(config: str, path: str) -> str:

    # Setting Up the Animation
    print("\n")
    with console.status("🔍 [blue]Extracting Text from the Image...[/blue]"):

        # Converting the Image to Text
        text = pytesseract.image_to_string(PIL.Image.open(path), config=config)

    # Showing a Result Message
    print("\n")
    console.print("✅ [green]Image Succesfully Processed! Text Extracted![/green]\n")

    # Returning the Extracted Text
    return text

# Method for Cleaning the Extracted Data
def cleanImageData(text: str) -> str:

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
            if not_filtered_list[i].isdigit() and i != 0  and len(not_filtered_list[i]) not in [3, 4]:
                new_text += "\n"
            new_text += f"{not_filtered_list[i]} "

    # Returning the New Cleaned Text
    return new_text

# Method for Storing the Extracted Answers' Clues
def getClues(filePath: str) -> list:

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
def getAnswers(cluesList: list) -> dict:

    # Answer Dictionary
    answers = {}

    # Getting all the Answer's URL's from Different Sites
    for i in track(range(len(cluesList)), description = "[yellow]Parsing Answers...[/yellow]\n"):
        splitted = cluesList[i].split(" ")
        phrase = " ".join(splitted[1:])
        url = query + phrase
        source = requests.get(url).text
        soup = BeautifulSoup(source, "html.parser")
        if ul := soup.find("ul"):
            href = ul.find("a")
            link = site + href["href"]
            source = requests.get(link).text
            soup = BeautifulSoup(source, "html.parser")
            answer = soup.find("b").text
            answers[splitted[0]] = answer

    # Returning the Answers in a Dictionary Data Structure
    return answers

# Method for Displaying the Answers
def showAnswers(answers: dict) -> None:

    # Output Message
    console.print("[blue]###### Answer List ######[/blue]")

    # Printing the Results in the Console
    for key, value in answers.items():
        console.print(f"[yellow]Answer N°{key}[/yellow]: [green]{value}[/green]")

# Defined Main Instance of the Program
if __name__ == "__main__":

    # Running the Initialization
    initialization = init()

    # Running the Image's Analisy
    text = extractText(initialization[0], initialization[1])

    # Cleaning the Text
    text = cleanImageData(text)

    # Writing to a File the Detected Text
    with open("temp.txt", "w") as f:
        f.write(text)

    # Getting the Clues
    clues_list = getClues("temp.txt")

    # Getting the Answers
    answers = getAnswers(clues_list)

    # Deleting Temporary Files
    os.remove("temp.txt")

    showAnswers(answers)