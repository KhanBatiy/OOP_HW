class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer)
                and course in lecturer.courses_attached
                and course in self.courses_in_progress
                and 0 <= grade <= 10):
            if course in lecturer.lect_grades:
                lecturer.lect_grades[course] += [grade]
            else:
                lecturer.lect_grades[course] = [grade]
        else:
            return 'Ошибка'

    def get_avg_rate(self):
        if not self.grades:
            return 0
        all_grades = []
        for course_grades in self.grades.values():
            all_grades.extend(course_grades)
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg_grades = self.get_avg_rate()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg_grades:.1f}\n"
            f"Курсы в процессе изучения: {courses_in_progress}\n"
            f"Завершенные курсы: {finished_courses}"
        )

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_avg_rate() == other.get_avg_rate()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_avg_rate() < other.get_avg_rate()

    def __gt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_avg_rate() > other.get_avg_rate()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lect_grades = {}

    def get_avg_rate(self):
        if not self.lect_grades:
            return 0
        all_grades = []
        for course_grades in self.lect_grades.values():
            all_grades.extend(course_grades)
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg_grades = self.get_avg_rate()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg_grades:.1f}"
        )

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_avg_rate() == other.get_avg_rate()

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_avg_rate() < other.get_avg_rate()

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_avg_rate() > other.get_avg_rate()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student)
                and course in self.courses_attached
                and course in student.courses_in_progress
                and 0 <= grade <= 10):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


def estimate_students_hw(students, course):
    if not students:
        return 0

    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])

    return sum(total_grades) / len(total_grades)


def estimate_lecturers(lecturers, course):
    if not lecturers:
        return 0

    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.lect_grades:
            total_grades.extend(lecturer.lect_grades[course])

    return sum(total_grades) / len(total_grades)


# Студенты
student1 = Student("Алексей", "Иванов", "male")
student1.courses_in_progress = ["Python", "Git", "Java"]
student1.finished_courses = ["Введение в программирование"]
student2 = Student("Мария", "Петрова", "female")
student2.courses_in_progress = ["Python", "JavaScript"]
student2.finished_courses = ["Основы программирования"]

# Лекторы
lecturer1 = Lecturer("Иван", "Сидоров")
lecturer1.courses_attached = ["Python", "Git"]
lecturer2 = Lecturer("Ольга", "Козлова")
lecturer2.courses_attached = ["Python", "JavaScript", "Java"]

# Ревьюеры
reviewer1 = Reviewer("Сергей", "Николаев")
reviewer1.courses_attached = ["Python", "Git"]
reviewer2 = Reviewer("Анна", "Смирнова")
reviewer2.courses_attached = ["Python", "JavaScript", "Java"]

reviewer1.rate_hw(student1, "Python", 9)
reviewer1.rate_hw(student1, "Python", 10)
reviewer1.rate_hw(student1, "Git", 8)
reviewer1.rate_hw(student1, "Git", 9)
reviewer2.rate_hw(student1, "Java", 7)
reviewer1.rate_hw(student2, "Python", 8)
reviewer1.rate_hw(student2, "Python", 9)
reviewer2.rate_hw(student2, "JavaScript", 10)

student1.rate_lecture(lecturer1, "Python", 10)
student1.rate_lecture(lecturer1, "Git", 9)
student2.rate_lecture(lecturer1, "Python", 8)
student1.rate_lecture(lecturer2, "Python", 9)
student1.rate_lecture(lecturer2, "Java", 8)
student2.rate_lecture(lecturer2, "Python", 10)
student2.rate_lecture(lecturer2, "JavaScript", 9)

print("Тестируем некорректные операции:")
# Курс не прикреплен к проверяющему
result1 = reviewer1.rate_hw(student1, "JavaScript", 5)
# Курс не прикреплен к лектору
result2 = student1.rate_lecture(lecturer1, "Java", 8)
# Некорректная оценка
result3 = reviewer1.rate_hw(student1, "Python", 15)
print(f"Некорректная оценка: {result1}")
print(f"Некорректная лекция: {result2}")
print(f"Некорректный диапазон: {result3}\n")

print("Информация о всех участниках:")
print("СТУДЕНТЫ:")
print(student1)
print()
print(student2)
print("\nЛЕКТОРЫ:")
print(lecturer1)
print()
print(lecturer2)
print("\nРЕВЬЮЕРЫ:")
print(reviewer1)
print()
print(reviewer2)

print("\nСравнение объектов:")
print()
print(f"student1 > student2: {student1 > student2}")
print(f"student1 < student2: {student1 < student2}")
print(f"student1 == student2: {student1 == student2}")
print(f"lecturer1 > lecturer2: {lecturer1 > lecturer2}")
print(f"lecturer1 < lecturer2: {lecturer1 < lecturer2}")
print(f"lecturer1 == lecturer2: {lecturer1 == lecturer2}")

# Используем функции для подсчета средних оценок по курсам
print("\nСредние оценки по курсам:")
students_list = [student1, student2]
lecturers_list = [lecturer1, lecturer2]
courses_to_check = ["Python", "Git", "Java", "JavaScript"]

for course in courses_to_check:
    student_avg = estimate_students_hw(students_list, course)
    lecturer_avg = estimate_lecturers(lecturers_list, course)

    print(f"\nКурс: {course}")
    print(f"  Средняя оценка студентов: {student_avg:.1f}")
    print(f"  Средняя оценка лекторов:  {lecturer_avg:.1f}")
