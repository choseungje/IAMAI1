import cv2
import matplotlib.pyplot as plt
import os
import numpy as np

folder_num = 15
picture_num = 20


def path(folder_num, picture_num):
    src = '../폴더'
    # src 경로의 파일안에 있는 모든 파일들을 리스트로 받아옴
    file_list = os.listdir(src)

    # ex) src + /경리
    plus_src = '/' + file_list[folder_num]

    full_src = src + plus_src
    # full_src 경로의 파일안에 있는 모든 파일들을 리스트로 받아옴
    inner_list = os.listdir(full_src)

    filePath = full_src + '/' + inner_list[picture_num]
    print(filePath)

    return filePath


def hangulFilePathImageRead(filePath):
    stream = open(filePath.encode("utf-8"), "rb")
    bytes = bytearray(stream.read())
    numpyArray = np.asarray(bytes, dtype=np.uint8)
    cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)
    return cv2.imdecode(numpyArray, cv2.IMREAD_UNCHANGED)


def cv(folder_num, picture_num):
    num = 0
    for f in range(folder_num):
        for p in range(picture_num):
            num += 1
            # 파일 경로 가져옴
            print("f, p :", f+1, p+1)
            filePath = path(f, p)
            # 이미지 imread
            image = hangulFilePathImageRead(filePath)
            # 그레이스케일 변환
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(grayImage, 1.03, 5)

            # print(faces.shape)
            print("Number of faces detected: " + str(faces.shape[0]))
            print(faces)
            # 얼굴로 인식되는 부분이 2개 이상일 경우 사각형을 비교해 큰 사각형을 얼굴로 인식하도록 함
            if len(faces) > 1:
                if faces[0][2] >= faces[1][2]:
                    faces = faces[[0]]
                else:
                    faces = faces[[1]]
            print(faces)

            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
                print(x, y, w, h)

                cropped = image[y + 1: y + h - 1, x + 1: x + w - 1]
                resize = cv2.resize(cropped, dsize=(128, 128), interpolation=cv2.INTER_LINEAR)
                cv2.imwrite("./crop/" + str(num) + ".jpg", resize)

            # # show---------------------------------------------------------
            # plt.figure(figsize=(12, 12))
            # plt.imshow(image, cmap='gray')
            # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
            # plt.show()
            #
            # cv2.imshow('image view', cropped)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            print("crop %d_%d" % (f+1, p+1))
            print("*" * 50)


# run
cv(folder_num, picture_num)
