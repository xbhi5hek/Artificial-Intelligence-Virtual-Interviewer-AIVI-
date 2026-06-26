import cv2
import time

class VideoService:
    def __init__(self):
        self.cap = None
        self.last_frame = None
        self.movement_detected = False
        self.is_running = False

    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.is_running = True

    def stop(self):
        if self.cap:
            self.cap.release()
        self.is_running = False

    def get_frame(self):
        if not self.is_running:
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Simple Movement Detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.last_frame is None:
            self.last_frame = gray
            return frame

        frame_delta = cv2.absdiff(self.last_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Check if movement is significant
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self.movement_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.movement_detected = True

        self.last_frame = gray
        
        if self.movement_detected:
            cv2.putText(frame, "Movement Detected", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        return frame

    def generate_frames(self):
        while self.is_running:
            frame = self.get_frame()
            if frame is None:
                break
            
            # Encode as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

video_service = VideoService()
