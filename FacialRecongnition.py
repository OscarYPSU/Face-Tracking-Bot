import cv2
import serial
import time
import threading

#emotion detection
from fer import FER
# Initialize FER detector outside the thread
emotion_detector = FER(mtcnn=True)  # mtcnn=True uses better face detection internally


lock = threading.Lock()

def detectFace():
    global faces, frame
    while True:
        if len(faces) > 0:
            (x, y, w, h) = faces[-1]  # latest (last) face in the list
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            sensY = .5
            sens = .35
            
            cv2.circle(frame, (face_center_x, face_center_y), 5, (255, 0, 0), -1)

            # Calculate offsets
            distanceY = int((frame_center_y - face_center_y) * sensY)
            distanceX = int((frame_center_x - face_center_x) * sens)

            data = f"Y{distanceY:03d}X{distanceX:03d}\n"
            print(f"sending data over to serial: {data}\n")

            ser.write(data.encode())

        time.sleep(1)  # smaller delay for smoother tracking
        
# Initialize serial port
ser = serial.Serial('COM3', 9600, timeout=1)

# ESP32 camera stream
url = "http://104.38.178.36:81/stream"
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("❌ Unable to open stream.")
    exit()

print("✅ Stream opened successfully!")

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_center_x = frame_width // 2
frame_center_y = frame_height // 2

# Load Haar Cascade (comes with OpenCV)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
i=0
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to grab frame.")
        break

    # Convert to grayscale (lighter for detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces (scaleFactor=1.1, minNeighbors=5 are standard fast settings)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    if i == 0:
        face_thread = threading.Thread(target=detectFace)
        i += 1
        face_thread.start()

    # Detect emotions directly
    result = emotion_detector.detect_emotions(frame)
    for face in result:
        (x, y, w, h) = face["box"]
        top_emotion = emotion_detector.top_emotion(frame[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{top_emotion}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
    
    # Draw frame center
    cv2.circle(frame, (frame_center_x, frame_center_y), 5, (0, 0, 255), -1)

    cv2.imshow("Face Detection (Lightweight)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
