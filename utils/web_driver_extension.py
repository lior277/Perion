from time import sleep
from typing import Any, List, Optional

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotVisibleException,
    ElementNotSelectableException,
    InvalidSelectorException,
    NoSuchFrameException,
    WebDriverException,
    TimeoutException,
)

from utils.config_manager import ConfigManager


def ignore_exception_types():
    return [
        NoSuchElementException,
        StaleElementReferenceException,
        ElementNotVisibleException,
        ElementNotSelectableException,
        InvalidSelectorException,
        ElementNotInteractableException,
        NoSuchFrameException,
        WebDriverException,
    ]


class SearchElement:
    def __init__(self, by: tuple):
        self.by = by
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> Optional[WebElement]:
        try:
            elem = driver.find_element(*self.by)
            if elem and elem.is_enabled():
                return elem
            return None
        except (StaleElementReferenceException, ElementNotInteractableException):
            sleep(0.2)
            return None
        except Exception as e:
            self.last_exception = e
            return None


class SearchElements:
    def __init__(self, by: tuple):
        self.by = by
        self.last_exception = None
        self.elements_found = False

    def __call__(self, driver: WebDriver) -> Optional[List[WebElement]]:
        try:
            elems = driver.find_elements(*self.by)
            self.elements_found = True
            return elems
        except StaleElementReferenceException:
            sleep(0.2)
            return None
        except Exception as e:
            self.last_exception = e
            return None


class ForceClick:
    def __init__(self, by: tuple = None, element: WebElement = None):
        self.by = by
        self.element = element
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> Optional[WebElement]:
        try:
            elem = self.element or driver.find_element(*self.by)
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", elem
            )
            elem.click()
            return elem
        except (ElementClickInterceptedException, ElementNotInteractableException):
            sleep(0.2)
            try:
                driver.execute_script("arguments[0].click();", elem)
                return elem
            except Exception as e:
                self.last_exception = e
                return None
        except StaleElementReferenceException:
            sleep(0.2)
            return None
        except Exception as e:
            self.last_exception = e
            return None


class GetElementText:
    def __init__(self, by: tuple):
        self.by = by
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> str:
        try:
            elem = driver.find_element(*self.by)
            txt = (
                elem.get_attribute("innerText")
                or elem.get_attribute("value")
                or ""
            )
            return txt.strip()
        except StaleElementReferenceException:
            sleep(0.2)
            return ""
        except Exception as e:
            self.last_exception = e
            return ""


class SendKeysAuto:
    def __init__(self, by: tuple, input_text: str):
        self.by = by
        self.input_text = input_text
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> bool:
        try:
            element = DriverEX.search_element(driver, self.by)
            element.clear()
            element.send_keys(self.input_text)
            return True
        except StaleElementReferenceException:
            sleep(0.3)
            return False
        except ElementNotInteractableException as e:
            self.last_exception = e
            sleep(0.2)
            return False
        except Exception as e:
            self.last_exception = e
            return False


class UploadFile:
    def __init__(self, by: tuple, input_text: str):
        self.by = by
        self.input_text = input_text
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> bool:
        try:
            elem = driver.find_element(*self.by)
            elem.send_keys(self.input_text)
            sleep(0.01)
            return True
        except StaleElementReferenceException:
            sleep(0.2)
            return False
        except Exception as e:
            self.last_exception = e
            return False


class NavigateToUrl:
    def __init__(self, url: str):
        self.url = url
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> None:
        try:
            driver.get(self.url)
        except StaleElementReferenceException:
            sleep(0.2)
        except Exception as e:
            self.last_exception = e


class SelectElementFromDropDownByValue:
    def __init__(self, by: tuple, list_item_value: str):
        self.by = by
        self.list_item_value = list_item_value
        self.last_exception = None

    def __call__(self, driver: WebDriver) -> Any:
        try:
            elem = driver.find_element(*self.by)
            Select(elem).select_by_value(self.list_item_value)
            return elem
        except (StaleElementReferenceException, ElementClickInterceptedException):
            sleep(0.2)
            return None
        except Exception as e:
            self.last_exception = e
            return None


class DriverEX:
    config_manager = ConfigManager()
    TIME_TO_WAIT_IN_SECONDS = config_manager.timeout()

    @staticmethod
    def search_element(driver: WebDriver, by: tuple) -> WebElement:
        search = SearchElement(by)
        try:
            return WebDriverWait(
                driver,
                DriverEX.TIME_TO_WAIT_IN_SECONDS,
                ignored_exceptions=ignore_exception_types(),
            ).until(search)
        except TimeoutException:
            if search.last_exception:
                raise search.last_exception
            raise

    @staticmethod
    def search_elements(
        driver: WebDriver,
        by: tuple,
        wait_if_empty: bool = False,
    ) -> List[WebElement]:
        search = SearchElements(by)
        if not wait_if_empty:
            return driver.find_elements(*by)
        try:
            elems = WebDriverWait(
                driver,
                DriverEX.TIME_TO_WAIT_IN_SECONDS,
                ignored_exceptions=ignore_exception_types(),
            ).until(search)
            return elems if elems else []
        except TimeoutException:
            if search.elements_found:
                return []
            return []

    @staticmethod
    def send_keys_auto(driver: WebDriver, by: tuple, input_text: str) -> None:
        action = SendKeysAuto(by, input_text)
        try:
            WebDriverWait(
                driver,
                DriverEX.TIME_TO_WAIT_IN_SECONDS,
                ignored_exceptions=ignore_exception_types(),
            ).until(action)
        except TimeoutException:
            if action.last_exception:
                raise action.last_exception
            raise

    @staticmethod
    def force_click(
        driver: WebDriver,
        by: tuple = None,
        element: WebElement = None,
    ) -> bool:
        action = ForceClick(by, element)
        try:
            elem = WebDriverWait(
                driver,
                DriverEX.TIME_TO_WAIT_IN_SECONDS,
                ignored_exceptions=ignore_exception_types(),
            ).until(action)
            return elem is not None
        except TimeoutException:
            if action.last_exception:
                raise action.last_exception
            raise

    @staticmethod
    def get_element_text(driver: WebDriver, by: tuple) -> str:
        action = GetElementText(by)
        try:
            return WebDriverWait(
                driver,
                DriverEX.TIME_TO_WAIT_IN_SECONDS,
                ignored_exceptions=ignore_exception_types(),
            ).until(action)
        except TimeoutException:
            if action.last_exception:
                raise action.last_exception
            raise

    @staticmethod
    def select_element_from_dropdown_by_value(
        driver: WebDriver,
        by: tuple,
        value: str,
    ) -> None:
        action = SelectElementFromDropDownByValue(by, value)
        try:
            WebDriverWait(
                driver,
                DriverEX.TIME_TO_WAIT_IN_SECONDS,
                ignored_exceptions=ignore_exception_types(),
            ).until(action)
        except TimeoutException:
            if action.last_exception:
                raise action.last_exception
            raise

    @staticmethod
    def upload_file(driver: WebDriver, by: tuple, path: str) -> None:
        action = UploadFile(by, path)
        try:
            WebDriverWait(
                driver,
                DriverEX.TIME_TO_WAIT_IN_SECONDS,
                ignored_exceptions=ignore_exception_types(),
            ).until(action)
        except TimeoutException:
            if action.last_exception:
                raise action.last_exception
            raise

    @staticmethod
    def navigate_to_url(driver: WebDriver, url: str) -> None:
        action = NavigateToUrl(url)
        try:
            WebDriverWait(
                driver,
                30,
                ignored_exceptions=ignore_exception_types(),
            ).until(action)
        except TimeoutException:
            if action.last_exception:
                raise action.last_exception
            raise
