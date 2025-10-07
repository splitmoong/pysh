"""
Package initialization for pysh.

This module applies a conservative, early suppression of noisy native
logging from absl/gRPC by setting the ABSL_MIN_LOG_LEVEL environment
variable and tightening Python logger levels for relevant loggers.

If you'd rather keep native stderr messages, set the environment
variable `PYSH_ALLOW_NATIVE_LOGS=1` before importing the package.
"""
import os
import logging

# Allow opt-out for users who want to see native logs
if os.getenv("PYSH_ALLOW_NATIVE_LOGS", "0") != "1":
	# Tell absl to drop logs below FATAL at C++ level early.
	os.environ.setdefault("ABSL_MIN_LOG_LEVEL", "3")

	# Also set Python logger levels to critical for noisy libraries.
	logging.getLogger("google").setLevel(logging.CRITICAL)
	logging.getLogger("grpc").setLevel(logging.CRITICAL)
	logging.getLogger("absl").setLevel(logging.CRITICAL)

__all__ = []
