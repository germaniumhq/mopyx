from adhesive.config import LocalConfigReader
from adhesive.config.LocalAdhesiveConfig import LocalAdhesiveConfig
from adhesive.config.NoopAdhesiveConfig import NoopAdhesiveConfig

current = LocalConfigReader.read_configuration()
