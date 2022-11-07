from sklearn.neighbors import KNeighborsRegressor
import pandas as pd

def get_neib(k_neib = 10):
    df_cian = pd.read_csv('database/worker_data/data.csv')
    df_input = pd.read_csv('database/worker_data/input_data.csv')
    df_cian = df_cian[df_cian.notna()]
    df_cian = df_cian.fillna(method="pad")
    X = df_cian[["lat", "lng", "area"]]
    y = df_cian["cost"]
    neigh = KNeighborsRegressor(n_neighbors=k_neib)
    neigh.fit(X, y)
    k_n = neigh.kneighbors(df_input)
    return df_cian[:len(k_n)], k_n


def main():
    pass

if __name__ == "__main__":
    main()
