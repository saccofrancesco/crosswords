# Importing Libraries
import pytesseract
import PIL.Image
import requests
from bs4 import BeautifulSoup
import os
import sys

# Set Up the Configurations' Options
CONFIG = r"--psm 6 --oem 3"

# Defining teh Image Path Manually or Via Command Line Arguments
try:
    path = sys.argv[1]
except IndexError:
    path = "img/text1.jpg"

# Converting thge Image to Text
text = pytesseract.image_to_string(PIL.Image.open(path), config=CONFIG)

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

# Writing to a File the Detected Text
with open("temp.txt", "w") as f:
    f.write(new_text)

# Clues List
words_clauses = []

# Storing Temporary Words' Clauses
with open("temp.txt", "r") as f:
    for line in f:
        cleaned_line = line.replace(" \n", "")
        words_clauses.append(cleaned_line)

# Dizy Site
site = "https://www.dizy.com"

# Getting the Query URL
query = "https://www.dizy.com/it/cruciverba/?q="

# Answer Dictionary
answers = {}

# Getting all the Answer's URL's from Different Sites
for claue in words_clauses:
    splitted = claue.split(" ")
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

# Deleting the Temporary File
os.remove("temp.txt")