# import tkinter as tk
# from tkinter import messagebox
# from tkinter import ttk
# import string
# from solver.bayesian_solver import BayesianSolver

# CORPUS_FILE_PATH = "data/hw1_word_counts_05.txt"
# WORD_LENGTH = 5

# class HangmanGUI:
    
#     def __init__(self, master):
#         self.master = master
#         master.title("Bayesian Hangman Solver")
#         # Use ttk Style for potential future theming and widget customization
#         self.style = ttk.Style()
#         self.style.theme_use('clam') # Or 'default', 'vista', 'xpnative', 'aqua', 'alt' etc.

#         # Style for the word label
#         self.style.configure("Word.TLabel", font=("Courier", 36, "bold"), anchor="center")
#         # Style for status/used letters labels
#         self.style.configure("Info.TLabel", font=("Arial", 12), anchor="center")
#         # Style for red/green status messages
#         self.style.configure("Red.TLabel", foreground="red")
#         self.style.configure("Green.TLabel", foreground="green")
#         self.style.configure("Orange.TLabel", foreground="orange")


#         # Main frame for layout
#         self.main_frame = ttk.Frame(master, padding="20") 
#         self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#         # Configure grid weights so widgets expand nicely
#         master.columnconfigure(0, weight=1)
#         master.rowconfigure(0, weight=1)
#         self.main_frame.columnconfigure(0, weight=1)
#         self.main_frame.columnconfigure(1, weight=1)

#         # --- Game Display Area (Row 0 or 1, Column 0/1) ---
#         # word_label will span both columns if no canvas is used in column 0
#         self.word_label = ttk.Label(self.main_frame, text="", style="Word.TLabel")
#         self.word_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky=(tk.W, tk.E)) 

#         # --- Status Area (Row 2, Column 0/1) ---
#         self.status_label = ttk.Label(self.main_frame, text="", style="Info.TLabel")
#         self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 5), sticky=(tk.W, tk.E))

#         # --- Used Letters Area (Row 3, Column 0/1) ---
#         self.used_letters_label = ttk.Label(self.main_frame, text="Used Letters: ", style="Info.TLabel")
#         self.used_letters_label.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))

#         # --- Letter Buttons Area (Row 4, Column 0/1) ---
#         self.letter_frame = ttk.Frame(self.main_frame, padding="10")
#         self.letter_frame.grid(row=3, column=0, columnspan=2, pady=10) 

#         self.letter_buttons = {} 
#         self._create_letter_buttons()

#         # --- Control Buttons Area (Row 5, Column 0/1) ---
#         self.control_frame = ttk.Frame(self.main_frame, padding="10 0 0 0") 
#         self.control_frame.grid(row=4, column=0, columnspan=2, pady=10)
#         self.control_frame.columnconfigure(0, weight=1) 
#         self.control_frame.columnconfigure(1, weight=1)

#         # Original Bayesian Guess button (optional, can be a hint or auto-solve)
#         self.bayesian_guess_button = ttk.Button(self.control_frame, text="Bayesian Auto-Guess", command=self.make_bayesian_guess)
#         self.bayesian_guess_button.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E)) 

#         self.restart_button = ttk.Button(self.control_frame, text="Restart Game", command=self.restart_game)
#         self.restart_button.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E)) 


#         # Initialize the game instance
#         try:
#             self.game = BayesianSolver(corpus_path=CORPUS_FILE_PATH, word_length=WORD_LENGTH)
#         except (FileNotFoundError, ValueError) as e:
#             messagebox.showerror("Initialization Error", f"Failed to load corpus or initialize game: {e}")
#             master.destroy() 
#             return 

#         # Store the default background color of the letter buttons
#         self._default_button_color = self.letter_buttons['A'].cget('bg')


#         # Start the first game display
#         self.update_gui()
#         self._enable_letter_buttons()
#         self.status_label.config(text=f"Attempts Left: {self.game.attempts_left}", style="Info.TLabel")
    
#     def _create_letter_buttons(self):
#         """Creates buttons for each letter of the alphabet using tk.Button for color control."""
#         row = 0
#         col = 0
#         buttons_per_row = 7 

#         for letter in string.ascii_uppercase:
#             # Use tk.Button instead of ttk.Button to allow easy background color change
#             button = tk.Button(self.letter_frame, text=letter, width=4, 
#                             font=("Arial", 10, "bold"), 
#                             command=lambda l=letter: self.on_letter_button_click(l), highlightbackground='#3fa0ca',
#                 highlightthickness=2)
#             button.grid(row=row, column=col, padx=2, pady=2)
#             self.letter_buttons[letter] = button 

#             col += 1
#             if col >= buttons_per_row:
#                 col = 0
#                 row += 1

#     def on_letter_button_click(self, letter):
#         """Handles a user clicking a letter button."""
#         if self.game.is_won() or self.game.is_lost():
#             return 

#         guess_char = letter.upper()
#         button = self.letter_buttons.get(guess_char)

#         if guess_char in self.game.guessed_letters:
#             # This check is redundant if buttons are disabled, but safe
#             return 

#         # Disable the clicked button
#         if button:
#             button.config(state=tk.DISABLED)

#         self.game.guessed_letters.add(guess_char)


#         # Check the guess against the true word and update state
#         if guess_char in self.game.true_word:
#             # The guess is correct
#             if button:
#                 button.config(bg="#90EE90") 
#             self.status_label.config(text=f"'{guess_char}' is correct!", style="Green.TLabel")

#             # Update solver's positive evidence
#             correct_feedback = {}
#             for i, char_in_word in enumerate(self.game.true_word):
#                 if char_in_word == guess_char:
#                     correct_feedback[i] = guess_char
#             self.game.update_evidence(correct_feedback, []) 

#         else:
#             # The guess is incorrect
#             if button:
#                 button.config(bg="#FFA07A") # Light coral background
#             self.game.attempts_left -= 1 
#             self.status_label.config(text=f"'{guess_char}' is incorrect! Attempts left: {self.game.attempts_left}", style="Red.TLabel")

#             # Update solver's negative evidence
#             self.game.update_evidence({}, [guess_char])


#         # Always update GUI after a guess
#         self.update_gui()

#         # Check for win/loss after updating GUI
#         if self.game.is_won():
#             self._end_game(won=True)
#         elif self.game.is_lost():
#             self._end_game(won=False)


#     def make_bayesian_guess(self):
#         """Triggers the solver to make its best guess."""
#         if self.game.is_won() or self.game.is_lost():
#             return 

#         # Use the solver's logic to get the best guess
#         ranked_guesses = self.game.rank_letter_guesses()

#         guess_char = None
#         # Find the best available guess (not already guessed)
#         for char, prob in ranked_guesses:
#             if char not in self.game.guessed_letters:
#                 guess_char = char
#                 break

#         if guess_char:
#             # Process this guess as if the user clicked the button
#             self.on_letter_button_click(guess_char)
#         else:
#             # Should only happen if all letters have been guessed without winning/losing
#             self.status_label.config(text="No new letters to guess.", style="Orange.TLabel")


#     def restart_game(self):
#         """Resets the game state and updates the GUI."""
#         try:
#             self.game.restart_game() 
#         except ValueError as e:
#             messagebox.showerror("Restart Error", f"Failed to restart game: {e}")
#             return

#         # Reset button states and colors BEFORE updating the GUI based on new game
#         self._enable_letter_buttons() 

#         self.update_gui()
#         self.status_label.config(text=f"Attempts Left: {self.game.attempts_left}", style="Info.TLabel")
#         self.bayesian_guess_button.config(state=tk.NORMAL)


#     def update_gui(self):
#         """Updates all GUI elements based on the current game state."""
#         self.word_label.config(text=self.game.current_state())

#         # Update the used letters display
#         used_letters_str = "Used Letters: " + " ".join(sorted(list(self.game.guessed_letters)))
#         self.used_letters_label.config(text=used_letters_str)

#         # Ensure buttons for already guessed letters are disabled (and keep their color)
#         for letter in string.ascii_uppercase:
#             button = self.letter_buttons.get(letter)
#             if button:
#                 if letter in self.game.guessed_letters:
#                     button.config(state=tk.DISABLED)


#     def _enable_letter_buttons(self):
#         """Enables all letter buttons and resets their color."""
#         for letter, button in self.letter_buttons.items():
#             button.config(state=tk.NORMAL)
#             # Reset the background color to the default
#             button.config(bg=self._default_button_color) 


#     def _end_game(self, won):
#         """Disables game controls and shows win/loss message."""
#         self._disable_game_controls()
#         final_message = f"The word was: {self.game.true_word}"
#         if won:
#             messagebox.showinfo("Victory!", f"Congratulations! You won!\n{final_message}")
#         else:
#             messagebox.showerror("Game Over", f"You lost!\n{final_message}")


#     def _disable_game_controls(self):
#         """Disables buttons/widgets that shouldn't be usable after the game ends."""
#         for button in self.letter_buttons.values():
#             button.config(state=tk.DISABLED)
#         self.bayesian_guess_button.config(state=tk.DISABLED)


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.minsize(500, 450)
#     root.update_idletasks()
#     width = root.winfo_width()
#     height = root.winfo_height()

#     x = (root.winfo_screenwidth() // 2) - (width // 2)
#     y = (root.winfo_screenheight() // 2) - (height // 2)

#     root.geometry('+{}+{}'.format(x, y)) 

#     gui = HangmanGUI(root)

#     if hasattr(gui, 'game') and gui.game.true_word is not None: 
#         root.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
import os # Import os to check file existence
# You might need PIL (Pillow) to load PNG, JPEG etc.
# If you need PIL, uncomment the next two lines and install it (pip install Pillow)
# from PIL import Image, ImageTk

from solver.bayesian_solver import BayesianSolver
CORPUS_FILE_PATH = "data/hw1_word_counts_05.txt"
WORD_LENGTH = 5

# Define paths to your icon files. Replace these with actual paths.
# Use .gif files if you are not using PIL.
# Example:
# WIN_ICON_PATH = "path/to/your/win_icon.gif"
# LOSS_ICON_PATH = "path/to/your/loss_icon.gif"

# --- Placeholder Icon Paths (Replace with your actual paths) ---
# You MUST replace these with valid paths to .gif image files.
# If the paths are invalid, the custom dialog will simply not show an icon.
# Make sure the paths are correct relative to where you run the script,
# or provide absolute paths.
WIN_ICON_PATH = os.path.join(os.path.dirname(__file__), "win.gif") # Example relative path
LOSS_ICON_PATH = os.path.join(os.path.dirname(__file__), "lose.gif") # Example relative path

# --- Custom Dialog Class for Win/Loss Messages ---
class CustomMessageDialog(tk.Toplevel):
    def __init__(self, parent, title, message, icon_path):
        super().__init__(parent) # Inherit from Toplevel
        self.title(title)
        self.transient(parent) # Show on top of the parent window
        self.grab_set() # Prevent interaction with parent window until dialog is closed
        self.resizable(False, False) # Make dialog not resizable

        self.parent = parent # Keep a reference to the parent

        # Add padding to the frame
        frame = ttk.Frame(self, padding="20")
        frame.pack(expand=True, fill="both") # Make frame expand and fill the window

        # Default column weights
        frame.columnconfigure(0, weight=1) # Icon column
        frame.columnconfigure(1, weight=3) # Message column

        # --- Icon ---
        self.tk_image = None # Store the PhotoImage to prevent garbage collection
        icon_loaded = False
        try:
            # Check if the icon_path exists before trying to load
            if icon_path and os.path.exists(icon_path):
                # Load image using tk.PhotoImage (supports GIF, PGM, PPM)
                self.tk_image = tk.PhotoImage(file=icon_path)
                # If you need PIL for other formats (PNG, JPEG, etc.), use this instead:
                # pil_image = Image.open(icon_path)
                # self.tk_image = ImageTk.PhotoImage(pil_image)

                icon_label = ttk.Label(frame, image=self.tk_image)
                icon_label.grid(row=0, column=0, padx=10, pady=10, sticky="n") # Align top-left
                icon_loaded = True
            else:
                 print(f"Icon file not found or path is empty: {icon_path}")


        except Exception as e:
            print(f"Could not load icon image: {icon_path} - {e}")
            icon_loaded = False

        # If image loading fails, the icon space will be empty
        if not icon_loaded:
            frame.columnconfigure(0, weight=0) # Give no weight to empty icon column
            frame.columnconfigure(1, weight=1) # Give all weight to message column


        # --- Message ---
        # Use wraplength to automatically wrap long messages
        message_label = ttk.Label(frame, text=message, wraplength=300,
                                  font=("Arial", 10), anchor="w", justify="left") # Align text left
        # Place message label
        if icon_loaded: # If icon loaded successfully, place message next to it
            message_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew") # Expand in all directions
        else: # If no icon, place message centered and spanning columns
             message_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
             message_label.config(anchor="center", justify="center") # Center the text itself

        # --- OK Button ---
        ok_button = ttk.Button(frame, text="OK", command=self.destroy_dialog)
        # Place button centered below the message/icon area, spanning columns
        ok_button.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # Center the dialog over the parent window (basic centering)
        self.update_idletasks() # Ensure window dimensions are calculated
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()

        # Calculate position to center over parent
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 3) - (dialog_height // 2) # Slightly higher than center

        self.geometry(f'+{x}+{y}')


        # Handle window close button
        self.protocol("WM_DELETE_WINDOW", self.destroy_dialog)

        # Ensure focus is on this window and wait until it's destroyed
        self.wait_window(self)

    def destroy_dialog(self):
        """Releases the grab and destroys the window."""
        self.grab_release()
        self.destroy()


# --- HangmanGUI Class ---
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


        # Main frame for layout - remains a ttk.Frame to get the themed background
        self.main_frame = ttk.Frame(master, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights so widgets expand nicely
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # --- Game Display Area (Row 0 or 1, Column 0/1) ---
        # word_label will span both columns if no canvas is used in column 0
        self.word_label = ttk.Label(self.main_frame, text="", style="Word.TLabel")
        self.word_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky=(tk.W, tk.E))

        # --- Status Area (Row 2, Column 0/1) ---
        self.status_label = ttk.Label(self.main_frame, text="", style="Info.TLabel")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 5), sticky=(tk.W, tk.E))

        # --- Used Letters Area (Row 3, Column 0/1) ---
        self.used_letters_label = ttk.Label(self.main_frame, text="Used Letters: ", style="Info.TLabel")
        self.used_letters_label.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))

        # --- Letter Buttons Area (Row 4, Column 0/1) ---
        # CHANGE: Use tk.Frame here and remove 'padding="10"'
        # Set a background color that visually matches the ttk theme's dark background
        self.letter_frame = tk.Frame(self.main_frame, bg="#203354") # Use a dark gray
        self.letter_frame.grid(row=3, column=0, columnspan=2, pady=10) # Use pady for vertical spacing around the frame

        self.letter_buttons = {}
        self._create_letter_buttons()

        # --- Control Buttons Area (Row 5, Column 0/1) ---
        self.control_frame = ttk.Frame(self.main_frame, padding="10 0 0 0")
        self.control_frame.grid(row=4, column=0, columnspan=2, pady=10)
        self.control_frame.columnconfigure(0, weight=1)
        self.control_frame.columnconfigure(1, weight=1)

        # Original Bayesian Guess button (optional, can be a hint or auto-solve)
        self.bayesian_guess_button = ttk.Button(self.control_frame, text="Bayesian Auto-Guess", command=self.make_bayesian_guess)
        self.bayesian_guess_button.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))

        self.restart_button = ttk.Button(self.control_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))


        # Initialize the game instance
        try:
            self.game = BayesianSolver(corpus_path=CORPUS_FILE_PATH, word_length=WORD_LENGTH)
        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror("Initialization Error", f"Failed to load corpus or initialize game: {e}")
            master.destroy()
            return

        # Store the default background color of the letter buttons
        # Need to ensure buttons exist before getting color
        if self.letter_buttons:
             # Get background color of the first button (assuming consistency)
            self._default_button_color = self.letter_buttons[list(self.letter_buttons.keys())[0]].cget('bg')
        else:
            # Fallback if no buttons were created (shouldn't happen)
            self._default_button_color = '#d9d9d9' # Default tkinter button gray

        # Get the background color of the letter frame (which is now a tk.Frame)
        # Use update_idletasks to ensure the frame exists and has a configured color
        self.master.update_idletasks()
        self._letter_frame_bg = self.letter_frame.cget('bg')


        # Start the first game display
        self.update_gui()
        self._enable_letter_buttons()
        self.status_label.config(text=f"Attempts Left: {self.game.attempts_left}", style="Info.TLabel")


    def _create_letter_buttons(self):
        """Creates buttons for each letter of the alphabet using tk.Button for color control."""
        row = 0
        col = 0
        buttons_per_row = 7

        # Get the frame's background color before creating buttons
        # This is safer now that we ensure the frame is created before this method call
        frame_bg = self.letter_frame.cget('bg')


        for letter in string.ascii_uppercase:
            # Use tk.Button instead of ttk.Button to allow easy background color change
            # highlightbackground is used to make the border match the frame background
            button = tk.Button(self.letter_frame, text=letter, width=4,
                            font=("Arial", 10, "bold"),
                            command=lambda l=letter: self.on_letter_button_click(l),
                            # Use the frame's background color for highlightbackground
                            highlightbackground=frame_bg,
                            highlightthickness=1) # Set a small highlight thickness
            button.grid(row=row, column=col, padx=2, pady=2) # padx/pady add spacing between/around buttons
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
            # This check is redundant if buttons are disabled, but safe
            return

        # Disable the clicked button
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
            # Need to update the solver's internal state representation based on the *current* known state
            current_pattern = self.game.current_state().replace(' _', '_').replace(' ', '') # Get pattern like "B_BER"
            self.game.update_evidence(correct_feedback, [])


        else:
            # The guess is incorrect
            if button:
                button.config(bg="#FFA07A") # Light coral background
            self.game.attempts_left -= 1
            self.status_label.config(text=f"'{guess_char}' is incorrect! Attempts left: {self.game.attempts_left}", style="Red.TLabel")

            # Update solver's negative evidence
            self.game.update_evidence({}, [guess_char])


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
        # The solver's rank_letter_guesses method automatically uses the evidence
        # that has been updated by previous guesses via update_evidence calls.
        # We do NOT need to explicitly pass the current pattern string to the solver.
        ranked_guesses = self.game.rank_letter_guesses()

        guess_char = None
        # Find the best available guess (not already guessed)
        for char, prob in ranked_guesses:
            if char not in self.game.guessed_letters:
                guess_char = char
                break

        if guess_char:
            # Process this guess as if the user clicked the button
            # This call will trigger on_letter_button_click, which correctly
            # updates the game state, GUI, and calls self.game.update_evidence.
            self.on_letter_button_click(guess_char)
        else:
            # Should only happen if all letters have been guessed without winning/losing
            self.status_label.config(text="No new letters to guess.", style="Orange.TLabel")


    def restart_game(self):
        """Resets the game state and updates the GUI."""
        try:
            self.game.restart_game()
        except ValueError as e:
            messagebox.showerror("Restart Error", f"Failed to restart game: {e}")
            return

        # Reset button states and colors BEFORE updating the GUI based on new game
        self._enable_letter_buttons()

        self.update_gui()
        self.status_label.config(text=f"Attempts Left: {self.game.attempts_left}", style="Info.TLabel")
        self.bayesian_guess_button.config(state=tk.NORMAL)


    def update_gui(self):
        """Updates all GUI elements based on the current game state."""
        # The game's current_state() should return the pattern with underscores
        self.word_label.config(text=self.game.current_state())

        # Update the used letters display
        used_letters_str = "Used Letters: " + " ".join(sorted(list(self.game.guessed_letters)))
        self.used_letters_label.config(text=used_letters_str)

        # Ensure buttons for already guessed letters are disabled (and keep their color set in on_letter_button_click)
        for letter in string.ascii_uppercase:
            button = self.letter_buttons.get(letter)
            if button:
                if letter in self.game.guessed_letters:
                    button.config(state=tk.DISABLED)
                # Note: The color set in on_letter_button_click persists because we don't reset it here


    def _enable_letter_buttons(self):
        """Enables all letter buttons and resets their color."""
        # Use the stored default color for the button face
        default_button_color = self._default_button_color

        # Use the stored frame background color for the highlight
        frame_bg_color = self._letter_frame_bg


        for letter, button in self.letter_buttons.items():
            button.config(state=tk.NORMAL)
            # Reset the background color to the default button color
            # Reset highlightbackground to the frame's background color
            button.config(bg=default_button_color, highlightbackground=frame_bg_color)


    # --- _end_game method (Uses Custom Dialog) ---
    def _end_game(self, won):
        """Disables game controls and shows win/loss message using custom dialog."""
        self._disable_game_controls()
        final_message = f"The word was: {self.game.true_word}"

        if won:
            title = "Victory!"
            message = f"Congratulations! You won!\n\n{final_message}"
            icon_path = WIN_ICON_PATH # Use the path to your win icon
        else:
            title = "Game Over"
            message = f"You lost!\n\n{final_message}"
            icon_path = LOSS_ICON_PATH # Use the path to your loss icon

        # Use the custom dialog instead of messagebox
        # Pass self.master as the parent window so the dialog is modal relative to it
        # The dialog will pause execution until it's closed because of wait_window
        CustomMessageDialog(self.master, title, message, icon_path)

        # After the dialog is closed, the game remains in the end state
        # The restart button is available.


    def _disable_game_controls(self):
        """Disables buttons/widgets that shouldn't be usable after the game ends."""
        for button in self.letter_buttons.values():
            button.config(state=tk.DISABLED)
        self.bayesian_guess_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 450)
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()

    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)

    root.geometry('+{}+{}'.format(x, y))

    gui = HangmanGUI(root)

    # Only start the mainloop if the game initialized successfully
    if hasattr(gui, 'game') and gui.game is not None:
         root.mainloop()

      
