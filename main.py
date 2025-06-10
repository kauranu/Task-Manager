import customtkinter as ctk
import json
import os

FILENAME = "tasks.json"


def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✅ Task Manager")
        height = 600
        width = 500
        self.geometry(f"{width}x{height}+{(self.winfo_screenwidth() - width) // 2}+{(self.winfo_screenheight() - height) // 2}")    
        self.resizable(False, False)
        self.configure(fg_color="#333333")
        self.tasks = load_tasks()
        self.create_widgets()
        self.update_task_list()
        

    def create_widgets(self):
    
        self.title_label = ctk.CTkLabel(self, text="My Task List ✅", font=("Arial", 30, "bold"), text_color="#ffb9f5" )
        self.title_label.pack(pady=20)

    
        self.task_listbox = ctk.CTkTextbox(self, height=300, width=450,font=("Arial", 20),fg_color="#1E1E1E",text_color="white", border_color="#DF95EB", border_width=2)
        self.task_listbox.pack(pady=10)
        self.task_listbox.configure(state="disabled")
        


        self.task_entry = ctk.CTkEntry(self, placeholder_text="Enter new task...", font=("Arial", 10), fg_color="#1E1E1E", text_color="white", border_color="#D6C7B9", border_width=2)
        self.task_entry.pack(pady=10)

        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        button_width = 100
        button_height = 40
        
        self.add_button = ctk.CTkButton(button_frame, text="➕ Add Task", command=self.add_task, width=button_width, height=button_height, fg_color="#CA85E2", hover_color="#8D0BA1", border_color="#49263b", border_width=2,text_color="black")
        self.add_button.grid(row=0, column=0, padx=5)

        self.complete_button = ctk.CTkButton(button_frame, text="✅ Complete", command=self.mark_task_completed, width=button_width, height=button_height, fg_color="#CA85E2", hover_color="#8D0BA1", border_color="#49263b", border_width=2, text_color="black")
        self.complete_button.grid(row=0, column=1, padx=5)

        self.delete_button = ctk.CTkButton(button_frame, text="🗑️ Delete", command=self.delete_task, width=button_width, height=button_height,fg_color="#CA85E2", hover_color="#8D0BA1", border_color="#49263b", border_width=2, text_color="black")
        self.delete_button.grid(row=0, column=2, padx=5)

        self.update_button = ctk.CTkButton(button_frame, text="✏️ Update", command=self.update_task , width=button_width, height=button_height,fg_color="#CA85E2", hover_color="#8D0BA1", border_color="#49263b", border_width=2, text_color="black")
        self.update_button.grid(row=0, column=3, padx=5)

    def update_task_list(self):
        
        self.task_listbox.configure(state="normal")
        self.task_listbox.delete("1.0", "end")
        for idx, task in enumerate(self.tasks):
            status = "✅" if task["completed"] else "⏳"
            self.task_listbox.insert("end", f"{idx+1}. {status} {task['name']}\n")
        self.task_listbox.configure(state="disabled")

    def add_task(self):
        task_name = self.task_entry.get().strip()
        if task_name:
            self.tasks.append({"name": task_name, "completed": False})
            save_tasks(self.tasks)
            self.task_entry.delete(0, "end")
            self.update_task_list()
            
    def mark_task_completed(self):
        task_number = self.get_selected_task_number()
        if task_number is not None:
            self.tasks[task_number]["completed"] = True
            save_tasks(self.tasks)
            self.update_task_list()

    def delete_task(self):
        task_number = self.get_selected_task_number()
        if task_number is not None:
            del self.tasks[task_number]
            save_tasks(self.tasks)
            self.update_task_list()
    def update_task(self):
        task_number = self.get_selected_task_number()
        if task_number is not None:
            new_name = ctk.CTkInputDialog(text="Enter new task name:", title="Update Task",).get_input()
            if new_name:
                self.tasks[task_number]["name"] = new_name
                save_tasks(self.tasks)
                self.update_task_list()
            else:
                ctk.CTkMessageBox.show_error("Error", "Task name cannot be empty.")

            
            
            
    def get_selected_task_number(self):
        try:
            number = int(ctk.CTkInputDialog(text="Enter task number:", title="Select Task").get_input())
            return number - 1 if 0 < number <= len(self.tasks) else None
        except:
            return None
            
            
def task():
    tasks=load_tasks()
    print("--welcome to the task manager--")
    
    if not tasks:
        total_tasks = int(input("Enter the number of tasks you want to add: "))
        for i in range(1, total_tasks + 1):
            task_name = input(f"Enter the name of task {i}: ")
            tasks.append({"name": task_name, "completed": False})
        save_tasks(tasks)
        
    print("\nToday's tasks:")
    for i, task in enumerate(tasks, 1):
        status = "✔" if task["completed"] else "✘"
        print(f"{i}. [{status}] {task['name']}")
    
    while True:
        operation = int(input("\nEnter:\n1 - Add a task\n2 - Update a task\n3 - Delete a task\n4 - View tasks\n5 - Mark task as completed\n6 - Exit\n"))
        
        
        if operation == 1:
            add = input("Enter the task you want to add: ")
            tasks.append({"name": add, "completed": False})
            save_tasks(tasks)
            print(f"Task '{add}' has been added successfully.")
            
            
            
        elif operation == 2:
            update_val = input("Enter the task you want to update: ")
            found = False
            for task in tasks:
                if task["name"] == update_val:
                    new_name = input("Enter the new task name: ")
                    task["name"] = new_name
                    print(f"Task updated to: '{new_name}'")
                    found = True
                    save_tasks(tasks)
                    break
            if not found:
                print(f"Task '{update_val}' not found.")
                
                

        elif operation == 3:
            delete_val = input("Enter the task you want to delete: ")
            for task in tasks:
                if task["name"] == delete_val:
                    tasks.remove(task)
                    save_tasks(tasks)
                    print(f"Task '{delete_val}' has been deleted.")
                    break
            else:
                print(f"Task '{delete_val}' not found.")
                
                
                
        elif operation == 4:
            print("\nToday's tasks:")
            for i, task in enumerate(tasks, 1):
                status = "✔" if task["completed"] else "✘"
                print(f"{i}. [{status}] {task['name']}")
                
        elif operation == 5:
            task_to_mark = input("Enter the name of the task to mark as completed: ")
            for task in tasks:
                if task["name"] == task_to_mark:
                    task["completed"] = True
                    save_tasks(tasks)
                    print(f"Task '{task_to_mark}' marked as completed.")
                    break
            else:
                print(f"Task '{task_to_mark}' not found.")
                
        elif operation == 6:
            save_tasks(tasks)
            print("Exiting Task Manager. Goodbye!")
            break

        else:
            print("Invalid operation. Please try again.")


if __name__ == "__main__":
    mode = input("Enter mode (gui / cli): ").strip().lower()

    if mode == "cli":
        task()
    else:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        app = TaskManagerApp()
        app.mainloop()


