import os
from pathlib import Path
import dotenv

def _get_project_env_path() -> Path:
    """
    Finds the path to the .env file in the project root.
    
    This assumes the script is located in a subdirectory two levels deep 
    from the project root where the .env file should be.
    Example structure: project_root/.env, project_root/src/utils/api_key_setup.py
    
    Adjust `parents[2]` if your script's location within the project is different.
    - `parents[0]` is the script's own directory.
    - `parents[1]` is one level up.
    - `parents[2]` is two levels up.
    """
    return Path(__file__).resolve().parents[2] / '.env'

def load_or_check_ai_api_key():
    """
    Checks for and sets up the GEMINI_API_KEY in the project's .env file.

    This function performs the following actions:
    1. Checks if a .env file exists in the project root and creates one if not.
    2. Checks if the GEMINI_API_KEY is present and non-empty in the .env file.
    3. If the key is missing, it prompts the user to input their key.
    4. The provided key is then saved to the .env file for future use and
       is also set in the current session's environment variables.
    """
    dotenv_path = _get_project_env_path()

    # 1. Check if .env exists; create it if it doesn't.
    if not dotenv_path.is_file():
        print(f"'.env' file not found. Creating a new one at: {dotenv_path}")
        try:
            dotenv_path.touch()
        except OSError as e:
            print(f"Error: Could not create .env file. Please check permissions.")
            print(f"Details: {e}")
            return

    # Load existing environment variables from the .env file.
    dotenv.load_dotenv(dotenv_path)

    # 2. Check if GEMINI_API_KEY exists and has a value.
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("\nGEMINI_API_KEY was not found or is empty in your .env file.")
        
        # Prompt the user to paste the key.
        user_key_input = input("Paste your Gemini API key and press Enter: ").strip()

        if user_key_input:
            # Save the key to the .env file.
            dotenv.set_key(str(dotenv_path), 'GEMINI_API_KEY', user_key_input)
            
            # Set the key in the current environment for immediate use.
            os.environ['GEMINI_API_KEY'] = user_key_input
            print("✅ Successfully saved GEMINI_API_KEY to your .env file.")
        else:
            print("No API key was provided. Please run the setup again when ready.")