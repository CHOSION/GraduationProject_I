import numpy as np
import cv2
from sklearn.cluster import KMeans
from PIL import ImageFont, ImageDraw, Image, ImageFilter

# 카메라 세팅
capture = cv2.VideoCapture(2)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 2160)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 4096)

# 이 부분을 주석처리하면 윈도우처럼 뜬다.
cv2.namedWindow('WINDOW_NAME', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('WINDOW_NAME', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 카운트 변수(중요함)
count = 122

while True:
    ret, frame = capture.read()
    key = cv2.waitKey(30)
    frame = cv2.flip(frame, 1)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # 텍스트
    img = frame
    img = Image.fromarray(img)

    # width / 2 = 1080
    # height / 2 = 2048
    draw = ImageDraw.Draw(img)
    font_s = ImageFont.truetype("../font/Daum_Regular.ttf", 50)
    font_b = ImageFont.truetype("../font/Daum_Regular.ttf", 72)
