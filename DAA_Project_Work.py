'''
GROUP FOUR DAA PROJECT
1. S23B23/041 Najjuma Teopista B24271
2. M23B23/023 Lakica Leticia B20720
3. S23B23/036 Mukama Joseph B24267
// Import required libraries
IMPORT datetime, tkinter, json, matplotlib, enum

// Task Type and Priority Enums
CREATE TaskType ENUM:
    SET ACADEMIC = "Academic"
    SET PERSONAL = "Personal"
    SET WORK = "Work"

CREATE TaskPriority ENUM:
    SET HIGH = "High"
    SET MEDIUM = "Medium"
    SET LOW = "Low"

// Task Class Definition
CLASS Task:
    FUNCTION __init__(title, task_type, priority, start_time, end_time):
        SET self.title = title
        SET self.task_type = task_type
        SET self.priority = priority
        SET self.start_time = start_time
        SET self.end_time = end_time
        SET self.completed = FALSE
        SET self.reminded = FALSE

    FUNCTION to_dict():
        RETURN {
            title: self.title,
            task_type: self.task_type.value,
            priority: self.priority.value,
            start_time: self.start_time as ISO format,
            end_time: self.end_time as ISO format,
            completed: self.completed,
            reminded: self.reminded
        }

// Scheduling Assistant Class Definition
CLASS SchedulingAssistant:
    FUNCTION __init__():
        SET self.tasks = empty list
        CALL self.load_tasks()

    FUNCTION add_task(task):
        ADD task to self.tasks
        CALL merge_sort on self.tasks  // Sort by priority and time
        CALL save_tasks()

    FUNCTION save_tasks():
        OPEN "tasks.json" in write mode
        WRITE tasks to file as JSON

    FUNCTION load_tasks():
        TRY:
            READ "tasks.json"
            FOR each task_data in file:
                CREATE new Task object
                SET task properties
                ADD task to self.tasks
        CATCH FileNotFound or JSONError:
            SET self.tasks to empty list

    FUNCTION merge_sort(tasks):
        IF length of tasks ≤ 1:
            RETURN tasks
        
        SET mid = length of tasks / 2
        SET left_half = merge_sort(tasks[0 to mid])
        SET right_half = merge_sort(tasks[mid to end])
        RETURN merge(left_half, right_half)

    FUNCTION merge(left, right):
        SET result = empty list
        WHILE left and right not empty:
            IF compare_tasks(left[0], right[0]) ≤ 0:
                ADD left[0] to result
                REMOVE first element from left
            ELSE:
                ADD right[0] to result
                REMOVE first element from right
        ADD remaining elements from left to result
        ADD remaining elements from right to result
        RETURN result

    FUNCTION compare_tasks(task1, task2):
        IF task1.priority ≠ task2.priority:
            RETURN compare_priority(task1.priority, task2.priority)
        RETURN time difference between task1 and task2 start times

    FUNCTION generate_gantt_chart():
        IF tasks is empty:
            SHOW message "No tasks to display"
            RETURN
        
        CREATE new matplotlib figure
        SET color map for priorities
        FOR each task in sorted tasks:
            CALCULATE task duration
            DRAW horizontal bar for task
            ADD task details as text
        FORMAT chart axes and labels
        DISPLAY chart

    FUNCTION get_busy_slots():
        SET busy_slots = empty list
        FOR each task in tasks:
            ADD {start, end, duration} to busy_slots
        RETURN busy_slots

    FUNCTION send_reminders():
        SET current_time = now
        FOR each task in tasks:
            IF not reminded AND starts within 24 hours:
                SHOW reminder message
                SET task.reminded = TRUE
        CALL save_tasks()

// GUI Class Definition
CLASS SchedulerGUI:
    FUNCTION __init__(root):
        CREATE SchedulingAssistant instance
        SET root window properties
        CALL create_widgets()

    FUNCTION create_widgets():
        CREATE main frame
        
        // Create Task List Section
        CREATE task list frame with TreeView
        ADD columns for task properties
        ADD delete button
        
        // Create Task Entry Section
        CREATE entry frame
        ADD input fields:
            - Title entry
            - Type dropdown
            - Priority dropdown
            - Start time entry
            - End time entry
        ADD "Add Task" button
        
        // Create Analysis Section
        CREATE analysis frame
        ADD buttons:
            - Gantt Chart
            - Reminders
            - Busy Slots Analysis
        
        CALL update_task_list()

    FUNCTION add_task():
        TRY:
            GET values from all entry fields
            CREATE new Task object
            VALIDATE time entries
            ADD task to scheduler
            UPDATE display
            SHOW success message
        CATCH error:
            SHOW error message

    FUNCTION delete_selected_task():
        GET selected task
        IF task selected:
            GET task title
            DELETE from scheduler
            UPDATE display
        ELSE:
            SHOW warning message

    FUNCTION update_task_list():
        CLEAR tree view
        FOR each task in scheduler:
            ADD task details to tree view

    FUNCTION analyze_busy_slots():
        GET busy slots from scheduler
        CREATE bar chart
        SET chart properties
        DISPLAY chart

// Main Program Execution
FUNCTION main():
    CREATE root window
    CREATE SchedulerGUI instance
    START main event loop

IF this is main module:
    CALL main()

// Program Flow
1. START program
2. Initialize GUI and Scheduler
3. LOOP until program exit:
    - HANDLE user input events
    - UPDATE task list as needed
    - SAVE changes to file
    - DISPLAY visualizations when requested
4. END program '''

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
import matplotlib.dates as mdates

class TaskType(Enum):
    ACADEMIC = "Academic"
    PERSONAL = "Personal"
    WORK = "Work"

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
        self.tasks = self.merge_sort(self.tasks)
        self.save_tasks()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                self.tasks = []
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
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def delete_task(self, title: str):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def send_reminders(self):
        now = datetime.datetime.now()
        for task in self.tasks:
            if not task.reminded and task.start_time - now <= datetime.timedelta(hours=24):
                messagebox.showinfo("Reminder", f"{task.title} is due soon!")
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
        if not self.tasks:
            messagebox.showinfo("Gantt Chart", "No tasks to display")
            return

        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Color mapping for priorities
        color_map = {
            TaskPriority.HIGH: 'red', 
            TaskPriority.MEDIUM: 'orange', 
            TaskPriority.LOW: 'green'
        }
        
        # Prepare data
        for i, task in enumerate(sorted(self.tasks, key=lambda x: x.start_time)):
            duration = (task.end_time - task.start_time).total_seconds() / 3600
            color = color_map.get(task.priority, 'blue')
            
            ax.barh(
                task.title, 
                duration, 
                left=mdates.date2num(task.start_time), 
                height=0.5, 
                color=color, 
                alpha=0.7,
                edgecolor='black',
                linewidth=1
            )
            
            # Add task details
            ax.text(
                mdates.date2num(task.start_time) + duration/2, 
                task.title, 
                f"{task.title}\n{task.task_type.value}\n{duration:.1f}h", 
                va='center', 
                ha='center', 
                fontsize=8
            )

        # Format x-axis
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gcf().autofmt_xdate()

        ax.set_title('Task Schedule Gantt Chart')
        ax.set_xlabel('Time')
        ax.set_ylabel('Tasks')
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()

    # Merge Sort Implementation
    def merge_sort(self, tasks: List[Task]) -> List[Task]:
        if len(tasks) <= 1:
            return tasks
        mid = len(tasks) // 2
        left_half = self.merge_sort(tasks[:mid])
        right_half = self.merge_sort(tasks[mid:])
        return self.merge(left_half, right_half)

    def merge(self, left: List[Task], right: List[Task]) -> List[Task]:
        sorted_tasks = []
        while left and right:
            if self.compare_tasks(left[0], right[0]) <= 0:
                sorted_tasks.append(left.pop(0))
            else:
                sorted_tasks.append(right.pop(0))
        sorted_tasks.extend(left)
        sorted_tasks.extend(right)
        return sorted_tasks

    def compare_tasks(self, task1: Task, task2: Task) -> int:
        """Comparison function to order tasks based on priority and start time"""
        if task1.priority != task2.priority:
            return self.compare_priority(task1.priority, task2.priority)
        return (task1.start_time - task2.start_time).total_seconds()

    def compare_priority(self, priority1: TaskPriority, priority2: TaskPriority) -> int:
        """Helper to compare priorities"""
        priority_order = {TaskPriority.HIGH: 3, TaskPriority.MEDIUM: 2, TaskPriority.LOW: 1}
        return priority_order[priority1] - priority_order[priority2]

class SchedulerGUI:
    def __init__(self, root):
        self.scheduler = SchedulingAssistant()
        self.root = root
        self.root.title("Personal Scheduling Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg="#F0F0F0")

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Task List Frame
        task_list_frame = ttk.LabelFrame(main_frame, text="Task List")
        task_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview for Tasks
        self.tree = ttk.Treeview(task_list_frame, columns=(
            "Title", "Type", "Priority", "Start Time", "End Time", "Status"
        ), show='headings')
        
        for col in ["Title", "Type", "Priority", "Start Time", "End Time", "Status"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Delete Button
        delete_btn = ttk.Button(task_list_frame, text="Delete Selected Task", command=self.delete_selected_task)
        delete_btn.pack(pady=5)

        # Task Entry Frame
        entry_frame = ttk.LabelFrame(main_frame, text="Add New Task")
        entry_frame.pack(fill=tk.X, padx=5, pady=5)

        # Entry Fields
        fields = [
            ("Title:", "title_entry"),
            ("Type:", "type_combo"),
            ("Priority:", "priority_combo"),
            ("Start Time (YYYY-MM-DD HH:MM):", "start_time_entry"),
            ("End Time (YYYY-MM-DD HH:MM):", "end_time_entry")
        ]

        for label, attr in fields:
            frame = ttk.Frame(entry_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=label).pack(side=tk.LEFT, padx=5)
            
            if attr == "type_combo":
                setattr(self, attr, ttk.Combobox(frame, values=[t.value for t in TaskType], state="readonly"))
            elif attr == "priority_combo":
                setattr(self, attr, ttk.Combobox(frame, values=[p.value for p in TaskPriority], state="readonly"))
            else:
                setattr(self, attr, ttk.Entry(frame, width=40))
            
            getattr(self, attr).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Add Task Button
        add_task_btn = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_task_btn.pack(pady=5)

        # Analysis Frame
        analysis_frame = ttk.LabelFrame(main_frame, text="Task Analysis")
        analysis_frame.pack(fill=tk.X, padx=5, pady=5)

        analysis_buttons = [
            ("Generate Gantt Chart", self.scheduler.generate_gantt_chart),
            ("Send Reminders", self.scheduler.send_reminders),
            ("Analyze Busy Slots", self.analyze_busy_slots)
        ]

        for label, command in analysis_buttons:
            ttk.Button(analysis_frame, text=label, command=command).pack(side=tk.LEFT, padx=5, pady=5)

        # Initial update
        self.update_task_list()

    def add_task(self):
        try:
            task = Task(
                title=self.title_entry.get(),
                task_type=TaskType(self.type_combo.get()),
                priority=TaskPriority(self.priority_combo.get()),
                start_time=datetime.datetime.strptime(self.start_time_entry.get(), "%Y-%m-%d %H:%M"),
                end_time=datetime.datetime.strptime(self.end_time_entry.get(), "%Y-%m-%d %H:%M")
            )
            
            if task.start_time >= task.end_time:
                raise ValueError("End time must be after start time")
            
            self.scheduler.add_task(task)
            self.update_task_list()
            messagebox.showinfo("Success", "Task added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_selected_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No task selected")
            return
        
        task_title = self.tree.item(selected[0])['values'][0]
        self.scheduler.delete_task(task_title)
        self.update_task_list()

    def update_task_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
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
        
        plt.figure(figsize=(10, 5))
        time_slots = [slot['start'].strftime("%Y-%m-%d %H:%M") for slot in busy_slots]
        loads = [slot['load'] for slot in busy_slots]
        
        plt.bar(time_slots, loads, color='skyblue')
        plt.title('Busy Time Slots')
        plt.xlabel('Time Slot')
        plt.ylabel('Load (Hours)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    root = tk.Tk()
    app = SchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()



























































































































































































































































































































































































































































































































































































































































































































































































































































































































































