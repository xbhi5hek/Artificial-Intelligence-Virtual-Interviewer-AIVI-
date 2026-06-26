import edge_tts
import asyncio
import os
import speech_recognition as sr
import time

class VoiceService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.voice = "en-US-GuyNeural"
        self.output_dir = "static/audio"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    async def speak_async(self, text, filename="question.mp3"):
        """Generates an MP3 file from text using edge-tts."""
        path = os.path.join(self.output_dir, filename)
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(path)
        return path

    def speak(self, text, filename="question.mp3"):
        """Synchronous wrapper for speak_async."""
        return asyncio.run(self.speak_async(text, filename))

    def listen(self, duration=5):
        """Listens to the microphone and returns the text."""
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return ""
            except sr.RequestError as e:
                print(f"STT Error: {e}")
                return ""
            except Exception as e:
                print(f"Listen error: {e}")
                return ""

voice_service = VoiceService()
