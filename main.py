import numpy as np
from psycopg2.extensions import register_adapter, AsIs
from Model.data import DB


# Даём правильное толкование типам данных из библиотеки Numpy:
register_adapter(np.int64, AsIs)


if __name__ == '__main__':
    db = DB()
    db.commit_data()
