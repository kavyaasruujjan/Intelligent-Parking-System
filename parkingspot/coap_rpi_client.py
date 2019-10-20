#!/usr/bin/env python
import socket
import sys

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri
import subprocess
import re


def getServerIp():
    try:
        p = subprocess.Popen(["avahi-browse", "-rtp", "_coap._udp"], stdout=subprocess.PIPE)
        output, err = p.communicate()
        # print "*** Running command ***\n", output

        # Extract IP from string
        ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', output)
        print("Server IP : " + ip[0])
        return ip[0]
    except:
        print("Epic fail")
        sys.exit(1)


class Client:

    def __init__(self, resource, path=None):

        if path is None:
            ip = getServerIp()
            path = "coap://" + ip + ":" + str(5683) + "/" + resource
        else:
            path = path + "/" + resource

        self.host, self.port, self.resource = parse_uri(path)

        try:
            tmp = socket.gethostbyname(self.host)
            self.host = tmp
        except socket.gaierror:
            pass

        self.client = HelperClient(server=(self.host, self.port))
        self.id = None

    def get(self):
        try:
            response = self.client.get(self.resource)
            print(response.pretty_print())
            return response
        except:
            pass

    def put(self, status):
        try:
            payload = self.id + ":" + status
            response = self.client.put(self.resource, payload)
        except:
            pass

    def assign_id(self):
        try:
            response = self.client.post(self.resource, "")
            self.id = response.payload
            return self.id
        except:
            pass

    def register(self, param_status):
        try:
            # payload = self.id + ":" + status
            response = self.client.post(self.resource + "/" + self.id, param_status)
        except:
            pass

    def update_status(self, param_id, param_status):
        try:
            # payload = self.id + ":" + status
            response = self.client.put(self.resource + "/" + param_id, param_status)
        except:
            pass

    def get_status(self):
        try:
            response = self.client.get(self.resource + "/" + self.id)
            return response
        except:
            pass

    # TODO don't use, to be removed
    def post(self):
        try:
            response = self.client.post(self.resource, "")
            self.id = response.payload
        except:
            pass

    def observe(self, client_callback_observe):
        try:
            self.client.observe(self.resource + "/" + self.id, client_callback_observe)
        except:
            pass

    def close(self):
        try:
            self.client.close()
        except:
            pass

