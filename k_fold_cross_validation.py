from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold, cross_val_score
from home_model import iamai
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
import numpy as np


def create_model():
    # 모델 생성
    # 128, 128
    model = Sequential()
    model.add(Conv2D(32, (5, 5), padding='same', activation='relu', input_shape=(128, 128, 1)))
    model.add(MaxPooling2D(2, 2))  # ->64,64

    model.add(Conv2D(32, (5, 5), padding='same', activation='relu'))
    model.add(MaxPooling2D(2, 2))  # ->32,32

    model.add(Conv2D(32, (5, 5), padding='same', activation='relu'))
    model.add(MaxPooling2D(2, 2))  # ->16, 16

    # 1,256
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(Dense(256, activation='relu'))
    # self.model.add(Dense(5, activation='softmax'))
    model.add(Dense(2, activation='sigmoid'))

    model.summary()

    # self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print("=" * 50)

    return model


run = iamai()
run.k_fold_cv_data()
print(run.k_y_train_encoded.shape)

k_fold_model = KerasClassifier(build_fn=create_model, epochs=20, batch_size=128, verbose=0)
print(k_fold_model)

k_fold = KFold(n_splits=10, shuffle=True)

result = cross_val_score(estimator=k_fold_model, X=run.k_img_train, y=run.k_y_train_encoded, cv=k_fold)
print(result)
print("모델 평가 평균 점수 :", np.mean(result))
