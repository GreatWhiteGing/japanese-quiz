import random
import tkinter as tk
import tkinter.messagebox as messagebox
from data import *
from score import save_score, load_history

# --- Global Variables ---
selected = []           # list of character tuples for the current quiz
current_char = None     # the current character being quizzed
total_questions = 0     # total questions answered this session
score = 0               # correct answers this session
label = ""              # tracks which mode was selected
incorrect_answers = []  # tracks incorrectly answered characters this session

# --- Menu Functions ---
def display_history():
    """Load and display recent session history on the menu screen"""
    # clear existing history labels to prevent duplicates
    for widget in menu_frame.winfo_children():
        if isinstance(widget, tk.Label) and widget != menu_label:
            widget.destroy()
    history = load_history()
    if not history:
        tk.Label(menu_frame, text="No recent sessions").pack()
        return
    
    tk.Label(menu_frame, text="--- Recent Sessions ---").pack()
    recent = history[-5:]
    for entry in recent:
        tk.Label(menu_frame, text=f"{entry['date']} | {entry['practiced']} | {entry['score']}/{entry['total']} ({entry['percentage']}%)").pack()

def start_hiragana():
    """Set up hiragana quiz and transition to quiz screen"""
    global selected, label
    selected = list(hiragana.items())
    label = "Hiragana"
    menu_frame.pack_forget()
    quiz_frame.pack()
    next_question()
    
def start_katakana():
    """Set up katakana quiz and transition to quiz screen"""
    global selected, label
    selected = list(katakana.items())
    label = "Katakana"
    menu_frame.pack_forget()
    quiz_frame.pack()
    next_question()

def start_both():
    """Set up combined hiragana and katakana quiz and transition to quiz screen"""
    global selected, label
    selected = list(hiragana.items()) + list(katakana.items())
    label = "Both"
    menu_frame.pack_forget()
    quiz_frame.pack()
    next_question()

def quit_app():
    """Close the application"""
    root.destroy()

# --- Quiz Functions ---
def quit_quiz():
    """Ask to save progress, reset score, and return to menu"""
    global total_questions, score
    if total_questions > 0:
        if messagebox.askyesno("Save Progress", "Would you like to save your progress?"):
            percentage = round((score / total_questions) * 100)
            save_score(label, score, total_questions, percentage)
        show_results()
    else:
        return_to_menu()

def check_answer():
    """Check the user's answer and update the score"""
    global total_questions, score, incorrect_answers
    result_label.config(text="")
    answer = answer_entry.get().lower()
    
    if answer == current_char[0]:
        result_label.config(text="Correct!", fg="green") 
        score += 1
    else:
        result_label.config(text=f"Incorrect! The answer was {current_char[0]}", fg="red")
        incorrect_answers.append(current_char)
    
    total_questions += 1
    score_label.config(text=f"Score: {score}/{total_questions}")
    next_question()

def next_question():
    """Pick a random character and display in on screen"""
    global current_char
    current_char = random.choice(selected)
    char_label.config(text=current_char[1])
    answer_entry.delete(0, tk.END)

# --- Results Functions ---
def show_results():
    """Display session results and incorrect answers"""
    quiz_frame.pack_forget()
    results_score_label.config(text=f"Final Score: {score}/{total_questions} ({round((score/total_questions)*100)}%)")
    if incorrect_answers:
        results_incorrect_label.config(text="Characters to revisit:")
        chars = "\n".join([f"{char[1]} = {char[0]}" for char in incorrect_answers])
        results_chars_label.config(text=chars)
    else:
        results_incorrect_label.config(text="Perfect score!")
        results_chars_label.config(text="")
    results_frame.pack()

def return_to_menu():
    """Reset session and return to menu"""
    global total_questions, score, incorrect_answers
    total_questions = 0
    score = 0
    incorrect_answers = []
    score_label.config(text="Score: 0/0")
    results_frame.pack_forget()
    menu_frame.pack()
    display_history()

# --- Window Setup ---
root = tk.Tk()
root.title("Japanese Quiz")
root.geometry("400x300")

# --- Frames ---
menu_frame = tk.Frame(root)
quiz_frame = tk.Frame(root)
results_frame = tk.Frame(root)

# --- Quiz Widgets ---
char_label = tk.Label(quiz_frame, text="", font=("Arial", 48))
answer_entry = tk.Entry(quiz_frame, width=20)
answer_entry.bind("<Return>", lambda event: check_answer()) # submit on Enter key
submit_btn =tk.Button(quiz_frame, text="Submit", command=check_answer)
result_label = tk.Label(quiz_frame, text="")
score_label = tk.Label(quiz_frame, text="Score: 0/0")

# --- Menu Widgets ---
menu_label = tk.Label(menu_frame, text="Japanese Quiz")
btn_hiragana = tk.Button(menu_frame, text="1. Hiragana", command=start_hiragana)
btn_katakana = tk.Button(menu_frame, text="2. Katakana", command=start_katakana)
btn_both = tk.Button(menu_frame, text="3. Both", command=start_both)
btn_quit = tk.Button(menu_frame, text="4. Quit", command=quit_app)
quit_quiz_btn = tk.Button(quiz_frame, text="Quit", command=quit_quiz)

# -- Results Widgets ---
results_title = tk.Label(results_frame, text="Session Complete!", font=("Arial", 16))
results_score_label = tk.Label(results_frame, text="")
results_incorrect_label = tk.Label(results_frame, text="")
results_chars_label = tk.Label(results_frame, text="", font=("Arial", 18))
return_btn = tk.Button(results_frame, text="Return to Menu", command=return_to_menu)

# --- Menu widget packs ---
menu_label.pack()
btn_hiragana.pack()
btn_katakana.pack()
btn_both.pack()
btn_quit.pack()

# --- Quiz widget packs ---
char_label.pack()
answer_entry.pack()
submit_btn.pack()
result_label.pack()
score_label.pack()
quit_quiz_btn.pack()

# --- Results widget pack ---
results_title.pack()
results_score_label.pack()
results_incorrect_label.pack()
results_chars_label.pack()
return_btn.pack()

# Show menu frame on startup
display_history()
menu_frame.pack()

# Start the tkinter event loop
root.mainloop()