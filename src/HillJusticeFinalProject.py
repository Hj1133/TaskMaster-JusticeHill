import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class TaskMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster")

        # Data structure to store tasks
        self.tasks = []
        self.categories = ["Work", "Personal", "Study"]

        # Create the main GUI components
        self.create_menu_bar()
        self.create_task_list()
        self.add_images()

    # Modularized: Function to create the menu bar
    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Task", command=self.open_task_form)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        report_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Reports", menu=report_menu)
        report_menu.add_command(label="Task Summary", command=self.show_summary_report)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Manage Categories", command=self.open_category_settings)

    # Modularized: Function to create the task list table
    def create_task_list(self):
        columns = ("Name", "Category", "Deadline", "Priority", "Status")

        self.task_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.task_tree.heading("Name", text="Task Name")
        self.task_tree.heading("Category", text="Category")
        self.task_tree.heading("Deadline", text="Deadline")
        self.task_tree.heading("Priority", text="Priority")
        self.task_tree.heading("Status", text="Status")

        self.task_tree.pack(fill="both", expand=True)

        # Add Buttons for Actions
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x")

        tk.Button(button_frame, text="Edit Task", command=self.edit_task).pack(side="left", padx=5, pady=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5, pady=5)
        tk.Button(button_frame, text="Mark as Completed", command=self.mark_task_completed).pack(side="left", padx=5, pady=5)

    # Adding Images: Load images from the specific folder path
    def add_images(self):
        # Hardcoded path to the images folder
        images_folder = r"C:\Users\justi\TaskMaster-JusticeHill\images"

        # Image placeholder 1
        # Alt text: "Task Manager Icon"
        try:
            img1_path = f"{images_folder}\\task_icon.png"
            img1 = tk.PhotoImage(file=img1_path)
            img_label1 = tk.Label(self.root, image=img1)
            img_label1.photo = img1  # Keep a reference to the image to prevent it from being garbage collected
            img_label1.pack(side="right", padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image 1: {e}")

        # Image placeholder 2
        # Alt text: "Task List Background"
        try:
            img2_path = f"{images_folder}\\task_list_bg.png"
            img2 = tk.PhotoImage(file=img2_path)
            img_label2 = tk.Label(self.root, image=img2)
            img_label2.photo = img2
            img_label2.pack(side="left", padx=5, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image 2: {e}")

    # Modularized: Open the task form window
    def open_task_form(self, task_index=None):
        self.task_form = tk.Toplevel(self.root)
        self.task_form.title("New Task" if task_index is None else "Edit Task")

        # Task Name
        tk.Label(self.task_form, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.task_name_var = tk.StringVar()
        tk.Entry(self.task_form, textvariable=self.task_name_var).grid(row=0, column=1, padx=5, pady=5)

        # Category Dropdown
        tk.Label(self.task_form, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar(value=self.categories[0])
        tk.OptionMenu(self.task_form, self.category_var, *self.categories).grid(row=1, column=1, padx=5, pady=5)

        # Deadline
        tk.Label(self.task_form, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.deadline_var = tk.StringVar()
        tk.Entry(self.task_form, textvariable=self.deadline_var).grid(row=2, column=1, padx=5, pady=5)

        # Priority
        tk.Label(self.task_form, text="Priority:").grid(row=3, column=0, padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        tk.Radiobutton(self.task_form, text="High", variable=self.priority_var, value="High").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(self.task_form, text="Medium", variable=self.priority_var, value="Medium").grid(row=3, column=1)
        tk.Radiobutton(self.task_form, text="Low", variable=self.priority_var, value="Low").grid(row=3, column=1, sticky="e")

        if task_index is not None:
            task = self.tasks[task_index]
            self.task_name_var.set(task["name"])
            self.category_var.set(task["category"])
            self.deadline_var.set(task["deadline"])
            self.priority_var.set(task["priority"])

        if task_index is None:
            tk.Button(self.task_form, text="Add Task", command=self.add_task).grid(row=4, column=0, padx=5, pady=5)
        else:
            tk.Button(self.task_form, text="Save Changes", command=lambda: self.save_task_changes(task_index)).grid(row=4, column=0, padx=5, pady=5)

        tk.Button(self.task_form, text="Cancel", command=self.task_form.destroy).grid(row=4, column=1, padx=5, pady=5)

    # Add task with improved input validation
    def add_task(self):
        task_name = self.task_name_var.get()
        category = self.category_var.get()
        deadline = self.deadline_var.get()
        priority = self.priority_var.get()
        status = "Pending"

        # Enhanced Input Validation
        if not task_name or not deadline or not category:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Deadline must be in YYYY-MM-DD format.")
            return

        self.tasks.append({"name": task_name, "category": category, "deadline": deadline, "priority": priority, "status": status})
        self.update_task_list()
        self.task_form.destroy()

    # Update task list table
    def update_task_list(self):
        for i in self.task_tree.get_children():
            self.task_tree.delete(i)
        for task in self.tasks:
            self.task_tree.insert("", "end", values=(task["name"], task["category"], task["deadline"], task["priority"], task["status"]))

    def edit_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to edit.")
            return
        task_index = self.task_tree.index(selected_item)
        self.open_task_form(task_index)

    def save_task_changes(self, task_index):
        task_name = self.task_name_var.get()
        category = self.category_var.get()
        deadline = self.deadline_var.get()
        priority = self.priority_var.get()

        if not task_name or not deadline or not category:
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Deadline must be in YYYY-MM-DD format.")
            return

        self.tasks[task_index] = {"name": task_name, "category": category, "deadline": deadline, "priority": priority, "status": self.tasks[task_index]["status"]}
        self.update_task_list()
        self.task_form.destroy()

    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to delete.")
            return
        task_index = self.task_tree.index(selected_item)
        del self.tasks[task_index]
        self.update_task_list()

    def mark_task_completed(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to mark as completed.")
            return
        task_index = self.task_tree.index(selected_item)
        self.tasks[task_index]["status"] = "Completed"
        self.update_task_list()

    # Summary Report
    def show_summary_report(self):
        completed_tasks = len([task for task in self.tasks if task["status"] == "Completed"])
        pending_tasks = len(self.tasks) - completed_tasks
        report_message = f"Completed Tasks: {completed_tasks}\nPending Tasks: {pending_tasks}"
        messagebox.showinfo("Task Summary", report_message)

    # Manage Categories
    def open_category_settings(self):
        self.category_form = tk.Toplevel(self.root)
        self.category_form.title("Manage Categories")

        tk.Label(self.category_form, text="Categories:").pack(padx=10, pady=5)

        self.category_listbox = tk.Listbox(self.category_form)
        self.category_listbox.pack(padx=10, pady=5)

        for category in self.categories:
            self.category_listbox.insert("end", category)

        tk.Button(self.category_form, text="Add Category", command=self.add_category).pack(padx=10, pady=5)
        tk.Button(self.category_form, text="Delete Category", command=self.delete_category).pack(padx=10, pady=5)

    def add_category(self):
        new_category = simpledialog.askstring("Add Category", "Category Name:")
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.category_listbox.insert("end", new_category)

    def delete_category(self):
        selected_category = self.category_listbox.curselection()
        if not selected_category:
            messagebox.showerror("Error", "Please select a category to delete.")
            return
        category_index = selected_category[0]
        del self.categories[category_index]
        self.category_listbox.delete(category_index)


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskMasterApp(root)
    root.mainloop()