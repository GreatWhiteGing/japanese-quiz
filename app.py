import random
import tkinter as tk
import tkinter.messagebox as messagebox
from data import *
from score import save_score, show_history

# --- Global Variables ---
selected = []       # list of character tuples for the current quiz
current_char = None # the current character being quizzed
total_questions = 0 # total questions answered this session
score = 0           # correct answers this session
label = ""          # tracks which mode was selected

# --- Menu Functions ---
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
    if messagebox.askyesno("Save Progress", "Would you like to save your progress?"):
        if total_questions > 0:
            percentage = round((score / total_questions) * 100)
            save_score(label, score, total_questions, percentage)
    # reset score variables
    total_questions = 0
    score = 0
    score_label.config(text="Score: 0/0")
    # return to menu
    quiz_frame.pack_forget()
    menu_frame.pack()

def check_answer():
    """Check the user's answer and update the score"""
    global total_questions, score
    result_label.config(text="")
    answer = answer_entry.get().lower()
    
    if answer == current_char[0]:
        result_label.config(text="Correct!", fg="green") 
        score += 1
    else:
        result_label.config(text=f"Incorrect! The answer was {current_char[0]}", fg="red")
    
    total_questions += 1
    score_label.config(text=f"Score: {score}/{total_questions}")
    next_question()

def next_question():
    """Pick a random character and display in on screen"""
    global current_char
    current_char = random.choice(selected)
    char_label.config(text=current_char[1])
    answer_entry.delete(0, tk.END)

# --- Window Setup ---
root = tk.Tk()
root.title("Japanese Quiz")
root.geometry("400x300")

# --- Frames ---
menu_frame = tk.Frame(root)
quiz_frame = tk.Frame(root)

# --- Quiz Widgets ---
char_label = tk.Label(quiz_frame, text="", font=("Arial", 48))
answer_entry = tk.Entry(quiz_frame, width=20)
answer_entry.bind("<Return>", lambda event: check_answer())
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

# Show menu frame on startup
menu_frame.pack()

# Start the tkinter event loop
root.mainloop()