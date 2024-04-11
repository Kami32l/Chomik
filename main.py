import re

# Nastepny plik gdy id niższe

# Będzie tylko działać dla folderów na chomiku gdzie
# sortowanie jest według daty dodania a pliki są ustawione według kolejnych indexów

# TODO pobieraj pliki z linków
# TODO podajesz link do folderu z plikami, retrieve linki do pobrania dla kazdego pliku


def ask_user():
    url = input('url: ')
    file_index = int(input('index pliku: '))
    num_of_files = int(input('ile plikow: '))
    return url, file_index, num_of_files


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
        numbers.append(lowest_number+i)
    return numbers


def generate_urls(numbers_list, url_split):
    ready_urls = []
    for number in numbers_list:
        new_url = url_split[0] + 'id=' + str(number) + url_split[1]
        ready_urls.append(new_url)
    return ready_urls


def download_links(urls):
    



def main():
    address_url, index_pliku, ilosc = ask_user()
    numer_id, adres_rozdzielony = filter_url(address_url)
    numery = generate_numbers(numer_id, index_pliku, ilosc)
    adresy = generate_urls(numery, adres_rozdzielony)

    for i in range(len(adresy)):
        print(i, adresy[i])

main()