import threading
import time
from selenium.common.exceptions import WebDriverException

TEXT_KEYWORDS = [
    "close", "dismiss", "cancel", "no thanks", "not now", "x",
    "ok", "got it", "continue", "skip", "accept", "deny", "allow", "agree"
]

CSS_CLOSE_SELECTORS = [
    "*[aria-label*='close']",
    "*[aria-label*='dismiss']",
    "button.close", ".close", ".btn-close", ".modal-close",
    "[data-test='close']", "[data-test='modal-close']",
    "[role='button'][aria-label*='close']",
]

OVERLAY_SELECTORS = [
    "[role='dialog']", "[aria-modal='true']",
    ".modal", ".popup", ".overlay", ".backdrop", ".modal-backdrop",
    "#modal", "#popup"
]


# -------------------------------------------------------------
# ULTRA STEEL POPUP KILLER (single execution)
# -------------------------------------------------------------
def steel_kill_popup(driver):
    """Destroys ANY popup using multiple brute-force methods."""
    if driver is None:
        return

    # 1️⃣ Text-based close button match
    for kw in TEXT_KEYWORDS:
        try:
            elements = driver.find_elements(
                "xpath",
                f"//*[contains(translate(text(),"
                "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{kw}')]"
            )
            for el in elements:
                try:
                    driver.execute_script("arguments[0].click();", el)
                    return
                except:
                    pass
        except:
            pass

    # 2️⃣ CSS close buttons
    for selector in CSS_CLOSE_SELECTORS:
        try:
            els = driver.find_elements("css selector", selector)
            for el in els:
                try:
                    driver.execute_script("arguments[0].click();", el)
                    return
                except:
                    pass
        except:
            pass

    # 3️⃣ Remove overlays
    for selector in OVERLAY_SELECTORS:
        try:
            els = driver.find_elements("css selector", selector)
            for el in els:
                try:
                    driver.execute_script("arguments[0].remove();", el)
                    return
                except:
                    pass
        except:
            pass

    # 4️⃣ Remove iframes (Facebook login, Google auth, etc.)
    try:
        frames = driver.find_elements("tag name", "iframe")
        for f in frames:
            try:
                driver.execute_script("arguments[0].remove();", f)
                return
            except:
                pass
    except:
        pass

    # 5️⃣ Blur Chrome native password bubble
    try:
        driver.execute_script("document.activeElement?.blur();")
    except WebDriverException:
        pass

    # 6️⃣ Remove ALL shadow-root modals
    try:
        driver.execute_script("""
            const killShadow = (root) => {
                try {
                    const closeEls = root.querySelectorAll('*');
                    for (const e of closeEls) {
                        if (e.innerText && /(close|dismiss|ok|cancel|not now)/i.test(e.innerText)) {
                            e.click();
                        }
                    }
                } catch (e) {}
            };

            document.querySelectorAll('*').forEach(el => {
                if (el.shadowRoot) killShadow(el.shadowRoot);
            });
        """)
    except:
        pass


# -------------------------------------------------------------
# BACKGROUND STEEL POPUP KILLER (runs forever)
# -------------------------------------------------------------
def start_steel_popup_killer(driver):
    """Runs popup killer every 120ms in background thread."""
    def loop():
        while True:
            try:
                steel_kill_popup(driver)
            except:
                pass
            time.sleep(0.12)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
