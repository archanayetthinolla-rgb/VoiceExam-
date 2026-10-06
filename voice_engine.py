import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
import pyttsx3
import tempfile
import os

# -----------------------------
# SETTINGS
# -----------------------------

SAMPLE_RATE = 16000
RECORD_SECONDS = 5
MICROPHONE = 9

# -----------------------------
# TEXT TO SPEECH
# -----------------------------

engine = pyttsx3.init()

def speak(text):
    print("Computer:", text)
    engine.say(text)
    engine.runAndWait()


# -----------------------------
# LOAD WHISPER
# -----------------------------

print("Loading Whisper model...")

model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded!")


# -----------------------------
# SPEECH TO TEXT
# -----------------------------

def listen():

    print("\n🎤 Listening...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MICROPHONE
    )

    sd.wait()

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as file:
        filename = file.name

    sf.write(filename, audio, SAMPLE_RATE)

    print("🧠 Converting speech to text...")

    segments, info = model.transcribe(
        filename,
        language="en",
        vad_filter=True
    )

    segments = list(segments)

    text = " ".join(
        segment.text for segment in segments
    ).strip()

    os.remove(filename)

    return text