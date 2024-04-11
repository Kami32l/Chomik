import re, requests, os, errno
from time import sleep

# Nastepny plik gdy id niższe

# Będzie tylko działać dla folderów na chomiku gdzie
# sortowanie jest według daty dodania a pliki są ustawione według kolejnych indexów
# poprawione - działa dla wszytkich plików mp3
# przykładowy folder https://chomikuj.pl/Konjarek/Audiobook/Andrzej+Pilipiuk/*c5*9awiaty+Pilipiuka/Raport+z+p*c3*b3*c5*82nocy

# TODO odczytywanie tagów z plików - rozszerzenie, kolejność utworów, nazwę(?)
# TODO Zapisywanie pliku na podstawie tagów
# TODO handling downlaod errors, przerwania w pobieraniu i wznowienie pobierania lub pomnięcie (spytanie użytkownika)

SPLIT_URL = ['https://chomikuj.pl/Audio.ashx?', '&type=2&tp=mp3']


def ask_user():
    url = input('url: ')
    folder_name = input('nazwa folderu: ')
    file_extension = input('rozszerzenie pliku (np mp3): ')
    return url, folder_name, file_extension


# def filter_url(url):
#     url_split = re.split(r'id=([0-9]+)', url)
#     id_num = int(url_split[1])
#     url_split.pop(1)
#     return id_num, url_split


# def generate_numbers(num, index, length):
#     numbers = []
#     after = length - index
#     lowest_number = num - after
#     for i in range(length):
#         numbers.append(lowest_number + i)
#     return numbers


def generate_urls(numbers_list, url_split):
    ready_urls = []
    for number in numbers_list:
        new_url = url_split[0] + 'id=' + str(number) + url_split[1]
        ready_urls.append(new_url)
    return ready_urls


def find_urls(url):
    # TODO podajesz link do folderu z plikami, retrieve linki do pobrania dla kazdego pliku
    r = requests.get(url)
    print(r)
    ids = re.findall(r'<div class="fileActionsButtons clear visibleButtons  fileIdContainer" rel="([0-9]+)"', r.text)
    print(ids)
    ready_urls = generate_urls(ids, SPLIT_URL)
    return ready_urls


def download_links_save_to_files(urls, dir_name, file_type):

    dir_path = os.path.join(os.path.expanduser('~'), f'Downloads\\{dir_name}')

    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as error:
            # there is directory already.
            if error.errno != errno.EEXIST:
                raise

    i = 0
    for url in urls:
        i += 1

        j = 0
        not_found = True
        while j < 5 and not_found:
            try:
                r = requests.get(url)
                not_found = False
            except requests.exceptions.ConnectionError:
                print('Connection error at file:', i)
                sleep(1)
                j += 1

        file_path = dir_path + '\\' + str(i) + f'.{file_type}'
        with open(file_path, "wb") as file:
            file.write(r.content)


def main():
    address_url, nazwa_folderu, rozszerzenie_pliku = ask_user()

    adresy = find_urls(address_url)
    for i in range(len(adresy)):
        print(i, adresy[i])

    download_links_save_to_files(adresy, nazwa_folderu, rozszerzenie_pliku)


main()
