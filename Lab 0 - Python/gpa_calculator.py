from typing import List
from college import Student, Course
import utils


def calculate_gpa(student: Student, courses: List[Course]) -> float:
    '''
    This function takes a student and a list of course
    It should compute the GPA for the student
    The GPA is the sum(hours of course * grade in course) / sum(hours of course)
    The grades come in the form: 'A+', 'A' and so on.
    But you can convert the grades to points using a static method in the course class
    To know how to use the Student and Course classes, see the file "college.py"  
    '''
    # TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    hours_sum = 0
    grade_points_sum = 0

    for course in courses:
        if student.id in course.grades:
            grade = course.grades[student.id]
            grade_points = Course.convert_grade_to_points(grade)
            grade_points_sum += grade_points * course.hours
            hours_sum += course.hours

    if hours_sum == 0:
        return 0.0

    return grade_points_sum / hours_sum
