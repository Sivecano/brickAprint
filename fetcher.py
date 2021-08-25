import requests, json
import pandas


def get_partlist(set):
    with open("key.txt", "r") as f:
        key = f.read().strip()

    parts = json.loads(requests.get("https://rebrickable.com/api/v3/lego/sets/" + set + "/parts/?key=" + key).text)

    out = []

    for i in range(parts["count"]):
        out.append({"quantity" : parts["results"][i]["quantity"],
                    "part_num" : parts["results"][i]["part"]["part_num"],
                    "colours" : [b[0] for b in parts["results"][i]["color"]["external_ids"]["LDraw"]["ext_descrs"]]})

    return pandas.DataFrame(out)

if __name__ == "__main__":
    print(get_partlist("8015-1"))
