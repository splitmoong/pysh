import os

def run(args):
    if not args:
        raise RuntimeError("mkdir: missing operand")
    for dir_path in args:
        os.makedirs(dir_path, exist_ok=True)
    print(f"Created directories: {', '.join(args)}")