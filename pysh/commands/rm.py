import os
import shutil

def run(args):
    if not args:
        raise RuntimeError("rm: missing operand")
    for item in args:
        if os.path.isfile(item):
            os.remove(item)
            print(f"Removed file: {item}")
        elif os.path.isdir(item):
            shutil.rmtree(item)
            print(f"Removed directory: {item}")
        else:
            print(f"rm: cannot remove '{item}': No such file or directory")