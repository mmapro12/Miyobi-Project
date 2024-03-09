import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import screen_brightness_control as brig


def main(cam, q_but):
    if cam:
        cam_num = cam
    else:

        if cv2.VideoCapture(5, cv2.CAP_DSHOW).isOpened():
            cam_num = 5
            f = 600
        elif cv2.VideoCapture(4, cv2.CAP_DSHOW).isOpened():
            cam_num = 4
            f = 600
        elif cv2.VideoCapture(3, cv2.CAP_DSHOW).isOpened():
            cam_num = 3
            f = 600
        elif cv2.VideoCapture(2, cv2.CAP_DSHOW).isOpened():
            cam_num = 2
            f = 600
        elif cv2.VideoCapture(1, cv2.CAP_DSHOW).isOpened():
            cam_num = 1
            f = 600
        elif cv2.VideoCapture(0, cv2.CAP_DSHOW).isOpened():
            cam_num = 0
            f = 620
        else:
            quit("Camera cant open!")

    quit_button = "q" if not q_but else str(q_but[0])

    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    detector = FaceMeshDetector(maxFaces=1)

    if not cap.isOpened():
        quit(f"Camera `{cam_num}` can't open!")

    while True:
        success, frame = cap.read()
        if not success:
            quit(f"Camera not usable!")

        # Finding faces
        frame, faces = detector.findFaceMesh(frame, draw=False)

        if faces:
            face = faces[0]
            pointLeft = face[145]
            pointRight = face[374]

            w, _ = detector.findDistance(pointLeft, pointRight)
            W = 6.3

            # Finding Focal Length
            # d = 30
            # f = (w * d) / W
            # print(f)


            d = W * f / w
            print(d)

            # Depth is close
            if d <= 35:
                cvzone.putTextRect(frame, "Be careful", (20, 70), 5, 3, (0, 0, 255))
                brig.set_brightness(20)
            else:
                cvzone.putTextRect(frame, "Good", (20, 70), 5, 3, (0, 255, 0))
                brig.set_brightness(100)

            # Adding text in the video
            cvzone.putTextRect(frame,
                               f"Depth: {int(d)} cm",
                               (face[10][0] - 100, face[10][1] - 50),
                               scale=2
                               )

        cv2.imshow("Eye Guard", frame)
        if cv2.waitKey(1) == ord(quit_button):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(0, "q")
