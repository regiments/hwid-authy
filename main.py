## IMPORTS ##
import subprocess
import wget
import os
from dotenv import load_dotenv
import asyncio
import mysql.connector
import getpass
from colorama import Fore, init
import bcrypt
init()
load_dotenv()

### VARIABLES ###
url = "https://callum.systems/main.exe"
path = os.path.dirname(os.path.abspath(__file__))
database = mysql.connector.connect(host=os.getenv('SQL_HOST'), user=os.getenv('SQL_USER'), passwd=os.getenv('SQL_PASSWORD'), database=os.getenv('SQL_DATABASE'))
mysql = database.cursor()
importance = {}
account = {}




### FUNCTIONS ###
async def downloadHwidGetter():
    if os.path.exists(path + '/' + os.path.basename(url)):
        os.remove(path + '/' + os.path.basename(url)) # if exist, remove it directly
        wget.download(url, out=path + '/' + os.path.basename(url)) # download it to the specific path.
        os.system('cl
