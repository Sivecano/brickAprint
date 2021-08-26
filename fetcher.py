import requests, json, os
import pandas


def get_partlist(set : str):
    with open("key.txt", "r") as f:
        url = f"https://rebrickable.com/api/v3/lego/sets/{set}/parts/?key=" + f.read().strip()

    readcount = 0
    out = []
    while True:
        parts = json.loads(requests.get(url).text)

        for i in range(min(parts["count"] - readcount * 100, 100)):
            
            if ("LEGO" in parts["results"][i]["color"]["external_ids"]):
                coloursource = "LEGO"
            elif "LDraw" in parts["results"][i]["color"]["external_ids"]:
                coloursource = "LDraw"
            else:
                coloursource = list(parts["results"][i]["color"]["external_ids"])[0]
            
            
            out.append({"quantity" : parts["results"][i]["quantity"],
                        "part_num" : parts["results"][i]["part"]["part_num"],
                        "colours" : [b[0] for b in parts["results"][i]["color"]["external_ids"][coloursource]["ext_descrs"]]})
        if parts["next"] is None:
            break
        url = parts["next"]
        readcount += 1

    return pandas.DataFrame(out)


class CacheMGR:
    def __init__(self, cache_dir='model_cache'):
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)
        
        if (not os.path.exists(cache_dir + os.sep + "cachelist.txt")):
            with open(cache_dir + os.sep + "cachelist.txt", "w") as f:
                pass
        self.cache_dir = cache_dir
        self.cache_list = open(cache_dir + os.sep + "cachelist.txt", 'r+')
        self.cached_parts = [p.strip() for p in self.cache_list.readlines()]

    def query_cache_for_part(self, part_number: int):
        return part_number in self.cached_parts

    def get_parts(self, part_list: list):
        number_of_downloaded_parts = 0
        for p in part_list:
            number_of_downloaded_parts += self.get_part(p)
        print(f'downloaded {number_of_downloaded_parts} parts')


    def get_part(self, model_number: str):
        if not self.query_cache_for_part(model_number):
            try:
                r = requests.get(url=f'https://www.ldraw.org/library/official/parts/{model_number}.dat')
                assert r.status_code == 200, 'Brick Acquisition Error'
                with open(f'model_cache/{model_number}.dat', 'w+') as f:
                    f.write(r.text)
                self.cached_parts.append(model_number)
                self.cache_list.write(f'{model_number}\n')
                return 1
            except AssertionError:
                try:
                    r = requests.get(url=f'https://www.ldraw.org/library/unofficial/parts/{model_number}.dat')
                    assert r.status_code == 200, 'Brick Acquisition Error'
                    with open(f'model_cache/{model_number}.dat', 'w+') as f:
                        f.write(r.text)
                    self.cached_parts.append(model_number)
                    self.cache_list.write(f'{model_number}\n')
                    print(f'got part nr. {model_number} from unofficial list')
                    return 1
                except AssertionError:
                    print(f'could not get brick model {model_number}')
        return 0


    def __del__(self):
        self.cache_list.close()


if __name__ == "__main__":
    parts = get_partlist("21045-1")
    print(parts)
    
    CacheMGR().get_parts([73230])
