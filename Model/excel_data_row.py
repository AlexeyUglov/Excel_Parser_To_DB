from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
import pandas as pd
from Model.dataframe_from_excel import DataframeFromExcel
from Config.config import config


Base = declarative_base()


# Класс для формирования строки таблицы
class ExcelDataRow(Base):
    __tablename__ = config.db.db_table_name

    @classmethod
    def set_attribute(cls, dataframe_from_excel: DataframeFromExcel):
        setattr(
            cls,
            'dataframe_from_excel',
            dataframe_from_excel
        )
        return cls

    dataframe_from_excel: DataframeFromExcel = DataframeFromExcel()

    # Генератор заголовков столбцов:
    column_name_generator = (column_name for column_name, column_data in dataframe_from_excel.df.items())

    id: Mapped[int] = mapped_column(
        name='id',
        type_=Integer,
        primary_key=True,
        index=True,
    )

    company: Mapped[str] = mapped_column(
        name=next(column_name_generator),
        type_=String,
        nullable=False,
    )

    fact_qliq_data1: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    fact_qliq_data2: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    fact_qoil_data1: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    fact_qoil_data2: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    forecast_qliq_data1: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    forecast_qliq_data2: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    forecast_qoil_data1: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    forecast_qoil_data2: Mapped[int] = mapped_column(
        name=next(column_name_generator),
        type_=Integer,
        nullable=True,
    )

    def __init__(self, table_row: pd.Series):
        cell_data_generator = (cell_data for cell_data in table_row)

        self.company = next(cell_data_generator)

        self.fact_qliq_data1 = self.__create_cell_data(cell_data=next(cell_data_generator))
        self.fact_qliq_data2 = self.__create_cell_data(cell_data=next(cell_data_generator))
        self.fact_qoil_data1 = self.__create_cell_data(cell_data=next(cell_data_generator))
        self.fact_qoil_data2 = self.__create_cell_data(cell_data=next(cell_data_generator))

        self.forecast_qliq_data1 = self.__create_cell_data(cell_data=next(cell_data_generator))
        self.forecast_qliq_data2 = self.__create_cell_data(cell_data=next(cell_data_generator))
        self.forecast_qoil_data1 = self.__create_cell_data(cell_data=next(cell_data_generator))
        self.forecast_qoil_data2 = self.__create_cell_data(cell_data=next(cell_data_generator))

    def __create_cell_data(self, cell_data: Integer | None) -> int:
        return cell_data if cell_data else 0
