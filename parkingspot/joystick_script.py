from sense_hat import SenseHat
from time import sleep
import coap_rpi_client as coap

client = None
status = None
spot_id = None


def init():
    global client
    global spot_id
    global status
    client = coap.Client("parkingspot")
    spot_id = client.assign_id()
    status = "FREE"
    client.register("FREE")
    print("Registered with ID " + spot_id + " and status " + status)
    sense = SenseHat()
    sense.clear((0,0,0))
    return sense


def set_light():
    global status
    if status == "FREE":
        sense.clear((0, 255, 0))
    elif status == "BUSY":
        sense.clear((255, 0, 0))
    elif status == "RESERVED":
        sense.clear((255, 140, 0))
    else:
        print("Unknown status: " + status)


def set_status(param_status):
    global status
    status = param_status
    client.update_status(spot_id, status)


def set_free():
    set_status("FREE")


def set_busy():
    set_status("BUSY")


def reserve():
    print("Action not supported")


# Tell the program which function to associate with which direction
sense = init()

sense.stick.direction_up = set_free
sense.stick.direction_down = set_busy
sense.stick.direction_left = reserve
sense.stick.direction_right = reserve


def callback(response):
    global status
    print("--- CALLBACK ---")
    if response is not None and response.payload is not None:
        if len(response.payload) > 0 and response.payload != "NOT ALLOWED":
            status = response.payload
            set_light()


# observe status
client.observe(callback)

while True:
    sleep(0.1)
