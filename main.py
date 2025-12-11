import time
from datetime import datetime
from tuya_iot import TuyaOpenAPI
from dotenv import load_dotenv, find_dotenv
from colorama import Fore, Style
import pyttsx3
import threading
import os

# ---------------------------------------------------------------
# FUNCTION: Asynchronous speech synthesis
# ---------------------------------------------------------------
# pyttsx3 often blocks or freezes if called repeatedly
# from the main thread in long-running loops. To avoid this,
# we run each speech command in its OWN thread.
#
# This mirrors robotics design where actuators run independently
# so perception isn't blocked by action.
# ---------------------------------------------------------------

def speak(text):
    def _speak():
        # Initialize a NEW TTS engine for each utterance.
        # This avoids audio driver locks after first use.
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    # Launch speech in a daemon thread so it doesn't block
    threading.Thread(target=_speak, daemon=True).start()

# ---------------------------------------------------------------
# LOAD CONFIGURATION FROM .env FILE
# ---------------------------------------------------------------
# Using environment variables avoids exposing credentials
# and is standard practice in production robotics/cloud systems.
# ---------------------------------------------------------------

load_dotenv()
find_dotenv()

ACCESS_ID = os.getenv("ACCESS_ID")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
ENDPOINT = os.getenv("ENDPOINT")
DEVICE_ID = os.getenv("DEVICE_ID")

USERNAME = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
COUNTRY_CODE = os.getenv("COUNTRY_CODE")

# ---------------------------------------------------------------
# INITIALIZE TUYA CLOUD OPENAPI CLIENT
# ---------------------------------------------------------------
# The client encapsulates signing, authentication, and
# authorized communication with Tuya’s cloud platform.
# ---------------------------------------------------------------
openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)

# ---------------------------------------------------------------
# INITIAL STATE: assume NO MOTION
# ---------------------------------------------------------------
# We use a simple Finite State Machine:
#   "none" = no motion
#   "pir"  = motion detected
#
# Keeping track of previous state avoids repeated alerts.
# ---------------------------------------------------------------
previous_motion_status = "none"

# ---------------------------------------------------------------
# AUTHENTICATE WITH TUYA CLOUD
# ---------------------------------------------------------------
# This converts your Tuya Smart App account into cloud access
# and returns an access token required for all API calls.
# ---------------------------------------------------------------
try:
    response = openapi.connect(USERNAME, PASSWORD, COUNTRY_CODE, "tuyaSmart")
    print("Token Response:", response)
except Exception as e:
    print("Error:", e)

# ===============================================================
# MAIN REAL-TIME LOOP
# ===============================================================
# This loop continuously:
# 1. polls the PIR sensor status from the cloud,
# 2. interprets the “pir” datapoint,
# 3. detects state transitions,
# 4. triggers speech and logs events.
#
# Equivalent to a perception → state machine → actuation loop.
# ===============================================================
while True:
    try:
        # -------------------------------------------------------
        # QUERY SENSOR STATUS FROM TUYA CLOUD
        # -------------------------------------------------------
        # Tuya returns a JSON structure including:
        #   - pir value: "pir" or "none"
        #   - battery info
        #   - timestamps
        # -------------------------------------------------------
        response = openapi.get(f"/v1.0/iot-03/devices/{DEVICE_ID}/status")
        print(f"{datetime.now()} - Device response: {response}")

        # If API call failed, skip this cycle
        if not response.get('success'):
            print("API Failure:", response)
            time.sleep(3)
            continue

        # -------------------------------------------------------
        # EXTRACT PIR SENSOR VALUE
        # -------------------------------------------------------
        pir_value = None
        for item in response['result']:
            if item['code'] == 'pir':
                pir_value = item['value']

        # If Tuya didn’t send PIR data, skip this cycle
        if pir_value is None:
            print("No PIR data in response!")
            time.sleep(3)
            continue
        
        # -------------------------------------------------------
        # STATE MACHINE LOGIC
        # -------------------------------------------------------
        # Detects transitions:
        #
        #   none → pir  → event: Motion detected
        #   pir  → none → event: No motion
        #
        # The speech actuator is triggered ONLY on transitions,
        # preventing redundant alerts due to polling frequency.
        # -------------------------------------------------------

        # ----------------------------
        # CASE 1: Motion detected
        # ----------------------------
        if pir_value == "pir":
            if previous_motion_status != "pir":
                print(Fore.GREEN + f"{datetime.now()} - Motion detected!" + Style.RESET_ALL)
                speak("Motion detected")

        # ----------------------------
        # CASE 2: No motion detected
        # ----------------------------
        elif pir_value == "none":
            if previous_motion_status != "none":
                print(f"{datetime.now()} - No motion detected.")

        # ----------------------------
        # CASE 3: Unexpected PIR value
        # ----------------------------
        else:
            print(f"Unexpected PIR value received: {pir_value}")

        # -------------------------------------------------------
        # UPDATE FINITE STATE MACHINE MEMORY
        # -------------------------------------------------------  
        previous_motion_status = pir_value

        # -------------------------------------------------------
        # LOOP TIMING
        # -------------------------------------------------------
        # 3 seconds is chosen to:
        # - avoid hitting Tuya rate limits
        # - avoid reading cached states repeatedly
        # - provide real-time responsiveness
        # -------------------------------------------------------
        time.sleep(3)

    # -----------------------------------------------------------
    # USER REQUESTED SHUTDOWN (CTRL+C)
    # -----------------------------------------------------------
    except KeyboardInterrupt:
        print("\nStopped by user.")
        break
    
    # -----------------------------------------------------------
    # ANY OTHER ERROR — do not crash, just retry later
    # -----------------------------------------------------------
    except Exception as e:
        print("Unexpected error:", e)
        time.sleep(5)
