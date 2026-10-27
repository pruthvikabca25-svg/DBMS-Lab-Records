# Student Record Management System 

## About the Project

The Student Record Management System is a small web application I built to make student records easier to manage. Instead of entering every detail directly into MySQL, users can work with student information through a simple browser-based interface.

I built this project using Python and Flask, with MySQL handling the data and HTML and CSS providing the pages and styling. It is a mini-project for learning how a web application connects to a database and performs everyday record-management tasks.

## What This Project Covers

This mini-project brings together Flask routes, HTML forms, Python-to-MySQL connectivity, SQL queries, and CRUD operations (Create, Read, Update, and Delete). It is a learning project rather than a fully secured production system.

## What Can It Do?

* **View the dashboard:** See student records and useful summary counts.
* **Add a student:** Enter personal and academic details through a form.
* **View records:** Check the information saved in the database.
* **Edit a record:** Update a student's details when something changes.
* **Delete a record:** Remove a student record when needed.
* **Search records:** Find students using the search options available in the application.
* **Dashboard statistics:** Check the total number of students, recent additions, and the number of departments represented in the records.

MySQL also generates each student ID automatically and prevents duplicate email addresses.

## Technologies Used

| Technology             | How It Is Used                                |
| ---------------------- | --------------------------------------------- |
| Python                 | Handles the application's logic               |
| Flask                  | Connects the web pages and application routes |
| MySQL                  | Stores the student records                    |
| mysql-connector-python | Lets Python communicate with MySQL            |
| HTML                   | Provides the structure of the pages and forms |
| CSS                    | Controls the appearance and layout            |

## Project Folder Structure

student_record_management/
├── README.md
├── app.py
├── student_db.sql
├── templates/
│   ├── index.html
│   ├── add.html
│   └── edit.html
└── static/
    └── style.css

## What You Need Before Starting

* Python 3
* MySQL Server
* A web browser
* MySQL Workbench (recommended, but optional)

## Getting the Project Running

### 1. Open the Project

Open the `student_record_management` folder in VS Code, or use the terminal to move into the folder.

### 2. Set Up a Virtual Environment

In Windows PowerShell, run:

powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

If you already use a virtual environment stored somewhere else, activate that one instead.

### 3. Install the Required Packages

With the virtual environment activated, run:

pip install Flask mysql-connector-python

### 4. Set Up the Database

Open MySQL Workbench and run the SQL below. It creates the database and table only if they do not already exist.

CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    gender VARCHAR(20),
    date_of_birth DATE,
    course VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    semester INT NOT NULL,
    admission_year YEAR,
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Already have the `students` table? You do not need to create a second one. Run the following command in MySQL Workbench to check the columns:

DESCRIBE students;

CREATE TABLE IF NOT EXISTS` will not update an existing table's structure.

### 5. Check the MySQL Connection

In app.py, make sure the connection settings match your local MySQL setup. Replace the placeholder password with your own MySQL password on your computer.

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="student_db"
    )


### 6. Start the Application

In the terminal, move into the project folder and run:

python app.py

When Flask starts, open the following address in your browser:

`http://127.0.0.1:5000`

Keep the terminal open while using the application. Stop the server by pressing Ctrl + C when finished.

## Using the Application

1. Start the Flask app from the terminal.
2. Open http://127.0.0.1:5000 in your browser.
3. Add a student through the form.
4. Return to the dashboard to see the saved record.
5. Use the search feature to find a student.
6. Edit a record or delete it using the available actions.
7. Refresh the page after making changes to see the latest records and statistics.

Changes made through the application are saved in MySQL. Changes made directly in MySQL should appear in the application after you refresh the page.

## What I Learned

While building this project, I gained practical experience with Python, Flask, MySQL, HTML, and CSS. I also learned how to connect a web application to a database, handle form submissions, execute SQL queries, and perform CRUD operations.

The project helped me understand how the frontend, backend, and database work together in a simple web application.

## Possible Improvements

Some features that could be added in the future include:

* User login and authentication
* Better input validation and error handling
* Pagination for large numbers of student records
* Exporting student records to CSV or Excel
* Improved mobile responsiveness

## Project Status

This is a college mini-project created for learning and practice. It demonstrates the basic operations needed to manage student records through a web-based interface.