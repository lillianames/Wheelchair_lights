# Wheelchair_lights  
Wheelchair lights that mount to the back of the wheelchair seat.

## Hardware list:
- Waveshare 4x8 RGB LED Hat
- Raspberry Pi Zero WH
- 32GB SD card
- USB cord
- Battery pack

## Assembly:

1. **Set up a hotspot** on a mobile device with a simple network name and password.

2. **Download the image file** to set up on an SD card for the Raspberry Pi:
   - [wheelchair_lights.img for Raspberry Pi Zero](https://mega.nz/file/jCJCXb6D#yqctBnDldJoIEpaP_x5YnqObicx_L_UAUbxd3iVq6C8)
   - [Wheelchairlights2.img for Raspberry Pi Zero 2](https://mega.nz/file/vfwjQJyT#CLdrzL3r-ozLoPqEql9SVEQoDTOwOZHmXN2aEqFzBxw)

   **Note**: After downloading the `.zip` file, unzip it to extract the `.img` file.

3. **Use Raspberry Pi Imager software** to write the custom OS using the `wheelchair_lights.img` file.  
   Set the Raspberry Pi device to **Raspberry Pi Zero** (not Zero 2 for this version).  
   Before writing the image to the SD card, edit the following settings:
   - **Set a password** for the username.
   - **Configure the SSID** with the network name of the hotspot.
   - **Enter the hotspot network password** (click "Show password").
   - **Enable SSH** and choose password authentication (click yes to apply these settings).

4. While the `.img` is being written and verified to the SD card, **attach the RGB LED Hat** to the GPIO pins of the Raspberry Pi Zero.

5. After the SD card is finished:
   - Insert the SD card into the Raspberry Pi Zero.
   - Plug the Raspberry Pi into the battery pack.

6. On the mobile device hosting the hotspot:
   - Go to **Manage Hotspot** and find the Raspberry Pi (or whatever you named the device) to locate its IP address. The format will be `192.168.xxx.xxx`.
   - In a web browser on your mobile device, enter the following URL:
     ```
     http://192.168.xxx.xxx:5000
     ```
     Replace the `xxx` with the actual IP address of the Raspberry Pi.

7. **Example interface**: See `wheelchair_lights_control.png` for an example of the control page interface.

---

## Code Files:
- The raw code for the project is located on the Raspberry Pi at:
  - `~/wheelchair_lights/app.py`
  - `~/wheelchair_lights/templates/index.html`
  
You can also find the code on the GitHub repository if needed.

---

## STL Files:
Included are the STL files for the Raspberry Pi Zero housing and the wheelchair attachment.
- **Note**: The wheelchair attachment is designed to fit the back of my wheelchair. If your wheelchair has a thinner back, the file may need to be modified.

---

**Safe travels!** 🌟
