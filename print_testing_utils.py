import fetcher
import os

def get_parts_stl(part_numbers: list):
    fetcher.CacheMGR().get_parts(part_numbers)
    os.system('chmod +x ldraw2stl/bin/dat2stl')
    for pn in part_numbers:
        os.system(os.path.join('.','ldraw2stl','bin','dat2stl --file model_cache',f'{pn}.dat --ldrawdir .','ldraw --scale 1 > print_test_stl_out',f'{pn}.stl')
