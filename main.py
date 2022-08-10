import os
import requests
import json

# AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
# AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
# AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")
import keys

endpoint = f'https://api.airtable.com/v0/{keys.AIRTABLE_BASE_ID}/{keys.AIRTABLE_TABLE_NAME}'


class AirtableData:
    def __init__(self, api_key, url):
        self.api_key = api_key
        self.url = url

    def add_to_airtable(self, name, link, date):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "records": [
                {
                    "fields": {
                        "Name": name,
                        "URL": link,
                        "Date": date
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
        # Method to "GET" data == .get and transform data to string == .text
        response = requests.get(self.url, headers=headers).text
        # read data with json package
        response_info = json.loads(response)
        print(response_info)
        urls_dic = []
        # Lê dicionario(nested) e trata erro quando chave não existe
        for record_values in response_info.values():
            for value in record_values:
                try:
                    urls = value["fields"]["URL"]
                except KeyError:
                    continue
                urls_dic.append(urls)
        return urls_dic


# Enter data to Airtable
airtable_data = AirtableData(keys.AIRTABLE_API_KEY, endpoint)
# Read data from Airtable
print(airtable_data.take_info())
