import pandas as pd
import datetime
from Config.config import config


class DataframeFromExcel:
    def __init__(self, file_path: str = config.input.excel_file_name):
        self.df = pd.read_excel(
            io=file_path,
            sheet_name=0,
            dtype={
                'id': object
            },
            keep_default_na=False,
            header=[0, 1, 2],
        )

        updated_column_labels: list = []

        for tuple_of_labels in self.df.columns:
            temp_list: list = []
            for label in tuple(tuple_of_labels):
                if label == 'data1':
                    temp_list.append(str(datetime.date(2023, 1, 1)))
                elif label == 'data2':
                    temp_list.append(str(datetime.date(2023, 1, 12)))
                elif not str(label).startswith('Unnamed:'):
                    temp_list.append(label)
            if len(temp_list) == 1:
                updated_column_labels.append(temp_list[0])
            else:
                updated_column_labels.append(tuple(temp_list))

        self.df.columns = [x for x in updated_column_labels]

        self.df = self.df.set_index(
            keys='id',
        )
