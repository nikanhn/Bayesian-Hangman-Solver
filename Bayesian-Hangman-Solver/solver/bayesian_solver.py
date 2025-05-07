import random
from collections import defaultdict
import string # Import string for potential alphabet reference

class BayesianSolver:

    # Define MAX_ATTEMPTS as a class attribute
    MAX_ATTEMPTS = 6 # Or 7, or whatever you want the total attempts to be

    def __init__(self, corpus_path: str, word_length: int = 5):
        self.corpus_path = corpus_path
        self.word_length = word_length
        # Load the full list of words of the correct length from the corpus
        self.full_word_list = self._load_corpus(self.corpus_path, self.word_length)

        # --- Game state specific to one round ---
        self.true_word = None       # The actual word for the current game
        # attempts_left will be initialized using MAX_ATTEMPTS in restart_game
        self.attempts_left = 0      
        self.guessed_letters = set() # Set of all letters guessed in the current game

        # --- Solver's internal state for probability calculation ---
        # This evidence is specific to the current game based on user guesses
        self.dict_evidence = {}     # Known positions: letter (e.g., {0:'A', 3:'L'})
        self.list_evidence = []     # Letters known to be incorrect (e.g., ['E', 'S'])

        # Start the first game automatically when the solver is initialized
        self.restart_game()


    def _load_corpus(self, path, length):
        word_list = []
        try:
            with open(path, 'r') as file:
                for line in file:
                    # Assuming format is "WORD COUNT"
                    parts = line.strip().split()
                    if not parts: continue # Skip empty lines
                    word = parts[0].upper() # Take the word part and convert to uppercase
                    # Basic validation: check if word contains only letters
                    if not all(c in string.ascii_uppercase for c in word):
                        print(f"Warning: Skipping non-alphabetic word '{word}' in corpus.")
                        continue
                    # Check if the word has the desired length
                    if len(word) == length:
                        word_list.append(word)
        except FileNotFoundError:
             print(f"Error: Corpus file not found at {self.corpus_path}")
             raise # Re-raise the error so the caller knows it failed
        except Exception as e:
             print(f"Error loading corpus file {self.corpus_path}: {e}")
             raise

        # Return a list of unique words of the specified length
        return list(set(word_list))


    def restart_game(self):
        """Starts a new game round."""
        if not self.full_word_list:
            raise ValueError("Corpus is empty or failed to load words of the specified length.")

        # 1. Pick a new random word
        self.true_word = random.choice(self.full_word_list)
        # print(f"Debug: Starting new game with word: {self.true_word}") # Optional debug print

        # 2. Reset game state
        # Initialize attempts_left using the MAX_ATTEMPTS constant
        self.attempts_left = self.MAX_ATTEMPTS 
        self.guessed_letters = set() # No letters guessed yet

        # 3. Reset solver's internal evidence for the new game
        self.dict_evidence = {}
        self.list_evidence = []


    def current_state(self):
        """Returns the displayed word state (e.g., "_ A _ _ L E")."""
        display = []
        for letter in self.true_word:
            if letter in self.guessed_letters:
                display.append(letter)
            else:
                display.append("_")
        return " ".join(display)


    def is_won(self):
        """Checks if the game has been won."""
        # The game is won if all letters in the true word have been guessed
        # A more robust check than current_state() == true_word, handles duplicates correctly
        return all(letter in self.guessed_letters for letter in set(self.true_word))


    def is_lost(self):
        """Checks if the game has been lost."""
        return self.attempts_left <= 0


    def make_guess(self):
        """Determines the best guess using Bayesian probability and updates game state."""
        if self.is_won() or self.is_lost():
            return "Game is already over. Please restart."

        # 1. Get the ranked list of potential guesses (letters not yet tried)
        ranked_guesses = self.rank_letter_guesses()

        # 2. Select the top-ranked letter that hasn't been guessed yet
        guess_char = None
        for char, prob in ranked_guesses:
             if char not in self.guessed_letters:
                  guess_char = char
                  break

        # Fallback: If for some reason no letters are available
        if guess_char is None:
             # This shouldn't happen if the corpus and logic are sound and game isn't over
             return "Error: No new letters to guess."


        # 3. Add the chosen letter to the set of all guessed letters
        # The GUI's on_letter_button_click does this *before* calling update_evidence
        # If you call make_guess directly (e.g., for an auto-play feature), you might
        # need to add it here *before* calling update_evidence based on feedback.
        # For GUI integration, it's better if the GUI handles the button click
        # which triggers the guess and updates guessed_letters *before* updating evidence.
        # Let's assume the GUI handles adding to guessed_letters before calling update_evidence.
        # If make_guess is called *without* a button click (auto-solve), you would need:
        # self.guessed_letters.add(guess_char)

        # 4. Check the guess against the true word and update state
        # This part is typically handled by the GUI after it gets the guess character
        # from make_guess and simulates a user clicking that button.
        # If make_guess is strictly for suggesting the guess:
        return guess_char # Return the suggested character


    # --- Methods for Bayesian Logic ---

    def update_evidence(self, correct: dict, incorrect: list):
        """Updates the solver's internal evidence based on game feedback."""
        # correct: {position: letter} e.g., {0:'A', 3:'L'}
        # incorrect: [letter1, letter2] e.g., ['E', 'S']
        self.dict_evidence.update(correct)
        # Ensure list_evidence contains only unique letters (add and then convert to set/list)
        for char in incorrect:
             if char not in self.list_evidence:
                  self.list_evidence.append(char)


    def _match(self, word):
        """Checks if a word from the corpus is consistent with the current evidence."""
        # 1. Word must be the correct length (already filtered by _load_corpus, but safe check)
        if len(word) != self.word_length:
            return False
            
        # 2. Word must not contain any letters from list_evidence
        if any(char in word for char in self.list_evidence):
             return False

        # 3. Word must match letters at known positions (dict_evidence)
        for pos, letter in self.dict_evidence.items():
             if pos >= len(word) or word[pos] != letter:
                  return False

        # 4. Word must contain all letters from dict_evidence, *even* if not at the specified positions,
        #    unless those letters are explicitly excluded from certain positions.
        #    This condition is more complex than the original _match. Let's stick to the original simple logic
        #    as it seems intended to check if the word *could* be the target word given known positions and known incorrect letters.
        #    The original condition 3 was: `if known_letters_values & letters_at_unknown_pos: return False`
        #    This original condition seems incorrect for standard Hangman/Wordle logic. If I know 'A' is at pos 0, 'A' *can* still be at pos 3 unless I've guessed pos 3 and found it's not 'A'.
        #    A more standard _match would be:
        #    - Word must not contain letters from list_evidence.
        #    - Word must match letters at dict_evidence positions.
        #    - Word must contain *at least* the number of occurrences of each letter as implied by dict_evidence.
        #    - If a letter from dict_evidence is found at a position *not* in dict_evidence, is that allowed? Yes, in standard Hangman.
        #    Let's revert _match to a simpler check based on your likely original intent before the complex condition 3 was added,
        #    or stick to the original simple one if that's what your Bayesian model expects.
        #    Reverting to a simpler check:
        #    - Must not contain incorrect letters.
        #    - Must match known positions.
        #    The complex condition seems to assume letters found at known positions cannot exist elsewhere, which isn't standard Hangman.
        #    Let's remove the complex condition 3 from the original _match.

        # Original complex condition 3 removed.
        # The check `if set(self.list_evidence) & set(word): return False` (now condition 2) is fine.
        # The check for known positions (now condition 3) is fine.
        # The core Bayesian logic needs to reason about *where* letters might be, not just if they are present.
        # A word matches the evidence if:
        # 1. It has the correct length.
        # 2. It does NOT contain any letters from `self.list_evidence`.
        # 3. For every position `p` and letter `L` in `self.dict_evidence`, the word has `L` at position `p`.
        # 4. (Optional but more complete for Bayesian) For every letter `L` known to be correct (in `self.dict_evidence.values()`),
        #    the word must contain at least as many occurrences of `L` as are defined in `self.dict_evidence`.
        #    Example: If dict_evidence is {0:'L', 3:'L'}, the word must have at least two 'L's.
        #    Your original code didn't check this. Let's add a basic check for condition 4 if needed,
        #    but often condition 3 is sufficient for simpler Bayesian models where `prob_next`
        #    simply counts words *containing* the character among matching words.

        # Sticking to the simpler _match: No letters from list_evidence, correct letters at dict_evidence positions.
        return True # If all checks pass

    # Let's refine _match slightly to be more robust, using the original code's structure but clarifying the complex condition.
    # Original Condition 3:
    # known_letters_values = set(self.dict_evidence.values())
    # letters_at_unknown_pos = {word[i] for i in range(len(word)) if i not in self.dict_evidence}
    # if known_letters_values & letters_at_unknown_pos: return False
    # This check implies that if a letter is KNOWN to be at a specific position (in dict_evidence),
    # it *cannot* appear at any other position UNLESS it's also explicitly known at that other position.
    # This is a *very* specific rule, not standard Hangman. It's more like a strict Mastermind-style clue interpretation.
    # Let's assume standard Hangman rules for _match:
    # 1. Must not contain letters from list_evidence.
    # 2. Must match letters at dict_evidence positions.
    # 3. (Crucial for hangman) For any letter `L` that appears at least once in `dict_evidence.values()`,
    #    the word must contain `L`. (Your `prob_next` covers the "contains" part implicitly by counting words with the char).
    #    Let's refine `_match` to the standard interpretation:
    def _match(self, word):
         """Checks if a word from the corpus is consistent with the current evidence (standard Hangman)."""
         # 1. Word must be the correct length
         if len(word) != self.word_length:
              return False

         # 2. Word must not contain any letters from list_evidence (known incorrect)
         if any(char in word for char in self.list_evidence):
              return False

         # 3. Word must match letters at known positions (dict_evidence)
         for pos, letter in self.dict_evidence.items():
              if pos >= len(word) or word[pos] != letter:
                   return False

         # 4. (Optional but good) Check if all letters known to be in the word (from dict_evidence values) are actually present.
         #    This is implicitly handled by how `prob_next` is calculated (counting words that *contain* the char),
         #    but a more rigorous _match could verify this.
         #    Let's skip this for now as it adds complexity and might not align with the original Bayesian formula's assumptions.
         #    The core checks 1, 2, and 3 (as redefined) are essential.

         return True # The word is consistent with the evidence


    def prob_next(self, char: str):
        """Calculates P(Char IS in word | Evidence). Used for ranking guesses."""
        # This calculates the probability that the character 'char' is anywhere in the true word,
        # given the current evidence.

        # Filter the full word list down to only those consistent with the current evidence
        matching_words = [w for w in self.full_word_list if self._match(w)]
        matching_words_count = len(matching_words)

        if matching_words_count == 0:
            # If no words match the current evidence, the probability of any un-guessed char being in the word is 0.
            return 0.0


        # Count words among the matching ones that *also* contain the character 'char'
        # We only calculate this for the character 'char' we are currently evaluating.
        words_with_char_count = sum(1 for w in matching_words if char in w)

        # Probability P(Char IS in word | Evidence)
        probability = words_with_char_count / matching_words_count

        return probability


    def rank_letter_guesses(self):
        """Ranks letters based on their probability of being in the word."""
        # Only consider letters that haven't been guessed yet
        alphabet = set(string.ascii_uppercase)
        available_letters = list(alphabet - self.guessed_letters)

        rankings = []
        for char in available_letters:
            # Calculate probability P(Char IS in word | Evidence)
            # But only if the character isn't already known to be correct from dict_evidence.
            # If a char is in dict_evidence values, its probability of being *in the word* is 1, but we shouldn't guess it again.
            # The `available_letters` check already handles not guessing letters in `guessed_letters`,
            # and `guessed_letters` should include letters from `dict_evidence.values()`.
            # So, calculating prob_next for available letters is correct.
            prob = self.prob_next(char)
            rankings.append((char, prob))

        # Sort by probability in descending order (highest probability first)
        # If probabilities are equal, sort alphabetically for consistency (optional)
        return sorted(rankings, key=lambda x: (-x[1], x[0]))

    # Add a property or method to expose MAX_ATTEMPTS if needed outside the class
    # (though accessing the class attribute directly like BayesianSolver.MAX_ATTEMPTS is fine)
    # Or expose it as an instance attribute if it *could* vary per instance (less common for max attempts)
    @property
    def max_attempts(self):
        return self.MAX_ATTEMPTS