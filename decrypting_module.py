import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

from encrypting_module import Steganography

class DecryptingModule(ttk.Frame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent)

        self.parent = parent
        self.go_back_callback = go_back_callback

        self.steganography = Steganography()

        ttk.Label(self, text="Decrypt Image", font=("Arial", 16, "bold")).pack(pady=10)

        decrypt_form = ttk.Frame(self)
        decrypt_form.pack(pady=10)

        self.image_path_var = tk.StringVar()
        ttk.Label(decrypt_form, text="Image File:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Entry(decrypt_form, textvariable=self.image_path_var, state='disabled', width=50).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(decrypt_form, text="Browse", command=self.browse_image).grid(row=0, column=2, padx=10, pady=5)

        ttk.Button(self, text="Decrypt Image", command=self.decrypt_image).pack(pady=10)

        self.decrypted_message_label = ttk.Label(self, text="", wraplength=600, justify='center', font=("Arial", 14))
        self.decrypted_message_label.pack(pady=20)

        ttk.Button(self, text="Back to Home", command=self.go_back).pack(pady=20)

    def browse_image(self):
        file_types = [("Image files", "*.jpg;*.jpeg;*.png")]
        image_path = filedialog.askopenfilename(filetypes=file_types)
        if image_path:
            self.image_path_var.set(image_path)

    def decrypt_image(self):
        image_path = self.image_path_var.get()

        if not image_path:
            messagebox.showerror("Error", "Please select an image.")
            return

        hidden_text = self.steganography.perform_decryption(image_path)

        self.decrypted_message_label.config(text=hidden_text)

    def go_back(self):
        self.destroy()  # Destroy current frame (decrypting module)
        self.go_back_callback()  # Call back to go back to main application page
