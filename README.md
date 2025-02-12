# Wheelchair_lights
Wheelchair_lights that mount to the back of the wheelchair seat

Hardware list:
Waveshare 4x8 rgb led hat
Raspberrry pi zero wh
32gb sd card
usb cord
battery pack

Assembly:

Set up a hotspot on a mobile device with a simple network name and password. 
Unzip the img folder, if using a raspberry pi zero 2 wh use the img found in Wheelchairlights2

Use raspberry pi imager software to add the custom OS using the file wheelchair_lights.img, set the Raspberry pi device to Raspberry pi zero (not 2 for this version) Before writing the img to the sd card, edit settings, setup a password for the username, configure the SSID with the network name of the hotspot, click show password and enter the network password. Under services, enable SSH and use password authentication and click yes to apply settings. 

While the img is writing and verifying to the sd card, attach the rgb led hat to the gpio pins of the raspberry pi zero. 

When the sd card is finished, insert into the sd slot on the raspberry pi zero and plug into the battery pack. On the mobile device hosting the hotspot go to manage hotspot and see the raspberrypi (or whatever you named the device) to find the ip address. If you select this connection the ip address of the raspberry pi will be in the 192.168.xxx.xxx format. 

In a web browser on your mobile device enter the following url http://192.168.xxx.xxx:5000 replacing the x's for the ip address of the raspberry pi. See wheelchair_lights_control.png example.

Included are the raw codes for the files app.py and index.html which can be found on the raspberry pi running the project at ~/wheelchair_lights/app.py and ~/wheelchair_lights/templates/index.html 

Included are the stl files for the raspberry pi zero housing and the wheelchair attachment. The wheelchair attachment file is made to fit the back of my wheelchair so it won't fit other thinner backed wheelchairs and the file will need to be modified accordingly.

Safe travels!
