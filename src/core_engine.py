from init_engine import *
from internet_utility_engine import *
from speech_recognition_engine import *


def intro_music():
    ev_stop = Event()
    if ev_stop.is_set():
        ev_stop.wait()

    playsound(intro_file_path)
    # time.sleep(music.duration)  # prevent from killing
    ev_stop.clear()


def start_core_engine():
    while True:

        global frame

        _, frame = cap.read()

        frame = cv2.resize(frame, (1080, 720), fx=0, fy=0,
                           interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

        # all faces in the frame
        faces_cur_frame = face_recognition.face_locations(frame)
        # encodings of all faces in the frame
        encode_face = face_recognition.face_encodings(frame, faces_cur_frame)
        for encodeFace, faceLoc in zip(encode_face, faces_cur_frame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace, tolerance=0.6)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                if classNames[matchIndex] == "admin":
                    live_frame = cv2.rectangle(
                        frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255, 255), 2)
                    cv2.putText(live_frame, "Admin", (faceLoc[3], faceLoc[0]-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                else:
                    live_frame = cv2.rectangle(
                        frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 255, 255), 2)
                    cv2.putText(live_frame, "Subject: " + classNames[matchIndex], (faceLoc[3], faceLoc[0]-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        emotion, score = detector.top_emotion(frame)

        # to be used later
        emotions_list.append(emotion)

        # cv2.imwrite("../frame.jpg", frame)

        cv2.putText(frame, 'CAMERA 0', (30, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (5, 5, 5), 2)

        current_time_frame = time.ctime()
        cv2.putText(frame, current_time_frame, (744, 680),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (5, 5, 5), 2)

        cv2.putText(frame, current_location, (30, 680),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (5, 5, 5), 2)

        cv2.putText(frame, weather_info[0][0:2] + " Deg C - " + weather_info[1], (780, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (5, 5, 5), 2)

        out.write(frame)

        cv2.imshow("The Machine", frame)

        if cv2.waitKey(1) == ord('s'):
            t3 = Thread(target=(real_time_speech), args=(frame,))
            t3.setDaemon(True)
            t3.start()


if __name__ == "__main__":
    start_core_engine()
