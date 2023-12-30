import cv2
import mediapipe as mp
import pyautogui

capture = cv2.VideoCapture(0) # Initialize The Camera Capture
if not capture.isOpened():
    print("Error : Camera Not Available...")
    exit()

# Initialize 'Hand_Detection' And 'Drawing_Utilities'
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size() # Get Screen Dimensions

index_y = 0
count = 1

while True: 

    ret, frame = capture.read() # To Take Input That Is Captured In Video Frame
    if not ret:
        print("Error : Failed To Capture Frame...")
        break

    frame = cv2.flip(frame, 1) # Flip The Frame.. '1' -> Y-Axis && '0' -> X-Axis
    frame_height, frame_width, _ = frame.shape     # Get Frame Dimensions
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert Frame Color To RGB

    # We Will Get Some Output After 'Processsing' The 'RGB_Frame' With 'Hand_Detector'
    output = hand_detector.process(rgb_frame) 
    hands = output.multi_hand_landmarks # There Are '21' Landmarks On Hand
    
    if hands:
        for hand in hands: # To Show Landmark Of Hand While Capturing Video
            drawing_utils.draw_landmarks(frame, hand) 
            landmarks = hand.landmark
            for id, mark in enumerate(landmarks):
                x = int(mark.x * frame_width)
                y = int(mark.y * frame_height)

                if id == 8: # To Identify The Tip Of Index Finger
                    cv2.circle(img = frame, center = (x,y), radius = 10, color = (0,255,0))

                    index_x = (screen_width/frame_width) * x
                    index_y = (screen_height/frame_height) * y

                    pyautogui.moveTo(index_x, index_y)
                    pyautogui.FAILSAFE = False
                
                if id == 4: # To Identify The Tip Of Thumb
                    cv2.circle(img = frame, center = (x,y), radius = 10, color = (0,255,0))

                    thumb_x = (screen_width/frame_width) * x
                    thumb_y = (screen_height/frame_height) * y

                    #print(abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        print("# Clicked.."+f"{count}")
                        count = count + 1
                        #pyautogui.sleep(0.5)
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)


    cv2.imshow("Virtual Mouse", frame)     # Show The Virtual Mouse Window
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Check for 'q' key press to exit the loop
        break


capture.release() # Release The Video Capture
cv2.destroyAllWindows() # Close The OpenCV Window