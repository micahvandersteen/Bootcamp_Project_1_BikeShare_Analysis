import geopandas as gpd
import numpy as np
import pandas as pd


# # Read in the shapefiles of city census tracts ( with their geometry)
m_census_gdf = gpd.read_file("Census_subsets/Mpls_CensusTracts.shp")
# # convert the GEOID field to an integer for merging later
m_census_gdf = m_census_gdf.astype({'GEOID': 'int64'})
# b_census_gdf = gpd.read_file("Census_subsets/Bos_CensusTracts.shp")
# b_census_gdf = b_census_gdf.astype({'GEOID': 'int64'})
# p_census_gdf = gpd.read_file("Census_subsets/Por_CensusTracts.shp")
# p_census_gdf = p_census_gdf.astype({'GEOID': 'int64'})

# # Read in the ACS census data from the census api
m_census_df = pd.read_csv('census_output/m_census.csv', index_col=0)
# b_census_df = pd.read_csv('census_output/b_census.csv', index_col=0)
# p_census_df = pd.read_csv('census_output/p_census.csv', index_col=0)

# # Read in the bike trips info
m_bike_df = pd.read_csv('census_output/m_bike.csv', index_col=0)
m_bike_df = m_bike_df.rename(columns={"start station longitude":"s_longitude", "start station latitude":"s_latitude",
    "end station longitude":"e_longitude", "end station latitude":"e_latitude"})
# b_bike_df = pd.read_csv('census_output/b_bike.csv', index_col=0)
# p_bike_df = pd.read_csv('census_output/p_bike.csv', index_col=0)


# # Merge the census api data to the census geometry data
m_merged = m_census_gdf.merge(m_census_df, on='GEOID')


# # Create geo dfs from the city bike data
m_bike_gdf = gpd.GeoDataFrame(
    m_bike_df, geometry=gpd.points_from_xy(m_bike_df.s_longitude, m_bike_df.s_latitude))

# Warning---- takes a long time to run!!!!!
# Satial join
# m_sjoin = gpd.sjoin(m_merged, m_bike_gdf, how="inner", op='intersects')
# m_sjoin.to_csv('census_output/m_sjoin.csv')

print("Success!")
