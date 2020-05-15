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
        # self.category = ['dog', 'cat', 'rabbit', 'fox', 'dino']
        self.category = ['fox', 'dino']

        # 카테고리당 데이터 개수
        self.data_num = 300
        # 전체 이미지 개수
        self.all_data_num = len(self.category) * self.data_num
        print("전체 이미지 개수(all_data_num) :", self.all_data_num)

        # 한 카테고리 당 테스트 데이터 개수
        # 300 * 0.2 = 60
        self.test_data_num = int(self.data_num * 0.2)

        # data_num - test_data_num = 240
        self.train_val_num = self.data_num - self.test_data_num

        # 한 카테고리 당 훈련 데이터 개수
        self.train_data_num = int(self.train_val_num * 0.8)
        print("한 카테고리당 훈련 데이터 개수(train_data_num) :", self.train_data_num)
        # 한 카테고리 당 검증 데이터 개수
        self.val_data_num = int(self.train_val_num * 0.2)
        print("한 카테고리당 검증 데이터 개수(val_data_num) :", self.val_data_num)

        print("한 카테고리당 test 데이터 개수(test_data_num) :", self.test_data_num)

        # 교차검증용 데이터
        self.k_img_train = []
        self.k_img_test = []
        self.k_y_train = []
        self.k_y_test = []
        self.k_y_train_encoded = []

        # 이미지를 리스트에 입력
        self.img_train = []
        self.img_val = []
        self.img_test = []

        # 타깃값 입력
        self.y_train = []
        self.y_val = []
        self.y_test = []

        # 원-핫 인코딩
        self.y_train_encoded = []
        self.y_val_encoded = []
        self.y_test_encoded = []

        # 모델 만들기
        self.model = tf.keras.Sequential()
        self.history = None

        print("초기화 완료")
        print()
        print("=" * 50)

    def k_fold_cv_data(self):
        # 교차 검증용 데이터 생성
        print("%d개의 카테고리" % len(self.category))
        # 카테고리 개수
        for category in range(len(self.category)):
            # 카테고리 내의 데이터 개수
            for data_num in range(self.data_num):
                src = "picture/gray_resize_picture/" + self.category[category] + "_" + str(data_num + 1) + ".jpg"
                # num < 192
                if data_num < self.train_val_num:
                    image = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                    self.k_img_train.append(image)
                else:
                    image = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                    self.k_img_test.append(image)

            print("교차 검증용 %s 사진 읽어옴" % self.category[category])
        print("교차 검증용 train data 개수 :", len(self.k_img_train))
        print("교차 검증용 test data 개수 :", len(self.k_img_test))

        print()

        # k_y_train
        y_num = -1
        # 카테고리 개수만큼 생성
        for category in range(len(self.category)):
            # 훈련 데이터 개수만큼 반복
            for num in range(self.train_val_num):
                # 한 카테고리당 데이터 개수
                # ex) num % 192 == 0
                if num % self.train_val_num == 0:
                    y_num += 1
                    self.k_y_train.append(int(y_num))
                else:
                    self.k_y_train.append(int(y_num))
        print("교차 검증용 훈련 데이터 y값 생성")
        # print(self.y_train)
        print("len(k_y_train) :", len(self.k_y_train))
        print()

        self.k_y_train_encoded = tf.keras.utils.to_categorical(self.k_y_train)

        self.k_img_train = np.array(self.k_img_train)
        self.k_img_train = self.k_img_train / 255
        self.k_img_train = np.reshape(self.k_img_train, (-1, 128, 128, 1))
        print("self.k_img_train.shape :", self.k_img_train.shape)
        print("self.k_y_train_encoded.shape :", self.k_y_train_encoded.shape)
        print("=" * 50)

    def load_img(self):
        print("%d개의 카테고리" % len(self.category))
        # 카테고리 개수
        for category in range(len(self.category)):
            # 카테고리 내의 데이터 개수
            for data_num in range(self.data_num):
                src = "picture/gray_resize_picture/" + self.category[category] + "_" + str(data_num + 1) + ".jpg"
                # num < 192
                if data_num < self.train_data_num:
                    image = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                    self.img_train.append(image)
                elif data_num < self.train_data_num + self.val_data_num:
                    image = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                    self.img_val.append(image)
                else:
                    image = cv2.imread(src, cv2.IMREAD_UNCHANGED)
                    self.img_test.append(image)

            print("%s 사진 읽어옴" % self.category[category])

        print()

        print("img_train 사진 개수 :", len(self.img_train))
        print("img_val 사진 개수 :", len(self.img_val))
        print("img_test 사진 개수 :", len(self.img_test))
        print("이미지 타입 :", type(self.img_train[0]))

        print("img_train 타입 :", type(self.img_train))
        print("=" * 50)

        return self.img_train, self.img_val, self.img_test

    def create_y(self):
        # y_train
        y_num = -1
        # 카테고리 개수만큼 생성
        for category in range(len(self.category)):
            # 훈련 데이터 개수만큼 반복
            for num in range(self.train_data_num):
                # 한 카테고리당 데이터 개수
                # ex) num % 192 == 0
                if num % self.train_data_num == 0:
                    y_num += 1
                    self.y_train.append(int(y_num))
                else:
                    self.y_train.append(int(y_num))
        print("훈련 데이터 y값 생성")
        # print(self.y_train)
        print("len(y_train) :", len(self.y_train))
        print()

        # y_val
        y_num = -1
        # 카테고리 개수만큼 생성
        for category in range(len(self.category)):
            # 검증 데이터 개수만큼 반복
            for num in range(self.val_data_num):
                # 한 카테고리당 데이터 개수
                # ex) num % 48 == 0
                if num % self.val_data_num == 0:
                    y_num += 1
                    self.y_val.append(int(y_num))
                else:
                    self.y_val.append(int(y_num))
        print("검증 데이터 y값 생성")
        print("len(y_val) :", len(self.y_val))
        print()

        # y_test
        y_num = -1
        # 카테고리 개수만큼 생성
        for category in range(len(self.category)):
            # test 데이터 개수만큼 반복
            for num in range(self.test_data_num):
                # 한 카테고리당 데이터 개수
                # ex) num % 60 == 0
                if num % self.test_data_num == 0:
                    y_num += 1
                    self.y_test.append(int(y_num))
                else:
                    self.y_test.append(int(y_num))
        print("test 데이터 y값 생성")
        print("len(y_test) :", len(self.y_test))
        print()

        print("=" * 50)

        return self.y_train, self.y_val, self.y_test

    # 데이터 전처리
    def data_pretreatment(self):
        # 원핫 인코딩 : y_train, y_val
        # np.array 변환 : img_train, img_val, img_test, y_train, y_val, y_test
        # 표준화, 채널 설정 : img_train, img_val, img_test
        #

        # 원-핫 인코딩 : 합성곱 신경망의 타깃으로 사용하려면 배열의 요소들을 원-핫 인코딩으로 변경해야 한다.
        self.y_train_encoded = tf.keras.utils.to_categorical(self.y_train)
        self.y_val_encoded = tf.keras.utils.to_categorical(self.y_val)
        self.y_test_encoded = tf.keras.utils.to_categorical(self.y_test)
        print("원-핫 인코딩 완료")
        # print(type(self.img_train))
        # print(type(self.img_train[1]))
        # print(self.img_train[1].shape)

        # np.array로 변환
        self.img_train = np.array(self.img_train)
        self.img_val = np.array(self.img_val)
        self.img_test = np.array(self.img_test)
        self.y_train = np.array(self.y_train)
        self.y_val = np.array(self.y_val)
        self.y_test = np.array(self.y_test)
        print("np.array 변환 성공")
        # print(type(self.y_val))

        # 입력 데이터 표준화, 채널 설정
        self.img_train = self.img_train / 255
        self.img_val = self.img_val / 255
        self.img_test = self.img_test / 255
        print("표준화 성공")

        self.img_train = self.img_train.reshape(-1, 128, 128, 1)
        self.img_val = self.img_val.reshape(-1, 128, 128, 1)
        self.img_test = self.img_test.reshape(-1, 128, 128, 1)
        print("채널 설정 성공")
        # print(self.img_train)

        print("훈련 데이터 : ")
        print(self.img_train.shape)
        print("검증 데이터 : ")
        print(self.img_val.shape)
        print("test 데이터 :")
        print(self.img_test.shape)
        print()
        print("타깃 훈련 데이터 : ")
        print(len(self.y_train))
        print("타깃 검증 데이터(원-핫 인코딩) : ")
        print(len(self.y_val_encoded))
        print("타깃 test 데이터 :")
        print(len(self.y_test))

        print("=" * 50)

        return self.img_train, self.img_val, self.y_train_encoded, self.y_val_encoded, self.img_test, self.y_test

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
        # self.model.add(Dense(5, activation='softmax'))
        self.model.add(Dense(2, activation='sigmoid'))

        self.model.summary()

        # 컴파일 : 모델을 기계가 이해할 수 있도록 컴파일 합니다. 오차 함수와 최적화 방법, 메트릭 함수를 선택할 수 있다.
        # adam 은 손실 함수의 값이 최적값에 가까워질수록 학습률을 낮춰 손실 함수의 값이 안정적으로 수렴될 수 있게 해준다.
        # self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        return self.model

    def training_model(self):
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
                                      batch_size=128)
        print("학습 종료")

        # 모델을 저장
        self.model.save(MODEL_DIR + "model.h5")
        print("저장 종료")

        # 가중치를 저장
        self.model.save_weights(MODEL_DIR + 'weights')
        print("가중치 저장 완료")

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

        return self.history
