### IMPORTS ##
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
        os.system('cls')       
    else:
        wget.download(url, out=path + '/' + os.path.basename(url)) # download it to the specific path.      
        os.system('cls')     

async def main():
        await downloadHwidGetter()
        hwid = subprocess.check_output("main")
        hwid = hwid.decode('utf-8')
        uuid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        if len(hwid) != 36:
            print(Fore.RED + 'Error: Invalid HWID | If this persists then please contact callum.')
            input('Press enter to exit.')
            await RegLogPage()
        else:
            importance['hwid'] = hwid
            importance['uuid'] = uuid
            await RegLogPage()

async def RegLogPage():
    os.system("mode con cols=110 lines=37")
    print(Fore.GREEN + '                                   Welcome to the registration page.' + Fore.BLUE + """         
                ╔═══════════════════════╦═══════════════════════╦═══════════════════════╗
                ║                             1. Login                                  ║
                ║                             2. Register                               ║
                ║                             3. Attempt Auto Login                     ║
                ╚═══════════════════════╩═══════════════════════╩═══════════════════════╝""")
    #print(importance.get('hwid'))
    option = input('Select Your Option: ')
    option = int(option)
    if option == 1:
        await ProcessLogin()
    elif option == 2:
        await ProcessRegister()
    elif option == 3:
        await AutoLogin()
    else:
        print(Fore.RED + 'Error: Invalid Option.')
        


### LOGIN & REGISTER ###
async def ProcessRegister():
    os.system('cls')
    print(Fore.GREEN + 'Welcome to the registration page.\n')
    key = input(Fore.BLUE + '\nPlease Enter Your License Key? ')
    key = key
    if len(key) > 32 or len(key) < 32:
        print(Fore.RED + 'Error: Invalid Key. (Too Short Or Too Long')
    else:
        print(Fore.GREEN + '\nProcessing...')
        mysql.execute("SELECT * FROM `license-keys` WHERE `key` = %s", (key,))
        res = mysql.fetchone()
        key = res[1]
        key_ident = res[0]
        used = int(res[2])
        if used == 0:
            username = input(Fore.BLUE + '\nPlease Enter Your Username: ')
            mysql.execute("SELECT * FROM `users` WHERE `username` = %s", (username,))
            res2 = mysql.fetchone()
            if res2 == None:
                password = getpass.getpass(Fore.BLUE + '\nPlease Enter Your Password: ')
                password = password
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                mysql.execute("INSERT INTO `users` (`username`, `password`, `hwid`, `uuid`, `key_owned`) VALUES (%s, %s, %s, %s, %s)", (username, password, importance.get('hwid'), importance.get('uuid'), key_ident))
                mysql.execute("UPDATE `license-keys` SET `used` = 1 WHERE `key` = %s", (key,))
                database.commit()
                print(Fore.GREEN + '\nRegistration Successful!')
                input('Press enter to continue.')
                await main()
            else:
                print(Fore.RED + 'Error: Username Taken.')
                input('Press enter to continue.')
                await main()
        else:
            print(Fore.RED + 'Error: Key Already Used.')
            input('Press enter to continue.')
            await main()

async def ProcessLogin():
    print(Fore.GREEN + 'Welcome to the login page.\n')
    username = input(Fore.BLUE + '\nPlease Enter Your Username: ')
    password = getpass.getpass(Fore.BLUE + '\nPlease Enter Your Password: ')
    mysql.execute("SELECT * FROM `users` WHERE `username` = %s", (username,))
    res = mysql.fetchone()
    hash = res[2]
    account['hwid'] = res[3]
    account['uuid'] = res[4]
    if bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8')):
        if account.get('hwid') == importance.get('hwid') and account.get('uuid') == importance.get('uuid'):
            print(Fore.GREEN + '\nLogin Successful!')
            account['username'] = res[1]
            account['id'] = res[0]
            await LoggedInPage()
        else:
            print('\nError: HWID or UUID does not match.')
    else:
        print('wrong pwd')
    


async def AutoLogin():
    mysql.execute("SELECT * FROM `users` WHERE `hwid` = %s AND `uuid` = %s", (importance.get('hwid'), importance.get('uuid')))
    res = mysql.fetchone()
    if res == None:
        print(Fore.RED + 'Error: No Account Found.')
        input('Press enter to continue.')
        await main()
    else:
        account['username'] = res[1]
        account['id'] = res[0]
        await LoggedInPage()


async def LoggedInPage():
    os.system("mode con cols=110 lines=37")
    print(Fore.GREEN + f'                                          Logged In As: {account.get("username")}' + Fore.BLUE + """         
                ╔═══════════════════════╦═══════════════════════╦═══════════════════════╗
                ║                             1. Option 1                               ║
                ║                             2. Option 2                               ║
                ╚═══════════════════════╩═══════════════════════╩═══════════════════════╝""")
    option = input('Select Your Option: ')
  
      
### MAIN ###
if __name__ == "__main__":
    if os.path.exists(path + '/' + os.path.basename(url)):
        os.remove(path + '/' + os.path.basename(url))
        asyncio.run(main())
    else:
        asyncio.run(main())
        
        



