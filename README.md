# pysh 🐚

**pysh** is a lightweight, python-based terminal shell inspired by Bash.
 It allows users to execute built-in commands, system commands, and will be extended with functionality like command history, autocomplete, and AI-driven natural language interpretation.

---

https://github.com/user-attachments/assets/5c380260-1183-4b57-8d15-dd14218255b4

## ✨ Features

- **Python REPL-based shell** for command execution.
- **Built-in commands**: `cd`, `pwd`, `exit`.
- **External command execution** with full `stdout`/`stderr` integration.
- **Modular architecture** with a Lexer and Parser for future enhancements.
- **Easily extendable** to support file operations, system monitoring, and AI-driven commands.

---

## 🚀 Installation

### macOS & Linux

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