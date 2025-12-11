import sys
from behave.__main__ import main as behave_main

if __name__ == "__main__":
    sys.argv = ["behave", "features/cart.feature", "--no-capture"]  # disable stdout capture so you see logs
    behave_main()
