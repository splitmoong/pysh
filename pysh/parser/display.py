#parser/display.py

'''
A file containing static functions that help display the parse tree
'''

GRAY = "\033[90m"
RESET = "\033[0m"
    
def display_parse_tree(node, prefix="", is_last=True):
    
    if node is None:
        return

    #print current
    connector = "└── " if is_last else "├── "
    print(f"{GRAY}{prefix}{connector}{str(node)}{RESET}")

    #recurse
    if hasattr(node, "children") and node.children:
        new_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(node.children):
            display_parse_tree(child, new_prefix, i == len(node.children) - 1)  