import time
import numpy as np
import cv2


def rectify(std_img, targ_img, max_iter=10, is_debug=False):
    surf = cv2.xfeatures2d_SURF.create()

    # 计算keypoints和描述子
    kp1, des1 = surf.detectAndCompute(std_img, None)
    kp2, des2 = surf.detectAndCompute(targ_img, None)

    # 暴力匹配
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # 调优
    good = []
    for m, n in matches:
        if m.distance < 0.20 * n.distance:
            good.append(m)

    good_kp1, good_kp2, tmp = [], [], []
    for i in range(len(good)):
        tmp.append(cv2.DMatch(i, i, 0))
        good_kp1.append(kp1[good[i].queryIdx])
        good_kp2.append(kp2[good[i].trainIdx])

    pt1 = [kp.pt for kp in good_kp1]
    pt2 = [kp.pt for kp in good_kp2]

    M, mask = cv2.findHomography(np.float32(pt2), np.float32(pt1), cv2.RANSAC, 1.0)
    dst = cv2.warpPerspective(targ_img, M, (int(targ_img.shape[1]), int(targ_img.shape[0])))
    # cv2.imwrite("std_wrap.jpeg", dst)

    if is_debug:
        dbg = cv2.drawMatches(std_img, good_kp1, targ_img, good_kp2, tmp, None, flags=2)
        cv2.imshow("Debug" + str(time.time())[-3:-1], dbg)
        # cv2.imwrite("surf.jpeg", dbg)
    return dst