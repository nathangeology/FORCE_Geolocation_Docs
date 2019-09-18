import pandas as pd
import geopandas as gpd

if __name__ == "__main__":
    npd_data = pd.read_csv('sample_data/with-coordinates.csv', delimiter=';')
    # npd_data.set_index(['wlbWellboreName'], drop=False)

    fields_test = gpd.read_file('sample_data/shapefiles/loc_npd_fields.shp')
    print('here')