import numpy as np
import pandas as pd


def get_data_from_cian():
    df_res = pd.DataFrame({'lat': [],
                           'lng': [],
                           'area': [],
                           'cost': [],
                           }).to_numpy()
    df7 = pd.read_excel('raw/Cian.xlsx', sheet_name='07_secondary')
    true_column = pd.Index(['LAT', 'LNG', 'FLAT_AREA_TOTAL', 'BARGAINTERMS_PRICE'],
                           dtype='object')
    df_res = np.concatenate((df7[true_column].to_numpy(), df_res), axis=0)

    df2 = pd.read_excel('raw/Cian.xlsx', sheet_name='02-price_parsing')
    true_column = pd.Index(['lat', 'lng', 'Площадь', 'Цена', ], dtype='object')
    df_res = np.concatenate((df2[true_column].to_numpy(), df_res), axis=0)

    df1 = pd.read_excel('raw/Cian.xlsx', sheet_name='01-deal')
    true_column = pd.Index(['lat', 'lng', 'Площадь', 'Оценка цены'], dtype='object')
    df_res = np.concatenate((df1[true_column].to_numpy(), df_res), axis=0)

    df3 = pd.read_excel('raw/Cian.xlsx', sheet_name='03-complex')
    true_column = pd.Index(['lat', 'lng', 'Площадь К', 'ID К'], dtype='object')
    df_res = np.concatenate((df3[true_column].to_numpy(), df_res), axis=0)

    df4 = pd.read_excel('raw/Cian.xlsx', sheet_name='04_placement')
    true_column = pd.Index(['lat', 'lng', 'Площадь', 'Оценка цены', ], dtype='object')
    df_res = np.concatenate((df4[true_column].to_numpy(), df_res), axis=0)

    df6 = pd.read_excel('raw/Cian.xlsx', sheet_name='06-price-cian')
    true_column = pd.Index(['geo_lat', 'geo_lng', 'livingarea', 'bargainterms_price', ], dtype='object')
    df_res = np.concatenate((df6[true_column].to_numpy(), df_res), axis=0)

    df = pd.DataFrame(df_res, columns=['lat', 'lng', 'area', 'cost'])  # index=range(df_res.shape[0]),
    df.to_csv('worker_data/data.csv', index=False)


def get_csv_from_input():
    df = pd.read_excel('input_example/data.xlsx')
    df['lat'] = 55.721265
    df['lng'] = 37.454753
    df['area'] = df['Площадь квартиры, кв.м']
    df = df[['lat', 'lng', 'area']]
    df.to_csv('worker_data/input_data.csv', index=False)


def main():
    get_csv_from_input()
    #get_data_from_cian()


if __name__ == "__main__":
    main()
