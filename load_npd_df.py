import pandas as pd

if __name__ == "__main__":
    npd_data = pd.read_csv('sample_data/with-coordinates.csv', delimiter=';')
    npd_data.set_index(['wlbWellboreName'], drop=False)
    print('here')