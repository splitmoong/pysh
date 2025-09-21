# pysh 🐚

**pysh** is python-based terminal shell inspired by bash.
 It allows users to execute built-in commands, system commands, cycle through command history and will be extended with AI-driven natural language interpretation.

### videos (pysh demo & Codemate.ai Builder)

https://drive.google.com/drive/folders/1Pjl8n9iTkAs59wZhGKMv-5qqqct0PgPE?usp=sharing

---

https://github.com/user-attachments/assets/d382e86e-1bc4-4dae-8407-5d45d3b07800


## Features

- **Built-in commands**
  - `cd`, `cpu`, `disk`, `ls`, `mem`, `mkdir`, `pwd`, `rm`
  - Each implemented in its own module under `commands/`.

- **External command execution**
  - Anything not recognized as a built-in is passed to the system via `subprocess`.
  - Full `stdout`/`stderr` integration.

- **Logging** 
    ```bash
    pysh$ --log
    logging enabled
    pysh$ cat foo.txt
    Tokens: [COMMAND(cat), ARG(foo.txt)]
    Parse tree:
    └── Statement
        └── Command
            ├── COMMAND_NAME(cat)
            └── ARG(foo.txt)
    roses are red,
    violets are blue.
    once this file is read,
    it says "hey, I'm foo!".
    ```
    - use --log to show the list of tokens and the parse tree.
    - use --nolog to return to default state.

- **History**
  - Use up and down arrows to cycle through previous commands. 
  - Works even after exiting pysh, stored externally at ~/.pysh_history.

- **Modular**
  - Each core piece of the shell (lexer, parser, checker, executor) and the commands live in their own files.

---

## Installation

### Linux & macOS

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/splitmoong/pysh.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd pysh
    ```

3.  **Make the REPL executable:**
    ```bash
    chmod +x pysh/repl.py
    ```

4.  **Create a symlink in your `PATH`:**
    ```bash
    sudo ln -s /full/path/to/pysh/pysh/repl.py /usr/local/bin/pysh
    ```
    > **Note**: Replace `/full/path/to/pysh` with the absolute path to the cloned repository on your system.

5.  **Test your shell:**
    ```bash
    pysh
    ```
    You should see the `pysh$` prompt.

### Windows (via PowerShell or Windows Terminal)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/splitmoong/pysh.git
    ```

2.  **Navigate to the project folder:**
    ```bash
    cd pysh
    ```

3.  **Run the REPL directly using Python:**
    ```bash
    python pysh\repl.py
    ```
    > On Windows, creating a global symlink like on Linux/macOS is less straightforward, so running the script directly is the recommended approach.

---
<!--
## 📁 Project Structure
--!>