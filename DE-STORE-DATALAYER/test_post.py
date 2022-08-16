import datetime
import requests
import json

now = datetime.datetime.now().strftime('%Y%m%d')

BASE = "http://127.0.0.1:5000/"

asd = '{"Status":1,"PaymentMethod":1,"Date":"'+now+'","User":1}'
print(asd)
response = requests.put(
    BASE + "PurchaseOrderAPI",
    data = asd,
    headers = {"Content-Type": "application/json"}
    )
try:
    print(response.json())
except:
    print(response)