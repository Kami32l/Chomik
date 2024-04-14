import re, requests, os, errno
from time import sleep
# from tinytag import TinyTag
from urllib.parse import unquote_plus, urlparse


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
## url - illegal keys? --fixed
## foldername - illegal keys? -- fixed
## check if url exists -- check response  --fixed
## what if no files found at url?
## accept 'https://chomikuj.pl/' and 'chomikuj.pl/' in url --fixed

SPLIT_URL = ['https://chomikuj.pl/Audio.ashx?', '&type=2&tp=mp3']


def ask_user():
    invalid_url_response = 'Url doesnt seem to be valid.'
    while True:
        url = input('url: ')
        os.system('cls')
        if not url.startswith('chomikuj.pl/') and not url.startswith('https://chomikuj.pl/') and not url.startswith('http://chomikuj.pl/'):
            # print('chomik')
            print(invalid_url_response)
            continue
        if url.startswith('chomikuj.pl'):
            url = 'https://' + url
        if uri_validator(url) is False: #does it even do anythin?
            # print('uri validator')
            print(invalid_url_response)
            continue
        if url_exists(url) is False:
            print(invalid_url_response)
            continue
        break

    while True:
        folder_name = input('nazwa folderu: ')
        if not is_valid_folder_name(folder_name):
            continue
        break

    return url, folder_name


def is_valid_folder_name(name: str):
    # Define a regular expression pattern to match forbidden characters
    ILLEGAL_NTFS_CHARS = r'[<>:/\\|?*\"]|[\0-\31]'
    # Define a list of forbidden names
    FORBIDDEN_NAMES = ['CON', 'PRN', 'AUX', 'NUL',
                       'COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                       'COM6', 'COM7', 'COM8', 'COM9',
                       'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5',
                       'LPT6', 'LPT7', 'LPT8', 'LPT9']
    # Check for forbidden characters
    match = re.search(ILLEGAL_NTFS_CHARS, name)
    if match:
        # raise ValueError(
        #     f"Invalid character {match[0]} for filename {name}")
        return False
    # Check for forbidden names
    if name.upper() in FORBIDDEN_NAMES:
        # raise ValueError(f"{name} is a reserved folder name in windows")
        return False
    # Check for empty name (disallowed in Windows)
    if name.strip() == "":
        # raise ValueError("Empty file name not allowed in Windows")
        return False
    # Check for names starting or ending with dot or space
    match = re.match(r'^[. ]|.*[. ]$', name)
    if match:
        # raise ValueError(
        #     f"Invalid start or end character ({match[0]})"
        #     f" in folder name {name}"
        # )
        return False
    return True


def url_exists(url):
    r = requests.get(url)
    if r.status_code == 200:
        return True

    elif r.status_code == 404:
        return False


def uri_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


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
