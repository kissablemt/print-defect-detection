import random
import numpy as np
import cv2
import imutils
import my_transform

img1 = cv2.imread('/Users/wzy/Pictures/opencv_test/std.jpeg')
img2 = cv2.imread('/Users/wzy/Pictures/opencv_test/test.jpeg')

img1 = cv2.resize(img1, (int(img2.shape[1]), int(img2.shape[0])))

# 压缩
img1 = imutils.resize(img1, width=800)
img2 = imutils.resize(img2, width=800)

# 灰度处理
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 滤波
blur1 = cv2.GaussianBlur(img1, (5, 5), 0)
blur2 = cv2.GaussianBlur(img2, (5, 5), 0)

bin1 = cv2.threshold(gray1, 127, 255, cv2.THRESH_BINARY)[1]
bin2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)[1]

dst1, contours1, hierarchy1 = cv2.findContours(bin1, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
dst2, contours2, hierarchy2 = cv2.findContours(bin2, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

contours1.sort(key=lambda x: len(x), reverse=True)
contours2.sort(key=lambda x: len(x), reverse=True)

dst1 = 0*dst1 + 255
dst2 = 0*dst2 + 255
cv2.drawContours(dst1, contours1, 0, (0, 0, 0), 3)
cv2.drawContours(dst2, contours2, 0, (0, 0, 0), 3)

tr = my_transform.transform(img1, img2)
gray3 = cv2.cvtColor(tr, cv2.COLOR_BGR2GRAY)
bin3 = cv2.threshold(gray3, 127, 255, cv2.THRESH_BINARY)[1]
dst3, contours3, hierarchy3 = cv2.findContours(bin3, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

# cv2.imshow("dst1", dst1)
# cv2.imshow("dst2", dst2)
# cv2.imshow("dst3", tr)
dst1 = img1.copy()
x, y, w, h = cv2.boundingRect(contours1[0])
cv2.rectangle(dst1, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('contours.png', dst1)

cv2.waitKey(0)