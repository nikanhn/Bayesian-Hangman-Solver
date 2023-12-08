# Bayesian Hangman Solver
This project focuses on building a Bayesian hangman solver that strategically predicts letters of a word in the hangman game. 
The solver utilizes Bayes' Rule to sequentially guess letters, aiming to maximize the chance of winning by correctly guessing the word.

Hangman Game Rules
In the hangman game, after each letter (A through Z) is guessed, the player is informed whether the letter appears in the word and its position(s). Given the evidence accumulated during the game, the goal is to determine the optimal letter to guess at each stage.

Word Counts
The project requires the 'hw1_word_counts_05.txt' file, which contains a list of 5-letter words and their counts from a large corpus of Wall Street Journal articles. The prior probability P(w)=COUNT(w)∑w′COUNT(w′)P(w)=∑w′​COUNT(w′)COUNT(w)​ is computed from these counts.

Results
As a sanity check, the script will print out the fifteen most frequent and the fourteen least frequent 5-letter words. Reviewing these results provides insights into the quality of the prior probability computation.
