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