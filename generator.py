from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

datagen = ImageDataGenerator(
    rescale=1. / 255,  # RGB 계수를 1/255로 스케일링하여 0-1 범위로 변환
    # 정수. 무작위 회전의 각도 범위
    rotation_range=30,
    # 임의 전단 변환 (shearing transformation) 범위
    shear_range=5.5,
    # 그림을 수평 또는 수직으로 랜덤하게 평행 이동시키는 범위
    # (원본 가로, 세로 길이에 대한 비율 값)
    width_shift_range=0.1,
    height_shift_range=0.1,

    # 임의 확대 축소 범위
    zoom_range=0.,
    horizontal_flip=True,
    vertical_flip=False,
    fill_mode='nearest')

for data_num in range(500, 1000):
    src = "crop_image/dino/dino_" + str(data_num+1) + ".jpg"
    img = load_img(src)  # PIL 이미지
    x = img_to_array(img)  # (3, 150, 150) 크기의 NumPy 배열

    x = x.reshape((1,) + x.shape)  # (1, 3, 150, 150) 크기의 NumPy 배열

    # 아래 .flow() 함수는 임의 변환된 이미지를 배치 단위로 생성해서
    # 지정된 `preview/` 폴더에 저장
    i = 0
    for batch in datagen.flow(x, batch_size=1, save_to_dir='picture/gray_resize_picture', save_prefix='dino', save_format='jpg'):
        i += 1
        if i >= 20:
            print(data_num + 1, i)
            break  # 이미지 20장을 생성하고 마칩니다
