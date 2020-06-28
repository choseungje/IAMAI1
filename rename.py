import os

# 주어진 디렉토리에 있는 항목들의 이름을 담고 있는 리스트를 반환합니다.
# 리스트는 임의의 순서대로 나열됩니다.
file_path = 'img_data2/category8/gray_dog_man'
# file_path = 'picture/gray_resize_picture'
file_names = os.listdir(file_path)
print(file_names)
# file_names.sort()
# print(file_names)

i = 1
for name in file_names:
    src = os.path.join(file_path, name)
    # 위 폴더안의 파일 이름만 바꿈, 새롭게 저장 X
    # 저장할 파일 이름
    dst = 'dogman_' + str(i) + '.jpg'
    # dst = str(i) + '.jpg'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    i += 1
