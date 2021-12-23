import numpy as np
import cv2
from sklearn.cluster import KMeans
from PIL import ImageFont, ImageDraw, Image, ImageFilter

# 색상 비율을 보여주는 함수
def centroid_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()
    return hist

#색상바 생성하는 함수
def plot_colors(hist, centroids):
    b_width = 610
    b_height = 528
    bar = np.zeros((b_height, b_width, 3), dtype="uint8")
    startY = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endY = startY + (percent * b_height)
        cv2.rectangle(bar, (0, int(startY)), (b_width, int(endY)),
                      color.astype("uint8").tolist(), -1)
        startY = endY
    # return the bar chart
    return bar

#블러처리 함수
def blur():
    image1 = Image.open("../no3_Ticket/colorBar/" + str(count) + '_colorBar.png')     #바 사진 불러옴

    # BoxBlur 사용
    blurI = image1.filter(ImageFilter.GaussianBlur(40))
    blurI.save("../no3_Ticket/blur/" + str(count) + '_blur.png')    #블러된 사진 저장

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

    # cv2.rectangle(frame, (720-220, 960-280), (720+220, 960+280), (0, 255, 0), 3)
    cv2.line(frame, (500-150, 680), (500-150, 680 + 70), (0, 255, 0), 3)
    cv2.line(frame, (500-150, 680), (500-150 + 100, 680), (0, 255, 0), 3)

    cv2.line(frame, (500-150, 1240), (500-150, 1240 - 70), (0, 255, 0), 3)
    cv2.line(frame, (500-150, 1240), (500-150 + 100, 1240), (0, 255, 0), 3)

    cv2.line(frame, (940-150, 680), (940-150, 680 + 70), (0, 255, 0), 3)
    cv2.line(frame, (940-150, 680), (940-150 - 100, 680), (0, 255, 0), 3)

    cv2.line(frame, (940-150, 1240), (940-150, 1240 - 70), (0, 255, 0), 3)
    cv2.line(frame, (940-150, 1240), (940-150 - 100, 1240), (0, 255, 0), 3)


    cv2.imshow('WINDOW_NAME', frame)

    if key == ord('a'):
        # 'a' 클릭 후 3초 후 촬영됨
        cv2.waitKey(30)

        img = frame
        dst = img[960 - 280 + 3: 960 + 280 - 3, 720 - 220 -150+ 3: 720 + 220-150 - 3].copy()
        # 잘린 사진 저장할 곳 (/no3_Ticket/image)
        cv2.imwrite("../no3_Ticket/image/" + str(count) + ".png", dst)

        image = dst.reshape((dst.shape[0] * dst.shape[1], 3))
        k = 3
        iterations = 4
        iteration = 300

        clt = KMeans(n_clusters=k, n_jobs=iterations, max_iter=iteration)
        clt.fit(image)

        hist = centroid_histogram(clt)
        bar = plot_colors(hist, clt.cluster_centers_)

        cv2.imwrite("../no3_Ticket/colorBar/" + str(count) + "_colorBar.png", bar)        #바 사진 저장할 곳
        blur()

        count += 1

    elif key == ord('q') or key == 27:  # 'q' 이거나 'esc' 이면 종료
        break

capture.release()
cv2.destroyAllWindows()
