import coap_rpi_client as coap

client = coap.Client("parkingspot", "coap://192.168.1.117:5683")
client.update_status("0", "RESERVED")
client.close()

