import cv2
import matplotlib.pyplot as plt
import os

src = '../인물별_여우상'
file_list = os.listdir(src)
print(len(file_list))
print(file_list[0])

image = cv2.imread('number2.jpg')
# 그레이스케일 변환
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = face_cascade.detectMultiScale(grayImage, 1.03, 5)

print(faces.shape)
print("Number of faces detected: " + str(faces.shape[0]))
print(faces)

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 1)
    print(x, y, w, h)
    # cropped = image[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
    cropped = image[y+1: y + h-1, x+1: x + w-1]
    cv2.imwrite("crop" + str(1) + ".png", cropped)

cv2.rectangle(image, (0, image.shape[0] - 25),
              (270, image.shape[0]), (255, 255, 255), -1)
cv2.putText(image, "PinkWink test", (0, image.shape[0] - 10),
            cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1)

plt.figure(figsize=(12, 12))
plt.imshow(image, cmap='gray')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

cv2.imshow('image view', cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
