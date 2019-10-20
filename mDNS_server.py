# mDNS Server
import subprocess
import threading

def publishService():
    p = subprocess.Popen(["avahi-publish-service", "parker", "_coap._udp", "5683", "\myparker"], stdout=subprocess.PIPE)
    output, err = p.communicate()
    print "*** Running command ***\n", output

x = threading.Thread(target=publishService)
x.start()