import json
import os
from datetime import datetime


class Database:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), "data.json")
        self.data = self.load_data()

    # ------------------------
    # LOAD & SAVE
    # ------------------------

    def load_data(self):
        if not os.path.exists(self.file_path):
            return {"students": [], "classes": []}

        with open(self.file_path, "r") as file:
            return json.load(file)

    def save_data(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    # ------------------------
    # STUDENT METHODS
    # ------------------------

    def get_all_students(self):
        return self.data["students"]

    def get_student_by_id(self, student_id):
        for student in self.data["students"]:
            if student["id"] == student_id:
                return student
        return None

    def add_student(self, student_data):
        new_id = self.generate_student_id()
        student_data["id"] = new_id
        student_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        self.data["students"].append(student_data)
        self.save_data()

    def delete_student(self, student_id):
        self.data["students"] = [
            student for student in self.data["students"]
            if student["id"] != student_id
        ]

        # Also remove student from classes
        for class_item in self.data["classes"]:
            if student_id in class_item["students"]:
                class_item["students"].remove(student_id)

        self.save_data()

    def update_student(self, student_id, updated_data):
        student = self.get_student_by_id(student_id)
        if student:
            student.update(updated_data)
            student["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            self.save_data()

    def add_note(self, student_id, note_text):
        student = self.get_student_by_id(student_id)
        if student:
            if "notes" not in student:
                student["notes"] = []

            student["notes"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "content": note_text
            })

            self.save_data()

    def generate_student_id(self):
        if not self.data["students"]:
            return 1
        return max(student["id"] for student in self.data["students"]) + 1

    # ------------------------
    # CLASS METHODS
    # ------------------------

    def get_all_classes(self):
        return self.data["classes"]

    def add_class(self, class_data):
        new_id = self.generate_class_id()
        class_data["id"] = new_id
        class_data["students"] = []
        self.data["classes"].append(class_data)
        self.save_data()

    def assign_student_to_class(self, student_id, class_id):
        student = self.get_student_by_id(student_id)

        for class_item in self.data["classes"]:
            if class_item["id"] == class_id:
                if student_id not in class_item["students"]:
                    class_item["students"].append(student_id)

                if class_id not in student["classes"]:
                    student["classes"].append(class_id)

        self.save_data()

    def generate_class_id(self):
        if not self.data["classes"]:
            return 1
        return max(class_item["id"] for class_item in self.data["classes"]) + 1
