import re
import requests
import os
import errno


# Nastepny plik gdy id niższe

# Będzie tylko działać dla folderów na chomiku gdzie
# sortowanie jest według daty dodania a pliki są ustawione według kolejnych indexów

# TODO pobieraj pliki z linków
# TODO podajesz link do folderu z plikami, retrieve linki do pobrania dla kazdego pliku


def ask_user():
    url = input('url: ')
    file_index = int(input('index pliku: '))
    num_of_files = int(input('ile plikow: '))
    folder_name = input('nazwa folderu: ')
    file_extension = input('rozszerzenie pliku (np mp3): ')
    return url, file_index, num_of_files, folder_name, file_extension


def filter_url(url):
    url_split = re.split(r'id=([0-9]+)', url)
    id_num = int(url_split[1])
    url_split.pop(1)
    return id_num, url_split


def generate_numbers(num, index, length):
    numbers = []
    after = length - index
    lowest_number = num - after
    for i in range(length):
        numbers.append(lowest_number + i)
    return numbers


def generate_urls(numbers_list, url_split):
    ready_urls = []
    for number in numbers_list:
        new_url = url_split[0] + 'id=' + str(number) + url_split[1]
        ready_urls.append(new_url)
    ready_urls.reverse()
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
        r = requests.get(url)
        file_path = dir_path + '\\' + str(i) + f'.{file_type}'
        with open(file_path, "wb") as file:
            file.write(r.content)


def main():
    address_url, index_pliku, ilosc, nazwa_folderu, rozszerzenie_pliku = ask_user()
    numer_id, adres_rozdzielony = filter_url(address_url)
    numery = generate_numbers(numer_id, index_pliku, ilosc)
    adresy = generate_urls(numery, adres_rozdzielony)

    for i in range(len(adresy)):
        print(i, adresy[i])

    download_links_save_to_files(adresy, nazwa_folderu, rozszerzenie_pliku)


main()
