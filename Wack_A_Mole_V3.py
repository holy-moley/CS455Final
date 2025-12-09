#imports 
import tkinter as tk #GUI
from tkinter import messagebox #POpups form a popUp
from PIL import Image, ImageTk #Images in GUI/Python
import random

# Game settings [Constants for Game Difficulty]
POPUP_LIFETIME = 2500  # milliseconds each popup shows
POPUP_INTERVAL = 1500  # milliseconds between spawn cycles
WIN_HITS = 5           # moles needed to win
GAME_DURATION = 20     # seconds to play game
OTHER_ANIMALS = ["rat.jpeg", "squirrel2.jpeg", "racoon2.jpeg"]


class PopupMoleGame:
    #python equivalent of main 
    def __init__(self, root, on_fail_callback=None):
        """Initialize the Whack-A-Mole game."""
        self.root = root #Makes the Game Window 
        self.on_fail_callback = on_fail_callback #Callback function on failure
        self.running = False #Game running state
        self.score = 0 #Player score
        self.remaining_time = GAME_DURATION #Time left in game
        self.active_popups = [] #List of active popup windows for game 

        # Setup window
        self.root.title("Popup Whack-a-Mole")
        self.root.geometry("300x200+0+0") #Window size and position
        self.root.attributes("-topmost", True) #Force window in top left corner

        # Load game images of animals and resize them 
        self.mole_img = ImageTk.PhotoImage(Image.open("mole.jpeg").resize((100, 100)))
        self.animal_imgs = []
        for filename in OTHER_ANIMALS:
            img = Image.open(filename).resize((100, 100))
            self.animal_imgs.append(ImageTk.PhotoImage(img))

        #Making of Clickable Buttons and 'text' for the Game
        # UI: score display 
        self.score_label = tk.Label(root, text=f"Moles Hit: {self.score}/{WIN_HITS}",
                                   font=("Arial", 16))
        self.score_label.pack(pady=5)

        # UI: timer display
        self.timer_label = tk.Label(root, text=f"Time Left: {self.remaining_time}s",
                                   font=("Arial", 16))
        self.timer_label.pack(pady=5)

        # UI: start button
        tk.Button(root, text="Start Game", font=("Arial", 14),
                 command=self.start_game).pack(pady=10)

        # UI: status message
        self.status_label = tk.Label(root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

    #Methoed once called will start the game 
    def start_game(self):

        if self.running: #Statement to ensure game only runs once
            return
        
        self.score = 0 #Users inital starting score
        self.remaining_time = GAME_DURATION #Reset timer to full duration
        self.running = True #Set game state to running

        self.status_label.config(text="Click the mole 5 times to win!")
        #Update functions to call 
        self.update_score()
        self.update_timer()
        self.spawn_popups()

    def spawn_popups(self):
        #Create random mole and animal popups.
        if not self.running:
            return

        # Clear old popups
        for popup in self.active_popups:
            try:
                popup.destroy() #How to delete a pop-up window 
            except:
                pass
        self.active_popups.clear()

        # Create 3-5 random popups with one mole
        num_popups = random.randint(3, 5)
        #Choses one window that will have the mole
        mole_idx = random.randint(0, num_popups - 1)
        used_positions = []

        #How all the window run through the game 
        for i in range(num_popups):
            # Find non-overlapping position
            while True:
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                #Code to actally prevent the overlapping of pop-ups
                overlap = any(abs(x - px) < 130 and abs(y - py) < 130
                             for px, py in used_positions)
                if not overlap:
                    used_positions.append((x, y))
                    break

            # Create popup window for animals 
            popup = tk.Toplevel(self.root) #Makes a new window that is not a parent
            popup.geometry(f"120x120+{x}+{y}") #Size and position of popup
            popup.attributes("-topmost", True)

            # when mole is hit code or wrong animal is hit code
            if i == mole_idx:
                btn = tk.Button(popup, image=self.mole_img,
                               command=lambda w=popup: self.hit_mole(w))
            else:
                img = random.choice(self.animal_imgs)
                btn = tk.Button(popup, image=img,
                               command=lambda px=x, py=y: self.hit_wrong(px, py))
            btn.pack(expand=True, fill="both")

            # Auto-close popUp window after a few seconds 
            popup.after(POPUP_LIFETIME, lambda p=popup: self._safe_destroy(p))
            self.active_popups.append(popup)

        # Schedule next spawn cycle
        self.root.after(POPUP_INTERVAL, self.spawn_popups)

    #Function for when mole is hit 
    def hit_mole(self, window):
        self._safe_destroy(window) #Close the mole hit window when clicked
        self.score += 1 #Increase score by 1
        self.update_score() #Call the update score method

        #Win condition check / Player has hit 5 moles
        if self.score >= WIN_HITS: 
            self.running = False
            self.status_label.config(text="You Win!")
            messagebox.showinfo("Victory!", "You bonked the Mole")
            self.cleanup()

    #Show an ouch popup when wrong animal is hit
    def hit_wrong(self, x, y):
        ouch = tk.Toplevel(self.root)
        ouch.geometry(f"100x50+{x+50}+{y+50}") #Shows popup window near wrong clicked animal 
        ouch.attributes("-topmost", True)
        tk.Label(ouch, text="Ouch!", font=("Arial", 14), fg="red").pack(expand=True, fill="both")
        ouch.after(1000, lambda: self._safe_destroy(ouch)) #Auto close the window after a second

    #Update user score when clicked on parent window
    def update_score(self):
        self.score_label.config(text=f"Moles Hit: {self.score}/{WIN_HITS}")

    #Timer count down 
    def update_timer(self):
        if not self.running:
            return

        #When time runs out meaning player lost 
        if self.remaining_time <= 0:
            self.running = False 

            self.status_label.config(text="Time's up! Game Over")
            messagebox.showinfo("Game Over", f"Time ran out! You hit {self.score} moles.")
            
            if self.on_fail_callback:
                self.on_fail_callback() #Tells launcher file game is a loss
            self.cleanup() #calls cleanup method to close all windows
            return

        # Update display and schedule next tick
        self.timer_label.config(text=f"Time Left: {self.remaining_time}s")
        self.remaining_time -= 1 #Makes time go down by 1 second
        self.root.after(1500, self.update_timer) #Game Speed 

    #Method to close all windows and pop-ups win or lose 
    def cleanup(self):
        for popup in list(self.active_popups):
            self._safe_destroy(popup) #Close any active pop-up windows
        self.active_popups.clear() #Empty list of active popups
        self._safe_destroy(self.root) #Close main game window automically

    #Method to catch any window if not already close (Error testing)
    def _safe_destroy(self, window):
        try:
            window.destroy()
        except:
            pass

#File only runable game for testing purposes
def start_game(on_fail_callback=None):
    root = tk.Tk()
    root.withdraw()
    PopupMoleGame(root, on_fail_callback=on_fail_callback)
    root.mainloop()


if __name__ == "__main__":
    start_game()
