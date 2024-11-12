"""
Group four
Najjuma Teopista S23b23/041  
Lakica leticia M23B23/023 
Mukama Joseph S23B23/036  


 Enums for task categorization
ENUM TaskType:
    ACADEMIC
    PERSONAL

ENUM TaskPriority:
    HIGH
    MEDIUM
    LOW

 Task Class Definition
CLASS Task:
    PROPERTIES:
        title: string
        task_type: TaskType
        priority: TaskPriority
        start_time: datetime
        end_time: datetime
        completed: boolean = false
        reminded: boolean = false

    METHOD to_dict():
        RETURN dictionary representation of task

 Main Scheduling Assistant Class
CLASS SchedulingAssistant:
    PROPERTIES:
        tasks: List<Task>

    METHOD init():
        load_tasks()

    METHOD add_task(task):
        ADD task to tasks list
        SORT tasks by priority and start_time
        save_tasks()

    METHOD save_tasks():
        WRITE tasks to JSON file

    METHOD load_tasks():
        IF tasks file exists:
            READ JSON file
            FOR EACH task_data in file:
                CREATE new Task from data
                ADD to tasks list

    METHOD delete_task(title):
        REMOVE task with matching title
        save_tasks()

    METHOD send_reminders():
        FOR EACH task in tasks:
            IF not reminded AND task starts within 24 hours:
                DISPLAY reminder message
                MARK task as reminded
                save_tasks()

    METHOD get_busy_slots():
        RETURN list of time slots with task durations

    METHOD generate_gantt_chart():
        CREATE new chart
        FOR EACH task:
            DRAW horizontal bar for task duration
            ADD task title label
        DISPLAY chart

 GUI Class
CLASS SchedulerGUI:
    PROPERTIES:
        scheduler: SchedulingAssistant
        root: Window
        task_list: TreeView
        input_fields: Various Entry and Combo widgets

    METHOD init():
        CREATE main window
        CREATE task list frame
        CREATE task entry frame
        CREATE analysis frame
        UPDATE task list display

    METHOD create_task_list_frame():
        CREATE treeview for tasks
        ADD columns for task properties
        ADD delete button

    METHOD create_task_entry_frame():
        CREATE input fields:
            - Title entry
            - Type dropdown
            - Priority dropdown
            - Start time entry
            - End time entry
        ADD "Add Task" button

    METHOD create_analysis_frame():
        ADD buttons:
            - Optimize Schedule
            - Analyze Busy Slots
            - Send Reminders
            - Generate Gantt Chart

    METHOD add_task():
        GET values from input fields
        VALIDATE input times
        IF valid:
            CREATE new Task
            ADD to scheduler
            UPDATE display
            SHOW success message
        ELSE:
            SHOW error message

    METHOD delete_selected_task():
        GET selected task
        IF task selected:
            DELETE from scheduler
            UPDATE display
        ELSE:
            SHOW warning message

    METHOD update_task_list():
        CLEAR current display
        FOR EACH task in scheduler:
            ADD task to treeview

    METHOD analyze_busy_slots():
        GET busy slots from scheduler
        CREATE bar chart
        DISPLAY in window

    METHOD optimize_schedule():
        DISPLAY optimization message

 Main Program
PROGRAM main:
    CREATE root window
    CREATE SchedulerGUI instance
    RUN application  """
import datetime
from typing import List, Dict
import tkinter as tk
from tkinter import ttk, messagebox
import json
from enum import Enum
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class TaskType(Enum):
    ACADEMIC = "Academic"
    PERSONAL = "Personal"

class TaskPriority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low" 



class Task:
    def __init__(self, title: str, task_type: TaskType, priority: TaskPriority,
                 start_time: datetime.datetime, end_time: datetime.datetime):
        self.title = title
        self.task_type = task_type
        self.priority = priority
        self.start_time = start_time
        self.end_time = end_time
        self.completed = False
        self.reminded = False

    def to_dict(self):
        return {
            "title": self.title,
            "task_type": self.task_type.value,
            "priority": self.priority.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "completed": self.completed,
            "reminded": self.reminded
        }

class SchedulingAssistant:
    def __init__(self):
        self.tasks: List[Task] = []
        self.load_tasks()

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: (x.priority, x.start_time))
        self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                for task_data in tasks:
                    task = Task(
                        title=task_data["title"],
                        task_type=TaskType(task_data["task_type"]),
                        priority=TaskPriority(task_data["priority"]),
                        start_time=datetime.datetime.fromisoformat(task_data["start_time"]),
                        end_time=datetime.datetime.fromisoformat(task_data["end_time"]),
                    )
                    task.completed = task_data.get("completed", False)
                    task.reminded = task_data.get("reminded", False)
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def delete_task(self, title: str):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def send_reminders(self):
        for task in self.tasks:
            if not task.reminded and task.start_time - datetime.datetime.now() <= datetime.timedelta(hours=24):
                messagebox.showinfo(f"Reminder for Task", f"{task.title} is due soon!")
                task.reminded = True
                self.save_tasks()

    def get_busy_slots(self) -> List[Dict]:
        busy_slots = []
        for task in self.tasks:
            busy_slots.append({
                "start": task.start_time,
                "end": task.end_time,
                "load": (task.end_time - task.start_time).total_seconds() / 3600
            })
        return busy_slots

    def generate_gantt_chart(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        for task in self.tasks:
            ax.barh(
                task.task_type.value,
                (task.end_time - task.start_time).total_seconds() / 3600,
                left=task.start_time.timestamp(),
                height=0.5,
                color="skyblue" if task.priority == TaskPriority.HIGH else "lightgrey"
            )
            ax.text(
                task.start_time.timestamp() + (task.end_time - task.start_time).total_seconds() / 7200,
                task.task_type.value,
                task.title,
                va='center', ha='center', fontsize=8
            )

        ax.set_xlabel('Time')
        ax.set_ylabel('Task Type')
        ax.set_title('Task Schedule Gantt Chart')
        ax.grid(True)
        plt.show()

class SchedulerGUI:
    def __init__(self, root):
        self.scheduler = SchedulingAssistant()
        self.root = root
        self.root.title("Personal Scheduling Assistant")
        self.root.geometry("1000x600")
        self.root.configure(bg="#F7F7F7")

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_task_list_frame()
        self.create_task_entry_frame()
        self.create_analysis_frame()
        self.update_task_list()

    def create_task_list_frame(self):
        task_list_frame = ttk.LabelFrame(self.main_frame, text="Task List", padding="5")
        task_list_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.tree = ttk.Treeview(task_list_frame, columns=("Title", "Type", "Priority", "Start Time", "End Time", "Status"), show='headings')
        self.tree.heading("Title", text="Title")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Start Time", text="Start Time")
        self.tree.heading("End Time", text="End Time")
        self.tree.heading("Status", text="Status")
        self.tree.grid(row=0, column=0, columnspan=2)

        delete_button = ttk.Button(task_list_frame, text="Delete Selected Task", command=self.delete_selected_task)
        delete_button.grid(row=1, column=0, columnspan=2, pady=5)

    def create_task_entry_frame(self):
        entry_frame = ttk.LabelFrame(self.main_frame, text="Add New Task", padding="5")
        entry_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(entry_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        self.title_entry = ttk.Entry(entry_frame, width=30)
        self.title_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(entry_frame, text="Type:").grid(row=1, column=0, sticky=tk.W)
        self.type_combo = ttk.Combobox(entry_frame, values=[t.value for t in TaskType], state="readonly")
        self.type_combo.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(entry_frame, text="Priority:").grid(row=2, column=0, sticky=tk.W)
        self.priority_combo = ttk.Combobox(entry_frame, values=[p.value for p in TaskPriority], state="readonly")
        self.priority_combo.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(entry_frame, text="Start Time (YYYY-MM-DD HH:MM):").grid(row=3, column=0, sticky=tk.W)
        self.start_time_entry = ttk.Entry(entry_frame, width=20)
        self.start_time_entry.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(entry_frame, text="End Time (YYYY-MM-DD HH:MM):").grid(row=4, column=0, sticky=tk.W)
        self.end_time_entry = ttk.Entry(entry_frame, width=20)
        self.end_time_entry.grid(row=4, column=1, sticky=tk.W)

        ttk.Button(entry_frame, text="Add Task", command=self.add_task).grid(row=5, column=0, columnspan=2, pady=5)

    def add_task(self):
        title = self.title_entry.get()
        task_type = TaskType(self.type_combo.get())
        priority = TaskPriority(self.priority_combo.get())

        try:
            start_time = datetime.datetime.strptime(self.start_time_entry.get(), "%Y-%m-%d %H:%M")
            end_time = datetime.datetime.strptime(self.end_time_entry.get(), "%Y-%m-%d %H:%M")
            if start_time >= end_time:
                raise ValueError("End time must be after start time.")
            task = Task(title, task_type, priority, start_time, end_time)
            self.scheduler.add_task(task)
            self.update_task_list()
            messagebox.showinfo("Success", "Task added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def create_analysis_frame(self):
        analysis_frame = ttk.LabelFrame(self.main_frame, text="Analysis and Visualization", padding="5")
        analysis_frame.grid(row=2, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        ttk.Button(analysis_frame, text="Optimize Schedule", command=self.optimize_schedule).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(analysis_frame, text="Analyze Busy Slots", command=self.analyze_busy_slots).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(analysis_frame, text="Send Reminders", command=self.scheduler.send_reminders).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(analysis_frame, text="Generate Gantt Chart", command=self.scheduler.generate_gantt_chart).grid(row=0, column=3, padx=5, pady=5)

    def delete_selected_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No task selected!")
            return
        task_title = self.tree.item(selected_item[0])["values"][0]
        self.scheduler.delete_task(task_title)
        self.update_task_list()

    def update_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.scheduler.tasks:
            self.tree.insert("", "end", values=(
                task.title,
                task.task_type.value,
                task.priority.value,
                task.start_time.strftime("%Y-%m-%d %H:%M"),
                task.end_time.strftime("%Y-%m-%d %H:%M"),
                "Completed" if task.completed else "Pending"
            ))

    def analyze_busy_slots(self):
        busy_slots = self.scheduler.get_busy_slots()
        fig, ax = plt.subplots(figsize=(10, 4))
        time_slots = [slot["start"].strftime("%H:%M") for slot in busy_slots]
        load = [slot["load"] for slot in busy_slots]
        ax.bar(time_slots, load, color="skyblue")
        ax.set_xlabel("Time Slot")
        ax.set_ylabel("Load (Hours)")
        ax.set_title("Busy Time Slots Analysis")
        
        canvas = FigureCanvasTkAgg(fig, self.root)
        canvas.get_tk_widget().grid(row=3, column=0, sticky=(tk.W, tk.E))
        canvas.draw()

    def optimize_schedule(self):
        messagebox.showinfo("Optimize Schedule", "Optimized task scheduling based on priority.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerGUI(root)
    app.run()
