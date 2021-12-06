from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
import qrcode
import numpy as np

import cv2
count = 1

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
'''
#드라이브에 폴더 생성
file_metadata = {
    'name': 'Invoices',                                   #폴더 이름
    'mimeType': 'application/vnd.google-apps.folder'      #폴더 위치
}
file = service.files().create(body=file_metadata, fields='id').execute()   #폴더 실행문
print( 'Folder ID: %s' % file.get('id'))          #폴더 아이디, 폴더 고유 번호 -> 파일을 넣으려면 폴더 아이디가 필요함.

while True:
    if key == ord('a'):
    #폴더에 파일 업로드
        file_metadata = {'name': str(count) + '_voice.wav', 'parents': ['1zvjIvmhnMri7KstpOEAiuBeZBS1o8WBK']}   #어떤 파일을 업로드할지?
        media = MediaFileUpload(str(count) + '_voice.wav', resumable = True)   #파일 위치
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        print('File ID: %s' % file.get('id'))  #파일의 아이디가 공유 링크의 뒷부분이다

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=20, border= 2)
        qr.add_data("https://drive.google.com/file/d/" + file.get('id') + "/view?usp=sharing")
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(count + "qrcode.png")
'''