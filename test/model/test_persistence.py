import unittest
import os

from germanium_build_monitor.model import persistence
from germanium_build_monitor.model.JenkinsServer import JenkinsServer


class TestPersistence(unittest.TestCase):
    def test_persistence(self):
        persistence.user_home = '/tmp'  # FIXME: temp folder

        config_path = os.path.join(persistence.user_home, '.felixbm')

        if os.path.exists(config_path):
            os.remove(config_path)

        root_model, settings = persistence.load_state()

        settings.systray_items_count = 22
        server = JenkinsServer(
            name="jentest",
            url="http://jen:8080",
            use_authentication=True,
            user="wut",
            password="wutpass",
        )

        root_model.servers.append(server)

        persistence.persist_state(root_model, settings)

        loaded_model, loaded_settings = persistence.load_state()

        self.assertEqual(22, loaded_settings.systray_items_count)
        self.assertEqual(1, len(loaded_model.servers))

        loaded_server = loaded_model.servers[0]

        self.assertEqual("jentest", loaded_server.name)
        self.assertEqual("http://jen:8080", loaded_server.url)
        self.assertTrue(loaded_server.use_authentication)
        self.assertEqual("wut", loaded_server.user)
        self.assertEqual("wutpass", loaded_server.password)


if __name__ == '__main__':
    unittest.main()
