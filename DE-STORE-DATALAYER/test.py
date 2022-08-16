from datetime import date
import requests
import json

BASE = "http://127.0.0.1:5000/"

response = requests.put(
    BASE + "StoreAPI",
    data='{"id": 1,"Name":"HEADQUARTERS","Address": "Lothian Industrial Estate", "manager": 1}',
    headers = {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "StoreAPI",
    data='{"id": 2,"Name":"Paper Street Store","Address": "Paper Street", "manager": 2}',
    headers = {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "StoreAPI",
    data='{"id": 3,"Name":"Scissor Street Store","Address": "Scissor Street", "manager": 3}',
    headers = {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 1, "UserType": 1, "Name": "Foo Barman", "Points": 0, "Email": "Foo.Barman@foo.bar", "Mobile": "0123456789", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 2, "UserType": 1, "Name": "Store ManagerOne", "Points": 0, "Email": "storeman1@foo.bar", "Mobile": "0123456777", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 3, "UserType": 1, "Name": "Store ManagerTwo", "Points": 0, "Email": "storeman2@foo.bar", "Mobile": "0123456778", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 4, "UserType": 2, "Name": "Good CustomerOne", "Points": 1000, "Email": "customer1@foo.bar", "Mobile": "0123456378", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 5, "UserType": 2, "Name": "Good CustomerTwo", "Points": 1000, "Email": "customer2@foo.bar", "Mobile": "0123556378", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 6, "UserType": 2, "Name": "Good CustomerThree", "Points": 1000, "Email": "customer3@foo.bar", "Mobile": "0223456378", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 7, "UserType": 2, "Name": "Good CustomerFour", "Points": 1000, "Email": "customer4@foo.bar", "Mobile": "0523456378", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "UserAPI",
    data = '{"id": 8, "UserType": 2, "Name": "Good CustomerFive", "Points": 1000, "Email": "customer5@foo.bar", "Mobile": "0923456378", "Active": 1}',
    headers =  {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "ArticleAPI",
    data = '{"id":1,"Name":"Bread","Description":"tasty","Price":2,"Points":1,"Active":1}',
    headers = {"Content-Type": "application/json"}
    )

response = requests.put(
    BASE + "ArticleAPI",
    data = '{"id":2,"Name":"Beer","Description":"beer=good!","Price":5,"Points":1,"Active":1}',
    headers = {"Content-Type": "application/json"}
    )

date = date.today()

i = 1
while i <= 10:
    response = requests.put(
        BASE + "ItemAPI",
        data = '{"id":'+str(i)+',"Article":2,"Status":1,"Store":1,"StockTransfer":0}',
        headers = {"Content-Type": "application/json"}
    )
    i = i + 1
i = 11
while i <= 20:
    response = requests.put(
        BASE + "ItemAPI",
        data = '{"id":'+str(i)+',"Article":1,"Status":1,"Store":1,"StockTransfer":0}',
        headers = {"Content-Type": "application/json"}
    )
    i = i + 1
asd = '{"SQL":"Select store_model.Name, store_model.Address, user_model.Name from store_model inner join user_model on user_model.id = manager where manager = 1"}'
response = requests.post(
    BASE + "SQLiteAPI",
    data = asd,
    headers = {"Content-Type": "application/json"}
    )
print(response.json())