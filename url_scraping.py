import requests
import xmltodict
import json
import os

# URL of the XML data
number = "1122"
for i in range(1,500):
    new_number = int(number)-i
    print("number -- ",new_number)
    url = f'https://nxtools-svc.siemens.net:19100/xmlExport/switchgearData/8DJH24-00{new_number}'
    print(url)

    response = requests.get(url,verify=False)
    if response.status_code == 200:
        xml_data = response.content
        try:
            dict_data = xmltodict.parse(xml_data)

            json_data = json.dumps(dict_data, indent=4)

            # print(json_data)
            with open(f'fetched_data/8DJH24-00{new_number}.json', 'w') as json_file:
                json_file.write(json_data)
            print(f"{new_number} saved successfully")
        except Exception as E:
            print(f"Execption occurred on {new_number} : {E}")
            continue
    else:
        continue
