import os
from dataclasses import dataclass


@dataclass
class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL", "sqlite:///urls.db")
    BASE_URL: str = os.environ.get("BASE_URL", "http://localhost:5000")
    SHORT_CODE_LENGTH: int = int(os.environ.get("SHORT_CODE_LENGTH", 6))


@dataclass
class DevelopmentConfig(Config):
    DEBUG: bool = True


@dataclass
class CIConfig(Config):
    DEBUG: bool = False
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    BASE_URL: str = "http://localhost"


@dataclass
class ProductionConfig(Config):
    DEBUG: bool = False


_configs = {
    "development": DevelopmentConfig,
    "testing": CIConfig,
    "production": ProductionConfig,
}


def get_config() -> Config:
    env = os.environ.get("FLASK_ENV", "development")
    return _configs.get(env, DevelopmentConfig)()
