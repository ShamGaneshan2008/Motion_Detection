import cv2
import streamlit as st
from datetime import datetime

st.title("Motion Detector")
start = st.button("Start Camera")

if start:
    images = st.image([])
    video = cv2.VideoCapture('http://10.140.50.137:4747/video')

    while True:
        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get current time as a datetime object
        time = datetime.now()

        # Get day and time add them to the frame
        cv2.putText(img=frame, text=time.strftime("%A"), org=(20,60),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255,255,255),
                    thickness=2, lineType=cv2.LINE_4)
        cv2.putText(img=frame, text=time.strftime("%H:%M:%S"), org=(20,100),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255,0,0),
                    thickness=2, lineType=cv2.LINE_4)

        images.image(frame)
