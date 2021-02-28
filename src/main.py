import numpy as np
import cv2
import my_transform


if __name__ == '__main__':
    std = cv2.imread('/Users/wzy/Pictures/opencv_test/std.bmp')
    test = cv2.imread('/Users/wzy/Pictures/opencv_test/test.bmp')

    # 统一尺寸
    std = cv2.resize(std, (int(test.shape[1]), int(test.shape[0])))

    # 标准图透视变换成待测图角度
    std_wrap = my_transform.rectify(test, std, is_debug=True)
    # cv2.imshow("std_wrap", std_wrap)

    # 调整后的标准图与待测图作差
    diff = cv2.absdiff(test, std_wrap)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("diff", diff)
    # cv2.imwrite("diff.jpeg", diff)

    # 阈值化
    diff_thr = cv2.threshold(diff, 50, 255, cv2.THRESH_TOZERO)[1]
    # cv2.imshow("After threshold", diff_thr)
    # cv2.imwrite("d_thr.jpeg", diff_thr)

    # 均值滤波
    diff_thr_blur = cv2.blur(diff_thr, (3, 3))
    # cv2.imshow("After threshold and blur", diff_thr_blur)
    # cv2.imwrite("dt_blur.jpeg", diff_thr_blur)

    # 闭运算后阈值化
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    diff_thr_mor = cv2.morphologyEx(diff_thr, cv2.MORPH_CLOSE, kernel)
    # diff_thr_mor = cv2.threshold(diff_thr_mor, 30, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("After threshold and morphology", diff_thr_mor)
    # cv2.imwrite("dtb_mor.jpeg", diff_thr_mor)

    # 标记
    dst = diff_thr_mor
    _, contours, hierarchy1 = cv2.findContours(dst, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    ex = test.copy()
    for c in contours:
        if len(c) < 9:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(ex, (x, y), (x + w, y + h), (255, 0, 255), 8)
    # cv2.imshow("Final", ex)
    cv2.imwrite("final.jpeg", ex)
    # cv2.waitKey(0)

    pass