# pysh 🐚

**pysh** is a python-based terminal shell inspired by bash.
 It allows users to execute built-in commands, system commands, cycle through command history and has an AI-driven natural language interpretation.

### videos (pysh demo & Codemate.ai Builder)

https://drive.google.com/drive/folders/1Pjl8n9iTkAs59wZhGKMv-5qqqct0PgPE?usp=sharing

---

https://github.com/user-attachments/assets/d382e86e-1bc4-4dae-8407-5d45d3b07800

## Index

- [Features](#features)
- [Installation](#installation)
- [AI integration and quick usage](#ai-integration-and-quick-usage)
- [Roadmap](#roadmap)


<a id="features"></a>
## Features

- **AI-driven command generation**
    - Use natural-language instructions prefixed with `!` to have pysh generate shell commands.
    ```bash
    pysh$ ! create a temp.py here
    ```

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

<a id="installation"></a>
## Installation

<a id="linux-macos"></a>
### Linux & macOS

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/splitmoong/pysh.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd pysh
    ```

2.a **Install Python dependencies (recommended)**
    ```bash
    pip install -r requirements.txt || pip install google-generativeai
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

<a id="ai"></a>
## AI integration and quick usage

pysh includes a simple AI-driven command generator. You can type natural-language instructions prefixed with an exclamation mark (!) and the REPL will call the AI helper to produce a shell command which can then be executed by pysh.

How it works:
- Prefix an instruction with `!`. Example:
    ```
    pysh$ ! create test.text here
    ```

Important safety note:
- AI-generated commands can be destructive. Review them before allowing execution.

API key setup (paste or prompt)

The AI integration requires a Gemini API key and the `google-generativeai` Python package. The project provides an interactive flow that will prompt you for a key on first use and optionally save it to a `.env` file at the repo root, or you can paste it manually.

1. Install client:
```sh
pip install google-generativeai
```

2. Provide your API key (choose one):

- Option A — Paste into `.env` (recommended for convenience):
    - Create or open a file named `.env` in the project root and add:
        ```env
        GEMINI_API_KEY=your_api_key_here
        ```
    - The `ai.managekeys` helper will read this value when present.

- Option B — Let pysh prompt and save it for you:
    - On first AI call (when no key is available), pysh will prompt you to paste the key. The `ai.managekeys.load_or_check_ai_api_key` helper handles prompting and storing the key.


3. Verify: run pysh and try a simple AI prompt:
```sh
pysh$ !list all hidden files in this directory
```

TODO / Improvements
- Add an explicit confirmation step before executing AI-generated commands.
- Add a safety heuristic to detect high-risk commands and refuse or highlight them.
- Allow selecting different Gemini models instead of a hardcoded model name.

<a id="roadmap"></a>
## Roadmap


```
○ [HERE] Add support for chaining multiple commands using ';', '&&', '||' and '&' (sequential, conditional and background).  
|   
|
○ Add support for more API keys, currently only gemini is supported. make a more graphical cli ui for choosing model, pasting key, managing keys etc.
|
|
○ Add support for local models using Ollama.
|
|   
○ Rework the Tokenization to be closer to bash (3 types), use ply (python-yacc-lex) module instead of manually building parse tree. just write the grammar rules.
|
|
...
```


