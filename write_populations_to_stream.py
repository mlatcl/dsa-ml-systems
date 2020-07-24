import urllib
import pandas as pd
import json

csv_file = pd.DataFrame(pd.read_csv("populations.csv"))
csv_file.columns = ['state', 'refcode', 'nation', 'nation_code', 'population']
csv_file = csv_file[['state', 'population']]
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
    ["faust", "-A", "dsa_streaming", "send", "@process_state_pops", json.dumps(obj)],
    stderr=subprocess.STDOUT)
