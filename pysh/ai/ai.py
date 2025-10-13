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


#for the api key
import ai.managekeys
import platform
import importlib


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
    def call_gemini(user_instruction: str):
        
        key = ai.managekeys.load_or_check_ai_api_key()

        # Configure the genai client after the key is available so it can use the env var
        try:
            genai = importlib.import_module('google.generativeai')
            # try to configure client explicitly if possible
            try:
                genai.configure(api_key=key)
            except Exception:
                # if configure fails, assume env var is sufficient
                pass
        except Exception:
            raise RuntimeError('google.generativeai library is required for AI commands')

        os_type = AI._get_os()
        prompt = (
            f"You are a command-line assistant. "
            f"Generate a valid shell command for {os_type} that performs the following task: "
            f"{user_instruction}. Output only the command."
        )

        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        return response.text.strip()