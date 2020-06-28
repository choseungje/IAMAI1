import cv2
import os

# 주어진 디렉토리에 있는 항목들의 이름을 담고 있는 리스트를 반환합니다.
# 리스트는 임의의 순서대로 나열됩니다.
file_path = 'data/confirm_man/g_dogcat'
# file_path = 'reset_data/crop/gender/aaa'
file_names = os.listdir(file_path)
print(file_names)

i = 1
for name in file_names:
    src = os.path.join(file_path, name)
    # 위 폴더안의 파일 이름만 바꿈, 새롭게 저장 X
    # 저장할 파일 이름
    dst = 'dogcat_' + str(i) + '.jpg'
    # dst = str(i) + '.jpg'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    i += 1


# 그레이스케일, 이미지 사이즈 변환
# 폴더 경로
file_path = 'data/confirm_man/g_dogcat'
# file_path = 'picture/gray_resize_picture'
# file_path = 'gray_s'
file_names = os.listdir(file_path)
file_num = len(file_names)

for num in range(file_num):
    # filePath 는 폴더이름/1.jpg 형식
    filePath = file_path + '/dogcat_' + str(num + 1) + '.jpg'
    # filePath = file_path + '/' + str(num + 1) + '.jpg'
    print(filePath)
    path = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)
    # path = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)
    print(path)
    resize = cv2.resize(path, dsize=(128, 128), interpolation=cv2.INTER_AREA)
    cv2.imwrite("data/confirm_man/gray_dogcat/dogcat_" + str(num+1) + ".jpg", resize)
    # cv2.imwrite("gray_s/dino_" + str(num + 1) + ".jpg", resize)
    print("%d번 사진 resize" % (num+1))

