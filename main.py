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