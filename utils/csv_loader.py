import csv
import os


def load_first_checkout_row():
    path = os.path.join("data", "checkout_data.csv")

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row = next(reader, None)

        if not row:
            raise ValueError("checkout_data.csv is empty or missing a row")

        required_fields = ["first", "last", "postal", "items"]
        for field in required_fields:
            if field not in row:
                raise KeyError(f"Missing column '{field}' in checkout_data.csv")

        return (
            row["first"],
            row["last"],
            row["postal"],
            int(row["items"])
        )
