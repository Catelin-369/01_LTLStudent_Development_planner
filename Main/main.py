from DataBase.Database import Database

db = Database()

print(db.get_all_students())

from UI.dashboard import edit_student_profile, show_student_profile

edit_student_profile("STD001")
show_student_profile("STD001")

import tkinter as tk
from UI.app import StudentApp

root = tk.Tk()
app = StudentApp(root)
root.mainloop()
