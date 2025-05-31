# This is the main logic code.

import time
import requests, datetime, smtplib


# Make some values constant , e.g. Pune's Longitude/Latitude etc.
PUNE_LAT = 18.8671
PUNE_LONG = 73.9801
MY_EMAIL = "your email"
MY_PASSWORD = "your_email_password"
current_hour = datetime.datetime.now().hour


# Trace the curent position for ISS if it passing over Pune. 
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if PUNE_LONG-5 < iss_longitude < PUNE_LONG+5 and PUNE_LAT-5 < iss_latitude < PUNE_LAT+5:
        return True


# Check Pune day/night status using Sunrise-Sunset API.
def is_night():
    parameter = {
        "lat": PUNE_LAT,
        "lng": PUNE_LONG,
        "formatted": 0
             }
    response2 = requests.get("https://api.sunrise-sunset.org/json", params=parameter)
    response2.raise_for_status()
    data2 = response2.json()
    pune_sunrise_hour = int(data2["results"]["sunrise"].split("T")[1].split(":")[0])+5
    pune_sunset_hour = int(data2["results"]["sunset"].split("T")[1].split(":")[0])+5
    if current_hour > pune_sunset_hour or current_hour < pune_sunrise_hour:
        return True
    
# Keep tracing the ISS & send an email alert if tracked in the night.
# Start SMTP connection to send an email.
while True:
    time.sleep(60)                           #Take pause every minute.
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="recipient-email-address",
                msg="Subject:ISS Passing over Pune.🛰\n\nnHey Rizwan,"
                    "\nWake up! ISS is passing over your city.Try to have a look if you can see it."
            )

