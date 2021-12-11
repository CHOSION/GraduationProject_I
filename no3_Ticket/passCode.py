from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

import qrcode
import keyboard
from PIL import Image, ImageDraw, ImageFont

# 1
count = 12
was_pressed = False


# 권한 인증 및 토큰 확인
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None

# 토큰 존재 시
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# 토큰 부재 or 기한 만료 시
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'Credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# 파이프를 통해 연결. 연결 인스턴스 생성
service = build('drive', 'v3', credentials=creds)

while True:
    if keyboard.is_pressed('s'):        # s 버튼을 막 누르면 안 됨! 다른 창이 띄워져있어도 s 버튼 인식함
        if not was_pressed:
            was_pressed = True

            # 음악 업로드 실행
            print("=====  No.{} 음성이 업로드됩니다  =====".format(count))
            file_metadata = {'name': '2021-05-22_' + str(count) + '_voice.wav', # 매일매일 이름의 날짜와 폴더ID 바꿔야 한다.
                             'parents': ['1QTAwj4llfne_nYAUlISG_LwC1tZ8jfLW']}  # 5월 21일 폴더ID : 1zvjIvmhnMri7KstpOEAiuBeZBS1o8WBK
                                                                                # 5월 22일 폴더ID : 1QTAwj4llfne_nYAUlISG_LwC1tZ8jfLW
                                                                                # 5월 23일 폴더ID : 10-yvjsEQ8G28jfvs_6xqjJvZSZj30xwX
            media = MediaFileUpload('voice/' + str(count) + '_voice.wav', resumable=True)  # 파일 위치
            file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()    # 파일 올리기

            # QR코드 생성
            print("=====  {}번째 QR코드 생성중  =====".format(count))
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=20, border=0)
            qr.add_data("https://drive.google.com/file/d/" + file.get('id') + "/view?usp=sharing")
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("QRCode/" + str(count) + "_qrcode.png")


            # 배경화면에 옷 이미지 넣기
            background = Image.open('background.jpg')
            blur = Image.open('blur/' + str(count) + '_blur.png')
            background_size = background.size
            background = background.convert('RGBA')
            ticket = Image.new('RGBA', (background_size[0], background_size[1]), (255, 255, 255))
            ticket.paste(background, (0, 0))
            ticket.paste(blur, (32, 32))

            # n번째 손님
            draw = ImageDraw.Draw(ticket)
            font = ImageFont.truetype("../font/함초롱바탕R.ttf", 24)
            org = (693, 295)  # 글씨의 위치
            draw.text(org, str(count) +"번째 손님", font=font, fill=(0, 0, 0), align = 'center')

            # 음파
            wave = Image.open('waveform/' + str(count) + '_waveform.png', 'r')
            wave = wave.resize((800, 300))
            ticket.paste(wave, (520, 290), wave)

            # QR코드
            QR = Image.open('QRCode/' + str(count) + '_qrcode.png')
            QR = QR.resize((100, 100))
            ticket.paste(QR, (888, 508))

            # 티켓 저장
            print("=====  {}번째 티켓이 저장되고 있습니다  =====".format(count))
            ticket.save('Ticket/' + str(count) + "_ticket.png")
            ticket.show()

            count += 1
    elif keyboard.is_pressed('esc'):
        break
    else:
        was_pressed = False