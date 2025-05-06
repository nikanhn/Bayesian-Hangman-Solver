# 🧠 Bayesian Hangman Solver

A Python-based Hangman game solver using Bayesian inference and frequency-based prediction. Comes with an interactive GUI to visualize the AI in action.

## 🚀 Features

- 🧮 Bayesian word prediction
- 📊 Frequency-based letter guessing
- 🖥️ Interactive GUI
- ✅ Simple test coverage
- 🔁 Easy-to-extend for other wordlists or strategies

## 📸 Demo

![hangman-gui-demo](demo/hangman.gif)

## 🧠 How It Works

1. Load a vocabulary of words.
2. Use Bayesian inference to assign probabilities to letters.
3. Guess letters that maximize expected information gain.
4. Update beliefs as guesses progress.

## 🔧 Installation

```bash
git clone https://github.com/nikanhn/Bayesian-Hangman-Solver
cd Bayesian-Hangman-Solver
pip install -r requirements.txt
