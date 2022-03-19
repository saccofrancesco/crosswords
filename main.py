# Importing Libraries
import pytesseract
import PIL.Image
import requests
from bs4 import BeautifulSoup
import os
import sys

# Set Up the Configurations' Options
CONFIG = r"--psm 6 --oem 3"