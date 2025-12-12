# Tuya Cloud Interface: Real-Time PIR Motion Sensor Monitoring

This guide explains how to set up and use a PIR Motion Sensor with the Tuya IoT Cloud platform and interact with it using the Tuya Cloud Interface Python project. 

Following these steps, you can link the sensor to the cloud, retrieve its data, and monitor real-time motion detection.

## Prerequisites
- A pc supporting Python 3.7 or higher.
- Create an accoun at [Tuya Developer Platform website](https://iot.tuya.com).
- Download the Tuya Smart app:
  - For Android devices: Download from the [Google Play Store](https://play.google.com/store/apps/details?id=com.tuya.smart&hl=it).
  -	For iOS devices: Download from the [App Store](https://apps.apple.com/us/app/tuya-smart/id1034649547).

***Important: Save your Tuya Smart App email and password — you will need these later.***

## Tuya IoT Project
1.	Visit the [Tuya Developer Platform website](https://iot.tuya.com).
2.	Log in if you already have one.
3.	Create a new cloud project with the following details:
    - Name: Your project name.
    - Description: A brief description of your project.
    - Industry: Education/Campus.
    - Development Method: Smart Home.
    - Data Center: Central Europe (to match the App Data Center).

4. In your cloud project, authorize the following API services:
    - **IoT Core**: Provides basic functionalities such as device management, real-time communication, and data collection.
    - **Authorization Token Managemen**t: Manages authentication and authorization for accessing other APIs.
    - **Smart Home Basic Service**: Offers essential functionalities for managing smart home devices.
    - **Device Status Notification**: Sends real-time notifications on device status updates.
    - **Device Pool Management**: Allows obtaining information about devices, including current status and properties.

5. Set Up the PIR Motion Sensor
    - Open the Tuya Smart app on your phone and log in.
    - Connect the PIR Motion Sensor to a power source and turn it on.
    -	Press and hold the side button until the green light blinks, indicating pairing mode.
    -	Add the sensor as a new device in the app, connecting it to a 2.4GHz Wi-Fi network.
    -	Set the work mode to “OnlyLight” to prevent it from sounding.

6. Link the Sensor to the Cloud Project
    -	In the [Tuya Developer Platform](https://platform.tuya.com), go to your project and navigate to Devices → Link App Account → Add App Account.
    -	In the Tuya Smart app, go to *Mi* at the bottom right of the screen and tap the QR code icon at the top right.
    -	Scan the QR code displayed on the Tuya Developer Platform to link the app with the cloud project.
    -	Verify that the sensor is visible in the cloud project and has been assigned an ID.

7. Set Up the Tuya Cloud Interface Project
Clone this repository in a folder of your choice by navigating to the folder and executing the following command in a terminal:
```bash
git clone https://github.com/giuliab00/AmbientIntelligence25
cd tuya_cloud_interface
```

8. Create a .env file
In the root directory of the project, create a file named .env and add the following content:
```bash
ACCESS_ID=your_access_id #change: Retrieve these from the Overview tab in your Tuya Cloud project.
ACCESS_SECRET=your_access_secret #change
ENDPOINT=https://openapi.tuyaeu.com  
DEVICE_ID=your_device_id #change: Visible in the Devices section of your Cloud Project.
EMAIL=your_tuya_app_email #change: Credentials for your Tuya Smart app account
PASSWORD=your_tuya_app_password #change: Credentials for your Tuya Smart app account
COUNTRY_CODE=+XX  #change: Credentials for your Tuya Smart app account (e.g., +39 for Italy)
```

9. Install the Dependencies
To install the libraries required to run the script, execute the following command in a terminal:
```bash
pip install -r requirements.txt
```

10. Test the Script
Run the script to verify if the sensor data is successfully retrieved:
    ```bash
    python3 main.py
    ```

11.	If successful, the script will return a message similar to the following:
    ```bash
    {
    "result": [
      {"code": "pir", "value": "pir"},
      {"code": "battery_percentage", "value": 0}
    ],
    "success": true,
    "t": 1733318804621,
    "tid": "67c94acbb24311ef828e8aa4893defa6"
    }
    ```

    The "result" field contains the key information from the PIR motion sensor:
  	- "code": "pir", "value": "pir" indicates that motion has been detected.
  	- "code": "pir", "value": "none" indicates no motion detected.
  	- "code": "battery_percentage", "value": 0 reflects the current battery level of the sensor (in this case, 0%).
    This output confirms that the sensor is operational and able to detect motion in real-time. The script can now be expanded to process this data in a way that meets your specific requirements.

## Conclusion 
The data retrieved from the sensor opens up a variety of possibilities for practical applications, such as:
- Storing Data in a Database: Log motion detection events with timestamps for analysis, reporting, or compliance tracking.
- Triggering Notifications: Set up real-time alerts (e.g., push notifications, SMS, or emails) to notify users when motion is detected.
- Home Automation: Use motion detection to automate smart home actions, such as turning on lights, adjusting thermostats, or activating security cameras.
- Behavioral Analytics: Analyze motion trends over time to gain insights into space usage, identify potential security risks, or optimize facility management.
- Machine Learning Applications: Leverage the data to train predictive models for tasks like anomaly detection, predictive maintenance, or optimizing smart environment responses.

Feel free to extend the script to incorporate these functionalities or adapt it to your specific use case. For further support and inspiration, explore the [Tuya Developer Documentation](https://developer.tuya.com/en/docs/iot).
