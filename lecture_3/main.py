#list of dictionaries students
students: list = []

# indicator of the presence of grades
exist_grades: int = 0


def print_menu() -> None:
    """
    Print the start menu options to the console.
    """
    menu_text = (
        "--- Student Grade Analyzer ---\n"
        "1. Add a new student\n"
        "2. Add grades for a student\n"
        "3. Generate a full report\n"
        "4. Find the top student\n"
        "5. Exit program"
    )
    print(menu_text)


def add_student() -> None:
    """
    Prompts for a student name, normalizes the input,
    and adds a new student to the list if not already present.
    """
    name = input("Enter student name: ").strip().title()

    if not name:
        print("Invalid name entered.")
        return

    for student in students:
        if student["name"] == name:
            print(f"Student with name '{name}' already exists.")
            return

    students.append({"name": name, "grades": []})


def add_grades(student_id: int) -> None:
    """
    Prompt the user to enter grades for a student and add them to the student's grade list.

    The user inputs grades between 0 and 100 inclusive. Entering "done" finishes the input.
    Invalid inputs trigger error messages and reprompt.

    Args:
        student_id (int): The identifier of the student to whom grades are being added.
    """
    global exist_grades
    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ")
        if grade_input.lower() == "done":
            return

        try:
            grade = int(grade_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if 0 <= grade <= 100:
            students[student_id]["grades"].append(grade)
            exist_grades = 1
        else:
            print("Invalid input. Please enter a number between 0 and 100.")


def calculate_mean():
    """Generator yielding (student_name, average_grade or 'N/A' if no grades)."""
    for student in students:
        try:
            yield student["name"], round(sum(student["grades"]) / len(student["grades"]), 1)
        except ZeroDivisionError:
            yield student["name"], "N/A"


def main():
    while True:
        try:
            print_menu()
            option = input("Enter your choice: ")
            match option:
                case "1":
                    add_student()
                case "2":
                    name = input("Enter student name: ").strip().title()
                    for id_student, student in enumerate(students):
                        if student["name"] == name:
                            add_grades(id_student)
                            break
                    else:
                        print(f"Student {name} is not found.")
                case "3":
                    if exist_grades:
                        print("--- Student Report ---")
                        mean_students = list(calculate_mean())
                        for name, mean_student in mean_students:
                            print(f"{name}'s average grade is {mean_student}.")
                        print("-" * 26)
                        # Filter valid averages
                        valid_means = [x[1] for x in mean_students if x[1] != "N/A"]
                        if valid_means:
                            print(f"Max Average: {max(valid_means)}")
                            print(f"Min Average: {min(valid_means)}")
                            overall = round(sum(valid_means) / len(valid_means), 1)
                            print(f"Overall Average: {overall}")
                    else:
                        print("There are no students or no grades at all.")
                case "4":
                    if exist_grades:
                        mean_students = list(filter(lambda x: x[1] != "N/A", calculate_mean()))
                        max_value = max(mean_students, key=lambda x: x[1])
                        print(f"The student with the highest average is {max_value[0]} with a grade of {max_value[1]}.")
                    else:
                        print("There are no students or no grades at all.")
                case "5":
                    print("Exiting program.")
                    break
                case _:
                    raise ValueError(f"Invalid option: {option}. Please choose a valid menu number.")

        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()

