from pydantic import ConfigDict

# DATABASE_HOSTNAME=localhost
# DATABASE_PORT=5432
# DATABASE_PASSWORD=admin123
# DATABASE_NAME=fastapi
# DATABASE_USERNAME=postgres
# SECRET_KEY=3cc90f581523c6980ce02c627e648d8057a5a3e122d150592d5e3c102634d13e
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

class Settings(ConfigDict):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


setting = Settings()
