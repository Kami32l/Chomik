import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class MainApplication(tk.Frame):
    def __init__(self, parent, verify_input, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.closing_app = False
        self.download_window_status = False
        self.folder = None
        self.url = None
        self.parent = parent
        self.verify_input = verify_input
        self.setup_window_position()
        self.setup_ui()

    def setup_window_position(self):
        # Setup window position
        self.window_height = 100
        self.window_width = 225
        self.x_pos = (self.parent.winfo_screenwidth() / 2) - (self.window_width / 2)
        self.y_pos = (self.parent.winfo_screenheight() / 2) - (self.window_height / 2)
        self.parent.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, self.x_pos, self.y_pos))

    def setup_ui(self):
        self.parent.title('Chomik')

        self.grid()

        # Row 0: URL Entry
        ttk.Label(self, text="URL:").grid(row=0, column=0, padx=5, pady=5)
        self.url_entry = ttk.Entry(self)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Row 1: Folder Entry
        ttk.Label(self, text="Folder:").grid(row=1, column=0, padx=5, pady=5)
        self.folder_entry = ttk.Entry(self)
        self.folder_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Row 2: Buttons
        ttk.Button(self, text="Exit", command=self.exit_app).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self, text="Pobierz", command=self.verify_user_input).grid(row=2, column=1, padx=5, pady=5,
                                                                              sticky='e')

    def exit_app(self):
        self.closing_app = True
        self.parent.quit()

    def verify_user_input(self):
        # TODO POBIERZ BUTTON
        # funkcja sprawdzajaca oba inputy usera i jezeli jest git to wtedy open download window i rozpocznij pobieranie

        self.url = self.url_entry.get()
        self.folder = self.folder_entry.get()
        input_check_response = self.verify_input(self.url, self.folder)
        if input_check_response == 1:
            self.open_download_window()
        else:
            if input_check_response == 3:
                message_text = 'Nieprawidłowy url'
            else:
                message_text = 'Nieprawidłowa nazwa folderu.'
            messagebox.showinfo(message=message_text)

    def open_download_window(self):
        self.download_window_status = True
        window = DownloadWindow(self.parent)
        window.grab_set()


class DownloadWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_window_position(parent)
        self.setup_ui()

    def setup_window_position(self, root):
        self.x = root.winfo_x()
        self.y = root.winfo_y()
        self.geometry("+%d+%d" % (self.x - 50, self.y))

    def setup_ui(self):
        self.title("Download Status")
        self.labelvar = tk.StringVar()
        self.labelvar.set('Pobieranie')
        self.status_label = ttk.Label(self, textvariable=self.labelvar).grid(row=0, column=0, padx=5, pady=5)
        self.progress = ttk.Progressbar(self, mode='determinate', maximum=100, length=320)
        self.progress.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.cancel_button = ttk.Button(self, text="Przerwij", command=self.cancel_download)
        self.cancel_button.grid(row=2, column=0, padx=5, pady=5)

    def update_progress(self, divider):
        if self.progress['value'] < 100:
            summ = self.progress['value'] + round(100 / divider)
            if summ >= 100:
                self.progress['value'] = 100
            else:
                self.progress['value'] = summ  # Increment the progress
            # self.after(1000, self.update_progress)  # Call this method again after 1s.
        else:
            self.download_complete()

    def download_complete(self):
        self.labelvar.set('Zakończono')
        self.cancel_button.config(text="Zamknij", command=self.destroy)
        self.cancel_button.grid(row=3, column=0, padx=5, pady=5)

    def cancel_download(self):
        # Placeholder for canceling the download logic
        self.destroy()


def main():
    root = tk.Tk()

    app = MainApplication(root)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
