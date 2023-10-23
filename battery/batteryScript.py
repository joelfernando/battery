import psutil
import requests
import datetime
import time


timeNow = datetime.datetime.now()
api_url = "https://blr1.blynk.cloud/external/api/isHardwareConnected?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj"
tel_url="https://api.telegram.org/bot6386197966:AAGBc-yNRyZNI5nWmp-sB-fhKOyVYQJ6UKg/sendMessage?chat_id=5441279564"
response = requests.get(api_url)
#print(response.json())
#print(type(response.json()))

if response.json() is True:
    #print ("Online") 
    battery = psutil.sensors_battery()
    percent = round(battery.percent,2)
    plugged = battery.power_plugged
    #print(plugged)
    #plugged = "Plugged In" if plugged else "Not Plugged In"
    switchStatus = requests.get("https://blr1.blynk.cloud/external/api/get?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj&v0").json()
    #print(type(switchStatus))
    print(f'Battery : {percent}%, Charging status : {plugged}, Switch status : {switchStatus}')
    #r1 = requests.post(tel_url,json={'text':f'Battery : {percent}%, Charging status : {plugged}, Switch status : {switchStatus}'}, timeout=10)

    if switchStatus == 1 and plugged == False:
        print(f"{timeNow}Error : Switch ON but not charging!")
        r1 = requests.post(tel_url,json={'text':f"{timeNow}Error : Switch ON but not charging!"}, timeout=10)
    elif switchStatus == 0 and plugged == True:
        print(f"{timeNow}Error : Switch OFF but charging!")
        r1 = requests.post(tel_url,json={'text':f"{timeNow}Error : Switch OFF but charging!"}, timeout=10)
    else:
        if percent<20 and plugged==False:
            print(f"{timeNow}: Initiating Blynk API to Switch ON server charger...")
            requests.get("https://blr1.blynk.cloud/external/api/update?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj&v0=1")
            time.sleep(1)
            requests.get("https://blr1.blynk.cloud/external/api/update?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj&v0=0")
            time.sleep(1)
            requests.get("https://blr1.blynk.cloud/external/api/update?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj&v0=1")
            r1 = requests.post(tel_url,json={'text':f"{timeNow}: Initiating Blynk API to Switch ON server charger..."}, timeout=10)

        elif percent>90 and plugged==True:
            print(f"{timeNow}: Initiating Blynk API to Switch OFF server charger...")
            requests.get("https://blr1.blynk.cloud/external/api/update?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj&v0=0")
            time.sleep(1)
            requests.get("https://blr1.blynk.cloud/external/api/update?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj&v0=1")
            time.sleep(1)
            requests.get("https://blr1.blynk.cloud/external/api/update?token=6emhHJLC1mJk3hS8eQE7UdZUuoApshSj&v0=0")
            r1 = requests.post(tel_url,json={'text':f"{timeNow}: Initiating Blynk API to Switch OFF server charger..."}, timeout=10)

else:
    print(f"{timeNow}: Offline")
    #telegramToken = "6386197966:AAGBc-yNRyZNI5nWmp-sB-fhKOyVYQJ6UKg"
      
    r = requests.post(tel_url,json={'text':f"{timeNow}: Device is offline"}, timeout=10)
    #telegramUrl = f"https://api.telegram.org/bot{telegramToken}"
    #params = {"chat_id": "5441279564", "text": "Hello World"}
    #r = requests.get(telegramUrl + "/sendMessage?", params=params)
    



