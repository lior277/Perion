import os
from behave.__main__ import main as behave_main

FEATURE_PATH = "features/cart.feature".lower()

if __name__ == "__main__":
    if not os.path.exists(FEATURE_PATH):
        raise FileNotFoundError(f"Feature file not found: {FEATURE_PATH}")
    behave_main(FEATURE_PATH)
