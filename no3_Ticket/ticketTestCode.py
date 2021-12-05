from PIL import Image, ImageDraw, ImageFont

count = 1
background = Image.open('0521_background.png')
#blur = Image.open('blur/' + str(count) + '_blur.png')
blur = Image.open('../rose_blur_4.png')
blur = blur.resize((610, 528))
background_size = background.size
background = background.convert('RGBA')
ticket = Image.new('RGBA', (background_size[0], background_size[1]), (255, 255, 255))
ticket.paste(blur, (15, 462))
ticket.paste(background, (0, 0), background)


# n번째 손님
draw = ImageDraw.Draw(ticket)
font = ImageFont.truetype("../font/조선일보명조.ttf", 30)
org = (300, 167)  # 글씨의 위치
draw.text(org, "#%03d" %count, font=font, fill=(100, 100, 100))

# soundwave
wave = Image.open('waveform/' + str(count) + '_waveform.png', 'r')
wave = wave.resize((510, 150))
ticket.paste(wave, (65, 310), wave)

# QR code
QR = Image.open('QRCode/' + str(count) + '_qrcode.png')
QR = QR.resize((120, 120))
ticket.paste(QR, (455, 75))

# save ticket
print("=====  {}번째 티켓이 저장되고 있습니다  =====".format(count))
ticket.save('Ticket/' + str(count) + "_ticket.png")
ticket.show()

# count += 1