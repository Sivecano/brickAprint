import os, importlib

path = f"Tweaker-3{os.sep}__init__.py"

if not os.path.exists(path):
    with open(path, "w") as f:
        f.write("from .MeshTweaker import Tweak\n")
        f.write("from . import FileHandler")


Tweaker3 = importlib.import_module("Tweaker-3")

FileHandler = Tweaker3.FileHandler
Tweak = Tweaker3.Tweak

def tweak_file(path):
    
    fileHandler = FileHandler.FileHandler()
    objs = fileHandler.load_mesh(path)
    if objs is None:
        return None

    info = {}
    for part, content in objs.items():
        mesh = content["mesh"]
        info[part] = {}
        # mesh, extended_mode, vebose, show_progress, favside, minimize volume?
        x = Tweak(mesh, True, False, True, None, True)
        info[part]["matrix"] = x.matrix
        info[part]["tweaker_stats"] = x
        #print("unprintability:", x.unprintability )

    try:
        fileHandler.write_mesh(objs, info, path, "binarystl")
    except FileNotFoundError:
        raise FileNotFoundError("WTF? couldn't output")

if __name__ == "__main__":
    tweak_file("6541.stl")
