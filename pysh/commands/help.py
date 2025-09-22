def run():
    help_text = f"""
pysh - the python shell
-----------------------

Usage:
  pysh$ [command] [arguments]
  pysh$ --log      Enable debug logging (tokens & parse tree)
  pysh$ --nolog    Disable debug logging
  pysh$ clear      Clear the screen
  pysh$ bye        Exit pysh
  pysh$ help       Show this help message

Built-in Commands:
  cd [dir]             Change current directory (defaults to home)
  ls                   List directory contents
      -a               Show all files    
  pwd                  Print current working directory
  mkdir [dir...]       Create directories
  rm [file/dir]        Remove files or directories
  cpu                  Display real-time CPU usage
  mem                  Display memory usage
  disk                 Display disk usage
  ps                   List active processes

Features:
  - Full external command support (subprocess, stdout/stderr)
  - Modular command architecture (each command in commands/)
  - Command history with up/down arrows
  - Logs show tokens and parse tree for debugging
"""
    print(help_text)