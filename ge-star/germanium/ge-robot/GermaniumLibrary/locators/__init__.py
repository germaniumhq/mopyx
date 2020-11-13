from germanium.static import (
    open_browser,
    close_browser,
    click,
    double_click,
    right_click,
    hover,
    go_to,
    waited,
    select_file,
    select,
    deselect,
    type_keys,
    get_web_driver,
    drag_and_drop,
    Button,
    Css,
    XPath,
    JsSelector,
    AnyOfSelector,
    Element,
    Input,
    CheckBox,
    Image,
    InputText,
    InputFile,
    Link,
    Text,
    Alert,
    Window,
    S,
)
from robot.api.deco import keyword


class GermaniumLocators:
    @keyword
    def use_selenium_browser(self):
        from robot.running.namespace import IMPORTER

        selenium_library = find_library(IMPORTER, "SeleniumLibrary")
        wd = selenium_library.get_instance(create=False).driver

        open_browser(wd=wd)

    @keyword
    def open_browser(self, browser_name: str):
        open_browser(browser_name)

    @keyword
    def close_browser(self):
        close_browser()

    @keyword
    def maximize_window(self):
        get_web_driver().maximize_window()

    @keyword
    def click(self, selector: str):
        s = self._resolve_selector(selector)
        click(s)

    @keyword
    def double_click(self, selector: str):
        s = self._resolve_selector(selector)
        double_click(s)

    @keyword
    def hover(self, selector: str):
        s = self._resolve_selector(selector)
        hover(s)

    @keyword
    def right_click(self, selector: str):
        s = self._resolve_selector(selector)
        right_click(s)

    @keyword
    def go_to(self, url: str):
        go_to(url)

    @keyword
    def type_keys(self, keys):
        type_keys(keys)

    @keyword
    def type_keys_in(self, selector, keys):
        s = self._resolve_selector(selector)
        type_keys(keys, s)

    @keyword
    def drag_and_drop(self, start_selector, end_selector):
        start = self._resolve_selector(start_selector)
        end = self._resolve_selector(end_selector)
        drag_and_drop(from_selector=start, to_selector=end)

    @keyword
    def select_by_index(self, selector, index):
        s = self._resolve_selector(selector)
        select(s, index=eval(index, globals(), locals()))

    @keyword
    def select_by_text(self, selector, text):
        s = self._resolve_selector(selector)
        select(s, text=eval(text, globals(), locals()))

    @keyword
    def select_by_value(self, selector, value):
        s = self._resolve_selector(selector)
        select(s, value=eval(value, globals(), locals()))

    @keyword
    def deselect_by_index(self, selector, index):
        s = self._resolve_selector(selector)
        deselect(s, index=eval(index, globals(), locals()))

    @keyword
    def deselect_by_text(self, selector, text):
        s = self._resolve_selector(selector)
        deselect(s, text=eval(text, globals(), locals()))

    @keyword
    def deselect_by_value(self, selector, value):
        s = self._resolve_selector(selector)
        deselect(s, value=eval(value, globals(), locals()))

    @keyword
    def select_file(self, selector, file_path):
        s = self._resolve_selector(selector)
        select_file(s, file_path=file_path)

    @keyword
    def assert_exists(self, selector):
        s = self._create_selector(selector)
        assert s.exists(), f"No elements matching selector {selector} could be found."

    @keyword
    def assert_missing(self, selector):
        s = self._create_selector(selector)
        assert s.not_exists(), f"Selector {selector} matched elements"

    def _resolve_selector(self, selector):
        s = self._create_selector(selector)

        try:
            return waited(s)
        except Exception as e:
            raise Exception(f"Unable to resolve {selector}", e)

    def _create_selector(self, selector):
        try:
            s = S(eval(selector, self.selector_globals(), locals()))

        except Exception as e:
            raise Exception(f"Unable to create selector {selector}", e)

        return s

    def selector_globals(self):
        extended_globals = dict(globals())

        extended_globals["S"] = S
        extended_globals["Css"] = Css
        extended_globals["XPath"] = XPath
        extended_globals["JsSelector"] = JsSelector
        extended_globals["AnyOfSelector"] = AnyOfSelector
        extended_globals["Button"] = Button
        extended_globals["Element"] = Element
        extended_globals["Input"] = Input
        extended_globals["CheckBox"] = CheckBox
        extended_globals["Image"] = Image
        extended_globals["InputText"] = InputText
        extended_globals["InputFile"] = InputFile
        extended_globals["Link"] = Link
        extended_globals["Text"] = Text
        extended_globals["Alert"] = Alert
        extended_globals["Window"] = Window

        return extended_globals

    @staticmethod
    def noop():
        """
        Method so the optimizing imports aren't removing it
        :return:
        """
        pass


def find_library(importer, library_name: str):
    for library in importer._library_cache.values():
        if library.name == library_name:
            return library

    raise Exception(f"Unable to find {library_name}. Make sure you load the library.")
