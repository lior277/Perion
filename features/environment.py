import json
import os

from utils.config_manager import ConfigManager
from utils.driver_factory import create_driver
from pages.pages_container import Pages

# Import STEEL popup killer
from utils.popup_killer import steel_kill_popup, start_steel_popup_killer


# ============================================================
#  BEHAVE HOOKS
# ============================================================

def before_all(context):
    """Load config + users.json"""
    context.settings = ConfigManager()

    users_path = os.path.join("data", "users.json")
    with open(users_path, "r", encoding="utf-8") as f:
        context.users = json.load(f)


def before_scenario(context, scenario):
    """Start browser + pages + background popup killer"""
    context.driver = create_driver()
    context.pages = Pages(context.driver, context.settings)

    # 🚀 Start continuous popup killer
    start_steel_popup_killer(context.driver)


def after_scenario(context, scenario):
    """Screenshot on scenario failure + quit driver"""
    if scenario.status == "failed" and hasattr(context, "driver"):
        os.makedirs("screenshots", exist_ok=True)

        safe = (
            scenario.name
            .replace(" ", "_")
            .replace("/", "_")
            .replace(":", "_")
        )

        path = os.path.join("screenshots", safe + ".png")
        context.driver.save_screenshot(path)
        print(f"[SCENARIO FAILURE SCREENSHOT] → {path}")

    if hasattr(context, "driver") and context.driver:
        context.driver.quit()


def after_step(context, step):
    """Run popup killer after every step + screenshot on failure"""

    # --- Run popup killer safely ---
    if hasattr(context, "driver") and context.driver:
        try:
            steel_kill_popup(context.driver)
        except Exception:
            pass

    # --- Step-level screenshot on failure ---
    if step.status == "failed" and hasattr(context, "driver"):
        os.makedirs("screenshots", exist_ok=True)

        safe = (
            step.name
            .replace(" ", "_")
            .replace("/", "_")
            .replace(":", "_")
        )

        path = os.path.join("screenshots", safe + ".png")
        context.driver.save_screenshot(path)
        print(f"[STEP FAILURE SCREENSHOT] → {path}")
