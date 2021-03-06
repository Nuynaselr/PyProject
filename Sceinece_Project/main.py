import datetime
import imutils
from time import sleep

import cv2

video = cv2.VideoCapture('output.avi')

firstFrame = None
while True:

    # считываем видеопоток по кадрово
    ret, frame = video.read()
    text = "Unoccupied"

    if frame is None:
        break

    # изменяем размер
    frame = imutils.resize(frame, width=500)
    # изменение цветогового пространства
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Гауссовский блюр
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # вычитание слоев
    frameDelta = cv2.absdiff(firstFrame, gray)
    # деление на черное и белое
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # утолщение белого
    thresh = cv2.dilate(thresh, None, iterations=10)

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # создает поля
        (x, y, w, h) = cv2.boundingRect(c)
        # отрисовка границ
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
    sleep(0.1)

# cleanup the camera and close any open windows
video.release()
cv2.destroyAllWindows()