import RPi.GPIO as GPIO
import time
import cv2


def pwm_setup():
    
    global left_freq
    left_freq = 5000
    
    global right_freq
    right_freq = 3000
    
    global person_freq
    person_freq = 1500
    
    global stair_status
    person_status = 0
    
    global BUZZER_PIN_E
    BUZZER_PIN_E = 18 
    
    global BUZZER_PIN_OBJ
    BUZZER_PIN_OBJ = 17

    # Set up GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN_E, GPIO.OUT)
    GPIO.setup(BUZZER_PIN_OBJ, GPIO.OUT)


    global pwm
    pwm = GPIO.PWM(BUZZER_PIN_E, 1)  
    pwm.start(50)  
    
    global pwm2
    pwm2 = GPIO.PWM(BUZZER_PIN_OBJ, 1)



def play_tone(frequency, pin):
    pwm.ChangeFrequency(frequency)  

def stop_tone(pin):
    pwm.ChangeFrequency(0)

def detect_face():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        print("Error loading Haar cascade classifier!")
        return 0

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture device.")
        return 0

    ret, frame = cap.read()
    cap.release()  

    if not ret:
        print("Failed to capture frame.")
        return 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    return 1 if len(faces) > 0 else 0




if __name__ == "__main__":
    
    pwm_setup()
    
    
    while(1):
        
        #read edge_distance_r
        edge_status_r = 0
        #read_edge_distance_l
        edge_status_l = 0
        
        #read object detection
        person_status = detect_face()
        
        if edge_status_r == 1:
            print("Entered_R")
            play_tone(right_freq, 1)
            
            
        elif edge_status_l == 1:
            print("Entered_L")
            play_tone(left_freq, 1)
            
        if person_status == 1:
            print("Entered_Person_Found")
            play_tone(person_freq, 1)
            
            
            
            
        
    