import json
from datetime import datetime

DATA_PATH = "DataBase/Student_Developer.json"


def load_data():
    with open(DATA_PATH, "r") as file:
        return json.load(file)


def save_data(data):
    data["meta"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    data["meta"]["total_students"] = len(data["students"])

    with open(DATA_PATH, "w") as file:
        json.dump(data, file, indent=4)

#New student ID

def generate_student_id(data):
    count = len(data["students"]) + 1
    return f"STD{count:03d}"

#Add a new student

def add_student(student_data):
    data = load_data()
    student_id = generate_student_id(data)

    data["students"][student_id] = {
        "personal_info": student_data["personal_info"],
        "classes": student_data.get("classes", []),
        "career_goal": student_data.get("career_goal", ""),
        "interests": student_data.get("interests", []),
        "strengths": student_data.get("strengths", []),
        "notes": [],
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    # Add student to class lists
    for class_id in data["students"][student_id]["classes"]:
        data["classes"][class_id]["students"].append(student_id)

    save_data(data)
    return student_id

#Edit student info

def edit_student(student_id, updated_fields):
    data = load_data()

    if student_id not in data["students"]:
        raise ValueError("Student not found")

    for key, value in updated_fields.items():
        data["students"][student_id][key] = value

    data["students"][student_id]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    save_data(data)

#Delete a student

def delete_student(student_id):
    data = load_data()

    if student_id not in data["students"]:
        raise ValueError("Student not found")

    # Remove from classes
    for class_data in data["classes"].values():
        if student_id in class_data["students"]:
            class_data["students"].remove(student_id)

    del data["students"][student_id]
    save_data(data)

#Assign to class

def assign_class(student_id, class_id):
    data = load_data()

    if student_id not in data["students"]:
        raise ValueError("Student not found")

    if class_id not in data["classes"]:
        raise ValueError("Class not found")

    if class_id not in data["students"][student_id]["classes"]:
        data["students"][student_id]["classes"].append(class_id)
        data["classes"][class_id]["students"].append(student_id)

    save_data(data)

#Add notes to student

def add_note(student_id, author, content):
    data = load_data()

    note = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "author": author,
        "content": content
    }

    data["students"][student_id]["notes"].append(note)
    save_data(data)

def get_student_by_id(student_id):
    data = load_data()

    if student_id not in data["students"]:
        raise ValueError("Student not found")

    student = data["students"][student_id]

    # Convert class IDs to readable class names
    class_names = []
    for class_id in student["classes"]:
        class_names.append(data["classes"][class_id]["name"])

    return {
        "id": student_id,
        "full_name": f"{student['personal_info']['first_name']} {student['personal_info']['last_name']}",
        "preferred_name": student['personal_info'].get("preferred_name", ""),
        "age": student['personal_info']['age'],
        "grade": student['personal_info']['grade'],
        "school": student['personal_info']['school'],
        "classes": class_names,
        "career_goal": student["career_goal"],
        "interests": student["interests"],
        "strengths": student["strengths"],
        "notes": student["notes"],
        "last_updated": student["last_updated"]
    }
