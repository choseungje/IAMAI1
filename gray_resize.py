import cv2
import os

# 폴더 경로
file_path = 'data/confirm_man/aa'
file_names = os.listdir(file_path)
file_num = len(file_names)

for num in range(file_num):
    # filePath 는 폴더이름/1.jpg 형식
    filePath = file_path + '/cat_' + str(num + 1) + '.jpg'
    print(filePath)
    path = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
    # path = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)
    print(path)
    resize = cv2.resize(path, dsize=(128, 128), interpolation=cv2.INTER_AREA)
    cv2.imwrite("data/confirm_man/gray_aa/cat_" + str(num+1) + ".jpg", resize)
    print("%d번 사진 resize" % (num+1))
