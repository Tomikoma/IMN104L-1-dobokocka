import cv2
import numpy as np
from imutils import resize


lowerWhite = np.array([25, 0, 0], dtype="uint8")
upperWhite = np.array([200, 25, 250], dtype="uint8")



def getBoundingBoxes(nlabels, stats) -> list:
    bboxes = list()
    # iterating over the labels
    for label in range(1, nlabels):
        # getting stats of the label
        x = stats[label, cv2.CC_STAT_LEFT] - 3
        y = stats[label, cv2.CC_STAT_TOP] - 3
        width = stats[label, cv2.CC_STAT_WIDTH] + 3
        height = stats[label, cv2.CC_STAT_HEIGHT] + 3
        # constructing bounding box from stats
        bbox = (x, y), (x + width, y + height)
        # appending to list if not too small
        if width > 30 and height > 30:
            bboxes.append(bbox)

    return bboxes


def cropImage(frame, bbox) -> np.ndarray:
    img = frame[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
    return img


def getDiceValue(path: str) -> int:
    value = 0
    img = cv2.imread(path)
    img = resize(img, 1000, 1000)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerWhite, upperWhite)
    res = cv2.bitwise_and(img, img, mask=mask)

    grayImg = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    output = cv2.connectedComponentsWithStats(grayImg, 8)
    nlabels = output[0]
    stats = output[2]
    bboxes = getBoundingBoxes(nlabels, stats)

    for bbox in bboxes:
        cv2.rectangle(img, (bbox[0][0], bbox[0][1]),
                      (bbox[1][0], bbox[1][1]), (0, 0, 255), 1)
        croppedImage = cropImage(img, bbox)
        if not croppedImage.any():
            continue
        grayCroppedImage = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(grayCroppedImage, cv2.HOUGH_GRADIENT, 1.05, croppedImage.shape[0] / 4,
                                   param1=125, param2=20,
                                   minRadius=4, maxRadius=30)
        if circles is not None:
            value += len(circles)
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(croppedImage, center, 1, (255, 0, 0), 3)
                # circle outline
                radius = i[2]
                cv2.circle(croppedImage, center, radius, (50, 255, 100), 3)
            #print("Value:", len(circles[0]))

            #cv2.imshow("crop", croppedImage)
            #cv2.waitKey(0)

    return value
