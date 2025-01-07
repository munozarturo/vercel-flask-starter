import os
from typing import Optional
import dotenv

dotenv.load_dotenv()


class EnvironementVariables:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True

    @staticmethod
    def __getitem__(name: str) -> Optional[str]:
        return os.getenv(name)


env = EnvironementVariables()

__all__ = ["env", "EnvironementVariables"]
