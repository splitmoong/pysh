import os

def run(args):
    path = args[0] if args else os.path.expanduser("~")
    os.chdir(path)
    print(f"Changed to directory: {os.getcwd()}")