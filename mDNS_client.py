# mDNS Client
import subprocess
import re

def getServerIp():
    p = subprocess.Popen(["avahi-browse", "-rtp", "_coap._udp"], stdout=subprocess.PIPE)
    output, err = p.communicate()
    # print "*** Running command ***\n", output
   
    #Extract IP from string
    ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', output)
    print("Server IP : " + ip[0])
    return ip[0]

getServerIp()    






