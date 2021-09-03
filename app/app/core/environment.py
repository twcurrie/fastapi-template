import logging
from aenum import MultiValueEnum  # type: ignore


class Environment(MultiValueEnum):
    PRODUCTION = "production", "prod", "PROD"
    SCALING = "scaling", "SCALING"
    DEVELOPMENT = "development", "dev", "DEV"
    TESTING = "testing", "test", "TEST"

    @classmethod
    def _missing_value_(cls, value):
        logging.warning(
            f"Unknown environment string provided ({value}), defaulting to {cls.DEVELOPMENT.name}"  # type: ignore
        )
        return cls.DEVELOPMENT

    def is_development(self):
        return self == Environment.DEVELOPMENT

    def is_testing(self):
        return self == Environment.TESTING

    def is_production(self):
        return self == Environment.PRODUCTION
