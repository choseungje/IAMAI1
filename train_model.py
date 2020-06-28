import os
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


seed = 0
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)


class iamai:
    def __init__(self):
        # 카테고리 리스트
        self.category = ['dogman', 'dogwoman', 'catman', 'catwoman',
                         'dinoman', 'dinowoman', 'foxman', 'foxwoman']

        self.category_num = len(self.category)

        # img 데이터 가져오는 폴더 url
        self.url = "img_data2/category8/"

        # l2규제
        self.l2 = 0.01

        # 에포크
        self.epochs = 5000

        # 카테고리당 데이터 개수
        self.data_num = 1200
        # 전체 이미지 개수
        self.all_data_num = len(self.category) * self.data_num
        print("전체 이미지 개수(all_data_num) :", self.all_data_num)

        # 한 카테고리 당 테스트 데이터 개수
        # 1000 * 0.1 = 100
        self.test_data_num = int(self.data_num * 0.1)

        # data_num - test_data_num = 900
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
                src = self.url + self.category[category] + "_" + str(data_num + 1) + ".jpg"
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

        # 데이터 셔플
        s_train = list(zip(self.k_img_train, self.k_y_train))
        random.shuffle(s_train)
        self.k_img_train, self.k_y_train = zip(*s_train)
        print("shuffle")
        print(self.k_y_train)
        print()

        # 데이터 전처리
        self.k_y_train_encoded = tf.keras.utils.to_categorical(self.k_y_train)

        self.k_img_train = np.array(self.k_img_train)
        self.k_img_train = self.k_img_train / 255
        self.k_img_train = np.reshape(self.k_img_train, (-1, 128, 128, 1))
        print("self.k_img_train.shape :", self.k_img_train.shape)
        print("self.k_y_train_encoded.shape :", self.k_y_train_encoded.shape)
        print("=" * 50)

        return self.k_img_test, self.k_img_train, self.k_y_test, self.k_y_train, self.k_y_train_encoded

    # 이미지 load
    def load_img(self):
        print("%d개의 카테고리" % len(self.category))
        # 카테고리 개수
        for category in range(len(self.category)):
            print("src = ", self.url + self.category[category])
            # 카테고리 내의 데이터 개수
            for data_num in range(self.data_num):
                src = self.url + self.category[category] + "_" + str(data_num + 1) + ".jpg"
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

    # img 데이터 셔플
    def img_shuffle(self):
        s_train = list(zip(self.img_train, self.y_train))
        s_val = list(zip(self.img_val, self.y_val))
        s_test = list(zip(self.img_test, self.y_test))

        random.shuffle(s_train)
        random.shuffle(s_val)
        random.shuffle(s_test)

        # print(s_val)

        self.img_train, self.y_train = zip(*s_train)
        self.img_val, self.y_val = zip(*s_val)
        self.img_test, self.y_test = zip(*s_test)

        print("shuffle")
        print("=" * 50)

        return self.img_train, self.img_val, self.img_test, self.y_train, self.y_val, self.y_test

    # 데이터 전처리
    def data_pretreatment(self):
        # 원핫 인코딩 : y_train, y_val
        # np.array 변환 : img_train, img_val, img_test, y_train, y_val, y_test
        # 표준화, 채널 설정 : img_train, img_val, img_test

        self.y_train_encoded = tf.keras.utils.to_categorical(self.y_train)
        self.y_val_encoded = tf.keras.utils.to_categorical(self.y_val)
        self.y_test_encoded = tf.keras.utils.to_categorical(self.y_test)
        print("원-핫 인코딩 완료")

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

        print("훈련 데이터 :", self.img_train.shape)
        print("검증 데이터 :", self.img_val.shape)
        print("test 데이터 :", self.img_test.shape)
        print()
        print("y_train_encoded shape :", self.y_train_encoded.shape)
        print("len(self.y_train) :", len(self.y_train))
        print("len(self.y_val_encoded) :", len(self.y_val_encoded))
        print("len(self.y_test) :", len(self.y_test))

        print("=" * 50)

        return self.img_train, self.img_val, self.y_train_encoded, self.y_val_encoded, self.img_test, self.y_test

    def create_model(self):
        # 모델 생성
        # 128, 128
        self.model.add(Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(128, 128, 1)))  # ->128,128,32
        self.model.add(MaxPooling2D(2, 2))  # ->64,64,32
        self.model.add(Dropout(0.5))

        self.model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))  # ->64,64,64
        self.model.add(MaxPooling2D(2, 2))  # ->32,32,64
        self.model.add(Dropout(0.5))

        self.model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))  # ->32,32,128
        self.model.add(MaxPooling2D(2, 2))  # ->16,16,128
        self.model.add(Dropout(0.5))

        self.model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))  # ->16,16,256
        self.model.add(MaxPooling2D(2, 2))  # ->8,8,256
        self.model.add(Dropout(0.5))

        self.model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))  # ->8,8,512
        self.model.add(MaxPooling2D(2, 2))  # ->4,4,512
        self.model.add(Dropout(0.5))

        # 8192,1
        self.model.add(Flatten())

        self.model.add(Dense(1024, activation='relu', kernel_regularizer=regularizers.l2(self.l2)))
        self.model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(self.l2)))
        self.model.add(Dense(self.category_num, activation='softmax'))

        self.model.summary()

        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        return self.model

    def training_model(self):
        # 모델을 저장
        MODEL_DIR = './model/'  # 모델 저장하는 폴더
        if not os.path.exists(MODEL_DIR):  # 위 폴더가 존재하지 않으면
            os.mkdir(MODEL_DIR)  # 폴더를 만든다

        model_path = './model/{epoch:02d}-{val_loss:.4f}.hdf5'

        check_pointer = ModelCheckpoint(filepath=model_path, monitor='val_loss', verbose=1, save_best_only=True)
        print("체크포인터 생성")

        # early_stopping_callback = EarlyStopping(monitor='val_loss', patience=5)

        self.history = self.model.fit(self.img_train, self.y_train_encoded, epochs=self.epochs,
                                      validation_data=(self.img_val, self.y_val_encoded),
                                      callbacks=[check_pointer],
                                      batch_size=256)
        # 고정된 test set 을 가지고 모델의 성능을 확인하고, 파라미터를 수정하고, 이 과정을 반복하면
        # 결국 test set 에만 잘 동작하는 모델이 되며, test set 에 과적합된다.

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
        plt.ylim(0, 3)
        plt.legend(['train_loss', 'val_loss'])
        plt.show()

        plt.plot(self.history.history['accuracy'])
        plt.plot(self.history.history['val_accuracy'])
        plt.xlabel('epoch')
        plt.ylabel('accuracy')
        plt.legend(['train_accuracy', 'val_accuracy'])
        plt.show()

        return self.history

    def k_fold_data_getter(self):
        return self.k_img_train, self.k_y_train_encoded, self.img_train


if __name__ == '__main__':

    run = iamai()
    run.load_img()
    run.create_y()
    run.img_shuffle()
    run.data_pretreatment()
    run.create_model()
    run.training_model()
