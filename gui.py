import tkinter as tk
from tkinter import ttk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
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
        ttk.Button(self, text="Exit", command=self.parent.quit).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self, text="Pobierz", command=self.verify_user_input).grid(row=2, column=1, padx=5, pady=5,
                                                                              sticky='e')

    def verify_user_input(self):
        # TODO POBIERZ BUTTON
        # funkcja sprawdzajaca oba inputy usera i jezeli jest git to wtedy open download window i rozpocznij pobieranie
        if True:
            self.open_download_window()

    def open_download_window(self):
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

    def start_download(self, num_of_files):
        # This is a placeholder for starting the download and updating the progress bar
        self.update_progress(num_of_files)

    def update_progress(self, divider):
        if self.progress['value'] < 100:
            self.progress['value'] += 100/divider  # Increment the progress
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
