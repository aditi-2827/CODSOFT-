"""
GUI-Based To-Do List Application
A user-friendly graphical interface for task management
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

class TodoListGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        
        self.filename = 'tasks_gui.json'
        self.tasks = self.load_tasks()
        
        # Configure style
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        self.refresh_task_list()
    
    def setup_styles(self):
        """Configure GUI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10))
        style.configure('Treeview', font=('Arial', 10), rowheight=25)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10, fill='x')
        
        title_label = ttk.Label(title_frame, text="📝 To-Do List Manager", 
                                style='Title.TLabel')
        title_label.pack()
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Add New Task", padding=10)
        input_frame.pack(pady=10, padx=20, fill='x')
        
        # Title input
        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=2, pady=5, sticky='ew')
        
        # Description input
        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, sticky='w', pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=2, pady=5, sticky='ew')
        
        # Priority selection
        ttk.Label(input_frame, text="Priority:").grid(row=2, column=0, sticky='w', pady=5)
        self.priority_var = tk.StringVar(value='Medium')
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                      values=['Low', 'Medium', 'High'], 
                                      state='readonly', width=15)
        priority_combo.grid(row=2, column=1, sticky='w', pady=5)
        
        # Add button
        add_btn = ttk.Button(input_frame, text="➕ Add Task", command=self.add_task)
        add_btn.grid(row=2, column=2, pady=5, padx=5)
        
        input_frame.columnconfigure(1, weight=1)
        
        # Task List Frame
        list_frame = ttk.LabelFrame(self.root, text="Task List", padding=10)
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Create Treeview
        columns = ('ID', 'Title', 'Description', 'Priority', 'Status', 'Created')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', 
                                 selectmode='browse')
        
        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Title')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Created', text='Created')
        
        # Define column widths
        self.tree.column('ID', width=40, anchor='center')
        self.tree.column('Title', width=150)
        self.tree.column('Description', width=200)
        self.tree.column('Priority', width=80, anchor='center')
        self.tree.column('Status', width=100, anchor='center')
        self.tree.column('Created', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_task_double_click)
        
        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=20, fill='x')
        
        ttk.Button(button_frame, text="✓ Mark Complete", 
                  command=self.mark_complete).pack(side='left', padx=5)
        ttk.Button(button_frame, text="✏ Edit Task", 
                  command=self.edit_task).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🗑 Delete Task", 
                  command=self.delete_task).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self.refresh_task_list).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📊 Statistics", 
                  command=self.show_statistics).pack(side='left', padx=5)
        
        # Filter Frame
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5, padx=20, fill='x')
        
        ttk.Label(filter_frame, text="Filter by Status:").pack(side='left', padx=5)
        self.filter_var = tk.StringVar(value='All')
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                    values=['All', 'Pending', 'Completed'],
                                    state='readonly', width=15)
        filter_combo.pack(side='left', padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_task_list())
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief='sunken', anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)
    
    def add_task(self):
        """Add a new task"""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        priority = self.priority_var.get()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a task title!")
            return
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'Pending',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': None
        }
        
        self.tasks.append(task)
        self.save_tasks()
        
        # Clear inputs
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.priority_var.set('Medium')
        
        self.refresh_task_list()
        self.update_status(f"Task '{title}' added successfully!")
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter tasks
        filter_status = self.filter_var.get()
        filtered_tasks = self.tasks if filter_status == 'All' else \
                         [t for t in self.tasks if t['status'] == filter_status]
        
        # Add tasks to tree
        for task in filtered_tasks:
            # Color code by priority
            tag = task['priority'].lower()
            self.tree.insert('', 'end', values=(
                task['id'],
                task['title'],
                task['description'],
                task['priority'],
                task['status'],
                task['created_at']
            ), tags=(tag,))
        
        # Configure tags for color coding
        self.tree.tag_configure('high', background='#ffcccc')
        self.tree.tag_configure('medium', background='#ffffcc')
        self.tree.tag_configure('low', background='#ccffcc')
        
        self.update_status(f"Showing {len(filtered_tasks)} task(s)")
    
    def mark_complete(self):
        """Mark selected task as completed"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task!")
            return
        
        item = self.tree.item(selection[0])
        task_id = item['values'][0]
        
        task = self.find_task(task_id)
        if task:
            task['status'] = 'Completed'
            task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
            self.refresh_task_list()
            self.update_status(f"Task #{task_id} marked as completed!")
    
    def edit_task(self):
        """Edit selected task"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task!")
            return
        
        item = self.tree.item(selection[0])
        task_id = item['values'][0]
        task = self.find_task(task_id)
        
        if not task:
            return
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Title
        ttk.Label(dialog, text="Title:").grid(row=0, column=0, sticky='w', padx=10, pady=10)
        title_entry = ttk.Entry(dialog, width=30)
        title_entry.insert(0, task['title'])
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Description
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, sticky='w', padx=10, pady=10)
        desc_entry = ttk.Entry(dialog, width=30)
        desc_entry.insert(0, task['description'])
        desc_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Priority
        ttk.Label(dialog, text="Priority:").grid(row=2, column=0, sticky='w', padx=10, pady=10)
        priority_var = tk.StringVar(value=task['priority'])
        priority_combo = ttk.Combobox(dialog, textvariable=priority_var,
                                      values=['Low', 'Medium', 'High'],
                                      state='readonly', width=27)
        priority_combo.grid(row=2, column=1, padx=10, pady=10)
        
        def save_changes():
            task['title'] = title_entry.get().strip()
            task['description'] = desc_entry.get().strip()
            task['priority'] = priority_var.get()
            self.save_tasks()
            self.refresh_task_list()
            self.update_status(f"Task #{task_id} updated!")
            dialog.destroy()
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Save", command=save_changes).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
    
    def delete_task(self):
        """Delete selected task"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task!")
            return
        
        item = self.tree.item(selection[0])
        task_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"Delete task #{task_id}?"):
            task = self.find_task(task_id)
            if task:
                self.tasks.remove(task)
                # Reassign IDs
                for i, t in enumerate(self.tasks, 1):
                    t['id'] = i
                self.save_tasks()
                self.refresh_task_list()
                self.update_status(f"Task #{task_id} deleted!")
    
    def on_task_double_click(self, event):
        """Handle double-click on task"""
        self.edit_task()
    
    def show_statistics(self):
        """Show task statistics"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t['status'] == 'Completed'])
        pending = total - completed
        
        high_priority = len([t for t in self.tasks if t['priority'] == 'High'])
        medium_priority = len([t for t in self.tasks if t['priority'] == 'Medium'])
        low_priority = len([t for t in self.tasks if t['priority'] == 'Low'])
        
        stats = f"""
         TASK STATISTICS
        ═══════════════════════════════
        
        Total Tasks: {total}
        ✓ Completed: {completed}
        ⏳ Pending: {pending}
        
        Priority Breakdown:
        🔴 High: {high_priority}
        🟡 Medium: {medium_priority}
        🟢 Low: {low_priority}
        """
        
        if total > 0:
            completion_rate = (completed/total)*100
            stats += f"\n        Completion Rate: {completion_rate:.1f}%"
        
        messagebox.showinfo("Statistics", stats)
    
    def find_task(self, task_id):
        """Find a task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = TodoListGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
