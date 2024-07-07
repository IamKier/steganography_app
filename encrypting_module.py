import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import random
import string
from steganography import Steganography

class EncryptingModule(ttk.Frame):
    def __init__(self, parent, go_back_callback):
        super().__init__(parent)

        self.parent = parent
        self.go_back_callback = go_back_callback
        self.steganography = Steganography()

        ttk.Label(self, text="Encrypt Image", font=("Arial", 16, "bold")).pack(pady=10)

        encrypt_form = ttk.Frame(self)
        encrypt_form.pack(pady=10)

        self.image_path_var = tk.StringVar()
        self.hidden_text_var = tk.StringVar()

        ttk.Label(encrypt_form, text="Image File:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Entry(encrypt_form, textvariable=self.image_path_var, state='disabled', width=50).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(encrypt_form, text="Browse", command=self.browse_image).grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(encrypt_form, text="Hidden Text:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        ttk.Entry(encrypt_form, textvariable=self.hidden_text_var, width=50).grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self, text="Encrypt Image", command=self.encrypt_image).pack(pady=10)

        ttk.Label(self, text="Encrypted Image:", font=("Arial", 12)).pack(pady=10)
        self.encrypted_image_label = ttk.Label(self)
        self.encrypted_image_label.pack()

        ttk.Button(self, text="Download Encrypted Image", command=self.download_encrypted_image).pack(pady=10)
        ttk.Button(self, text="Back to Home", command=self.go_back).pack(pady=20)

    def browse_image(self):
        file_types = [("Image files", "*.jpg;*.jpeg;*.png")]
        image_path = filedialog.askopenfilename(filetypes=file_types)
        if image_path:
            self.image_path_var.set(image_path)

    def encrypt_image(self):
        image_path = self.image_path_var.get()
        hidden_text = self.hidden_text_var.get()

        if not image_path:
            messagebox.showerror("Error", "Please select an image.")
            return

        if not hidden_text:
            messagebox.showerror("Error", "Please enter the text to hide.")
            return

        encrypted_image_path = self.steganography.perform_encryption(image_path, hidden_text)

        if encrypted_image_path:
            img = Image.open(encrypted_image_path)
            img = img.resize((400, 300))  # Resize image if necessary
            img = ImageTk.PhotoImage(img)
            self.encrypted_image_label.config(image=img)
            self.encrypted_image_label.image = img  # Keep a reference to prevent garbage collection
            self.encrypted_image_path = encrypted_image_path

    def download_encrypted_image(self):
        if not hasattr(self, 'encrypted_image_path'):
            messagebox.showerror("Error", "No encrypted image available to download.")
            return

        download_folder = filedialog.askdirectory()

        if not os.path.exists(download_folder):
            messagebox.showerror("Error", f"Download folder '{download_folder}' does not exist.")
            return

        image_name = os.path.basename(self.encrypted_image_path)
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        download_path = os.path.join(download_folder, f"{random_filename}_{image_name}")

        try:
            os.rename(self.encrypted_image_path, download_path)
            messagebox.showinfo("Download", f"Encrypted image downloaded as {download_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download image: {str(e)}")

    def go_back(self):
        self.destroy()  # Destroy current frame (encrypting module)
        self.go_back_callback()  # Call back to go back to main application page
