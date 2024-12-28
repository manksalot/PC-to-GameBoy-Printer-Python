from Print_Image import print_image, feed
import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

# Determine the path to the icon file
if getattr(sys, 'frozen', False):
    # If the application is frozen (running as an executable)
    icon_path = os.path.join(sys._MEIPASS, 'gameboy.ico')
else:
    # If the application is running in a normal Python environment
    icon_path = os.path.join(os.path.dirname(__file__), 'gameboy.ico')

class ImagePrinterApp:
    def __init__(self, root):
        global icon_path
        self.root = root
        self.root.title("PC to Gameboy Printer")
        self.root.geometry("500x500")

        # Set the icon
        self.root.iconbitmap(icon_path)

        # Define dark mode color scheme
        self.dark_mode = {
            "bg": "#2E2E2E",
            "fg": "white",
            "button_bg": "#4A4A4A",
            "button_fg": "white",
            "note_bg": "#2E2E2E",
            "note_fg": "white"
        }

        # Apply dark mode colors
        self.apply_colors()

        # Create a label to display the image
        self.image_label = tk.Label(root, bg=self.dark_mode["bg"], fg=self.dark_mode["fg"])
        self.image_label.pack(pady=10)

        # Create a frame to hold the message label
        self.message_frame = tk.Frame(root, bg=self.dark_mode["bg"])
        self.message_frame.pack(side=tk.BOTTOM, pady=(0, 5))

        # Create a note label above the buttons
        self.note_label = tk.Label(self.message_frame, text="NOTE: import only .png, .jpg, .jpeg, .bmp or .gif", font=("Arial", 12), bg=self.dark_mode["note_bg"], fg=self.dark_mode["note_fg"])
        self.note_label.pack()

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(root, bg=self.dark_mode["bg"])
        self.button_frame.pack(side=tk.BOTTOM, pady=10)

        # Create buttons
        self.select_button = tk.Button(self.button_frame, text="Select Image", command=self.select_image, bg=self.dark_mode["button_bg"], fg=self.dark_mode["button_fg"])
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.feed_button = tk.Button(self.button_frame, text="Feed", command=self.feedpaper, bg=self.dark_mode["button_bg"], fg=self.dark_mode["button_fg"])
        self.feed_button.pack(side=tk.LEFT, padx=5)

        self.print_button = tk.Button(self.button_frame, text="Print", command=self.print_image, bg=self.dark_mode["button_bg"], fg=self.dark_mode["button_fg"])
        self.print_button.pack(side=tk.LEFT, padx=5)

        self.image_path = None

    def apply_colors(self):
        # Set the background color for the root window
        self.root.configure(bg=self.dark_mode["bg"])

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if self.image_path:
            self.display_image()

    def display_image(self):
        try:
            image = Image.open(self.image_path)
            image.thumbnail((400, 400), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def print_image(self):
        if self.image_path:
            try:
                messagebox.showinfo("Print", f"Printing {self.image_path}...")
                print_image(self.image_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to print image: {e}")
        else:
            messagebox.showwarning("Warning", "No image selected!")

    def feedpaper(self):
        try:
            feed()
            messagebox.showinfo("Feed", "Paper fed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to feed paper: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImagePrinterApp(root)
    root.mainloop()