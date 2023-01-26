import os, sys, platform, ctypes, phonenumbers
from phonenumbers import carrier
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Installation des librairies
os.system("pip install phonenumbers")

# Pour mettre à jour le titre de la fenêtre
def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

is_windows = True if platform.system() == "Windows" else False

# Demander à l'utilisateur de choisir le pays
os.system('cls' if os.name == 'nt' else 'clear')
print("Sélectionnez le pays pour la numérotation :")
print("1. France")
print("2. Suisse")
print("3. Belgique")

choice = int(input())
if choice == 1:
    country_code = "FR"
elif choice == 2:
    country_code = "CH"
elif choice == 3:
    country_code = "BE"
else:
    print("Sélection de pays non valide.")
    exit()

# Demander à l'utilisateur de choisir le fichier à importer
root = tk.Tk()
root.withdraw()
print("Entrez le chemin du fichier contenant les numéros : ")
file_path = filedialog.askopenfilename(title = ('Sélectionner votre fichier à trier'))

# Vérifier si le fichier existe
if not os.path.isfile(file_path):
    print("Le fichier spécifié n'existe pas.")
    exit()

# Créer un dossier pour le pays sélectionné s'il n'existe pas
if not os.path.isdir(country_code):
    os.mkdir(country_code)

# Ouvrir le fichier et lire les numéros
with open(file_path, 'r') as file:
    numbers = file.readlines()

# Dictionnaire pour stocker les numéros triés par opérateur
operators = {}

# Trier les numéros selon l'opérateur et le pays
for i, number in enumerate(numbers):
    try:
        parsed_number = phonenumbers.parse(number, country_code)
        carrier = phonenumbers.carrier.name_for_number(parsed_number, "fr")
        if carrier not in operators:
            operators[carrier] = []
        operators[carrier].append(number)
        set_console_title(f'Checking {i+1}/{len(numbers)} numbers...')
        sys.stdout.write(f'Checking {i+1}/{len(numbers)} numbers...\r')
        sys.stdout.flush()
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(e)

# Ecrire les numéros triés dans des fichiers
for operator, numbers in operators.items():
    file_name = operator + "_" + datetime.now().strftime("%Y%m%d") + ".txt"
    file_path = os.path.join(country_code, file_name)
    with open(file_path, 'w') as file:
        file.writelines(numbers)

print("Les numéros ont été triés et enregistrés dans le dossier", country_code)