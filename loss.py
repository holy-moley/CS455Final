# loss.py
import os

def trigger_loss():
    """Creates 15 'You Lose' files on the Desktop."""
    #Find desktop path, works for windows or most linux distros
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    
    try:
        for x in range (14):
            name = str(x) + "_loss.txt"
            file_path = os.path.join(desktop_path, name)
            with open(file_path, "w") as f:
                f.write("You lose!")
                f.write(str(x))
            print(f"Penalty executed. File created at: {file_path}")
    except Exception as e:
        print(f"Error creating penalty file: {e}")

# This allows you to test this file by running it directly
if __name__ == "__main__":
    print("Testing penalty module...")
    trigger_loss()