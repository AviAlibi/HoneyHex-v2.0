import os
from hashlib import sha512
from cryptography.fernet import Fernet, InvalidToken
import base64
from colorama import Fore, Back
from tkinter import filedialog
from time import sleep
import getpass

divider = '*$*%*&*'

def is_valid_fernet_key(key):
    try:
        decoded_key = base64.urlsafe_b64decode(key)
        return len(decoded_key) == 32
    except (base64.binascii.Error, ValueError):
        return False

def setup():
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # passwords_file_path = os.path.join(script_dir, "passwords.txt")
    # print(passwords_file_path)
    
    # if not os.path.exists(passwords_file_path):
    #     with open(passwords_file_path, 'w') as new_file:
    #         print("'passwords.txt' file created in the script's directory.")
    print('Please create a txt file in whatever location of your choosing, we recommend a removable drive')
    input('\nPress ENTER to return to the menu... ')

def encrypt_and_save_data():
    global divider
    key = getpass.getpass('Input your password: ')
    print('A box will soon appear, please select your password file')
    sleep(2)
    passwordFile = filedialog.askopenfile()
    for _ in range(0, 3):
        key = sha512(key.encode('UTF-8')).hexdigest()
    key = key.encode()
    key = key[:32]
    key = base64.urlsafe_b64encode(key)
    cipher_suite = Fernet(key)
    del key
    service = input("Service the data is for: ")
    username_email = input("The primary credential (Usually an email or username): ")
    password = input("The secondary credential (Usually a password): ")
    plain_text = service + divider + username_email + divider + password
    del service
    del username_email
    del password
    cipher_text = cipher_suite.encrypt(plain_text.encode())
    # print(cipher_text)
    decrypted_text = cipher_suite.decrypt(cipher_text).decode()
    del cipher_suite
    # print(f'Decrypted Text: {decrypted_text.split(divider)}')
    with open(passwordFile.name, 'a') as f:
        f.write(cipher_text.decode('utf-8') + "\n")
    print(f"\nEncrypted data has been added to {passwordFile.name}")
    input('\nPress ENTER to return to the menu... ')

def decrypt_data():
    global divider
    key = getpass.getpass('Input your password: ')
    print('A box will soon appear, please select your password file')
    sleep(2)
    passwordFile = filedialog.askopenfile()
    for _ in range(0, 3):
        key = sha512(key.encode('UTF-8')).hexdigest()
    key = key.encode()
    key = key[:32]
    key = base64.urlsafe_b64encode(key)
    cipher_suite = Fernet(key)
    del key
    lines = passwordFile.readlines()
    for line in lines:
            cipher_text = line.strip()
            try:
                plain_text = cipher_suite.decrypt(cipher_text.encode('utf-8'))
            except:
                os.system('cls')
                input('Error code: FISH')
                exit()
            plain_text = plain_text.decode('utf-8').split(divider)
            print(plain_text)
    input('\nPress ENTER to return to the menu... ')
    
def clear_data():
    try:
        file_path = filedialog.askopenfilename()
        
        if not file_path:
            print("No file selected.")
        else:
            if os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    file.truncate(0)

                print(f"Data removed from '{file_path}'.")
            else:
                print(f'The file was deleted or relocated mid-operation')
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    input('Press ENTER to return to the menu... ')

def main():
    firstStart = True
    while True:
        if firstStart:
            print(Fore.YELLOW + Back.BLACK +
'''
/  \__/  \__/  \__/  \__/  \__/  \__
\__/  \__/  \__/  \__/  \__/  \__/  
/  \__/  \__/  \__/  \__/  \__/  \__
\__/  \__/  \_            _/  \__/  
/  \__/  \__/   HoneyHex   \__/  \__
\__/  \__/  \_            _/  \__/  
/  \__/  \__/  \__/  \__/  \__/  \__
\__/  \__/  \__/  \__/  \__/  \__/  
''')
            sleep(3)
            firstStart = False
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(Fore.YELLOW + 'Password Manager:')
        print(Fore.WHITE + '1. Setup' + Fore.YELLOW + Back.BLACK)
        print(Fore.GREEN + '2. Encrypt and Save Data' + Fore.YELLOW + Back.BLACK)
        print(Fore.MAGENTA + '3. Decrypt Data' + Fore.YELLOW + Back.BLACK)
        print(Fore.CYAN + '4. Clear File' + Fore.YELLOW + Back.BLACK)
        print(Fore.RED + '5. Exit' + Fore.YELLOW + Back.BLACK)

        choice = input('Choose an option: ')
        
        if choice == '1':
            setup()
        elif choice == '2':
            encrypt_and_save_data()
        elif choice == '3':
            decrypt_data()
        elif choice == '4':
            clear_data()
        elif choice == '5':
            print("Goodbye!" + Fore.RESET + Back.RESET)
            break
        else:
            print("Invalid option. Please choose a number between 1 and 3.")
            input('Press Enter to continue...')

if __name__ == "__main__":
    main()
