import requests
from datetime import datetime
import smtplib

MY_EMAIL = "example@com"
MY_PASS = "my password"
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

def iss_over():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5  and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise :
        return True


if iss_over() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.login(MY_EMAIL, MY_PASS)
    connection.sendmail(from_addr=MY_EMAIL,
                        to_addrs=MY_EMAIL,
                        msg="Subject:Look UP\n\nThe ISS is somewhere above you :)"
                        )





