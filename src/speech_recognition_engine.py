import speech_recognition as sr
from gtts import gTTS
from threading import *
from init_engine import *
import time
from internet_utility_engine import *
from playsound import *

sample_rate = 48000

chunk_size = 1024

r = sr.Recognizer()

terminate_session_exp = ["bye", "exit", "quit",
                         "goodbye", "good bye", "see you later"]

image_ocr_exp = ["perform ocr on this image",
                 "perform ocr on this", "ocr on this image", "ocr"]


def real_time_speech(frame):
    ev_stop = Event()
    if ev_stop.is_set():
        ev_stop.wait()
    with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        # read the audio data from the default microphone
        audio_data = r.listen(source, timeout=25)
        try:
            # convert speech to text
            text = r.recognize_google(audio_data)
            print(text)
            command = text.split()[0]
            query = text.split()[1:]

            if text in terminate_session_exp:
                ev_stop.clear()
                text_to_speech("Bye, see you later")
                time.sleep(1)
                out.write(frame)

                out.release()
                cap.release()
                cv2.destroyAllWindows()
            if command == "search":
                ev_stop.clear()

                text_to_speech("Searching")

                time.sleep(2)

                text_to_speech("Gathering fetched results")

                search_google(query)
            if text in image_ocr_exp:
                cv2.imwrite(image_ocr_file_path, frame)
                time.sleep(1)
                img = cv2.imread(image_ocr_file_path)
                norm_img = np.zeros((img.shape[0], img.shape[1]))
                img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
                img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
                img = cv2.GaussianBlur(img, (1, 1), 0)
                text = pytesseract.image_to_string(img)
                text_to_speech(text)

                time.sleep(1)

                results = pytesseract.image_to_data(
                    img, output_type=Output.DICT)

                for i in range(0, len(results["text"])):
                    x = results["left"][i]
                    y = results["top"][i]

                    w = results["width"][i]
                    h = results["height"][i]
                    text = results["text"][i]
                    conf = int(results["conf"][i])
                    if conf > 70:
                        text = "".join(
                            [c if ord(c) < 128 else "" for c in text]).strip()
                        cv2.rectangle(
                            img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(img, text, (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
                cv2.imshow("image", img)
        except sr.UnknownValueError:
            print()
        except sr.RequestError as e:
            print()


def text_to_speech(text):
    tts = gTTS(text, lang="en", tld="co.uk")
    tts.save(voice_file_path)

    playsound(voice_file_path)

    # time.sleep(voice.duration)  # prevent from killing
    os.remove(voice_file_path)  # remove temporary file
