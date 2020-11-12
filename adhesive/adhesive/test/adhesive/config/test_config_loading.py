import unittest

from adhesive.config.LocalConfigReader import read_configuration


class TestConfigLoading(unittest.TestCase):
    def test_local_config_reading(self):
        config = read_configuration(
            cwd="test/adhesive/config/tc_local/local",
            environment={
                "HOME": "test/adhesive/config/tc_local/user",
                "ADHESIVE_ENVIRONMENT": "environment",
                "ADHESIVE_ENVIRONMENT_LIST": "environment_environment_list_a:environment_environment_list_b"
            }
        )

        self.assertEqual("local", config.local)
        self.assertEqual("user", config.user)
        self.assertEqual("environment", config.environment)
        self.assertEqual("/tmp/adhesive", config.temp_folder)
        self.assertEqual([
            "environment_environment_list_a",
            "environment_environment_list_b",
        ], config.environment_list)
        self.assertEqual([
            "local_local_list_a",
            "local_local_list_b",
        ], config.local_list)
        self.assertEqual([
            "user_user_list_a",
            "user_user_list_b",
        ], config.user_list)

        self.assertIsNone(config.not_existing)
