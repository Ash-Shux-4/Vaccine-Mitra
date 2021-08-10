from os import environ
from datetime import datetime, timedelta
import pytz
import requests
import time
import schedule
import pandas as pd

#defining constants


time_interval = 20  # (in seconds) Specify the frequency of code execution
dist_id = "195"
msg = "Blank"
tel_token = "1734684130:AAG17ffVctKSf7O_cfYjsUMBg9f5lfJvoI0" # Authentication token provided by Telegram bot
tel_id = "-1001308896244"
IST = pytz.timezone('Asia/Kolkata')           # Indian Standard Time - Timezone
slot_found =  False
register="https://selfregistration.cowin.gov.in/"

df = pd.DataFrame(columns=['Name','Date'])
df=df.append({'Name':"UHC 25",'Date':"15-06-2021"},ignore_index=True)


def process(dist_id):
    raw_TS = datetime.now(IST) + timedelta(days=1)  # Tomorrows date
    tom_date = raw_TS.strftime("%d-%m-%Y")  # Formatted Tomorrow's date
    today_date = datetime.now(IST).strftime("%d-%m-%Y")  # Current Date
    curr_time = (datetime.now().strftime("%H:%M:%S"))  # Current time
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={dist_id}&date={today_date}"
    response = requests.get(url)
    raw_JSON = response.json()
    return raw_JSON, today_date, curr_time

def get_availability_18(age=18):



    global df
    raw_JSON, today_date, curr_time = process(dist_id)
    for cent in raw_JSON["centers"]:
        for sess in cent["sessions"]:
            sess_date = sess['date']
            res=((df['Name'] == cent["name"]) & (df['Date'] == sess_date)).any()

            if sess["min_age_limit"] == age and sess["available_capacity"] > 0:
                if res == False:
                    df = df.append({'Name': cent['name'], 'Date': sess_date}, ignore_index=True)
                    print(df)
                    slot_found = True
                    msg = f"""For age 18+ [Vaccine Available] at {cent["pincode"]} on {sess_date}\n\tCenter : {cent["name"]}\n\tVaccine: {sess["vaccine"]}\n\tDose_1: {sess["available_capacity_dose1"]}\n\tDose_2: {sess["available_capacity_dose2"]}
                            \n\n\tRegister: {register}"""

                    send_msg_on_telegram(msg)

                    print(f"INFO: [{curr_time}] Vaccine Found for 18+")
                else:
                    print("Already sent the notif")
    else:
        slot_found = False
        print(f"INFO: [{today_date}-{curr_time}] Vaccine NOT Found for 18+ in Panipat")





def send_msg_on_telegram(msg):
    telegram_api_url = f"https://api.telegram.org/bot{tel_token}/sendMessage?chat_id={tel_id}&text={msg}"
    tel_resp = requests.get(telegram_api_url)

    if tel_resp.status_code == 200:
        print("Notification has been sent on Telegram")
    else:
        print("Could not send Message")

def welcome():
    wel="Welcome to the Grp"
    send_msg_on_telegram(wel)
#welcome()
def clear():
    global df
    df= df.iloc[0:1]
get_availability_18()



schedule.every(47).minutes.do(clear)
schedule.every(2).minutes.do(get_availability_18)

while True:
    schedule.run_pending()
    time.sleep(5)