import fetcher
import os

def get_parts_stl(part_numbers: list):
    fetcher.CacheMGR().get_parts(part_numbers)
    os.system('chmod +x ldraw2stl/bin/dat2stl')
    for pn in part_numbers:
        os.system(f'./ldraw2stl/bin/dat2stl --file model_cache/{pn}.dat --ldrawdir ./ldraw --scale 1 > print_test_stl_out/{pn}.stl')