CREATE DATABASE student_db;
USE student_db;

CREATE TABLE students(
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

ALTER TABLE students AUTO_INCREMENT = 1;

TRUNCATE TABLE students;

SELECT * FROM students;

SELECT COUNT(*) AS total_students
FROM students;

SELECT COUNT(DISTINCT department) AS total_departments
FROM students
WHERE department IS NOT NULL
AND department <> '';

SELECT *
FROM students
WHERE first_name LIKE '%rahul%'
   OR last_name LIKE '%rahul%'
   OR email LIKE '%rahul%';