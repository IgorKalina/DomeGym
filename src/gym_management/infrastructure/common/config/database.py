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

    def get_full_url(self, safe: bool = True) -> str:
        password = self.user.password if safe else self.user.password.get_secret_value()
        return f"{self.driver}://{self.user.name}:{password}@{self.host}:{self.port}/{self.name}"
