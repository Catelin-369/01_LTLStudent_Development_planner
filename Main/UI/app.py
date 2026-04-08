import tkinter as tk
from tkinter import ttk, messagebox

from Services.students import load_data
from UI.dashboard import get_all_students, show_student_profile
from Services.students import add_note, load_data

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Developer Dashboard")
        self.root.geometry("900x500")

        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(search_frame, text="Search:").pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_students)

        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        columns = ("ID", "Name", "School", "Grade", "Classes", "Updated")

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)

        self.tree.pack(fill="both", expand=True)
        tk.Button(button_frame, text="Add Note", command=self.add_note_ui).pack(side="left", padx=5)
        
    def load_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.all_students = get_all_students()  # store all students

        self.display_filtered_students(self.all_students)
        

        students = get_all_students()

        for s in students:
            self.tree.insert("", "end", values=(
                s["id"],
                s["name"],
                s["school"],
                s["grade"],
                ", ".join(s["classes"]),
                s["last_updated"]
            ))
          
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x")

        tk.Button(button_frame, text="View Profile", command=self.view_student).pack(side="left", padx=5, pady=5)
        tk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        tk.Button(button_frame, text="Edit Student", command=self.edit_student).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Student", command=self.delete_student).pack(side="left", padx=5)
        
    def get_selected_student_id(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a student")
            return None

        return self.tree.item(selected[0])["values"][0]

    def add_note_ui(self):
        student_id = self.get_selected_student_id()
        if not student_id:
            return

    popup = tk.Toplevel(self.root)
    popup.title("Add Note")
    popup.geometry("400x300")

    tk.Label(popup, text="Author").pack()
    author_entry = tk.Entry(popup)
    author_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(popup, text="Note").pack()
    note_text = tk.Text(popup, height=8)
    note_text.pack(fill="both", padx=10, pady=5)

    def save_note():
        author = author_entry.get()
        content = note_text.get("1.0", "end").strip()

        if not author or not content:
            messagebox.showerror("Error", "All fields required")
            return

        add_note(student_id, author, content)

        messagebox.showinfo("Success", "Note added!")
        popup.destroy()

    tk.Button(popup, text="Save Note", command=save_note).pack(pady=10)

    def view_student(self):
        student_id = self.get_selected_student_id()
        if not student_id:
            return

        data = load_data()
        student = data["students"][student_id]

        popup = tk.Toplevel(self.root)
        popup.title("Student Profile")
        popup.geometry("400x500")

        info = student["personal_info"]

        notes_text = "\n".join(
            [f"[{n['date']}] {n['author']}: {n['content']}" for n in student["notes"]]
        ) or "No notes yet."

        text = f"""
        Name: {info['first_name']} {info['last_name']}
        Preferred: {info.get('preferred_name', '')}
        Age: {info['age']}
        Grade: {info['grade']}
        School: {info['school']}

        Career Goal: {student['career_goal']}

        Classes: {', '.join(student['classes'])}

        Interests:
        - {'\n- '.join(student['interests'])}

        Strengths:
        - {'\n- '.join(student['strengths'])}

        Notes:
        {notes_text}
        """

        tk.Label(popup, text=text, justify="left").pack(padx=10, pady=10)

from Services.students import delete_student

   def delete_student(self):
       student_id = self.get_selected_student_id()
       if not student_id:
           return

       confirm = messagebox.askyesno("Confirm", "Delete this student?")
       if confirm:
           delete_student(student_id)
           self.load_students()

   def add_student(self):
    popup = tk.Toplevel(self.root)
    popup.title("Add Student")
    popup.geometry("400x600")

    # --- FORM FIELDS ---
    fields = {}

    def create_field(label):
        tk.Label(popup, text=label).pack()
        entry = tk.Entry(popup)
        entry.pack(fill="x", padx=10, pady=5)
        fields[label] = entry

    create_field("First Name")
    create_field("Last Name")
    create_field("Preferred Name")
    create_field("Age")
    create_field("Grade")
    create_field("School")
    create_field("Career Goal")
    create_field("Interests (comma separated)")
    create_field("Strengths (comma separated)")
    create_field("Class IDs (comma separated)")

    # --- SAVE FUNCTION ---
    def save_student():
        try:
            student_data = {
                "personal_info": {
                    "first_name": fields["First Name"].get(),
                    "last_name": fields["Last Name"].get(),
                    "preferred_name": fields["Preferred Name"].get(),
                    "age": int(fields["Age"].get()),
                    "grade": fields["Grade"].get(),
                    "school": fields["School"].get()
                },
                "career_goal": fields["Career Goal"].get(),
                "interests": [i.strip() for i in fields["Interests (comma separated)"].get().split(",") if i.strip()],
                "strengths": [s.strip() for s in fields["Strengths (comma separated)"].get().split(",") if s.strip()],
                "classes": [c.strip() for c in fields["Class IDs (comma separated)"].get().split(",") if c.strip()]
            }

            add_student(student_data)

            messagebox.showinfo("Success", "Student added successfully!")
            popup.destroy()
            self.load_students()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age")

        if not fields["First Name"].get() or not fields["Last Name"].get():
            messagebox.showerror("Error", "Name is required")
            return

    tk.Button(popup, text="Save Student", command=save_student).pack(pady=20)

from Services.students import edit_student, load_data

def edit_student(self):
    student_id = self.get_selected_student_id()
    if not student_id:
        return

    data = load_data()
    student = data["students"][student_id]
    info = student["personal_info"]

    popup = tk.Toplevel(self.root)
    popup.title("Edit Student")
    popup.geometry("400x600")

    fields = {}

    def create_field(label, value):
        tk.Label(popup, text=label).pack()
        entry = tk.Entry(popup)
        entry.insert(0, value)
        entry.pack(fill="x", padx=10, pady=5)
        fields[label] = entry

    create_field("First Name", info["first_name"])
    create_field("Last Name", info["last_name"])
    create_field("Preferred Name", info.get("preferred_name", ""))
    create_field("Age", info["age"])
    create_field("Grade", info["grade"])
    create_field("School", info["school"])
    create_field("Career Goal", student["career_goal"])
    create_field("Interests", ", ".join(student["interests"]))
    create_field("Strengths", ", ".join(student["strengths"]))
    create_field("Classes", ", ".join(student["classes"]))

    def save_changes():
        try:
            updates = {
                "personal_info": {
                    "first_name": fields["First Name"].get(),
                    "last_name": fields["Last Name"].get(),
                    "preferred_name": fields["Preferred Name"].get(),
                    "age": int(fields["Age"].get()),
                    "grade": fields["Grade"].get(),
                    "school": fields["School"].get()
                },
                "career_goal": fields["Career Goal"].get(),
                "interests": [i.strip() for i in fields["Interests"].get().split(",") if i.strip()],
                "strengths": [s.strip() for s in fields["Strengths"].get().split(",") if s.strip()],
                "classes": [c.strip() for c in fields["Classes"].get().split(",") if c.strip()]
            }

            edit_student(student_id, updates)

            messagebox.showinfo("Success", "Student updated successfully!")
            popup.destroy()
            self.load_students()

        except ValueError:
            messagebox.showerror("Error", "Invalid input (check age)")
        if not fields["First Name"].get():
            messagebox.showerror("Error", "First name required")
            return
    
    tk.Button(popup, text="Save Changes", command=save_changes).pack(pady=20)

import tkinter as tk
from UI.app import StudentApp


root = tk.Tk()
app = StudentApp(root)
root.mainloop()
