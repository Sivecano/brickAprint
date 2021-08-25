import requests, json

set = "8015-1"

with open("key.txt", "r") as f:
    key = f.read().strip()

parts = json.loads(requests.get("https://rebrickable.com/api/v3/lego/sets/" + set + "/parts/?key=" + key).text)

for i in range(parts["count"]):
    print(parts["results"][i]["quantity"],parts["results"][i]["part"]["part_num"])
