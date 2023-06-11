"""
    Author: Iga Kordula s24646
"""
import csv
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
import re
import os

Base = declarative_base()
engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)
session = Session()


class Student(Base):
    """
    Represents a student entity in the database.
    """

    __tablename__ = 'students'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    student_number = Column(String(6))
    name = Column(String(30))
    surname = Column(String(30))
    date_of_birth = Column(String(10))
    email = Column(String(40))

    def __init__(self, student_number, name, surname, date_of_birth, email):
        self.student_number = student_number
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.email = email


def get_all_students(student_listbox):
    """
    Retrieves all students from the database and refreshes the student listbox.

    Args:
        student_listbox (Listbox): The Listbox widget to display the students.
    """
    students = session.query(Student).all()
    session.close()
    refresh_students(students, student_listbox)


def get_student(entry, student_listbox):
    """
    Retrieves students from the database based on the provided search entry and refreshes the student listbox.

    Args:
        entry (str): The search entry to find the student.
        student_listbox (Listbox): The Listbox widget to display the students.
    """
    students = session.query(Student).filter(
        or_(
            Student.id == entry,
            Student.student_number == entry,
            Student.name == entry,
            Student.surname == entry,
            Student.date_of_birth == entry,
            Student.email == entry
        )
    ).all()
    session.close()
    if students:
        refresh_students(students, student_listbox)
    else:
        student_listbox.delete(0, END)
        student_listbox.insert(END, f"No student with data '{entry}' found.")


def insert_student(student_number, name, surname, date_of_birth, email, student_listbox):
    """
    Inserts a new student into the database and refreshes the student listbox.

    Args:
        student_number (str): The student number.
        name (str): The name of the student.
        surname (str): The surname of the student.
        date_of_birth (str): The date of birth of the student.
        email (str): The email of the student.
        student_listbox (Listbox): The Listbox widget to display the students.
    """
    try:
        if not is_valid_student_number(student_number) or not is_valid_name(name) or not is_valid_surname(surname) or not is_valid_date_of_birth(date_of_birth) or not is_valid_email(email):
            messagebox.showerror("Error", "Wrong data format")
            return
        snum = session.query(Student).filter(Student.student_number == student_number).first()
        if snum is not None:
            messagebox.showerror("Error", "Student with this student number already exists")
            return
        student = Student(student_number=student_number, name=name, surname=surname, date_of_birth=date_of_birth,
                          email=email)
        session.add(student)
        session.commit()
        session.close()
        get_all_students(student_listbox)
    except SQLAlchemyError as e:
        messagebox.showerror("Error", "Failed to add student: " + str(e))
        session.rollback()


def open_new_window(root, student_listbox, command, entry):
    """
    Opens a new window for adding or updating a student.

    Args:
        root (Tk): The root Tkinter window.
        student_listbox (Listbox): The Listbox widget to display the students.
        command (str): The command indicating "Add" or "Update" student.
        entry (str): The student ID or number for updating a student (None for adding).
    """
    if command == "Add" and entry is None:
        new_window = tk.Toplevel(root)
        new_window.title("New Student")
        student_number_entry = "Student number"
        name_entry = "Name"
        surname_entry = "Surname"
        date_of_birth_entry = "Date of birth"
        email_entry = "Email"
    else:
        student = session.query(Student).filter(
            or_(
                Student.id == entry,
                Student.student_number == entry
            )
        ).first()
        if student:
            student_number_entry = student.student_number
            name_entry = student.name
            surname_entry = student.surname
            date_of_birth_entry = student.date_of_birth
            email_entry = student.email
            new_window = tk.Toplevel(root)
            new_window.title("Update Student")
        else:
            messagebox.showerror("Error", "Student not found.")
            return
    window_width = 400
    window_height = 200
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    new_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    label = tk.Label(new_window, text="Enter student data:")
    label.pack()

    student_number = tk.Entry(new_window, width=50)
    student_number.insert(0, student_number_entry)
    student_number.bind('<Button-1>', lambda event: student_number.delete(0, 'end'))
    student_number.pack()

    name = tk.Entry(new_window, width=50)
    name.insert(0, name_entry)
    name.bind('<Button-1>', lambda event: name.delete(0, 'end'))
    name.pack()

    surname = tk.Entry(new_window, width=50)
    surname.insert(0, surname_entry)
    surname.bind('<Button-1>', lambda event: surname.delete(0, 'end'))
    surname.pack()

    date_of_birth = tk.Entry(new_window, width=50)
    date_of_birth.insert(0, date_of_birth_entry)
    date_of_birth.bind('<Button-1>', lambda event: date_of_birth.delete(0, 'end'))
    date_of_birth.pack()

    email = tk.Entry(new_window, width=50)
    email.insert(0, email_entry)
    email.bind('<Button-1>', lambda event: email.delete(0, 'end'))
    email.pack()

    if command == "Add" and entry is None:
        submit_button = tk.Button(new_window, text="Submit",
                                  command=lambda: insert_student(student_number.get(), name.get(), surname.get(),
                                                                 date_of_birth.get(), email.get(), student_listbox))
    else:
        submit_button = tk.Button(new_window, text="Submit",
                                  command=lambda: update_student(student_number.get(), name.get(), surname.get(),
                                                                 date_of_birth.get(), email.get(), student_listbox,
                                                                 student))
    submit_button.pack()


def update_student(student_number, name, surname, date_of_birth, email, student_listbox, student):
    """
    Updates an existing student in the database and refreshes the student listbox.

    Args:
        student_number (str): The updated student number.
        name (str): The updated name of the student.
        surname (str): The updated surname of the student.
        date_of_birth (str): The updated date of birth of the student.
        email (str): The updated email of the student.
        student_listbox (Listbox): The Listbox widget to display the students.
        student (Student): The student object to update.
    """
    try:
        if not is_valid_student_number(student_number) or not is_valid_name(name) or not is_valid_surname(surname) or not is_valid_date_of_birth(date_of_birth) or not is_valid_email(email):
            messagebox.showerror("Error", "Wrong data format")
            return
        if student.student_number != student_number:
            snum = session.query(Student).filter(Student.student_number == student_number).first()
            if snum is not None:
                messagebox.showerror("Error", "Student with this student number already exists")
                return
        student.student_number = student_number
        student.name = name
        student.surname = surname
        student.date_of_birth = date_of_birth
        student.email = email

        session.commit()
        get_all_students(student_listbox)
        messagebox.showinfo("Success", "Student updated successfully.")
    except SQLAlchemyError as e:
        messagebox.showerror("Error", "Failed to update student: " + str(e))
        session.rollback()


def delete_student(student_listbox, entry):
    """
    Deletes a student from the database and refreshes the student listbox.

    Args:
        student_listbox (Listbox): The Listbox widget to display the students.
        entry (str): The student ID or number to delete.
    """
    try:
        student = session.query(Student).filter(
            or_(
                Student.id == entry,
                Student.student_number == entry
            )
        ).first()
        if student:
            session.delete(student)
            session.commit()
            get_all_students(student_listbox)
            messagebox.showinfo("Success", "Student deleted successfully.")
        else:
            messagebox.showerror("Error", "Student not found")
    except SQLAlchemyError as e:
        messagebox.showerror("Error", "Failed to update student: " + str(e))
        session.rollback()


def refresh_students(students, student_listbox):
    """
    Refreshes the student listbox with the provided list of students.

    Args:
        students (list): The list of student objects to display.
        student_listbox (Listbox): The Listbox widget to display the students.
    """
    student_listbox.delete(0, END)

    for student in students:
        student_listbox.insert(END, f"ID {student.id}: {student.student_number}, {student.name} {student.surname}, "
                                    f"{student.date_of_birth}, {student.email}")


def upload_file(student_listbox):
    """
    Uploads student data from a CSV file and inserts them into the database.

    Args:
        student_listbox (Listbox): The Listbox widget to display the students.
    """
    file_path = filedialog.askopenfilename()
    ext = os.path.splitext(file_path)[-1].lower()
    if ext != '.csv':
        messagebox.showerror("Error", "This is not a CSV file.")
        upload_file(student_listbox)
    else:
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=";")

            for row in reader:
                student_number, name, surname, date_of_birth, email = row
                insert_student(student_number, name, surname, date_of_birth, email, student_listbox)

        messagebox.showinfo("Success", "Students have been successfully added from the CSV file.")


def is_valid_student_number(student_number):
    """
    Checks if the student number has a valid format.

    Args:
        student_number (str): The student number to validate.

    Returns:
        bool: True if the student number is valid, False otherwise.
    """
    return re.match(r'^s\d{5}$', student_number) is not None


def is_valid_name(name):
    """
    Checks if the name has a valid format.

    Args:
        name (str): The name to validate.

    Returns:
        bool: True if the name is valid, False otherwise.
    """
    return re.match(r'^[A-Z][a-zA-Z\s-]*$', name) is not None


def is_valid_surname(surname):
    """
    Checks if the surname has a valid format.

    Args:
        surname (str): The surname to validate.

    Returns:
        bool: True if the surname is valid, False otherwise.
    """
    return re.match(r'^[A-Z][a-zA-Z\s-]*$', surname) is not None


def is_valid_date_of_birth(date_of_birth):
    """
    Checks if the date of birth has a valid format.

    Args:
        date_of_birth (str): The date of birth to validate.

    Returns:
        bool: True if the date of birth is valid, False otherwise.
    """
    return re.match(r'^\d{2}\.\d{2}\.\d{4}$', date_of_birth) is not None


def is_valid_email(email):
    """
    Checks if the email has a valid format.

    Args:
        email (str): The email to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    return re.match(r'^[\w.-]+@[\w.-]+\.\w+$', email) is not None


def main():
    """
    The main function that initializes the GUI and sets up the database.
    """
    Base.metadata.create_all(engine)

    # window settings
    root = tk.Tk()
    root.title("Student management system")
    window_width = 500
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # list of students
    student_listbox = Listbox(root, width=80, height=20)
    student_listbox.grid(row=0, column=0, columnspan=5, padx=5, pady=5)
    get_all_students(student_listbox)

    # labels
    Label(root, text="All students").grid(row=2, column=0, padx=5, pady=5)
    Label(root, text="Find student").grid(row=3, column=0, padx=5, pady=5)
    Label(root, text="Add student").grid(row=4, column=0, padx=5, pady=5)
    Label(root, text="Update student").grid(row=5, column=0, padx=5, pady=5)
    Label(root, text="Delete student").grid(row=6, column=0, padx=5, pady=5)

    # find all students
    find_students_button = tk.Button(root, text="See all students",
                                     command=lambda: get_all_students(student_listbox), width=20)
    find_students_button.grid(row=2, column=1)

    # find student
    search_input = Entry(root, width=20)
    search_input.insert(0, "Enter student data")
    search_input.bind('<Button-1>', lambda event: search_input.delete(0, 'end'))
    search_input.grid(row=3, column=1)
    find_student_button = tk.Button(root, text="Find Student", command=lambda: get_student(search_input.get(),
                                                                                           student_listbox), width=20)
    find_student_button.grid(row=3, column=2)

    # add new student
    add_new_button = tk.Button(root, text="Add new student",
                               command=lambda: open_new_window(root, student_listbox, "Add", None),
                               width=20)
    add_new_button.grid(row=4, column=1)
    upload_button = tk.Button(root, text="Upload CSV file", command=lambda: upload_file(student_listbox), width=20)
    upload_button.grid(row=4, column=2)

    # update student
    update_input = Entry(root, width=20)
    update_input.insert(0, "Enter student number or ID")
    update_input.bind('<Button-1>', lambda event: update_input.delete(0, 'end'))
    update_input.grid(row=5, column=1)
    update_student_button = tk.Button(root, text="Update Student",
                                      command=lambda: open_new_window(root, student_listbox,
                                                                      "Update", update_input.get()),
                                      width=20)
    update_student_button.grid(row=5, column=2)

    # delete student
    delete_input = Entry(root, width=20)
    delete_input.insert(0, "Enter student number or ID")
    delete_input.bind('<Button-1>', lambda event: delete_input.delete(0, 'end'))
    delete_input.grid(row=6, column=1)
    delete_student_button = tk.Button(root, text="Delete Student",
                                      command=lambda: delete_student(student_listbox, delete_input.get()),
                                      width=20)
    delete_student_button.grid(row=6, column=2)

    root.mainloop()


if __name__ == '__main__':
    main()
