
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

count = 142

#권한 인증 및 토큰 확인
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None

#토큰이 있으면
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#토큰이 없거나 기한이 만료되면
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

#파이프를 통해 연결. 연결 인스턴스 생성
service = build('drive', 'v3', credentials=creds)

while True:
    s = input("쓰세요 : ")
    if s == 'a':
        #음악 업로드 실행
        print("=====  {}번째 음성이 업로드됩니다  =====".format(count))
        file_metadata = {'name': '2021-05-23_' + str(count) + '_voice.wav', # 매일매일 이름의 날짜와 폴더ID 바꿔야합니다
                        'parents': ['10-yvjsEQ8G28jfvs_6xqjJvZSZj30xwX']}  # 5월 21일 폴더ID : 1zvjIvmhnMri7KstpOEAiuBeZBS1o8WBK
                                                                                # 5월 22일 폴더ID : 1QTAwj4llfne_nYAUlISG_LwC1tZ8jfLW
                                                                                # 5월 23일 폴더ID : 10-yvjsEQ8G28jfvs_6xqjJvZSZj30xwX
                                                                                # 테스트 폴더 : 1BVg4nm0n2HjvckWxXEoOulgENtjMYpcE
        media = MediaFileUpload('voice/' + str(count) + '_voice.wav', resumable=True)  # 파일 위치
        file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()    #파일올리는 거예요

        #QR코드 만들기
        print("=====  {}번째 QR코드 생성중  =====".format(count))
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=20, border=0)
        qr.add_data("https://drive.google.com/file/d/" + file.get('id') + "/view?usp=sharing")
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("QRCode/" + str(count) + "_qrcode.png")


        #배경화면에 옷 이미지 넣기
        background = Image.open('0523_background.png')
        blur = Image.open('blur/' + str(count) + '_blur.png')
        blur = blur.resize((610, 528))
        background_size = background.size
        background = background.convert('RGBA')
        ticket = Image.new('RGBA', (background_size[0], background_size[1]), (255, 255, 255))
        ticket.paste(blur, (15, 462))
        ticket.paste(background, (0, 0), background)


        #몇 번째 손님인지
        draw = ImageDraw.Draw(ticket)
        font = ImageFont.truetype("../font/조선일보명조.ttf", 30)
        org = (300, 167)  # 글씨의 위치
        draw.text(org, "#%03d" % count, font=font, fill=(100, 100, 100))

        #음파 넣기
        wave = Image.open('waveform/' + str(count) + '_waveform.png', 'r')
        wave = wave.resize((510, 150))
        ticket.paste(wave, (65, 310), wave)

        #QR코드 넣기
        QR = Image.open('QRCode/' + str(count) + '_qrcode.png')
        QR = QR.resize((120, 120))
        ticket.paste(QR, (455, 75))

        #티켓 저장
        print("=====  {}번째 티켓이 저장되고 있습니다  =====".format(count))
        ticket.save('Ticket/' + str(count) + "_ticket.png")
        ticket.show()

        count += 1


    elif s == 'q':
        print("===== 종료합니다, 마지막 count : {}  =====".format(count-1))
        break
    else:
        pass