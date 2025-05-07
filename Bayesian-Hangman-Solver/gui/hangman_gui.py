# gui/hangman_gui.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
from solver.bayesian_solver import BayesianSolver
# Import Canvas specifically for drawing
from tkinter import Canvas


CORPUS_FILE_PATH = "data/hw1_word_counts_05.txt"
WORD_LENGTH = 5

class HangmanGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bayesian Hangman Solver")

        # Use ttk Style for potential future theming and widget customization
        self.style = ttk.Style()
        self.style.theme_use('clam') # Or 'default', 'vista', 'xpnative', 'aqua', 'alt' etc.

        # Style for the word label
        self.style.configure("Word.TLabel", font=("Courier", 36, "bold"), anchor="center")
        # Style for status/used letters labels
        self.style.configure("Info.TLabel", font=("Arial", 12), anchor="center")
        # Style for red/green status messages
        self.style.configure("Red.TLabel", foreground="red")
        self.style.configure("Green.TLabel", foreground="green")
        self.style.configure("Orange.TLabel", foreground="orange")


        # Main frame for layout
        self.main_frame = ttk.Frame(master, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights so widgets expand nicely
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        # Column 0 for Canvas (fixed size), Column 1 for text labels (expands)
        self.main_frame.columnconfigure(0, weight=0) # Canvas column
        self.main_frame.columnconfigure(1, weight=1) # Text labels column


        # --- Hangman Canvas Area (Row 0, Column 0, spanning down) ---
        self.canvas = Canvas(self.main_frame, width=200, height=250, bg="white")
        # Place canvas to the left, spanning multiple rows vertically
        # It will span row 0 (word), row 1 (status), row 2 (used letters)
        self.canvas.grid(row=0, column=0, rowspan=3, padx=(0, 20), sticky=(tk.N, tk.S))


        # --- Game Display Area (Row 0, Column 1) ---
        self.word_label = ttk.Label(self.main_frame, text="", style="Word.TLabel")
        self.word_label.grid(row=0, column=1, pady=(10, 20), sticky=(tk.W, tk.E)) # Now in column 1

        # --- Status Area (Row 1, Column 1) ---
        self.status_label = ttk.Label(self.main_frame, text="", style="Info.TLabel")
        self.status_label.grid(row=1, column=1, pady=(0, 5), sticky=(tk.W, tk.E)) # Now in column 1

        # --- Used Letters Area (Row 2, Column 1) ---
        self.used_letters_label = ttk.Label(self.main_frame, text="Used Letters: ", style="Info.TLabel")
        self.used_letters_label.grid(row=2, column=1, pady=(0, 10), sticky=(tk.W, tk.E)) # Now in column 1

        # --- Letter Buttons Area (Row 3, Column 0/1) ---
        self.letter_frame = ttk.Frame(self.main_frame, padding="10")
        self.letter_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        # Center the letter frame contents
        self.main_frame.rowconfigure(3, weight=1)


        self.letter_buttons = {}
        self._create_letter_buttons()

        # Store the default background color of the letter buttons *after* creation
        # Accessing it like this requires the buttons to be tk.Button, not ttk.Button
        self._default_button_color = self.letter_buttons['A'].cget('bg')


        # --- Control Buttons Area (Row 4, Column 0/1) ---
        self.control_frame = ttk.Frame(self.main_frame, padding="10 0 0 0")
        self.control_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)

        self.bayesian_guess_button = ttk.Button(self.control_frame, text="Bayesian Auto-Guess", command=self.make_bayesian_guess)
        self.bayesian_guess_button.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))

        self.restart_button = ttk.Button(self.control_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))


        # --- Hangman Drawing Sequence ---
        # Define the sequence of drawing parts for incorrect guesses
        # Ensure this list has exactly MAX_ATTEMPTS number of drawing functions
        self.drawing_parts = [] # Will be populated after initializing the game

        # Initialize the game instance
        try:
             self.game = BayesianSolver(corpus_path=CORPUS_FILE_PATH, word_length=WORD_LENGTH)
             # Define drawing parts based on MAX_ATTEMPTS from the solver
             # Assuming MAX_ATTEMPTS = 6 -> Need 6 parts (Head, Body, L Arm, R Arm, L Leg, R Leg)
             if self.game.max_attempts == 6:
                 self.drawing_parts = [
                     self._draw_head,
                     self._draw_body,
                     self._draw_left_arm,
                     self._draw_right_arm,
                     self._draw_left_leg,
                     self._draw_right_leg,
                 ]
             elif self.game.max_attempts > 6:
                 # Add more parts if attempts allow (e.g., eyes, mouth, hands, feet)
                 self.drawing_parts = [
                      self._draw_head,
                      self._draw_body,
                      self._draw_left_arm,
                      self._draw_right_arm,
                      self._draw_left_leg,
                      self._draw_right_leg,
                      # Add more drawing steps here if MAX_ATTEMPTS is higher
                 ][:self.game.max_attempts] # Cap the list just in case
             else:
                 print(f"Warning: MAX_ATTEMPTS ({self.game.max_attempts}) is less than 6. Hangman drawing might be incomplete.")
                 # Use a subset of drawings
                 self.drawing_parts = [
                      self._draw_head,
                      self._draw_body,
                      self._draw_left_arm,
                      self._draw_right_arm,
                      self._draw_left_leg,
                      self._draw_right_leg,
                 ][:self.game.max_attempts]


        except (FileNotFoundError, ValueError) as e:
             messagebox.showerror("Initialization Error", f"Failed to load corpus or initialize game: {e}")
             master.destroy()
             return

        # Start the first game display
        self.update_gui()
        self._enable_letter_buttons() # Reset button states and colors
        self._draw_gallows() # Draw the initial gallows
        self.status_label.config(text=f"Attempts Left: {self.game.attempts_left}", style="Info.TLabel")


    def _create_letter_buttons(self):
        """Creates buttons for each letter of the alphabet using tk.Button for color control."""
        row = 0
        col = 0
        buttons_per_row = 7

        for letter in string.ascii_uppercase:
            # Use tk.Button instead of ttk.Button to allow easy background color change
            button = tk.Button(self.letter_frame, text=letter, width=4,
                               font=("Arial", 10, "bold"),
                               command=lambda l=letter: self.on_letter_button_click(l),
                               highlightbackground='#d9d9d9', # Default Tk color
                               highlightthickness=1)
            button.grid(row=row, column=col, padx=2, pady=2)
            self.letter_buttons[letter] = button

            col += 1
            if col >= buttons_per_row:
                col = 0
                row += 1

    def on_letter_button_click(self, letter):
        """Handles a user clicking a letter button."""
        if self.game.is_won() or self.game.is_lost():
            return

        guess_char = letter.upper()
        button = self.letter_buttons.get(guess_char)

        if guess_char in self.game.guessed_letters:
             return

        # Disable the clicked button immediately
        if button:
            button.config(state=tk.DISABLED)

        self.game.guessed_letters.add(guess_char)

        # Check the guess against the true word and update state
        if guess_char in self.game.true_word:
            # The guess is correct
            if button:
                button.config(bg="#90EE90") # Light green background
            self.status_label.config(text=f"'{guess_char}' is correct!", style="Green.TLabel")

            # Update solver's positive evidence
            correct_feedback = {}
            for i, char_in_word in enumerate(self.game.true_word):
                if char_in_word == guess_char:
                    correct_feedback[i] = guess_char
            self.game.update_evidence(correct_feedback, [])

        else:
            # The guess is incorrect
            if button:
                button.config(bg="#FFA07A") # Light coral background
            self.game.attempts_left -= 1
            self.status_label.config(text=f"'{guess_char}' is incorrect! Attempts left: {self.game.attempts_left}", style="Red.TLabel")

            # Update solver's negative evidence
            self.game.update_evidence({}, [guess_char])

            # --- Draw a Hangman part for incorrect guess ---
            incorrect_guesses_count = self.game.max_attempts - self.game.attempts_left
            if 0 < incorrect_guesses_count <= len(self.drawing_parts):
                 # Call the next drawing function in sequence
                 self.drawing_parts[incorrect_guesses_count - 1]()


        # Always update GUI after a guess
        self.update_gui()

        # Check for win/loss after updating GUI
        if self.game.is_won():
            self._end_game(won=True)
        elif self.game.is_lost():
            self._end_game(won=False)


    def make_bayesian_guess(self):
        """Triggers the solver to make its best guess."""
        if self.game.is_won() or self.game.is_lost():
            return

        # Use the solver's logic to get the best guess
        # Filter available letters first before ranking for efficiency?
        # No, rank_letter_guesses already does this.
        ranked_guesses = self.game.rank_letter_guesses()

        guess_char = None
        # Find the best available guess (not already guessed)
        for char, prob in ranked_guesses:
            if char not in self.game.guessed_letters:
                guess_char = char
                break

        if guess_char:
             # Process this guess as if the user clicked the button
             self.on_letter_button_click(guess_char)
        else:
             # Should only happen if all letters have been guessed without winning/losing
             # This implies something might be wrong with the corpus or word selection
             self.status_label.config(text="Solver cannot find a new letter to guess.", style="Orange.TLabel")


    def restart_game(self):
        """Resets the game state and updates the GUI."""
        try:
             self.game.restart_game()
        except ValueError as e:
             messagebox.showerror("Restart Error", f"Failed to restart game: {e}")
             return

        # --- Clear and Redraw Gallows ---
        self.canvas.delete("all") # Clear the canvas
        self._draw_gallows()     # Draw the initial gallows


        # Reset button states and colors BEFORE updating the GUI based on new game
        self._enable_letter_buttons()

        self.update_gui()
        self.status_label.config(text=f"Attempts Left: {self.game.attempts_left}", style="Info.TLabel")
        self.bayesian_guess_button.config(state=tk.NORMAL)


    def update_gui(self):
        """Updates all GUI elements based on the current game state."""
        self.word_label.config(text=self.game.current_state())

        # Update the used letters display
        used_letters_str = "Used Letters: " + " ".join(sorted(list(self.game.guessed_letters)))
        self.used_letters_label.config(text=used_letters_str)

        # Ensure buttons for already guessed letters are disabled (and keep their color)
        for letter in string.ascii_uppercase:
            button = self.letter_buttons.get(letter)
            if button:
                if letter in self.game.guessed_letters:
                    button.config(state=tk.DISABLED)


    def _enable_letter_buttons(self):
        """Enables all letter buttons and resets their color."""
        # Ensure default color is captured if it wasn't already (e.g., if init failed)
        if not hasattr(self, '_default_button_color') or self._default_button_color is None:
             if 'A' in self.letter_buttons:
                 self._default_button_color = self.letter_buttons['A'].cget('bg')
             else:
                 # Fallback if buttons haven't been created yet
                 self._default_button_color = '#d9d9d9' # Typical Tk default gray


        for letter, button in self.letter_buttons.items():
            button.config(state=tk.NORMAL)
            # Reset the background color to the default
            button.config(bg=self._default_button_color)


    def _end_game(self, won):
        """Disables game controls and shows win/loss message."""
        self._disable_game_controls()
        final_message = f"The word was: {self.game.true_word}"
        if won:
            # Optionally draw the complete happy hangman or just leave it
            messagebox.showinfo("Victory!", f"Congratulations! You won!\n{final_message}")
        else:
            # Draw the final part if not already done
            incorrect_guesses_count = self.game.max_attempts - self.game.attempts_left
            if 0 < incorrect_guesses_count <= len(self.drawing_parts):
                 self.drawing_parts[incorrect_guesses_count - 1]() # Draw the last part if game ended on the last attempt
            messagebox.showerror("Game Over", f"You lost!\n{final_message}")


    def _disable_game_controls(self):
        """Disables buttons/widgets that shouldn't be usable after the game ends."""
        for button in self.letter_buttons.values():
            button.config(state=tk.DISABLED)
        self.bayesian_guess_button.config(state=tk.DISABLED)


    # --- Hangman Drawing Functions ---
    # Coordinates are relative to the canvas (width=200, height=250)
    def _draw_gallows(self):
        """Draws the basic gallows structure."""
        c = self.canvas
        # Base (slightly off the bottom)
        c.create_line(20, 230, 180, 230, width=3)
        # Upright
        c.create_line(50, 230, 50, 30, width=3)
        # Crossbar
        c.create_line(50, 30, 150, 30, width=3)
        # Rope
        c.create_line(150, 30, 150, 60, width=2)

    def _draw_head(self):
        """Draws the head."""
        c = self.canvas
        # Oval for head (x1, y1, x2, y2)
        c.create_oval(130, 60, 170, 100, width=2)

    def _draw_body(self):
        """Draws the body."""
        c = self.canvas
        # Line for body
        c.create_line(150, 100, 150, 170, width=2)

    def _draw_left_arm(self):
        """Draws the left arm."""
        c = self.canvas
        # Line for left arm (from body)
        c.create_line(150, 110, 120, 150, width=2)

    def _draw_right_arm(self):
        """Draws the right arm."""
        c = self.canvas
        # Line for right arm (from body)
        c.create_line(150, 110, 180, 150, width=2)

    def _draw_left_leg(self):
        """Draws the left leg."""
        c = self.canvas
        # Line for left leg (from body)
        c.create_line(150, 170, 130, 210, width=2)

    def _draw_right_leg(self):
        """Draws the right leg."""
        c = self.canvas
        # Line for right leg (from body)
        c.create_line(150, 170, 170, 210, width=2)


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 450) # Minimum size might need adjustment with canvas
    root.update_idletasks()

    # Center the window
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('+{}+{}'.format(x, y))

    gui = HangmanGUI(root)

    # Only start the mainloop if initialization was successful
    if hasattr(gui, 'game') and gui.game.true_word is not None:
        root.mainloop()