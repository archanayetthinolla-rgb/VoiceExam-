const startBtn = document.getElementById("startBtn");

let recognition = null;
let examStarted = false;


// ==================================================
// TEXT TO SPEECH
// ==================================================

function speak(text) {

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "en-IN";
    speech.rate = 0.9;
    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}


// ==================================================
// BROWSER VOICE SUPPORT
// ==================================================

if ("webkitSpeechRecognition" in window) {

    recognition = new webkitSpeechRecognition();

    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.lang = "en-IN";


    recognition.onstart = function () {

        console.log("🎤 Browser microphone started.");

    };


    recognition.onresult = function (event) {

        const result =
            event.results[
                event.results.length - 1
            ][0].transcript;

        console.log(
            "Browser heard:",
            result
        );
    };


    recognition.onerror = function (event) {

        console.log(
            "Browser microphone error:",
            event.error
        );

    };

}


// ==================================================
// START VOICE EXAM
// ==================================================

startBtn.addEventListener(
    "click",
    async function () {

        if (examStarted) {

            speak(
                "The examination is already running."
            );

            return;
        }


        examStarted = true;


        // Disable button
        startBtn.disabled = true;

        startBtn.innerText =
            "Starting Voice Exam...";


        speak(
            "Starting Voice Exam."
        );


        // --------------------------------------------------
        // IMPORTANT:
        // Stop browser speech recognition because
        // Python Whisper will use the microphone.
        // --------------------------------------------------

        if (recognition) {

            try {

                recognition.stop();

            } catch (error) {

                console.log(
                    "Recognition already stopped."
                );

            }
        }


        // --------------------------------------------------
        // CONNECT TO FASTAPI
        // --------------------------------------------------

        try {

            const response = await fetch(
                "/start-exam",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json"
                    }
                }
            );


            const data =
                await response.json();


            console.log(
                "Server response:",
                data
            );


            if (data.success) {

                startBtn.innerText =
                    "🎙️ Voice Exam Running";

                speak(
                    "Voice examination started. " +
                    "Please listen to the computer."
                );


                // Check status
                checkExamStatus();

            } else {

                examStarted = false;

                startBtn.disabled = false;

                startBtn.innerText =
                    "Start Voice Exam";


                speak(
                    data.message ||
                    "The examination could not be started."
                );
            }


        } catch (error) {

            console.error(
                "Connection error:",
                error
            );


            examStarted = false;

            startBtn.disabled = false;

            startBtn.innerText =
                "Start Voice Exam";


            speak(
                "I could not connect to the VoiceExam server. " +
                "Please make sure the server is running."
            );
        }

    }
);


// ==================================================
// CHECK EXAM STATUS
// ==================================================

async function checkExamStatus() {

    try {

        const response = await fetch(
            "/exam-status"
        );


        const data =
            await response.json();


        console.log(
            "Exam status:",
            data
        );


        if (data.running) {

            setTimeout(
                checkExamStatus,
                3000
            );

        } else {

            examStarted = false;

            startBtn.disabled = false;

            startBtn.innerText =
                "Start Voice Exam";

            speak(
                "The VoiceExam session has ended."
            );
        }


    } catch (error) {

        console.log(
            "Unable to check exam status."
        );

    }

}