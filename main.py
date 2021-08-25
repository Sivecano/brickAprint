import os
import fetcher
import stlconverter

def convert_to_stl(parts: list, stldir : str):
    os.system('chmod +x ldraw2stl/bin/dat2stl')
    for part in parts:
        path = os.path.join(stldir,part)
        os.system(f'./ldraw2stl/bin/dat2stl --file model_cache/{part}.dat --ldrawdir ./ldraw --scale 1 > {path}.stl')
        
        

def tweak_parts(parts: list, stldir : str):
    for part in parts:
        path = os.path.join(stldir, f"{part}.stl")
        if os.path.exists(path):
            if os.path.getsize(path) > 4:
                stlconverter.tweak_file(f"{stldir}/{part}.stl")

                
def repair_stl(parts: list, stldir: str):
    for part in parts:
        path = os.path.join(stldir,part)
        os.system(f"prusa-slicer --export-stl --repair {path}.stl")

def get_set(set_number : str):
    print("fetching partlist")
    parts = fetcher.get_partlist(set_number)
    numbers = parts["part_num"].tolist()
    print("partlist: ")
    print(parts)
    
    outdir = input("where do you want to store the all the files? : ")
    stldir = os.path.join(outdir, "stl")
    
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists(stldir):
        os.mkdir(stldir)

    manager = fetcher.CacheMGR("model_cache")
    print("downloading parts...")
    manager.get_parts(numbers)
    print("downloaded parts")
    
    print("converting parts...")
    convert_to_stl(numbers, stldir)
    print("done converting parts to stl")
    print("checking and repairing parts...")
    repair_stl(numbers, stldir)
    print("all parts fixed")
                  
    if input("do you want to automatically tweak part orientation? [y/N] ").lower().startswith("y"):
        print("begin tweaking")
        tweak_parts(numbers, stldir)
        print("finished tweaking")
        
    parts.to_csv(os.path.join(outdir, f"{set_number}_part_list.csv"))

    print("\nall done :)")

    

       

if __name__ == "__main__":
    print("Welcome to BrickAPrint :)")
    print("this is a project inspired by the printAbrick project")
    print("this program takes a lego set number as found on rebrickable.com")
    print("and will spit out all the stl files needed to print the set")
    print("as well as the quantities of each part")
    set = input("set to download: ").strip()
    get_set(set)
