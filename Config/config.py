from dataclasses import dataclass
from dacite import from_dict
import json
import os


@dataclass
class DB:
    username: str
    password: str
    db_table_name: str
    host: str
    port: int
    db_name: str


@dataclass
class Input:
    excel_file_name: str


@dataclass
class Config:
    db: DB
    input: Input


class ConfigCreator:
    def __init__(self, file_name: str):
        with open(file=file_name, mode="r", encoding="utf-8") as f:
            self.json_dict: dict = json.load(f)

    def create_config(self) -> Config:
        check_params: tuple = ("username", "password")
        missing_params: list = []

        for param in check_params:
            env_var: str = str(self.json_dict["db"][param]).strip().lstrip("$")

            if env_var not in os.environ.keys():
                missing_params.append(env_var)

        if missing_params:
            raise Exception(f"""\n!!!!!!!!!!!!!!!!!!!!!!!!\nНе заданы необходимые переменные среды — {', '.join("'" + element + "'" for element in missing_params)}\n!!!!!!!!!!!!!!!!!!!!!!!!""")

        self.json_dict["db"]["username"] = os.path.expandvars(self.json_dict["db"]["username"]).strip()
        self.json_dict["db"]["password"] = os.path.expandvars(self.json_dict["db"]["password"]).strip()

        config: Config = from_dict(
            data_class=Config,
            data=self.json_dict
        )

        return config


config: Config = ConfigCreator(file_name=r"Config/config.json").create_config()
