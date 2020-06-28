from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold, cross_val_score
from train_model import iamai
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from keras import regularizers
import numpy as np


def create_model():
    # 모델 생성
    # 128, 128
    model = Sequential()
    model.add(Conv2D(32, (10, 10), padding='same', activation='relu', input_shape=(128, 128, 1)))  # ->128,128,32
    model.add(MaxPooling2D(2, 2))  # ->64,64,32
    model.add(Dropout(0.5))

    model.add(Conv2D(32, (10, 10), padding='same', activation='relu'))  # ->64,64,32
    model.add(MaxPooling2D(2, 2))  # ->32,32,32
    model.add(Dropout(0.5))

    model.add(Conv2D(32, (10, 10), padding='same', activation='relu'))  # ->32,32,32
    model.add(MaxPooling2D(2, 2))  # ->16,16,32
    model.add(Dropout(0.5))

    # 8192,1
    model.add(Flatten())

    # 2097152,1
    model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
    model.add(Dropout(0.5))

    # 768
    model.add(Dense(4, activation='softmax'))
    # model.add(Dense(2, activation='softmax'))

    model.summary()

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print("=" * 50)

    return model


# print(run.k_y_train_encoded.shape)
#

def vaildation():
    k_fold_model = KerasClassifier(build_fn=create_model, epochs=200, batch_size=256, verbose=0)
    print("k_fold_model", k_fold_model)

    k_fold = KFold(n_splits=5, shuffle=True)

    result = cross_val_score(estimator=k_fold_model, X=k_img_train, y=k_y_train_encoded, cv=k_fold)
    print(result)
    print("모델 평가 평균 점수 :", np.mean(result))


if __name__ == '__main__':
    run = iamai()
    run.k_fold_cv_data()

    k_img_train, k_y_train_encoded, img_train = run.k_fold_data_getter()
    print("type :", type(k_img_train))
    print("k_img_train.shape", k_img_train.shape)
    print("len(k_img_train) :", len(k_img_train))
    print("len(k_y_train_encoded) :", len(k_y_train_encoded))
    print("len(img_train) :", len(img_train))

    vaildation()
