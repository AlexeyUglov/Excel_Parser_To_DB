import sqlalchemy as sqla
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from typing import Any
from Model.excel_data_row import Base, ExcelDataRow
from Model.excel_data_table import ExcelDataTable
from Config.config import config


class DB:
    def __init__(self):
        self.session: Any = None
        self.file_path = config.input.excel_file_name
        self.engine: Engine = sqla.create_engine(f"postgresql+psycopg2://{config.db.username}:{config.db.password}@{config.db.host}:{str(config.db.port)}/{config.db.db_name}")
        self.excel_data_table = ExcelDataTable(file_path=self.file_path)

    def commit_data(self):
        Base.metadata.drop_all(bind=self.engine, tables=[ExcelDataRow.__table__])
        Base.metadata.create_all(bind=self.engine, checkfirst=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.session.add_all(instances=self.excel_data_table.excel_data_rows)
        self.session.commit()
