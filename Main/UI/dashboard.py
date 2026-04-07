from Services.students import load_data
from Services.students import get_student_by_id
from Services.students import edit_student
from Services.students import add_student

def get_all_students():
    data = load_data()
    students = []

    for student_id, student in data["students"].items():
        students.append({
            "id": student_id,
            "name": f"{student['personal_info']['first_name']} {student['personal_info']['last_name']}",
            "preferred_name": student["personal_info"].get("preferred_name", ""),
            "school": student["personal_info"]["school"],
            "grade": student["personal_info"]["grade"],
            "classes": student["classes"],
            "last_updated": student["last_updated"]
        })

    return students

def show_student_profile(student_id):
    student = get_student_by_id(student_id)

    print("\n" + "=" * 50)
    print("STUDENT PROFILE")
    print("=" * 50)

    print(f"Name: {student['full_name']}")
    print(f"Preferred Name: {student['preferred_name']}")
    print(f"Age: {student['age']}")
    print(f"Grade: {student['grade']}")
    print(f"School: {student['school']}")
    print(f"Career Goal: {student['career_goal']}")

    print("\nClasses:")
    for c in student["classes"]:
        print(f" - {c}")

    print("\nInterests:")
    for i in student["interests"]:
        print(f" - {i}")

    print("\nStrengths:")
    for s in student["strengths"]:
        print(f" - {s}")

    print("\nNotes:")
    if not student["notes"]:
        print(" No notes yet.")
    else:
        for note in student["notes"]:
            print(f" [{note['date']}] {note['author']}: {note['content']}")

    print(f"\nLast Updated: {student['last_updated']}")
    print("=" * 50)


#from Services.students import edit_student

def edit_student_profile(student_id):
    print("\nEDIT STUDENT PROFILE")

    new_grade = input("New grade (leave blank to keep current): ")
    new_school = input("New school (leave blank to keep current): ")
    new_goal = input("New career goal (leave blank to keep current): ")

    updates = {
        "personal_info": {},
    }

    if new_grade:
        updates["personal_info"]["grade"] = new_grade
    if new_school:
        updates["personal_info"]["school"] = new_school
    if new_goal:
        updates["career_goal"] = new_goal

    if updates["personal_info"] or "career_goal" in updates:
        edit_student(student_id, updates)
        print("Student updated successfully.")
    else:
        print("No changes made.")
        
#add student
#from Services.students import add_student
def add_student_profile():
    print("\nADD NEW STUDENT")

    first_name = input("First name: ")
    last_name = input("Last name: ")
    preferred_name = input("Preferred name: ")
    age = int(input("Age: "))
    grade = input("Grade: ")
    school = input("School: ")

    career_goal = input("Career goal: ")

    interests = input("Interests (comma separated): ").split(",")
    strengths = input("Strengths (comma separated): ").split(",")

    classes = input("Class IDs (comma separated, e.g. CS_L1,PY_L1): ").split(",")

    student_data = {
        "personal_info": {
            "first_name": first_name,
            "last_name": last_name,
            "preferred_name": preferred_name,
            "age": age,
            "grade": grade,
            "school": school
        },
        "classes": [c.strip() for c in classes if c.strip()],
        "career_goal": career_goal,
        "interests": [i.strip() for i in interests if i.strip()],
        "strengths": [s.strip() for s in strengths if s.strip()]
    }

    student_id = add_student(student_data)
    print(f"Student added successfully with ID: {student_id}")
    
    for class_id in data["students"][student_id]["classes"]:
        if class_id in data["classes"]:
            data["classes"][class_id]["students"].append(student_id)
