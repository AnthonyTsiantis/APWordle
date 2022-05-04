"""
Word list sourced from GitHub: https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee 
"""

# Import all necessary libraries
from tkinter import *
import random as rand
import time as t

# Create Game Class
class Game():
    # Set up Game Class
    def __init__(self):
        self.current_row = 0 
        self.root = Tk(className=" AP Wordle") # Create tkinter object
        self.start_time = t.time() # Start game time
        # Get user screen width and height and set Gui height and width
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.GUI_HEIGHT = 725
        self.GUI_WIDTH = 500
        # Calculate position of window
        self.x = int((self.screen_width / 2) - (self.GUI_WIDTH / 2))
        self.y = int((self.screen_height / 2) - (self.GUI_HEIGHT / 2))
        self.FILE_LENGTH = 2308 # Length of file 
        self.windows = 1 # keep track of the number of windows open to prevent duplicate menu's

    # Create new Game window
    def create_new(self):
        # Reset all variable and create a new Tkinter Object
        self.current_row = 0
        self.windows = 1
        self.root.destroy()
        self.root = Tk(className=" AP Wordle")
        self.start_time = t.time() # Restart Game time

        # Set window size and position
        self.root.geometry(f"{self.GUI_WIDTH}x{self.GUI_HEIGHT}+{self.x}+{self.y}")
        self.root.configure(bg='#121212')
        self.root.resizable(False, False)

        # Set title configurations and poisition
        title = Label(self.root, text="AP Wordle", justify="center", font=("Arial", 35), bg="#121212", fg="white")
        title.grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")

        # Read file into memory
        self.file = open("words.txt", "r")
        self.file = self.file.read().splitlines() 

        # Select a random index and word
        rand_word_index = rand.randint(1, 2309)
        self.WORD = self.file[rand_word_index].strip("\n")

        # reset rows (Keeps track of all Entry widgets)
        self.rows = []
        # Create Text Entry
        for i in range(2, 8):
            entries = [] # Create list for 2D array's
            Grid.rowconfigure(self.root, i, weight=1) # Configure Row weighting
            # Iterate over columns
            for j in range(1, 6): 
                # configure column weighting
                if i == 1:
                    Grid.columnconfigure(self.root, j, weight=1)

                # Create text entry and place in grid
                entry = Entry(self.root, width=2, font=('Arial', 50, "bold"), justify="center", validatecommand=self.validate)
                entry.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                # register and configure key input validation
                reg = self.root.register(self.validate)
                entry.config(validate ="key", validatecommand=(reg, '%P'))
                # Disable all rows except first row
                if i != 2:
                    entry.config(state="disabled", disabledbackground="#a0a0a1")
                # Append all individual entries
                entries.append(entry)
            # append grouped entries
            self.rows.append(entries)

        # Focus cursor on first input
        self.rows[0][0].focus_set()
        # bind enter button to validate row function
        self.root.bind('<Return>', self.validate_row)
        # Create menu button and place on grid
        menu_button = Button(self.root, text ="Menu", font=("Arial", 20), command=self.menu)
        menu_button.grid(row=9, column=2, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Run main loop
        self.root.mainloop()
        
    # This function validates entry widgets
    def validate(self, input):
        # Length cannot be greater than 1
        if len(input) > 1:
            return False

        # Cannot be a digit
        elif input.isdigit():
            return False

        # All else is valid
        else:
            return True

    # Once enter button has been pressed, validate row and update tile color
    def validate_row(self, e):
        # Number of correct letters
        correct_counter = 0
        # Empty string fro assessing word
        string = ""

        # iterate entry widgets and concatenate into string
        for i in range(0, 5):
            string += self.rows[self.current_row][i].get().lower()

        # Make sure string is 5 characters long
        if len(string) != 5:
            # Create message label and place in grid
            message = Label(self.root, text="Word must be 5 characters long!", font=('Arial', 12, "bold"), fg="red") 
            message.grid(row=1, column=2, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Make sure string is a valid word
        elif string not in self.file:
            # Clear all entry widgets in row
            for i in range(0, 5):
                self.rows[self.current_row][i].delete(0, END)
            self.rows[self.current_row][0].focus_set() # focus on first entry
            # Create error message and place
            message = Label(self.root, text=f"Word \'{string}\' not in word list!", font=('Arial', 12, "bold"), fg="red")
            message.grid(row=1, column=2, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # String is valid
        else:
            # Iterate over each character
            for i in range(0, 5):
                current_character = self.rows[self.current_row][i].get().lower() # Get character from widget
                word_character = self.WORD[i] # get the goal word's character at that index
                # if character is in right spot
                if current_character == word_character:
                    self.rows[self.current_row][i].config(disabledbackground="#528d4d", disabledforeground="black", state="disabled") # Set tile green and disable
                    correct_counter += 1 # increment correct character counter 
                
                # if the character is in the word
                elif current_character in self.WORD:
                    self.rows[self.current_row][i].config(disabledbackground="#b59f3a", disabledforeground="black", state="disabled") # Set tile yellow and disable
                
                # Character is not in the word
                else:
                    self.rows[self.current_row][i].config(disabledbackground="#3a3a3c", disabledforeground="black", state="disabled") # Disable and set tile color grey

            # If all characters are correct
            if correct_counter == 5:
                self.end_game(True) # Call end_game function with victory

            # If not all of the characters are correct and there are more rows
            elif correct_counter != 5 and self.current_row != 5:
                correct_counter = 0 # reset correct character count
                self.open_next_row() # open the next row
            
            # If not all characters are correct and no more rows
            else:
                self.end_game(False) # end game with failure


    # Once a row has been validated disable it and enable the next
    def open_next_row(self):
        self.current_row += 1 # Increment current row
        # Iterate over each cell and enable it
        for i in range(0, 5):
            self.rows[self.current_row][i].config(state="normal")
        
        # Focus on the first cell in the row
        self.rows[self.current_row][0].focus_set()

    # Handle window closing
    def on_closing(self):
        self.menu_window.destroy() # Close menu window
        self.windows -= 1 # decrement window counter

    # Create Instruction Menu 
    def menu(self):
        self.windows += 1 # Increment window counter

        # if there are less than three windows
        if self.windows < 3:
            self.menu_window = Toplevel(self.root) # Create Tkinter Menu object
            self.menu_window.title("Menu") # Change its title
            # Get user screen width and height and set Gui height and width
            self.MENU_HEIGHT = 350
            self.MENU_WIDTH = 500
            # Calculate position of window
            x = int((self.screen_width / 2) - (self.MENU_WIDTH / 2)) + 500 # Add displacement to place beside
            y = int((self.screen_height / 2) - (self.MENU_HEIGHT / 2))
            # Configure window position and details
            self.menu_window.geometry(f"{self.MENU_WIDTH}x{self.MENU_HEIGHT}+{(self.x + 500)}+{self.y}")
            self.menu_window.configure(bg='#121212')
            self.menu_window.resizable(False, False)
            self.menu_window.protocol("WM_DELETE_WINDOW", self.on_closing)

            # Create Menu title and display on screen
            title = Label(self.menu_window, text="Instructions", font=('Arial', 25, "bold"), fg="#b59f3a", bg="#121212")
            title.pack(padx=10, pady=10)
            
            # Create instruction text area and display on screen
            instructions_text = """You have 6 guesses to get the AP WORDLE. To begin, enter your 
first letter in the first box of the first row. You may tab over to the 
next box or click any of the boxes on the first row. Once you have filled 
out an entire row, hit the enter key to submit your guess. Each guess 
must be a valid five-letter word. After each guess, the color of the 
tiles will change to show how close your guess was to the word. If the 
tile is grey, the letter you guessed is not in the word. If the tile is 
yellow, the letter you guessed is in the word, just not in that position. 
If the tile is green, the letter is in the word, in that position. This 
game is NOT case sensitive."""
            instructions = Text(self.menu_window, height=12, width=75, font=("Arial", 12), fg="white", bg="#121212", padx=10, pady=10)
            instructions.insert(END, instructions_text)
            instructions.pack()

            restart_button = Button(self.menu_window, text ="Restart Game", command=self.create_new, font=("Arial", 12))
            restart_button.pack()


    # Create Victory/Loss Menu 
    def end_game(self, won):
        # Create instance of menu
        self.end_game_menu = Toplevel(self.root)
        # Get user screen width and height and set Gui height and width
        self.MENU_HEIGHT = 350
        self.MENU_WIDTH = 500
        # Calculate position of window
        x = int((self.screen_width / 2) - (self.MENU_WIDTH / 2))
        y = int((self.screen_height / 2) - (self.MENU_HEIGHT / 2))
        # Configure window position and details
        self.end_game_menu.geometry(f"{self.MENU_WIDTH}x{self.MENU_HEIGHT}+{self.x}+{self.y}")
        self.end_game_menu.configure(bg='#121212')
        self.end_game_menu.resizable(False, False)
        self.end_game_menu.columnconfigure(0, weight=1)
        self.end_game_menu.rowconfigure(0, weight=1)

        # End timer
        complete_time = t.time() - self.start_time

        # Create Title, Timer, and answer labels
        title = Label(self.end_game_menu, bg="#121212")
        title.grid(column=0, row=0, pady=25)
        time = Label(self.end_game_menu, text=f"Time: {round(complete_time, 2)} seconds", font=('Arial', 25, "bold"), fg="white", bg="#121212")
        time.grid(column=0, row=1, pady=25)
        word = Label(self.end_game_menu, text=f"Word: {self.WORD.upper()}", font=('Arial', 25, "bold"), fg="white", bg="#121212")
        word.grid(column=0, row=2, pady=25)

        # if game is won display victory text and title
        if won:
            self.end_game_menu.title("Victory!!!")
            title.config(text="Victory!!!", fg="#528d4d", font=('Arial', 50, "bold"))

        # Else display loss
        else:
            self.end_game_menu.title("Better luck next time.")
            title.config(text="Better luck next time.", fg="red", font=('Arial', 35, "bold"))

# When the program is run, create a new Game object and create a new game using create_new method
if __name__ == "__main__":
    game = Game()
    game.create_new()