import json
import os


class ConfigManager:
    def __init__(self, path: str | None = None):
        if path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(base_dir)
            path = os.path.join(root_dir, "config.json")

        self._path = path
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found at: {path}")

        with open(path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def base_url(self) -> str:
        return self._data.get("base_url", "https://www.saucedemo.com/")

    def browser(self) -> str:
        return self._data.get("browser", "chrome")

    def timeout(self) -> int:
        return int(self._data.get("timeout", 20))

    def headless(self) -> bool:
        return bool(self._data.get("headless", False))
