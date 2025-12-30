import random
import string
import re
import tkinter as tk
from tkinter import ttk, messagebox

def calculate_password_strength(password):
    """Calculate password strength score (0-100)"""
    score = 0
    length = len(password)
    
    # Length score (max 30 points)
    if length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    elif length >= 6:
        score += 10
    
    # Character variety (max 40 points)
    if re.search(r'[a-z]', password):
        score += 10
    if re.search(r'[A-Z]', password):
        score += 10
    if re.search(r'[0-9]', password):
        score += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 10
    
    # Uniqueness (max 30 points)
    unique_chars = len(set(password))
    uniqueness_ratio = unique_chars / length if length > 0 else 0
    score += int(uniqueness_ratio * 30)
    
    return min(score, 100)

def get_strength_label(score):
    """Get strength label based on score"""
    if score >= 80:
        return "Very Strong", "🟢"
    elif score >= 60:
        return "Strong", "🟡"
    elif score >= 40:
        return "Medium", "🟠"
    else:
        return "Weak", "🔴"

def generate_password(length, use_lowercase=True, use_uppercase=True, use_digits=True, use_symbols=True):
    characters = ""
    
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    
    if not characters:
        return "Error: At least one character type must be selected!"
    
    # Ensure at least one character from each selected type
    password = []
    if use_lowercase:
        password.append(random.choice(string.ascii_lowercase))
    if use_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if use_digits:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest randomly
    for _ in range(length - len(password)):
        password.append(random.choice(characters))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    return ''.join(password)

def password_generator():
    print("=" * 50)
    print("        PASSWORD GENERATOR")
    print("=" * 50)
    
    while True:
        try:
            length = input("\nEnter password length (minimum 4): ")
            if length.lower() == 'q':
                print("Exiting password generator. Goodbye!")
                break
            
            length = int(length)
            
            if length < 4:
                print("Password length must be at least 4 characters!")
                continue
            
            print("\nSelect password complexity:")
            print("1. Low (lowercase letters only)")
            print("2. Medium (lowercase + uppercase letters)")
            print("3. High (letters + numbers)")
            print("4. Very High (letters + numbers + symbols)")
            
            complexity = input("\nEnter your choice (1-4): ")
            
            if complexity == '1':
                password = generate_password(length, use_uppercase=False, use_digits=False, use_symbols=False)
            elif complexity == '2':
                password = generate_password(length, use_digits=False, use_symbols=False)
            elif complexity == '3':
                password = generate_password(length, use_symbols=False)
            elif complexity == '4':
                password = generate_password(length)
            else:
                print("Invalid choice! Using default (Very High complexity)")
                password = generate_password(length)
            
            # Calculate and display password strength
            strength_score = calculate_password_strength(password)
            strength_label, strength_icon = get_strength_label(strength_score)
            
            print("\n" + "=" * 50)
            print(f"Generated Password: {password}")
            print(f"Password Strength: {strength_icon} {strength_label} ({strength_score}/100)")
            print(f"Length: {len(password)} characters")
            print("=" * 50)
            print("\n💡 Tip: Copy your password now! It won't be shown again.")
            
            another = input("\nGenerate another password? (y/n): ")
            if another.lower() != 'y':
                print("Thank you for using Password Generator!")
                break
        
        except ValueError:
            print("Error: Please enter a valid number!")
        except Exception as e:
            print(f"An error occurred: {e}")

# ============================================
# GUI VERSION
# ============================================

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator Pro")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        self.password_history = []
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#1e1e1e")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🔐 Password Generator Pro",
            font=("Segoe UI", 24, "bold"),
            bg="#1e1e1e",
            fg="#00d4ff"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Create strong, secure passwords instantly",
            font=("Segoe UI", 10),
            bg="#1e1e1e",
            fg="#888888"
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#2d2d2d", relief=tk.RAISED, bd=2)
        main_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        # Password length
        length_frame = tk.Frame(main_frame, bg="#2d2d2d")
        length_frame.pack(pady=15, padx=20, fill=tk.X)
        
        length_label = tk.Label(
            length_frame,
            text="Password Length:",
            font=("Segoe UI", 11, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        length_label.pack(anchor=tk.W)
        
        length_control_frame = tk.Frame(length_frame, bg="#2d2d2d")
        length_control_frame.pack(fill=tk.X, pady=5)
        
        self.length_var = tk.IntVar(value=12)
        self.length_label_display = tk.Label(
            length_control_frame,
            text="12",
            font=("Segoe UI", 12, "bold"),
            bg="#2d2d2d",
            fg="#00d4ff",
            width=3
        )
        self.length_label_display.pack(side=tk.RIGHT)
        
        self.length_slider = tk.Scale(
            length_control_frame,
            from_=4,
            to=64,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            command=self.update_length_label,
            bg="#2d2d2d",
            fg="#ffffff",
            highlightthickness=0,
            troughcolor="#1e1e1e",
            activebackground="#00d4ff"
        )
        self.length_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Character options
        options_frame = tk.Frame(main_frame, bg="#2d2d2d")
        options_frame.pack(pady=10, padx=20, fill=tk.X)
        
        options_title = tk.Label(
            options_frame,
            text="Include:",
            font=("Segoe UI", 11, "bold"),
            bg="#2d2d2d",
            fg="#ffffff"
        )
        options_title.pack(anchor=tk.W, pady=(0, 5))
        
        self.lowercase_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        checkbox_style = {
            "font": ("Segoe UI", 10),
            "bg": "#2d2d2d",
            "fg": "#ffffff",
            "selectcolor": "#1e1e1e",
            "activebackground": "#2d2d2d",
            "activeforeground": "#00d4ff"
        }
        
        tk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.lowercase_var, **checkbox_style).pack(anchor=tk.W, pady=2)
        tk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.uppercase_var, **checkbox_style).pack(anchor=tk.W, pady=2)
        tk.Checkbutton(options_frame, text="Digits (0-9)", variable=self.digits_var, **checkbox_style).pack(anchor=tk.W, pady=2)
        tk.Checkbutton(options_frame, text="Symbols (!@#$%...)", variable=self.symbols_var, **checkbox_style).pack(anchor=tk.W, pady=2)
        
        # Generate button
        button_frame = tk.Frame(main_frame, bg="#2d2d2d")
        button_frame.pack(pady=15)
        
        self.generate_button = tk.Button(
            button_frame,
            text="⚡ Generate Password",
            font=("Segoe UI", 12, "bold"),
            bg="#00d4ff",
            fg="#1e1e1e",
            activebackground="#00b8d4",
            activeforeground="#1e1e1e",
            relief=tk.FLAT,
            cursor="hand2",
            width=20,
            height=2,
            command=self.generate_password
        )
        self.generate_button.pack()
        
        # Password display
        display_frame = tk.Frame(main_frame, bg="#1e1e1e", relief=tk.SUNKEN, bd=2)
        display_frame.pack(pady=15, padx=20, fill=tk.X)
        
        self.password_display = tk.Text(
            display_frame,
            height=3,
            font=("Consolas", 14, "bold"),
            bg="#1e1e1e",
            fg="#00ff00",
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.password_display.pack(fill=tk.X)
        self.password_display.insert(1.0, "Your password will appear here...")
        self.password_display.config(state=tk.DISABLED)
        
        # Strength indicator
        strength_frame = tk.Frame(main_frame, bg="#2d2d2d")
        strength_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.strength_label = tk.Label(
            strength_frame,
            text="Password Strength: Not Generated",
            font=("Segoe UI", 10),
            bg="#2d2d2d",
            fg="#888888"
        )
        self.strength_label.pack(anchor=tk.W)
        
        self.strength_bar = ttk.Progressbar(
            strength_frame,
            length=400,
            mode='determinate',
            style="Strength.Horizontal.TProgressbar"
        )
        self.strength_bar.pack(fill=tk.X, pady=5)
        
        # Configure progressbar style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Strength.Horizontal.TProgressbar", 
                       background='#00d4ff',
                       troughcolor='#1e1e1e',
                       bordercolor='#2d2d2d',
                       lightcolor='#00d4ff',
                       darkcolor='#00d4ff')
        
        # Action buttons
        action_frame = tk.Frame(main_frame, bg="#2d2d2d")
        action_frame.pack(pady=15)
        
        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "relief": tk.FLAT,
            "cursor": "hand2",
            "width": 15,
            "height": 1
        }
        
        self.copy_button = tk.Button(
            action_frame,
            text="📋 Copy",
            bg="#4caf50",
            fg="white",
            activebackground="#45a049",
            command=self.copy_password,
            state=tk.DISABLED,
            **button_style
        )
        self.copy_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = tk.Button(
            action_frame,
            text="🗑️ Clear",
            bg="#f44336",
            fg="white",
            activebackground="#da190b",
            command=self.clear_password,
            state=tk.DISABLED,
            **button_style
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        self.history_button = tk.Button(
            action_frame,
            text="📜 History",
            bg="#ff9800",
            fg="white",
            activebackground="#e68900",
            command=self.show_history,
            **button_style
        )
        self.history_button.pack(side=tk.LEFT, padx=5)
        
    def update_length_label(self, value):
        self.length_label_display.config(text=str(int(float(value))))
        
    def get_strength_info(self, score):
        if score >= 80:
            return "Very Strong 🟢", "#4caf50"
        elif score >= 60:
            return "Strong 🟡", "#8bc34a"
        elif score >= 40:
            return "Medium 🟠", "#ff9800"
        else:
            return "Weak 🔴", "#f44336"
    
    def generate_password(self):
        length = self.length_var.get()
        
        if not any([self.lowercase_var.get(), self.uppercase_var.get(), 
                   self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showwarning("Warning", "Please select at least one character type!")
            return
        
        generated_password = generate_password(
            length,
            self.lowercase_var.get(),
            self.uppercase_var.get(),
            self.digits_var.get(),
            self.symbols_var.get()
        )
        
        # Display password
        self.password_display.config(state=tk.NORMAL)
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(1.0, generated_password)
        self.password_display.config(state=tk.DISABLED)
        
        # Update strength
        strength_score = calculate_password_strength(generated_password)
        strength_label, strength_color = self.get_strength_info(strength_score)
        
        self.strength_label.config(
            text=f"Password Strength: {strength_label} ({strength_score}/100)",
            fg=strength_color
        )
        self.strength_bar['value'] = strength_score
        
        # Enable buttons
        self.copy_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)
        
        # Add to history
        self.password_history.insert(0, {
            'password': generated_password,
            'strength': strength_score,
            'length': length
        })
        if len(self.password_history) > 10:
            self.password_history.pop()
    
    def copy_password(self):
        password = self.password_display.get(1.0, tk.END).strip()
        if password and password != "Your password will appear here...":
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Success", "Password copied to clipboard! ✅")
    
    def clear_password(self):
        self.password_display.config(state=tk.NORMAL)
        self.password_display.delete(1.0, tk.END)
        self.password_display.insert(1.0, "Your password will appear here...")
        self.password_display.config(state=tk.DISABLED)
        
        self.strength_label.config(text="Password Strength: Not Generated", fg="#888888")
        self.strength_bar['value'] = 0
        
        self.copy_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
    
    def show_history(self):
        if not self.password_history:
            messagebox.showinfo("History", "No passwords generated yet!")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Password History")
        history_window.geometry("500x400")
        history_window.configure(bg="#1e1e1e")
        
        title = tk.Label(
            history_window,
            text="Recent Passwords (Last 10)",
            font=("Segoe UI", 14, "bold"),
            bg="#1e1e1e",
            fg="#00d4ff"
        )
        title.pack(pady=10)
        
        # Scrollable frame
        canvas = tk.Canvas(history_window, bg="#1e1e1e", highlightthickness=0)
        scrollbar = tk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, entry in enumerate(self.password_history, 1):
            frame = tk.Frame(scrollable_frame, bg="#2d2d2d", relief=tk.RAISED, bd=1)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            info_text = f"#{i} | Length: {entry['length']} | Strength: {entry['strength']}/100"
            tk.Label(
                frame,
                text=info_text,
                font=("Segoe UI", 9),
                bg="#2d2d2d",
                fg="#888888"
            ).pack(anchor=tk.W, padx=5, pady=2)
            
            tk.Label(
                frame,
                text=entry['password'],
                font=("Consolas", 10, "bold"),
                bg="#2d2d2d",
                fg="#00ff00"
            ).pack(anchor=tk.W, padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

def launch_gui():
    """Launch the GUI version"""
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("   PASSWORD GENERATOR - Choose Your Interface")
    print("=" * 50)
    print("\n1. GUI (Graphical User Interface)")
    print("2. CLI (Command Line Interface)")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == '1':
        try:
            launch_gui()
        except Exception as e:
            print(f"\nError launching GUI: {e}")
            print("Falling back to CLI version...\n")
            password_generator()
    else:
        password_generator()
