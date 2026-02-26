from Services.students import load_data
from Services.students import get_student_by_id

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
