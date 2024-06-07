import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import screen_brightness_control as sbc

BRIGHTNESS = 5  # %5 parlaklık
NORMAL_BRIGHTNESS = sbc.get_brightness()  # Normal parlaklık %100

def get_camera():
    for cam_num in range(6):
        cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cam_num, cap
    raise ValueError("Cant find useable camera!")

def calculate_distance(w, W=6.3, f=600):
    return W * f / w

def set_brightness(distance, threshold=35):
    if distance < threshold:
        sbc.set_brightness(BRIGHTNESS)
    else:
        sbc.set_brightness(NORMAL_BRIGHTNESS)

def main(cam, quit_button='q'):
    try:
        if cam:
            cap = cv2.VideoCapture(cam, cv2.CAP_DSHOW)
        else:
            cam_num, cap = get_camera()
        detector = FaceMeshDetector(maxFaces=1)

        while True:
            success, frame = cap.read()
            if not success:
                raise ValueError("Cant use camera now!")

            frame, faces = detector.findFaceMesh(frame, draw=False)

            if faces:
                face = faces[0]
                pointLeft = face[145]
                pointRight = face[374]

                w, _ = detector.findDistance(pointLeft, pointRight)
                d = calculate_distance(w)

                if d <= 35:
                    cvzone.putTextRect(frame, "Be careful", (20, 70), 5, 3, (0, 0, 255))
                else:
                    cvzone.putTextRect(frame, "Good", (20, 70), 5, 3, (0, 255, 0))

                set_brightness(d)

                cvzone.putTextRect(frame,
                                   f"{int(d)} cm",
                                   (face[10][0] - 100, face[10][1] - 50),
                                   scale=2)

            cv2.imshow("Miyobi", frame)
            if cv2.waitKey(1) == ord(quit_button):
                break

        cap.release()
        cv2.destroyAllWindows()
    
    except ValueError as e:
        print(e)
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Welcome to Miyobi System! ")
    main(0, "q")
