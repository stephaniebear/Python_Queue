#!/usr/bin/python
# -*- coding: UTF-8 -*-

import RPi.GPIO as GPIO
import time
from PIL import Image, ImageFont, ImageOps, ImageDraw
from escpos.printer import Usb
import sys
import os

#--------- Datetime ----------
from datetime import datetime
#-----------------------------

fontName = 'configs/THSarabunNew.ttf'

def printQueue(queue):
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
        font = ImageFont.truetype(fontName, fontSize)
        fontSize = font.getsize(text)
        return ((imgWidth - fontSize[0]) / 2)


    def calPosX(imgWidth, text, fontSize):
        font = ImageFont.truetype(fontName, fontSize)
        fontSize = font.getsize(text)
        return ((imgWidth - fontSize[0]) / 2)

    def objFont(fontSize):
            return ImageFont.truetype(fontName, fontSize)

    content = []
    #---------- Read Config ----------
    path = os.path.dirname(os.path.realpath(__file__))
    path += '/configs'
    print('Now path : ' + path)
    fileState = 0
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print('File : ' + str(os.path.join(file)))
            if str(os.path.join(file)) == 'config.txt':
                    fileState = 1

    if fileState == 1:
        print('found config.txt')
        f = open('configs/config.txt', 'r')
        for row in f:
            tempContent = row.replace('\n', '')
            tempContent = tempContent.replace('\r', '')
            content.append(tempContent.decode('unicode-escape'))
            #tempContent.decode('unicode-escape')
            #print('Content in file : ' + tempContent.decode('unicode-escape'))
        f.close()
    else:
        print('Create file config.txt')
        f = open('configs/config.txt', 'w')
        f.write('\u0e2a\u0e33\u0e19\u0e31\u0e01\u0e07\u0e32\u0e19\u0e17\u0e35\u0e48\u0e14\u0e34\u0e19\n')
        f.write('\u0e2a\u0e32\u0e02\u0e32\n')
        f.write('\u0e2a\u0e48\u0e27\u0e19\u0e41\u0e22\u0e01')
        f.close()

    print('array : ' ,len(content))
    H = 10
    for row in content:
        font = ImageFont.truetype(fontName, 40)
        print(row)
        tempH = font.getsize(row)
        print('H : ', H)
        H = H + tempH[1] + 10
        print(font.getsize(row))



    #---------------------------------

    #---------- Read Telephone number ----------
    telephone_number = ''
    path = os.path.dirname(os.path.realpath(__file__))
    path += '/configs'
    print('Telephone Number path : ' + path)
    fileState = 0
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print('File : ' + str(os.path.join(file)))
            if str(os.path.join(file)) == 'tel.txt':
                f = open('configs/tel.txt', 'r')
                for row in f:
                    telephone_number = row.replace('\n', ' ')
                f.close()
            else:
                telephone_number = ''

    #-------------------------------------------

    text = u"\u0E2A\u0E33\u0E19\u0E31\u0E01\u0E07\u0E32\u0E19\u0E17\u0E35\u0E48\u0E14\u0E34\u0E19\u0E08\u0E31\u0E07\u0E2B\u0E27\u0E31\u0E14\u0E02\u0E2D\u0E19\u0E41\u0E01\u0E48\u0E19\n"
    text1 = "____________________"
    text3 = u"\u0E04\u0E34\u0E27\u0E2A\u0E33\u0E2B\u0E23\u0E31\u0E1A\u0E23\u0E2D\u0E15\u0E23\u0E27\u0E08\u0E2A\u0E2D\u0E1A\u0E40\u0E2D\u0E01\u0E2A\u0E32\u0E23"
    #text4 = u"\u0E27\u0E31\u0E19\u0E17\u0E35\u0E48 " + getDay(str(now.strftime("%d"))) + ' ' + getMonth(str(now.strftime("%m"))) + ' '
    #text4 += str(int(now.strftime("%Y"))+543) + ' '
    #text4 += u"  \u0E40\u0E27\u0E25\u0E32 : " + str(now.strftime("%H:%M:%S"))
    text5 = u"\u0E15\u0E34\u0E14\u0E15\u0E48\u0E2D\u0E2A\u0E2D\u0E1A\u0E16\u0E32\u0E21\u0E42\u0E17\u0E23 : " + telephone_number

    now = datetime.now()
    timestamp = u"\u0E27\u0E31\u0E19\u0E17\u0E35\u0E48 " + getDay(str(now.strftime("%d"))) + ' ' + getMonth(str(now.strftime("%m"))) + ' '
    timestamp += str(int(now.strftime("%Y"))+543) + ' '
    timestamp += u" \u0E40\u0E27\u0E25\u0E32 : " + str(now.strftime("%H:%M:%S"))
    
    print(text)
    print(text1)
    print(queue)
    print(text3)
    #print(text4)
    print(timestamp)
    print(text5)

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

    draw = ImageDraw.Draw(image)

    posY = 10

    for row in content:
        font = objFont(35)
        posX = calPosX(imgWidth, row, 35)
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

    font = objFont(35)
    posX = calPosX(imgWidth, text5, 40)
    posY += 50
    draw.text((posX , posY), text5, font=font, fill=(0, 0, 0))

    posX = calPosX(imgWidth, timestamp, 40)
    posY += 35
    draw.text((posX , posY), timestamp, font=font, fill=(0, 0, 0))

    QR = Image.open('configs/qrcode.png') #Load QR Code
    QR = QR.resize((160, 160)) #Resize Width = 160, Heigh = 160
    posX = ((imgWidth - 160) / 2)
    posY += 50
    image.paste(QR, (posX, posY))

    print('Pos Y : ', posY)

    #image = ImageOps.invert(image)   # invert image to black on white

    image.save('static/images/queue.png')

    try:
        p = Usb(0x0483, 0x070b, 0, 0x81, 0x02)
        p.set("CENTER", "A", "", 1, 1)
        p.image(image)
        #p.image("name.png")
        p.cut()
    except:
        print('Please turn on printer')
#------------------------

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
#GPIO.setup(17,GPIO.IN)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#--------- Printslip ----------
#def printSlip(queue):
    
#------------------------------


# datetime object containing current date and time
now = datetime.now()
print("Date now : " , now)

# dd/mm/YY H:M:S
#date = now.strftime("%d/%m/%Y %H:%M:%S")
date = now.strftime("%Y%m%d")
print("Date : " + date)
#-----------------------------

btnState = 0
queue = 0
backupdate = date

#---------- Read files ----------
path = os.path.dirname(os.path.realpath(__file__))
path += '/logs'
print('Now path : ' + path)
fileState = 0
for file in os.listdir(path):
    if file.endswith(".txt"):
        print('This files : ' + str(os.path.join(file)))
    if str(os.path.join(file)) in 'date.txt':
        fileState = 1

if fileState == 1:
    print('Found date.txt')
    f = open('logs/date.txt', 'r')
    
    temp = f.read().split(',') # Split date and Queue
    oldDate = temp[0]
    oldQueue = temp[1]

    print('Found date.txt')
    print('Date : ' + oldDate + ', Queue : ' + oldQueue)
    if int(oldDate) < int(date): # if date in file < now date = create file
        print('Intens date and Clear queue')
        f = open('logs/date.txt', 'w')
        f.write(date + ',' + '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
        
        print('Create logs file')
        f = open(str(now.strftime("%Y%m%d")) + '.txt', 'w')
        f.write( '1' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
    else:
        print('Load queue')
        queue = int(oldQueue)
    f.close()
else:
    print('Cant\'n found date.txt')
    print('Create ' + date + ' > date.txt ')
    f = open('logs/date.txt', 'w')
    f.write(date + ',' + '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
    
    print('Create logs file')
    f = open(str(now.strftime("%Y%m%d")) + '.txt', 'w')
    f.write( '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))

    f.close()
#--------------------------------

if backupdate != date:
    print('Clear Queue!!')
    queue = 0
    backupdate = datetime
    

while True:
    now = datetime.now()
    
    print('PID : ', os.getpid())
    print('Datetime : ' , str(now.strftime("%Y/%m/%d %H:%M:%S")))
    print('Queue : ' + str(queue))
    if GPIO.input(17) == 1:
        GPIO.output(27,1)
    else:
        GPIO.output(27,0)
    
    #Button
    if GPIO.input(17) == 1 and btnState == 0 :
        btnState = 1
        print('Waiting for active')
    elif GPIO.input(17) == 0 and btnState == 1:
        btnState = 0
        queue = queue + 1

        f = open('logs/date.txt', 'r')
        temp = f.read().split(',') # Split date and Queue
        
        oldDate = temp[0]
        oldQueue = temp[1]

        printQueue(str(queue))
        
        # Check old date and clear
        if int(oldDate) < int(date):
            print('Intens date and Clear queue')
            f = open('logs/date.txt', 'w')
            f.write(date + ',' + '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
            
            print('Create logs file')
            logsfile = 'logs/' + str(now.strftime("%Y%m%d")) + '.txt'
            f = open(logsfile , 'w')
            f.write( '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))

        else:
            print('Queue saved')
            f = open('logs/date.txt', 'w')
            f.write(date + ',' + str(queue) + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
            
            logsfile = 'logs/' + str(now.strftime("%Y%m%d")) + '.txt'
            f = open(logsfile, 'a')
            f.write( '\n' + str(queue) + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))

        f.close()
        
        print('Active Printer')
        
        #GPIO.output(27,1)
        #time.sleep(0.5)
        #GPIO.output(27,0)
        #time.sleep(0.5)

