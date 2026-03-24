import random
from data import *
from score import save_score, show_history

total_questions = 0
score = 0

incorrect_answers = []

show_history()

while True:
    print("What would you like to practice?\n")
    print("1. Hiragana")
    print("2. Katakana")
    print("3. Both")
    print("4. Quit\n")
    
    choice = input("Enter 1, 2, 3, or 4: ")
    
    if choice == "1":
        selected = list(hiragana.items())
        label = "Hiragana"
        break
    elif choice == "2":
        selected = list(katakana.items())
        label = "Katakana"
        break
    elif choice == "3":
        selected = list(hiragana.items()) + list(katakana.items())
        label = "Both"
        break
    elif choice == "4":
        print("\nSee you next time!")
        exit()
    else:
        print("Invalid choice, please enter 1, 2, 3, or 4\n")

while True:
    random_char = random.choice(selected)
    answer = input(f"What is this character? {random_char[1]} ")
    
    if answer.lower() == "quit":
        print("Good work! See you next time")
        if total_questions > 0:
            percentage = round((score / total_questions) * 100)
            print(f"Final score: {score}/{total_questions} ({percentage}%)")
            save_score(label, score, total_questions, percentage)
        
            if incorrect_answers:
                print("\nCharacters to revisit:")
                for romaji, character in incorrect_answers:
                    print(f"{character} = {romaji}")
        else:
            print("No questions answered")
        break
    elif answer.lower() == random_char[0]:
        print("Correct!")
        total_questions+= 1
        score += 1
    else:
        print(f"Incorrect! The answer was {random_char[0]}")
        incorrect_answers.append(random_char)
        total_questions += 1