# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
from sensor.sensor import Sensor
import os
os.environ['DISPLAY'] = ':0'

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

STREAM = os.environ['STREAM_URL']
HOST = os.environ['MQTT_HOST']
PORT = 1883
USERNAME = os.environ['MQTT_USER']
PASSWORD = os.environ['MQTT_PASSWORD']
MIN_AREA = os.environ['MIN_AREA']
if args.get("video", None) is None:
    vs = VideoStream(STREAM).start()
    time.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream

firstFrame = None
lastUploaded = datetime.datetime.now()
sensor = Sensor(username=USERNAME, password=PASSWORD, host=HOST)
# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text

    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    timestamp = datetime.datetime.now()
    text = "Khong co ai"
    occupied = False
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
# compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < float(MIN_AREA):
            continue

#         print("area:", str(cv2.contourArea(c)))
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Thay roi nha"
        occupied = True
# draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    sc = (timestamp - lastUploaded).seconds
#     print("sc:", sc)
#     if (occupied):
#     if (sc >= 3):
#     print("[INFO]", text)
    sensor.setState(occupied)
#         lastUploaded = timestamp
    # show the frame and record if the user presses a key
#     cv2.imshow("Security Feed", frame)
#     cv2.imshow("Thresh", thresh)
#     cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
