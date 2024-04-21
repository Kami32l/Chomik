import os
import re
import requests
import tkinter as tk
from time import sleep
from urllib.parse import urlparse

from gui import MainApplication
from get_files import GetFiles
from validators import is_valid_folder_name, uri_validator, url_exists

# brak obsługi dla innych plików niż mp3 - wykorzystuje lukę do odtwarzania w przeglądarce na chomiku plików mp3
# przykładowy folder poprzestawiany:
# https://chomikuj.pl/Konjarek/Audiobook/Andrzej+Pilipiuk/*c5*9awiaty+Pilipiuka/Raport+z+p*c3*b3*c5*82nocy
# folder z dużymi plikami mp3:
# https://chomikuj.pl/barmar7/2017+ROK+2017/01+STYCZEN+2017/Audioboki+w+MP+4+i+mp3
# przykładowy z jpg i mp3 plikami:
# https://chomikuj.pl/JuRiWlO/Audiobooki/AUDIOBOOK/Polskie/Pilipiuk+Andrzej/Pilipiuk+Andrzej+-+Cykl+Kroniki+Jakuba+Wedrowniczka/Pilipiuk+Andrzej+-++Faceci+w+gumofilcach

SPLIT_URL = ['https://chomikuj.pl/Audio.ashx?', '&type=2&tp=mp3']


def ask_user():
    response_to_incorrect_url = 'Url doesnt seem to be valid.'
    while True:
        os.system('cls')
        url = input('url: ')
        if not url.startswith('chomikuj.pl/') and not url.startswith('https://chomikuj.pl/') and not url.startswith(
                'http://chomikuj.pl/'):
            # print('chomik')
            print(response_to_incorrect_url)
            sleep(3)
            continue
        if url.startswith('chomikuj.pl'):
            url = 'https://' + url
        if uri_validator(url) is False:  # does it even do anythin?
            # print('uri validator')
            print(response_to_incorrect_url)
            sleep(3)
            continue
        if url_exists(url) is False:
            print(response_to_incorrect_url)
            sleep(3)
            continue
        break

    while True:
        folder_name = input('nazwa folderu: ')
        if not is_valid_folder_name(folder_name):
            continue
        break

    return url, folder_name

    # if len(urls) == 1:
    #     path_to_file = dir_path + '\\' + names[0] + f'.{file_type}'
    #     download_file(urls[0], path_to_file)
    # else:
    #     i = 0
    #     for url in urls:
    #         path_to_file = dir_path + '\\' + names[i] + f'.{file_type}'
    #         i += 1
    #         download_file(url, path_to_file)
    #         print(f'Pobrano plik {i} z {len(urls)}.')


def verify_user_input(url, folder_name):
    if not url.startswith('chomikuj.pl/') and not url.startswith('https://chomikuj.pl/') and not url.startswith(
            'http://chomikuj.pl/'):
        return False
    if url.startswith('chomikuj.pl'):
        url = 'https://' + url
    if uri_validator(url) is False:
        return False
    if url_exists(url) is False:
        return False
    if not is_valid_folder_name(folder_name):
        return False
    return True

def main():
    root = tk.Tk()

    app = MainApplication(root, verify_input=verify_user_input)
    app.pack(fill="both", expand=True)
    root.mainloop()

    # replace with gui
    # address_url, nazwa_folderu = ask_user()
    #
    # nazwy, identyfikatory = find_ids_names(address_url)
    # if len(nazwy) == 0 or len(identyfikatory) == 0:
    #     print("Nie znaleziono plików możliwych do pobrania.")
    #     sleep(3)
    #     continue
    #
    # adresy = generate_urls(identyfikatory, SPLIT_URL)
    #
    # # for i in range(len(adresy)):
    # #     print(i, adresy[i])
    #
    # print('Rozpoczynanie pobierania.')
    #
    # download_files_from_url(adresy, nazwa_folderu, nazwy)
    #
    # print('Zakończono pobieranie pomyślnie.')
    #
    # continue_input = input('Czy chcesz pobierać kolejne pliki? wpisz "y" lub "Y" jeżeli chcesz kontynuować: ')
    # if not (continue_input == 'y' or continue_input == 'Y'):
    #     break


main()
