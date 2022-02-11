import speech_recognition as sr
from gtts import gTTS
import pyglet
from threading import *
from init_engine import *
import time
from internet_utility_engine import *

sample_rate = 48000

chunk_size = 1024

r = sr.Recognizer()


def real_time_speech(frame):
    ev_stop = Event()
    if ev_stop.is_set():
        ev_stop.wait()
    with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
        # read the audio data from the default microphone
        r.adjust_for_ambient_noise(source)
        audio_data = r.listen(source, timeout=25)
        try:
            # convert speech to text
            text = r.recognize_google(audio_data)
            print(text)
            command = text.split()[0]
            query = text.split()[1:]

            if command == "bye":
                ev_stop.clear()
                text_to_speech("Bye, see you later")
                time.sleep(1)
                out.write(frame)

                out.release()

                out.release()
                cap.release()
                cv2.destroyAllWindows()
            if command == "search":
                ev_stop.clear()

                text_to_speech("Searching")

                time.sleep(2)

                text_to_speech("Gathering fetched results")

                search_google(query)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))


def text_to_speech(text):
    tts = gTTS(text, lang="en", tld="co.uk")
    tts.save(voice_file_path)
    voice = pyglet.media.load(voice_file_path, streaming=False)
    voice.play()

    # time.sleep(voice.duration)  # prevent from killing
    os.remove(voice_file_path)  # remove temporary file
