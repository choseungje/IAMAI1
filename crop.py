import cv2
import glob

face_cascade = cv2.CascadeClassifier('C:\\Users\\조승제\\Desktop\\git\\IAMAI1\\haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 경로
path = glob.glob("picture/a/Han_Hyojoo/*.jpg")
imglist = []

for imgname in path:
    i = cv2.imread(imgname)
    imglist.append(i)
    print(i)

imgnum = 1
for img in imglist:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("gray", gray)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cropped = img[y:y + h, x:x + w]
        # 저장경로
        cv2.imwrite("picture/a/crop/Han_Hyojoo_" + str(imgnum) + ".jpg", cropped)

    imgnum += 1


