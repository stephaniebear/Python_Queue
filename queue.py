import RPi.GPIO as GPIO
import time
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
#GPIO.setup(17,GPIO.IN)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#--------- Printslip ----------
#def printSlip(queue):
	
#------------------------------

#--------- Datetime ----------
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
 
print("now = " , now)

# dd/mm/YY H:M:S
#date = now.strftime("%d/%m/%Y %H:%M:%S")
date = now.strftime("%Y%m%d")

print("date and time = " + date)
#-----------------------------

btnState = 0
queue = 0
backupdate = date

#---------- Read files ----------
path = os.path.dirname(os.path.realpath(__file__))
print('Now path : ' + path)
fileState = 0
for file in os.listdir(path):
    if file.endswith(".txt"):
        print('File : ' + str(os.path.join(file)))
	if str(os.path.join(file)) == 'date.txt':
		fileState = 1

if fileState == 1:
	print('Found date.txt')
	f = open('date.txt', 'r')
	
	temp = f.read().split(',') # Split date and Queue
	oldDate = temp[0]
	oldQueue = temp[1]

	print('File is already')
	print('Date : ' + oldDate + ', Queue : ' + oldQueue)
	if int(oldDate) < int(date): # if date in file < now date = create file
		print('Intens date and Clear queue')
		f = open('date.txt', 'w')
		f.write(date + ',' + '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
		
		print('Create logs file')
		f = open(str(now.strftime("%Y%m%d")) + '.txt', 'w')
		f.write( '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
	else:
		print('Load queue')
		queue = int(oldQueue)
	f.close()
else:
	print('Cant\'n found date.txt')
	print('Create ' + date + ' > date.txt ')
	f = open('date.txt', 'w')
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

		f = open('date.txt', 'r')
		temp = f.read().split(',') # Split date and Queue
		
		oldDate = temp[0]
		oldQueue = temp[1]
		
		# Check old date and clear
		if int(oldDate) < int(date):
			print('Intens date and Clear queue')
			f = open('date.txt', 'w')
			f.write(date + ',' + '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))
			
			print('Create logs file')
			f = open(str(now.strftime("%Y%m%d")) + '.txt', 'w')
			f.write( '0' + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))

		else:
			print('Queue saved')
			f = open('date.txt', 'w')
			f.write(date + ',' + str(queue) + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))

			f = open(str(now.strftime("%Y%m%d")) + '.txt', 'a')
			f.write( '\n' + str(queue) + ',' + str(now.strftime("%Y/%m/%d %H:%M:%S")))

		f.close()
		
		print('Active')
		
        #GPIO.output(27,1)
        #time.sleep(0.5)
        #GPIO.output(27,0)
        time.sleep(0.5)