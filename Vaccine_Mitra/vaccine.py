import requests
import json
import pandas as pd
import csv



#print(json.dumps(kk))

def vac_data():
    global df
    global kk
    pincode = input("Pincode: ")
    date = input("Date: ")
    #age=self.cmb1.get()

    # url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=132103&date=06-06-2021"
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + pincode + "&date=" + date + ""

    r = requests.get(url)
    kk = r.json()
    df = pd.DataFrame(columns=['Name', 'Capacity', 'Min Age'])
    for i in kk["sessions"]:
        #address =
        #print(i["name"],i["block_name"],i["available_capacity"],i["min_age_limit"],i["slots"])
        df = df.append({'Name': i["name"], 'Capacity': i["address"],'Dist': i["district_name"]},ignore_index = True)
        address=str(i["name"]+", "+i["district_name"]+", "+str(i["pincode"])+", "+i["state_name"])
    #print(address)
    add="GC Gupta hospital, Panipat, 132103, Haryana"
    url1 = "https://api.mapbox.com/geocoding/v5/mapbox.places/"+add+".json?limit=2&access_token=pk.eyJ1IjoiYXNoMTMiLCJhIjoiY2twemsyODlpMDNpMDMwbXU5dWQ2djA1cSJ9.zsRspPHLRQiwemyYTpPm2g"
    params = {
        "key": "oeLHVzGDolUEU0kgRoH4BirAO7JSpvar",
        "location": "UHC Sec 25, Panipat, 132103, Haryana"
    }
    r1 = requests.get(url1)
    kk1=r1.json()
    print(kk1)
    print(r1)

def show():
    global address
    #print(address)

vac_data()
#show()
def get_availability_18(age=18):
    raw_JSON, today_date, curr_time = update_timestamp_send_Request(PINCODE)
    for cent in raw_JSON['centers']:
        for sess in cent["sessions"]:
            sess_date = sess['date']
            if sess["min_age_limit"] == age and sess["available_capacity"] > 0:
                slot_found = True
                msg = f"""For age 18+ [Vaccine Available] at {PINCODE} on {sess_date}\n\tCenter : {cent["name"]}\n\tVaccine: {sess["vaccine"]}\n\tDose_1: {sess["available_capacity_dose1"]}\n\tDose_2: {sess["available_capacity_dose2"]}"""
                send_msg_on_telegram(msg)
                print(f"INFO: [{curr_time}] Vaccine Found for 18+ at {PINCODE}")
    else:
        slot_found = False
        print(f"INFO: [{today_date}-{curr_time}] Vaccine NOT Found for 18+ at {PINCODE}")

def get_availability_18(age=18):



    global df
    raw_JSON, today_date, curr_time = process(dist_id)
    for cent in raw_JSON["centers"]:
        for sess in cent["sessions"]:
            sess_date = sess['date']
            res=df.loc[(df['Name'] == cent["name"]) & (df['Date'] == sess_date)]


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
