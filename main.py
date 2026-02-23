import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread


os.makedirs("images", exist_ok=True)

# This is the link for the Droid camera
video = cv2.VideoCapture(os.getenv("CAMERA_URL"))
time.sleep(1)  # simply pauses the program for some time

first_frame = None       # background frame not set yet
status_list = [0, 0]     # stores motion status (previous & current)
frame_per_sec = 1        # used to name images

img_w_object = None      # stores image path with detected object
image_saved = False     # ensures only ONE image per motion event


def clean_folder():
    print("clean_folder function started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder function ended")


while True:
    status = 0
    check, frame = video.read()  # reads current frame from camera

    # if frame is not received, skip this iteration
    if not check or frame is None:
        continue

    # convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # apply Gaussian blur to reduce noise
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # set the first frame as background and skip detection
    if first_frame is None:
        first_frame = gray_frame_gau
        continue

    # compare current frame with background frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # convert difference image into black and white
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]

    # make white regions thicker for better contour detection
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # find outlines of moving objects
    contours, _ = cv2.findContours(
        dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:
        # ignore small movements
        if cv2.contourArea(contour) < 6000:
            continue

        # draw rectangle around detected motion
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

        status = 1  # motion detected

        # save only ONE image per motion event
        if not image_saved:
            img_w_object = f"images/{frame_per_sec}.png"
            cv2.imwrite(img_w_object, frame)
            frame_per_sec += 1
            image_saved = True

    # store last two statuses
    status_list.append(status)
    status_list = status_list[-2:]

    # when motion ends (1 → 0), send email
    if status_list[0] == 1 and status_list[1] == 0:
        if img_w_object:
            email_thread = Thread(
                target=send_email, args=(img_w_object,)
            )
            email_thread.start()
            email_thread.join()   # wait until email is sent
            clean_folder()        # delete images after email

            image_saved = False
            img_w_object = None

    # show video with motion rectangle
    cv2.imshow("Video", frame)

    # wait 1 millisecond for key press
    key = cv2.waitKey(1)

    # press 'q' to quit
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
