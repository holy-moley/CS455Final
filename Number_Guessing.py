import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessPopup:
    def __init__(self, parent, on_fail_callback=None, number_range=(1, 10), max_attempts=3):
        #self.root = root
        
        self.on_fail_callback = on_fail_callback
        self.number_to_guess = random.randint(*number_range)
        self.guesses_left = max_attempts

        # Use Toplevel instead of Tk
        self.popup = tk.Toplevel(parent)


        self.popup.title("Number Guessing Game")
        self.popup.geometry("300x200+300+200")
        self.popup.attributes("-topmost", True)

        # Disable close button
        self.popup.protocol("WM_DELETE_WINDOW", self.disable_event)

        # Instruction label
        self.label = tk.Label(self.popup, text=f"Guess a number between {number_range[0]} and {number_range[1]}", font=("Arial", 12))
        self.label.pack(pady=10)

        # Entry field
        self.entry = tk.Entry(self.popup, font=("Arial", 12))
        self.entry.pack(pady=5)

        # Submit button
        self.submit_btn = tk.Button(self.popup, text="Submit", font=("Arial", 12), command=self.check_guess)
        self.submit_btn.pack(pady=10)

        # Attempts left
        self.attempt_label = tk.Label(self.popup, text=f"Guesses left: {self.guesses_left}", font=("Arial", 12))
        self.attempt_label.pack(pady=5)

    # Prevent closing
    def disable_event(self):
        pass

    # Check user guess
    def check_guess(self):
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter a valid number")
            return

        self.guesses_left -= 1

        if guess == self.number_to_guess:
            messagebox.showinfo("Victory!", f"Correct! The number was {self.number_to_guess}")
            self.popup.destroy()
        elif self.guesses_left <= 0:
            messagebox.showinfo("Game Over", f"You ran out of guesses! The number was {self.number_to_guess}")
            self.popup.destroy()
            # Trigger launcher fail callback
            if self.on_fail_callback:
                self.on_fail_callback()
        else:
            if guess < self.number_to_guess:
                messagebox.showinfo("Try Again", "Too low! Guess higher!")
            else:
                messagebox.showinfo("Try Again", "Too high! Guess lower!")
            self.attempt_label.config(text=f"Guesses left: {self.guesses_left}")
            self.entry.delete(0, tk.END)

# ----------------------
# Top-level function for launcher
# ----------------------
def start_game(on_fail_callback=None):
    # Use the launcher root
    from tkinter import _default_root as root
    if root is None:
        root = tk.Tk()
    NumberGuessPopup(root, on_fail_callback=on_fail_callback)

# ----------------------
# Run standalone
# ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window the frist one
    NumberGuessPopup(root)
    root.mainloop()
