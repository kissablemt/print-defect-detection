import random
import numpy as np
import cv2
import imutils
import my_transform

def matchAB(imgA, imgB, n):
    # 转换成灰色
    grayA = imgA
    grayB = imgB
    grayA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    # 获取图片A的大小
    height, width = grayA.shape

    # 取局部图像，寻找匹配位置
    result_window = np.zeros((height, width), dtype=imgA.dtype)
    for start_y in range(0, height - 100, 10):
        for start_x in range(0, width - 100, 10):
            window = grayA[start_y:start_y + 100, start_x:start_x + 100]
            match = cv2.matchTemplate(grayB, window, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(match)
            matched_window = grayB[max_loc[1]:max_loc[1] + 100, max_loc[0]:max_loc[0] + 100]
            result = cv2.absdiff(window, matched_window)
            result_window[start_y:start_y + 100, start_x:start_x + 100] = result

    result = result_window.copy()
    # result = cv2.GaussianBlur(result, (5, 5), 0)

    cv2.normalize(result, result, 0, 1, norm_type=cv2.NORM_MINMAX)
    # cv2.normalize(result, result, 0, 1, norm_type=cv2.NORM_INF)
    result = 255 * result

    # result = cv2.GaussianBlur(result, (5, 5), 0)
    # result = cv2.boxFilter(result, -1, (5, 5))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
    result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)

    cv2.normalize(result, result, 0, 255, norm_type=cv2.NORM_MINMAX)


    cv2.imshow("result_window"+n, result)

    # # 用四边形圈出不同部分
    # _, result_window_bin = cv2.threshold(result_window, 30, 255, cv2.THRESH_BINARY)
    # _, contours, _ = cv2.findContours(result_window_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # imgC = imgA.copy()
    # for contour in contours:
    #     min = np.nanmin(contour, 0)
    #     max = np.nanmax(contour, 0)
    #     loc1 = (min[0][0], min[0][1])
    #     loc2 = (max[0][0], max[0][1])
    #     cv2.rectangle(imgC, loc1, loc2, 255, 2)
    #
    # cv2.imshow("A", cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB))
    # cv2.imshow("B", cv2.cvtColor(imgB, cv2.COLOR_BGR2RGB))
    # cv2.imshow("Answer", cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB))
    # cv2.waitKey(0)

random.seed(0)

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

# 滤波
blur1 = cv2.GaussianBlur(img1, (5, 5), 0)
blur2 = cv2.GaussianBlur(img2, (5, 5), 0)

dst = my_transform.transform(gray1, gray2, max_iter=10, is_debug=False)
# gray3 = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
gray3 = dst.copy()

norm1 = cv2.normalize(gray1, None, 0, 255, cv2.NORM_MINMAX)
norm3 = cv2.normalize(gray3, None, 0, 255, cv2.NORM_MINMAX)

bin1 = cv2.threshold(gray1, 178, 255, cv2.THRESH_BINARY)[1]
bin3 = cv2.threshold(gray3, 178, 255, cv2.THRESH_BINARY)[1]

diff1 = dst - gray1
# cv2.imshow("Direct Diff", diff1)

diff2 = norm3 - norm1
result = cv2.blur(diff2, (3, 3))
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# result = cv2.morphologyEx(diff2, cv2.MORPH_CLOSE, kernel)
# result = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
cv2.imshow("Norm Diff", result)

diff3 = bin3 - bin1
# cv2.imshow("Binary Diff", diff3)

diff4 = gray3 - gray1
# cv2.imshow("Gray Diff", diff4)

# matchAB(img1, dst, "1")

# 锐化
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
eh = cv2.filter2D(dst, -1, kernel=kernel)


# matchAB(img1, dst, "1")

# dst = my_transform.transform(img1, dst, is_debug=True)
# matchAB(img1, dst2, "2")

# show
# cv2.imshow("img1", gray1)
# cv2.imshow("img2", gray2)
# cv2.imshow("dst", dst)
# cv2.imshow("add", add)
# cv2.imshow("eh", eh)
# cv2.imshow("diff", diff)



cv2.waitKey(0)

