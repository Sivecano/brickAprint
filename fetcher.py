import requests, json
import pandas


def get_partlist(set):
    with open("key.txt", "r") as f:
        url = "https://rebrickable.com/api/v3/lego/sets/" + set + "/parts/?key=" + f.read().strip()

    readcount = 0
    out = []
    while True:
        parts = json.loads(requests.get(url).text)

        for i in range(min(parts["count"] - readcount * 100, 100)):
            out.append({"quantity" : parts["results"][i]["quantity"],
                        "part_num" : parts["results"][i]["part"]["part_num"],
                        "colours" : [b[0] for b in parts["results"][i]["color"]["external_ids"]["LDraw"]["ext_descrs"]]})
        if parts["next"] is None:
            break
        url = parts["next"]
        readcount += 1

    return pandas.DataFrame(out)

if __name__ == "__main__":
    print(get_partlist("21045-1"))
