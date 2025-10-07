'''
ai static class which returns a response from the ai model

available gemini models
models/gemini-2.0-flash-live-001
models/gemini-live-2.5-flash-preview
models/gemini-2.5-flash-live-preview
models/gemini-2.5-flash-native-audio-latest
models/gemini-2.5-flash-native-audio-preview-09-2025
'''

import os
import logging
import sys

# Suppress absl logs entirely
os.environ["ABSL_MIN_LOG_LEVEL"] = "3"  # 0=INFO, 1=WARNING, 2=ERROR, 3=FATAL
logging.getLogger("google").setLevel(logging.CRITICAL)

#for the api key
from dotenv import load_dotenv
import platform

# Import the google generative AI library while temporarily silencing
# C/C++-level stderr. Some lower-level libraries (gRPC/absl) emit
# messages directly to the process stderr which bypass Python's
# logging handlers. To prevent the noisy "ALTS creds ignored..."
# message, redirect fd 2 to /dev/null just for the import.
try:
    # POSIX-only; safe on Linux which this project targets
    devnull = open(os.devnull, "w")
    _stderr_fd = sys.stderr.fileno()
    _saved_stderr_fd = os.dup(_stderr_fd)
    os.dup2(devnull.fileno(), _stderr_fd)
    import google.generativeai as genai
finally:
    # restore original stderr
    try:
        os.dup2(_saved_stderr_fd, _stderr_fd)
    except Exception:
        pass
    try:
        os.close(_saved_stderr_fd)
    except Exception:
        pass
    try:
        devnull.close()
    except Exception:
        pass

# Make sure Python-level loggers are quiet for grpc/absl/google
logging.getLogger("grpc").setLevel(logging.CRITICAL)
logging.getLogger("absl").setLevel(logging.CRITICAL)

class AI:
    @staticmethod
    def _get_os():
        system = platform.system().lower()
        if "linux" in system:
            return "linux"
        elif "windows" in system:
            return "windows"
        elif "darwin" in system:
            return "macos"
        else:
            return "unknown"

    @staticmethod
    def _load_key():
        load_dotenv()
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("API key not found in .env")
        return key

    @staticmethod
    def call_gemini(user_instruction: str):
        key = AI._load_key()

        # Some native libraries (gRPC/absl) may emit messages directly to
        # the process stderr when the model is configured or content is
        # generated. Temporarily redirect fd 2 to /dev/null to suppress
        # those messages (POSIX-only). This prevents the E0000 ALTS message
        # from appearing when the model initializes.
        devnull = open(os.devnull, "w")
        _stderr_fd = sys.stderr.fileno()
        _saved_stderr_fd = os.dup(_stderr_fd)
        try:
            os.dup2(devnull.fileno(), _stderr_fd)
            genai.configure(api_key=key)

            os_type = AI._get_os()
            prompt = (
                f"You are a command-line assistant. "
                f"Generate a valid shell command for {os_type} that performs the following task: "
                f"{user_instruction}. Output only the command."
            )

            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
        finally:
            try:
                os.dup2(_saved_stderr_fd, _stderr_fd)
            except Exception:
                pass
            try:
                os.close(_saved_stderr_fd)
            except Exception:
                pass
            try:
                devnull.close()
            except Exception:
                pass

        return response.text.strip()
