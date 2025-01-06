from pydantic import BaseModel, SecretStr


class DatabaseUser(BaseModel):
    name: str
    password: SecretStr


class DatabaseConfig(BaseModel):
    user: DatabaseUser
    host: str
    port: int
    name: str
    driver: str

    @property
    def full_url(self) -> str:
        return f"{self.driver}://{self.user.name}:{self.user.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
