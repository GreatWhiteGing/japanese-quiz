import random
import tkinter as tk
from data import *
from score import save_score, show_history

selected = []
current_char = None
total_questions = 0
score = 0

def start_hiragana():
    global selected
    selected = list(hiragana.items())
    menu_frame.pack_forget()
    quiz_frame.pack()
    next_question()
    
def start_katakana():
    global selected
    selected = list(katakana.items())
    menu_frame.pack_forget()
    quiz_frame.pack()
    next_question()

def start_both():
    global selected
    selected = list(hiragana.items()) + list(katakana.items())
    menu_frame.pack_forget()
    quiz_frame.pack()
    next_question()

def quit_app():
    root.destroy()

def check_answer():
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
    global current_char
    current_char = random.choice(selected)
    char_label.config(text=current_char[1])
    answer_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Japanese Quiz")
root.geometry("400x300")

menu_frame = tk.Frame(root)
quiz_frame = tk.Frame(root)

char_label = tk.Label(quiz_frame, text="", font=("Arial", 48))
answer_entry = tk.Entry(quiz_frame, width=20)
answer_entry.bind("<Return>", lambda event: check_answer())
submit_btn =tk.Button(quiz_frame, text="Submit", command=check_answer)
result_label = tk.Label(quiz_frame, text="")
score_label = tk.Label(quiz_frame, text="Score: 0/0")

label = tk.Label(menu_frame, text="Japanese Quiz")
btn_hiragana = tk.Button(menu_frame, text="1. Hiragana", command=start_hiragana)
btn_katakana = tk.Button(menu_frame, text="2. Katakana", command=start_katakana)
btn_both = tk.Button(menu_frame, text="3. Both", command=start_both)
btn_quit = tk.Button(menu_frame, text="4. Quit", command=quit_app)

# Menu widget packs
label.pack()
btn_hiragana.pack()
btn_katakana.pack()
btn_both.pack()
btn_quit.pack()

# Quiz widget packs
char_label.pack()
answer_entry.pack()
submit_btn.pack()
result_label.pack()
score_label.pack()

menu_frame.pack()

root.mainloop()