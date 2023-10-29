import cv2
import requests
import numpy as np

image_url = "https://firebasestorage.googleapis.com/v0/b/module5-img.appspot.com/o/files%2Favatar4.jpg?alt=media&token=a5892f05-8c1b-4271-b0c3-aa5c2f681137"

# Sử dụng thư viện requests để tải ảnh từ URL
response = requests.get(image_url)
img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

# Tạo Cascade Classifier cho việc phát hiện mắt
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# Chuyển ảnh thành ảnh xám (nếu cần)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Phát hiện mắt trên ảnh
eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

if len(eyes) > 0:
    print("Người này có đeo kính.")
else:
    print("Người này không đeo kính.")

for (x, y, w, h) in eyes:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('Detected Glasses', image)
cv2.waitKey(0)
cv2.destroyAllWindows()