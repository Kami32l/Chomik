
class GetFiles():
    def __init__(self, url):
        self.split_url = ['https://chomikuj.pl/Audio.ashx?', '&type=2&tp=mp3']
        self.names, self.ids = self.find_ids_names(url)
        self.addresses = self.generate_urls()

    def find_ids_names(self, url):
        pass

    def generate_urls(self):
        #self.ids, self.split_url
        pass

    def download_files_from_url(self, dir_name):
        # self.names, self.addresses
        pass

    def download_file(self, download_url, file_path):
        pass
