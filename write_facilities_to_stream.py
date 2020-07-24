import urllib
import pandas as pd
import json

csv_file = pd.DataFrame(pd.read_csv("facilities.csv"))
csv_file = csv_file.rename(columns={"admin1RefName": "state"})[['state', 'num_doctors_fulltime', 'facility_name','facility_type_display']]
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
    ["faust", "-A", "dsa_streaming", "send", "@process_facility", json.dumps(obj)],
    stderr=subprocess.STDOUT)
