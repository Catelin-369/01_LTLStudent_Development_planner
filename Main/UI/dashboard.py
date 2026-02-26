from Services.students import load_data

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

