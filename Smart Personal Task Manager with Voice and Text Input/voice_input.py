import speech_recognition as sr

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
                return ""
            except sr.RequestError:
                print("Could not request results; check your network connection.")
                return ""
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                return ""

if __name__ == "__main__":
    vi = VoiceInput()
    task = vi.listen()
    print(f"Recognized task: {task}")
