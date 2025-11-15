
# (High Cohesion) -Low Coupling -Encapsulation -SOLID Architecture
# Domain Models, Repositories, Services, and Clean Orchestration

# ---DOMAIN MODELS

class Person:
    def __init__(self, person_id, name, email, phone=None):
        self._person_id = person_id
        self._name = name
        self._email = email
        self._phone = phone

    @property
    def person_id(self): return self._person_id

    @property
    def name(self): return self._name

    @property
    def email(self): return self._email

    @property
    def phone(self): return self._phone

    @phone.setter
    def phone(self, value): self._phone = value


class Student(Person):
    """Represents a student with course membership only (high cohesion)."""
    
    
    def __init__(self, person_id, name, email, phone=None):
        super().__init__(person_id, name, email, phone)
        self._courses = set()
        self._grades = {}        # grade per course
        self._attendance = {}    # attendance per course

    @property
    def courses(self): return tuple(self._courses)

    @property
    def grades(self): return dict(self._grades)

    @property
    def attendance(self): return dict(self._attendance)

    def enroll(self, course_id):
        self._courses.add(course_id)

    def record_grade(self, course_id, grade):
        self._grades[course_id] = grade

    def record_attendance(self, course_id, record_list):
        self._attendance[course_id] = record_list


class Course:
    """Represents a course with basic info and enrolled student IDs."""
    def __init__(self, course_id, name, teacher_id):
        self._course_id = course_id
        self._name = name
        self._teacher_id = teacher_id
        self._students = set()

    @property
    def course_id(self): return self._course_id

    @property
    def name(self): return self._name

    @property
    def teacher_id(self): return self._teacher_id

    @property
    def students(self): return tuple(self._students)

    def enroll(self, student_id):
        self._students.add(student_id)


# ---REPOSITORIES
# Decouples storage from business logic

class StudentRepository:
    def __init__(self):
        self._students = {}

    def add(self, student): self._students[student.person_id] = student
    def get(self, student_id): return self._students.get(student_id)
    def all(self): return self._students.values()


class CourseRepository:
    def __init__(self):
        self._courses = {}

    def add(self, course): self._courses[course.course_id] = course
    def get(self, course_id): return self._courses.get(course_id)
    def all(self): return self._courses.values()


# ---SERVICES
# each service handles one responsibility only

class EnrollmentService:
    def enroll_student(self, student_repo, course_repo, student_id, course_id):
        student = student_repo.get(student_id)
        course = course_repo.get(course_id)

        if not student or not course:
            return False

        student.enroll(course_id)
        course.enroll(student_id)
        return True


class PerformanceService:
    GRADE_POINTS = {"A": 4, "B": 3, "C": 2, "D": 1, "E": 0}

    def calculate_gpa(self, grades: dict):
        if not grades:
            return 0
        points = sum(self.GRADE_POINTS.get(g, 0) for g in grades.values())
        return round(points / len(grades), 2)

    def calculate_attendance(self, attendance: dict):
        if not attendance:
            return 0
        totals = [(sum(r) / len(r)) * 100 for r in attendance.values() if r]
        return round(sum(totals) / len(totals), 1)


class ReportService:
    def __init__(self):
        self.performance = PerformanceService()

    def student_report(self, student: Student):
        gpa = self.performance.calculate_gpa(student.grades)
        att = self.performance.calculate_attendance(student.attendance)
        print(f"Student: {student.name} | GPA={gpa} | Attendance={att}%")

    def course_report(self, course: Course):
        print(f"Course {course.course_id} - {course.name} | Students: {len(course.students)}")

    def full_report(self, student_repo, course_repo):
        print("UNIVERSITY REPORT")
        for c in course_repo.all(): self.course_report(c)
        for s in student_repo.all(): self.student_report(s)


# ---ORCHESTRATION

if __name__ == "__main__":
    student_repo = StudentRepository()
    course_repo = CourseRepository()

    # create objects
    s1 = Student(1, "Alice", "alice@uni.com")
    s2 = Student(2, "Bob", "bob@uni.com")
    
    c1 = Course("CS101", "Intro to Programming", teacher_id=3)
    c2 = Course("CS201", "Data Structures", teacher_id=21)


    # store
    student_repo.add(s1)
    student_repo.add(s2)

    course_repo.add(c1)
    course_repo.add(c2)

    # enroll
    enroll_service = EnrollmentService()
    enroll_service.enroll_student(student_repo, course_repo, 1, 101)
    enroll_service.enroll_student(student_repo, course_repo, 2, 101)

    # record grades & attendance
    s1.record_grade(101, "C")
    s1.record_attendance(105, [True, True, False, True])

    s2.record_grade(101, "B")
    s2.record_attendance(102, [True, False, True])

    # report
    report = ReportService()
    report.full_report(student_repo, course_repo)
    
    
    student = student_repo.get(2)
course = course_repo.get(101)


