# IoTParker

IoT Parking system

## Getting Started

### Prerequisites

- Python 2.7

## Deployment

### Upload
You can use deploy.bat to upload a folder to host and run a python script:
``` shell
> deploy.bat [host-address] [folder-to-upload] [script-filename]
```

Example 1:
``` shell
> deploy.bat pi@iot-pi116.local parkingspot script.py
```

Example 1:
``` shell
> deploy.bat 192.168.1.254 parkingspot start.py
```

### Avoid passwords
To avoid typing passwords generate the private/public key pair:
``` shell
> ssh-keygen -t rsa
```
accept all the defaults
