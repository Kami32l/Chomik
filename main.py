import tkinter as tk
from get_files import GetFiles
from gui import MainApplication
from validators import is_valid_folder_name, uri_validator, url_exists
import re


# brak obsługi dla innych plików niż mp3 - wykorzystuje lukę do odtwarzania w przeglądarce na chomiku plików mp3
# przykładowy folder poprzestawiany:
# https://chomikuj.pl/Konjarek/Audiobook/Andrzej+Pilipiuk/*c5*9awiaty+Pilipiuka/Raport+z+p*c3*b3*c5*82nocy
# folder z dużymi plikami mp3:
# https://chomikuj.pl/barmar7/2017+ROK+2017/01+STYCZEN+2017/Audioboki+w+MP+4+i+mp3
# przykładowy z jpg i mp3 plikami:
# https://chomikuj.pl/JuRiWlO/Audiobooki/AUDIOBOOK/Polskie/Pilipiuk+Andrzej/Pilipiuk+Andrzej+-+Cykl+Kroniki+Jakuba+Wedrowniczka/Pilipiuk+Andrzej+-++Faceci+w+gumofilcach

def verify_user_input(url, folder_name):
    if not url.startswith('https://chomikuj.pl/') and not url.startswith(
            'http://chomikuj.pl/'):
        return 3
    url = re.search(r'(chomikuj\.pl.+)', url)
    if url is None:
        return 3
    # print(url[0])
    if '//' in url[0] or url[0] == 'chomikuj.pl/':
        return 3
    url = 'https://' + url[0]
    if uri_validator(url) is False:
        return 3
    if url_exists(url) is False:
        return 3
    if not is_valid_folder_name(folder_name):
        return 2
    return 1


def round_3(a):
    a = int(a * 1000)
    return a / 1000


def main():
    root = tk.Tk()

    app = MainApplication(root, verify_input=verify_user_input)
    app.pack(fill="both", expand=True)

    used_get_files = False
    while True:
        if app.closing_app is not True:
            if app.download_window_status and not used_get_files:
                used_get_files = True
                gf = GetFiles(app.url)
                gf.create_directory(app.folder)
                # print(gf.addresses)
                # print(app.folder)
                app.window.progress['value'] = 0
                if len(gf.addresses) == 0:
                    app.window.message_info(message_text='Nie znaleziono plików pod podanym adresem url!')
                    app.window.terminate_download_window()
                if len(gf.addresses) == 1:
                    path_to_file = gf.dir_path + '\\' + gf.names[0] + '.mp3'
                    gf.download_file(gf.addresses[0], path_to_file)

                    # update progress bar
                    app.window.progress['value'] = 100
                    # print(app.window.progress['value'])
                    app.window.download_complete()

                    root.update()
                else:
                    for url in gf.addresses:
                        path_to_file = gf.dir_path + '\\' + gf.names[gf.file_dwnl_nr] + '.mp3'
                        gf.file_dwnl_nr += 1
                        gf.download_file(url, path_to_file)

                        # update progress bar
                        if app.window.progress['value'] < 100:
                            summ = app.window.progress['value'] + round_3(1 / gf.addresses_len * 100)
                            # print(
                            #     f"summ: {summ}, progress[value]: {app.window.progress['value']}, gf.addresses_len: {gf.addresses_len}, round_3(1 / gf.addresses_len * 100): {round_3(1 / gf.addresses_len * 100)}")
                            if summ >= 100 or gf.file_dwnl_nr == len(gf.addresses):
                                app.window.progress['value'] = 100
                                app.window.download_complete()
                            else:
                                app.window.progress['value'] = summ  # Increment the progress

                        # print(app.window.progress['value'])
                        root.update()
                app.download_window_status = False
                used_get_files = False
            root.update()
            continue
        break

    # print(app.download_window_status)


main()
