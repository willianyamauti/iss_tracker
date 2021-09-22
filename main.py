import requests
import datetime as dt
import smtplib
import time

# get yours at https://www.latlong.net/
LATITUDE = -20.385574
LONGITUDE = -43.503578

MY_EMAIL = 'willianyamauti@yahoo.com'
PASSWORD = 'dslgwquaazedtcpq'
SMTP = "smtp.mail.yahoo"


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])

    if LATITUDE - 5 <= LATITUDE <= LATITUDE + 5 and LONGITUDE - 5 <= LONGITUDE <= LONGITUDE + 5:
        return True

def is_night():
    parameters = {
        "lat": LATITUDE,
        "lng": LONGITUDE,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data['results']['sunrise'].split("T")[1].split(":")[0]
    sunset = data['results']['sunrise'].split("T")[1].split(":")[0]
    time_now = dt.datetime.now()
    if sunset <= time_now.hour <= sunrise:
        return True

while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        connection = smtplib.SMTP(SMTP)
        connection.starttls()
        connection.login(MY_EMAIL,PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Look up ☝️\n\nThe ISS is visible in the sky!!!"
        )
