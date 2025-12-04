import tkinter as tk
from PIL import Image, ImageTk
import Wack_A_Mole_V3
import Number_Guessing
import Rock_Paper_Scissors

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        #This line of code cause problems with main window opening
        #self.root.withdraw()  # Hide main window (1st one for la)

        self.root.title("Game Launcher")
        self.root.geometry("400x300+200+200")

        tk.Label(self.root,
                 text="Download Free RAM",
                 font=("Arial", 16)).pack(pady=20)

        tk.Button(self.root, text="Download", font=("Arial", 14),
                  command=self.start_games).pack(pady=20)

        self.failed = False
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)

    def disable_event(self):
        pass

    def start_games(self):
        # Hide the launcher window
        self.root.withdraw()

        # Launch all games on Toplevel windows
        Wack_A_Mole_V3.PopupMoleGame(tk.Toplevel(self.root), on_fail_callback=self.game_failed)
        Number_Guessing.NumberGuessPopup(tk.Toplevel(self.root), on_fail_callback=self.game_failed)
        Rock_Paper_Scissors.RockPaperScissorsPopup(tk.Toplevel(self.root), on_fail_callback=self.game_failed)

    def game_failed(self):
        if not self.failed:
            self.failed = True
            self.show_fullscreen_cat()

    def show_fullscreen_cat(self):
        top = tk.Toplevel()
        top.attributes("-fullscreen", True)
        top.attributes("-topmost", True)

        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        img = Image.open("Cat.jpeg").resize((screen_width, screen_height))
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(top, image=photo)
        label.image = photo
        label.pack()

        top.after(3000, lambda: self.quit_all(top))

    def quit_all(self, top):
        top.destroy()
        try:
            tk._default_root.quit()
        except:
            pass

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.root.mainloop()
