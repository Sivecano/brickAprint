import requests, json

set = "8015-1"

parts = requests.get("https://rebrickable.com/api/v3/lego/sets/" + set + "/parts/?key=cbd9de9e2b376ed4049d5be2be4c4457")
print(json.fromstring(parts.text))
