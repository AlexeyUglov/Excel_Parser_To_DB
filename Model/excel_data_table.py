import pandas as pd
from Model.excel_data_row import ExcelDataRow
from Model.dataframe_from_excel import DataframeFromExcel
from Config.config import config


# Класс для формирования всей таблицы
class ExcelDataTable:
    def __init__(
        self,
        file_path: str = config.input.excel_file_name
    ):
        self.excel_data_rows: list[ExcelDataRow] = []
        self.file_path: str = file_path
        self.dataframe_from_excel = DataframeFromExcel(file_path=self.file_path)

        # Формируем и добавляем строки таблицы:
        excel_data_row_generator = (ExcelDataRow.set_attribute(dataframe_from_excel=self.dataframe_from_excel)(row) for index, row in self.dataframe_from_excel.df.iterrows())

        while True:
            excel_data_row: ExcelDataRow = next(excel_data_row_generator, None)

            if excel_data_row is None:
                break

            self.excel_data_rows.append(excel_data_row)

        # Формируем и добавляем строку с расчетными тоталами по Qoil, Qliq:
        self.totals_row: pd.Series = self.calculate_totals()
        self.excel_data_rows.append(ExcelDataRow(self.totals_row))

    def calculate_totals(self) -> pd.Series:
        totals_row_data: list = [
            'TOTAL:',
            sum([each_row.fact_qliq_data1 for each_row in self.excel_data_rows]),
            sum([each_row.fact_qliq_data2 for each_row in self.excel_data_rows]),
            sum([each_row.fact_qoil_data1 for each_row in self.excel_data_rows]),
            sum([each_row.fact_qoil_data2 for each_row in self.excel_data_rows]),
            sum([each_row.forecast_qliq_data1 for each_row in self.excel_data_rows]),
            sum([each_row.forecast_qliq_data2 for each_row in self.excel_data_rows]),
            sum([each_row.forecast_qoil_data1 for each_row in self.excel_data_rows]),
            sum([each_row.forecast_qoil_data2 for each_row in self.excel_data_rows]),
        ]

        return pd.Series(data=totals_row_data)
