from picamera import PiCamera
from time import sleep
from openalpr import Alpr
import json
from coap_rpi_client import Client

current_plate = ""
occupied = False

def scan():
	global alpr
	
	cam = PiCamera()
	cam.start_preview()
	sleep(2)

	picname = "license_plate.jpg"
	cam.capture(picname)
	cam.stop_preview()
	cam.close()

	result = ["0"]
	results = alpr.recognize_file("/home/pi/parking/" + picname)
	
	with open('lastscan.json', 'w+') as ls:
		ls.write(json.dumps(results, indent=4))
		ls.close()
	
	n_results = len(results.values()[4])
	
	if n_results > 0:
		print("Found {} licence plate(s)".format(n_results))
		result[0] = str(n_results)
		for i in range(n_results):
			lp = results.values()[4][i].values()[0]
			print(lp)
			result.append(lp)  

	else:
		print("No licence plate found")

	return result
	
alpr = Alpr("eu", "/etc/openalpr/openalp.conf", "/usr/share/openalpr/runtime_data")
	
if not alpr.is_loaded():
	print("Failed to load OpenALPR")

client = Client("parkingspot")
id = client.assign_id()
client.register("FREE")

while(True):	
	result = scan()
	
	if (result[0] == "0" and occupied == True):
		current_plate = ""
		occupied = False
		client.update_status(id,"FREE")
		print("Status : FREE")
		
	if (not result[0] == "0" and occupied == False):
		current_plate = result[1]
		occupied = True
		client.update_status(id,"BUSY")
		print("Status : BUSY")  

	sleep(5)
	
alpr.unload()	