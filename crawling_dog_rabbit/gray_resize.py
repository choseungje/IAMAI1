import cv2
import os

for num in range(1000):
    # filePath 는 폴더이름/1.jpg 형식
    filePath = "rabbit/rabbit_" + str(num + 1) + '.jpg'
    print(filePath)

    path = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
    print(path)
    resize = cv2.resize(path, dsize=(128, 128), interpolation=cv2.INTER_AREA)
    cv2.imwrite("../picture/gray_resize_picture/rabbit_" + str(num+1) + ".jpg", resize)
    print("%d번 사진 resize" % (num+1))
