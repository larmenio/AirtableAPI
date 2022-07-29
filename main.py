import requests
import os
from datetime import date
import json

from sqlalchemy import null
import candidates

AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'



class Airtable_data:
    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url

    def add_to_airtable(self, candidate):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "records": [
                {
                    "fields": {
                        "Name": name,
                        "Email": email,
                        "Birth Date": birth
                    }
                }
            ]
        }
        # http methods?
        # What is the method to "create"=> POST

        r = requests.post(self.url, json=data, headers=headers)
        print(r.json())
        print(r.status_code)


    def take_info(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        #Method to "GET" data == .get and transform data to string == .text
        response = requests.get(self.url, headers=headers).text
        #read data with json package
        response_info = json.loads(response)
        print(response_info)
        names = []
        #Le dicionario(nested) e trata erro quando chave não existe
        for record_values  in response_info.values():
            for value in record_values:
                try:
                    name = value["fields"]["Name"]
                except KeyError:
                    continue
                names.append(name)
        return names

#Enter data to Airtable
start = True
while start:  
    print("Enter data: ")
    name = input('Type your name: ')
    email = input('Type your email: ')

    error_date = True
    #tratamento de exceção data incorreta
    while error_date:
        try:
            birth = str(date.fromisoformat(input("Type date (YYYY-MM-DD): ")))
            candidate = candidates.Candidates(name, email, birth) 
        except ValueError:
            print('Incorrect date format!')
        else:
            break
        
    Airtable_data(AIRTABLE_API_KEY, endpoint).add_to_airtable(candidate)
    print('Add more data? ')
    decision = input('Y or N ')
    decision = decision.upper()
    if decision == 'Y':
        start = True
    elif decision == 'N':
        break

#Read data from Airtable
print(Airtable_data(AIRTABLE_API_KEY, endpoint).take_info())

