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
        #Code that prevents closing the launcher window from user 
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)


    def disable_event(self):
        #prevent the closing of the launcher while the games are running
        pass

    def start_games(self):
        # Hide the launcher window
        self.root.withdraw()
        
        # Launch all games. Keep references so we can close them if one fails.
        # Pass the launcher root to games that create their own Toplevel windows
        # to avoid creating an extra blank Toplevel first.
        self.mole_game = Wack_A_Mole_V3.PopupMoleGame(tk.Toplevel(self.root), on_fail_callback=self.game_failed)
        self.number_game = Number_Guessing.NumberGuessPopup(self.root, on_fail_callback=self.game_failed)
        self.rps_game = Rock_Paper_Scissors.RockPaperScissorsPopup(self.root, on_fail_callback=self.game_failed)
        
        

    def game_failed(self):
        if not self.failed:
            self.failed = True
            # Close other game windows first. Use safe checks because some
            # games may already have destroyed themselves before calling us.
            for attr in ("mole_game", "number_game", "rps_game"):
                game = getattr(self, attr, None)
                if not game:
                    continue
                try:
                    # Wack-A-Mole keeps a list of active popups
                    if hasattr(game, 'active_popups'):
                        for p in list(getattr(game, 'active_popups', [])):
                            try:
                                p.destroy()
                            except:
                                pass
                    # Number guess stores its Toplevel in `popup`
                    if hasattr(game, 'popup'):
                        try:
                            game.popup.destroy()
                        except:
                            pass
                    # Most others expose `root` = Toplevel or Tk
                    elif hasattr(game, 'root'):
                        try:
                            # Don't destroy the launcher's main root
                            if game.root is not self.root:
                                game.root.destroy()
                        except:
                            pass
                except Exception:
                    pass

            # Give the window manager a moment to close windows, then show cat
            self.root.after(400, self.show_fullscreen_cat)

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
