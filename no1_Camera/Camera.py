import numpy as np
import cv2
from sklearn.cluster import KMeans
from PIL import ImageFont, ImageDraw, Image, ImageFilter

# CAMERA SETTING
capture = cv2.VideoCapture(2)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 2160)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 4096)