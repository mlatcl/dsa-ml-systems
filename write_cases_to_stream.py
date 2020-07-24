import urllib.request
import pandas as pd
import json

covid_data_url = 'https://raw.githubusercontent.com/dsfsi/covid19africa/master/data/line_lists/line-list-nigeria.csv'
covid_data_csv = 'cases.csv'
urllib.request.urlretrieve(covid_data_url, covid_data_csv)

csv_file = pd.DataFrame(pd.read_csv("cases.csv"))
csv_file = csv_file.rename(columns={"province/state": "state"})[['case_id', 'age', 'gender', 'city', 'state']]
print(csv_file.columns)
csv_file.to_json("cases.json", orient='index')

lines=[]
with open('cases.json', 'r') as f:
    while True:
        # Get next line from file 
        line = f.readline() 
        lines.append(line)
        
        # if line is empty 
        # end of file is reached 
        if not line: 
            break

json_lines = json.loads(lines[0])
import subprocess
for index, obj in json_lines.items():
    print(json.dumps(obj))
    subprocess.check_output(
    ["faust", "-A", "dsa_streaming", "send", "@process_case", json.dumps(obj)],
    stderr=subprocess.STDOUT)
