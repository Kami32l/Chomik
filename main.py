import re, requests, os, errno
from time import sleep
# from tinytag import TinyTag
from urllib.parse import unquote_plus

# Nastepny plik gdy id niższe

# Będzie tylko działać dla folderów na chomiku gdzie sortowanie jest według daty dodania a pliki są ustawione według
# kolejnych indexów poprawione - działa dla wszytkich plików mp3 (problem - gdy nie w kolejnosci to i tak wedlug
# pobierania zapisuje nazwy)
# poprawione nazwy plików - teraz odczytuje z metadanych pobranych plików więc koljeność powinna być git
# (jest problem gdy w jednym folderze jest wiele książek pojedyńczych albo tycxh które w tytule mają już numer wtedy dublowanie)
# brak obsługi dla innych plików - wykorzystuje lukę do odtwarzania w przeglądarce na chomiku plików mp3
# przykładowy folder poprzestawiany:
# https://chomikuj.pl/Konjarek/Audiobook/Andrzej+Pilipiuk/*c5*9awiaty+Pilipiuka/Raport+z+p*c3*b3*c5*82nocy
# folder z dużymi plikami mp3:
# https://chomikuj.pl/barmar7/2017+ROK+2017/01+STYCZEN+2017/Audioboki+w+MP+4+i+mp3
# przykładowy z jpg i mp3 plikami:
# https://chomikuj.pl/JuRiWlO/Audiobooki/AUDIOBOOK/Polskie/Pilipiuk+Andrzej/Pilipiuk+Andrzej+-+Cykl+Kroniki+Jakuba+Wedrowniczka/Pilipiuk+Andrzej+-++Faceci+w+gumofilcach

# TODO idiot proof inputs
## url - illegal keys?
## foldername - illegal keys?
## check if url exists
## what if no files found at url?
## accept 'https://chomikuj.pl/' and 'chomikuj.pl/' in ur

SPLIT_URL = ['https://chomikuj.pl/Audio.ashx?', '&type=2&tp=mp3']


def ask_user():
    url = input('url: ')
    folder_name = input('nazwa folderu: ')
    return url, folder_name


def generate_urls(numbers_list, url_split):
    # generates download urls
    ready_urls = []
    for number in numbers_list:
        new_url = url_split[0] + 'id=' + str(number) + url_split[1]
        ready_urls.append(new_url)
    return ready_urls


def find_ids_names(url):
    # finds ids of every file in directory
    r = requests.get(url)
    print(r)
    test_1 = re.search(r'<div class="fileActionsButtons clear visibleButtons  fileIdContainer" rel="([0-9]+)"', r.text)
    names = []
    ids = []

    if test_1 is None:
        names_ids = re.findall(r'<a class="downloadAction downloadContext" href=".+/(.+),([0-9]+).mp3', r.text)

    else:
        names_ids = re.findall(r'href="/(.+),([0-9]+).mp3.+" class="downloadAction downloadContext"', r.text)

    for name, ida in names_ids:
        # print(name, ida)
        name_split = name.split('/')
        decoded_name = unquote_plus(name_split[-1].replace('*', '%'))
        # print("decoded_name:", decoded_name)
        names.append(decoded_name)
        ids.append(ida)

    return names, ids


def download_files_from_url(urls, dir_name, names, file_type="mp3"):
    """
    :param urls: list - one or more should be supplied
    :param dir_name: name of the directory files will be saved in
    :param file_type: file extension - eg: mp3, used for saving files
    :param names: list of filenames
    :return:
    """
    dir_path = os.path.join(os.path.expanduser('~'), f'Downloads\\{dir_name}')

    # checks if dir_name directory exists
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as error:
            # there is directory already.
            if error.errno != errno.EEXIST:
                raise

    if len(urls) == 1:
        path_to_file = dir_path + '\\' + names[0] + f'.{file_type}'
        download_file(urls[0], path_to_file)
    else:
        i = 0
        for url in urls:
            path_to_file = dir_path + '\\' + names[i] + f'.{file_type}'
            i += 1
            download_file(url, path_to_file)
            print(f'Pobrano plik {i} z {len(urls)}.')


def download_file(url, file_path):
    # https://stackoverflow.com/a/35504626 - alternative to handle retries
    j = 0
    not_found = True
    while j < 3 and not_found:
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, "wb") as file:
                    # will download in chunks od chunk_size at once
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        file.write(chunk)
            not_found = False

        except requests.exceptions.RequestException as error:
            print(f"An error occurred: {error}")
            sleep(0.1)
            j += 1


def main():
    address_url, nazwa_folderu = ask_user()

    nazwy, identyfikatory = find_ids_names(address_url)
    adresy = generate_urls(identyfikatory, SPLIT_URL)

    # for i in range(len(adresy)):
    #     print(i, adresy[i])

    print('Rozpoczynanie pobierania.')

    download_files_from_url(adresy, nazwa_folderu, nazwy)

    print('Zakończono pobieranie pomyślnie.')


main()
