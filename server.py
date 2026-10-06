from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import sys
import os


app = FastAPI(
    title="VoiceExam API",
    description="Backend for VoiceExam AI Examination System"
)


exam_process = None


# ==================================================
# STUDENT FRONTEND
# ==================================================

@app.get("/")
def home():
    return FileResponse("student/index.html")


@app.get("/style.css")
def style():
    return FileResponse("student/style.css")


@app.get("/voice.js")
def voice_js():
    return FileResponse("student/voice.js")


# ==================================================
# START EXAM
# ==================================================

@app.post("/start-exam")
def start_exam():

    global exam_process

    # Check whether an exam is already running
    if exam_process is not None:

        if exam_process.poll() is None:

            return {
                "success": False,
                "message": "An examination is already running."
            }


    # Start exam controller
    exam_process = subprocess.Popen(
        [
            sys.executable,
            "exam_controller.py"
        ],
        cwd=os.getcwd()
    )


    return {
        "success": True,
        "message": "Voice examination started."
    }


# ==================================================
# CHECK EXAM STATUS
# ==================================================

@app.get("/exam-status")
def exam_status():

    global exam_process

    if exam_process is None:

        return {
            "running": False
        }


    if exam_process.poll() is None:

        return {
            "running": True
        }


    return {
        "running": False
    }