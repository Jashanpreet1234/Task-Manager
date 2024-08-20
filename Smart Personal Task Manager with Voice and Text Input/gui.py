import tkinter as tk
from tkinter import messagebox, ttk
import threading
import speech_recognition as sr

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task, priority):
        self.tasks.append({"task": task, "priority": priority})

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def move_task_up(self, index):
        if index > 0:
            self.tasks[index], self.tasks[index - 1] = self.tasks[index - 1], self.tasks[index]

    def move_task_down(self, index):
        if index < len(self.tasks) - 1:
            self.tasks[index], self.tasks[index + 1] = self.tasks[index + 1], self.tasks[index]

    def get_tasks(self):
        return [(index, task["task"], task["priority"]) for index, task in enumerate(self.tasks)]

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return ""
            except sr.RequestError:
                print("Could not request results; check your network connection.")
                return ""
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                return ""

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Manager")
        
        # Configure for mobile-friendly resizing
        self.root.geometry("400x550")
        self.root.minsize(300, 450)
        self.root.configure(bg='#F4E1D2')  # Soft peachy background

        self.manager = TaskManager()
        self.voice_input = VoiceInput()

        self.create_widgets()

        # Bind arrow keys to move tasks up and down
        self.root.bind('<Up>', self.move_task_up)
        self.root.bind('<Down>', self.move_task_down)

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="Task Manager", font=("Helvetica", 20, "bold"), bg='#F4E1D2')  # soft peachy
        title_label.pack(pady=10)

        # Task list display
        self.task_list = tk.Listbox(self.root, height=10, font=("Helvetica", 12), selectmode=tk.SINGLE, bg='#ffffff', fg='#4A4A4A', bd=0, highlightthickness=0, relief='flat')
        self.task_list.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Task input frame
        input_frame = tk.Frame(self.root, bg='#F4E1D2')  # soft peachy
        input_frame.pack(pady=10, fill=tk.X)

        # Task input entry
        self.entry = tk.Entry(input_frame, width=20, font=("Helvetica", 12), bg='#ffffff', fg='#4A4A4A', relief='flat', bd=1)
        self.entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        input_frame.grid_columnconfigure(0, weight=1)

        # Priority dropdown
        self.priority_var = tk.StringVar(value="Normal")
        priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["Low", "Normal", "High"], font=("Helvetica", 12), state="readonly", width=10)
        priority_menu.grid(row=0, column=1, padx=5, pady=5)

        # Button for adding tasks
        add_btn = tk.Button(input_frame, text="Add Task", font=("Helvetica", 12), command=self.add_task, bg='#81c784', fg='#ffffff', relief='flat')  # Light pastel MINT
        add_btn.grid(row=0, column=2, padx=5, pady=5)

        # Button for voice input
        voice_btn = tk.Button(input_frame, text="Voice Input", font=("Helvetica", 12), command=self.add_task_by_voice, bg='#64b5f6', fg='#ffffff', relief='flat')  # Light pastel blue
        voice_btn.grid(row=0, column=3, padx=5, pady=5)

        # Button to delete tasks
        delete_btn = tk.Button(input_frame, text="Delete Task", font=("Helvetica", 12), command=self.delete_task, bg='#e57373', fg='#ffffff', relief='flat')  # Light pastel red
        delete_btn.grid(row=0, column=4, padx=5, pady=5)

        # Button to trigger analytics
        analytics_btn = tk.Button(self.root, text="Show Task Analytics", font=("Helvetica", 12), command=self.show_analytics, bg='#543310', fg='#ffffff', relief='flat')  # Light pastel yellow
        analytics_btn.pack(pady=10, fill=tk.X)

        # Instructions for shortcuts
        shortcut_label = tk.Label(self.root, text="Use Up/Down arrows to move tasks", font=("Helvetica", 8, "italic"), bg='#d7ccc8', fg='#5d4037')
        shortcut_label.pack(pady=5)

        # Initially update the task list
        self.update_task_list()

    def add_task(self):
        task = self.entry.get()
        priority = self.priority_var.get()
        if task:
            self.manager.add_task(task, priority)
            self.entry.delete(0, tk.END)  # Clear entry field after adding the task
            self.update_task_list()
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def add_task_by_voice(self):
        threading.Thread(target=self._add_task_by_voice_thread).start()

    def _add_task_by_voice_thread(self):
        task = self.voice_input.listen()
        if task:
            priority = self.priority_var.get()
            self.manager.add_task(task, priority)
            self.update_task_list()
        else:
            messagebox.showwarning("Voice Input Error", "No task detected or recognized. Please try again.")

    def delete_task(self):
        selected_task_index = self.task_list.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.manager.delete_task(task_index)
            self.update_task_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def move_task_up(self, event=None):
        selected_task_index = self.task_list.curselection()
        if selected_task_index and selected_task_index[0] > 0:
            task_index = selected_task_index[0]
            self.manager.move_task_up(task_index)
            self.update_task_list()
            self.task_list.selection_set(task_index - 1)  # Move selection up

    def move_task_down(self, event=None):
        selected_task_index = self.task_list.curselection()
        if selected_task_index and selected_task_index[0] < len(self.task_list.get(0, tk.END)) - 1:
            task_index = selected_task_index[0]
            self.manager.move_task_down(task_index)
            self.update_task_list()
            self.task_list.selection_set(task_index + 1)  # Move selection down

    def update_task_list(self):
        tasks = self.manager.get_tasks()
        self.task_list.delete(0, tk.END)
        for task in tasks:
            self.task_list.insert(tk.END, f"{task[1]} (Priority: {task[2]})")

    def show_analytics(self):
        task_count = len(self.manager.get_tasks())
        priorities = [task["priority"] for task in self.manager.tasks]
        priority_distribution = {priority: priorities.count(priority) for priority in set(priorities)}

        # Creating a simple message to display the analytics
        analytics_message = f"Total tasks: {task_count}\n\nPriority distribution:\n"
        for priority, count in priority_distribution.items():
            analytics_message += f"{priority}: {count}\n"

        messagebox.showinfo("Task Analytics", analytics_message)

if __name__ == "__main__":
    root = tk.Tk()
    gui = TaskManagerGUI(root)
    root.mainloop()
