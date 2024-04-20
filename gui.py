import tkinter as tk
from tkinter import ttk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
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
        ttk.Button(self, text="Pobierz", command=self.open_download_window).grid(row=2, column=1, padx=5, pady=5, sticky='e')

    def open_download_window(self):
        window = DownloadWindow(self.parent)
        window.grab_set()


class DownloadWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.title("Download Status")
        ttk.Label(self, text="Rozpoczynanie").grid(row=0, column=0, padx=5, pady=5)
        self.progress = ttk.Progressbar(self, mode='determinate', maximum=100)
        self.progress.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.cancel_button = ttk.Button(self, text="Przerwij", command=self.cancel_download)
        self.cancel_button.grid(row=2, column=0, padx=5, pady=5)

        self.start_download()

    def start_download(self):
        # This is a placeholder for starting the download and updating the progress bar
        self.update_progress()

    def update_progress(self):
        if self.progress['value'] < 100:
            self.progress['value'] += 50  # Increment the progress
            self.after(1000, self.update_progress)  # Call this method again after 1s.
        else:
            self.download_complete()

    def download_complete(self):
        ttk.Label(self, text="Zakończono").grid(row=2, column=0, padx=5, pady=5)
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
