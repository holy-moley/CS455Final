import tkinter as tk
from tkinter import messagebox
import random

class NumberGuessPopup:
    #Initialize the number guessing game popup
    def __init__(self, parent, on_fail_callback=None, number_range=(1, 10), max_attempts=3):
        self.on_fail_callback = on_fail_callback #tell lancuher if player loss
        self.number_to_guess = random.randint(*number_range) #Pick a random Number
        self.guesses_left = max_attempts #Number of guesses allowed
        self.number_range = number_range #Range of numbers to guess from

        # Create a popup window (child of parent launcher window)
        self.popup = tk.Toplevel(parent)
        self.popup.title("Number Guessing Game")
        self.popup.geometry("300x200+300+200")  # Size and position
        self.popup.attributes("-topmost", True)  # Keep on top of other windows
        self.popup.protocol("WM_DELETE_WINDOW", self.disable_event)  # Prevent closing early

        #Creation of UI Elements inside the popup window
        # Display instructions to the player inside of popUp
        tk.Label(self.popup, 
                text=f"Guess a number between {number_range[0]} and {number_range[1]}", 
                font=("Arial", 12)).pack(pady=10)

        # Input box where player types their guess
        self.entry = tk.Entry(self.popup, font=("Arial", 12))
        self.entry.pack(pady=5)

        # Submit button to process the guess
        tk.Button(self.popup, text="Submit", font=("Arial", 12), 
                 command=self.check_guess).pack(pady=10)

        # Tell user how many guesses are remaining inside window
        self.attempt_label = tk.Label(self.popup, 
                                     text=f"Guesses left: {self.guesses_left}", 
                                     font=("Arial", 12))
        self.attempt_label.pack(pady=5)

    #Prevents user from closing the game window early
    def disable_event(self):
        pass

    #Takes uswers guess and checks if correct otherwise inform user
    def check_guess(self):
        # Try to get the player's input as a number
        try:
            guess = int(self.entry.get())
        except ValueError:
            # If input is not a valid number, show error and return
            messagebox.showinfo("Invalid Input", "Please enter a valid number")
            return

        # Decrease guesses remaining
        self.guesses_left -= 1

        # Check if the guess is correct
        if guess == self.number_to_guess:
            # User wins shows in popup from a popup window
            messagebox.showinfo("Victory!", f"Correct! The number was {self.number_to_guess}")
            self.popup.destroy()
        # Check if player ran out of guesses
        elif self.guesses_left <= 0:
            # User loses
            messagebox.showinfo("Game Over", 
                              f"You ran out of guesses! The number was {self.number_to_guess}")
            self.popup.destroy()
            # Notify the launcher that this game failed
            if self.on_fail_callback:
                self.on_fail_callback()

        # Player still has guesses left - give a hint
        else:
            # Tell them if their guess is too high or too low
            if guess < self.number_to_guess:
                messagebox.showinfo("Try Again", "Too low! Guess higher!")
            else:
                messagebox.showinfo("Try Again", "Too high! Guess lower!")

            # Update remaining guesses display
            self.attempt_label.config(text=f"Guesses left: {self.guesses_left}")
            # Clear the input field for next guess to reset the entry box
            self.entry.delete(0, tk.END)


# Standalone launcher function for testing the game without the launcher
def start_game(on_fail_callback=None):
    # Create hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    NumberGuessPopup(root, on_fail_callback=on_fail_callback)
    root.mainloop() #starts game 

if __name__ == "__main__":
    start_game()

   
