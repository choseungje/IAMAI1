from train_model import iamai
from tensorflow.keras.models import load_model
import cv2
import numpy as np

evaluating = iamai()
evaluating.load_img()
evaluating.create_y()
evaluating.data_pretreatment()

get_model = load_model('model/latest_model/4901-0.8052.hdf5')

get_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# test셋으로 모델 평가
loss, accuracy = get_model.evaluate(evaluating.img_test, evaluating.y_test_encoded, verbose=0)
print(loss)
print(accuracy)

# # 모델 사용
# predict = get_model.predict_classes(evaluating.img_test)
# score = 0
#
# for i, p in enumerate(predict):
#     print(i + 1, p)

# for predict, yhat in zip(predict, evaluating.y_test):
#     if predict == yhat:
#         score += 1
#
# score = score / len(evaluating.y_test)
#
# print(score)

# 모델 사용
src = "maru.jpg"
image = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
img_list = [image]
img_list = np.array(img_list)
img_list = img_list / 255
img_list = np.reshape(img_list, (-1, 128, 128, 1))

predict = get_model.predict(img_list)
print(predict)
