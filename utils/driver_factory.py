from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from utils.config_manager import ConfigManager


def create_driver():
    config = ConfigManager()
    browser = config.browser().lower()

    # -----------------------------
    # FIREFOX
    # -----------------------------
    if browser == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        if config.headless():
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        return driver

    # -----------------------------
    # CHROME
    # -----------------------------
    options = ChromeOptions()

    # Headless if requested
    if config.headless():
        options.add_argument("--headless=new")

    # ----------------------------------
    # Disable Chrome automation banner
    # ----------------------------------
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # ----------------------------------
    # Disable Save, Change password popups
    # ----------------------------------

    prefs = {
        # Disable Chrome "save password?" popup
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,

        # Disable Chrome "change your password" (leak detection)
        "profile.password_manager_leak_detection": False,

        # Disable Chrome "save card" popup
        "autofill.credit_card_enabled": False,

        # Disable Chrome "save address" popup
        "autofill.profile_enabled": False,
        "autofill.address_enabled": False,
    }

    options.add_experimental_option("prefs", prefs)

    # -----------------------------
    # Stability flags (optional)
    # -----------------------------
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # Use a fresh profile so Chrome forgets password behavior
    options.add_argument("--user-data-dir=C:/Temp/ChromeTestProfile")

    # Instantiate the driver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver
