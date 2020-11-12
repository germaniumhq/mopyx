from selenium import webdriver


class ActionChains(webdriver.ActionChains):
    def add_action(self, f):
        self._actions.append(f)
        return self

    def add_dynamic_action(self, action_provider):
        def dynamic_action():
            nested_actions = ActionChains(self._driver)
            action_provider(nested_actions)

            nested_actions.perform()

        self.add_action(dynamic_action)
        return self
