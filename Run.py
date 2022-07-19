import cv2
import numpy as np
import playsound
import smtplib
import ssl
import socket


Fire_Reported = 0
Alarm_Status = False


def play_audio():
	playsound.playsound('alarm sound.mp3',True)

def send_email_function():

	recipientEmail = "Fire_Engine_Email_Address"
	recipientEmail = recipientEmail.lower()

	try:
		port = 587  # For starttls
		smtp_server = "smtp.gmail.com"
		sender_email = "musiccontentsystem@gmail.com"
		receiver_email = "teju101999@gmail.com"
		password = "bcvvncwcnhnckpuk"
		message = """\
Subject: Fire Detection
Warning A Fire Accident has been reported on ABC company"""
		
		context = ssl.create_default_context()
		with smtplib.SMTP(smtp_server, port) as server:
			server.ehlo()
			server.starttls(context=context)
			server.ehlo()
			server.login(sender_email, password)
			server.sendmail(sender_email, receiver_email, message)
	except Exception as e:
		print(e)


video = cv2.VideoCapture("Fire07.mov")

while True:

	ret, frame = video.read()
	frame = cv2.resize(frame, (1000,600))
	blur = cv2.GaussianBlur(frame, (15,15),0)
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	lower = [18,50,50]
	upper = [35,255,255]

	lower = np.array(lower,dtype='uint8')
	upper = np.array(upper,dtype='uint8')

	mask = cv2.inRange(hsv,lower,upper)

	output = cv2.bitwise_and(frame,hsv,mask=mask)

	size = cv2.countNonZero(mask)

	if int(size) > 15000:
		Fire_Reported = Fire_Reported +1

		if Fire_Reported >= 1:
			if Alarm_Status == False:
				send_email_function()
				play_audio()
				Alarm_Status = True

			
			
				
		

    
	if ret == False:
		break

	cv2.imshow('Output', hsv)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
video.release()
