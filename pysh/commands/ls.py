import os

def run(args):
    show_all = False
    paths = []

    for arg in args:
        if arg.startswith("-"):
            if "a" in arg:
                show_all = True
        else:
            paths.append(arg)

    if not paths:
        paths = ["."]
    
    items = []
    for path in paths:
        if os.path.isdir(path):
            for f in os.listdir(path):
                if show_all or f not in (".DS_Store", ".localized"):
                    items.append(os.path.join(path, f) if path != "." else f)
        elif os.path.exists(path):
            items.append(path)
        else:
            print(f"ls: cannot access '{path}': No such file or directory")

    for item in sorted(items):
        print(item)