import random
import numpy as np
import cv2
import imutils
import my_transform

img1 = cv2.imread('/Users/wzy/Pictures/opencv_test/std.jpeg')
img2 = cv2.imread('/Users/wzy/Pictures/opencv_test/test.jpeg')

# stitcher = cv2.createStitcher(False)
# result = stitcher.stitch((img1, img2))
# cv2.imshow("stitch_image", result[1])

img1 = cv2.resize(img1, (int(img2.shape[1]), int(img2.shape[0])))

# 压缩
img1 = imutils.resize(img1, width=800)
img2 = imutils.resize(img2, width=800)

# 灰度处理
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 归一化
cv2.normalize(gray1, gray1, 0, 255, cv2.NORM_MINMAX)
cv2.normalize(gray2, gray2, 0, 255, cv2.NORM_MINMAX)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
result = cv2.morphologyEx(gray2, cv2.MORPH_CLOSE, kernel)
result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
result = result-gray2
cv2.normalize(result, result, 0, 255, cv2.NORM_MINMAX)
# result = cv2.threshold(result, 200, 255, cv2.THRESH_BINARY_INV)[1]
# cv2.normalize(result-gray2, result, 0, 255, cv2.NORM_MINMAX)


cv2.imshow("Mor", result)
cv2.waitKey(0)