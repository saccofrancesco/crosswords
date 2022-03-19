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