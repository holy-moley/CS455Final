import tkinter as tk
import random
from tkinter import messagebox

class RockPaperScissorsPopup:
    def __init__(self, root=None, on_fail_callback=None):
        self.on_fail_callback = on_fail_callback


        # Create popup window
        # If no root provided, create one (standalone mode)
        self.standalone = False
        if root is None:
            self.root = tk.Tk() #Opens the window 
            self.standalone = True
        else:
            self.root = tk.Toplevel(root)


        #Setting the window bounds and title
        self.root.title("Rock-Paper-Scissors")
        self.root.geometry("400x300+300+200")
        self.root.attributes("-topmost", True)

        # Disable close button
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)

        # Game state
        self.choices = ["Rock", "Paper", "Scissors"]
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.max_rounds = 3  # User has 3 chances

        # Labels
        self.label = tk.Label(self.root, text="Choose Rock, Paper, or Scissors", font=("Arial", 14))
        self.label.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 12))
        self.score_label.pack(pady=10)

        # Buttons
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=10)

        for choice in self.choices:
            btn = tk.Button(self.buttons_frame, text=choice, width=10, font=("Arial", 12),
                            command=lambda c=choice: self.play_round(c))
            btn.pack(side="left", padx=5)

        #self.root.mainloop()

    def disable_event(self):
        pass  # Prevent closing

    def play_round(self, user_choice):
        if self.rounds_played >= self.max_rounds:
            return  # Game over

        # Computer randomly chooses Rock, Paper, or Scissors
        computer_choice = random.choice(self.choices)

        result_text = f"You chose {user_choice}. Computer chose {computer_choice}.\n"

        # Expanded if-then logic for clarity
        if user_choice == "Rock":
            if computer_choice == "Rock":
                result_text += "It's a tie!"
            elif computer_choice == "Paper":
                result_text += "Computer wins this round!"
                self.computer_score += 1
            elif computer_choice == "Scissors":
                result_text += "You win this round!"
                self.user_score += 1

        elif user_choice == "Paper":
            if computer_choice == "Rock":
                result_text += "You win this round!"
                self.user_score += 1
            elif computer_choice == "Paper":
                result_text += "It's a tie!"
            elif computer_choice == "Scissors":
                result_text += "Computer wins this round!"
                self.computer_score += 1

        elif user_choice == "Scissors":
            if computer_choice == "Rock":
                result_text += "Computer wins this round!"
                self.computer_score += 1
            elif computer_choice == "Paper":
                result_text += "You win this round!"
                self.user_score += 1
            elif computer_choice == "Scissors":
                result_text += "It's a tie!"

        else:
            result_text += "Invalid choice! No points awarded."

        # Update rounds played
        self.rounds_played += 1

        # Update labels
        self.result_label.config(text=result_text)
        self.score_label.config(text=self.get_score_text())

        # Check if max rounds reached
        if self.rounds_played == self.max_rounds:
            if self.user_score > self.computer_score:
                messagebox.showinfo("Game Over", f"You won the game! Final Score: {self.user_score}-{self.computer_score}")
            elif self.user_score < self.computer_score:
                # Notify loss, call the launcher's failure callback, then close.
                try:
                    messagebox.showinfo("Game Over", f"You lost the game! Final Score: {self.user_score}-{self.computer_score}")
                except:
                    pass
                # Inform launcher that a game failed (if provided)
                try:
                    if self.on_fail_callback:
                        self.on_fail_callback()
                except:
                    pass
            else:
                try:
                    messagebox.showinfo("Game Over", f"It's a tie! Final Score: {self.user_score}-{self.computer_score}")
                except:
                    pass
            # Close this game's window
            try:
                self.root.destroy()
            except:
                pass

    def get_score_text(self):
        return f"Round {self.rounds_played}/{self.max_rounds} - You: {self.user_score}  Computer: {self.computer_score}"

# ----------------------
# Top-level function for launcher
# ----------------------
def start_game(on_fail_callback=None, parent=None):
    if parent is None:
        root = tk.Tk() #OPens the start game 
        root.withdraw()  # Hide main window
        RockPaperScissorsPopup(root=root, on_fail_callback=on_fail_callback)
        root.mainloop()
    else:
        RockPaperScissorsPopup(root=parent, on_fail_callback=on_fail_callback)

        
# ----------------------
# Run standalone
# ----------------------
if __name__ == "__main__":
    start_game()
