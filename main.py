import tkinter as tk
from tkinter import ttk
from encrypting_module import EncryptingModule
from decrypting_module import DecryptingModule

class SteganographyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Steganography App")
        self.geometry("800x600")  # Set initial window size

        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.init_main_page()

    def init_main_page(self):
        ttk.Label(self.container, text="Steganography App", font=("Arial", 24, "bold")).pack(pady=20)

        ttk.Button(self.container, text="Encrypt Image", command=self.show_encrypting_module).pack(pady=10)
        ttk.Button(self.container, text="Decrypt Image", command=self.show_decrypting_module).pack(pady=10)

    def show_encrypting_module(self):
        self.clear_container()
        encrypting_module = EncryptingModule(self.container, self.show_main_page)
        encrypting_module.pack(fill=tk.BOTH, expand=True)

    def show_decrypting_module(self):
        self.clear_container()
        decrypting_module = DecryptingModule(self.container, self.show_main_page)
        decrypting_module.pack(fill=tk.BOTH, expand=True)

    def show_main_page(self):
        self.clear_container()
        self.init_main_page()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = SteganographyApp()
    app.mainloop()
