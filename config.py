# THIS HOW TUTOR WROTE THE BELOW CODE.#

import time
import requests, datetime, smtplib

PUNE_LAT = 18.8671
PUNE_LONG = 73.9801
MY_EMAIL = "mrdumy001@gmail.com"
MY_PASSWORD = "gmplbyywyevldfuw"
current_hour = datetime.datetime.now().hour


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    if PUNE_LONG-5 < iss_longitude < PUNE_LONG+5 and PUNE_LAT-5 < iss_latitude < PUNE_LAT+5:
        return True
    

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
    

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="mrdumy001@gmail.com",
                msg="Subject:ISS Passing over Pune.🛰\n\nnHey Rizwan,"
                    "\nWake up! ISS is passing over your city.Try to have a look if you can see it."
            )
        print("mail sent, check!")



