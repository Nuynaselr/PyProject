import datetime
import imutils
from imutils.video import FPS
import numpy as np
import sys
import cv2

if __name__ == '__main__':
    width = int(sys.argv[1])
    video = cv2.VideoCapture('output.avi')

    firstFrame = None

    fps = FPS().start()
    ret, frame_original = video.read()
    frame_original = imutils.resize(frame_original, width=width)
    image_array = np.array([frame_original])

    while True:
        fps.update()
        if frame_original is None:
            break

        text = "Unoccupied"

        frame_original = imutils.resize(frame_original, width=width)
        image_array = np.append(image_array, np.array([frame_original]), axis=0)

        frame_transform = np.mean(image_array, axis=0)
        frame_transform = frame_transform.astype(np.uint8)

        # изменение цветогового пространства
        gray = cv2.cvtColor(frame_transform, cv2.COLOR_BGR2GRAY)
        # Гауссовский блюр
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        gray_new_frame = cv2.cvtColor(frame_original, cv2.COLOR_BGR2GRAY)
        # Гауссовский блюр
        gray_new_frame = cv2.GaussianBlur(gray_new_frame, (21, 21), 0)

        firstFrame = gray

        # cv2.imshow("Gray", gray_new_frame)

        # вычитание слоев
        frameDelta = cv2.absdiff(firstFrame, gray_new_frame)
        # деление на черное и белое
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # утолщение белого
        thresh = cv2.dilate(thresh, None, iterations=20)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)


        # loop over the contours
        for c in cnts:
            # создает поля
            (x, y, w, h) = cv2.boundingRect(c)
            # отрисовка границ
            cv2.rectangle(frame_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"

        # draw the text and timestamp on the frame
        cv2.putText(frame_original, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame_original, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame_original.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # show the frame and record if the user presses a key
        # cv2.imshow("Security Feed", frame_original)
        # cv2.imshow("Thresh", thresh)
        # cv2.imshow("Frame Delta", frameDelta)



        if len(image_array) == 10:
            image_array = np.roll(image_array, -1, axis=0)
            image_array = np.delete(image_array, 9, axis=0)

        ret, frame_original = video.read()

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

        # cleanup the camera and close any open windows
    fps.stop()
    video.release()
    cv2.destroyAllWindows()


    with open('data.txt', 'a') as file:
        file.write('3:' + str(fps.fps()) + ' width: ' + str(width) + '\n')
