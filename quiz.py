import tkinter as tk
from tkinter import messagebox
import json
import random
import os

# -------------------- FILES --------------------
QUESTIONS_FILE = "questions.json"
USERS_FILE = "users.json"
LEADERBOARD_FILE = "leaderboard.json"
HISTORY_FILE = "history.json"

# -------------------- INITIALIZE FILES --------------------
if not os.path.exists(QUESTIONS_FILE):
    sample_questions = {
        "Science": [
            {"question": "What is the chemical symbol for water?", "options": ["H2O","O2","CO2","NaCl"], "answer":"H2O"},
            {"question": "What planet is known as the Red Planet?", "options":["Earth","Mars","Jupiter","Venus"], "answer":"Mars"}
        ],
        "Math": [
            {"question": "What is 5 + 7?", "options":["10","11","12","13"], "answer":"12"},
            {"question": "What is the square root of 16?", "options":["2","4","8","16"], "answer":"4"}
        ]
    }
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(sample_questions, f, indent=4)

# Load data
with open(QUESTIONS_FILE, "r") as f:
    questions_data = json.load(f)

users = {}
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)

leaderboard = {}
if os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "r") as f:
        leaderboard = json.load(f)

history = {}
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

# -------------------- MAIN WINDOW --------------------
root = tk.Tk()
root.title("Advanced Offline Quiz System")
root.geometry("800x550")
root.config(bg="#f0f0f0")

# -------------------- GLOBAL VARIABLES --------------------
username = ""
current_category = ""
current_questions = []
current_index = 0
score = 0
answer_var = tk.StringVar()
category_var = tk.StringVar()
timer_seconds = 20
timer_id = None

# -------------------- HELPERS --------------------
def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

# -------------------- LOGIN --------------------
def login():
    global username
    user = entry_username.get().strip()
    pwd = entry_password.get().strip()
    if user == "" or pwd == "":
        messagebox.showerror("Error", "Enter username and password")
        return
    if user in users:
        if users[user]["password"] == pwd:
            username = user
            show_category_screen()
        else:
            messagebox.showerror("Error", "Incorrect password")
    else:
        users[user] = {"password": pwd}
        save_json(USERS_FILE, users)
        messagebox.showinfo("Success", "New account created")
        username = user
        show_category_screen()

def show_login_screen():
    clear_frame()
    tk.Label(frame, text="Welcome to Advanced Quiz", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(frame, text="Username:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    global entry_username
    entry_username = tk.Entry(frame, font=("Arial", 12))
    entry_username.pack(pady=5)
    tk.Label(frame, text="Password:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    global entry_password
    entry_password = tk.Entry(frame, show="*", font=("Arial", 12))
    entry_password.pack(pady=5)
    tk.Button(frame, text="Login / Sign Up", font=("Arial", 12), bg="#4CAF50", fg="white", command=login).pack(pady=20)

# -------------------- CATEGORY SELECTION --------------------
def show_category_screen():
    clear_frame()
    tk.Label(frame, text=f"Hello, {username}!", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    tk.Label(frame, text="Select a Quiz Category:", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
    for cat in questions_data.keys():
        tk.Radiobutton(frame, text=cat, variable=category_var, value=cat, font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
    tk.Button(frame, text="Start Quiz", font=("Arial", 12), bg="#2196F3", fg="white", command=start_quiz).pack(pady=15)
    tk.Button(frame, text="View Leaderboard", font=("Arial", 12), bg="#FF9800", fg="white", command=view_leaderboard).pack(pady=5)

# -------------------- QUIZ LOGIC --------------------
def start_quiz():
    global current_category, current_questions, current_index, score
    current_category = category_var.get()
    if current_category == "":
        messagebox.showerror("Error", "Select a category")
        return
    current_questions = questions_data[current_category][:]
    random.shuffle(current_questions)
    for q in current_questions:
        random.shuffle(q['options'])
    current_index = 0
    score = 0
    show_question()

def show_question():
    global current_index, timer_seconds, timer_id
    clear_frame()
    if current_index < len(current_questions):
        timer_seconds = 20
        q = current_questions[current_index]
        tk.Label(frame, text=f"Q{current_index+1}: {q['question']}", font=("Arial", 13), wraplength=700, bg="#f0f0f0").pack(pady=10)
        answer_var.set(None)
        for option in q['options']:
            tk.Radiobutton(frame, text=option, variable=answer_var, value=option, font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        tk.Label(frame, text=f"Time Left: {timer_seconds} s", font=("Arial", 12), bg="#f0f0f0", fg="red").pack(pady=5)
        tk.Button(frame, text="Next", font=("Arial", 12), bg="#4CAF50", fg="white", command=next_question).pack(pady=10)
        update_timer()
    else:
        finish_quiz()

def update_timer():
    global timer_seconds, timer_id
    for widget in frame.winfo_children():
        if "Time Left" in str(widget.cget("text")):
            widget.config(text=f"Time Left: {timer_seconds} s")
    if timer_seconds > 0:
        timer_seconds -= 1
        timer_id = root.after(1000, update_timer)
    else:
        messagebox.showinfo("Time Up", "Moving to next question")
        next_question()

def next_question():
    global current_index, score, timer_id
    if timer_id:
        root.after_cancel(timer_id)
    if answer_var.get() == current_questions[current_index]['answer']:
        score += 1
        messagebox.showinfo("Correct!", "Your answer is correct!")
    else:
        messagebox.showinfo("Incorrect!", f"Correct answer: {current_questions[current_index]['answer']}")
    current_index += 1
    show_question()

def finish_quiz():
    global username, score, current_category
    leaderboard[username] = score
    save_json(LEADERBOARD_FILE, leaderboard)
    if username not in history:
        history[username] = {}
    if current_category not in history[username]:
        history[username][current_category] = []
    history[username][current_category].append(score)
    save_json(HISTORY_FILE, history)
    clear_frame()
    tk.Label(frame, text=f"Quiz Finished! Your Score: {score}/{len(current_questions)}", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Button(frame, text="View Leaderboard", font=("Arial", 12), bg="#FF9800", fg="white", command=view_leaderboard).pack(pady=5)
    tk.Button(frame, text="Back to Categories", font=("Arial", 12), bg="#2196F3", fg="white", command=show_category_screen).pack(pady=5)
    tk.Button(frame, text="Exit", font=("Arial", 12), bg="#f44336", fg="white", command=root.destroy).pack(pady=5)

# -------------------- LEADERBOARD --------------------
def view_leaderboard():
    clear_frame()
    tk.Label(frame, text="Leaderboard (Top Scores)", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    sorted_board = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5]
    for user, sc in sorted_board:
        tk.Label(frame, text=f"{user} : {sc}", font=("Arial", 12), bg="#f0f0f0").pack()
    tk.Button(frame, text="Back", font=("Arial", 12), bg="#2196F3", fg="white", command=show_category_screen).pack(pady=15)

# -------------------- GUI SETUP --------------------
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(expand=True, fill="both")

show_login_screen()
root.mainloop()
