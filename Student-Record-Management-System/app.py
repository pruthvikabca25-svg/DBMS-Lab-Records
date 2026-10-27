import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "studenthub_local_project_key"


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="student_db"
    )


def get_student_values(form):
    return (
        form.get("first_name", "").strip(),
        form.get("last_name", "").strip(),
        form.get("email", "").strip(),
        form.get("phone", "").strip() or None,
        form.get("gender", "") or None,
        form.get("date_of_birth", "") or None,
        form.get("course", "").strip(),
        form.get("department", "").strip() or None,
        int(form.get("semester", 0)),
        form.get("admission_year", "") or None,
        form.get("city", "").strip() or None
    )


@app.route("/")
def home():
    search_query = request.args.get("search", "").strip()

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if search_query:
            search_pattern = f"%{search_query}%"

            cursor.execute("""
                SELECT *
                FROM students
                WHERE CAST(student_id AS CHAR) LIKE %s
                   OR first_name LIKE %s
                   OR last_name LIKE %s
                   OR CONCAT(first_name, ' ', last_name) LIKE %s
                   OR email LIKE %s
                ORDER BY student_id DESC
            """, (
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern,
                search_pattern
            ))
        else:
            cursor.execute("""
                SELECT *
                FROM students
                ORDER BY student_id DESC
            """)

        students = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total_students
            FROM students
        """)
        total_students = cursor.fetchone()["total_students"]

        cursor.execute("""
            SELECT COUNT(*) AS recent_adds
            FROM students
            WHERE created_at >= NOW() - INTERVAL 7 DAY
        """)
        recent_adds = cursor.fetchone()["recent_adds"]

        cursor.execute("""
            SELECT COUNT(DISTINCT department) AS total_departments
            FROM students
            WHERE department IS NOT NULL
              AND department <> ''
        """)
        total_departments = cursor.fetchone()["total_departments"]

    finally:
        cursor.close()
        connection.close()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        recent_adds=recent_adds,
        total_departments=total_departments,
        search_query=search_query
    )


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        try:
            values = get_student_values(request.form)

            if not values[0] or not values[1] or not values[2] or not values[6]:
                flash("Please fill in all required fields.", "error")
                return redirect(url_for("add_student"))

            connection = get_db_connection()
            cursor = connection.cursor()

            try:
                cursor.execute("""
                    INSERT INTO students (
                        first_name,
                        last_name,
                        email,
                        phone,
                        gender,
                        date_of_birth,
                        course,
                        department,
                        semester,
                        admission_year,
                        city
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                """, values)

                connection.commit()

            finally:
                cursor.close()
                connection.close()

            flash("Student added successfully.", "success")
            return redirect(url_for("home"))

        except mysql.connector.IntegrityError:
            flash("This email address is already registered.", "error")

        except (ValueError, mysql.connector.Error):
            flash("Unable to add the student. Please check the details.", "error")

    return render_template("add.html")


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        if request.method == "POST":
            values = get_student_values(request.form)

            if not values[0] or not values[1] or not values[2] or not values[6]:
                flash("Please fill in all required fields.", "error")
                return redirect(url_for("edit_student", student_id=student_id))

            cursor.execute("""
                UPDATE students
                SET first_name = %s,
                    last_name = %s,
                    email = %s,
                    phone = %s,
                    gender = %s,
                    date_of_birth = %s,
                    course = %s,
                    department = %s,
                    semester = %s,
                    admission_year = %s,
                    city = %s
                WHERE student_id = %s
            """, values + (student_id,))

            connection.commit()

            flash("Student details updated successfully.", "success")
            return redirect(url_for("home"))

        cursor.execute("""
            SELECT *
            FROM students
            WHERE student_id = %s
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
            return "Student not found.", 404

        return render_template("edit.html", student=student)

    except mysql.connector.IntegrityError:
        flash("That email address is already registered.", "error")
        return redirect(url_for("edit_student", student_id=student_id))

    finally:
        cursor.close()
        connection.close()


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM students
            WHERE student_id = %s
        """, (student_id,))

        connection.commit()

        if cursor.rowcount:
            flash("Student deleted successfully.", "success")
        else:
            flash("Student record not found.", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)