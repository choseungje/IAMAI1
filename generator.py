from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import numpy as np
import os

img_dir = os.listdir("./data/confirm_man/dog")
# img_dir = os.listdir("../s")
datagen = ImageDataGenerator(
    rescale=1. / 255,  # RGB 계수를 1/255로 스케일링하여 0-1 범위로 변환
    # 정수. 무작위 회전의 각도 범위
    rotation_range=15,
    # # 임의 전단 변환 (shearing transformation) 범위
    # shear_range=5.5,
    # 그림을 수평 또는 수직으로 랜덤하게 평행 이동시키는 범위
    # (원본 가로, 세로 길이에 대한 비율 값)
    width_shift_range=0.1,
    height_shift_range=0.1,

    # 임의 확대 축소 범위
    zoom_range=0.,
    horizontal_flip=True,
    vertical_flip=False,
    fill_mode='nearest')


for idx, dir_img in enumerate(img_dir):
    src = "./data/confirm_man/dog/" + dir_img
    # src = "../s/" + dir_img
    img = load_img(src)
    x = img_to_array(img)
    print(idx, dir_img)

    x = x.reshape((1,) + x.shape)
    gen = datagen.flow(x, batch_size=1, save_to_dir='./data/confirm_man/g_dogcat', save_prefix='dogcat1_' + str(idx),
                       save_format='jpg')

    for i in range(10):
        gen.__next__()
