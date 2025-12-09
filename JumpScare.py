import tkinter as tk
from PIL import Image, ImageTk

def show_cat_jump_scare():
    top = tk.Toplevel()
    top.attributes("-fullscreen", True)
    top.attributes("-topmost", True)

    try:
        img = Image.open("Cat.jpeg")
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img = img.resize((screen_width, screen_height))
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(top, image=photo)
        label.image = photo
        label.pack()
    except Exception:
        # fallback if image not found
        tk.Label(top, text="MEOW!", font=("Arial", 100)).pack(expand=True)

    # Close the jump scare after 3 seconds
    top.after(3000, top.destroy)
