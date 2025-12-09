import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import Wack_A_Mole_V3
import Number_Guessing
import Rock_Paper_Scissors
import loss #The file bomb code 

class GameLauncher:
    def __init__(self):
        # Main launcher window
        self.root = tk.Tk()
        self.root.title("Game Launcher")
        self.root.geometry("400x300+200+200")

        # Game state: lives and failure tracking
        self.lives = 3
        self.failed = False
        self.game_instances = {}
        
        # UI: title and start button
        tk.Label(self.root, text="Download Free RAM", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Download", font=("Arial", 14),
                  command=self.start_games).pack(pady=20)

        # Prevent closing the launcher
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)

    #Prevent closing the launcher window early
    def disable_event(self):
        pass

    #Start Game 
    def start_games(self):
        self.root.withdraw() #Hide the launcher window
        
        # Launch all three games
        self.mole_game = Wack_A_Mole_V3.PopupMoleGame(tk.Toplevel(self.root), on_fail_callback=self.game_failed)
        self.number_game = Number_Guessing.NumberGuessPopup(self.root, on_fail_callback=self.game_failed)
        self.rps_game = Rock_Paper_Scissors.RockPaperScissorsPopup(self.root, on_fail_callback=self.game_failed)
        
        
        
    #Close all active game windows (Variable format for each game)
    def close_all_games(self):
        # Close Whack-A-Mole popups and window, using attributes
        if hasattr(self.mole_game, 'active_popups'):
            for popup in list(self.mole_game.active_popups):
                try:
                    popup.destroy()
                except:
                    pass
        if hasattr(self.mole_game, 'root') and self.mole_game.root is not self.root:
            try:
                self.mole_game.root.destroy()
            except:
                pass
        
        # Close Number Guessing popup
        if hasattr(self.number_game, 'popup'):
            try:
                self.number_game.popup.destroy()
            except:
                pass
        
        # Close Rock-Paper-Scissors window
        if hasattr(self.rps_game, 'root') and self.rps_game.root is not self.root:
            try:
                self.rps_game.root.destroy()
            except:
                pass
        
    #Handles a loss in any of the games
    def game_failed(self):
        if self.failed:
            return  # Already processing failure
        
        self.failed = True
        self.lives -= 1
        self.close_all_games()
        
        # Check if player has lives remaining
        if self.lives > 0:
            # Show warning and restart games
            messagebox.showwarning("Strike!", 
                f"You have {self.lives} lives left! Better make 'em count.")
            self.failed = False
            self.start_games()
        else:
            # No lives left: show jumpscare and trigger penalty
            self.root.after(400, self.show_fullscreen_cat)
            loss.trigger_loss() #Trigger the bomb code

    def show_fullscreen_cat(self):
        #Put image on full screen on top of everything
        jumpscare_window = tk.Toplevel()
        jumpscare_window.attributes("-fullscreen", True)
        jumpscare_window.attributes("-topmost", True)

        # Load and display cat image
        screen_width = jumpscare_window.winfo_screenwidth()
        screen_height = jumpscare_window.winfo_screenheight()
        img = Image.open("Cat.jpeg").resize((screen_width, screen_height))
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(jumpscare_window, image=photo)
        label.image = photo
        label.pack()

        # Close jumpscare after 3 seconds
        jumpscare_window.after(3000, lambda: self.quit_all(jumpscare_window))

    #Close everything 
    def quit_all(self, window):
        window.destroy()
        try:
            self.root.quit()
        except:
            pass


if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.root.mainloop()
