import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os


class iamai:
    def __init__(self):
        # 카테고리 리스트
        self.category = ['fox', 'dino']

        # 카테고리당 데이터 개수
        self.data_num = 300
        # 전체 이미지 개수
        self.all_data_num = len(self.category) * self.data_num
        print("전체 이미지 개수(all_data_num) :", self.all_data_num)
        # 한 카테고리 당 훈련 데이터 개수
        self.train_data_num = int(self.data_num * 0.8)
        print("한 카테고리당 훈련 데이터 개수(train_data_num) :", self.train_data_num)
        # 한 카테고리 당 검증 데이터 개수
        self.val_data_num = int(self.data_num * 0.2)
        print("한 카테고리당 검증 데이터 개수(val_data_num) :", self.val_data_num)

        # 이미지를 리스트에 입력
        self.img_train = []
        self.img_val = []

        # 타깃값 입력
        self.y_train = []
        self.y_val = []

        # 원-핫 인코딩
        self.y_train_encoded = []
        self.y_val_encoded = []

        # 모델 만들기
        self.model = tf.keras.Sequential()
        self.history = None
        print("초기화")

    def load_img(self):
        print("%d개의 카테고리" % len(self.category))
        # 여우
        for data_num in range(300):
            fox_src = "picture/gray_resize_picture/fox_" + str(data_num + 1) + ".jpg"
            print(fox_src)
            if data_num < 240:
                image = cv2.imread(fox_src, cv2.IMREAD_UNCHANGED)
                self.img_train.append(image)
            else:
                image = cv2.imread(fox_src, cv2.IMREAD_UNCHANGED)
                self.img_val.append(image)
        print("여우 사진 읽어옴")

        # 공룡
        for data_num in range(300):
            dino_src = "picture/gray_resize_picture/dino_" + str(data_num + 1) + ".jpg"
            print(dino_src)
            if data_num < 240:
                image = cv2.imread(dino_src, cv2.IMREAD_UNCHANGED)
                self.img_train.append(image)
            else:
                image = cv2.imread(dino_src, cv2.IMREAD_UNCHANGED)
                self.img_val.append(image)
        print("공룡 사진 읽어옴")

        print(len(self.img_train))
        print(len(self.img_val))

        self.img_train = np.array(self.img_train)
        # print(self.img_train)
        print(self.img_train.shape)

    def create_y(self):
        y_num = -1
        # 카테고리 개수만큼 생성
        for category in range(len(self.category)):
            # 훈련 데이터 y값
            # 훈련 데이터 개수만큼 반복
            for num in range(self.train_data_num):
                if num % 240 == 0:
                    y_num += 1
                    self.y_train.append(str(y_num))
                else:
                    self.y_train.append(str(y_num))
        print("훈련 데이터 y값 생성")
        print("len(y_train) :", len(self.y_train))

        y_num = -1
        # 카테고리 개수만큼 생성
        for category in range(len(self.category)):
            # 검증 데이터 y값
            for num in range(self.val_data_num):
                if num % 60 == 0:
                    y_num += 1
                    self.y_val.append(str(y_num))
                else:
                    self.y_val.append(str(y_num))
        print("검증 데이터 y값 생성")
        print("len(y_val) :", len(self.y_val))

        return self.y_train, self.y_val

    # 데이터 전처리
    def data_pretreatment(self):
        # 원-핫 인코딩 : 합성곱 신경망의 타깃으로 사용하려면 배열의 요소들을 원-핫 인코딩으로 변경해야 한다.
        self.y_train_encoded = tf.keras.utils.to_categorical(self.y_train)
        self.y_val_encoded = tf.keras.utils.to_categorical(self.y_val)
        print("원-핫 인코딩 완료")
        # print(type(self.img_train))
        # print(type(self.img_train[1]))
        # print(self.img_train[1].shape)

        # np.array로 변환
        self.img_train = np.array(self.img_train)
        self.img_val = np.array(self.img_val)
        self.y_train = np.array(self.y_train)
        self.y_val = np.array(self.y_val)
        print("np.array 변환 성공")
        # print(type(self.y_val))

        print(self.img_train.shape)
        print(self.img_val.shape)
        print(self.y_train.shape)
        print(self.y_val.shape)

        # 입력 데이터 표준화, 채널 설정
        self.img_train = self.img_train / 255
        self.img_val = self.img_val / 255
        print("표준화 성공")

        self.img_train = self.img_train.reshape(-1, 128, 128, 1)
        self.img_val = self.img_val.reshape(-1, 128, 128, 1)
        print("채널 설정 성공")
        # print(self.img_train)

        print("훈련 데이터 : ")
        print(self.img_train.shape)
        print("검증 데이터 : ")
        print(self.img_val.shape)
        print("타깃 훈련 데이터 : ")
        print(len(self.y_train))
        print("타깃 검증 데이터 : ")
        print(len(self.y_val))
        print("타깃 검증 데이터(원-핫 인코딩 : ")
        print(len(self.y_val_encoded))

        return self.img_train, self.img_val, self.y_train, self.y_val, self.y_train_encoded, self.y_val_encoded

    def create_model(self):
        # 모델 생성
        # 128, 128
        self.model.add(Conv2D(32, (5, 5), padding='same', activation='relu', input_shape=(128, 128, 1)))
        self.model.add(MaxPooling2D(2, 2))  # ->64,64

        self.model.add(Conv2D(32, (5, 5), padding='same', activation='relu'))
        self.model.add(MaxPooling2D(2, 2))  # ->32,32

        self.model.add(Conv2D(32, (5, 5), padding='same', activation='relu'))
        self.model.add(MaxPooling2D(2, 2))  # ->16, 16

        # 1,256
        self.model.add(Flatten())
        # 하나의 레이어가 이전 레이어로부터 같은 입력을 두번 이상 받지 못하도록 한다.
        self.model.add(Dropout(0.3))
        # print("create Classifier")
        self.model.add(Dense(256, activation='relu'))
        self.model.add(Dense(2, activation='sigmoid'))

        self.model.summary()

        # 컴파일 : 모델을 기계가 이해할 수 있도록 컴파일 합니다. 오차 함수와 최적화 방법, 메트릭 함수를 선택할 수 있다.
        # adam 은 손실 함수의 값이 최적값에 가까워질수록 학습률을 낮춰 손실 함수의 값이 안정적으로 수렴될 수 있게 해준다.
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # 모델을 저장
        MODEL_DIR = './model/'  # 모델 저장하는 폴더
        if not os.path.exists(MODEL_DIR):  # 위 폴더가 존재하지 않으면
            os.mkdir(MODEL_DIR)  # 폴더를 만든다

        model_path = './model/{epoch:02d}-{val_loss:.4f}.hdf5'

        check_pointer = ModelCheckpoint(filepath=model_path, monitor='val_loss', verbose=1, save_best_only=True)
        print("체크포인터 생성")

        early_stopping_callback = EarlyStopping(monitor='val_loss', patience=3)

        self.history = self.model.fit(self.img_train, self.y_train_encoded, epochs=50,
                                      validation_data=(self.img_val, self.y_val_encoded),
                                      callbacks=[check_pointer, early_stopping_callback],
                                      batch_size=256)
        print("학습 종료")

        # 모델을 저장
        self.model.save(MODEL_DIR + "model.h5")
        print("저장 종료")

        # # 가중치를 저장
        # self.model.save_weights('weights')
        # print("가중치 저장 완료")

        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend(['train_loss', 'val_loss'])
        plt.show()

        plt.plot(self.history.history['accuracy'])
        plt.plot(self.history.history['val_accuracy'])
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.legend(['train_accuracy', 'val_accuracy'])
        plt.show()

        return self.model, self.history
