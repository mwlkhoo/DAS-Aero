# TODO: Add file IO to write to file and reference relative to current filepath

import re
import sys
import webbrowser
import os

from pymavlink import mavutil

openHTML = "<!DOCTYPE html>\n<html>\n<head>\n<style>p { font-size:180px; margin: 0; padding:0; }</style>\n</head>\n<body>\n"
closeHTML = "</body>\n</html>\n"

currentPath = os.path.dirname(os.path.abspath(__file__))
fileName = "results.html"
resultsUrl = currentPath + "\\" + fileName

feetPerMetre = 3.28084

def servo():
	try:
		servoData = the_connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True)
		return servoData
	except:
		print("Error getting servo data")
		return "error"

# VFR_HUD contains altitude param
def VFR():
	try:
		vfrData = the_connection.recv_match(type='VFR_HUD', blocking=True)
		return vfrData
	except: 
		print("Error getting VFR HUD data")
		return "error"

def rawRC():
	try: 
		rawRCData = the_connection.recv_match(type='RC_CHANNELS_RAW', blocking=True)
		return rawRCData
	except: 
		print("Error getting raw RC data")
		return "error"

def RC():
	try:
		RCData = the_connection.recv_match(type='RC_CHANNELS', blocking=True)
		return RCData
	except:
		print("Error getting RC data")
		return "error"

def updateResults(body):
	with open(resultsUrl, 'w') as file:
		file.write(openHTML + body + closeHTML)
		file.close()

# the_connection = mavutil.mavlink_connection('udpin:localhost:14550')
the_connection = mavutil.mavlink_connection('tcp:localhost:14550')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
# print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_system))
print("\nMavlink connection successful")
print("\nRELEASED:\n", flush=True)

global body
body = ""
# global resultStrings
# resultStrings = [None, None, None]

global servoData
global VFRData

global CDAAlt
global waterAlt
global habitatAlt

# Record which info was recorded first
global CDAOrder
global waterOrder
global habitatOrder

# global order
# order = 0


# CDA = CDA1 = CDA2
CDAAlt = None
waterAlt = None
habitatAlt = None

defaultTrigger = 1600

CDATrigger = defaultTrigger
waterTrigger = defaultTrigger
habitatTrigger = defaultTrigger

# IMPORTANT TODO: Double check
	 # servo number is correct
	 # double check servo trigger and < vs. > is correct

try: 
	while(CDAAlt == None or waterAlt == None or habitatAlt == None):
		servoData = servo()
		VFRData = VFR()

		# TODO: add while loop for error
		altData = VFRData.alt

		if(CDAAlt == None):
			CDAServo = servoData.servo5_raw
			if(CDAServo > CDATrigger):
				CDAAltMetres = altData
				CDAAlt = '%.3f'%(CDAAltMetres * feetPerMetre)
				# CDAOrder = order
				CDAString = "<p>CDA1:" + str(CDAAlt) + "ft</p>\n<p>CDA2:" + str(CDAAlt) + "ft</p>\n"
				body = CDAString + body
				# resultStrings[CDAOrder] = CDAString
				# order += 1

				print("CDA1 altitude:", CDAAlt, "ft\nCDA2 altitude:", CDAAlt, "ft", flush=True)
				updateResults(body)
				webbrowser.open(resultsUrl)



		if(waterAlt == None):
			waterServo = servoData.servo8_raw
			if(waterServo > waterTrigger):
				waterAltMetres = altData
				waterAlt = '%.3f'%(waterAltMetres * feetPerMetre)
				# waterOrder = order
				waterString = "<p>Water:" + str(waterAlt) + "ft</p>\n"
				body = waterString + body
				# resultStrings[waterOrder] = waterString
				# order += 1

				print("Water altitude:", waterAlt, "ft", flush=True)
				updateResults(body)
				webbrowser.open(resultsUrl)



		if(habitatAlt == None):
			habitatServo = servoData.servo7_raw
			if(habitatServo > habitatTrigger):
				habitatAltMetres = altData
				habitatAlt = '%.3f'%(habitatAltMetres * feetPerMetre)
				# habitatOrder = order
				habitatString = "<p>Habitat:" + str(habitatAlt) + "ft</p>\n"
				body = habitatString + body
				# resultStrings[habitatOrder] = habitatString
				# order += 1

				print("Habitat altitude:", habitatAlt, "ft", flush=True)
				updateResults(body)
				webbrowser.open(resultsUrl)


except KeyboardInterrupt:
	exit()

# Example commands:
# print(servoData)
# print(servoData.servo3_raw)
# print(servo().servo1_raw)