import json
import time

from voice_engine import speak, listen
from database import create_database, save_result


# ==================================================
# DATABASE
# ==================================================

create_database()


# ==================================================
# LOAD QUESTIONS
# ==================================================

with open("questions.json", "r") as file:
    questions = json.load(file)


# ==================================================
# SETTINGS
# ==================================================

EXAM_DURATION = 5 * 60
total_questions = len(questions)

# Store confirmed answers
answers = {}

start_time = None


# ==================================================
# ANSWER DETECTION
# ==================================================

def detect_answer(student_text, options):

    text = student_text.lower().strip()

    # Option commands
    if "option a" in text or text in ["a", "ay"]:
        return "A"

    if "option b" in text or text in ["b", "bee", "be"]:
        return "B"

    if "option c" in text or text in ["c", "see", "sea"]:
        return "C"

    if "option d" in text or text in ["d", "dee"]:
        return "D"

    # Match complete option text
    for letter, option_text in options.items():

        option_text_lower = option_text.lower()

        if option_text_lower in text:
            return letter

        # Match important words
        words = option_text_lower.split()

        matches = 0

        for word in words:

            if len(word) > 3 and word in text:
                matches += 1

        if matches >= 2:
            return letter

    return None


# ==================================================
# TIME
# ==================================================

def remaining_time():

    remaining = EXAM_DURATION - (
        time.time() - start_time
    )

    return max(0, int(remaining))


def announce_time():

    remaining = remaining_time()

    minutes = remaining // 60
    seconds = remaining % 60

    speak(
        f"You have {minutes} minutes "
        f"and {seconds} seconds remaining."
    )


# ==================================================
# READ QUESTION
# ==================================================

def read_question(index):

    item = questions[index]

    speak(
        f"Question {index + 1}. "
        + item["question"]
    )

    for letter, option in item["options"].items():

        speak(
            f"Option {letter}. {option}"
        )

    # Tell previously saved answer
    if index in answers:

        speak(
            f"You previously selected "
            f"Option {answers[index]}."
        )


# ==================================================
# GET FINAL SCORE
# ==================================================

def calculate_score():

    score = 0

    for index, selected_answer in answers.items():

        correct_answer = questions[index]["answer"]

        if selected_answer == correct_answer:
            score += 1

    return score


# ==================================================
# STUDENT NAME
# ==================================================

speak("Welcome to VoiceExam.")

speak("Please say your name.")

name = listen()

if not name:

    speak(
        "I could not hear your name. "
        "The examination cannot start."
    )

    exit()


speak(
    f"Hello {name}. "
    "Your examination is starting."
)

speak(
    "You have five minutes to complete "
    "the examination."
)


# ==================================================
# START TIMER
# ==================================================

start_time = time.time()


# ==================================================
# CURRENT QUESTION
# ==================================================

current_question = 0

exam_submitted = False


# ==================================================
# MAIN EXAM LOOP
# ==================================================

while current_question < total_questions:

    # --------------------------------------------------
    # TIME CHECK
    # --------------------------------------------------

    if remaining_time() <= 0:

        speak(
            "Your examination time is over."
        )

        break


    # --------------------------------------------------
    # READ CURRENT QUESTION
    # --------------------------------------------------

    read_question(current_question)


    # --------------------------------------------------
    # QUESTION LOOP
    # --------------------------------------------------

    while True:

        # Time check
        if remaining_time() <= 0:

            speak(
                "Your examination time is over."
            )

            current_question = total_questions
            break


        speak(
            "Please answer, or say "
            "Repeat, Time, Next, Previous, or Submit."
        )

        command = listen()


        # --------------------------------------------------
        # EMPTY INPUT
        # --------------------------------------------------

        if not command:

            speak(
                "I could not hear you. "
                "Please try again."
            )

            continue


        command = command.lower().strip()


        # ==================================================
        # REPEAT
        # ==================================================

        if "repeat" in command:

            read_question(current_question)

            continue


        # ==================================================
        # TIME
        # ==================================================

        if "time" in command:

            announce_time()

            continue


        # ==================================================
        # PREVIOUS
        # ==================================================

        if "previous" in command:

            if current_question > 0:

                current_question -= 1

                speak(
                    "Going to the previous question."
                )

                break

            else:

                speak(
                    "This is the first question."
                )

                continue


        # ==================================================
        # NEXT
        # ==================================================

        if "next" in command:

            if current_question in answers:

                speak(
                    "Moving to the next question."
                )

                current_question += 1

                break

            else:

                speak(
                    "You have not answered this question yet."
                )

                continue


        # ==================================================
        # SUBMIT
        # ==================================================

        if "submit" in command:

            answered = len(answers)

            speak(
                f"You have answered {answered} "
                f"out of {total_questions} questions."
            )

            speak(
                "Are you sure you want to submit? "
                "Say Confirm or Cancel."
            )

            confirmation = listen()


            if confirmation:

                confirmation = confirmation.lower()


                if "confirm" in confirmation:

                    speak(
                        "Your examination is being submitted."
                    )

                    exam_submitted = True

                    current_question = total_questions

                    break


                elif "cancel" in confirmation:

                    speak(
                        "Submission cancelled."
                    )

                    continue


                else:

                    speak(
                        "Please say Confirm or Cancel."
                    )

                    continue

            continue


        # ==================================================
        # ANSWER DETECTION
        # ==================================================

        selected = detect_answer(
            command,
            questions[current_question]["options"]
        )


        if selected is None:

            speak(
                "I could not identify your answer."
            )

            speak(
                "Please say Option A, Option B, "
                "Option C, or Option D."
            )

            continue


        # ==================================================
        # CONFIRM ANSWER
        # ==================================================

        speak(
            f"You selected Option {selected}."
        )

        speak(
            "Say Confirm or Redo."
        )

        confirmation = listen()


        if not confirmation:

            speak(
                "I could not hear you."
            )

            continue


        confirmation = confirmation.lower().strip()


        # ==================================================
        # CONFIRM
        # ==================================================

        if "confirm" in confirmation:

            # Save / replace answer
            answers[current_question] = selected

            speak(
                "Answer confirmed."
            )

            # Automatically move to next question
            current_question += 1

            break


        # ==================================================
        # REDO
        # ==================================================

        elif "redo" in confirmation:

            speak(
                "Okay. Please answer the question again."
            )

            continue


        # ==================================================
        # UNKNOWN CONFIRMATION
        # ==================================================

        else:

            speak(
                "Please say Confirm or Redo."
            )

            continue


# ==================================================
# FINAL SCORE
# ==================================================

score = calculate_score()


# ==================================================
# PERCENTAGE
# ==================================================

percentage = (
    score / total_questions * 100
    if total_questions > 0
    else 0
)


# ==================================================
# SAVE RESULT
# ==================================================

save_result(
    student_name=name,
    score=score,
    total_questions=total_questions,
    percentage=percentage,
    status="Completed"
)


# ==================================================
# FINAL MESSAGE
# ==================================================

speak(
    f"The examination is completed. "
    f"You answered {len(answers)} "
    f"out of {total_questions} questions."
)

speak(
    f"Your final score is "
    f"{score} out of {total_questions}."
)


# ==================================================
# TERMINAL RESULT
# ==================================================

print()
print("================================")
print("        VOICE EXAM RESULT")
print("================================")
print("Student       :", name)
print("Answered      :", len(answers))
print("Score         :", score, "/", total_questions)
print("Percentage    :", round(percentage, 2), "%")
print("Status        : Saved")
print("================================")