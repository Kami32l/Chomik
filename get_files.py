from urllib.parse import unquote_plus
import os
import requests
import re
import errno
from time import sleep
from bs4 import BeautifulSoup


class GetFiles:
    def __init__(self, url):
        self.dir_path = None
        self.split_url = ['https://chomikuj.pl/Audio.ashx?', '&type=2&tp=mp3']
        self.url_list = self.find_pages(url)
        self.names, self.ids = self.find_ids_names(self.url_list)
        self.addresses = self.generate_urls()
        self.addresses_len = len(self.addresses)    # Ilość plików do pobrania
        self.file_dwnl_nr = 0   # Nr pobieranego pliku

    @staticmethod
    def find_pages(url):
        page_urls = [url]
        site = 'https://chomikuj.pl'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find(id="listView")

        try:
            urls_elements = result.find("div", class_="paginator clear fileListPage").find("ul").find_all("li", class_="")
            for element in urls_elements:
                relative_url = element.find('a')['href']
                link = site + relative_url
                page_urls.append(link)
        except AttributeError:
            # print('Only one url')
            pass

        return page_urls

    @staticmethod
    def find_ids_names(urls_list):
        # finds ids and names of every file in directory
        names = []
        ids = []

        for url in urls_list:
            r = requests.get(url)
            # print(r)
            test_1 = re.search(r'<div class="fileActionsButtons clear visibleButtons  fileIdContainer" rel="([0-9]+)"',
                               r.text)

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

    def generate_urls(self):
        # generates download urls
        ready_urls = []
        for number in self.ids:
            new_url = self.split_url[0] + 'id=' + str(number) + self.split_url[1]
            ready_urls.append(new_url)
        return ready_urls

    def create_directory(self, dir_name):
        self.dir_path = os.path.join(os.path.expanduser('~'), f'Downloads\\{dir_name}')

        # checks if dir_name directory exists
        if not os.path.exists(self.dir_path):
            try:
                os.makedirs(self.dir_path)
            except OSError as error:
                # there is directory already (was created since last check).
                if error.errno != errno.EEXIST:
                    raise

    # def download_files_from_url(self, dir_name):
    #     #
    #     self.create_directory(dir_name)
    #
    #     if len(self.addresses) == 1:
    #         path_to_file = self.dir_path + '\\' + self.names[0] + '.mp3'
    #         self.download_file(self.addresses[0], path_to_file)
    #     else:
    #         for url in self.addresses:
    #             path_to_file = self.dir_path + '\\' + self.names[self.file_dwnl_nr] + '.mp3'
    #             self.file_dwnl_nr += 1
    #             self.download_file(url, path_to_file)
    #             # print(f'Pobrano plik {self.i} z {len(self.addresses)}.')

    @staticmethod
    def download_file(download_url, file_path):
        # https://stackoverflow.com/a/35504626 - alternative to handle retries
        j = 0
        not_found = True
        while j < 3 and not_found:
            try:
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, "wb") as file:
                        # will download in chunks od chunk_size at once
                        for chunk in r.iter_content(chunk_size=1024 * 1024):
                            file.write(chunk)
                not_found = False

            except requests.exceptions.RequestException as error:
                # print(f"An error occurred: {error}")
                sleep(0.1)
                j += 1
