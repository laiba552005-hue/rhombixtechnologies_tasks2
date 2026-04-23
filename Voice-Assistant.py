import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import logging
import wikipedia
from PIL import Image
import pytesseract

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ProfessionalAssistant:
    def __init__(self, name="Laiba"):
        self.name = name
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')

        self.engine.setProperty('voice', self.voices[0].id)
        self.engine.setProperty('rate', 175)

    def speak(self, text):
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            logging.info("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"User: {query}")
            return query.lower()

        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return "none"

        except sr.RequestError:
            self.speak("Network error.")
            return "none"

    # Image scanner
    def scan_image(self, image_path):
        try:
            text = pytesseract.image_to_string(Image.open(image_path))
            self.speak("Scanning image...")

            print("Scanned Text:\n", text)

            if text.strip():
                self.speak(text)
            else:
                self.speak("No text found in image.")

        except Exception as e:
            self.speak("Scanning failed.")
            print(e)

    def execute_task(self, command):

        # Name
        if 'your name' in command or 'who are you' in command:
            self.speak("I am Laiba, your Python voice assistant")

        # Time
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            self.speak(f"The time is {time}")


        # Date
        elif 'date' in command:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            self.speak(f"Today's date is {date}")

        # Google
        elif 'open google' in command:
            self.speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # YouTube
        elif 'youtube' in command:
            self.speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        # WhatsApp
        elif 'whatsapp' in command:
            self.speak("Opening WhatsApp")
            webbrowser.open("https://web.whatsapp.com")

        # Wikipedia
        elif 'wikipedia' in command:
            self.speak("Searching Wikipedia...")
            command = command.replace("wikipedia", "")
            result = wikipedia.summary(command, sentences=2)
            self.speak(result)

        # Search
        elif 'search' in command:
            query = command.replace("search", "").strip()
            self.speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")




        #  SCANNER COMMAND
        elif 'scan image' in command:
            self.speak("Please enter image path")
            path = input("Enter image path: ")
            self.scan_image(path)

        # Exit
        elif 'exit' in command or 'shutdown' in command:
            self.speak("Goodbye! Shutting down.")
            return False

        else:
            self.speak("I am still learning this command.")

        return True


# MAIN
if __name__ == "__main__":
    assistant = ProfessionalAssistant(name="Laiba")

    assistant.speak("I am Laiba, how can I help you?")

    running = True

    while running:
        user_input = assistant.listen()

        if user_input != "none":
            running = assistant.execute_task(user_input)
