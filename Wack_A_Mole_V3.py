import tkinter as tk
from PIL import Image, ImageTk
import random
import time
from loss import trigger_loss #The file Bomb will need to fix 

# Game settings
POPUP_LIFETIME = 2500  # ms popup stays
POPUP_INTERVAL = 1500  # ms between popup refresh
WIN_HITS = 5
GAME_DURATION = 20     # seconds
OTHER_ANIMALS = ["rat.jpeg", "squirrel2.jpeg", "racoon2.jpeg"]

class PopupMoleGame:
    def __init__(self, root, on_fail_callback=None):
        self.root = root
        self.root.title("Popup Whack-a-Mole")
        
        self.root.geometry("300x200+0+0") #width x height + x_offset + y_offset
        self.root.attributes("-topmost", True) #Put item in leftmost conorer and on top

        #Code to have the game be called only from other file 
        #Code for the launcher file to work 
        self.on_fail_callback = on_fail_callback

        #Game Variables func. 
        self.score = 0
        self.running = False
        self.remaining_time = GAME_DURATION

        # Load images
        self.mole_img = ImageTk.PhotoImage(Image.open("mole.jpeg").resize((100, 100)))
        self.animal_imgs = []
        for img_file in OTHER_ANIMALS:
            img = Image.open(img_file).resize((100, 100))
            self.animal_imgs.append(ImageTk.PhotoImage(img))

        # UI
        self.score_label = tk.Label(root, text=f"Moles Hit: {self.score}/{WIN_HITS}", font=("Arial", 16))
        self.score_label.pack(pady=5)

        self.timer_label = tk.Label(root, text=f"Time Left: {self.remaining_time}s", font=("Arial", 16))
        self.timer_label.pack(pady=5)

        self.start_btn = tk.Button(root, text="Start Game", font=("Arial", 14), command=self.start_game)
        self.start_btn.pack(pady=10)

        self.status_label = tk.Label(root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        # Keep track of active popups
        self.active_popups = []


    # ----------------------
    # Start Game
    # ----------------------
    def start_game(self):
        if self.running:
            return
        self.score = 0
        self.remaining_time = GAME_DURATION
        self.running = True
        self.update_score()
        self.update_timer()
        self.status_label.config(text="Click the mole 5 times to win!")

        # Start popup cycle
        self.spawn_popups()

    # ----------------------
    # Spawn Popups
    # ----------------------
    def spawn_popups(self):
        if not self.running:
            return

        # Close previous popups
        for popup in self.active_popups:
            try:
                popup.destroy()
            except:
                pass
        self.active_popups.clear()

        num_popups = random.randint(3, 5)
        mole_position = random.randint(0, num_popups - 1)
        positions = []

        for i in range(num_popups):
            # Find non-overlapping position
            while True:
                x = random.randint(100, 700)
                y = random.randint(100, 500)
                overlap = False
                for px, py in positions:
                    if abs(x - px) < 130 and abs(y - py) < 130:
                        overlap = True
                        break
                if not overlap:
                    positions.append((x, y))
                    break

            popup = tk.Toplevel(self.root)
            popup.geometry(f"120x120+{x}+{y}")
            popup.attributes("-topmost", True)

            if i == mole_position:
                btn = tk.Button(popup, image=self.mole_img, command=lambda w=popup: self.hit_mole(w))
            else:
                img = random.choice(self.animal_imgs)
                btn = tk.Button(popup, image=img, command=lambda px=x, py=y: self.hit_wrong(px, py))
            btn.pack(expand=True, fill="both")
            popup.after(POPUP_LIFETIME, popup.destroy)

            self.active_popups.append(popup)

        # Schedule next popup cycle
        self.root.after(POPUP_INTERVAL, self.spawn_popups)

   # ----------------------
    # Mole clicked
    # ----------------------
    def hit_mole(self, window):
        try:
            window.destroy()
        except:
            pass
        self.score += 1
        self.update_score()
        if self.score >= WIN_HITS:
            self.running = False
            self.status_label.config(text="You Win!")
            # Notify the player, then clean up: destroy any remaining popup
            # windows and close this game's main window so it doesn't linger.
            try:
                tk.messagebox.showinfo("Victory!", "You bonked the Mole")
            except:
                pass
            
            #make the window close properly if the game has won 
            # Destroy any active popup windows
            try:
                for p in list(getattr(self, 'active_popups', [])):
                    try:
                        p.destroy()
                    except:
                        pass
                self.active_popups.clear()
            except:
                pass

            # Close the game's main window (safe-guard in case it's a Toplevel)
            try:
                if hasattr(self, 'root') and self.root is not None:
                    self.root.destroy()
            except:
                pass
    # ----------------------
    # Wrong animal clicked
    # ----------------------
    def hit_wrong(self, x, y):
        ouch_popup = tk.Toplevel(self.root)
        ouch_popup.geometry(f"100x50+{x+50}+{y+50}")
        ouch_popup.attributes("-topmost", True)
        tk.Label(ouch_popup, text="Ouch!", font=("Arial", 14), fg="red").pack(expand=True, fill="both")
        ouch_popup.after(1000, ouch_popup.destroy)

    # ----------------------
    # Update score label
    # ----------------------
    def update_score(self):
        self.score_label.config(text=f"Moles Hit: {self.score}/{WIN_HITS}")

    # ----------------------
    # Countdown timer
    # ----------------------
    def update_timer(self):
        if not self.running:
            return
        if self.remaining_time <= 0:
            self.running = False
            self.status_label.config(text="Time's up! Game Over")
            
            #Current file Bomb loaction (might move to lancher file)
            #was Here ................
            if self.on_fail_callback:
                self.on_fail_callback() 
            self.root.destroy() #Close mole game window

            tk.messagebox.showinfo("Game Over", f"Time ran out! You hit {self.score} moles.")
            return
        

        self.timer_label.config(text=f"Time Left: {self.remaining_time}s")
        self.remaining_time -= 1
        self.root.after(1500, self.update_timer)


# ----------------------
# Top-level function for launcher (run when lanuchers dose it)
# ----------------------
def start_game(on_fail_callback=None):
    root = tk.Tk() #Creates the window #--------------------------------Problem -------------------------
    game = PopupMoleGame(root, on_fail_callback=on_fail_callback)
    root.mainloop()


# ----------------------
# Run standalone For testing purposes of just the mole game 
# ----------------------
if __name__ == "__main__":
    start_game()
