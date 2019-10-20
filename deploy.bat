echo off

if "%3"=="" (
  echo "Missing a parameters:"
  echo "Usage: `deploy.bat [host-address] [folder-to-upload] [script-filename]`"
  echo "Example usage: `deploy.bat pi@iot-pi%2.local parkingspot script.py`"
  echo "Example usage: `deploy.bat 192.168.1.254 parkingspot start.py`"
  exit /b 0
)

scp %userprofile%/.ssh/id_rsa.pub %1:~/.ssh/authorized_keys

ECHO Stopping remote scripts...
ssh %1 pkill python

ECHO Deleting remote files...
ssh %1 rm -rf ~/parking/

ECHO Uploading files..
scp -r %2/ %1:~/parking/

ECHO Starting script...
ssh %1 nohup python ~/parking/%3 &

ECHO Complete!