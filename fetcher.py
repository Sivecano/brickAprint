import requests, json
import pandas

set = "8015-1"

with open("key.txt", "r") as f:
    key = f.read().strip()

parts = json.loads(requests.get("https://rebrickable.com/api/v3/lego/sets/" + set + "/parts/?key=" + key).text)

out = []

for i in range(parts["count"]):
    out.append({"quantity" : parts["results"][i]["quantity"],
                "part_num" : parts["results"][i]["part"]["part_num"],
                "colours" : [b[0] for b in parts["results"][i]["color"]["external_ids"]["LDraw"]["ext_descrs"]]})

print(pandas.DataFrame(out))

