import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str

@dataclass
class SiteConfig:
        url: str


@dataclass
class AdminConfig:
    email: str
    password: str
    debug: bool


@dataclass
class BotConfig:
    bot_token: str
    group_id: int


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str
    db_name: typing.Optional[str]


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig = None
    bot: BotConfig = None
    database: DatabaseConfig = None
    site: SiteConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    current_db = raw_config['database']['db']

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
            debug=raw_config["admin"]["debug"],
        ),

        bot=BotConfig(
            bot_token=raw_config["bot"]["token"],
            group_id=raw_config["bot"]["group_id"],
        ),

        database=DatabaseConfig(**raw_config[current_db]),

        site=SiteConfig(url=raw_config['site']['url']),

    )
