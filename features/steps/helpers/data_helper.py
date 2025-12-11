import csv
import os


class DataHelper:
    def load_first_checkout_row(self):
        path = os.path.join("data", "checkout_data.csv")

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            row = next(reader, None)

            if not row:
                raise ValueError("checkout_data.csv is empty or missing a row")

            required = ["first", "last", "postal", "items"]
            for field in required:
                if field not in row:
                    raise KeyError(f"Missing column '{field}' in checkout_data.csv")

            return (
                row["first"],
                row["last"],
                row["postal"],
                int(row["items"]),
            )
