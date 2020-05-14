from home_model import iamai
from tensorflow.keras.models import load_model

evaluating = iamai()
evaluating.load_img()
evaluating.create_y()
evaluating.data_pretreatment()

get_model = load_model('model/model.h5')
get_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

loss, accuracy = get_model.evaluate(evaluating.img_test, evaluating.y_test_encoded, verbose=0)
print(loss)
print(accuracy)

predict = get_model.predict_classes(evaluating.img_test)
print(predict)