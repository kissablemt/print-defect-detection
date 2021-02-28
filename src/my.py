import random
import numpy as np
import cv2
import imutils

random.seed(0)

img1 = cv2.imread('/Users/wzy/Pictures/opencv_test/std.jpeg')
img2 = cv2.imread('/Users/wzy/Pictures/opencv_test/test.jpeg')

# 压缩
img1 = imutils.resize(img1, width=1800)
img2 = imutils.resize(img2, width=1800)

# 灰度处理
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

surf = cv2.xfeatures2d_SURF.create()

# 计算keypoints和描述子
kp1, des1 = surf.detectAndCompute(img1, None)
kp2, des2 = surf.detectAndCompute(img2, None)

# 暴力匹配
bf = cv2.BFMatcher()
matches = bf.match(des1, des2)

# 调优
matches.sort(key=lambda x: x.distance)
matches = random.sample(matches[:50], 4)

good = []
good_kp1 = []
good_kp2 = []

for i in range(len(matches)):
    good.append(cv2.DMatch(i, i, 0))
    good_kp1.append(kp1[matches[i].queryIdx])
    good_kp2.append(kp2[matches[i].trainIdx])

pt1 = [kp.pt for kp in good_kp1]
pt2 = [kp.pt for kp in good_kp2]

M = cv2.getPerspectiveTransform(np.float32(pt2), np.float32(pt1))
dst = cv2.warpPerspective(img2, M, (img2.shape[1], img2.shape[0]))


# 匹配图
# img3 = cv2.drawMatches(img1, good_kp1, img2, good_kp2, good, None, flags=2)

# img1和img2新keypoints图
# img4 = cv2.drawKeypoints(img1, good_kp1, None)
# img5 = cv2.drawKeypoints(img2, good_kp2, None)

# show
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)
# cv2.imshow("Matches", img3)
# cv2.imshow("img1 good key", img4)
# cv2.imshow("img2 good key", img5)
cv2.imshow("dst", dst)

cv2.waitKey(0)

