import cv2
from deepface import DeepFace

def detect_emotion():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            print("Emotion:", emotion)
        except:
            pass

        cv2.imshow("Emotion Detector", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()