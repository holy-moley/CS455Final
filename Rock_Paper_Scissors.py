import tkinter as tk
import random
from tkinter import messagebox

class RockPaperScissorsPopup:
    def __init__(self, root=None, on_fail_callback=None):
        #Set up the Game Window 
        self.on_fail_callback = on_fail_callback #Tells launcher if loss happens
        self.choices = ["Rock", "Paper", "Scissors"]

        #Sets up Inital game Variables 
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.max_rounds = 3

        # Create window: use Toplevel 
        self.root = tk.Toplevel(root) if root else tk.Tk()
        self.root.title("Rock-Paper-Scissors")
        self.root.geometry("400x300+300+200") #Size and position
        self.root.attributes("-topmost", True)
        #Prevent closing the game window early
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)

        # UI: labels for instructions and results
        tk.Label(self.root, text="Choose Rock, Paper, or Scissors", 
                font=("Arial", 14)).pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text=self.get_score_text(), 
                                   font=("Arial", 12))
        self.score_label.pack(pady=10)

        # UI: buttons for choices #Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10) #size of button frame

        for choice in self.choices:
            tk.Button(button_frame, text=choice, width=10, font=("Arial", 12),
                     command=lambda c=choice: self.play_round(c)).pack(side="left", padx=5)

    #Prevent closing the game window early
    def disable_event(self):
        pass

    def get_score_text(self):
        #Return formatted score and round info
        return f"Round {self.rounds_played}/{self.max_rounds} - You: {self.user_score}  Computer: {self.computer_score}"

    #Start a round of the game (Called each time)
    def play_round(self, user_choice):
        if self.rounds_played >= self.max_rounds:
            return 

        # Get computer's choice using random 
        computer_choice = random.choice(self.choices)
        result_text = f"You chose {user_choice}. Computer chose {computer_choice}. "

        # Determine winner - check if choices match
        #Tie
        if user_choice == computer_choice:
            result_text += "It's a tie!"
        
        # User wins with Rock and Computer Scissors
        elif user_choice == "Rock" and computer_choice == "Scissors":
            # Rock beats Scissors
            result_text += "You win this round!"
            self.user_score += 1
        
        #User wins with Paper and Computer Rock
        elif user_choice == "Paper" and computer_choice == "Rock":
            # Paper beats Rock
            result_text += "You win this round!"
            self.user_score += 1
        
        #User wins with Scissors and Computer Paper
        elif user_choice == "Scissors" and computer_choice == "Paper":
            # Scissors beats Paper
            result_text += "You win this round!"
            self.user_score += 1
        
        # If none of the above conditions are true, the computer wins
        else:
            result_text += "Computer wins this round!"
            self.computer_score += 1

        # Update display
        self.rounds_played += 1
        self.result_label.config(text=result_text)
        self.score_label.config(text=self.get_score_text())

        # Check if game is over
        if self.rounds_played == self.max_rounds:
            self.end_game()

    #Final out come of game and reports to lancher 
    def end_game(self):
        if self.user_score > self.computer_score:
            result = f"You won the game! Final Score: {self.user_score}-{self.computer_score}"
            messagebox.showinfo("Game Over", result)

        elif self.user_score < self.computer_score:
            result = f"You lost the game! Final Score: {self.user_score}-{self.computer_score}"
            messagebox.showinfo("Game Over", result)

            # Notify launcher of loss
            if self.on_fail_callback:
                self.on_fail_callback()
        else:
            result = f"It's a tie! Final Score: {self.user_score}-{self.computer_score}"
            messagebox.showinfo("Game Over", result)

        # Close window
        self.root.destroy()



#To test the file as a single game without launcher 
def start_game(on_fail_callback=None, parent=None):
    if parent is None:
        root = tk.Tk()
        root.withdraw()
        RockPaperScissorsPopup(root=root, on_fail_callback=on_fail_callback)
        root.mainloop()
    else:
        RockPaperScissorsPopup(root=parent, on_fail_callback=on_fail_callback)

if __name__ == "__main__":
    start_game()
