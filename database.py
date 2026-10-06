import sqlite3
from datetime import datetime


# ==================================================
# DATABASE SETTINGS
# ==================================================

DATABASE_NAME = "voiceexam.db"


# ==================================================
# CREATE DATABASE TABLE
# ==================================================

def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==================================================
# SAVE EXAM RESULT
# ==================================================

def save_result(
    student_name,
    score,
    total_questions,
    percentage,
    status="Completed"
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    exam_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO exam_results
        (
            student_name,
            exam_date,
            score,
            total_questions,
            percentage,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        exam_date,
        score,
        total_questions,
        percentage,
        status
    ))

    connection.commit()
    connection.close()


# ==================================================
# GET ALL RESULTS
# ==================================================

def get_results():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            student_name,
            exam_date,
            score,
            total_questions,
            percentage,
            status
        FROM exam_results
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


# ==================================================
# CREATE DATABASE WHEN FILE IS RUN
# ==================================================

if __name__ == "__main__":

    create_database()

    print("VoiceExam database created successfully.")