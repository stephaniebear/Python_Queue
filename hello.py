#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PIL import Image, ImageFont, ImageOps, ImageDraw
from datetime import datetime
from escpos.printer import Usb
import sys
import os


"""
import cups
conn = cups.Connection ()
printers = conn.getPrinters()
printer_name = printers.keys()[0]
for printer in printers:
    print printer, printers[printer]["device-uri"]

fileName = "/home/pi/Desktop/hello.txt"
conn.printFile(printer_name, fileName, " ", {})
"""

reload(sys)  # Reload is a hack
sys.setdefaultencoding('UTF-8')

def getDay(day):
	switcher = {
		"01": "1",
		"02": "2",
		"03": "3",
		"04": "4",
		"05": "5",
		"06": "6",
		"07": "7",
		"08": "8",
		"09": "9"
	}
	return switcher.get(day, day) #str(now.strftime("%d"))

def getMonth(month):
    switcher = {
        "01": u"\u0E21.\u0E04.",
        "02": u"\u0E01.\u0E1E.",
        "03": u"\u0E21\u0E35.\u0E04.",
        "04": u"\u0E40\u0E21.\u0E22.",
        "05": u"\u0E1E.\u0E04.",
        "06": u"\u0E21\u0E34.\u0E22.",
        "07": u"\u0E01.\u0E04.",
	"08": u"\u0E2A.\u0E04.",
	"09": u"\u0E01.\u0E22.",
	"10": u"\u0E15.\u0E04.",
	"11": u"\u0E1E.\u0E22.",
	"12": u"\u0E18.\u0E04."
    }
    return switcher.get(month, "get month Error")

def calWidth(imgWidth, text, fontSize):
	font = ImageFont.truetype('THSarabunNew.ttf', fontSize)
	fontSize = font.getsize(text)
	return ((imgWidth - fontSize[0]) / 2)


def calPosX(imgWidth, text, fontSize):
	font = ImageFont.truetype('THSarabunNew.ttf', fontSize)
	fontSize = font.getsize(text)
	return ((imgWidth - fontSize[0]) / 2)

def objFont(fontSize):
        return ImageFont.truetype('THSarabunNew.ttf', fontSize)

content = []

#---------- Read Config ----------
path = os.path.dirname(os.path.realpath(__file__))
print('Now path : ' + path)
fileState = 0
for file in os.listdir(path):
    if file.endswith(".txt"):
        print('File : ' + str(os.path.join(file)))
        if str(os.path.join(file)) == 'config.txt':
                fileState = 1

if fileState == 1:
	print('found config.txt')
	f = open('config.txt', 'r')
	for row in f:
		tempContent = row.replace('\n', ' ')
		content.append(tempContent.decode('unicode-escape'))
		#tempContent.decode('unicode-escape')
		#print('Content in file : ' + tempContent.decode('unicode-escape'))
	f.close()
else:
	print('Create file config.txt')
	f = open('config.txt', 'w')
	f.write('\u0e2a\u0e33\u0e19\u0e31\u0e01\u0e07\u0e32\u0e19\u0e17\u0e35\u0e48\u0e14\u0e34\u0e19\n')
	f.write('\u0e2a\u0e32\u0e02\u0e32\n')
	f.write('\u0e2a\u0e48\u0e27\u0e19\u0e41\u0e22\u0e01')
	f.close()

print('array : ' ,len(content))
H = 10
for row in content:
	font = ImageFont.truetype('THSarabunNew.ttf', 40)
	print(row)
	tempH = font.getsize(row)
	print('H : ', H)
	H = H + tempH[1] + 10
	print(font.getsize(row))
	
#---------------------------------

queue = '1'

text = u"\u0E2A\u0E33\u0E19\u0E31\u0E01\u0E07\u0E32\u0E19\u0E17\u0E35\u0E48\u0E14\u0E34\u0E19\u0E08\u0E31\u0E07\u0E2B\u0E27\u0E31\u0E14\u0E02\u0E2D\u0E19\u0E41\u0E01\u0E48\u0E19\n"
text1 = "____________________"
text3 = u"\u0E04\u0E34\u0E27\u0E2A\u0E33\u0E2B\u0E23\u0E31\u0E1A\u0E23\u0E2D\u0E15\u0E23\u0E27\u0E08\u0E2A\u0E2D\u0E1A\u0E40\u0E2D\u0E01\u0E2A\u0E32\u0E23"
now = datetime.now()
text4 = u"\u0E27\u0E31\u0E19\u0E17\u0E35\u0E48 " + getDay(str(now.strftime("%d"))) + ' ' + getMonth(str(now.strftime("%m"))) + ' '
text4 += str(int(now.strftime("%Y"))+543) + ' '
text4 += u"  \u0E40\u0E27\u0E25\u0E32 : " + str(now.strftime("%H:%M:%S"))
text5 = u"\u0E15\u0E34\u0E14\u0E15\u0E48\u0E2D\u0E2A\u0E2D\u0E1A\u0E16\u0E32\u0E21\u0E42\u0E17\u0E23 : 043-236528"

"""
for i in range(1,13):
	if i <= 9 :
		print(getMonth('0'+str(i)))
	else:
		print(getMonth(str(i)))
"""

print(text)
print(text1)
print(queue)
print(text3)
print(text4)
print(text5)

"""
font = ImageFont.truetype('THSarabunNew.ttf', 40)
sizeText5 = font.getsize(text5)
print('size',sizeText5)
width = (sizeText5[0]/2) - (len(text5)/2)
print(width)
"""
imgHeigh = 10

for row in content:
	getHeigh = font.getsize(row)
	imgHeigh += getHeigh[1]
	print('Pos Y ', imgHeigh)

imgHeigh += 160 # Size QR Code
imgHeigh += 315 # Number of axis Y

print('Result : ', imgHeigh )

#image = Image.new('RGB', (box[0], 15 * box[1]), color = (255, 255, 255))
#---------- Initial img size ----------
imgWidth = 390 #600
#imgHeigh = 600 #450
#--------------------------------------
image = Image.new('RGB', (imgWidth , imgHeigh), color = (255, 255, 255))

#logo = Image.open('logo.jpg')
#logo2 = logo.copy()
#image.paste(logo, (10, 10))

draw = ImageDraw.Draw(image)
#draw.text((0, 0), text, font=font)

posY = 10

for row in content:
	font = objFont(45)
	posX = calPosX(imgWidth, row, 45)
	draw.text((posX , posY ), row, font=font, fill=(0, 0, 0))
	getHeigh = font.getsize(row)
	posY = posY + getHeigh[1]

font = objFont(50)
posX = calPosX(imgWidth, text1, 50)
posY -= 20
draw.text((posX , posY), text1, font=font, fill=(0, 0, 0)) #+20

font = objFont(120)
posX = calPosX(imgWidth, queue, 120)
posY += 40
draw.text((posX ,posY), queue, font=font, fill=(0, 0, 0)) #+50

font = objFont(40)
posX = calPosX(imgWidth, text3, 40)
posY += 130
draw.text((posX , posY), text3, font=font, fill=(0, 0, 0)) #+150

font = objFont(50)
posX = calPosX(imgWidth, text1, 50)
posY -= 10
draw.text((posX , posY), text1, font=font, fill=(0, 0, 0)) #------

font = objFont(40)
posX = calPosX(imgWidth, text5, 40)
posY += 50
draw.text((posX , posY), text5, font=font, fill=(0, 0, 0))

posX = calPosX(imgWidth, text4, 40)
posY += 35
draw.text((posX , posY), text4, font=font, fill=(0, 0, 0))

QR = Image.open('qrcode.png') #Load QR Code
QR = QR.resize((160, 160)) #Resize Width = 160, Heigh = 160
posX = ((imgWidth - 160) / 2)
posY += 50
image.paste(QR, (posX, posY))

print('Pos Y : ', posY)

#image = ImageOps.invert(image)   # invert image to black on white

"""
for i in range(QR.size[0]): # for every pixel:
	for j in range(QR.size[1]):
		QR.putpixel((i, j), (0, 0, 0)) #Set color black
		r,g,b = QR.getpixel( (i,j) ) #Get color from picture
		print("Red: {0}, Green: {1}, Blue: {2}".format(r,g,b))

#QR.putpixel((0, 0), (0, 0, 0)) #Set color black
#r,g,b = QR.getpixel( (0,0) ) #Get color from picture
#print("Red: {0}, Green: {1}, Blue: {2}".format(r,g,b))
"""

image.save('queue.png')

p = Usb(0x0483, 0x070b, 0, 0x81, 0x02)
p.set("CENTER", "A", "", 1, 1)
p.image(image)
#p.image("name.png")
p.cut()
