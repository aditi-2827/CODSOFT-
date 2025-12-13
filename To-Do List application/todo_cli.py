"""
Command-Line To-Do List Application
A simple and efficient CLI-based task management system
"""

import json
import os
from datetime import datetime

class TodoListCLI:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    
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
    
    def add_task(self, title, description='', priority='Medium'):
        """Add a new task"""
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
        print(f"✓ Task '{title}' added successfully!")
    
    def view_tasks(self, filter_status=None):
        """View all tasks or filtered by status"""
        if not self.tasks:
            print("\nNo tasks found!")
            return
        
        filtered_tasks = self.tasks
        if filter_status:
            filtered_tasks = [t for t in self.tasks if t['status'] == filter_status]
        
        if not filtered_tasks:
            print(f"\nNo {filter_status} tasks found!")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Title':<25} {'Priority':<10} {'Status':<12} {'Created':<20}")
        print("="*80)
        
        for task in filtered_tasks:
            print(f"{task['id']:<5} {task['title']:<25} {task['priority']:<10} "
                  f"{task['status']:<12} {task['created_at']:<20}")
            if task['description']:
                print(f"      Description: {task['description']}")
        print("="*80)
    
    def update_task(self, task_id, title=None, description=None, priority=None):
        """Update an existing task"""
        task = self.find_task(task_id)
        if task:
            if title:
                task['title'] = title
            if description:
                task['description'] = description
            if priority:
                task['priority'] = priority
            self.save_tasks()
            print(f"✓ Task #{task_id} updated successfully!")
        else:
            print(f"✗ Task #{task_id} not found!")
    
    def mark_complete(self, task_id):
        """Mark a task as completed"""
        task = self.find_task(task_id)
        if task:
            task['status'] = 'Completed'
            task['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_tasks()
            print(f"✓ Task #{task_id} marked as completed!")
        else:
            print(f"✗ Task #{task_id} not found!")
    
    def delete_task(self, task_id):
        """Delete a task"""
        task = self.find_task(task_id)
        if task:
            self.tasks.remove(task)
            # Reassign IDs
            for i, t in enumerate(self.tasks, 1):
                t['id'] = i
            self.save_tasks()
            print(f"✓ Task #{task_id} deleted successfully!")
        else:
            print(f"✗ Task #{task_id} not found!")
    
    def find_task(self, task_id):
        """Find a task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def get_statistics(self):
        """Display task statistics"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t['status'] == 'Completed'])
        pending = total - completed
        
        print("\n" + "="*50)
        print("TASK STATISTICS")
        print("="*50)
        print(f"Total Tasks: {total}")
        print(f"Completed: {completed}")
        print(f"Pending: {pending}")
        if total > 0:
            print(f"Completion Rate: {(completed/total)*100:.1f}%")
        print("="*50)

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("TO-DO LIST APPLICATION - COMMAND LINE")
    print("="*50)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Update Task")
    print("6. Mark Task as Completed")
    print("7. Delete Task")
    print("8. View Statistics")
    print("9. Exit")
    print("="*50)

def main():
    """Main function to run the CLI application"""
    todo = TodoListCLI()
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            title = input("Enter task title: ").strip()
            description = input("Enter task description (optional): ").strip()
            priority = input("Enter priority (Low/Medium/High) [Medium]: ").strip() or 'Medium'
            todo.add_task(title, description, priority)
        
        elif choice == '2':
            todo.view_tasks()
        
        elif choice == '3':
            todo.view_tasks('Pending')
        
        elif choice == '4':
            todo.view_tasks('Completed')
        
        elif choice == '5':
            try:
                task_id = int(input("Enter task ID to update: "))
                print("Leave blank to keep current value")
                title = input("Enter new title: ").strip() or None
                description = input("Enter new description: ").strip() or None
                priority = input("Enter new priority: ").strip() or None
                todo.update_task(task_id, title, description, priority)
            except ValueError:
                print("✗ Invalid task ID!")
        
        elif choice == '6':
            try:
                task_id = int(input("Enter task ID to mark as completed: "))
                todo.mark_complete(task_id)
            except ValueError:
                print("✗ Invalid task ID!")
        
        elif choice == '7':
            try:
                task_id = int(input("Enter task ID to delete: "))
                confirm = input(f"Are you sure you want to delete task #{task_id}? (y/n): ")
                if confirm.lower() == 'y':
                    todo.delete_task(task_id)
            except ValueError:
                print("✗ Invalid task ID!")
        
        elif choice == '8':
            todo.get_statistics()
        
        elif choice == '9':
            print("\nThank you for using To-Do List Application!")
            break
        
        else:
            print("✗ Invalid choice! Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
