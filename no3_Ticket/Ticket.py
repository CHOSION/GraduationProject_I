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

#토큰 존재 시
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#토큰 부재 or 기한 만료 시
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

#파이프를 통해 연결, 연결 인스턴스 생성
service = build('drive', 'v3', credentials=creds)