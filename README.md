# Student-Management-App

## Purpose
The purpose of this project is to create a student management system that allows users to manage student records. The system provides features for adding, updating, and deleting student information. It also supports importing student data from CSV files. The project aims to provide a user-friendly interface and ensure data integrity by validating input formats.

## Functionality
1. View all students: Display a list of all students in the system.
2. Find student: Search for a student using their ID, student number, name, surname, date of birth, or email.
3. Add student: Add a new student to the system by entering their student number, name, surname, date of birth, and email.
4. Update student: Update an existing student's information by specifying their ID or student number and entering the updated details.
5. Delete student: Delete a student from the system using their ID or student number.
6. Import students from CSV: Upload a CSV file containing student data and add the students to the system.

## Dependencies
- Python 3.x
- Tkinter library
- SQLAlchemy library

## How to Run the Program
1. Install Python 3.x on your system.
2. Install the required dependencies by running the command pip install tkinter sqlalchemy.
3. Clone the project repository from GitHub: git clone <repository-url>.
4. Open a terminal or command prompt and navigate to the project directory.
5. Run the command python main.py to start the student management system.
6. The application window will open and you can interact with the system using the provided buttons and input fields.
  
## Examples of Program Usage
### See all students:
  1. Click on the "See all students" button.
  2. A list of all students and their information will show.
  
### Find a student:
  1. Enter the student's ID, student number, name, surname, date of birth or email in the input field.
  2. Click on the "Find student" button.
  3. A list of students for whom the prerequisites are fulfilled will show.
### Add a student:

  1. Click on the "Add new student" button.
  2. Enter the student's details in the input fields (e.g., student number, name, surname, date of birth, email).
  3. Click the "Submit" button to add the student to the system.
### Update a student:

  1. Enter the student's ID or student number in the "Update student" input field.
  2. Click on the "Update Student" button.
  3. Modify the student's details in the input fields.
  4. Click the "Submit" button to update the student's information.
### Delete a student:

  1. Enter the student's ID or student number in the "Delete student" input field.
  2. Click on the "Delete Student" button.
  3. The student will be removed from the system.
### Import students from a CSV file:

  1. Click on the "Upload CSV file" button.
  2. Select a CSV file containing student data.
  3. The students from the CSV file will be added to the system.
  
## Challenges Faced
During the development of this project, I've encountered a few problems:

- Implementing data validation: Ensuring that the entered student information adheres to the specified formats required careful handling of regular expressions and input validation logic.
- Integrating with a database: Setting up a database connection, defining the data model, and implementing database operations with SQLAlchemy required careful planning and knowledge of the SQLAlchemy library.
- Handling GUI interactions: Designing and managing the graphical user interface using Tkinter involved understanding handling user inputs effectively.
  
## Lessons Learned
Throughout the development process, I've learned the following lessons:

- Proper planning is crucial: Clear project requirements and a well-defined system design help in the smooth implementation of features.
- Effective error handling: Implementing appropriate error handling mechanisms helps improve the user experience and provides useful feedback.
- Continuous testing and debugging: Regular testing and debugging during development are essential to identify and fix issues early on.
  
