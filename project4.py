
import random

word_list = ["heart", "loopy", "audio", "laugh", "trial"]

print("Choose a game mode:")
print("1. Guess a random word")
print("2. Pick the letters")

mode = input("Enter 1 or 2: ")

if mode == "1":
    hidden_word = random.choice(word_list)
elif mode == "2":
    hidden_word = input("Choose a five-letter word: ").lower()

    if len(hidden_word) != 5 or not hidden_word.isalpha():
        print("Please enter exactly five letters.")
        raise SystemExit
else:
    print("Please choose 1 or 2.")
    raise SystemExit

for _ in range(5):
    guess_word = input("Guess the five-letter word: ").lower()

    if len(guess_word) != 5:
        print("Your guess must be five letters.")
        continue

    output = ""

    for i in range(5):
        if guess_word[i] == hidden_word[i]:
            output += "🟩"
        elif guess_word[i] in hidden_word:
            output += "🟨"
        else:
            output += "⬛"

    print(output)

    if guess_word == hidden_word:
        print("You win!")
        break
else:
    print("The word was:", hidden_word)



