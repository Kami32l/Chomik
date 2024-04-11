import re, requests, os, errno
from time import sleep

# Nastepny plik gdy id niższe

# Będzie tylko działać dla folderów na chomiku gdzie
# sortowanie jest według daty dodania a pliki są ustawione według kolejnych indexów
# poprawione - działa dla wszytkich plików mp3 (problem - gdy nie w kolejnosci to i tak wedlug pobierania zapisuje nazwy)
# przykładowy folder poprzestawiany https://chomikuj.pl/Konjarek/Audiobook/Andrzej+Pilipiuk/*c5*9awiaty+Pilipiuka/Raport+z+p*c3*b3*c5*82nocy
# folder z dużymi plikami mp3 https://chomikuj.pl/barmar7/2017+ROK+2017/01+STYCZEN+2017/Audioboki+w+MP+4+i+mp3

# TODO odczytywanie tagów z plików - rozszerzenie, kolejność utworów, nazwę(?)
# TODO Zapisywanie nazwy, kolejnośći pliku na podstawie tagów
# TODO pomnięcie pobierania pliku (spytanie użytkownika)

SPLIT_URL = ['https://chomikuj.pl/Audio.ashx?', '&type=2&tp=mp3']


def ask_user():
    url = input('url: ')
    folder_name = input('nazwa folderu: ')
    file_extension = input('rozszerzenie pliku (np mp3): ')
    return url, folder_name, file_extension


def generate_urls(numbers_list, url_split):
    ready_urls = []
    for number in numbers_list:
        new_url = url_split[0] + 'id=' + str(number) + url_split[1]
        ready_urls.append(new_url)
    return ready_urls


def find_urls(url):
    r = requests.get(url)
    print(r)
    ids = re.findall(r'<div class="fileActionsButtons clear visibleButtons  fileIdContainer" rel="([0-9]+)"', r.text)
    print(ids)
    ready_urls = generate_urls(ids, SPLIT_URL)
    return ready_urls


def download_files(urls, dir_name, file_type):
    dir_path = os.path.join(os.path.expanduser('~'), f'Downloads\\{dir_name}')

    # checks if dir_name directory exists
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as error:
            # there is directory already.
            if error.errno != errno.EEXIST:
                raise


    i = 0
    #TODO zabezpieczenie przed tym że tylko jeden adres url w urls
    for url in urls:
        i += 1
        file_path = dir_path + '\\' + str(i) + f'.{file_type}'

        #https://stackoverflow.com/a/35504626 - alternative to handle retries
        j = 0
        not_found = True
        while j < 3 and not_found:
            try:
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, "wb") as file:
                        # will download in chunks od chunk_size at once
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            file.write(chunk)
                not_found = False

            except requests.exceptions.RequestException as error:
                print(f"An error occurred: {error}")
                sleep(0.1)
                j += 1


def main():
    address_url, nazwa_folderu, rozszerzenie_pliku = ask_user()

    adresy = find_urls(address_url)
    for i in range(len(adresy)):
        print(i, adresy[i])

    download_files(adresy, nazwa_folderu, rozszerzenie_pliku)

    print('Finished downloading successfully.')

main()
