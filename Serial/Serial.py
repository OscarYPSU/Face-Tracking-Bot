import serial
import threading
import time
import cv2
#emotion detection
from fer import FER

class serial:
    def __init__(self, baurRate):
        self.baurRate = baurRate
        self.ser = serial.Serial('COM3', self.baurRate, timeout=1)
        
        # emotion detecter
        self.topEmotions = ""
        self.emotion_detector = FER(mtcnn=True)  # mtcnn=True uses better face detection internally

    # sends emotions over tot e serial to the micro controller
    def sendEmotions(self):
        
        while True:
            if self.topEmotions:
                data = f"EMO##{str(self.topEmotions).lower()}"
                print(f"sending emotion data over: {data}\n")
                self.ser.write(data.encode()) 
                
                # waits a minute to allow oled screen to settle animations            
                time.sleep(60)
    
    def detectFace(self):
        while True:
            if len(self.faces) > 0:
                (x, y, w, h) = self.faces[-1]  # latest (last) face in the list
                self.face_center_x = x + w // 2
                self.face_center_y = y + h // 2
                sensY = .5
                sens = .35
                
                cv2.circle(self.frame, (self.face_center_x, self.face_center_y), 5, (255, 0, 0), -1)

                # Calculate offsets
                distanceY = int((self.frame_center_y - self.face_center_y) * sensY)
                distanceX = int((self.frame_center_x - self.face_center_x) * sens)

                data = f"Y{distanceY:03d}X{distanceX:03d}\n"
                print(f"sending data over to serial: {data}\n")

                self.ser.write(data.encode())

            time.sleep(1)  # smaller delay for smoother tracking
    
    def start(self):
        print("Starting serial face detection\n")
        
        # ESP32 camera stream
        url = "http://104.38.178.36:81/stream"
        cap = cv2.VideoCapture(url)
        
        # debugging
        if not cap.isOpened():
            print("❌ Unable to open stream.")
            exit()
        print("✅ Stream opened successfully!")
        
        # set up for face recognition
        self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_center_x = self.frame_width // 2
        self.frame_center_y = self.frame_height // 2
        
        # Load Haar Cascade (comes with OpenCV)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        i=0
        
        while True:
            self.ret, self.frame = cap.read()
            if not self.ret:
                print("⚠️ Failed to grab frame.")
                break

            # Convert to grayscale (lighter for detection)
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # Detect faces (scaleFactor=1.1, minNeighbors=5 are standard fast settings)
            self.faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

            if i == 0:
                face_thread = threading.Thread(target=self.detectFace)
                emotionDataThread = threading.Thread(target=self.sendEmotions)
                i += 1
                face_thread.start()
                emotionDataThread.start()

            # Detect emotions directly
            result = self.emotion_detector.detect_emotions(self.frame)
            for face in result:
                (x, y, w, h) = face["box"]
                top_emotion = self.emotion_detector.top_emotion(self.frame[y:y+h, x:x+w])
                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(self.frame, f"{top_emotion}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
            
            # Draw frame center
            cv2.circle(self.frame, (self.frame_center_x, self.frame_center_y), 5, (0, 0, 255), -1)

            cv2.imshow("Face Detection (Lightweight)", self.frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    
            